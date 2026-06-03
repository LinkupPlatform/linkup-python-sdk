import json
from datetime import date
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock

import httpx
import pydantic
import pytest
from httpx import Response
from pytest_mock import MockerFixture

import linkup


class Company(pydantic.BaseModel):
    name: str
    creation_date: str
    website_url: str
    founders_names: list[str]


test_search_parameters = [
    (
        {"query": "query", "depth": "standard", "output_type": "searchResults"},
        {"q": "query", "depth": "standard", "outputType": "searchResults"},
        b"""
        {
            "results": [
                {
                    "type": "text",
                    "name": "foo",
                    "url": "https://foo.com",
                    "content": "lorem ipsum dolor sit amet",
                    "favicon": "https://foo.com/favicon.ico"
                },
                {"type": "image", "name": "bar", "url": "https://bar.com"}
            ]
        }
        """,
        linkup.SearchResults(
            results=[
                linkup.SearchTextResult(
                    type="text",
                    name="foo",
                    url="https://foo.com",
                    content="lorem ipsum dolor sit amet",
                    favicon="https://foo.com/favicon.ico",
                ),
                linkup.SearchImageResult(
                    type="image",
                    name="bar",
                    url="https://bar.com",
                ),
            ]
        ),
    ),
    (
        {"query": "query", "depth": "fast", "output_type": "searchResults"},
        {"q": "query", "depth": "fast", "outputType": "searchResults"},
        b'{"results": []}',
        linkup.SearchResults(results=[]),
    ),
    (
        {
            "query": "A long query.",
            "depth": "deep",
            "output_type": "searchResults",
            "include_images": True,
            "from_date": date(2023, 1, 1),
            "to_date": date(2023, 12, 31),
            "exclude_domains": ["excluded.com"],
            "include_domains": ["example.com", "example.org"],
            "max_results": 10,
            "include_inline_citations": True,
            "include_sources": True,
        },
        {
            "q": "A long query.",
            "depth": "deep",
            "outputType": "searchResults",
            "includeImages": True,
            "fromDate": "2023-01-01",
            "toDate": "2023-12-31",
            "excludeDomains": ["excluded.com"],
            "includeDomains": ["example.com", "example.org"],
            "maxResults": 10,
            "includeInlineCitations": True,
            "includeSources": True,
        },
        b'{"results": []}',
        linkup.SearchResults(results=[]),
    ),
    (
        {
            "query": "query",
            "depth": "standard",
            "output_type": "searchResults",
            "from_date": "2026-05-01T08:15:30.000Z",
            "to_date": "2026-05-31T23:59:59.000Z",
        },
        {
            "q": "query",
            "depth": "standard",
            "outputType": "searchResults",
            "fromDate": "2026-05-01T08:15:30.000Z",
            "toDate": "2026-05-31T23:59:59.000Z",
        },
        b'{"results": []}',
        linkup.SearchResults(results=[]),
    ),
    (
        {
            "query": "query with timeout",
            "depth": "standard",
            "output_type": "searchResults",
            "timeout": 30.0,
        },
        {"q": "query with timeout", "depth": "standard", "outputType": "searchResults"},
        b'{"results": []}',
        linkup.SearchResults(results=[]),
    ),
    (
        {"query": "query", "depth": "standard", "output_type": "sourcedAnswer"},
        {"q": "query", "depth": "standard", "outputType": "sourcedAnswer"},
        b"""
        {
            "answer": "foo bar baz",
            "sources": [
                {
                    "name": "foo",
                    "url": "https://foo.com",
                    "snippet": "lorem ipsum dolor sit amet",
                    "favicon": "https://foo.com/favicon.ico"
                },
                {
                    "name": "bar",
                    "url": "https://bar.com",
                    "snippet": "consectetur adipiscing elit",
                    "favicon": "https://bar.com/favicon.ico"
                },
                {
                    "name": "baz",
                    "url": "https://baz.com",
                    "snippet": "",
                    "favicon": ""
                }
            ]
        }
        """,
        linkup.SourcedAnswer(
            answer="foo bar baz",
            sources=[
                linkup.Source(
                    name="foo",
                    url="https://foo.com",
                    snippet="lorem ipsum dolor sit amet",
                    favicon="https://foo.com/favicon.ico",
                ),
                linkup.Source(
                    name="bar",
                    url="https://bar.com",
                    snippet="consectetur adipiscing elit",
                    favicon="https://bar.com/favicon.ico",
                ),
                linkup.Source(
                    name="baz",
                    url="https://baz.com",
                    snippet="",
                    favicon="",
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
        },
        b"""
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/"
        }
        """,
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/",
        },
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
        },
        b"""
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/"
        }
        """,
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/",
        },
    ),
    (
        {
            "query": "query",
            "depth": "standard",
            "output_type": "structured",
            "structured_output_schema": Company.model_json_schema(),
        },
        {
            "q": "query",
            "depth": "standard",
            "outputType": "structured",
            "structuredOutputSchema": json.dumps(Company.model_json_schema()),
        },
        b"""
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/"
        }
        """,
        {
            "name": "Linkup",
            "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            "creation_date": "2024",
            "website_url": "https://www.linkup.so/",
        },
    ),
    (
        {
            "query": "query",
            "depth": "standard",
            "output_type": "structured",
            "structured_output_schema": Company,
            "include_sources": True,
        },
        {
            "q": "query",
            "depth": "standard",
            "outputType": "structured",
            "structuredOutputSchema": json.dumps(Company.model_json_schema()),
            "includeSources": True,
        },
        b"""
        {
            "data": {
                "name": "Linkup",
                "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
                "creation_date": "2024",
                "website_url": "https://www.linkup.so/"
            },
            "sources": [
                {
                    "type": "text",
                    "name": "foo",
                    "url": "https://foo.com",
                    "content": "lorem ipsum dolor sit amet",
                    "favicon": "https://foo.com/favicon.ico"
                },
                {"type": "image", "name": "bar", "url": "https://bar.com"}
            ]
        }
        """,
        linkup.SearchStructuredResponse(
            data={
                "name": "Linkup",
                "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
                "creation_date": "2024",
                "website_url": "https://www.linkup.so/",
            },
            sources=[
                linkup.SearchTextResult(
                    type="text",
                    name="foo",
                    url="https://foo.com",
                    content="lorem ipsum dolor sit amet",
                    favicon="https://foo.com/favicon.ico",
                ),
                linkup.SearchImageResult(type="image", name="bar", url="https://bar.com"),
            ],
        ),
    ),
]


@pytest.mark.parametrize(
    (
        "search_kwargs",
        "expected_request_params",
        "mock_request_response_content",
        "expected_search_response",
    ),
    test_search_parameters,
)
def test_search(
    mocker: MockerFixture,
    client: linkup.Client,
    search_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_search_response: Any,  # noqa: ANN401
) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    search_response = cast("Any", client.search(**search_kwargs))
    expected_timeout = search_kwargs.get("timeout", None)
    request_mock.assert_called_once_with(
        method="POST",
        url="/search",
        json=expected_request_params,
        timeout=expected_timeout,
    )
    assert search_response == expected_search_response


def test_search_structured_output_model_dump_preserves_data(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "data": {
                    "name": "Linkup",
                    "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
                    "creation_date": "2024",
                    "website_url": "https://www.linkup.so/"
                },
                "sources": []
            }
            """,
        ),
    )

    search_response = client.search(
        query="query",
        depth="standard",
        output_type="structured",
        structured_output_schema=Company,
        include_sources=True,
    )

    assert search_response.model_dump()["data"] == {
        "name": "Linkup",
        "founders_names": ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
        "creation_date": "2024",
        "website_url": "https://www.linkup.so/",
    }


def test_search_structured_output_requires_schema(client: linkup.Client) -> None:
    with pytest.raises(
        TypeError,
        match="structured_output_schema must be provided",
    ):
        client.search(
            query="query",
            depth="standard",
            output_type="structured",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "search_kwargs",
        "expected_request_params",
        "mock_request_response_content",
        "expected_search_response",
    ),
    test_search_parameters,
)
async def test_async_search(
    mocker: MockerFixture,
    client: linkup.Client,
    search_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_search_response: Any,  # noqa: ANN401
) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    search_response = cast("Any", await client.async_search(**search_kwargs))
    expected_timeout = search_kwargs.get("timeout", None)
    request_mock.assert_called_once_with(
        method="POST",
        url="/search",
        json=expected_request_params,
        timeout=expected_timeout,
    )
    assert search_response == expected_search_response


@pytest.mark.asyncio
async def test_async_search_structured_output_requires_schema(client: linkup.Client) -> None:
    with pytest.raises(
        TypeError,
        match="structured_output_schema must be provided",
    ):
        await client.async_search(
            query="query",
            depth="standard",
            output_type="structured",
        )


test_search_error_parameters = [
    (
        402,
        b"""
        {
            "error": {
                "code": "PAYMENT_REQUIRED",
                "message": "Payment required",
                "details": []
            }
        }
        """,
        linkup.PaymentRequiredError,
    ),
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
        linkup.AuthenticationError,
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
        linkup.AuthenticationError,
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
        linkup.InsufficientCreditError,
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
        linkup.TooManyRequestsError,
    ),
    (
        429,
        b"""
        {
            "error": {
                "code": "EXCEED_BUDGET_LIMIT",
                "message": "The API key has reached its budget limit.",
                "details": []
            }
        }
        """,
        linkup.BudgetLimitExceededError,
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
        linkup.UnknownError,
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
        linkup.InvalidRequestError,
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
        linkup.NoResultError,
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
        linkup.UnknownError,
    ),
]


@pytest.mark.parametrize(
    ("mock_request_response_status_code", "mock_request_response_content", "expected_exception"),
    test_search_error_parameters,
)
def test_search_error(
    mocker: MockerFixture,
    client: linkup.Client,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: type[Exception],
) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
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
    ("mock_request_response_status_code", "mock_request_response_content", "expected_exception"),
    test_search_error_parameters,
)
async def test_async_search_error(
    mocker: MockerFixture,
    client: linkup.Client,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: type[Exception],
) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=mock_request_response_status_code,
            content=mock_request_response_content,
        ),
    )

    with pytest.raises(expected_exception):
        await client.async_search(query="query", depth="standard", output_type="searchResults")
    request_mock.assert_called_once()


def test_search_timeout(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.Client.request",
        side_effect=httpx.ReadTimeout("Request timed out"),
    )

    with pytest.raises(linkup.TimeoutError):
        client.search(query="query", depth="standard", output_type="searchResults", timeout=1.0)


@pytest.mark.asyncio
async def test_async_search_timeout(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.AsyncClient.request",
        side_effect=httpx.ReadTimeout("Request timed out"),
    )

    with pytest.raises(linkup.TimeoutError):
        await client.async_search(
            query="query", depth="standard", output_type="searchResults", timeout=1.0
        )


def test_research(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "4a44f4e0-eaf0-42eb-8ea4-99311b1d0f01",
                "input": {
                    "mode": "auto",
                    "outputType": "sourcedAnswer",
                    "q": "query"
                },
                "output": null,
                "status": "pending",
                "type": "research",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    research_response = client.research(query="query", output_type="sourcedAnswer", mode="auto")

    request_mock.assert_called_once_with(
        method="POST",
        url="/research",
        json={
            "q": "query",
            "outputType": "sourcedAnswer",
            "mode": "auto",
        },
        timeout=None,
    )
    assert research_response == linkup.ResearchTask(
        created_at="2026-05-18T00:00:00.000Z",
        error=None,
        id="4a44f4e0-eaf0-42eb-8ea4-99311b1d0f01",
        input=linkup.ResearchTaskInput(
            query="query",
            output_type="sourcedAnswer",
            mode="auto",
        ),
        output=None,
        status="pending",
        type="research",
        updated_at="2026-05-18T00:00:00.000Z",
    )


def test_research_structured_output_requires_schema(client: linkup.Client) -> None:
    with pytest.raises(
        TypeError,
        match="structured_output_schema must be provided",
    ):
        client.research(
            query="query",
            output_type="structured",
        )


def test_get_research_structured_output_keeps_sourced_answer_shape_raw(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c",
                "input": {
                    "outputType": "structured",
                    "q": "query",
                    "structuredOutputSchema": {
                        "type": "object"
                    }
                },
                "output": {
                    "answer": "structured answer field",
                    "sources": []
                },
                "status": "completed",
                "type": "research",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    research_response = client.get_research("bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c")

    assert research_response.output == {
        "answer": "structured answer field",
        "sources": [],
    }
    assert research_response.input.structured_output_schema == {"type": "object"}


@pytest.mark.asyncio
async def test_async_research(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "9a1c4553-4d42-4622-98b1-113004c4cf20",
                "input": {
                    "outputType": "structured",
                    "q": "query",
                    "structuredOutputSchema": {
                        "type": "object"
                    }
                },
                "output": {
                    "summary": "done"
                },
                "status": "completed",
                "type": "research",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    research_response = await client.async_research(
        query="query",
        output_type="structured",
        structured_output_schema=Company,
    )

    request_mock.assert_called_once_with(
        method="POST",
        url="/research",
        json={
            "q": "query",
            "outputType": "structured",
            "structuredOutputSchema": json.dumps(Company.model_json_schema()),
        },
        timeout=None,
    )
    assert research_response.output == {"summary": "done"}
    assert research_response.input.query == "query"
    assert research_response.input.structured_output_schema == {"type": "object"}


@pytest.mark.asyncio
async def test_async_research_structured_output_requires_schema(
    client: linkup.Client,
) -> None:
    with pytest.raises(
        TypeError,
        match="structured_output_schema must be provided",
    ):
        await client.async_research(
            query="query",
            output_type="structured",
        )


def test_research_with_iso_datetime_string_dates(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "f93f33c8-2688-4bd0-ab11-47c8ff89f7b7",
                "input": {
                    "fromDate": "2026-05-01",
                    "outputType": "sourcedAnswer",
                    "q": "query",
                    "toDate": "2026-05-31"
                },
                "output": null,
                "status": "pending",
                "type": "research",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    research_response = client.research(
        query="query",
        output_type="sourcedAnswer",
        from_date="2026-05-01T08:15:30.000Z",
        to_date="2026-05-31T23:59:59.000Z",
    )

    request_mock.assert_called_once_with(
        method="POST",
        url="/research",
        json={
            "q": "query",
            "outputType": "sourcedAnswer",
            "fromDate": "2026-05-01T08:15:30.000Z",
            "toDate": "2026-05-31T23:59:59.000Z",
        },
        timeout=None,
    )
    assert research_response.input.from_date == "2026-05-01"
    assert research_response.input.to_date == "2026-05-31"


test_fetch_parameters = [
    (
        {"url": "https://example.com"},
        {"url": "https://example.com"},
        b'{"markdown": "Some web page content"}',
        linkup.FetchResponse(markdown="Some web page content", raw_html=None),
    ),
    (
        {
            "url": "https://example.com",
            "include_raw_html": True,
            "render_js": True,
            "extract_images": True,
        },
        {
            "url": "https://example.com",
            "includeRawHtml": True,
            "renderJs": True,
            "extractImages": True,
        },
        b'{"markdown": "#Some web page content", "rawHtml": "<html>...</html>"}',
        linkup.FetchResponse(markdown="#Some web page content", raw_html="<html>...</html>"),
    ),
    (
        {"url": "https://example.com", "timeout": 15.0},
        {"url": "https://example.com"},
        b'{"markdown": "Some web page content"}',
        linkup.FetchResponse(markdown="Some web page content", raw_html=None),
    ),
]


@pytest.mark.parametrize(
    (
        "fetch_kwargs",
        "expected_request_params",
        "mock_request_response_content",
        "expected_fetch_response",
    ),
    test_fetch_parameters,
)
def test_fetch(
    mocker: MockerFixture,
    client: linkup.Client,
    fetch_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_fetch_response: linkup.FetchResponse,
) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    fetch_response: linkup.FetchResponse = client.fetch(**fetch_kwargs)
    expected_timeout = fetch_kwargs.get("timeout", None)
    request_mock.assert_called_once_with(
        method="POST",
        url="/fetch",
        json=expected_request_params,
        timeout=expected_timeout,
    )
    assert fetch_response == expected_fetch_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "fetch_kwargs",
        "expected_request_params",
        "mock_request_response_content",
        "expected_fetch_response",
    ),
    test_fetch_parameters,
)
async def test_async_fetch(
    mocker: MockerFixture,
    client: linkup.Client,
    fetch_kwargs: dict[str, Any],
    expected_request_params: dict[str, Any],
    mock_request_response_content: bytes,
    expected_fetch_response: linkup.FetchResponse,
) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=200,
            content=mock_request_response_content,
        ),
    )

    fetch_response: linkup.FetchResponse = await client.async_fetch(**fetch_kwargs)
    expected_timeout = fetch_kwargs.get("timeout", None)
    request_mock.assert_called_once_with(
        method="POST",
        url="/fetch",
        json=expected_request_params,
        timeout=expected_timeout,
    )
    assert fetch_response == expected_fetch_response


test_fetch_error_parameters = [
    (
        400,
        b"""
        {
            "error": {
                "code": "FETCH_ERROR",
                "message": "Could not fetch the URL",
                "details": []
            }
        }
        """,
        linkup.FailedFetchError,
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
                        "field": "url",
                        "message": "url must be a valid URL"
                    }
                ]
            }
        }
        """,
        linkup.InvalidRequestError,
    ),
    (
        400,
        b"""
        {
            "error": {
                "code": "FETCH_RESPONSE_TOO_LARGE",
                "message": "The fetched response is too large",
                "details": []
            }
        }
        """,
        linkup.FetchResponseTooLargeError,
    ),
    (
        400,
        b"""
        {
            "error": {
                "code": "FETCH_UNSUPPORTED_CONTENT_TYPE",
                "message": "The URL returned an unsupported content type",
                "details": []
            }
        }
        """,
        linkup.FetchUnsupportedContentTypeError,
    ),
]


@pytest.mark.parametrize(
    ("mock_request_response_status_code", "mock_request_response_content", "expected_exception"),
    test_fetch_error_parameters,
)
def test_fetch_error(
    mocker: MockerFixture,
    client: linkup.Client,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: type[Exception],
) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=mock_request_response_status_code,
            content=mock_request_response_content,
        ),
    )

    with pytest.raises(expected_exception):
        client.fetch(url="https://example.com")
    request_mock.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("mock_request_response_status_code", "mock_request_response_content", "expected_exception"),
    test_fetch_error_parameters,
)
async def test_async_fetch_error(
    mocker: MockerFixture,
    client: linkup.Client,
    mock_request_response_status_code: int,
    mock_request_response_content: bytes,
    expected_exception: type[Exception],
) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=mock_request_response_status_code,
            content=mock_request_response_content,
        ),
    )

    with pytest.raises(expected_exception):
        await client.async_fetch(url="https://example.com")
    request_mock.assert_called_once()


def test_fetch_timeout(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.Client.request",
        side_effect=httpx.ReadTimeout("Request timed out"),
    )

    with pytest.raises(linkup.TimeoutError):
        client.fetch(url="https://example.com", timeout=1.0)


@pytest.mark.asyncio
async def test_async_fetch_timeout(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.AsyncClient.request",
        side_effect=httpx.ReadTimeout("Request timed out"),
    )

    with pytest.raises(linkup.TimeoutError):
        await client.async_fetch(url="https://example.com", timeout=1.0)


def test_create_tasks(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            [
                {
                    "created_at": "2026-05-18T00:00:00.000Z",
                    "error": null,
                    "id": "7132d2b9-61b8-4d6f-a6f2-b69daeff6d58",
                    "input": {
                        "depth": "deep",
                        "outputType": "structured",
                        "q": "query",
                        "structuredOutputSchema": {
                            "type": "object"
                        }
                    },
                    "output": null,
                    "status": "pending",
                    "type": "search",
                    "updatedAt": "2026-05-18T00:00:00.000Z"
                },
                {
                    "createdAt": "2026-05-18T00:00:00.000Z",
                    "error": null,
                    "id": "42057d84-72ea-4029-9598-1bf7424a6113",
                    "input": {
                        "extractImages": true,
                        "url": "https://example.com"
                    },
                    "output": {
                        "images": [
                            {
                                "alt": "hero",
                                "url": "https://example.com/image.png"
                            }
                        ],
                        "markdown": "Fetched content"
                    },
                    "status": "completed",
                    "type": "fetch",
                    "updatedAt": "2026-05-18T00:00:00.000Z"
                }
            ]
            """,
        ),
    )

    tasks_response = client.create_tasks(
        [
            linkup.SearchTaskInput(
                query="query",
                depth="deep",
                output_type="structured",
                structured_output_schema=Company,
            ),
            linkup.FetchTaskInput(
                url="https://example.com",
                extract_images=True,
            ),
        ]
    )

    request_mock.assert_called_once_with(
        method="POST",
        url="/tasks",
        json=[
            {
                "type": "search",
                "input": {
                    "q": "query",
                    "depth": "deep",
                    "outputType": "structured",
                    "structuredOutputSchema": json.dumps(Company.model_json_schema()),
                },
            },
            {
                "type": "fetch",
                "input": {
                    "url": "https://example.com",
                    "extractImages": True,
                },
            },
        ],
        timeout=None,
    )
    assert isinstance(tasks_response[0], linkup.SearchTask)
    assert tasks_response[0].input.query == "query"
    assert tasks_response[0].input.structured_output_schema == {"type": "object"}
    assert isinstance(tasks_response[1], linkup.FetchTask)
    assert tasks_response[1].output is not None
    assert tasks_response[1].output.images is not None
    assert tasks_response[1].output.images[0].url == "https://example.com/image.png"


def test_create_tasks_research_model(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            [
                {
                    "createdAt": "2026-05-18T00:00:00.000Z",
                    "error": null,
                    "id": "bbd897fb-b761-4dd9-bf6a-b41ec52f2de7",
                    "input": {
                        "mode": "answer",
                        "outputType": "sourcedAnswer",
                        "q": "query",
                        "reasoningDepth": "S"
                    },
                    "output": null,
                    "status": "processing",
                    "type": "research",
                    "updatedAt": "2026-05-18T00:00:00.000Z"
                }
            ]
            """,
        ),
    )

    tasks_response = client.create_tasks(
        [
            linkup.ResearchTaskInput(
                query="query",
                output_type="sourcedAnswer",
                mode="answer",
                reasoning_depth="S",
            )
        ]
    )

    request_mock.assert_called_once_with(
        method="POST",
        url="/tasks",
        json=[
            {
                "type": "research",
                "input": {
                    "q": "query",
                    "outputType": "sourcedAnswer",
                    "mode": "answer",
                    "reasoningDepth": "S",
                },
            }
        ],
        timeout=None,
    )
    assert isinstance(tasks_response[0], linkup.ResearchTask)
    assert tasks_response[0].input.reasoning_depth == "S"


def test_create_tasks_queue_limit_error(mocker: MockerFixture, client: linkup.Client) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=429,
            content=b"""
            {
                "error": {
                    "code": "TASKS_QUEUE_LIMIT_EXCEEDED",
                    "message": "Too many pending tasks.",
                    "details": []
                }
            }
            """,
        ),
    )

    with pytest.raises(linkup.TasksQueueLimitExceededError):
        client.create_tasks([linkup.FetchTaskInput(url="https://example.com")])


@pytest.mark.asyncio
async def test_async_create_tasks_queue_limit_error(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=429,
            content=b"""
            {
                "error": {
                    "code": "TASKS_QUEUE_LIMIT_EXCEEDED",
                    "message": "Too many pending tasks.",
                    "details": []
                }
            }
            """,
        ),
    )

    with pytest.raises(linkup.TasksQueueLimitExceededError):
        await client.async_create_tasks([linkup.FetchTaskInput(url="https://example.com")])


@pytest.mark.asyncio
async def test_async_list_research(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "data": [
                    {
                        "createdAt": "2026-05-18T00:00:00.000Z",
                        "error": null,
                        "id": "cdedcd9f-ab4a-4404-b8c6-b9ca9dc4c837",
                        "input": {
                            "outputType": "sourcedAnswer",
                            "q": "query"
                        },
                        "output": null,
                        "status": "pending",
                        "type": "research",
                        "updatedAt": "2026-05-18T00:00:00.000Z"
                    }
                ],
                "metadata": {
                    "page": 2,
                    "pageSize": 5,
                    "total": 11,
                    "totalPages": 3
                }
            }
            """,
        ),
    )

    research_page = await client.async_list_research(page=2, page_size=5)

    request_mock.assert_called_once_with(
        method="GET",
        url="/research",
        params={
            "page": 2,
            "pageSize": 5,
        },
        timeout=None,
    )
    assert research_page == linkup.ResearchTasksPage(
        data=[
            linkup.ResearchTask(
                created_at="2026-05-18T00:00:00.000Z",
                error=None,
                id="cdedcd9f-ab4a-4404-b8c6-b9ca9dc4c837",
                input=linkup.ResearchTaskInput(
                    query="query",
                    output_type="sourcedAnswer",
                ),
                output=None,
                status="pending",
                type="research",
                updated_at="2026-05-18T00:00:00.000Z",
            )
        ],
        metadata=linkup.TaskMetadata(
            page=2,
            page_size=5,
            total=11,
            total_pages=3,
        ),
    )


def test_get_task_not_found(mocker: MockerFixture, client: linkup.Client) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=404,
            content=b"""
            {
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task task-404 not found.",
                    "details": []
                }
            }
            """,
        ),
    )

    with pytest.raises(linkup.TaskNotFoundError):
        client.get_task("task-404")


@pytest.mark.asyncio
async def test_async_get_research_not_found(mocker: MockerFixture, client: linkup.Client) -> None:
    mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=404,
            content=b"""
            {
                "error": {
                    "code": "TASK_NOT_FOUND",
                    "message": "Task research-404 not found.",
                    "details": []
                }
            }
            """,
        ),
    )

    with pytest.raises(linkup.TaskNotFoundError):
        await client.async_get_research("research-404")


def test_list_tasks(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "data": [
                    {
                        "createdAt": "2026-05-18T00:00:00.000Z",
                        "error": null,
                        "id": "bbd897fb-b761-4dd9-bf6a-b41ec52f2de7",
                        "input": {
                            "outputType": "sourcedAnswer",
                            "q": "query"
                        },
                        "output": null,
                        "status": "processing",
                        "type": "research",
                        "updatedAt": "2026-05-18T00:00:00.000Z"
                    }
                ],
                "metadata": {
                    "page": 1,
                    "pageSize": 10,
                    "total": 1,
                    "totalPages": 1
                },
                "quota": {
                    "inFlight": 1,
                    "limit": 100
                }
            }
            """,
        ),
    )

    tasks_page = client.list_tasks(
        status="pending",
        task_type="search",
    )

    request_mock.assert_called_once_with(
        method="GET",
        url="/tasks",
        params={
            "status": "pending",
            "type": "search",
        },
        timeout=None,
    )
    assert isinstance(tasks_page, linkup.TasksPage)
    assert isinstance(tasks_page.data[0], linkup.ResearchTask)
    assert tasks_page.data[0].input.query == "query"
    assert tasks_page.quota.in_flight == 1


def test_get_task_structured_search_output_keeps_search_results_shape_raw(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c",
                "input": {
                    "depth": "standard",
                    "outputType": "structured",
                    "q": "query",
                    "structuredOutputSchema": {
                        "type": "object"
                    }
                },
                "output": {
                    "results": []
                },
                "status": "completed",
                "type": "search",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    task = client.get_task("bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c")

    assert isinstance(task, linkup.SearchTask)
    assert task.output == {"results": []}


def test_get_task_structured_search_output_raw(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "createdAt": "2026-05-18T00:00:00.000Z",
                "error": null,
                "id": "bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c",
                "input": {
                    "depth": "standard",
                    "outputType": "structured",
                    "q": "query",
                    "structuredOutputSchema": {
                        "type": "object"
                    }
                },
                "output": {
                    "summary": "done"
                },
                "status": "completed",
                "type": "search",
                "updatedAt": "2026-05-18T00:00:00.000Z"
            }
            """,
        ),
    )

    task = client.get_task("bfeb26f5-f4d6-47d2-9818-7f62fbcd0b0c")

    assert isinstance(task, linkup.SearchTask)
    assert task.input.structured_output_schema == {"type": "object"}
    assert task.output == {"summary": "done"}


def test_list_tasks_with_multiple_filters(mocker: MockerFixture, client: linkup.Client) -> None:
    request_mock = mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "data": [],
                "metadata": {
                    "page": 1,
                    "pageSize": 10,
                    "total": 0,
                    "totalPages": 0
                },
                "quota": {
                    "inFlight": 0,
                    "limit": 100
                }
            }
            """,
        ),
    )

    tasks_page = client.list_tasks(
        status=["pending", "processing"],
        task_type=["search", "research"],
    )

    request_mock.assert_called_once_with(
        method="GET",
        url="/tasks",
        params={
            "status": ["pending", "processing"],
            "type": ["search", "research"],
        },
        timeout=None,
    )
    assert tasks_page.metadata.total == 0


@pytest.mark.asyncio
async def test_async_list_tasks_with_multiple_filters(
    mocker: MockerFixture, client: linkup.Client
) -> None:
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=200,
            content=b"""
            {
                "data": [],
                "metadata": {
                    "page": 1,
                    "pageSize": 10,
                    "total": 0,
                    "totalPages": 0
                },
                "quota": {
                    "inFlight": 0,
                    "limit": 100
                }
            }
            """,
        ),
    )

    tasks_page = await client.async_list_tasks(
        status=["pending", "processing"],
        task_type=["search", "research"],
    )

    request_mock.assert_called_once_with(
        method="GET",
        url="/tasks",
        params={
            "status": ["pending", "processing"],
            "type": ["search", "research"],
        },
        timeout=None,
    )
    assert tasks_page.metadata.total == 0


_402_BODY = b'{"error": {"code": "PAYMENT_REQUIRED", "message": "Pay", "details": []}}'

_402_BODY_FULL = (
    b'{"error": {"code": "PAYMENT_REQUIRED", "message": "Payment required", "details": []}}'
)

_500_BODY = b'{"error": {"code": "INTERNAL_SERVER_ERROR", "message": "Error", "details": []}}'


def test_client_x402_signer(mock_x402_signer: MagicMock) -> None:
    client = linkup.Client(x402_signer=mock_x402_signer)
    assert client._x402_signer is mock_x402_signer  # noqa: SLF001
    assert client._api_key is None  # noqa: SLF001


def test_client_both_api_key_and_x402_signer_raises(
    mock_x402_signer: MagicMock,
) -> None:
    with pytest.raises(ValueError, match="Cannot provide both"):
        linkup.Client(api_key="test-key", x402_signer=mock_x402_signer)


def test_client_custom_auth_header(
    mocker: MockerFixture,
) -> None:
    client = linkup.Client(api_key="my-key", auth_header="Ocp-Apim-Subscription-Key")

    client_mock = mocker.patch("httpx.Client")
    client_mock.return_value.__enter__.return_value = client_mock.return_value
    client_mock.return_value.request.return_value = Response(
        status_code=200, content=b'{"results": []}'
    )
    client.search(query="query", depth="standard", output_type="searchResults")

    init_kwargs = client_mock.call_args[1]
    assert "Ocp-Apim-Subscription-Key" in init_kwargs["headers"]
    assert init_kwargs["headers"]["Ocp-Apim-Subscription-Key"] == "my-key"
    assert "Authorization" not in init_kwargs["headers"]


def test_client_x402_no_auth_header(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.create_payment_headers.return_value = {
        "X-Payment": "signed",
    }
    request_mock = mocker.patch(
        "httpx.Client.request",
        side_effect=[
            Response(
                status_code=402,
                content=_402_BODY,
                headers={"X-Payment-Required": "true"},
            ),
            Response(status_code=200, content=b'{"results": []}'),
        ],
    )

    x402_client.search(query="query", depth="standard", output_type="searchResults")

    first_call_args = request_mock.call_args_list[0]
    assert first_call_args == mocker.call(
        method="POST",
        url="/search",
        json={
            "q": "query",
            "depth": "standard",
            "outputType": "searchResults",
        },
        timeout=None,
    )


def test_x402_retry_sync(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.create_payment_headers.return_value = {
        "X-Payment": "signed",
    }
    request_mock = mocker.patch(
        "httpx.Client.request",
        side_effect=[
            Response(
                status_code=402,
                content=_402_BODY,
                headers={"X-Payment-Required": "true"},
            ),
            Response(status_code=200, content=b'{"results": []}'),
        ],
    )

    result = x402_client.search(query="query", depth="standard", output_type="searchResults")
    assert result.results == []
    mock_x402_signer.create_payment_headers.assert_called_once()

    # Verify the retry call merges payment headers with base headers
    retry_call = request_mock.call_args_list[1]
    assert retry_call == mocker.call(
        method="POST",
        url="/search",
        json={
            "q": "query",
            "depth": "standard",
            "outputType": "searchResults",
        },
        timeout=None,
        headers={
            "User-Agent": f"Linkup-Python/{x402_client.__version__}",
            "X-Payment": "signed",
        },
    )


def test_x402_retry_failure_sync(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.create_payment_headers.return_value = {
        "X-Payment": "signed",
    }
    mocker.patch(
        "httpx.Client.request",
        side_effect=[
            Response(
                status_code=402,
                content=_402_BODY,
                headers={"X-Payment-Required": "true"},
            ),
            Response(status_code=500, content=_500_BODY),
        ],
    )

    with pytest.raises(linkup.UnknownError):
        x402_client.search(query="query", depth="standard", output_type="searchResults")


def test_x402_signer_error_sync(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.create_payment_headers.side_effect = RuntimeError("signing failed")
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=402,
            content=_402_BODY,
            headers={"X-Payment-Required": "true"},
        ),
    )

    with pytest.raises(linkup.PaymentRequiredError, match="signing failed"):
        x402_client.search(query="query", depth="standard", output_type="searchResults")


def test_402_without_signer(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.Client.request",
        return_value=Response(
            status_code=402,
            content=_402_BODY_FULL,
        ),
    )

    with pytest.raises(linkup.PaymentRequiredError):
        client.search(query="query", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
async def test_x402_retry_async(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.async_create_payment_headers = AsyncMock(return_value={"X-Payment": "signed"})
    request_mock = mocker.patch(
        "httpx.AsyncClient.request",
        side_effect=[
            Response(
                status_code=402,
                content=_402_BODY,
                headers={"X-Payment-Required": "true"},
            ),
            Response(status_code=200, content=b'{"results": []}'),
        ],
    )

    result = await x402_client.async_search(
        query="query", depth="standard", output_type="searchResults"
    )
    assert result.results == []
    mock_x402_signer.async_create_payment_headers.assert_called_once()

    # Verify the retry call merges payment headers with base headers
    retry_call = request_mock.call_args_list[1]
    assert retry_call == mocker.call(
        method="POST",
        url="/search",
        json={
            "q": "query",
            "depth": "standard",
            "outputType": "searchResults",
        },
        timeout=None,
        headers={
            "User-Agent": f"Linkup-Python/{x402_client.__version__}",
            "X-Payment": "signed",
        },
    )


@pytest.mark.asyncio
async def test_x402_retry_failure_async(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.async_create_payment_headers = AsyncMock(return_value={"X-Payment": "signed"})
    mocker.patch(
        "httpx.AsyncClient.request",
        side_effect=[
            Response(
                status_code=402,
                content=_402_BODY,
                headers={"X-Payment-Required": "true"},
            ),
            Response(status_code=500, content=_500_BODY),
        ],
    )

    with pytest.raises(linkup.UnknownError):
        await x402_client.async_search(query="query", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
async def test_x402_signer_error_async(
    mocker: MockerFixture,
    x402_client: linkup.Client,
    mock_x402_signer: MagicMock,
) -> None:
    mock_x402_signer.async_create_payment_headers = AsyncMock(
        side_effect=RuntimeError("signing failed")
    )
    mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=402,
            content=_402_BODY,
            headers={"X-Payment-Required": "true"},
        ),
    )

    with pytest.raises(linkup.PaymentRequiredError, match="signing failed"):
        await x402_client.async_search(query="query", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
async def test_402_without_signer_async(
    mocker: MockerFixture,
    client: linkup.Client,
) -> None:
    mocker.patch(
        "httpx.AsyncClient.request",
        return_value=Response(
            status_code=402,
            content=_402_BODY_FULL,
        ),
    )

    with pytest.raises(linkup.PaymentRequiredError):
        await client.async_search(query="query", depth="standard", output_type="searchResults")
