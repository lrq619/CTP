# CTP
Collect Then Process: A python data collection library 

What do you need to do if you are running some programs on the remote server and you want to collect some runtime data during program running, and process it on your local PC, e.g. plot a figure? See how many steps you need without ctp:
* collect the data
* serialize the data
* download the data to your local computer through various ways: scp, ftp ...
* deserialize the data on your local computer
* process the data, e.g plot a figure

Tired of all this? ctp now provides a easy to use solution of just Collect then Process:

Collect on the remote cloud server:
```python
import ctp
with ctp.append_run("my_experiment") as run:
    run.collect("my_data", data)
```
Then Process on your local computer:
```python
import ctp
with ctp.get_run("my_experiment") as run:
    data = run.process("my_data")
```
## Usage:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cthenp
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
run = ctp.append_run("sample_exp")
```
This appends a new run of the experiment, to collect data to new run:
```python
for i in range(10):
    run.collect("sample_data")
```
Or you can also pass a list created by yourself by:
```python
sample_data = [] # sample data list created by your self
run.monitor("sample_data", sample_data)
for i in range(10):
    sample_data.append(i)
```
After collecting data, finish collect and upload all data to server:
```python
run.stop_collect()
```
If you don't want to deal with start and stop by your self, you can:
```python
with ctp.append_run("sample_exp") as run:
    ... ## your code here
```
will automatically upload all data once this block is finished

### Process
To process data from other machines:
```python
import ctp
run = ctp.get_run("sample_exp")
```
get sample data:
```python
sample_data = run.process("sample_data")
```
## API
### ctp
```python
def start_listen(ip : str = "localhost", port : int = 50057) -> None:

def append_run(exp_name : str, ip : str = "localhost", port : int = 50057) -> ctp.Run:


def get_run(exp_name : str, ip : str = "localhost", port : int = 50057) -> ctp.Run:
```
### ctp.Run:
```python
def collect(self, user_label : str, data : any = None, prefix : str = '_') -> List[any]:

def monitor(self, user_label : str, datas : List[any], prefix : str = '_') -> None:

def stop_collect() -> None:

def process(self, user_label : str = None) -> Optional[dict[str,List[any]],List[any]]:
```
