import httpx
from typing import Literal
import os
from dotenv import load_dotenv

# load_dotenv()


class LinkupClient:
    """
    Linkup Client class
    """

    __version__ = "0.1.0"
    __base_url__ = "https://api.linkup.so/v1"

    def __init__(self, api_key: str = os.getenv("LINKUP_API_KEY")):
        if not api_key:
            raise ValueError("LINKUP_API_KEY is not set")
        
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
        
    def search(self, query: str, depth: Literal["standard", "deep"] = "standard") -> dict:
        """
        Search for a query in the Linkup API.

        Args:
            query (str): The search query.
            depth (Literal["standard", "deep"], optional): The depth of the search. Defaults to "standard".

        Returns:
            dict: The search results.
        """
        try:
            response = self._request("GET", "/search", params={"q": query, "depth": depth}, timeout=None)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
