import sys
import os
import random
import time
from threading import Thread

import ctp
from server import StartServer

ip = "0.0.0.0"
port = 50057

def test_server(capfd):
    with StartServer():
        pass