#!/usr/bin/env python
# coding: utf-8

# # Passthrough information
# 
# An example that shows how to pass through additional info with the request, and get it back with the response.



from langchain.prompts.chat import ChatPromptTemplate




from langserve import RemoteRunnable

chain = RemoteRunnable("http://localhost:8000/v1/")


# Let's create a prompt composed of a system message and a human message.



chain.invoke({'thing': 'apple', 'language': 'italian', 'info': {"user_id": 42, "user_info": {"address": 42}}})




for chunk in chain.stream({'thing': 'apple', 'language': 'italian', 'info': {"user_id": 42, "user_info": {"address": 42}}}):
    print(chunk)




from langserve import RemoteRunnable

chain = RemoteRunnable("http://localhost:8000/v2/")




chain.invoke({'thing': 'apple', 'language': 'italian', 'info': {"user_id": 42, "user_info": {"address": 42}}})

