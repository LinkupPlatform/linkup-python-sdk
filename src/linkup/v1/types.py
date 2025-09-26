from typing import Literal, Union

import pydantic
from typing_extensions import TypeAlias


class TextSearchResult(pydantic.BaseModel):
    type: Literal["text"]
    name: str
    url: str
    content: str


class ImageSearchResult(pydantic.BaseModel):
    type: Literal["image"]
    name: str
    url: str


SearchResult: TypeAlias = Union[TextSearchResult, ImageSearchResult]


class SearchResponse(pydantic.BaseModel):
    data: str
    search_results: list[SearchResult]
