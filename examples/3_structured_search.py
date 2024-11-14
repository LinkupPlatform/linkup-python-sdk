"""
The structured search feature of the Linkup API makes possible to require any arbitrary and
documented data structure to the Linkup API, using JSON schema, in order to steer the Linkup API in
any direction.
"""

from linkup import LinkupClient
from pydantic import BaseModel, Field


class Event(BaseModel):
    date: str = Field(description="The date of the event")
    description: str = Field(description="The description of the event")


class Events(BaseModel):
    events: list[Event] = Field(description="The list of events")


client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="structured",
    structured_output_schema=Events,
)

print(response)
