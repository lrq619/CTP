import sys
import os
import random

# Append the path of the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import ctp

ip = "localhost"
port = 50057

class StartServer:
    def __init__(self, ip : str = "localhost", port : int = 50057) -> None:
        self.ip = "localhost"
        self.port = port

    def __enter__(self):
        ctp.start_listen(self.ip, self.port) 

    def __exit__(self, exc_type, exc_val, exc_tb):
        ctp.stop_listen()

if __name__ == "__main__":
    with StartServer():
        pass