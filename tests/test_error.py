import sys
import os
import random
import time

import ctp
from server import StartServer

ip = "0.0.0.0"
err_ip = "00.0.0.0"
port = 50057


exp_name = "sample_project"
heights = [random.randint(160,240) for i in range(10)] 
label = "height"

"""
Error operations that shoulde be handled, but would not affect the main program
"""
def test_error_collect(capfd):
    with StartServer():
        with ctp.append_run(exp_name, err_ip) as run:
            assert run.run_id == -1
            assert run.status == ctp.RunStatus.OFFLINE
            for i, height in enumerate(heights):
                run.collect(label, height)


def test_error_pipeline(capfd):
    with StartServer():
        with ctp.append_run(exp_name, err_ip) as run:
            assert run.run_id == -1
            assert run.status == ctp.RunStatus.OFFLINE
            for i, height in enumerate(heights):
                run.collect(label, height)

        time.sleep(1)
        run = ctp.get_run(exp_name, ip=ip)
        assert run.run_id == -1
        assert run.status == ctp.RunStatus.OFFLINE

def test_error_sync(capfd):
    with StartServer():
        with ctp.append_run(exp_name, ip=ip) as run:
            assert run.run_id == 0
            assert run.status == ctp.RunStatus.COLLECT
            run.monitor(label, heights)

        time.sleep(1)
        run = ctp.get_run(exp_name, ip=ip)
        assert run.run_id == 0
        assert run.status == ctp.RunStatus.PROCESS
        e = 250
        run.collect(label, e)
        run.stop_collect()

        run = ctp.get_run(exp_name, ip=ip)
        assert run.run_id == 0
        assert run.status == ctp.RunStatus.PROCESS
        _heights = run.process(label)
        assert _heights == heights
        