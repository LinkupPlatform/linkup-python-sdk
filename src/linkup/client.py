import json
import os
from datetime import date
from typing import Any, Dict, Literal, Optional, Type, Union

import httpx
from pydantic import BaseModel

from linkup._version import __version__
from linkup.errors import (
    LinkupAuthenticationError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
    LinkupTooManyRequestsError,
    LinkupUnknownError,
)
from linkup.types import LinkupSearchResults, LinkupSourcedAnswer


class LinkupClient:
    """The Linkup Client class.

    The LinkupClient class provides functions and other tools to interact with the Linkup API in
    Python, making possible to perform search queries based on the Linkup API sources, that is the
    web and the Linkup Premium Partner sources, using natural language.

    Args:
        api_key: The API key for the Linkup API. If None, the API key will be read from the
            environment variable `LINKUP_API_KEY`.
        base_url: The base URL for the Linkup API. In general, there's no need to change this.
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
        structured_output_schema: Union[Type[BaseModel], str, None] = None,
        include_images: bool = False,
        exclude_domains: Union[list[str], None] = None,
        include_domains: Union[list[str], None] = None,
        from_date: Union[date, None] = None,
        to_date: Union[date, None] = None,
    ) -> Any:
        """
        Search for a query in the Linkup API.

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
            include_images: If output_type is "searchResults", specifies if the response can include
                images. Default to False.
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            from_date: The date from which the search results should be considered. If None, the
                search results will not be filtered by date.
            to_date: The date until which the search results should be considered. If None, the
                search results will not be filtered by date.

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
        params: Dict[str, Union[str, bool, list[str]]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            from_date=from_date,
            to_date=to_date,
        )

        response: httpx.Response = self._request(
            method="POST",
            url="/search",
            json=params,
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response)

        return self._validate_search_response(
            response=response,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
        )

    async def async_search(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[Type[BaseModel], str, None] = None,
        include_images: bool = False,
        exclude_domains: Union[list[str], None] = None,
        include_domains: Union[list[str], None] = None,
        from_date: Union[date, None] = None,
        to_date: Union[date, None] = None,
    ) -> Any:
        """
        Asynchronously search for a query in the Linkup API.

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
            include_images: If output_type is "searchResults", specifies if the response can include
                images. Default to False
            exclude_domains: If you want to exclude specific domains from your search.
            include_domains: If you want the search to only return results from certain domains.
            from_date: The date from which the search results should be considered. If None, the
                search results will not be filtered by date.
            to_date: The date until which the search results should be considered. If None, the
                search results will not be filtered by date.

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
            LinkupAuthenticationError: If the Linkup API key is invalid, or there is no more credit
                available.
        """
        params: Dict[str, Union[str, bool, list[str]]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
            exclude_domains=exclude_domains,
            include_domains=include_domains,
            from_date=from_date,
            to_date=to_date,
        )

        response: httpx.Response = await self._async_request(
            method="POST",
            url="/search",
            json=params,
            timeout=None,
        )
        if response.status_code != 200:
            self._raise_linkup_error(response)

        return self._validate_search_response(
            response=response,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
        )

    def _user_agent(self) -> str:  # pragma: no cover
        return f"Linkup-Python/{self.__version__}"

    def _headers(self) -> Dict[str, str]:  # pragma: no cover
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
            message = error.get("message", "")
            details = error.get("details", [])

            error_msg = f"{message}"
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
        structured_output_schema: Union[Type[BaseModel], str, None],
        include_images: bool,
        from_date: Union[date, None],
        include_domains: Union[list[str], None],
        exclude_domains: Union[list[str], None],
        to_date: Union[date, None],
    ) -> Dict[str, Union[str, bool, list[str]]]:
        params: Dict[str, Union[str, bool, list[str]]] = dict(
            q=query,
            depth=depth,
            outputType=output_type,
            includeImages=include_images,
        )

        if output_type == "structured" and structured_output_schema is not None:
            if isinstance(structured_output_schema, str):
                params["structuredOutputSchema"] = structured_output_schema
            elif issubclass(structured_output_schema, BaseModel):
                json_schema: Dict[str, Any] = structured_output_schema.model_json_schema()
                params["structuredOutputSchema"] = json.dumps(json_schema)
            else:
                raise TypeError(
                    f"Unexpected structured_output_schema type: '{type(structured_output_schema)}'"
                )
        if from_date is not None:
            params["fromDate"] = from_date.isoformat()
        if exclude_domains is not None:
            params["excludeDomains"] = exclude_domains
        if include_domains is not None:
            params["includeDomains"] = include_domains
        if to_date is not None:
            params["toDate"] = to_date.isoformat()

        return params

    def _validate_search_response(
        self,
        response: httpx.Response,
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[Type[BaseModel], str, None],
    ) -> Any:
        response_data: Any = response.json()
        output_base_model: Optional[Type[BaseModel]] = None
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
