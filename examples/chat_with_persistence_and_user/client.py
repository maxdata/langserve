#!/usr/bin/env python
# coding: utf-8

# # Chat History
# 
# Here we'll be interacting with a server that's exposing a chat bot with message history being persisted on the backend.



import uuid
from langserve import RemoteRunnable

conversation_id = str(uuid.uuid4())
chat = RemoteRunnable("http://localhost:8000/", cookies={"user_id": "eugene"})


# Let's create a prompt composed of a system message and a human message.



chat.invoke({"human_input": "my name is eugene. what is your name?"}, {'configurable': { 'conversation_id': conversation_id } })




chat.invoke({"human_input": "what was my name?"}, {'configurable': { 'conversation_id': conversation_id } })


# Use different user but same conversation id



chat = RemoteRunnable("http://localhost:8000/", cookies={"user_id": "nuno"})




chat.invoke({"human_input": "what was my name?"}, {'configurable': { 'conversation_id': conversation_id }})




for chunk in chat.stream({'human_input': "Can you count till 10?"},  {'configurable': { 'conversation_id': conversation_id } }):
    print()
    print(chunk.content, end='', flush=True)




conversation_id




get_ipython().system('tree chat_histories/')




get_ipython().system('cat chat_histories/eugene/cd8e5a55-0295-41cd-a885-775e0403fd25.json | jq .')




get_ipython().system('cat chat_histories/nuno/cd8e5a55-0295-41cd-a885-775e0403fd25.json | jq .')

