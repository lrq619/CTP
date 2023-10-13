from .run import Run, RunStatus
from typing import List

MAXRUNS = 20

class Experiment:
    def __init__(self, exp_name : str) -> None:
        self.exp_name : str = exp_name
        self.runs : WrapRuns = WrapRuns(MAXRUNS) 
        self.latest_run_id : int = -1

    def append_run(self) -> int:
        self.latest_run_id += 1
        new_run = Run(exp_name=self.exp_name, run_id = self.latest_run_id, status=RunStatus.ONCLOUD)
        self.runs.append(new_run)
        return self.latest_run_id


    def get_latest_run_id(self):
        return self.latest_run_id

    def get_run(self, run_id) -> Run:
        return self.runs.get_run(run_id)

    def get_latest_run(self) -> Run:
        return self.runs.get_run(self.latest_run_id)


class WrapRuns:
    def __init__(self, length : int) -> None:
        assert length > 0
        self.runs : List[Run] = [None for _ in range(length)]
        self.next_pos = 0
        self.length = length
    
    def append(self, run : Run):
        self.runs[self.next_pos] = run
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