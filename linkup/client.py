import json
import os
from typing import Any, Literal, Type

import httpx
from pydantic import BaseModel, ValidationError

from linkup.types import LinkupSearchResults, LinkupSourcedAnswer


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

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        return self.client.request(method, path, **kwargs)

    def search(
        self,
        query: str,
        depth: Literal["standard", "deep"] = "standard",
        output_type: Literal["sourcedAnswer", "searchResults", "structured"] = "sourcedAnswer",
        structured_output_schema: Type[BaseModel] | str | None = None,
    ) -> Any:
        """
        Search for a query in the Linkup API.

        Args:
            query: The search query.
            depth: The depth of the search, "standard" (default) or "deep". Asking for a standard
                depth will make the API respond quickly. In contrast, asking for a deep depth will
                take longer for the API to respond, but results will be spot on.
            output_type: The type of output which is expected: "sourcedAnswer" (default) will output
                the answer to the query and sources supporting it, "searchResults" will output raw
                search results, and "structured" will base the output on the format provided in
                structured_output_schema.
            structured_output_schema: If output_type is "structured", specify the schema of the
                output. Supported formats are a pydantic.BaseModel or a string representing a
                valid object JSON schema.

        Returns:
            The Linkup API search result. If output_type is "sourcedAnswer", the result will be a
            linkup.LinkupSourcedAnswer. If output_type is "searchResults", the result will be a
            linkup.LinkupSearchResults. If output_type is "structured", the result will be either an
            instance of the provided pydantic.BaseModel, or an arbitrary data structure, following
            structured_output_schema.
        """
        params = dict(
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

        try:
            response: httpx.Response = self._request(
                method="GET",
                path="/search",
                params=params,
                timeout=None,
            )
        except Exception as e:
            raise Exception(f"Something went wrong during the API call: '{e}'")

        response_data: Any = response.json()

        output_base_model: Type[BaseModel] | None = None
        if output_type == "sourcedAnswer":
            output_base_model = LinkupSourcedAnswer
        elif output_type == "searchResults":
            output_base_model = LinkupSearchResults
        elif (
            output_type == "structured"
            and not isinstance(structured_output_schema, (str, type(None)))
            and issubclass(structured_output_schema, BaseModel)
        ):
            output_base_model = structured_output_schema

        if output_base_model is None:
            return response_data

        try:
            return output_base_model.model_validate(response_data)
        except ValidationError:
            raise ValueError(
                f"The response data format doesn't match the required format of "
                f"'{output_base_model}': '{response_data}'"
            )
