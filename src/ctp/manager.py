# This is the manager of Experiments and Run
from typing import List, Dict, TypeVar, Generic
from .run import Run
from .experiment import Experiment
from .utils import logger


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
            if run_id == -1:
               return exp.get_latest_run() 
            run = exp.get_run(run_id)
            logger.debug(f"manager finds {run}")
            return run
        except:
            logger.warning(f"manager cannot get run for: [{exp_name}:{run_id}]")
            return Run()


    def sync(self, exp_name : str, run_id : int, records : Dict[str, List[any]]) -> List[str]:
        try:
            exp = self.experiments[exp_name]
            run = exp.get_run(run_id)
            logger.debug(f"manager starts sync on {run}")
            for label in records.keys():
                if label not in run.records:
                    run.records[label] = records[label]
                else:
                    run.records[label] += records[label]
            return records.keys()
        except Exception as e:
            logger.warning(f"manager cannot sync run for [{exp_name}:{run_id}], error: {e}")


        

