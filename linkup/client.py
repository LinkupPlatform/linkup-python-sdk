import json
import os
from typing import Any, Dict, Literal, Optional, Type, Union

import httpx
from pydantic import BaseModel

from linkup._version import __version__
from linkup.errors import (
    LinkupAuthenticationError,
    LinkupInsufficientCreditError,
    LinkupInvalidRequestError,
    LinkupNoResultError,
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
        params: Dict[str, Union[str, bool]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
        )

        response: httpx.Response = self._request(
            method="GET",
            url="/search",
            params=params,
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
        params: Dict[str, Union[str, bool]] = self._get_search_params(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
            include_images=include_images,
        )

        response: httpx.Response = await self._async_request(
            method="POST",
            url="/search",
            data=params,
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
        message: Any = response.json().get("message", "No message provided")
        message = ", ".join(message) if isinstance(message, list) else str(message)

        if response.status_code == 400:
            if message == "The query did not yield any result":
                raise LinkupNoResultError(
                    "The Linkup API returned a no result error (400). Try rephrasing you query.\n"
                    f"Original error message: {message}."
                )
            else:
                raise LinkupInvalidRequestError(
                    "The Linkup API returned an invalid request error (400). Make sure the "
                    "parameters you used are valid (correct values, types, mandatory parameters, "
                    "etc.) and you are using the latest version of the Python SDK.\n"
                    f"Original error message: {message}."
                )
        elif response.status_code == 403:
            raise LinkupAuthenticationError(
                "The Linkup API returned an authentication error (403). Make sure your API "
                "key is valid.\n"
                f"Original error message: {message}."
            )
        elif response.status_code == 429:
            raise LinkupInsufficientCreditError(
                "The Linkup API returned an insufficient credit error (429). Make sure "
                "you haven't exhausted your credits.\n"
                f"Original error message: {message}."
            )
        else:
            raise LinkupUnknownError(
                f"The Linkup API returned an unknown error ({response.status_code}).\n"
                f"Original error message: ({message})."
            )

    def _get_search_params(
        self,
        query: str,
        depth: Literal["standard", "deep"],
        output_type: Literal["searchResults", "sourcedAnswer", "structured"],
        structured_output_schema: Union[Type[BaseModel], str, None],
        include_images: bool,
    ) -> Dict[str, Union[str, bool]]:
        params: Dict[str, Union[str, bool]] = dict(
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
