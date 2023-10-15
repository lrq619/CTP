import sys
import os
import random
import time

# Append the path of the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import ctp
from server import StartServer

ip = "0.0.0.0"
port = 50057


exp_name = "sample_project"
heights = [i * 10 for i in range(10)] 
label = "height"


def test_collect(capfd):
    with StartServer(): 
        with ctp.append_run(exp_name) as run:
            assert run.run_id == 0
            out ,err = capfd.readouterr()
            assert "Append run success, current run" in out 
            for i, height in enumerate(heights):
                run.collect(label, height)



def test_collect_then_process():
    with StartServer():
        with ctp.append_run(exp_name) as run:
            assert run.run_id == 0
            for i, height in enumerate(heights):
                run.collect(label, height)

        time.sleep(1) 

        run = ctp.get_run(exp_name)
        _heights = run.process(label)
        assert _heights == heights


def test_monitor():
    with StartServer():
        with ctp.append_run(exp_name) as run:
            assert run.run_id == 0
            run.monitor(label, heights)
            e = random.randint(160,240)
            heights.append(e)

        time.sleep(1)

        run = ctp.get_run(exp_name)
        _heights = run.process(label)
        assert _heights[-1] == e 

def test_multiple_runs():
    with StartServer():
        run_iterations = len(heights)
        for i in range(run_iterations):
            with ctp.append_run(exp_name) as run:
                assert run.run_id == i
                run.collect(label, heights[i])

        time.sleep(1)
        latest_run = ctp.get_run(exp_name)
        assert latest_run.process(label) == [heights[-1]]
        for i in range(run_iterations):
            run = ctp.get_run(exp_name,i)
            assert run.process(label) == [heights[i]]
        


        
    
