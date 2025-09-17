import os

import pytest

from linkup import LinkupClient


@pytest.fixture(scope="session")
def client() -> LinkupClient:
    if os.getenv("LINKUP_API_KEY") is None:
        os.environ["LINKUP_API_KEY"] = "<linkup-api-key>"
    return LinkupClient()
