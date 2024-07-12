#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Client code interacting with a server that implements: 
# 
# * custom streaming for an agent
# * agent with user selected tools
# 
# This agent does not have memory! See other examples in LangServe to see how to add memory.
# 
# **ATTENTION** We made the agent stream strings as an output. This is almost certainly not what you would want for your application. Feel free to adapt to return more structured output; however, keep in mind that likely the client can just use `astream_events`!
# 
# See relevant documentation about agents:
# 
# * Creating a custom agent: https://python.langchain.com/docs/modules/agents/how_to/custom_agent
# * Streaming with agents: https://python.langchain.com/docs/modules/agents/how_to/streaming#custom-streaming-with-events
# * General streaming documentation: https://python.langchain.com/docs/expression_language/streaming

# You can interact with this via API directly



word = "audioeeeeeeeeeee"
len(word)




import requests

inputs = {"input": {"input": f"what is the length of the word {word}?", "chat_history": [], "tools": []}}
response = requests.post("http://localhost:8000/invoke", json=inputs)

print(response.json()['output'])


# Let's provide it with a tool to test that tool selection works



import requests

inputs = {"input": {"input": f"what is the length of the word {word}?", "chat_history": [], "tools": ["word_length", "favorite_animal"]}}
response = requests.post("http://localhost:8000/invoke", json=inputs)

print(response.json()['output'])


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables

# ## Stream
# 
# Streaming output from a **CUSTOM STREAMING** implementation that streams string representations of intermediate steps. Please see server side implementation for details.



async for chunk in remote_runnable.astream({"input": "What is eugenes favorite animal?", "tools": ["word_length"]}):
    print(chunk, end='|', flush=True)




async for chunk in remote_runnable.astream({"input": "What is eugenes favorite animal?", "tools": ["word_length", "favorite_animal"]}):
    print(chunk, end='|', flush=True)

