# 🚀 Linkup Python SDK

[![PyPI version](https://badge.fury.io/py/linkup-python-sdk.svg)](https://pypi.org/project/linkup-python-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python SDK for the [Linkup API](https://linkup-api.readme.io/reference/getting-started), allowing easy integration with Linkup's services. 🐍

## 🌟 Features

- ✅ **Simple and intuitive API client.**
- 🔍 **Supports both standard and deep search queries.**
- 🔒 **Handles authentication and request management.**

## 📦 Installation

Install the SDK using `pip`:

```bash
pip install linkup-python-sdk
```

## 🛠️ Usage

### Setting Up Your Environment

1. **🔑 Obtain an API Key:**

	Sign up on Linkup to get your API key.

2. **⚙️ Set the API Key as an Environment Variable:**

   Option 1: Export the LINKUP_API_KEY environment variable in your shell before using the Python
   SDK.

   ```bash
   export LINKUP_API_KEY='YOUR_LINKUP_API_KEY'
   ```

   Option 2: Set the `LINKUP_API_KEY` environment variable directly within Python, using
   `os.environ` or [python-dotenv](https://github.com/theskumar/python-dotenv) for instance, before
   creating the Linkup Client.

   ```python
   import os
   from linkup import LinkupClient

   os.environ["LINKUP_API_KEY"] = "YOUR_LINKUP_API_KEY"
   client = LinkupClient()
   ...
   ```

   Option 3: Pass the Linkup API key to the Linkup Client when creating it.

   ```python
   from linkup import LinkupClient

   client = LinkupClient(api_key="YOUR_LINKUP_API_KEY")
   ...
   ```

## 📋 Example

```python
from linkup.client import LinkupClient, LinkupClientResponse

# Initialize the client (API key is automatically read from the environment variable)
client = LinkupClient()

# Perform a search query
reponse: LinkupClientResponse = client.search("example query", depth="standard")

# Print the results
print(f"Content: {response.content}")
print(f"Sources: {response.sources}")
```
