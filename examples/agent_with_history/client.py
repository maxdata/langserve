#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of a client interacting with a remote agent that can use history.
# 
# See relevant documentation about agents:
# 
# * Creating a custom agent: https://python.langchain.com/docs/modules/agents/how_to/custom_agent
# * Streaming with agents: https://python.langchain.com/docs/modules/agents/how_to/streaming#custom-streaming-with-events
# * General streaming documentation: https://python.langchain.com/docs/expression_language/streaming

# You can interact with this via API directly



import requests

inputs = {"input": {"input": "what is the length of the word audioee?", "chat_history": []}}
response = requests.post("http://localhost:8000/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/")


# Remote runnable has the same interface as local runnables



from langchain_core.messages import HumanMessage, AIMessage




chat_history = []

while True:
    human = input("Human (Q/q to quit): ")
    if human in {"q", "Q"}:
        print('AI: Bye bye human')
        break
    ai = await remote_runnable.ainvoke({"input": human, "chat_history": chat_history})
    print(f"AI: {ai['output']}")
    chat_history.extend([HumanMessage(content=human), AIMessage(content=ai['output'])])


# ## Stream
# 
# Please note that streaming alternates between actions and observations. It does not stream individual tokens!
# 
# To stream individual tokens, we need to use the astream events endpoint (see below).



chat_history = []

while True:
    human = input("Human (Q/q to quit): ")
    if human in {"q", "Q"}:
        print('AI: Bye bye human')
        break

    ai = None
    print("AI: ")
    async for chunk in remote_runnable.astream({"input": human, "chat_history": chat_history}):
        # Agent Action
        if "actions" in chunk:
            for action in chunk["actions"]:
                print(
                    f"Calling Tool ```{action['tool']}``` with input ```{action['tool_input']}```"
                )
        # Observation
        elif "steps" in chunk:
            for step in chunk["steps"]:
                print(f"Got result: ```{step['observation']}```")
        # Final result
        elif "output" in chunk:
            print(chunk['output'])
            ai = AIMessage(content=chunk['output'])
        else:
            raise ValueError
        print("------")        
    chat_history.extend([HumanMessage(content=human), ai])


# ## Stream Events



chat_history = []

while True:
    human = input("Human (Q/q to quit): ")
    if human in {"q", "Q"}:
        print('AI: Bye bye human')
        break
    ai = None
    print("AI: ")
    async for event in remote_runnable.astream_events(
        {"input": human, "chat_history": chat_history},
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

