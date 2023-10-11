from typing import List, Optional, Dict
from .utils import can_append, get_type
class Run:
    
    def __init__(self, run_id : int = -1) -> None:
        self.run_id : int = run_id
        self.records : Dict[str, List[any]] = {}
        self.tag = ""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_collect()



    def collect(self, user_label : str, data : any = None, prefix : str = '_') -> List[any]:
        label = prefix + user_label
        if label in self.records:
            datas = self.records[label]
            if data is None:
                return datas

            if not can_append(data, datas):
                raise ValueError(f"data's type: {type(data)}, records[{label}]'s type {get_type(datas)}")

            datas.append(data)
            return datas
        else:
            self.records[label] = []
            datas = self.records[label]
            if data is None:
                return datas

            datas.append(data)
            return datas  

    
    def monitor(self, user_label : str, datas : List[any], prefix : str = '_') -> None:
        label = prefix + user_label
        if label in self.records:
            raise ValueError(f"{label} already in the records, cannot monitor again")
        else:
            self.records[label] = datas


    def stop_collect(self):
        print(f"Run {self.run_id} stopped collecting...")

    def get_raw_records(self) -> Dict[str, List[any]]:
        return self.records

    def process(self, user_label, prefix = "_")->List[any] :
        label = prefix + user_label
        if label in self.records:
            datas = self.records[label]
            return datas
        raise ValueError(f"{label} not in the records")