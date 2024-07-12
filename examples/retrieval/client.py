#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a remote retriever. 

# You can interact with this via API directly



import requests

inputs = {"input": "tree"}
response = requests.post("http://localhost:8000/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



await remote_runnable.ainvoke("tree")




remote_runnable.invoke("water")




await remote_runnable.abatch(["wolf", "tiger"])




remote_runnable.batch(["wood", "feline"])




async for chunk in remote_runnable.astream("ball"):
    print(chunk)




for chunk in remote_runnable.stream("ball"):
    print(chunk)

