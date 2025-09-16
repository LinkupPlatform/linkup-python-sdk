"""
The Linkup fetch can output the raw content of a web page.
"""

from dotenv import load_dotenv
from rich import print

from linkup import LinkupClient

load_dotenv()
client = LinkupClient()

response = client.fetch(
    url="https://docs.linkup.so",
    render_js=False,
)
print(response)
