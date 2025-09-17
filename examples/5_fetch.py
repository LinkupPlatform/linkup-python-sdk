"""Example of web page fetch.

The Linkup fetch can output the content of a web page as a cleaned up markdown.

To use this script, copy the `.env.example` file at the root of the repository inside a `.env`, and
fill the missing values, or pass a Linkup API key to the `LinkupClient` initialization.
"""

from dotenv import load_dotenv
from rich import print

from linkup import LinkupClient

load_dotenv()
client = LinkupClient()

response = client.fetch(
    url="https://docs.linkup.so",
)
print(response)
