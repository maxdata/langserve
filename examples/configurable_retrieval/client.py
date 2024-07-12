#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a configurable retriever (see server code)

# You can interact with this via API directly



import requests

inputs = {"input": "cat"}
response = requests.post("http://localhost:8000/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



await remote_runnable.ainvoke("cat")




await remote_runnable.ainvoke("cat", {"configurable": {"collection_name": "Index 1"}})




await remote_runnable.ainvoke("cat", {"configurable": {"collection_name": "Index 2"}})

