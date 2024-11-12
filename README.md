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

	Option 1: Export the LINKUP_API_KEY environment variable in your shell.

	```bash
	export LINKUP_API_KEY='your_api_key_here'
	```

	Option 2: Create a .env file in your project directory and add your API key.

	```env
	LINKUP_API_KEY=your_api_key_here
	```

## 📋 Example

```python
from linkup.client import LinkupClient

# Initialize the client (API key is automatically read from the environment variable)
client = LinkupClient()

# Perform a search query
results = client.search("example query", depth="standard")

# Print the results
print(results)
```