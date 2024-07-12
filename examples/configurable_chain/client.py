#!/usr/bin/env python
# coding: utf-8

# # Client
# 
# Demo of client interacting with the simple chain server, which deploys a chain that tells jokes about a particular topic.

# You can interact with this via API directly



import requests

inputs = {"input": {"topic": "sports"}}
response = requests.post("http://localhost:8000/configurable_temp/invoke", json=inputs)

response.json()


# You can also interact with this via the RemoteRunnable interface (to use in other chains)



from langserve import RemoteRunnable

remote_runnable = RemoteRunnable("http://localhost:8000/configurable_temp")


# Remote runnable has the same interface as local runnables



response = await remote_runnable.ainvoke({"topic": "sports"})


# The client can also execute langchain code synchronously, and pass in configs



from langchain.schema.runnable.config import RunnableConfig

remote_runnable.batch([{"topic": "sports"}, {"topic": "cars"}])


# The server supports streaming (using HTTP server-side events), which can help interact with long responses in real time



async for chunk in remote_runnable.astream({"topic": "bears, but a bit verbose"}):
    print(chunk, end="", flush=True)


# ## Configurability
# 
# The server chains have been exposed as configurable chains!
# 
# ```python 
# 
# model = ChatOpenAI(temperature=0.5).configurable_alternatives(
#     ConfigurableField(
#         id="llm",
#         name="LLM",
#         description=(
#             "Decide whether to use a high or a low temperature parameter for the LLM."
#         ),
#     ),
#     high_temp=ChatOpenAI(temperature=0.9),
#     low_temp=ChatOpenAI(temperature=0.1),
#     default_key="medium_temp",
# )
# prompt = PromptTemplate.from_template(
#     "tell me a joke about {topic}."
# ).configurable_fields(  # Example of a configurable field
#     template=ConfigurableField(
#         id="prompt",
#         name="Prompt",
#         description=("The prompt to use. Must contain {topic}."),
#     )
# )
# ```

# We can now use the configurability of the runnable in the API!



await remote_runnable.ainvoke(
    {"topic": "sports"},
    config={
        "configurable": {"prompt": "how to say {topic} in french", "llm": "low_temp"}
    },
)


# ## Configurability Based on Request Properties
# 
# If you want to change your chain invocation based on your request's properties,
# you can do so with `add_routes`'s `per_req_config_modifier` method as follows:
# 
# ```python 
# 
# # Add another example route where you can configure the model based
# # on properties of the request. This is useful for passing in API
# # keys from request headers (WITH CAUTION) or using other properties
# # of the request to configure the model.
# def fetch_api_key_from_header(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
#     if "x-api-key" in req.headers:
#         config["configurable"]["openai_api_key"] = req.headers["x-api-key"]
#     return config
# 
# dynamic_auth_model = ChatOpenAI(openai_api_key='placeholder').configurable_fields(
#     openai_api_key=ConfigurableField(
#         id="openai_api_key",
#         name="OpenAI API Key",
#         description=(
#             "API Key for OpenAI interactions"
#         ),
#     ),
# )
# 
# dynamic_auth_chain = dynamic_auth_model | StrOutputParser()
# 
# add_routes(
#     app, 
#     dynamic_auth_chain, 
#     path="/auth_from_header",
#     config_keys=["configurable"], 
#     per_req_config_modifier=fetch_api_key_from_header
# )
# ```

# Now, we can see that our request to the model will only work if we have a specific request
# header set:



# The model will fail with an auth error
unauthenticated_response = requests.post(
    "http://localhost:8000/auth_from_header/invoke", json={"input": "hello"}
)
unauthenticated_response.json()


# Now, ensure that you have run the following locally on your shell
# ```bash
# export TEST_API_KEY=<INSERT MY KEY HERE>
# ```



# The model will succeed as long as the above shell script is run previously
import os

test_key = os.environ["TEST_API_KEY"]
authenticated_response = requests.post(
    "http://localhost:8000/auth_from_header/invoke",
    json={"input": "hello"},
    headers={"x-api-key": test_key},
)
authenticated_response.json()






