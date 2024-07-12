#!/usr/bin/env python
# coding: utf-8

# # Chat History
# 
# An example of a client interacting with a chatbot where message history is persisted on the backend.



import uuid
from langserve import RemoteRunnable

chat = RemoteRunnable("http://localhost:8000/")


# Let's create a prompt composed of a system message and a human message.



session_id = str(uuid.uuid4())




chat.invoke({"human_input": "my name is eugene. i like cats. what is your name?"}, {'configurable': { 'session_id': session_id } })




chat.invoke({"human_input": "what was my name?"}, {'configurable': { 'session_id': session_id } })




chat.invoke({"human_input": "What animal do i like?"}, {'configurable': { 'session_id': session_id } })




for chunk in chat.stream({'human_input': "Can you count till 10?"},  {'configurable': { 'session_id': session_id } }):
    print()
    print(chunk.content, end='', flush=True)




get_ipython().system('cat chat_histories/c7a327f3-5578-4fb7-a8f2-3082d7cb58cc.json | jq .')

