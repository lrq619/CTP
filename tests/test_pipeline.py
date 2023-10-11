import sys
import os
import random

# Append the path of the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ctp import start_listen, start_collect

heights = [random.randint(160,240) for i in range(10)] 
label = "height"

def test_collect_then_process():
    with start_collect("sample_project") as run:
        for i, height in enumerate(heights):
            run.collect(label, height)
            _heights = run.process(label)
            assert _heights == heights[:i+1]
        assert _heights == heights