"""
The Linkup API can also be used to retrieve raw search results, which can then be re-used in a RAG
system, for instance.
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="searchResults",
)

print(response)
