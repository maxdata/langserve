#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# This is an example client that interacts with the server that has "auth".
# 
# Please reference appropriate documentation in the server code and in FastAPI to actually make this secure.
# 
# 
# **ATTENTION** Only the invoke endpoint has been defined by the server! 
# So batch/stream won't work. If you want to add stream and batch, you can do so as well on the server side.
# The server is implemented using the APIHandler, it's more flexible, but does require a bit more code. :)

# ## Login as Alice



import requests

response = requests.post("http://localhost:8000/token", data={"username": "alice", "password": "secret1"})
result = response.json()




token = result['access_token']




inputs = {"input": "hello"}
response = requests.post("http://localhost:8000/my_runnable/invoke", 
    json={
        'input': 'hello',
    },
    headers={
        'Authorization': f"Bearer {token}"
    }
)




response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/my_runnable", headers={"Authorization": f"Bearer {token}"})




await remote_runnable.ainvoke("cat")


# ## Login as John



import requests

response = requests.post("http://localhost:8000/token", data={"username": "john", "password": "secret2"})
token = response.json()['access_token']
remote_runnable = RemoteRunnable("http://localhost:8000/my_runnable", headers={"Authorization": f"Bearer {token}"})




await remote_runnable.ainvoke("water")

