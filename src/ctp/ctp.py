import grpc
import concurrent.futures as futures
import pickle

from .run import Run
from .ctp_grpc import ctp_pb2
from .ctp_grpc import ctp_pb2_grpc
from .utils import logger
from .manager import Manager


manager = Manager()

class CtpService(ctp_pb2_grpc.CtpServiceServicer):
    
    def AppendRun(self, request, context):
        # Implement the logic for AppendRun here
        exp_name = request.exp_name
        run_id = manager.append_run(exp_name=exp_name)
        return ctp_pb2.AppendRunResponse(run_id=run_id)  

    def GetRun(self, request, context):
        # Implement the logic for GetRun here
        exp_name = request.exp_name
        run_id = request.run_id
        run = manager.get_run(exp_name=exp_name, run_id=run_id)
        run_bytes = pickle.dumps(run)
        return ctp_pb2.GetRunResponse(run_bytes=run_bytes)  

    
    def SyncRecords(self, request, context):
        exp_name = request.exp_name
        run_id = request.run_id
        records_bytes = request.records
        records = pickle.loads(records_bytes)

        successful_labels = manager.sync(exp_name, run_id, records)
        logger.debug(f"sync on {exp_name}:{run_id} with {len(records.keys())} succeeds on {len(successful_labels)} labels")

        return ctp_pb2.SyncRecordsResponse(successful_labels = successful_labels)

def init_grpc_server(ip : str = "localhost", port : int = 50057) -> any:

    # Create a gRPC server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the implemented service with the server
    ctp_pb2_grpc.add_CtpServiceServicer_to_server(CtpService(), grpc_server)

    # Start the server
    grpc_server.add_insecure_port(f"{ip}:{port}")
    logger.info(f"Starting server on {ip}:{port}")
    return grpc_server
    

def start_listen(ip : str = "localhost", port : int = 50057) -> None:
    grpc_server = init_grpc_server(ip=ip, port=port)
    grpc_server.start()
    # Keep the server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        grpc_server.stop(0)

def start_collect(exp_label : str, ip : str = "localhost", port : int = 50057) -> Run:
    return Run()


def start_process(exp_label : str, exp_id : int = -1, ip : str = "localhost", port : int = 50057) -> Run:
    pass