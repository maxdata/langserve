#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a custom runnable executor that supports configuration.
# 
# This server does not support invoke or batch! only stream and astream log! (see backend code.)
# 
# The underlying backend code is just a demo in this case -- it's working around an existing bug, but uses 
# the opportunity to show how to create custom runnables.

# You can interact with this via API directly



import requests

inputs = {"input": {"input": "what does eugene think of cats?"}}
response = requests.post("http://localhost:8000/stream", json=inputs)

print(response.text)


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



async for chunk in remote_runnable.astream({"input": "hi!"}):
    print(chunk)




async for chunk in remote_runnable.astream_log({"input": "what does eugene think about cats?"}):
    print(chunk)




async for chunk in remote_runnable.astream_log({"input": "what does eugene think about cats?"}, include_names=["LLM"]):
    print(chunk)

