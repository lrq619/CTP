import grpc
import concurrent.futures as futures
import pickle
import threading
import json
from typing import List, Dict

from .run import Run, RunStatus
from .ctp_grpc import ctp_pb2
from .ctp_grpc import ctp_pb2_grpc
from .utils import logger
from .manager import Manager
from .conf import *

stop_event = threading.Event()




class CtpService(ctp_pb2_grpc.CtpServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.manager = Manager()
    
    def AppendRun(self, request, context):
        # Implement the logic for AppendRun here
        exp_name = request.exp_name
        run_id = self.manager.append_run(exp_name=exp_name)
        return ctp_pb2.AppendRunResponse(run_id=run_id)  

    def GetRun(self, request, context):
        # Implement the logic for GetRun here
        exp_name = request.exp_name
        run_id = request.run_id
        run = self.manager.get_run(exp_name=exp_name, run_id=run_id)
        records_bytes = pickle.dumps(run.records)
        logger.debug(f"get run: {run}, send out {len(records_bytes) / 1024} KB data")

        run_id = run.run_id 
        return ctp_pb2.GetRunResponse(records_bytes=records_bytes, run_id = run_id)  

    
    def SyncRecords(self, request, context):
        exp_name = request.exp_name
        run_id = request.run_id
        records_bytes = request.records_bytes
        records = pickle.loads(records_bytes)

        successful_labels = self.manager.sync(exp_name, run_id, records)
        logger.debug(f"sync on [{exp_name}:{run_id}] with {len(records.keys())} succeeds on {len(successful_labels)} labels, recv bytes: {len(records_bytes)/1024} KB")

        return ctp_pb2.SyncRecordsResponse(successful_labels = successful_labels)

def init_grpc_server(ip : str = DEFAULT_IP, port : int = DEFAULT_PORT) -> any:

    # Create a gRPC server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the implemented service with the server
    ctp_pb2_grpc.add_CtpServiceServicer_to_server(CtpService(), grpc_server)

    # Start the server
    grpc_server.add_insecure_port(f"{ip}:{port}")
    logger.info(f"Starting server on {ip}:{port}")
    return grpc_server
    
def _server_run(ip: str, port: int) -> None:
    grpc_server = init_grpc_server(ip=ip, port=port)
    grpc_server.start()
    try:
        while not stop_event.is_set():
            stop_event.wait(1)
    except KeyboardInterrupt as e:
        logger.info("keyboard interrupt")
    finally:
        grpc_server.stop(0)

def start_listen(ip: str = DEFAULT_IP, port: int = DEFAULT_PORT) -> None:
    stop_event.clear()
    server_thread = threading.Thread(target=_server_run, args=(ip, port))
    server_thread.start()

def stop_listen() -> None:
    stop_event.set()

def append_run(exp_name : str, ip : str = DEFAULT_IP, port : int = DEFAULT_PORT) -> Run:
    try:
        options = [
                ('grpc.keepalive_time_ms', 30000),  # send keepalive ping every 30 seconds
                ('grpc.keepalive_timeout_ms', 10000),  # keepalive ping time out after 10 seconds
                ('grpc.keepalive_permit_without_calls', True),  # allow keepalive pings when there are no calls
                ('grpc.http2.min_time_between_pings_ms', 30000),  # minimum amount of time a ping would be sent without receiving any data frame
            ]
        channel = grpc.insecure_channel(f"{ip}:{port}", options=options)
        stub = ctp_pb2_grpc.CtpServiceStub(channel)
        request = ctp_pb2.AppendRunRequest(exp_name = exp_name)
        response = stub.AppendRun(request)
        run_id = response.run_id
        run = Run(exp_name, run_id, status=RunStatus.COLLECT)
        run.args["stub"] = stub
        print(f"Append run success, current run: {run}")
    except Exception as e:
        run = Run(exp_name, -1, status=RunStatus.OFFLINE)
        print(f"append a new run to expriment: {exp_name} failed! error: {e}")
    return run

def append_sync_run(exp_name : str, ip : str = DEFAULT_IP, port : int = DEFAULT_PORT) -> Run:
    try:
        options = [
                ('grpc.keepalive_time_ms', 30000),  # send keepalive ping every 30 seconds
                ('grpc.keepalive_timeout_ms', 10000),  # keepalive ping time out after 10 seconds
                ('grpc.keepalive_permit_without_calls', True),  # allow keepalive pings when there are no calls
                ('grpc.http2.min_time_between_pings_ms', 30000),  # minimum amount of time a ping would be sent without receiving any data frame
            ]
        channel = grpc.insecure_channel(f"{ip}:{port}", options=options)
        stub = ctp_pb2_grpc.CtpServiceStub(channel)
        request = ctp_pb2.AppendRunRequest(exp_name = exp_name)
        response = stub.AppendRun(request)
        run_id = response.run_id
        run = Run(exp_name, run_id, status=RunStatus.COLLECT)

        run_args = {
            "stub": stub,
            "sync": True
        }

        run.args = run_args

        print(f"Append sync run success, current run: {run}")
    except Exception as e:
        run = Run(exp_name, -1, status=RunStatus.OFFLINE)
        print(f"append a new run to expriment: {exp_name} failed! error: {e}")
    return run



def get_run(exp_name : str, run_id : int = -1, is_collect = False ,ip : str = DEFAULT_IP, port : int = DEFAULT_PORT) -> Run:
    try:
        options = [
                ('grpc.keepalive_time_ms', 30000),  # send keepalive ping every 30 seconds
                ('grpc.keepalive_timeout_ms', 10000),  # keepalive ping time out after 10 seconds
                ('grpc.keepalive_permit_without_calls', True),  # allow keepalive pings when there are no calls
                ('grpc.http2.min_time_between_pings_ms', 30000),  # minimum amount of time a ping would be sent without receiving any data frame
            ]
        channel = grpc.insecure_channel(f"{ip}:{port}", options=options)
        stub = ctp_pb2_grpc.CtpServiceStub(channel)
        request = ctp_pb2.GetRunRequest(exp_name = exp_name, run_id = run_id)
        response = stub.GetRun(request)
        records = pickle.loads(response.records_bytes)
        run_id = response.run_id
        if run_id < 0:
            return Run()
        run = Run(exp_name, run_id, status=RunStatus.PROCESS)
        
        if is_collect:
            run.status = RunStatus.COLLECT
            run.args["stub"] = stub
        run.records = records
        print(f"Get run success, current run: {run}")
    except Exception as e:
        run = Run(exp_name=exp_name)
        print(f"get a new run to experiment: {exp_name} failed! error: {e}")
    return run

def get_sync_run(exp_name : str, run_id : int = -1, is_collect = False ,ip : str = DEFAULT_IP, port : int = DEFAULT_PORT) -> Run:
    try:
        options = [
                ('grpc.keepalive_time_ms', 30000),  # send keepalive ping every 30 seconds
                ('grpc.keepalive_timeout_ms', 10000),  # keepalive ping time out after 10 seconds
                ('grpc.keepalive_permit_without_calls', True),  # allow keepalive pings when there are no calls
                ('grpc.http2.min_time_between_pings_ms', 30000),  # minimum amount of time a ping would be sent without receiving any data frame
            ]
        channel = grpc.insecure_channel(f"{ip}:{port}", options=options)
        stub = ctp_pb2_grpc.CtpServiceStub(channel)
        request = ctp_pb2.GetRunRequest(exp_name = exp_name, run_id = run_id)
        response = stub.GetRun(request)
        records = pickle.loads(response.records_bytes)
        run_id = response.run_id
        if run_id < 0:
            return Run()
        run = Run(exp_name, run_id, status=RunStatus.PROCESS)
        
        if is_collect:
            run.status = RunStatus.COLLECT
            run_args = {
                "stub": stub,
                "sync": True
            }

            run.args = run_args
        run.records = records
        print(f"Get run success, current run: {run}")
    except Exception as e:
        run = Run(exp_name=exp_name)
        print(f"get a new run to experiment: {exp_name} failed! error: {e}")
    return run