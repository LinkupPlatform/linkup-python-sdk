"""
The Linkup search can also be used to perform direct Question Answering, with output_type set to
"sourcedAnswer". In this case, the API will output an answer to the query in natural language,
along with the sources supporting it.
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln ?",
    depth="standard",  # or "deep"
    output_type="sourcedAnswer",
)
print(response)
