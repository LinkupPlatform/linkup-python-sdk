import json
import os
from typing import Any, Literal, Type

import httpx
from pydantic import BaseModel

from linkup.errors import LinkupAuthenticationError, LinkupInvalidRequestError, LinkupUnknownError
from linkup.types import LinkupContent, LinkupSearchResults, LinkupSourcedAnswer


class LinkupClient:
    """
    The Linkup Client class.
    """

    __version__ = "0.1.0"
    __base_url__ = "https://api.linkup.so/v1"

    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = os.getenv("LINKUP_API_KEY")
        if not api_key:
            raise ValueError("The Linkup API key was not provided")

        self.api_key = api_key
        self.client = httpx.Client(base_url=self.__base_url__, headers=self._headers())

    def _user_agent(self) -> str:
        return f"Linkup-Python/{self.__version__}"

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": self._user_agent(),
        }

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        return self.client.request(
            method=method,
            url=url,
            **kwargs,
        )

    def content(self, url: str) -> LinkupContent:
        """
        Retrieve the content of a webpage of one of our Premium Sources Partners.

        Args:
            url: The URL of the webpage.

        Returns:
            The content of the webpage.

        Raises:
            LinkupInvalidRequestError: If the URL is not a valid URL in our Premium Sources
                Partners.
            LinkupAuthenticationError: If the Linkup API key is invalid, or there is no more credit
                available.
        """
        params: dict[str, str] = dict(url=url)

        response: httpx.Response = self._request(
            method="GET",
            url="/content",
            params=params,
            timeout=None,
        )
        if response.status_code != 200:
            message: Any = response.json().get("message", "No message provided")
            message = ", ".join(message) if isinstance(message, list) else str(message)
            if response.status_code == 400:
                raise LinkupInvalidRequestError(
                    "The Linkup API returned an invalid request error (400). Make sure the URL you "
                    "requested is a valid URL in our Premium Sources Partners, and you are using "
                    "the latest version of the Python SDK.\n"
                    f"Original error message: {message}."
                )
            elif response.status_code == 403:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authentication error (403). Make sure your API "
                    "key is valid, and you haven't exhausted your credits.\n"
                    f"Original error message: {message}."
                )
            else:
                raise LinkupUnknownError(
                    f"The Linkup API returned an unknown error ({response.status_code}).\n"
                    f"Original error message: ({message})."
                )

        response_data: Any = response.json()
        return LinkupContent.model_validate(response_data)

    def search(
        self,
        query: str,
        depth: Literal["standard", "deep"] = "standard",
        output_type: Literal["searchResults", "sourcedAnswer", "structured"] = "searchResults",
        structured_output_schema: Type[BaseModel] | str | None = None,
    ) -> Any:
        """
        Search for a query in the Linkup API.

        Args:
            query: The search query.
            depth: The depth of the search, "standard" (default) or "deep". Asking for a standard
                depth will make the API respond quickly. In contrast, asking for a deep depth will
                take longer for the API to respond, but results will be spot on.
            output_type: The type of output which is expected: "searchResults" (default) will output
                raw search results, "sourcedAnswer" will output the answer to the query and sources
                supporting it, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel or a string representing a
                valid object JSON schema.

        Returns:
            The Linkup API search result. If output_type is "searchResults", the result will be a
            linkup.LinkupSearchResults. If output_type is "sourcedAnswer", the result will be a
            linkup.LinkupSourcedAnswer. If output_type is "structured", the result will be either an
            instance of the provided pydantic.BaseModel, or an arbitrary data structure, following
            structured_output_schema.

        Raises:
            ValueError: If structured_output_schema is not provided when output_type is
                "structured".
            TypeError: If structured_output_schema is not a string or a pydantic.BaseModel when
                output_type is "structured".
            LinkupInvalidRequestError: If structured_output_schema doesn't represent a valid object
                JSON schema when output_type is "structured".
            LinkupAuthenticationError: If the Linkup API key is invalid, or there is no more credit
                available.
        """
        params: dict[str, str] = dict(
            q=query,
            depth=depth,
            outputType=output_type,
        )

        if output_type == "structured":
            if structured_output_schema is None:
                raise ValueError(
                    "A structured_output_schema must be provided when using "
                    "output_type='structured'"
                )

            if isinstance(structured_output_schema, str):
                params["structuredOutputSchema"] = structured_output_schema
            elif issubclass(structured_output_schema, BaseModel):
                json_schema: dict[str, Any] = structured_output_schema.model_json_schema()
                params["structuredOutputSchema"] = json.dumps(json_schema)
            else:
                raise TypeError(
                    f"Unexpected structured_output_schema type: '{type(structured_output_schema)}'"
                )

        response: httpx.Response = self._request(
            method="GET",
            url="/search",
            params=params,
            timeout=None,
        )
        if response.status_code != 200:
            message: Any = response.json().get("message", "No message provided")
            message = ", ".join(message) if isinstance(message, list) else str(message)
            if response.status_code == 400:
                raise LinkupInvalidRequestError(
                    "The Linkup API returned an invalid request error (400). Make sure the "
                    "parameters you are using are valid, (e.g. structured_output_schema must be a "
                    "valid object schema if output_type is 'structured'), and you are using the "
                    "latest version of the Python SDK.\n"
                    f"Original error message: {message}."
                )
            elif response.status_code == 403:
                raise LinkupAuthenticationError(
                    "The Linkup API returned an authentication error (403). Make sure your API "
                    "key is valid, and you haven't exhausted your credits.\n"
                    f"Original error message: {message}."
                )
            else:
                raise LinkupUnknownError(
                    f"The Linkup API returned an unknown error ({response.status_code}).\n"
                    f"Original error message: ({message})."
                )

        response_data: Any = response.json()
        output_base_model: Type[BaseModel] | None = None
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
