import json
from typing import Any, List, Type, Union

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
from linkup.errors import LinkupInsufficientCreditError, LinkupNoResultError
from linkup.types import LinkupSearchImageResult, LinkupSearchTextResult


class Company(BaseModel):
    name: str
    creation_date: str
    website_url: str
    founders_names: List[str]


def test_search_search_results(mocker: MockerFixture, client: LinkupClient) -> None:
    content = b"""
    {
      "results": [
        {
          "type": "text",
          "name": "foo",
          "url": "https://foo.bar/baz",
          "content": "foo bar baz"
        },
        {
          "type": "image",
          "name": "foo",
          "url": "https://foo.bar/baz"
        }
      ]
    }
    """

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=content,
        ),
    )

    response: Any = client.search(query="foo", depth="standard", output_type="searchResults")

    assert isinstance(response, LinkupSearchResults)
    assert isinstance(response.results[0], LinkupSearchTextResult)
    assert response.results[0].name == "foo"
    assert response.results[0].url == "https://foo.bar/baz"
    assert response.results[0].content == "foo bar baz"
    assert isinstance(response.results[1], LinkupSearchImageResult)
    assert response.results[1].name == "foo"
    assert response.results[1].url == "https://foo.bar/baz"


def test_search_sourced_answer(mocker: MockerFixture, client: LinkupClient) -> None:
    content = b"""
    {
      "answer": "foo bar baz",
      "sources": [
        {
          "name": "foo",
          "url": "https://foo.bar/baz",
          "snippet": "foo bar baz qux"
        }
      ]
    }
    """

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=content,
        ),
    )

    response: Any = client.search(query="foo", depth="standard", output_type="sourcedAnswer")

    assert isinstance(response, LinkupSourcedAnswer)
    assert isinstance(response.sources[0], LinkupSource)
    assert response.answer == "foo bar baz"
    assert response.sources[0].name == "foo"
    assert response.sources[0].url == "https://foo.bar/baz"
    assert response.sources[0].snippet == "foo bar baz qux"


@pytest.mark.parametrize(
    "structured_output_schema",
    [Company, json.dumps(Company.model_json_schema())],
)
def test_search_structured_search(
    mocker: MockerFixture,
    client: LinkupClient,
    structured_output_schema: Union[Type[BaseModel], str],
) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "structured"

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b'{"name":"Linkup","founders_names":["Philippe Mizrahi","Denis Charrier",'
            b'"Boris Toledano"],"creation_date":"2024","website_url":"","title":"Company"}',
        ),
    )

    response: Any = client.search(
        query=query,
        depth=depth,
        output_type=output_type,
        structured_output_schema=structured_output_schema,
    )

    if isinstance(structured_output_schema, str):
        assert response == dict(
            creation_date="2024",
            founders_names=["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            name="Linkup",
            title="Company",
            website_url="",
        )

    else:
        assert isinstance(response, Company)
        assert response.name == "Linkup"
        assert response.creation_date == "2024"
        assert response.website_url == ""
        assert response.founders_names == ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"]


def test_search_authentication_error(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=403,
            content=b'{"message":"Forbidden resource","error":"Forbidden","statusCode":403}',
        ),
    )

    with pytest.raises(LinkupAuthenticationError):
        client.search(query=query, depth=depth, output_type=output_type)


def test_search_insufficient_credit_error(mocker: MockerFixture, client: LinkupClient) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=429,
            content=b"{}",
        ),
    )
    with pytest.raises(LinkupInsufficientCreditError):
        client.search(query="foo", depth="standard", output_type="searchResults")


def test_search_structured_search_invalid_request(
    mocker: MockerFixture,
    client: LinkupClient,
) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "structured"
    # Schema corresponding to the Company class, without "type": "object"
    structured_output_schema = json.dumps(
        {
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "creation_date": {"title": "Creation Date", "type": "string"},
                "website_url": {"title": "Website Url", "type": "string"},
                "founders_names": {
                    "items": {"type": "string"},
                    "title": "Founders Names",
                    "type": "array",
                },
            },
            "required": ["name", "creation_date", "website_url", "founders_names"],
            "title": "Company",
        }
    )

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=400,
            content=b'{"message":["structuredOutputSchema must be valid JSON schema of type '
            b'object"],"error":"Bad Request","statusCode":400}',
        ),
    )

    with pytest.raises(LinkupInvalidRequestError):
        client.search(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
        )


def test_search_no_result_error(mocker: MockerFixture, client: LinkupClient) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=400,
            content=b'{"message": "The query did not yield any result"}',
        ),
    )
    with pytest.raises(LinkupNoResultError):
        client.search(query="foo", depth="standard", output_type="searchResults")


def test_search_unknown_error(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=500,
            content=b'{"message":"Something weird happened","error":"unknown","statusCode":500}',
        ),
    )

    with pytest.raises(LinkupUnknownError):
        client.search(query=query, depth=depth, output_type=output_type)


@pytest.mark.asyncio
async def test_async_search_search_results(mocker: MockerFixture, client: LinkupClient) -> None:
    content = b"""
    {
      "results": [
        {
          "type": "text",
          "name": "foo",
          "url": "https://foo.bar/baz",
          "content": "foo bar baz"
        },
        {
          "type": "image",
          "name": "foo",
          "url": "https://foo.bar/baz"
        }
      ]
    }
    """

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=content,
        ),
    )

    response: Any = await client.async_search(
        query="foo", depth="standard", output_type="searchResults"
    )

    assert isinstance(response, LinkupSearchResults)
    assert isinstance(response.results[0], LinkupSearchTextResult)
    assert response.results[0].name == "foo"
    assert response.results[0].url == "https://foo.bar/baz"
    assert response.results[0].content == "foo bar baz"
    assert isinstance(response.results[1], LinkupSearchImageResult)
    assert response.results[1].name == "foo"
    assert response.results[1].url == "https://foo.bar/baz"


@pytest.mark.asyncio
async def test_async_search_sourced_answer(mocker: MockerFixture, client: LinkupClient) -> None:
    content = b"""
    {
      "answer": "foo bar baz",
      "sources": [
        {
          "name": "foo",
          "url": "https://foo.bar/baz",
          "snippet": "foo bar baz qux"
        }
      ]
    }
    """

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=content,
        ),
    )

    response: Any = await client.async_search(
        query="foo", depth="standard", output_type="sourcedAnswer"
    )

    assert isinstance(response, LinkupSourcedAnswer)
    assert isinstance(response.sources[0], LinkupSource)
    assert response.answer == "foo bar baz"
    assert response.sources[0].name == "foo"
    assert response.sources[0].url == "https://foo.bar/baz"
    assert response.sources[0].snippet == "foo bar baz qux"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "structured_output_schema",
    [Company, json.dumps(Company.model_json_schema())],
)
async def test_async_search_structured_search(
    mocker: MockerFixture,
    client: LinkupClient,
    structured_output_schema: Union[Type[BaseModel], str],
) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "structured"

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b'{"name":"Linkup","founders_names":["Philippe Mizrahi","Denis Charrier",'
            b'"Boris Toledano"],"creation_date":"2024","website_url":"","title":"Company"}',
        ),
    )

    response: Any = await client.async_search(
        query=query,
        depth=depth,
        output_type=output_type,
        structured_output_schema=structured_output_schema,
    )

    if isinstance(structured_output_schema, str):
        assert response == dict(
            creation_date="2024",
            founders_names=["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"],
            name="Linkup",
            title="Company",
            website_url="",
        )

    else:
        assert isinstance(response, Company)
        assert response.name == "Linkup"
        assert response.creation_date == "2024"
        assert response.website_url == ""
        assert response.founders_names == ["Philippe Mizrahi", "Denis Charrier", "Boris Toledano"]


@pytest.mark.asyncio
async def test_async_search_authentication_error(
    mocker: MockerFixture, client: LinkupClient
) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=403,
            content=b'{"message":"Forbidden resource","error":"Forbidden","statusCode":403}',
        ),
    )

    with pytest.raises(LinkupAuthenticationError):
        await client.async_search(query=query, depth=depth, output_type=output_type)


@pytest.mark.asyncio
async def test_async_search_insufficient_credit_error(
    mocker: MockerFixture, client: LinkupClient
) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(status_code=429, content=b"{}"),
    )
    with pytest.raises(LinkupInsufficientCreditError):
        await client.async_search(query="foo", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
async def test_async_search_structured_search_invalid_request(
    mocker: MockerFixture,
    client: LinkupClient,
) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "structured"
    # Schema corresponding to the Company class, without "type": "object"
    structured_output_schema = json.dumps(
        {
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "creation_date": {"title": "Creation Date", "type": "string"},
                "website_url": {"title": "Website Url", "type": "string"},
                "founders_names": {
                    "items": {"type": "string"},
                    "title": "Founders Names",
                    "type": "array",
                },
            },
            "required": ["name", "creation_date", "website_url", "founders_names"],
            "title": "Company",
        }
    )

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=400,
            content=b'{"message":["structuredOutputSchema must be valid JSON schema of type '
            b'object"],"error":"Bad Request","statusCode":400}',
        ),
    )

    with pytest.raises(LinkupInvalidRequestError):
        await client.async_search(
            query=query,
            depth=depth,
            output_type=output_type,
            structured_output_schema=structured_output_schema,
        )


@pytest.mark.asyncio
async def test_async_search_no_result_error(mocker: MockerFixture, client: LinkupClient) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=400,
            content=b'{"message": "The query did not yield any result"}',
        ),
    )
    with pytest.raises(LinkupNoResultError):
        await client.async_search(query="foo", depth="standard", output_type="searchResults")


@pytest.mark.asyncio
async def test_async_search_unknown_error(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=500,
            content=b'{"message":"Something weird happened","error":"unknown","statusCode":500}',
        ),
    )

    with pytest.raises(LinkupUnknownError):
        await client.async_search(query=query, depth=depth, output_type=output_type)
