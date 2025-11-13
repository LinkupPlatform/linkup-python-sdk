"""Input and output types for Linkup functions."""

# ruff: noqa: FA100 (pydantic models don't play well with future annotations)

from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class LinkupSearchTextResult(BaseModel):
    """A text result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case "text".
        name: The name of the search result.
        url: The URL of the search result.
        content: The text of the search result.
    """

    type: Literal["text"]
    name: str
    url: str
    content: str


class LinkupSearchImageResult(BaseModel):
    """An image result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case "image".
        name: The name of the image result.
        url: The URL of the image result.
    """

    type: Literal["image"]
    name: str
    url: str


class LinkupSearchResults(BaseModel):
    """The results of the Linkup search.

    Attributes:
        results: The results of the Linkup search.
    """

    results: list[Union[LinkupSearchTextResult, LinkupSearchImageResult]]


class LinkupSource(BaseModel):
    """A source supporting a Linkup answer.

    Attributes:
        name: The name of the source.
        url: The URL of the source.
        snippet: The text excerpt supporting the Linkup answer. Can be empty for image sources.
    """

    name: str
    url: str
    snippet: str = ""


class LinkupSourcedAnswer(BaseModel):
    """A Linkup answer, with the sources supporting it.

    Attributes:
        answer: The answer text.
        sources: The sources supporting the answer.
    """

    answer: str
    sources: list[LinkupSource]


class LinkupSearchStructuredResponse(BaseModel):
    """A Linkup `search` structured response, with the sources supporting it.

    Attributes:
        data: The answer data, either as a Pydantic model or an arbitrary JSON structure.
        sources: The sources supporting the answer.
    """

    data: Any
    sources: list[Union[LinkupSearchTextResult, LinkupSearchImageResult]]


class LinkupFetchImageExtraction(BaseModel):
    """An image extraction from a Linkup web page fetch.

    Attributes:
        alt: The alt text of the image.
        url: The URL of the image.
    """

    alt: str
    url: str


class LinkupFetchResponse(BaseModel):
    """The response from a Linkup web page fetch.

    Attributes:
        markdown: The cleaned up markdown content.
        raw_html: The optional raw HTML content.
        images: The optional list of image URLs.
    """

    model_config = ConfigDict(populate_by_name=True)

    markdown: str
    raw_html: Optional[str] = Field(default=None, validation_alias="rawHtml")
    images: Optional[list[LinkupFetchImageExtraction]] = Field(default=None)
