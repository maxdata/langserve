#!/usr/bin/env python
# coding: utf-8

# # LLMs
# 
# Here we'll be interacting with a server that's exposing 2 LLMs via the runnable interface.



from langchain.prompts.chat import ChatPromptTemplate




from langserve import RemoteRunnable

openai_llm = RemoteRunnable("http://localhost:8000/openai/")
anthropic = RemoteRunnable("http://localhost:8000/anthropic/")


# Let's create a prompt composed of a system message and a human message.



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a highly educated person who loves to use big words. "
            + "You are also concise. Never answer in more than three sentences.",
        ),
        ("human", "Tell me about your favorite novel"),
    ]
).format_messages()


# We can use either LLM



anthropic.invoke(prompt)




openai_llm.invoke(prompt)


# As with regular runnables, async invoke, batch and async batch variants are available by default



await openai_llm.ainvoke(prompt)




anthropic.batch([prompt, prompt])




await anthropic.abatch([prompt, prompt])


# Streaming is available by default



for chunk in anthropic.stream(prompt):
    print(chunk.content, end="", flush=True)




async for chunk in anthropic.astream(prompt):
    print(chunk.content, end="", flush=True)




from langchain.schema.runnable import RunnablePassthrough




comedian_chain = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a comedian that sometimes tells funny jokes and other times you just state facts that are not funny. Please either tell a joke or state fact now but only output one.",
            ),
        ]
    )
    | openai_llm
)

joke_classifier_chain = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Please determine if the joke is funny. Say `funny` if it's funny and `not funny` if not funny. Then repeat the first five words of the joke for reference...",
            ),
            ("human", "{joke}"),
        ]
    )
    | anthropic
)


chain = {"joke": comedian_chain} | RunnablePassthrough.assign(
    classification=joke_classifier_chain
)




chain.invoke({})

