# 🚀 Linkup Python SDK

[![PyPI version](https://badge.fury.io/py/linkup-sdk.svg)](https://pypi.org/project/linkup-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python SDK for the [Linkup API](https://linkup-api.readme.io/reference/getting-started), allowing easy integration with Linkup's services. 🐍

## 🌟 Features

- ✅ **Simple and intuitive API client.**
- 🔍 **Supports both standard and deep search queries.**
- 🔒 **Handles authentication and request management.**

## 📦 Installation

Install the SDK using `pip`:

```bash
pip install linkup-sdk
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

   Option 2: Set the `LINKUP_API_KEY` environment variable directly within Python, using for
   instance `os.environ` or [python-dotenv](https://github.com/theskumar/python-dotenv) with a
   `.env` file (python-dotenv needs to be installed separately in this case), before creating the
   Linkup Client.

   ```python
   import os
   from linkup import LinkupClient

   os.environ["LINKUP_API_KEY"] = "YOUR_LINKUP_API_KEY"
   # or dotenv.load_dotenv()
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
from linkup import LinkupClient

# Initialize the client (API key can be read from the environment variable or passed as an argument)
client = LinkupClient()

# Perform a search query
search_response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="searchResults",  # or "sourcedAnswer" or "structured"
    structured_output_schema=None,  # must be filled if output_type is "structured"
)
print(search_response)

# Get access to our Premium Sources Partners content
content_response = client.content(
    url="https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
    "of-indias-independence",
)
print(content_response)
```

See the `examples/` directory for more examples and documentation, for instance on how to use Linkup
entrypoints using asynchronous functions.
