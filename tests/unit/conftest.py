import os
from unittest.mock import MagicMock

import pytest

from linkup import LinkupClient
from linkup.x402 import LinkupX402Signer


@pytest.fixture(scope="session")
def client() -> LinkupClient:
    if os.getenv("LINKUP_API_KEY") is None:
        os.environ["LINKUP_API_KEY"] = "<linkup-api-key>"
    return LinkupClient()


@pytest.fixture
def mock_x402_signer() -> MagicMock:
    return MagicMock(spec=LinkupX402Signer)


@pytest.fixture
def x402_client(mock_x402_signer: MagicMock) -> LinkupClient:
    return LinkupClient(x402_signer=mock_x402_signer)
