from typing import List, Union

from pydantic import BaseModel


class LinkupSearchTextResult(BaseModel):
    """
    A text result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case 'text'
        name: The name of the search result.
        url: The URL of the search result.
        content: The text of the search result.
    """

    type: str
    name: str
    url: str
    content: str


class LinkupSearchImageResult(BaseModel):
    """
    An image result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case 'image'
        name: The name of the image result.
        url: The URL of the image result.
    """

    type: str
    name: str
    url: str


class LinkupSearchResults(BaseModel):
    """
    The results of the Linkup search.

    Attributes:
        results: The results of the Linkup search.
    """

    results: List[Union[LinkupSearchTextResult, LinkupSearchImageResult]]


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
    sources: List[Union[LinkupSource, LinkupSearchTextResult, LinkupSearchImageResult]]
