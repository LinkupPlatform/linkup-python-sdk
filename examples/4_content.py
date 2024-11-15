"""
As an alternative use-case to the Linkup search, the Linkup API comes with another entrypoint,
content, able to retrieve the raw content of a webpage of one of our Premium Sources Partners.
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.content(
    url="https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
    "of-indias-independence",
)
print(response)
