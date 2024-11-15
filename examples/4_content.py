"""
An alternative use-case of the Linkup API is to retrieve the content of a webpage of one of our
Premium Sources Partners.
"""

from linkup import LinkupClient

client = LinkupClient()

response = client.content(
    url="https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
    "of-indias-independence",
)

print(response)
