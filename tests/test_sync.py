import sys
import os
import random
import time

import ctp
from server import StartServer

ip = "0.0.0.0"
port = 50057


exp_name = "sample_project"
heights = [i * 10 for i in range(10)] 
label = "height"


def test_single_sync(capfd):
    with StartServer(): 
        run = ctp.append_sync_run(exp_name, ip=ip)
        assert run.run_id == 0
        out ,err = capfd.readouterr()
        assert "Append sync run success, current run" in out 
        height = 100
        run.collect(label, height)

        process_run = ctp.get_run(exp_name, ip=ip, run_id=0)
        _heights = process_run.process(label)
        assert height == _heights[0]

def test_array_sync(capfd):
    with StartServer():
        run = ctp.append_sync_run(exp_name, ip=ip)
        assert run.run_id == 0
        out ,err = capfd.readouterr()
        assert "Append sync run success, current run" in out 
        for i, height in enumerate(heights):
            run.collect(label, height)

            process_run = ctp.get_run(exp_name, ip=ip, run_id=0)
            _heights = process_run.process(label)
            assert _heights == heights[:i+1]
        
            