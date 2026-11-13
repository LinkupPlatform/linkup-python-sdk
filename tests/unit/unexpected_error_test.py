import httpx
import pytest
from pytest_mock import MockerFixture

import linkup


@pytest.mark.parametrize(
    "body",
    [
        b"<html>Bad Gateway</html>",
        b"",
        b"Bad Gateway",
        b"null",
        b"[]",
        b'{"message": "upstream unavailable"}',
        b'{"error": "upstream unavailable"}',
        b'{"error": null}',
        b'{"error": {"message": "upstream unavailable"}}',
    ],
)
def test_unexpected_error_response(
    body: bytes, mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch("httpx.Client.request", return_value=httpx.Response(502, content=body))

    with pytest.raises(linkup.UnknownError, match="502"):
        client.search(query="test", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        b"<html>Bad Gateway</html>",
        b"",
        b"Bad Gateway",
        b"null",
        b"[]",
        b'{"message": "upstream unavailable"}',
        b'{"error": "upstream unavailable"}',
        b'{"error": null}',
        b'{"error": {"message": "upstream unavailable"}}',
    ],
)
async def test_async_unexpected_error_response(
    body: bytes, mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch("httpx.AsyncClient.request", return_value=httpx.Response(502, content=body))

    with pytest.raises(linkup.UnknownError, match="502"):
        await client.async_search(query="test", depth="standard", output_type="searchResults")
