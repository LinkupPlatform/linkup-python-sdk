"""
By default, whatever its depth parameter, the Linkup API outputs an answer, along with the sources
supporting it.
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln ?",
    depth="standard",  # or "deep"
)

print(response)
