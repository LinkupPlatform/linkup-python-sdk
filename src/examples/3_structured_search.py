"""
With output_type set to "structured", the Linkup search can be used to require any arbitrary data
structure, based on a JSON schema or a pydantic.BaseModel. This can be used with a well defined and
documented schema to steer the Linkup search in any direction.
"""

from typing import List

from pydantic import BaseModel, Field

from linkup import LinkupClient


class Event(BaseModel):
    date: str = Field(description="The date of the event")
    description: str = Field(description="The description of the event")


class Events(BaseModel):
    events: List[Event] = Field(description="The list of events")


client = LinkupClient()

response = client.search(
    query="What are the 3 major events in the life of Abraham Lincoln?",
    depth="standard",  # or "deep"
    output_type="structured",
    structured_output_schema=Events,
)
print(response)
