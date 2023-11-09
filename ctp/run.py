from typing import List, Optional, Dict
from .utils import can_append, get_type
from .ctp_grpc import ctp_pb2
from .ctp_grpc import ctp_pb2_grpc

import pickle
from enum import Enum

class RunStatus(Enum):
    OFFLINE = 0 # The run is not connected to server 
    PROCESS = 1 # The run is currently processing data, cannot sync to cloud server, can only process data
    COLLECT = 2 # The run is currently collecting data, can sync to cloud server, and can also process data
    ONCLOUD = 3 # The run is currently stored on cloud, have all permissions

    def __str__(self) -> str:
        return super().__str__()

STATUS_STR = ["OFFLINE", "PROCESS", "COLLECT"]



class Run:
    
    def __init__(self, exp_name : str = "", run_id : int = -1, status : RunStatus = RunStatus.OFFLINE) -> None:
        self.exp_name : str = exp_name
        self.run_id : int = run_id
        self.records : Dict[str, List[any]] = {}
        self.status = status
        self.args = {} # used to store temporary objects
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_collect()

    def __str__(self) -> str:
        return f"[{self.exp_name}:run_{self.run_id}, status={self.status}]"

    def _sync(self):
        try:
            stub = self.args.get("stub", None)
            records_bytes = pickle.dumps(self.records)
            request = ctp_pb2.SyncRecordsRequest(exp_name = self.exp_name, run_id = self.run_id, records_bytes = records_bytes)
            response = stub.SyncRecords(request)
            print(f"{self} sync {len(response.successful_labels)} records to cloud server")
        except ValueError as e:
            print(f"This run is not connected to server! Cannot upload. error: {e}")

    def _clear_records(self):
        self.records = {}



    def print_records(self):
        print(f"{self.__str__()} has the following records:")
        print("-----------------------")
        for label in self.records.keys():
            print(f"{label}: {len(self.records[label])}")
        print("-----------------------")

    def collect(self, user_label : str, data : any = None, prefix : str = '_') -> List[any]:
        if self.status != RunStatus.COLLECT:
            return []
        label = prefix + user_label
        if label in self.records:
            datas = self.records[label]
            if data is None:
                return datas

            if not can_append(data, datas):
                raise ValueError(f"data's type: {type(data)}, records[{label}]'s type {get_type(datas)}")

            datas.append(data)
        else:
            self.records[label] = []
            datas = self.records[label]
            if data is None:
                return datas

            datas.append(data)
        sync = self.args.get("sync", False)
        if sync:
            self._sync()
            self._clear_records() # clear the records after sync
        return datas

    
    def monitor(self, user_label : str, datas : List[any], prefix : str = '_') -> None:
        if self.status != RunStatus.COLLECT:
            return []
        label = prefix + user_label
        if label in self.records:
            raise ValueError(f"{label} already in the records, cannot monitor again")
        else:
            self.records[label] = datas


    def stop_collect(self) -> None:
        if self.status != RunStatus.COLLECT:
            return

        if "stub" not in self.args.keys():
            return
        
        print(f"{self} stopped collecting...")
        sync = self.args.get("sync", False)

        # if not sync every collect, sync at the end
        if not sync:
            self._sync()


    def get_raw_records(self) -> Dict[str, List[any]]:
        return self.records

    def process(self, user_label, prefix = "_")->List[any] :
        if self.status == RunStatus.OFFLINE:
            return []
        label = prefix + user_label
        if label in self.records:
            datas = self.records[label]
            return datas
        raise ValueError(f"{label} not in the records")
