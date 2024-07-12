#!/usr/bin/env python
# coding: utf-8

# # File processing
# 
# This client will be uploading a PDF file to the langserve server which will read the PDF and extract content from the first page.

# Let's load the file in base64 encoding:



import base64

with open("sample.pdf", "rb") as f:
    data = f.read()

encoded_data = base64.b64encode(data).decode("utf-8")


# Using raw requests



import requests

requests.post(
    "http://localhost:8000/pdf/invoke/", json={"input": {"file": encoded_data}}
).json()


# Using the SDK



from langserve import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/pdf/")




runnable.invoke({"file": encoded_data})




runnable.batch([{"file": encoded_data}, {"file": encoded_data, "num_chars": 10}])

