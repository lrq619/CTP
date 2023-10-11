# This is the manager of Experiments and Run
from typing import List, Dict, TypeVar, Generic
from .run import Run
from .utils import logger

MAXRUNS = 20

class Manager:
    def __init__(self) -> None:
        self.experiments : Dict[str, Experiment] = {}

    def append_run(self, exp_name : str) -> int:
        if exp_name not in self.experiments.keys():
            self.experiments[exp_name] = Experiment(exp_name=exp_name)
        exp = self.experiments[exp_name]
        latest_run_id = exp.append_run() 
        logger.debug(f"manager appends a new run to experiment: {exp_name}, latest_run_id: {latest_run_id}") 
        return latest_run_id
        

    def get_run(self, exp_name : str, run_id : int) -> Run:
        try:
            exp = self.experiments[exp_name]
            run = exp.get_run(run_id)
            logger.debug(f"manager finds run_{run_id} for {exp_name}")
            return run
        except:
            logger.warning(f"manager cannot get run for: {exp_name}:{run_id}")
            return Run(-1)


    def sync(self, exp_name : str, run_id : int, records : Dict[str, List[any]]) -> List[str]:
        pass 


class Experiment:
    def __init__(self, exp_name : str) -> None:
        self.exp_name : str = exp_name
        self.runs : WrapRuns = WrapRuns(MAXRUNS) 
        self.latest_run_id : int= -1

    def append_run(self) -> int:
        self.latest_run_id += 1
        new_run = Run(self.latest_run_id)
        self.runs.append(new_run)
        return self.latest_run_id


    def get_latest_run_id(self):
        return self.latest_run_id

    def get_run(self, run_id) -> Run:
        self.runs.get_run(run_id)


class WrapRuns:
    def __init__(self, length : int) -> None:
        assert length > 0
        self.runs : List[Run] = [None for _ in range(length)]
        self.next_pos = 0
        self.length = length
    
    def append(self, run : Run):
        self._list[self.next_pos] = run
        self.next_pos += 1
        if self.next_pos >= self.length:
            self.next_pos = 0

    def get_latest_run(self) -> Run:
        latest_pos = self.next_pos - 1
        if latest_pos < 0:
            latest_pos = 0
        return self.runs[latest_pos]

    def get_run(self, run_id : int) -> Run:
        for run in self.runs:
            if run.run_id == run_id:
                return run
        raise ValueError(f"Cannot find run_id {run_id}")
        

