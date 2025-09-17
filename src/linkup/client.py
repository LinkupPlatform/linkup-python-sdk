import json
import os
from datetime import date
from typing import Any, Literal, Optional, Union

import httpx
from pydantic import BaseModel

from linkup._version import __version__
from linkup.errors import (
    LinkupAuthenticationError,
    LinkupFailedFetchError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
    LinkupTooManyRequestsError,
    LinkupUnknownError,
)
from linkup.types import LinkupFetchResponse, LinkupSearchResults, LinkupSourcedAnswer


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
        api_key: Optional[str] = None,
        base_url: str = "https://api.linkup.so/v1",
    ) -> None:
        if api_key is None:
            api_key = os.getenv("LINKUP_API_KEY")
        if not api_key:
            raise ValueError("The Linkup API key was not provided")

        self.__api_key = api_key
        self.__base_url = base_url

    def search(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[type[BaseModel], str, None] = None,
        include_images: Optional[bool] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        exclude_domains: Optional[list[str]] = None,
        include_domains: Optional[list[str]] = None,
        include_inline_citations: Optional[bool] = None,
    ) -> Any:
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
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.

        Returns:
            The Linkup API search result. If output_type is "searchResults", the result will be a
                linkup.LinkupSearchResults. If output_type is "sourcedAnswer", the result will be a
                linkup.LinkupSourcedAnswer. If output_type is "structured", the result will be
                either an instance of the provided pydantic.BaseModel, or an arbitrary data
                structure, following structured_output_schema.

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string or a
                pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupNoResultError: If the search query did not yield any result.
        """
        params: dict[str, Union[str, bool, list[str]]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            include_inline_citations=include_inline_citations,
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
        )

    async def async_search(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[type[BaseModel], str, None] = None,
        include_images: Optional[bool] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        exclude_domains: Optional[list[str]] = None,
        include_domains: Optional[list[str]] = None,
        include_inline_citations: Optional[bool] = None,
    ) -> Any:
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
            include_inline_citations: If output_type is "sourcedAnswer", indicate whether the
                answer should include inline citations.

        Returns:
            The Linkup API search result. If output_type is "searchResults", the result will be a
                linkup.LinkupSearchResults. If output_type is "sourcedAnswer", the result will be a
                linkup.LinkupSourcedAnswer. If output_type is "structured", the result will be
                either an instance of the provided pydantic.BaseModel, or an arbitrary data
                structure, following structured_output_schema.

        Raises:
            TypeError: If structured_output_schema is not provided or is not a string or a
                pydantic.BaseModel when output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid.
            LinkupInsufficientCreditError: If you have run out of credit.
            LinkupNoResultError: If the search query did not yield any result.
        """
        params: dict[str, Union[str, bool, list[str]]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            from_date=from_date,
            to_date=to_date,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            include_inline_citations=include_inline_citations,
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
        )

    def fetch(
        self,
        url: str,
        include_raw_html: Optional[bool] = None,
        render_js: Optional[bool] = None,
    ) -> LinkupFetchResponse:
        """Fetch the content of a web page using the Linkup API `fetch` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
        """
        params: dict[str, Union[str, bool]] = self._get_fetch_params(
            url=url,
            include_raw_html=include_raw_html,
            render_js=render_js,
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
        include_raw_html: Optional[bool] = None,
        render_js: Optional[bool] = None,
    ) -> LinkupFetchResponse:
        """Asynchronously fetch the content of a web page using the Linkup API `fetch` endpoint.

        All optional parameters will default to the Linkup API defaults when not provided. The
        Linkup API defaults are available in the
        [official documentation](https://docs.linkup.so/pages/documentation/api-reference/endpoint/post-fetch).

        Args:
            url: The URL of the web page to fetch.
            include_raw_html: Whether to include the raw HTML of the webpage in the response.
            render_js: Whether the API should render the JavaScript of the webpage.

        Returns:
            The response of the web page fetch, containing the web page content.

        Raises:
            LinkupInvalidRequestError: If the provided URL is not valid.
            LinkupFailedFetchError: If the provided URL is not found or can't be fetched.
        """
        params: dict[str, Union[str, bool]] = self._get_fetch_params(
            url=url,
            include_raw_html=include_raw_html,
            render_js=render_js,
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
            "Authorization": f"Bearer {self.__api_key}",
            "User-Agent": self._user_agent(),
        }

    def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:  # pragma: no cover
        with httpx.Client(base_url=self.__base_url, headers=self._headers()) as client:
            return client.request(
                method=method,
                url=url,
                **kwargs,
            )

    async def _async_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:  # pragma: no cover
        async with httpx.AsyncClient(base_url=self.__base_url, headers=self._headers()) as client:
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
                else:
                    raise LinkupInvalidRequestError(
                        "The Linkup API returned an invalid request error (400). Make sure the "
                        "parameters you used are valid (correct values, types, mandatory "
                        "parameters, etc.) and you are using the latest version of the Python "
                        "SDK.\n"
                        f"Original error message: {error_msg}."
                    )
            elif response.status_code == 401:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authentication error (401). Make sure your API "
                    "key is valid.\n"
                    f"Original error message: {error_msg}."
                )
            elif response.status_code == 403:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authorization error (403). Make sure your API "
                    "key is valid.\n"
                    f"Original error message: {error_msg}."
                )
            elif response.status_code == 429:
                if code == "INSUFFICIENT_FUNDS_CREDITS":
                    raise LinkupInsufficientCreditError(
                        "The Linkup API returned an insufficient credit error (429). Make sure "
                        "you haven't exhausted your credits.\n"
                        f"Original error message: {error_msg}."
                    )
                elif code == "TOO_MANY_REQUESTS":
                    raise LinkupTooManyRequestsError(
                        "The Linkup API returned a too many requests error (429). Make sure "
                        "you not sending too many requests at a time.\n"
                        f"Original error message: {error_msg}."
                    )
                else:
                    raise LinkupUnknownError(
                        "The Linkup API returned an invalid request error (429). Make sure the "
                        "parameters you used are valid (correct values, types, mandatory "
                        "parameters, etc.) and you are using the latest version of the Python "
                        "SDK.\n"
                        f"Original error message: {error_msg}."
                    )
            else:
                raise LinkupUnknownError(
                    f"The Linkup API returned an unknown error ({response.status_code}).\n"
                    f"Original error message: ({error_msg})."
                )

    def _get_search_params(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[type[BaseModel], str, None],
        include_images: Optional[bool],
        from_date: Optional[date],
        to_date: Optional[date],
        exclude_domains: Optional[list[str]],
        include_domains: Optional[list[str]],
        include_inline_citations: Optional[bool],
    ) -> dict[str, Union[str, bool, list[str]]]:
        params: dict[str, Union[str, bool, list[str]]] = dict(
            q=query,
            depth=depth,
            outputType=output_type,
        )

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
        if include_inline_citations is not None:
            params["includeInlineCitations"] = include_inline_citations

        return params

    def _get_fetch_params(
        self,
        url: str,
        include_raw_html: Optional[bool],
        render_js: Optional[bool],
    ) -> dict[str, Union[str, bool]]:
        params: dict[str, Union[str, bool]] = {
            "url": url,
        }
        if include_raw_html is not None:
            params["includeRawHtml"] = include_raw_html
        if render_js is not None:
            params["renderJs"] = render_js
        return params

    def _parse_search_response(
        self,
        response: httpx.Response,
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[type[BaseModel], str, None],
    ) -> Any:
        response_data: Any = response.json()
        output_base_model: Optional[type[BaseModel]] = None
        if output_type == "searchResults":
            output_base_model = LinkupSearchResults
        elif output_type == "sourcedAnswer":
            output_base_model = LinkupSourcedAnswer
        elif (
            output_type == "structured"
            and not isinstance(structured_output_schema, (str, type(None)))
            and issubclass(structured_output_schema, BaseModel)
        ):
            output_base_model = structured_output_schema

        if output_base_model is None:
            return response_data
        return output_base_model.model_validate(response_data)

    def _parse_fetch_response(self, response: httpx.Response) -> LinkupFetchResponse:
        return LinkupFetchResponse.model_validate(response.json())
