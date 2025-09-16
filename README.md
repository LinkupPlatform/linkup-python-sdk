# 🚀 Linkup Python SDK

[![PyPI version](https://badge.fury.io/py/linkup-sdk.svg)](https://pypi.org/project/linkup-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![PyPI - Downloads](https://img.shields.io/pypi/dm/linkup-sdk)
[![Discord](https://img.shields.io/discord/1303713168916348959?color=7289da&logo=discord&logoColor=white)](https://discord.gg/9q9mCYJa86)

A [Python SDK](https://docs.linkup.so/pages/sdk/python/python) for the
[Linkup API](https://www.linkup.so/), allowing easy integration with Linkup's services. 🐍

## 🌟 Features

- ✅ **Simple and intuitive API client.**
- 🔍 **Support all Linkup entrypoints and parameters.**
- ⚡ **Supports synchronous and asynchronous requests.**
- 🔒 **Handles authentication and request management.**

## 📦 Installation

Simply install the Linkup Python SDK as any Python package, for instance using `pip`:

```bash
pip install linkup-sdk
```

## 🛠️ Usage

### Setting Up Your Environment

1. **🔑 Obtain an API Key:**

   Sign up on Linkup to get your API key.

2. **⚙️ Set-up the API Key:**

   Option 1: Export the `LINKUP_API_KEY` environment variable in your shell before using the Python
   SDK.

   ```bash
   export LINKUP_API_KEY='YOUR_LINKUP_API_KEY'
   ```

   Option 2: Set the `LINKUP_API_KEY` environment variable directly within Python, using for
   instance `os.environ` or [python-dotenv](https://github.com/theskumar/python-dotenv) with a
   `.env` file (`python-dotenv` needs to be installed separately in this case), before creating the
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

### 📋 Examples

#### 📝 Search

The `search` function can be used to performs web searches. It supports two very different
complexity modes:

- with `depth="standard"`, the search will be straightforward and fast, suited for relatively simple
  queries (e.g. "What's the weather in Paris today?")
- with `depth="deep"`, the search will use an agentic workflow, which makes it in general slower,
  but it will be able to solve more complex queries (e.g. "What is the company profile of LangChain
  accross the last few years, and how does it compare to its concurrents?")

The `search` function also supports three output types:

- with `output_type="searchResults"`, the search will return a list of relevant documents
- with `output_type="sourcedAnswer"`, the search will return a concise answer with sources
- with `output_type="structured"`, the search will return a structured output according to a
  user-defined schema

```python
from linkup import LinkupClient, LinkupSourcedAnswer
from typing import Any

client = LinkupClient()  # API key can be read from the environment variable or passed as an argument
search_response: Any = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="deep",  # "standard" or "deep"
    output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
    structured_output_schema=None,  # must be filled if output_type is "structured"
)
assert isinstance(search_response, LinkupSourcedAnswer)
print(search_response.model_dump())
# Response:
# {
#   answer="The three major events in the life of Abraham Lincoln are: 1. ...",
#   sources=[
#     {
#       "name": "HISTORY",
#       "url": "https://www.history.com/topics/us-presidents/abraham-lincoln",
#       "snippet": "Abraham Lincoln - Facts & Summary - HISTORY ..."
#     },
#     ...
#   ]
# }
```

#### 🪝 Fetch

The `fetch` function can be used to retrieve the content of a given web page in a cleaned up
markdown format.

You can use the `render_js` flag to execute the JavaScript code of the page before returning the
content, and ask to `include_raw_html` to the response if you feel like it.

```python
from linkup import LinkupClient, LinkupFetchResponse

client = LinkupClient()  # API key can be read from the environment variable or passed as an argument
fetch_response: LinkupFetchResponse = client.fetch(
    url="https://docs.linkup.so",
    render_js=False,
    include_raw_html=True,
)
print(fetch_response.model_dump())
# Response:
# {
#   markdown="Get started for free, no credit card required...",
#   raw_html="<!DOCTYPE html><html lang=\"en\"><head>...</head><body>...</body></html>"
# }
```

#### 📚 More Examples

See the `examples/` directory for more examples and documentation, for instance on how to use Linkup
entrypoints using asynchronous functions.
