# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctp_pb2 as ctp__pb2


class CtpServiceStub(object):
    """Service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AppendRun = channel.unary_unary(
                '/ctp.CtpService/AppendRun',
                request_serializer=ctp__pb2.AppendRunRequest.SerializeToString,
                response_deserializer=ctp__pb2.AppendRunResponse.FromString,
                )
        self.GetRun = channel.unary_unary(
                '/ctp.CtpService/GetRun',
                request_serializer=ctp__pb2.GetRunRequest.SerializeToString,
                response_deserializer=ctp__pb2.GetRunResponse.FromString,
                )


class CtpServiceServicer(object):
    """Service definition
    """

    def AppendRun(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRun(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CtpServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AppendRun': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendRun,
                    request_deserializer=ctp__pb2.AppendRunRequest.FromString,
                    response_serializer=ctp__pb2.AppendRunResponse.SerializeToString,
            ),
            'GetRun': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRun,
                    request_deserializer=ctp__pb2.GetRunRequest.FromString,
                    response_serializer=ctp__pb2.GetRunResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ctp.CtpService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CtpService(object):
    """Service definition
    """

    @staticmethod
    def AppendRun(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ctp.CtpService/AppendRun',
            ctp__pb2.AppendRunRequest.SerializeToString,
            ctp__pb2.AppendRunResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRun(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ctp.CtpService/GetRun',
            ctp__pb2.GetRunRequest.SerializeToString,
            ctp__pb2.GetRunResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
