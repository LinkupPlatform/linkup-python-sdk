"""Example of search results search.

The Linkup search can output raw search results which can then be re-used in different use-cases,
for instance in a RAG system, with the `output_type` parameter set to `searchResults`.

To use this script, copy the `.env.example` file at the root of the repository inside a `.env`, and
fill the missing values, or pass a Linkup API key to the `LinkupClient` initialization.
"""

import rich
from dotenv import load_dotenv

from linkup import LinkupClient

load_dotenv()
client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="searchResults",
)
rich.print(response)
