"""Linkup client, the entrypoint for Linkup functions."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any, Literal, cast, overload

import httpx
import pydantic

from ._errors import (
    LinkupAuthenticationError,
    LinkupBudgetLimitExceededError,
    LinkupFailedFetchError,
    LinkupFetchResponseTooLargeError,
    LinkupFetchUnsupportedContentTypeError,
    LinkupFetchUrlIsFileError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
    LinkupPaymentRequiredError,
    LinkupTaskNotFoundError,
    LinkupTasksQueueLimitExceededError,
    LinkupTimeoutError,
    LinkupTooManyRequestsError,
    LinkupUnknownError,
)
from ._types import (
    JSONObject,
    LinkupFetchResponse,
    LinkupFetchTask,
    LinkupFetchTaskInput,
    LinkupResearchTask,
    LinkupResearchTaskInput,
    LinkupResearchTasksPage,
    LinkupSearchResults,
    LinkupSearchStructuredResponse,
    LinkupSearchTask,
    LinkupSearchTaskInput,
    LinkupSourcedAnswer,
    LinkupTask,
    LinkupTaskInput,
    LinkupTasksPage,
)
from ._version import __version__

if TYPE_CHECKING:
    import datetime

    from .x402 import LinkupX402Signer


class LinkupClient:
    """The Linkup Client class, providing functions to call the Linkup API endpoints using Python.

    Args:
        api_key: The API key for the Linkup API. If None, the API key will be read from the
            environment variable LINKUP_API_KEY.
        base_url: The base URL for the Linkup API, for development purposes.
        x402_signer: An optional x402 signer for payment-gated endpoints. If provided, the
            client will attempt to handle 402 responses automatically. Cannot be used together
            with api_key.
        auth_header: Custom header name to use for the API key (e.g. "Ocp-Apim-Subscription-Key").
            When set, the API key value is sent as <auth_header>: <api_key> instead of the default
            Authorization: Bearer <api_key>.

    Raises:
        ValueError: If the API key is not provided and not found in the environment variable.
        ValueError: If both api_key and x402_signer are provided.
    """

    __version__ = __version__

    def __init__(
        self,
        api_key: str | pydantic.SecretStr | None = None,
        base_url: str = "https://api.linkup.so/v1",
        x402_signer: LinkupX402Signer | None = None,
        auth_header: str | None = None,
    ) -> None:
        if api_key is not None and x402_signer is not None:
            raise ValueError("Cannot provide both api_key and x402_signer")

        self._x402_signer: LinkupX402Signer | None = x402_signer

        if x402_signer is not None:
            self._api_key: pydantic.SecretStr | None = None
        else:
            if api_key is None:
                api_key = os.getenv("LINKUP_API_KEY")
            if not api_key:
                raise ValueError("The Linkup API key was not provided")
            if isinstance(api_key, str):
                api_key = pydantic.SecretStr(api_key)
            self._api_key = api_key

        self._base_url: str = base_url
        self._auth_header: str | None = auth_header

    @overload
    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults"],
        structured_output_schema: None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSearchResults: ...

    @overload
    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["sourcedAnswer"],
        structured_output_schema: None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSourcedAnswer: ...

    @overload
    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: Literal[False] | None = None,
        timeout: float | None = None,
    ) -> JSONObject: ...

    @overload
    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: Literal[True],
        timeout: float | None = None,
    ) -> LinkupSearchStructuredResponse: ...

    @overload
    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> (
        LinkupSearchResults | LinkupSourcedAnswer | JSONObject | LinkupSearchStructuredResponse
    ): ...

    def search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSearchResults | LinkupSourcedAnswer | JSONObject | LinkupSearchStructuredResponse:
        """Perform a web search using the Linkup API /search endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search).

        Args:
            query: The search query.
            depth: The depth of the search. Can be "fast" (beta), for a sub-second search (query
                must be keyword-based), "standard", for a simple, straightforward search (query can
                be free text), or "deep" for a more powerful agentic workflow (query can be free
                text).
            output_type: The type of output which is expected: "searchResults" will output raw
                search results, "sourcedAnswer" will output the answer to the query and sources
                supporting it, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel, a Python dictionary containing
                a valid object JSON schema, or a string representing a valid object JSON schema.
            include_images: Indicate whether images should be included during the search.
            from_date: The date from which the search results should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, the search
                results will not be filtered by date.
            to_date: The date until which the search results should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, the search
                results will not be filtered by date.
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            max_results: The maximum number of results to return.
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.
            include_sources: If output_type is "structured", indicate whether the answer should
                include sources. This will modify the schema of the structured response.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The Linkup API search result, which can have different types based on the parameters:
            - LinkupSearchResults if output_type is "searchResults"
            - LinkupSourcedAnswer if output_type is "sourcedAnswer"
            - a raw dictionary if output_type is "structured" and include_sources is False
            - LinkupSearchStructuredResponse if output_type is "structured" and include_sources is
              True

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string, dictionary,
                or pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupBudgetLimitExceededError: If the API key has reached its configured budget limit.
            LinkupNoResultError: If the search query did not yield any result.
            LinkupTimeoutError: If the request times out.
        """
        params: dict[str, str | bool | int | list[str]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            max_results=max_results,
            include_inline_citations=include_inline_citations,
            include_sources=include_sources,
        )

        response: httpx.Response = self._request(
            method="POST",
            url="/search",
            json=params,
            timeout=timeout,
        )

        return self._parse_search_response(
            response_data=response.json(),
            output_type=output_type,
            include_sources=include_sources,
        )

    @overload
    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults"],
        structured_output_schema: None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSearchResults: ...

    @overload
    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["sourcedAnswer"],
        structured_output_schema: None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSourcedAnswer: ...

    @overload
    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: Literal[False] | None = None,
        timeout: float | None = None,
    ) -> JSONObject: ...

    @overload
    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: Literal[True],
        timeout: float | None = None,
    ) -> LinkupSearchStructuredResponse: ...

    @overload
    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> (
        LinkupSearchResults | LinkupSourcedAnswer | JSONObject | LinkupSearchStructuredResponse
    ): ...

    async def async_search(
        self,
        query: str,
        *,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        include_images: bool | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupSearchResults | LinkupSourcedAnswer | JSONObject | LinkupSearchStructuredResponse:
        """Asynchronously perform a web search using the Linkup API /search endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search).

        Args:
            query: The search query.
            depth: The depth of the search. Can be "fast" (beta), for a sub-second search (query
                must be keyword-based), "standard", for a simple, straightforward search (query can
                be free text), or "deep" for a more powerful agentic workflow (query can be free
                text).
            output_type: The type of output which is expected: "searchResults" will output raw
                search results, "sourcedAnswer" will output the answer to the query and sources
                supporting it, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel, a Python dictionary containing
                a valid object JSON schema, or a string representing a valid object JSON schema.
            include_images: Indicate whether images should be included during the search.
            from_date: The date from which the search results should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, the search
                results will not be filtered by date.
            to_date: The date until which the search results should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, the search
                results will not be filtered by date.
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            max_results: The maximum number of results to return.
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.
            include_sources: If output_type is "structured", indicate whether the answer should
                include sources. This will modify the schema of the structured response.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The Linkup API search result, which can have different types based on the parameters:
            - LinkupSearchResults if output_type is "searchResults"
            - LinkupSourcedAnswer if output_type is "sourcedAnswer"
            - a raw dictionary if output_type is "structured" and include_sources is False
            - LinkupSearchStructuredResponse if output_type is "structured" and include_sources is
              True

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string, dictionary,
                or pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupBudgetLimitExceededError: If the API key has reached its configured budget limit.
            LinkupNoResultError: If the search query did not yield any result.
            LinkupTimeoutError: If the request times out.
        """
        params: dict[str, str | bool | int | list[str]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            max_results=max_results,
            include_inline_citations=include_inline_citations,
            include_sources=include_sources,
        )

        response: httpx.Response = await self._async_request(
            method="POST",
            url="/search",
            json=params,
            timeout=timeout,
        )

        return self._parse_search_response(
            response_data=response.json(),
            output_type=output_type,
            include_sources=include_sources,
        )

    def research(
        self,
        query: str,
        output_type: Literal["sourcedAnswer", "structured"],
        reasoning_depth: Literal["S", "M", "L", "XL"] | None = None,
        mode: Literal["answer", "auto", "investigate", "research"] | None = None,
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        timeout: float | None = None,
    ) -> LinkupResearchTask:
        """Create an asynchronous research task using the Linkup API /research endpoint.

        The returned task can be inspected later with get_research, list_research, get_task,
        or list_tasks.

        Args:
            query: The research query to investigate.
            output_type: The expected research output type. Use "sourcedAnswer" for an answer with
                supporting sources, or "structured" for output matching structured_output_schema.
            reasoning_depth: The amount of reasoning effort to use. If None, the Linkup API default
                is used.
            mode: The research mode to use. If None, the Linkup API default is used.
            structured_output_schema: If output_type is "structured", specify the output schema.
                Supported formats are a pydantic.BaseModel, a Python dictionary containing a valid
                object JSON schema, or a string representing a valid object JSON schema.
            from_date: The date from which the research sources should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, sources will
                not be filtered by a start date.
            to_date: The date until which the research sources should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, sources will
                not be filtered by an end date.
            exclude_domains: Domains to exclude from the research sources.
            include_domains: Domains to restrict the research sources to.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The newly created research task, with "pending" status and no output.

        Raises:
            TypeError: If structured_output_schema is not provided when output_type is
                "structured", or if it is not a string, dictionary, or pydantic.BaseModel when
                provided.
            LinkupInvalidRequestError: If the request parameters are invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupBudgetLimitExceededError: If the API key has reached its configured budget limit.
            LinkupTimeoutError: If the request times out.
        """
        params = self._get_research_params(
            query=query,
            output_type=output_type,
            reasoning_depth=reasoning_depth,
            mode=mode,
            structured_output_schema=structured_output_schema,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
        )

        response = self._request(
            method="POST",
            url="/research",
            json=params,
            timeout=timeout,
        )

        return self._parse_research_task(response.json())

    async def async_research(
        self,
        query: str,
        output_type: Literal["sourcedAnswer", "structured"],
        reasoning_depth: Literal["S", "M", "L", "XL"] | None = None,
        mode: Literal["answer", "auto", "investigate", "research"] | None = None,
        structured_output_schema: type[pydantic.BaseModel] | dict[str, Any] | str | None = None,
        from_date: datetime.date | str | None = None,
        to_date: datetime.date | str | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        timeout: float | None = None,
    ) -> LinkupResearchTask:
        """Asynchronously create a research task using the Linkup API /research endpoint.

        The returned task can be inspected later with async_get_research, async_list_research,
        async_get_task, or async_list_tasks.

        Args:
            query: The research query to investigate.
            output_type: The expected research output type. Use "sourcedAnswer" for an answer with
                supporting sources, or "structured" for output matching structured_output_schema.
            reasoning_depth: The amount of reasoning effort to use. If None, the Linkup API default
                is used.
            mode: The research mode to use. If None, the Linkup API default is used.
            structured_output_schema: If output_type is "structured", specify the output schema.
                Supported formats are a pydantic.BaseModel, a Python dictionary containing a valid
                object JSON schema, or a string representing a valid object JSON schema.
            from_date: The date from which the research sources should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, sources will
                not be filtered by a start date.
            to_date: The date until which the research sources should be considered. Accepts a
                datetime.date, YYYY-MM-DD, or full ISO datetime string. If None, sources will
                not be filtered by an end date.
            exclude_domains: Domains to exclude from the research sources.
            include_domains: Domains to restrict the research sources to.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The newly created research task, with "pending" status and no output.

        Raises:
            TypeError: If structured_output_schema is not provided when output_type is
                "structured", or if it is not a string, dictionary, or pydantic.BaseModel when
                provided.
            LinkupInvalidRequestError: If the request parameters are invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupBudgetLimitExceededError: If the API key has reached its configured budget limit.
            LinkupTimeoutError: If the request times out.
        """
        params = self._get_research_params(
            query=query,
            output_type=output_type,
            reasoning_depth=reasoning_depth,
            mode=mode,
            structured_output_schema=structured_output_schema,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
        )

        response = await self._async_request(
            method="POST",
            url="/research",
            json=params,
            timeout=timeout,
        )

        return self._parse_research_task(response.json())

    def list_research(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_by: Literal["createdAt", "updatedAt"] | None = None,
        sort_direction: Literal["asc", "desc"] | None = None,
        timeout: float | None = None,
    ) -> LinkupResearchTasksPage:
        """List research tasks for the authenticated organization.

        Args:
            page: The page number to retrieve. If None, the Linkup API default is used.
            page_size: The number of tasks per page. If None, the Linkup API default is used.
            sort_by: The field to sort by, either "createdAt" or "updatedAt". If None, the Linkup
                API default is used.
            sort_direction: The sort direction, either "asc" or "desc". If None, the Linkup API
                default is used.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            A paginated page of research tasks.

        Raises:
            LinkupInvalidRequestError: If the pagination or sorting parameters are invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = self._request(
            method="GET",
            url="/research",
            params=self._get_paginated_params(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_direction=sort_direction,
            ),
            timeout=timeout,
        )

        return self._parse_research_tasks_page(response.json())

    async def async_list_research(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_by: Literal["createdAt", "updatedAt"] | None = None,
        sort_direction: Literal["asc", "desc"] | None = None,
        timeout: float | None = None,
    ) -> LinkupResearchTasksPage:
        """Asynchronously list research tasks for the authenticated organization.

        Args:
            page: The page number to retrieve. If None, the Linkup API default is used.
            page_size: The number of tasks per page. If None, the Linkup API default is used.
            sort_by: The field to sort by, either "createdAt" or "updatedAt". If None, the Linkup
                API default is used.
            sort_direction: The sort direction, either "asc" or "desc". If None, the Linkup API
                default is used.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            A paginated page of research tasks.

        Raises:
            LinkupInvalidRequestError: If the pagination or sorting parameters are invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = await self._async_request(
            method="GET",
            url="/research",
            params=self._get_paginated_params(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_direction=sort_direction,
            ),
            timeout=timeout,
        )

        return self._parse_research_tasks_page(response.json())

    def get_research(self, research_id: str, timeout: float | None = None) -> LinkupResearchTask:
        """Retrieve a single research task by identifier.

        Args:
            research_id: The identifier of the research task to retrieve.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The requested research task.

        Raises:
            LinkupTaskNotFoundError: If the research identifier does not match an existing task.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = self._request(
            method="GET",
            url=f"/research/{research_id}",
            timeout=timeout,
        )

        return self._parse_research_task(response.json())

    async def async_get_research(
        self, research_id: str, timeout: float | None = None
    ) -> LinkupResearchTask:
        """Asynchronously retrieve a single research task by identifier.

        Args:
            research_id: The identifier of the research task to retrieve.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The requested research task.

        Raises:
            LinkupTaskNotFoundError: If the research identifier does not match an existing task.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = await self._async_request(
            method="GET",
            url=f"/research/{research_id}",
            timeout=timeout,
        )

        return self._parse_research_task(response.json())

    def create_tasks(
        self, tasks: list[LinkupTaskInput], timeout: float | None = None
    ) -> list[LinkupTask]:
        """Create a mixed batch of search, fetch, and research tasks.

        Args:
            tasks: The tasks to create. Supported task input models are LinkupSearchTaskInput,
                LinkupFetchTaskInput, and LinkupResearchTaskInput.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The newly created tasks with "pending" status and no output.

        Raises:
            TypeError: If a task has an unsupported model type, or if a structured output schema has
                an unsupported type.
            LinkupInvalidRequestError: If the task payload is invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupTasksQueueLimitExceededError: If too many tasks are already pending or processing.
            LinkupTimeoutError: If the request times out.
        """
        response = self._request(
            method="POST",
            url="/tasks",
            json=self._get_tasks_payload(tasks),
            timeout=timeout,
        )

        response_data = cast("list[dict[str, Any]]", response.json())
        return [self._parse_task(task) for task in response_data]

    async def async_create_tasks(
        self, tasks: list[LinkupTaskInput], timeout: float | None = None
    ) -> list[LinkupTask]:
        """Asynchronously create a mixed batch of search, fetch, and research tasks.

        Args:
            tasks: The tasks to create. Supported task input models are LinkupSearchTaskInput,
                LinkupFetchTaskInput, and LinkupResearchTaskInput.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The newly created tasks with "pending" status and no output.

        Raises:
            TypeError: If a task has an unsupported model type, or if a structured output schema has
                an unsupported type.
            LinkupInvalidRequestError: If the task payload is invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupTasksQueueLimitExceededError: If too many tasks are already pending or processing.
            LinkupTimeoutError: If the request times out.
        """
        response = await self._async_request(
            method="POST",
            url="/tasks",
            json=self._get_tasks_payload(tasks),
            timeout=timeout,
        )

        response_data = cast("list[dict[str, Any]]", response.json())
        return [self._parse_task(task) for task in response_data]

    def list_tasks(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_by: Literal["createdAt", "updatedAt"] | None = None,
        sort_direction: Literal["asc", "desc"] | None = None,
        status: Literal["pending", "processing", "completed", "failed"]
        | list[Literal["pending", "processing", "completed", "failed"]]
        | None = None,
        task_type: Literal["search", "fetch", "research"]
        | list[Literal["search", "fetch", "research"]]
        | None = None,
        timeout: float | None = None,
    ) -> LinkupTasksPage:
        """List tasks for the authenticated organization.

        Args:
            page: The page number to retrieve. If None, the Linkup API default is used.
            page_size: The number of tasks per page. If None, the Linkup API default is used.
            sort_by: The field to sort by, either "createdAt" or "updatedAt". If None, the Linkup
                API default is used.
            sort_direction: The sort direction, either "asc" or "desc". If None, the Linkup API
                default is used.
            status: One or more task statuses to filter by. If None, no status filter is sent.
            task_type: One or more task types to filter by. If None, no task type filter is sent.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            A paginated page of tasks with pagination metadata and quota information.

        Raises:
            LinkupInvalidRequestError: If the filtering, pagination, or sorting parameters are
                invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = self._request(
            method="GET",
            url="/tasks",
            params=self._get_task_list_params(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_direction=sort_direction,
                status=status,
                task_type=task_type,
            ),
            timeout=timeout,
        )

        return self._parse_tasks_page(response.json())

    async def async_list_tasks(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_by: Literal["createdAt", "updatedAt"] | None = None,
        sort_direction: Literal["asc", "desc"] | None = None,
        status: Literal["pending", "processing", "completed", "failed"]
        | list[Literal["pending", "processing", "completed", "failed"]]
        | None = None,
        task_type: Literal["search", "fetch", "research"]
        | list[Literal["search", "fetch", "research"]]
        | None = None,
        timeout: float | None = None,
    ) -> LinkupTasksPage:
        """Asynchronously list tasks for the authenticated organization.

        Args:
            page: The page number to retrieve. If None, the Linkup API default is used.
            page_size: The number of tasks per page. If None, the Linkup API default is used.
            sort_by: The field to sort by, either "createdAt" or "updatedAt". If None, the Linkup
                API default is used.
            sort_direction: The sort direction, either "asc" or "desc". If None, the Linkup API
                default is used.
            status: One or more task statuses to filter by. If None, no status filter is sent.
            task_type: One or more task types to filter by. If None, no task type filter is sent.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            A paginated page of tasks with pagination metadata and quota information.

        Raises:
            LinkupInvalidRequestError: If the filtering, pagination, or sorting parameters are
                invalid.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = await self._async_request(
            method="GET",
            url="/tasks",
            params=self._get_task_list_params(
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_direction=sort_direction,
                status=status,
                task_type=task_type,
            ),
            timeout=timeout,
        )

        return self._parse_tasks_page(response.json())

    def get_task(self, task_id: str, timeout: float | None = None) -> LinkupTask:
        """Retrieve a single task by identifier.

        Args:
            task_id: The identifier of the task to retrieve.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The requested task, parsed according to its task type.

        Raises:
            LinkupTaskNotFoundError: If the task identifier does not match an existing task.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = self._request(
            method="GET",
            url=f"/tasks/{task_id}",
            timeout=timeout,
        )

        return self._parse_task(cast("dict[str, Any]", response.json()))

    async def async_get_task(self, task_id: str, timeout: float | None = None) -> LinkupTask:
        """Asynchronously retrieve a single task by identifier.

        Args:
            task_id: The identifier of the task to retrieve.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The requested task, parsed according to its task type.

        Raises:
            LinkupTaskNotFoundError: If the task identifier does not match an existing task.
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupTimeoutError: If the request times out.
        """
        response = await self._async_request(
            method="GET",
            url=f"/tasks/{task_id}",
            timeout=timeout,
        )

        return self._parse_task(cast("dict[str, Any]", response.json()))

    def fetch(
        self,
        url: str,
        include_raw_html: bool | None = None,
        render_js: bool | None = None,
        extract_images: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupFetchResponse:
        """Fetch the content of a web page using the Linkup API /fetch endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.
            extract_images: Whether the API should extract images from the webpage and return them
                in the response.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
            LinkupFetchResponseTooLargeError: If the fetch response is too large.
            LinkupFetchUnsupportedContentTypeError: If the URL resolves to an unsupported content
                type.
            LinkupTimeoutError: If the request times out.
        """
        params: dict[str, str | bool] = self._get_fetch_params(
            url=url,
            include_raw_html=include_raw_html,
            render_js=render_js,
            extract_images=extract_images,
        )

        response: httpx.Response = self._request(
            method="POST",
            url="/fetch",
            json=params,
            timeout=timeout,
        )

        return self._parse_fetch_response(response_data=response.json())

    async def async_fetch(
        self,
        url: str,
        include_raw_html: bool | None = None,
        render_js: bool | None = None,
        extract_images: bool | None = None,
        timeout: float | None = None,
    ) -> LinkupFetchResponse:
        """Asynchronously fetch the content of a web page using the Linkup API /fetch endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.
            extract_images: Whether the API should extract images from the webpage and return them
                in the response.
            timeout: The timeout for the HTTP request, in seconds. If None, the request will have
                no timeout.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
            LinkupFetchResponseTooLargeError: If the fetch response is too large.
            LinkupFetchUnsupportedContentTypeError: If the URL resolves to an unsupported content
                type.
            LinkupTimeoutError: If the request times out.
        """
        params: dict[str, str | bool] = self._get_fetch_params(
            url=url,
            include_raw_html=include_raw_html,
            render_js=render_js,
            extract_images=extract_images,
        )

        response: httpx.Response = await self._async_request(
            method="POST",
            url="/fetch",
            json=params,
            timeout=timeout,
        )

        return self._parse_fetch_response(response_data=response.json())

    def _user_agent(self) -> str:  # pragma: no cover
        return f"Linkup-Python/{self.__version__}"

    def _headers(self) -> dict[str, str]:  # pragma: no cover
        headers: dict[str, str] = {"User-Agent": self._user_agent()}
        if self._api_key is not None:
            if self._auth_header is not None:
                headers[self._auth_header] = self._api_key.get_secret_value()
            else:
                headers["Authorization"] = f"Bearer {self._api_key.get_secret_value()}"
        return headers

    def _request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | list[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None,
    ) -> httpx.Response:
        try:
            with httpx.Client(base_url=self._base_url, headers=self._headers()) as client:
                request_kwargs: dict[str, Any] = {
                    "method": method,
                    "url": url,
                    "timeout": timeout,
                }
                if json is not None:
                    request_kwargs["json"] = json
                if params is not None:
                    request_kwargs["params"] = params
                response: httpx.Response = client.request(
                    **request_kwargs,
                )
                if response.status_code == 402 and self._x402_signer is not None:
                    return self._handle_x402_payment(
                        client=client,
                        response=response,
                        method=method,
                        url=url,
                        json=json,
                        params=params,
                        timeout=timeout,
                    )
        except httpx.TimeoutException as e:
            raise LinkupTimeoutError(
                "The request to the Linkup API timed out. Try increasing the timeout value."
            ) from e
        if response.status_code != 200:
            self._raise_linkup_error(response=response)
        return response

    async def _async_request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | list[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None,
    ) -> httpx.Response:
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url, headers=self._headers()
            ) as client:
                request_kwargs: dict[str, Any] = {
                    "method": method,
                    "url": url,
                    "timeout": timeout,
                }
                if json is not None:
                    request_kwargs["json"] = json
                if params is not None:
                    request_kwargs["params"] = params
                response: httpx.Response = await client.request(
                    **request_kwargs,
                )
                if response.status_code == 402 and self._x402_signer is not None:
                    return await self._async_handle_x402_payment(
                        client=client,
                        response=response,
                        method=method,
                        url=url,
                        json=json,
                        params=params,
                        timeout=timeout,
                    )
        except httpx.TimeoutException as e:
            raise LinkupTimeoutError(
                "The request to the Linkup API timed out. Try increasing the timeout value."
            ) from e
        if response.status_code != 200:
            self._raise_linkup_error(response=response)
        return response

    def _handle_x402_payment(
        self,
        client: httpx.Client,
        response: httpx.Response,
        method: str,
        url: str,
        json: dict[str, Any] | list[dict[str, Any]] | None,
        params: dict[str, Any] | None,
        timeout: float | None,
    ) -> httpx.Response:
        if self._x402_signer is None:
            raise RuntimeError("x402 signer is not configured")

        try:
            payment_headers = self._x402_signer.create_payment_headers(
                response_headers=dict(response.headers),
                response_body=response.content,
            )
        except Exception as e:
            raise LinkupPaymentRequiredError(
                "The Linkup API returned a payment required error (402). "
                "x402 payment signing failed.\n"
                f"Original error: {e}."
            ) from e

        merged_headers = {**self._headers(), **payment_headers}
        request_kwargs: dict[str, Any] = {
            "method": method,
            "url": url,
            "timeout": timeout,
            "headers": merged_headers,
        }
        if json is not None:
            request_kwargs["json"] = json
        if params is not None:
            request_kwargs["params"] = params
        retry_response: httpx.Response = client.request(**request_kwargs)

        if retry_response.status_code != 200:
            self._raise_linkup_error(response=retry_response)

        return retry_response

    async def _async_handle_x402_payment(
        self,
        client: httpx.AsyncClient,
        response: httpx.Response,
        method: str,
        url: str,
        json: dict[str, Any] | list[dict[str, Any]] | None,
        params: dict[str, Any] | None,
        timeout: float | None,
    ) -> httpx.Response:
        if self._x402_signer is None:
            raise RuntimeError("x402 signer is not configured")

        try:
            payment_headers = await self._x402_signer.async_create_payment_headers(
                response_headers=dict(response.headers),
                response_body=response.content,
            )
        except Exception as e:
            raise LinkupPaymentRequiredError(
                "The Linkup API returned a payment required error (402). "
                "x402 payment signing failed.\n"
                f"Original error: {e}."
            ) from e

        merged_headers = {**self._headers(), **payment_headers}
        request_kwargs: dict[str, Any] = {
            "method": method,
            "url": url,
            "timeout": timeout,
            "headers": merged_headers,
        }
        if json is not None:
            request_kwargs["json"] = json
        if params is not None:
            request_kwargs["params"] = params
        retry_response: httpx.Response = await client.request(**request_kwargs)

        if retry_response.status_code != 200:
            self._raise_linkup_error(response=retry_response)

        return retry_response

    def _raise_linkup_error(self, response: httpx.Response) -> None:
        error_data = response.json()

        if "error" in error_data:
            error = error_data["error"]
            code = error.get("code", "")
            error_msg = error.get("message", "")
            details = error.get("details", [])

            if details and isinstance(details, list):
                for detail in details:  # pyright: ignore[reportUnknownVariableType]
                    if isinstance(detail, dict):
                        field = detail.get("field", "")  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                        field_message = detail.get("message", "")  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
                        error_msg += f" {field}: {field_message}"

            if response.status_code == 402:
                raise LinkupPaymentRequiredError(
                    "The Linkup API returned a payment required error (402). "
                    "This endpoint requires x402 payment.\n"
                    f"Original error message: {error_msg}."
                )
            if response.status_code == 400:
                if code == "SEARCH_QUERY_NO_RESULT":
                    raise LinkupNoResultError(
                        "The Linkup API returned a no result error (400). "
                        "Try rephrasing you query.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "FETCH_ERROR":
                    raise LinkupFailedFetchError(
                        "The Linkup API returned a fetch error (400). "
                        "The provided URL might not be found or can't be fetched.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "FETCH_RESPONSE_TOO_LARGE":
                    raise LinkupFetchResponseTooLargeError(
                        "The Linkup API returned a fetch response too large error (400). "
                        "The provided URL's response is too large to be processed.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "FETCH_UNSUPPORTED_CONTENT_TYPE":
                    raise LinkupFetchUnsupportedContentTypeError(
                        "The Linkup API returned an unsupported content type error (400). "
                        "The provided URL does not point to a supported web page content type.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "FETCH_URL_IS_FILE":
                    raise LinkupFetchUrlIsFileError(
                        "The Linkup API returned a fetch URL is file error (400). "
                        "The provided URL points to a file and not a web page.\n"
                        f"Original error message: {error_msg}."
                    )
                raise LinkupInvalidRequestError(
                    "The Linkup API returned an invalid request error (400). Make sure the "
                    "parameters you used are valid (correct values, types, mandatory "
                    "parameters, etc.) and you are using the latest version of the Python "
                    "SDK.\n"
                    f"Original error message: {error_msg}."
                )
            if response.status_code == 401:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authentication error (401). Make sure your API "
                    "key is valid.\n"
                    f"Original error message: {error_msg}."
                )
            if response.status_code == 403:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authorization error (403). Make sure your API "
                    "key is valid.\n"
                    f"Original error message: {error_msg}."
                )
            if response.status_code == 404:
                if code == "TASK_NOT_FOUND":
                    raise LinkupTaskNotFoundError(
                        "The Linkup API returned a task not found error (404). "
                        "The requested task identifier does not exist.\n"
                        f"Original error message: {error_msg}."
                    )
                raise LinkupUnknownError(
                    f"The Linkup API returned an unknown error (404).\n"
                    f"Original error message: ({error_msg})."
                )
            if response.status_code == 429:
                if code == "INSUFFICIENT_FUNDS_CREDITS":
                    raise LinkupInsufficientCreditError(
                        "The Linkup API returned an insufficient credit error (429). Make sure "
                        "you haven't exhausted your credits.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "EXCEED_BUDGET_LIMIT":
                    raise LinkupBudgetLimitExceededError(
                        "The Linkup API returned a budget limit exceeded error (429). "
                        "The API key has reached its configured budget limit.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "TASKS_QUEUE_LIMIT_EXCEEDED":
                    raise LinkupTasksQueueLimitExceededError(
                        "The Linkup API returned a tasks queue limit exceeded error (429). "
                        "Too many tasks are already pending or processing.\n"
                        f"Original error message: {error_msg}."
                    )
                if code == "TOO_MANY_REQUESTS":
                    raise LinkupTooManyRequestsError(
                        "The Linkup API returned a too many requests error (429). Make sure "
                        "you not sending too many requests at a time.\n"
                        f"Original error message: {error_msg}."
                    )
                raise LinkupUnknownError(
                    "The Linkup API returned an invalid request error (429). Make sure the "
                    "parameters you used are valid (correct values, types, mandatory "
                    "parameters, etc.) and you are using the latest version of the Python "
                    "SDK.\n"
                    f"Original error message: {error_msg}."
                )
            raise LinkupUnknownError(
                f"The Linkup API returned an unknown error ({response.status_code}).\n"
                f"Original error message: ({error_msg})."
            )

    def _get_search_params(
        self,
        query: str,
        depth: Literal["fast", "standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[pydantic.BaseModel] | str | dict[str, Any] | None,
        include_images: bool | None,
        from_date: datetime.date | str | None,
        to_date: datetime.date | str | None,
        exclude_domains: list[str] | None,
        include_domains: list[str] | None,
        max_results: int | None,
        include_inline_citations: bool | None,
        include_sources: bool | None,
    ) -> dict[str, str | bool | int | list[str]]:
        if output_type == "structured" and structured_output_schema is None:
            raise TypeError(
                "structured_output_schema must be provided when output_type is 'structured'"
            )

        params: dict[str, str | bool | int | list[str]] = {
            "q": query,
            "depth": depth,
            "outputType": output_type,
        }

        if structured_output_schema is not None:
            if isinstance(structured_output_schema, str):
                params["structuredOutputSchema"] = structured_output_schema
            elif isinstance(structured_output_schema, dict):
                params["structuredOutputSchema"] = json.dumps(structured_output_schema)
            elif issubclass(structured_output_schema, pydantic.BaseModel):
                json_schema: dict[str, Any] = structured_output_schema.model_json_schema()
                params["structuredOutputSchema"] = json.dumps(json_schema)
            else:
                raise TypeError(
                    f"Unexpected structured_output_schema type: '{type(structured_output_schema)}'"
                )
        if include_images is not None:
            params["includeImages"] = include_images
        if from_date is not None:
            params["fromDate"] = from_date if isinstance(from_date, str) else from_date.isoformat()
        if to_date is not None:
            params["toDate"] = to_date if isinstance(to_date, str) else to_date.isoformat()
        if exclude_domains is not None:
            params["excludeDomains"] = exclude_domains
        if include_domains is not None:
            params["includeDomains"] = include_domains
        if max_results is not None:
            params["maxResults"] = max_results
        if include_inline_citations is not None:
            params["includeInlineCitations"] = include_inline_citations
        if include_sources is not None:
            params["includeSources"] = include_sources

        return params

    def _get_research_params(
        self,
        query: str,
        output_type: Literal["sourcedAnswer", "structured"],
        reasoning_depth: Literal["S", "M", "L", "XL"] | None,
        mode: Literal["answer", "auto", "investigate", "research"] | None,
        structured_output_schema: type[pydantic.BaseModel] | str | dict[str, Any] | None,
        from_date: datetime.date | str | None,
        to_date: datetime.date | str | None,
        exclude_domains: list[str] | None,
        include_domains: list[str] | None,
    ) -> dict[str, str | bool | list[str]]:
        if output_type == "structured" and structured_output_schema is None:
            raise TypeError(
                "structured_output_schema must be provided when output_type is 'structured'"
            )

        params: dict[str, str | bool | list[str]] = {
            "q": query,
            "outputType": output_type,
        }

        if reasoning_depth is not None:
            params["reasoningDepth"] = reasoning_depth
        if mode is not None:
            params["mode"] = mode

        if structured_output_schema is not None:
            if isinstance(structured_output_schema, str):
                params["structuredOutputSchema"] = structured_output_schema
            elif isinstance(structured_output_schema, dict):
                params["structuredOutputSchema"] = json.dumps(structured_output_schema)
            elif issubclass(structured_output_schema, pydantic.BaseModel):
                json_schema: dict[str, Any] = structured_output_schema.model_json_schema()
                params["structuredOutputSchema"] = json.dumps(json_schema)
            else:
                raise TypeError(
                    f"Unexpected structured_output_schema type: '{type(structured_output_schema)}'"
                )
        if from_date is not None:
            params["fromDate"] = from_date if isinstance(from_date, str) else from_date.isoformat()
        if to_date is not None:
            params["toDate"] = to_date if isinstance(to_date, str) else to_date.isoformat()
        if exclude_domains is not None:
            params["excludeDomains"] = exclude_domains
        if include_domains is not None:
            params["includeDomains"] = include_domains

        return params

    def _get_paginated_params(
        self,
        page: int | None,
        page_size: int | None,
        sort_by: Literal["createdAt", "updatedAt"] | None,
        sort_direction: Literal["asc", "desc"] | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_direction is not None:
            params["sortDirection"] = sort_direction
        return params

    def _get_task_list_params(
        self,
        page: int | None,
        page_size: int | None,
        sort_by: Literal["createdAt", "updatedAt"] | None,
        sort_direction: Literal["asc", "desc"] | None,
        status: Literal["pending", "processing", "completed", "failed"]
        | list[Literal["pending", "processing", "completed", "failed"]]
        | None,
        task_type: Literal["search", "fetch", "research"]
        | list[Literal["search", "fetch", "research"]]
        | None,
    ) -> dict[str, Any]:
        params = self._get_paginated_params(
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_direction=sort_direction,
        )
        if status is not None:
            params["status"] = status
        if task_type is not None:
            params["type"] = task_type
        return params

    def _get_tasks_payload(self, tasks: list[LinkupTaskInput]) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []

        for task in tasks:
            if isinstance(task, LinkupSearchTaskInput):
                payload.append(
                    {
                        "type": "search",
                        "input": self._get_search_params(
                            query=task.query,
                            depth=task.depth,
                            output_type=task.output_type,
                            structured_output_schema=task.structured_output_schema,
                            include_images=task.include_images,
                            from_date=task.from_date,
                            to_date=task.to_date,
                            exclude_domains=task.exclude_domains,
                            include_domains=task.include_domains,
                            max_results=task.max_results,
                            include_inline_citations=task.include_inline_citations,
                            include_sources=task.include_sources,
                        ),
                    }
                )
                continue

            if isinstance(task, LinkupFetchTaskInput):
                payload.append(
                    {
                        "type": "fetch",
                        "input": self._get_fetch_params(
                            url=task.url,
                            include_raw_html=task.include_raw_html,
                            render_js=task.render_js,
                            extract_images=task.extract_images,
                        ),
                    }
                )
                continue

            if isinstance(task, LinkupResearchTaskInput):
                payload.append(
                    {
                        "type": "research",
                        "input": self._get_research_params(
                            query=task.query,
                            output_type=task.output_type,
                            structured_output_schema=task.structured_output_schema,
                            from_date=task.from_date,
                            to_date=task.to_date,
                            exclude_domains=task.exclude_domains,
                            include_domains=task.include_domains,
                            mode=task.mode,
                            reasoning_depth=task.reasoning_depth,
                        ),
                    }
                )
                continue

            raise TypeError(f"Unexpected task model type: '{type(task)}'")

        return payload

    def _get_fetch_params(
        self,
        url: str,
        include_raw_html: bool | None,
        render_js: bool | None,
        extract_images: bool | None,
    ) -> dict[str, str | bool]:
        params: dict[str, str | bool] = {
            "url": url,
        }
        if include_raw_html is not None:
            params["includeRawHtml"] = include_raw_html
        if render_js is not None:
            params["renderJs"] = render_js
        if extract_images is not None:
            params["extractImages"] = extract_images
        return params

    def _parse_search_response(
        self,
        response_data: dict[str, Any],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        include_sources: bool | None,
    ) -> LinkupSearchResults | LinkupSourcedAnswer | JSONObject | LinkupSearchStructuredResponse:
        if output_type == "searchResults":
            return LinkupSearchResults.model_validate(response_data)
        if output_type == "sourcedAnswer":
            return LinkupSourcedAnswer.model_validate(response_data)
        if output_type == "structured":
            # HACK: we assume that include_sources will default to False, since the API output can
            # be arbitrary so we can't guess if it includes sources or not
            if include_sources:
                return LinkupSearchStructuredResponse.model_validate(response_data)
            return response_data
        raise ValueError(f"Unexpected output_type value: '{output_type}'")

    def _parse_fetch_response(self, response_data: dict[str, Any]) -> LinkupFetchResponse:
        return LinkupFetchResponse.model_validate(response_data)

    def _parse_research_task(self, task_data: dict[str, Any]) -> LinkupResearchTask:
        research_input = LinkupResearchTaskInput.model_validate(task_data["input"])
        parsed_output = task_data.get("output")
        task = LinkupResearchTask.model_validate(
            {**task_data, "input": research_input, "output": None}
        )

        # Following conversion is a bit convoluted but avoids parsing as sourced answer if using a
        # structured output schema that matches the sourced answer schema
        if parsed_output is None:
            return task
        if research_input.output_type == "sourcedAnswer":
            parsed_output = LinkupSourcedAnswer.model_validate(parsed_output)
        return task.model_copy(update={"output": parsed_output})

    def _parse_task(self, task_data: dict[str, Any]) -> LinkupTask:
        task_type = task_data["type"]

        if task_type == "search":
            search_input = LinkupSearchTaskInput.model_validate(task_data["input"])
            parsed_output = task_data.get("output")
            task = LinkupSearchTask.model_validate(
                {**task_data, "input": search_input, "output": None}
            )

            if parsed_output is not None:
                parsed_output = self._parse_search_response(
                    response_data=parsed_output,
                    output_type=search_input.output_type,
                    include_sources=search_input.include_sources,
                )
                return task.model_copy(update={"output": parsed_output})
            return task

        if task_type == "fetch":
            fetch_input = LinkupFetchTaskInput.model_validate(task_data["input"])
            parsed_output = task_data.get("output")
            if parsed_output is not None:
                parsed_output = self._parse_fetch_response(parsed_output)
            return LinkupFetchTask.model_validate(
                {**task_data, "input": fetch_input, "output": parsed_output}
            )

        if task_type == "research":
            return self._parse_research_task(task_data)

        raise ValueError(f"Unexpected task type value: '{task_type}'")

    def _parse_research_tasks_page(self, response_data: dict[str, Any]) -> LinkupResearchTasksPage:
        return LinkupResearchTasksPage.model_validate(
            {
                **response_data,
                "data": [self._parse_research_task(task) for task in response_data["data"]],
            }
        )

    def _parse_tasks_page(self, response_data: dict[str, Any]) -> LinkupTasksPage:
        return LinkupTasksPage.model_validate(
            {
                **response_data,
                "data": [self._parse_task(task) for task in response_data["data"]],
            }
        )
