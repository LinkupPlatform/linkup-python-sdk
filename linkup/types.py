from typing import List

from pydantic import BaseModel


class LinkupContent(BaseModel):
    """
    The content of a webpage of one of our Premium Sources Partners.

    Attributes:
        content: The content of the webpage.
    """

    content: str


class LinkupSearchResult(BaseModel):
    """
    A result in a Linkup search.

    Attributes:
        name: The name of the search result.
        url: The URL of the search result.
        content: The text of the search result.
    """

    name: str
    url: str
    content: str


class LinkupSearchResults(BaseModel):
    """
    The results of the Linkup search.

    Attributes:
        results: The results of the Linkup search.
    """

    results: List[LinkupSearchResult]


class LinkupSource(BaseModel):
    """
    A source supporting a Linkup answer.

    Attributes:
        name: The name of the source.
        url: The URL of the source.
        snippet: The text excerpt supporting the Linkup answer.
    """

    name: str
    url: str
    snippet: str


class LinkupSourcedAnswer(BaseModel):
    """
    A Linkup answer, with the sources supporting it.

    Attributes:
        answer: The answer text.
        sources: The sources supporting the answer.
    """

    answer: str
    sources: List[LinkupSource]
