# CTP
A python data collection library 
## Usage:
```python
pip install ctp
```
### Server:
To start a server locally:
```python
import ctp
ctp.start_listen(ip = "localhost", port=50057)
```
### Collect:
Example usage of collecting data and transfer it to server:
```python
import ctp
run = ctp.start_collect(exp_label="sample_exp", ip="localhost", port=50057)
```
This appends a new run of the experiment, to collect data to new run:
```python
sample_data = run.collect(data_label = "sample_data")
for i in range(10):
    sample_data.append(i)
```
Or you can also pass a list created by yourself by:
```python
sample_data = [] # sample data list created by your self
run.monitor(data_label = "sample_data", value = sample_data)
for i in range(10):
    sample_data.append(i)
```
After collecting data, finish collect and upload all data to server:
```python
run.stop_collect()
```

### Process
To process data from other machines:
```python
import ctp
run = ctp.start_process(exp_label="sample_exp", tag = "lastest", ip="localhost", port=50057)
```
get sample data:
```python
sample_data = run.process(data_label="sample_data")
```
## API
### ctp
```python
def start_listen(ip : str = "localhost", port : int = 50057) -> None:

def start_collect(exp_label : str, ip : str = "localhost", port : int = 50057) -> ctp.Run:

def stop_collect() -> None:

def start_process(exp_label : str, tag : str = "latest", ip : str = "localhost", port : int = 50057) -> ctp.Run:
```
### ctp.Run:
```python
def collect(self, data_label : str) -> List[any]:

def monitor(self, data_label : str, value : List[any]) -> None:

def process(self, data_label : str) -> List[any]:
```
