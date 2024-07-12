#!/usr/bin/env python
# coding: utf-8

# # Local LLM
# 
# Here, we'll use a server that's serving a local LLM.
# 
# **Attention** This is OK for prototyping / dev usage, but should not be used for production cases when there might be concurrent requests from different users. As of the time of writing, Ollama is designed for single user and cannot handle concurrent requests see this issue: https://github.com/ollama/ollama/issues/358



from langchain.prompts.chat import ChatPromptTemplate




from langserve import RemoteRunnable

model = RemoteRunnable("http://localhost:8000/ollama/")


# Let's test out the standard interface of a chat model.



prompt = "Tell me a 3 sentence story about a cat."




model.invoke(prompt)




await model.ainvoke(prompt)


# Batched API works, but b/c ollama does not support parallelism, it's no faster than using .invoke twice.



get_ipython().run_cell_magic('time', '', 'model.batch([prompt, prompt])\n')




get_ipython().run_cell_magic('time', '', 'for _ in range(2):\n    model.invoke(prompt)\n')




await model.abatch([prompt, prompt])


# Streaming is available by default



for chunk in model.stream(prompt):
    print(chunk.content, end="|", flush=True)




async for chunk in model.astream(prompt):
    print(chunk.content, end="|", flush=True)


# And so is the event stream API



i = 0
async for event in model.astream_events(prompt, version='v1'):
    print(event)
    if i > 10:
        print('...')
        break
    i += 1

