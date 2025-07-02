"""
The Linkup search can output raw search results which can then be re-used in different use-cases,
for instance in a RAG system, with the output_type parameter set to "searchResults".
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="searchResults",
)
print(response)
