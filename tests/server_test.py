import sys
import os

# Append the path of the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ctp import start_listen
start_listen()