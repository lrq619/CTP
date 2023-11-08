import sys
import os
import random
import time
from threading import Thread

import ctp
from server import StartServer

list_length = 1000
ip = "localhost"
exp_name = "stress_exp"

x = [i for i in range(list_length)]
y = [i for i in range(list_length)]
z = [z for z in range(list_length)]

def test_stress():
    with StartServer():
        with ctp.append_run(exp_name,ip=ip) as run:
            run.monitor("x", x)
            run.monitor("y", y)
            run.monitor("z", z)

        run = ctp.get_run(exp_name, ip=ip)
        _x = run.process("x")
        _y = run.process("y")
        _z = run.process("z")

        assert _x == x
        assert _y == y
        assert _z == z