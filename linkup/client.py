import httpx
from typing import Any, Literal
import os
from dataclasses import dataclass


@dataclass
class LinkupClientSource:
    """
    A source supporting the content a Linkup Client response.

    Attributes:
        name (str): The name of the source.
        url (str): The URL of the source.
        snippet (str): The snippet of the source content supporting the Linkup Client response.
    """

    name: str
    url: str
    snippet: str


@dataclass
class LinkupClientResponse:
    """
    A response of the Linkup Client.

    Attributes:
        content (Any): The content of the response.
        sources (list[LinkupClientSource]): The sources supporting the response.
    """

    content: Any
    sources: list[LinkupClientSource]


class LinkupClient:
    """
    Linkup Client class
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
    ) -> LinkupClientResponse:
        """
        Search for a query in the Linkup API.

        Args:
            query (str): The search query.
            depth (Literal["standard", "deep"], optional): The depth of the search. Defaults to "standard".

        Returns:
            LinkupClientResponse: The search results.
        """
        try:
            response: httpx.Response = self._request(
                method="GET",
                path="/search",
                params={"q": query, "depth": depth},
                timeout=None,
            )
            response_data: dict[str, Any] = response.json()

            if "content" not in response_data or "sources" not in response_data:
                raise ValueError("Unexpected response format of Linkup API")
            content: Any = response_data["content"]
            sources: list[LinkupClientSource] = []
            for source_data in response_data["sources"]:
                if (
                    "name" not in source_data
                    or "url" not in source_data
                    or "snippet" not in source_data
                ):
                    raise ValueError("Unexpected response format of Linkup API sources")
                source = LinkupClientSource(
                    name=source_data["name"],
                    url=source_data["url"],
                    snippet=source_data["snippet"],
                )
                sources.append(source)

            return LinkupClientResponse(content=content, sources=sources)

        except Exception as e:
            raise Exception(f"Something went wrong: {e}")
