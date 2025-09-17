import json
from datetime import date
from typing import Any

import pytest
from httpx import Response
from pydantic import BaseModel
from pytest_mock import MockerFixture

from linkup import (
    LinkupAuthenticationError,
    LinkupClient,
    LinkupInvalidRequestError,
    LinkupSearchResults,
    LinkupSource,
    LinkupSourcedAnswer,
    LinkupUnknownError,
)
from linkup.errors import (
    LinkupInsufficientCreditError,
    LinkupNoResultError,
    LinkupTooManyRequestsError,
)
from linkup.types import LinkupSearchImageResult, LinkupSearchTextResult


class Company(BaseModel):
    name: str
    creation_date: str
    website_url: str
    founders_names: list[str]


test_search_parameters = [
    (
        {"query": "query", "depth": "standard", "output_type": "searchResults"},
        {
            "q": "query",
            "depth": "standard",
            "outputType": "searchResults",
            "structuredOutputSchema": "",
            "includeImages": False,
            "excludeDomains": [],
            "includeDomains": [],
            "fromDate": None,
            "toDate": "2000-01-01",
        },
        b"""
        {
            "results": [
                {
                    "type": "text",
                    "name": "foo",
                    "url": "https://foo.com",
                    "content": "lorem ipsum dolor sit amet"
                },
                {"type": "image", "name": "bar", "url": "https://bar.com"}
            ]
        }
        """,
        LinkupSearchResults(
            results=[
                LinkupSearchTextResult(
                    type="text",
                    name="foo",
                    url="https://foo.com",
                    content="lorem ipsum dolor sit amet",
                ),
                LinkupSearchImageResult(
                    type="image",
                    name="bar",
                    url="https://bar.com",
                ),
            ]
        ),
    ),
    (
        {
            "query": "A long query.",
            "depth": "deep",
            "output_type": "searchResults",
            "include_images": True,
            "from_date": date(2023, 1, 1),
            "to_date": date(2023, 12, 31),
            "include_domains": ["example.com", "example.org"],
            "exclude_domains": ["excluded.com"],
        },
        {
            "q": "A long query.",
            "depth": "deep",
            "outputType": "searchResults",
            "structuredOutputSchema": "",
            "includeImages": True,
            "excludeDomains": ["excluded.com"],
            "includeDomains": ["example.com", "example.org"],
            "fromDate": "2023-01-01",
            "toDate": "2023-12-31",
        },
        b'{"results": []}',
        LinkupSearchResults(results=[]),
    ),
    (
        {"query": "query", "depth": "standard", "output_type": "sourcedAnswer"},
        {
            "q": "query",
            "depth": "standard",
            "outputType": "sourcedAnswer",
            "structuredOutputSchema": "",
            "includeImages": False,
            "excludeDomains": [],
            "includeDomains": [],
            "fromDate": None,
            "toDate": "2000-01-01",
        },
        b"""
        {
            "answer": "foo bar baz",
            "sources": [
                {"name": "foo", "url": "https://foo.com", "snippet": "lorem ipsum dolor sit amet"},
                {"name": "bar", "url": "https://bar.com", "snippet": "consectetur adipiscing elit"},
                {"name": "baz", "url": "https://baz.com"}
            ]
        }
        """,
        LinkupSourcedAnswer(
            answer="foo bar baz",
            sources=[
                LinkupSource(
                    name="foo",
                    url="https://foo.com",
                    snippet="lorem ipsum dolor sit amet",
                ),
                LinkupSource(
                    name="bar",
                    url="https://bar.com",
                    snippet="consectetur adipiscing elit",
                ),
                LinkupSource(
                    name="baz",
                    url="https://baz.com",
                    snippet="",
                ),
            ],
        ),
    ),
    (
        {
            "query": "query",
            "depth": "standard",
            "output_type": "structured",
            "structured_output_schema": Company,
        },
        {
            "q": "query",
            "depth": "standard",
            "outputType": "structured",
            "structuredOutputSchema": json.dumps(Company.model_json_schema()),
            "includeImages": False,
            "excludeDomains": [],
            "includeDomains": [],
            "fromDate": None,
            "toDate": "2000-01-01",
        },
        b"""
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/"
        }
        """,
        Company(
            name="Linkup",
            founders_names=["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            creation_date="2024",
            website_url="https://www.linkup.so/",
        ),
    ),
    (
        {
            "query": "query",
            "depth": "standard",
            "output_type": "structured",
            "structured_output_schema": json.dumps(Company.model_json_schema()),
        },
        {
            "q": "query",
            "depth": "standard",
            "outputType": "structured",
            "structuredOutputSchema": json.dumps(Company.model_json_schema()),
            "includeImages": False,
            "excludeDomains": [],
            "includeDomains": [],
            "fromDate": None,
            "toDate": "2000-01-01",
        },
        b"""
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/"
        }
        """,
        dict(
            name="Linkup",
            founders_names=["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            creation_date="2024",
            website_url="https://www.linkup.so/",
        ),
    ),
]


@pytest.mark.parametrize(
    "search_kwargs, expected_request_params, mock_request_response_content, "
    "expected_search_response",
    test_search_parameters,
)
def test_search(
    mocker: MockerFixture,
    client: LinkupClient,
    search_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_search_response: Any,
) -> None:
    mocker.patch("linkup.client.date").today.return_value = date(2000, 1, 1)
    request_mock = mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    search_response: Any = client.search(**search_kwargs)
    request_mock.assert_called_once_with(
        method="POST",
        url="/search",
        json=expected_request_params,
        timeout=None,
    )
    assert search_response == expected_search_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "search_kwargs, expected_request_params, mock_request_response_content, "
    "expected_search_response",
    test_search_parameters,
)
async def test_async_search(
    mocker: MockerFixture,
    client: LinkupClient,
    search_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_search_response: Any,
) -> None:
    mocker.patch("linkup.client.date").today.return_value = date(2000, 1, 1)
    request_mock = mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    search_response: Any = await client.async_search(**search_kwargs)
    request_mock.assert_called_once_with(
        method="POST",
        url="/search",
        json=expected_request_params,
        timeout=None,
    )
    assert search_response == expected_search_response


test_search_error_parameters = [
    (
        403,
        b"""
        {
            "error": {
                "code": "FORBIDDEN",
                "message": "Forbidden action",
                "details": []
            }
        }
        """,
        LinkupAuthenticationError,
    ),
    (
        401,
        b"""
        {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Unauthorized action",
                "details": []
            }
        }
        """,
        LinkupAuthenticationError,
    ),
    (
        429,
        b"""
        {
            "error": {
                "code": "INSUFFICIENT_FUNDS_CREDITS",
                "message": "You do not have enough credits to perform this request.",
                "details": []
            }
        }
        """,
        LinkupInsufficientCreditError,
    ),
    (
        429,
        b"""
        {
            "error": {
                "code": "TOO_MANY_REQUESTS",
                "message": "Too many requests.",
                "details": []
            }
        }
        """,
        LinkupTooManyRequestsError,
    ),
    (
        429,
        b"""
        {
            "error": {
                "code": "FOOBAR",
                "message": "Foobar",
                "details": []
            }
        }
        """,
        LinkupUnknownError,
    ),
    (
        400,
        b"""
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": [
                    {
                        "field": "structuredOutputSchema",
                        "message": "structuredOutputSchema must be valid JSON schema of type"
                    }
                ]
            }
        }
        """,
        LinkupInvalidRequestError,
    ),
    (
        400,
        b"""
        {
            "error": {
                "code": "SEARCH_QUERY_NO_RESULT",
                "message": "The query did not yield any result",
                "details": []
            }
        }
        """,
        LinkupNoResultError,
    ),
    (
        500,
        b"""
        {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
                "details": []
            }
        }
        """,
        LinkupUnknownError,
    ),
]


@pytest.mark.parametrize(
    "mock_request_response_status_code, mock_request_response_content, expected_exception",
    test_search_error_parameters,
)
def test_search_error(
    mocker: MockerFixture,
    client: LinkupClient,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: Any,
) -> None:
    request_mock = mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=mock_request_response_status_code,
            content=mock_request_response_content,
        ),
    )

    with pytest.raises(expected_exception):
        client.search(query="query", depth="standard", output_type="searchResults")
    request_mock.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_request_response_status_code, mock_request_response_content, expected_exception",
    test_search_error_parameters,
)
async def test_async_search_error(
    mocker: MockerFixture,
    client: LinkupClient,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: Any,
) -> None:
    request_mock = mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=mock_request_response_status_code,
            content=mock_request_response_content,
        ),
    )

    with pytest.raises(expected_exception):
        await client.async_search(query="query", depth="standard", output_type="searchResults")
    request_mock.assert_called_once()
