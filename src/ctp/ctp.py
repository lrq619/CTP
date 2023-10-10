import grpc
import concurrent.futures as futures

from .run import Run
from .ctp_grpc import ctp_pb2
from .ctp_grpc import ctp_pb2_grpc
from .utils import logger

class CtpService(ctp_pb2_grpc.CtpServiceServicer):
    
    def AppendRun(self, request, context):
        # Implement the logic for AppendRun here

        return ctp_pb2.AppendRunResponse(run_id=1)  # Sample response

    def GetRun(self, request, context):
        # Implement the logic for GetRun here
        return ctp_pb2.GetRunResponse(run_id=2)  # Sample response

def start_listen(ip : str = "localhost", port : int = 50057) -> None:
    # Create a gRPC server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the implemented service with the server
    ctp_pb2_grpc.add_CtpServiceServicer_to_server(CtpService(), grpc_server)

    # Start the server
    grpc_server.add_insecure_port(f"{ip}:{port}")
    logger.info(f"Starting server on {ip}:{port}")
    grpc_server.start()

    # Keep the server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        grpc_server.stop(0)

def start_collect(exp_label : str, ip : str = "localhost", port : int = 50057) -> Run:
    return Run()

def stop_collect() -> None:
    pass

def start_process(exp_label : str, exp_id : int = -1, ip : str = "localhost", port : int = 50057) -> Run:
    pass