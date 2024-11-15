"""
By default, the Linkup search outputs a raw search results, which can then be re-used in different
use-cases, for instance in a RAG system. This is controlled by the output_type parameter, which
defaults to "searchResults".
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="searchResults",
)
print(response)
