"""Input and output types for Linkup functions."""

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class _LinkupBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class LinkupSearchTextResult(_LinkupBaseModel):
    """A text result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case "text".
        name: The name of the search result.
        url: The URL of the search result.
        content: The text of the search result.
        favicon: The favicon URL of the search result, if available.
    """

    type: Literal["text"]
    name: str
    url: str
    content: str
    favicon: str = ""


class LinkupSearchImageResult(_LinkupBaseModel):
    """An image result from a Linkup search.

    Attributes:
        type: The type of the search result, in this case "image".
        name: The name of the image result.
        url: The URL of the image result.
    """

    type: Literal["image"]
    name: str
    url: str


class LinkupSearchResults(_LinkupBaseModel):
    """The results of the Linkup search.

    Attributes:
        results: The results of the Linkup search.
    """

    results: list[LinkupSearchTextResult | LinkupSearchImageResult]


class LinkupSource(_LinkupBaseModel):
    """A source supporting a Linkup answer.

    Attributes:
        name: The name of the source.
        url: The URL of the source.
        snippet: The text excerpt supporting the Linkup answer. Can be empty for image sources.
        favicon: The favicon URL of the source, if available.
    """

    name: str
    url: str
    snippet: str = ""
    favicon: str = ""


class LinkupSourcedAnswer(_LinkupBaseModel):
    """A Linkup answer, with the sources supporting it.

    Attributes:
        answer: The answer text.
        sources: The sources supporting the answer.
    """

    answer: str
    sources: list[LinkupSource]


class LinkupSearchStructuredResponse(_LinkupBaseModel):
    """A Linkup `search` structured response, with the sources supporting it.

    Attributes:
        data: The answer data, either as a Pydantic model or an arbitrary JSON structure.
        sources: The sources supporting the answer.
    """

    data: Any
    sources: list[LinkupSearchTextResult | LinkupSearchImageResult]


class LinkupFetchImageExtraction(_LinkupBaseModel):
    """An image extraction from a Linkup web page fetch.

    Attributes:
        alt: The alt text of the image.
        url: The URL of the image.
    """

    alt: str
    url: str


class LinkupFetchResponse(_LinkupBaseModel):
    """The response from a Linkup web page fetch.

    Attributes:
        markdown: The cleaned up markdown content.
        raw_html: The optional raw HTML content.
        images: The optional list of image URLs.
    """

    markdown: str
    raw_html: str | None = Field(default=None, validation_alias="rawHtml")
    images: list[LinkupFetchImageExtraction] | None = Field(default=None)


class LinkupSearchTaskInput(_LinkupBaseModel):
    """Input for creating or retrieving a search task.

    Attributes:
        query: The search query.
        depth: The search depth.
        output_type: The expected search output type.
        include_images: Whether image results should be included.
        from_date: The start date used to filter search sources, if any.
        to_date: The end date used to filter search sources, if any.
        exclude_domains: Domains to exclude from the search, if any.
        include_domains: Domains to restrict the search to, if any.
        max_results: The maximum number of search results requested, if any.
        include_inline_citations: Whether inline citations should be included.
        include_sources: Whether sources should be included for structured output.
        structured_output_schema: The structured output schema, if any.
    """

    query: str = Field(validation_alias="q")
    depth: Literal["standard", "deep"]
    output_type: Literal["searchResults", "sourcedAnswer", "structured"] = Field(
        validation_alias="outputType"
    )
    include_images: bool | None = Field(default=None, validation_alias="includeImages")
    from_date: date | str | None = Field(default=None, validation_alias="fromDate")
    to_date: date | str | None = Field(default=None, validation_alias="toDate")
    exclude_domains: list[str] | None = Field(default=None, validation_alias="excludeDomains")
    include_domains: list[str] | None = Field(default=None, validation_alias="includeDomains")
    max_results: int | None = Field(default=None, validation_alias="maxResults")
    include_inline_citations: bool | None = Field(
        default=None, validation_alias="includeInlineCitations"
    )
    include_sources: bool | None = Field(default=None, validation_alias="includeSources")
    structured_output_schema: type[BaseModel] | str | dict[str, Any] | None = Field(
        default=None, validation_alias="structuredOutputSchema"
    )


class LinkupResearchTaskInput(_LinkupBaseModel):
    """Input for creating or retrieving a research task.

    Attributes:
        query: The research query.
        output_type: The expected research output type.
        mode: The research mode to use, if provided.
        reasoning_depth: The reasoning depth to use, if provided.
        from_date: The start date used to filter research sources, if any.
        to_date: The end date used to filter research sources, if any.
        exclude_domains: Domains to exclude from the research sources, if any.
        include_domains: Domains to restrict the research sources to, if any.
        structured_output_schema: The structured output schema, if any.
    """

    query: str = Field(validation_alias="q")
    output_type: Literal["sourcedAnswer", "structured"] = Field(validation_alias="outputType")
    mode: Literal["answer", "auto", "investigate", "research"] | None = None
    reasoning_depth: Literal["S", "M", "L", "XL"] | None = Field(
        default=None, validation_alias="reasoningDepth"
    )
    from_date: date | str | None = Field(default=None, validation_alias="fromDate")
    to_date: date | str | None = Field(default=None, validation_alias="toDate")
    exclude_domains: list[str] | None = Field(default=None, validation_alias="excludeDomains")
    include_domains: list[str] | None = Field(default=None, validation_alias="includeDomains")
    structured_output_schema: type[BaseModel] | str | dict[str, Any] | None = Field(
        default=None, validation_alias="structuredOutputSchema"
    )


class LinkupFetchTaskInput(_LinkupBaseModel):
    """Input for creating or retrieving a fetch task.

    Attributes:
        url: The URL requested for fetching.
        include_raw_html: Whether raw HTML should be included in the fetch response.
        render_js: Whether JavaScript rendering should be enabled.
        extract_images: Whether image extraction should be enabled.
    """

    url: str
    include_raw_html: bool | None = Field(default=None, validation_alias="includeRawHtml")
    render_js: bool | None = Field(default=None, validation_alias="renderJs")
    extract_images: bool | None = Field(default=None, validation_alias="extractImages")


LinkupTaskInput = LinkupSearchTaskInput | LinkupFetchTaskInput | LinkupResearchTaskInput


class LinkupTaskMetadata(_LinkupBaseModel):
    """Pagination metadata returned by list endpoints.

    Attributes:
        page: The current page number.
        page_size: The number of tasks per page.
        total: The total number of tasks matching the request.
        total_pages: The total number of available pages.
    """

    page: int
    page_size: int = Field(validation_alias="pageSize")
    total: int
    total_pages: int = Field(validation_alias="totalPages")


class LinkupTaskQuota(_LinkupBaseModel):
    """Task quota information returned by `list_tasks`.

    Attributes:
        in_flight: The number of tasks currently in flight.
        limit: The maximum number of in-flight tasks allowed.
    """

    in_flight: int = Field(validation_alias="inFlight")
    limit: int


class LinkupSearchTask(_LinkupBaseModel):
    """A search task returned by the Linkup API.

    Attributes:
        created_at: The task creation timestamp.
        error: The task error message, if the task failed.
        id: The task identifier.
        input: The normalized search input for this task.
        output: The parsed search output, if available.
        status: The current task status.
        type: The task type, in this case "search".
        updated_at: The last task update timestamp.
    """

    created_at: str = Field(validation_alias="createdAt")
    error: str | None = None
    id: str
    input: LinkupSearchTaskInput
    output: Any = None
    status: Literal["pending", "processing", "completed", "failed"]
    type: Literal["search"]
    updated_at: str = Field(validation_alias="updatedAt")


class LinkupFetchTask(_LinkupBaseModel):
    """A fetch task returned by the Linkup API.

    Attributes:
        created_at: The task creation timestamp.
        error: The task error message, if the task failed.
        id: The task identifier.
        input: The normalized fetch input for this task.
        output: The parsed fetch output, if available.
        status: The current task status.
        type: The task type, in this case "fetch".
        updated_at: The last task update timestamp.
    """

    created_at: str = Field(validation_alias="createdAt")
    error: str | None = None
    id: str
    input: LinkupFetchTaskInput
    output: LinkupFetchResponse | None = None
    status: Literal["pending", "processing", "completed", "failed"]
    type: Literal["fetch"]
    updated_at: str = Field(validation_alias="updatedAt")


class LinkupResearchTask(_LinkupBaseModel):
    """A research task returned by the Linkup API.

    Attributes:
        created_at: The task creation timestamp.
        error: The task error message, if the task failed.
        id: The task identifier.
        input: The normalized research input for this task.
        output: The parsed research output, if available.
        status: The current task status.
        type: The task type, in this case "research".
        updated_at: The last task update timestamp.
    """

    created_at: str = Field(validation_alias="createdAt")
    error: str | None = None
    id: str
    input: LinkupResearchTaskInput
    output: Any = None
    status: Literal["pending", "processing", "completed", "failed"]
    type: Literal["research"]
    updated_at: str = Field(validation_alias="updatedAt")


LinkupTask = LinkupSearchTask | LinkupFetchTask | LinkupResearchTask


class LinkupResearchTasksPage(_LinkupBaseModel):
    """Paginated research task list.

    Attributes:
        data: The research tasks in the current page.
        metadata: Pagination metadata for the result page.
    """

    data: list[LinkupResearchTask]
    metadata: LinkupTaskMetadata


class LinkupTasksPage(_LinkupBaseModel):
    """Paginated task list.

    Attributes:
        data: The tasks in the current page.
        metadata: Pagination metadata for the result page.
        quota: Task quota information for the authenticated organization.
    """

    data: list[LinkupTask]
    metadata: LinkupTaskMetadata
    quota: LinkupTaskQuota
