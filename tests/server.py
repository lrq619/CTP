import sys
import os
import random
import time
import ctp

ip = "localhost"
port = 50057

class StartServer:
    def __init__(self, ip : str = "localhost", port : int = 50057) -> None:
        self.ip = "localhost"
        self.port = port

    def __enter__(self):
        ctp.start_listen(self.ip, self.port) 
        time.sleep(0.5)
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        ctp.stop_listen()

if __name__ == "__main__":
    with StartServer():
        pass