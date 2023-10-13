import sys
import os
import random
import time
from threading import Thread

# Append the path of the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import ctp
from server import StartServer

ip = "0.0.0.0"
port = 50057

def test_server(capfd):
    with StartServer():
        pass