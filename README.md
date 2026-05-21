# 🚀 Linkup Python SDK

[![PyPI version](https://badge.fury.io/py/linkup-sdk.svg)](https://pypi.org/project/linkup-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![PyPI - Downloads](https://img.shields.io/pypi/dm/linkup-sdk)
[![Discord](https://img.shields.io/discord/1303713168916348959?color=7289da&logo=discord&logoColor=white)](https://discord.gg/9q9mCYJa86)

A Python SDK for the [Linkup API](https://www.linkup.so/), allowing easy integration with Linkup's
services in any Python application. 🐍

Checkout the official
[API documentation](https://docs.linkup.so/pages/documentation/get-started/introduction) and
[SDK documentation](https://docs.linkup.so/pages/sdk/python/python) for additional details on how to
benefit from Linkup services to the full extent. 📝

## 🌟 Features

- ✅ **Simple and intuitive API client.**
- 🔍 **Supports Linkup search, fetch, research, and task workflows.**
- ⚡ **Support synchronous and asynchronous calls.**
- 🔒 **Handle authentication and request management.**
- 💳 **Built-in x402 payment protocol support for on-chain payments.**

## 📦 Installation

Simply install the Linkup Python SDK as any Python package, for instance using `pip`:

```bash
pip install linkup-sdk
```

To use the x402 payment protocol (on-chain payments via EVM), install the optional x402 extras:

```bash
pip install linkup-sdk[x402]
```

## 🛠️ Usage

### Setting Up Your Environment

1. **🔑 Obtain an API Key:**

   Sign up on Linkup to get your API key.

2. **⚙️ Set-up the API Key:**

   Option 1: Export the `LINKUP_API_KEY` environment variable in your shell before using the Python
   SDK.

   ```bash
   export LINKUP_API_KEY=<your-linkup-api-key>
   ```

   Option 2: Set the `LINKUP_API_KEY` environment variable directly within Python, using for
   instance `os.environ` or [python-dotenv](https://github.com/theskumar/python-dotenv) with a
   `.env` file (`python-dotenv` needs to be installed separately in this case), before creating the
   Linkup Client.

   ```python
   import os
   import linkup

   os.environ["LINKUP_API_KEY"] = "<your-linkup-api-key>"
   # or dotenv.load_dotenv()
   client = linkup.Client()
   ...
   ```

   Option 3: Pass the Linkup API key to the Linkup Client when creating it.

   ```python
   import linkup

   client = linkup.Client(api_key="<your-linkup-api-key>")
   ...
   ```

### 📋 Examples

#### 📝 Search

The `search` function can be used to performs web searches. It supports three different complexity
modes, through the `depth` parameter:

- `"fast"` (**beta**), for sub-second responses to simple, focused queries (must be keyword-based)
- `"standard"`, for single-iteration agentic search that can interpret the query, run parallel
  sub-searches, and scrape one URL while remaining fast
- `"deep"`, for slower, more agentic and complex responses, suited to more complex queries (e.g.
  "What is the company profile of LangChain accross the last few years, and how does it compare to
  its concurrents?")

The `search` function also supports three output types, through the `output_type` parameter:

- with `"searchResults"`, the search will return a list of relevant documents
- with `"sourcedAnswer"`, the search will return a concise answer with sources
- with `"structured"`, the search will return a structured output according to a user-defined schema

```python
from typing import Any

import linkup

client = linkup.Client()  # API key can be read from the environment variable or passed as an argument
search_response: Any = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="deep",  # "fast" (beta), "standard", or "deep"
    output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
    structured_output_schema=None,  # must be filled if output_type is "structured"
)
assert isinstance(search_response, linkup.SourcedAnswer)
print(search_response.model_dump())
```

Which prints:

```bash
{
  answer="The three major events in the life of Abraham Lincoln are: 1. ...",
  sources=[
    {
      "name": "HISTORY",
      "url": "https://www.history.com/topics/us-presidents/abraham-lincoln",
      "snippet": "Abraham Lincoln - Facts & Summary - HISTORY ...",
      "favicon": "https://www.history.com/favicon.ico",
    },
    ...
  ]
}
```

Check the code or the
[official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search)
for the detailed list of available parameters.

#### 🪝 Fetch

The `fetch` function can be used to retrieve the content of a given web page in a cleaned up
markdown format.

You can use the `render_js` flag to execute the JavaScript code of the page before returning the
content, and ask to `include_raw_html` to the response if you feel like it.

```python
import linkup

client = linkup.Client()  # API key can be read from the environment variable or passed as an argument
fetch_response: linkup.FetchResponse = client.fetch(
    url="https://docs.linkup.so",
    render_js=False,
    include_raw_html=True,
)
print(fetch_response.model_dump())
```

Which prints:

```bash
{
  markdown="Get started for free, no credit card required...",
  raw_html="<!DOCTYPE html><html lang=\"en\"><head>...</head><body>...</body></html>"
}
```

Check the code or the
[official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch)
for the detailed list of available parameters.

#### 🧠 Research

The `research` function creates an asynchronous research task. You can then use `get_research` or
`list_research` to inspect it later.

```python
import linkup

client = linkup.Client()
research_task: linkup.ResearchTask = client.research(
    query="What changed in the AI browser market this quarter?",
    output_type="sourcedAnswer",
)
print(research_task.id)
```

#### 🗂️ Tasks

The `create_tasks` function lets you submit mixed `search`, `fetch`, and `research` jobs in a single
batch, then inspect them through `get_task` or `list_tasks`.

```python
import linkup

client = linkup.Client()
tasks = client.create_tasks(
    [
        linkup.SearchTaskInput(
            query="Linkup latest product updates",
            depth="deep",
            output_type="sourcedAnswer",
        ),
        linkup.FetchTaskInput(
            url="https://docs.linkup.so",
        ),
    ]
)
print([task.id for task in tasks])
```

#### ⌛ Asynchronous Calls

All the Linkup main functions come with an asynchronous counterpart, with the same behavior and the
same name prefixed by `async_` (e.g. `async_search` for `search`). This should be favored in
production use cases to avoid blocking the main thread while waiting for the Linkup API to respond.
This makes possible to call the Linkup API several times concurrently for instance.

```python
import asyncio
from typing import Any

import linkup

async def main() -> None:
    client = linkup.Client()  # API key can be read from the environment variable or passed as an argument
    search_response: Any = await client.async_search(
        query="What are the 3 major events in the life of Abraham Lincoln?",
        depth="deep",  # "fast" (beta), "standard", or "deep"
        output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
        structured_output_schema=None,  # must be filled if output_type is "structured"
    )
    assert isinstance(search_response, linkup.SourcedAnswer)
    print(search_response.model_dump())

asyncio.run(main())
```

Which prints:

```bash
{
  answer="The three major events in the life of Abraham Lincoln are: 1. ...",
  sources=[
    {
      "name": "HISTORY",
      "url": "https://www.history.com/topics/us-presidents/abraham-lincoln",
      "snippet": "Abraham Lincoln - Facts & Summary - HISTORY ..."
      "favicon": "https://www.history.com/favicon.ico",
    },
    ...
  ]
}
```

#### 💳 x402 Payment Protocol

The SDK supports the [x402 payment protocol](https://www.x402.org/), allowing clients to
automatically handle HTTP 402 responses by signing and retrying requests with on-chain payments via
[EVM](https://ethereum.org/en/developers/docs/evm/)-compatible networks (currently Base). This can
be used as an alternative to API key authentication.

Create an `eth_account` `LocalAccount` compatible with Base (Ethereum):

```python
from eth_account import Account

account = Account.from_key("<YOUR WALLET PRIVATE KEY>")
```

```python
from eth_account import Account

Account.enable_unaudited_hdwallet_features()
account = Account.from_mnemonic("<YOUR MNEMONIC PHRASE>")
```

Then pass it to `create_x402_signer` and use the Linkup client:

```python
import linkup
from linkup.x402 import create_x402_signer

signer = create_x402_signer(account)
client = linkup.Client(x402_signer=signer)

result = client.search(
    query="What is x402?",
    depth="standard",
    output_type="sourcedAnswer",
)
print(result.answer)
```
