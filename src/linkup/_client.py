"""Linkup client, the entrypoint for Linkup functions."""

from __future__ import annotations

import json
import os
from datetime import date  # noqa: TC003 (`date` is used in test mocks)
from typing import Any, Literal

import httpx
from pydantic import BaseModel, SecretStr

from ._errors import (
    LinkupAuthenticationError,
    LinkupFailedFetchError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
    LinkupTooManyRequestsError,
    LinkupUnknownError,
)
from ._types import (
    LinkupFetchResponse,
    LinkupSearchResults,
    LinkupSearchStructuredResponse,
    LinkupSourcedAnswer,
)
from ._version import __version__


class LinkupClient:
    """The Linkup Client class, providing functions to call the Linkup API endpoints using Python.

    Args:
        api_key: The API key for the Linkup API. If None, the API key will be read from the
            environment variable `LINKUP_API_KEY`.
        base_url: The base URL for the Linkup API, for development purposes.

    Raises:
        ValueError: If the API key is not provided and not found in the environment variable.
    """

    __version__ = __version__

    def __init__(
        self,
        api_key: str | SecretStr | None = None,
        base_url: str = "https://api.linkup.so/v1",
    ) -> None:
        if api_key is None:
            api_key = os.getenv("LINKUP_API_KEY")
        if not api_key:
            raise ValueError("The Linkup API key was not provided")
        if isinstance(api_key, str):
            api_key = SecretStr(api_key)

        self._api_key: SecretStr = api_key
        self._base_url: str = base_url

    def search(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[BaseModel] | str | None = None,
        include_images: bool | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
    ) -> Any:  # noqa: ANN401
        """Perform a web search using the Linkup API `search` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search).

        Args:
            query: The search query.
            depth: The depth of the search. Can be either "standard", for a straighforward and
                fast search, or "deep" for a more powerful agentic workflow.
            output_type: The type of output which is expected: "searchResults" will output raw
                search results, "sourcedAnswer" will output the answer to the query and sources
                supporting it, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel or a string representing a
                valid object JSON schema.
            include_images: Indicate whether images should be included during the search.
            from_date: The date from which the search results should be considered. If None, the
                search results will not be filtered by date.
            to_date: The date until which the search results should be considered. If None, the
                search results will not be filtered by date.
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            max_results: The maximum number of results to return.
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.
            include_sources: If output_type is "structured", indicate whether the answer should
                include sources. This will modify the schema of the structured response.

        Returns:
            The Linkup API search result, which can have different types based on the parameters:
            - LinkupSearchResults if output_type is "searchResults"
            - LinkupSourcedAnswer if output_type is "sourcedAnswer"
            - the provided pydantic.BaseModel or an arbitrary data structure if output_type is
              "structured" and include_sources is False
            - LinkupSearchStructuredResponse with the provided pydantic.BaseModel or an arbitrary
              data structure as data field, if output_type is "structured" and include_sources is
              True

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string or a
                pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupNoResultError: If the search query did not yield any result.
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
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response=response)

        return self._parse_search_response(
            response=response,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_sources=include_sources,
        )

    async def async_search(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[BaseModel] | str | None = None,
        include_images: bool | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        exclude_domains: list[str] | None = None,
        include_domains: list[str] | None = None,
        max_results: int | None = None,
        include_inline_citations: bool | None = None,
        include_sources: bool | None = None,
    ) -> Any:  # noqa: ANN401
        """Asynchronously perform a web search using the Linkup API `search` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-search).

        Args:
            query: The search query.
            depth: The depth of the search. Can be either "standard", for a straighforward and
                fast search, or "deep" for a more powerful agentic workflow.
            output_type: The type of output which is expected: "searchResults" will output raw
                search results, "sourcedAnswer" will output the answer to the query and sources
                supporting it, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel or a string representing a
                valid object JSON schema.
            include_images: Indicate whether images should be included during the search.
            from_date: The date from which the search results should be considered. If None, the
                search results will not be filtered by date.
            to_date: The date until which the search results should be considered. If None, the
                search results will not be filtered by date.
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            max_results: The maximum number of results to return.
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.
            include_sources: If output_type is "structured", indicate whether the answer should
                include sources. This will modify the schema of the structured response.

        Returns:
            The Linkup API search result, which can have different types based on the parameters:
            - LinkupSearchResults if output_type is "searchResults"
            - LinkupSourcedAnswer if output_type is "sourcedAnswer"
            - the provided pydantic.BaseModel or an arbitrary data structure if output_type is
              "structured" and include_sources is False
            - LinkupSearchStructuredResponse with the provided pydantic.BaseModel or an arbitrary
              data structure as data field, if output_type is "structured" and include_sources is
              True

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string or a
                pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupNoResultError: If the search query did not yield any result.
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
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response=response)

        return self._parse_search_response(
            response=response,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_sources=include_sources,
        )

    def fetch(
        self,
        url: str,
        include_raw_html: bool | None = None,
        render_js: bool | None = None,
        extract_images: bool | None = None,
    ) -> LinkupFetchResponse:
        """Fetch the content of a web page using the Linkup API `fetch` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.
            extract_images: Whether the API should extract images from the webpage and return them
                in the response.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
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
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response=response)

        return self._parse_fetch_response(response=response)

    async def async_fetch(
        self,
        url: str,
        include_raw_html: bool | None = None,
        render_js: bool | None = None,
        extract_images: bool | None = None,
    ) -> LinkupFetchResponse:
        """Asynchronously fetch the content of a web page using the Linkup API `fetch` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.
            extract_images: Whether the API should extract images from the webpage and return them
                in the response.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
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
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response=response)

        return self._parse_fetch_response(response=response)

    def _user_agent(self) -> str:  # pragma: no cover
        return f"Linkup-Python/{self.__version__}"

    def _headers(self) -> dict[str, str]:  # pragma: no cover
        return {
            "Authorization": f"Bearer {self._api_key.get_secret_value()}",
            "User-Agent": self._user_agent(),
        }

    def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:  # pragma: no cover
        with httpx.Client(base_url=self._base_url, headers=self._headers()) as client:
            return client.request(
                method=method,
                url=url,
                **kwargs,
            )

    async def _async_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> httpx.Response:  # pragma: no cover
        async with httpx.AsyncClient(base_url=self._base_url, headers=self._headers()) as client:
            return await client.request(
                method=method,
                url=url,
                **kwargs,
            )

    def _raise_linkup_error(self, response: httpx.Response) -> None:
        error_data = response.json()

        if "error" in error_data:
            error = error_data["error"]
            code = error.get("code", "")
            error_msg = error.get("message", "")
            details = error.get("details", [])

            if details and isinstance(details, list):
                for detail in details:
                    if isinstance(detail, dict):
                        field = detail.get("field", "")
                        field_message = detail.get("message", "")
                        error_msg += f" {field}: {field_message}"

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
            if response.status_code == 429:
                if code == "INSUFFICIENT_FUNDS_CREDITS":
                    raise LinkupInsufficientCreditError(
                        "The Linkup API returned an insufficient credit error (429). Make sure "
                        "you haven't exhausted your credits.\n"
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
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[BaseModel] | str | None,
        include_images: bool | None,
        from_date: date | None,
        to_date: date | None,
        exclude_domains: list[str] | None,
        include_domains: list[str] | None,
        max_results: int | None,
        include_inline_citations: bool | None,
        include_sources: bool | None,
    ) -> dict[str, str | bool | int | list[str]]:
        params: dict[str, str | bool | int | list[str]] = {
            "q": query,
            "depth": depth,
            "outputType": output_type,
        }

        if structured_output_schema is not None:
            if isinstance(structured_output_schema, str):
                params["structuredOutputSchema"] = structured_output_schema
            elif issubclass(structured_output_schema, BaseModel):
                json_schema: dict[str, Any] = structured_output_schema.model_json_schema()
                params["structuredOutputSchema"] = json.dumps(json_schema)
            else:
                raise TypeError(
                    f"Unexpected structured_output_schema type: '{type(structured_output_schema)}'"
                )
        if include_images is not None:
            params["includeImages"] = include_images
        if from_date is not None:
            params["fromDate"] = from_date.isoformat()
        if to_date is not None:
            params["toDate"] = to_date.isoformat()
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
        response: httpx.Response,
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: type[BaseModel] | str | None,
        include_sources: bool | None,
    ) -> Any:  # noqa: ANN401
        response_data: Any = response.json()
        if output_type == "searchResults":
            return LinkupSearchResults.model_validate(response_data)
        if output_type == "sourcedAnswer":
            return LinkupSourcedAnswer.model_validate(response_data)
        if output_type == "structured":
            if structured_output_schema is None:
                raise ValueError(
                    "structured_output_schema must be provided when output_type is 'structured'"
                )
            # HACK: we assume that `include_sources` will default to False, since the API output can
            # be arbitrary so we can't guess if it includes sources or not
            if include_sources:
                if not isinstance(structured_output_schema, str) and issubclass(
                    structured_output_schema, BaseModel
                ):
                    response_data["data"] = structured_output_schema.model_validate(
                        response_data["data"]
                    )
                return LinkupSearchStructuredResponse.model_validate(response_data)
            if not isinstance(structured_output_schema, str) and issubclass(
                structured_output_schema, BaseModel
            ):
                return structured_output_schema.model_validate(response_data)
            return response_data
        raise ValueError(f"Unexpected output_type value: '{output_type}'")

    def _parse_fetch_response(self, response: httpx.Response) -> LinkupFetchResponse:
        return LinkupFetchResponse.model_validate(response.json())
