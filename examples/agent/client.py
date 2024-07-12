#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a remote agent. 

# You can interact with this via API directly



import requests

inputs = {"input": {"input": "what does eugene think of cats?"}}
response = requests.post("http://localhost:8000/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



await remote_runnable.ainvoke({"input": "hi!"})




remote_runnable.invoke({"input": "what does eugene think of cats?"})


# ## Stream
# 
# Please note that streaming alternates between actions and observations. It does not stream individual tokens! If you need to stream individual tokens you will need to use astream_log!



async for chunk in remote_runnable.astream({"input": "what does eugene think of cats? Then tell me a story about that thought."}):
    print('--')
    print(chunk)


# ## Stream Events
# 
# The client is looking for a runnable name called `agent` for the chain events. This name was defined on the server side using `runnable.with_config({"run_name": "agent"}`



async for event in remote_runnable.astream_events(
    {"input": "what does eugene think of cats? Then tell me a story about that thought."},
    version="v1",
):
    kind = event["event"]
    if kind == "on_chain_start":
        if (
            event["name"] == "agent"
        ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
            print(
                f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
            )
    elif kind == "on_chain_end":
        if (
            event["name"] == "agent"
        ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
            print()
            print("--")
            print(
                f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
            )
    if kind == "on_chat_model_stream":
        content = event["data"]["chunk"].content
        if content:
            # Empty content in the context of OpenAI means
            # that the model is asking for a tool to be invoked.
            # So we only print non-empty content
            print(content, end="|")
    elif kind == "on_tool_start":
        print("--")
        print(
            f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
        )
    elif kind == "on_tool_end":
        print(f"Done tool: {event['name']}")
        print(f"Tool output was: {event['data'].get('output')}")
        print("--")


# ## Stream log
# 
# If you need acccess the individual llm tokens from an agent use `astream_log`. Please make sure that you set **streaming=True** on your LLM (see server code). For this to work, the LLM must also support streaming!



async for chunk in remote_runnable.astream_log({"input": "what does eugene think of cats?"}):
    print('--')
    print(chunk)

