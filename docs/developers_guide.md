# Developers Guide
First install all required packages by:
```
pip install -r requirements.txt
```
or
```
conda craete --name ctp --file requirements.txt
```

## Architecture
CTP uses architecture of: Experiment -> Run -> Record
Now it uses a dict in the memory to store all records, future it will be changed to a database

# Run and Record
In each run, `Records` are stored in the format of key-val pairs in a dict. 

`Record` are pairs of `label` : str, and  `datas` : List[]  

`label` are composed of `prefix`+`user_label`, where `prefix` is the CTP system's prefix, default prefix is `'_'`, `user_label` is the string passed when Run.collect(`user_label`) or Run.monitor(`user_label`) is invoked.

Both Run.collect(`user_label`) and Run.monitor(`user_label`) will check whether the given `label` is already in Run, and both of them would create a new `Record` with corresponding `label` if it's not. Run.collect() will return the newly created `Record.datas` as a reference which can be further operated. However, if there is already a `Record` in `Run`, Run.collect() and Run.monitor() deals it differently: Run.collect() would simply return the current `Record.datas` but Run.monitor() would throw out an error. 

When Run.stop_collect() is invoked, it will upload the collected records to the cloud server.

When Run.process(`user_label`) is invoked, the input `user_label` would be concactaned behind the default `prefix` if the prefix is not specified by user. 
