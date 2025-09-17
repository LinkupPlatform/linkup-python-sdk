"""
The Linkup search can also be used to perform direct Question Answering, with output_type set to
"sourcedAnswer". In this case, the API will output an answer to the query in natural language,
along with the sources supporting it.
"""

from dotenv import load_dotenv
from rich import print

from linkup import LinkupClient

load_dotenv()
client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln ?",
    depth="standard",  # or "deep"
    output_type="sourcedAnswer",
)
print(response)
