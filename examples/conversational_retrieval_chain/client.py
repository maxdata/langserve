#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a remote conversational retrieval chain. 

# You can interact with this via API directly



import requests

inputs = {"input": {"question": "what do you know about harrison", "chat_history": []}}
response = requests.post("http://localhost:8000/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



await remote_runnable.ainvoke({"question": "what do you know about harrison", "chat_history": []})




await remote_runnable.ainvoke(
    {"question": "what do you know about harrison", "chat_history": [("hi", "hi")]}
)




async for chunk in remote_runnable.astream(
    {"question": "what do you know about harrison", "chat_history": [("hi", "hi")]}
):
    print(chunk)


# stream log shows all intermediate steps as well!



async for chunk in remote_runnable.astream_log(
    {"question": "what do you know about harrison", "chat_history": [("hi", "hi")]}
):
    print(chunk)

