import json
from typing import Any, List, Type, Union

import pytest
from httpx import Response
from pydantic import BaseModel
from pytest_mock import MockerFixture

from linkup import (
    LinkupAuthenticationError,
    LinkupClient,
    LinkupContent,
    LinkupInvalidRequestError,
    LinkupSearchResult,
    LinkupSearchResults,
    LinkupSource,
    LinkupSourcedAnswer,
    LinkupUnknownError,
)
from linkup.errors import LinkupInsufficientCreditError, LinkupNoResultError


class Company(BaseModel):
    name: str
    creation_date: str
    website_url: str
    founders_names: List[str]


def test_content(mocker: MockerFixture, client: LinkupClient) -> None:
    url = (
        "https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
        "of-indias-independence"
    )
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b'{"content":"# Capgemini Employees Walk Together in Celebration of India\'s '
            b"Independence\\n\\n*Capgemini India engaged employees with creative contests. ... "
            b"\\n\\nThe events undersc ored the company\xe2\x80\x99s commitment to fostering a "
            b"work environment where employees not only work together but also celebrate together, "
            b'creating a culture of unity and shared purpose."}',
        ),
    )

    response: LinkupContent = client.content(url=url)

    assert isinstance(response, LinkupContent)
    assert response.content == (
        "# Capgemini Employees Walk Together in Celebration of India's Independence\n\n*Capgemini "
        "India engaged employees with creative contests. ... \n\nThe events undersc ored the "
        "company’s commitment to fostering a work environment where employees not only work "
        "together but also celebrate together, creating a culture of unity and shared purpose."
    )


def test_content_authentication_error(mocker: MockerFixture, client: LinkupClient) -> None:
    url = (
        "https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
        "of-indias-independence"
    )
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=403,
            content=b'{"message":"Forbidden resource","error":"Forbidden","statusCode":403}',
        ),
    )

    with pytest.raises(LinkupAuthenticationError):
        client.content(url=url)


def test_content_invalid_request(mocker: MockerFixture, client: LinkupClient) -> None:
    url = "https://www.abcd.com"
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=400,
            content=b'{"message":["Cannot get content for URL \\"https://www.abcd.com\\""],'
            b'"error":"Bad Request","statusCode":400}',
        ),
    )

    with pytest.raises(LinkupInvalidRequestError):
        client.content(url=url)


def test_content_unknown_error(mocker: MockerFixture, client: LinkupClient) -> None:
    url = "https://www.abcd.com"
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=500,
            content=b'{"message":"Something weird happened","error":"unknown","statusCode":500}',
        ),
    )

    with pytest.raises(LinkupUnknownError):
        client.content(url=url)


@pytest.mark.asyncio
async def test_async_content(mocker: MockerFixture, client: LinkupClient) -> None:
    url = (
        "https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
        "of-indias-independence"
    )
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b'{"content":"# Capgemini Employees Walk Together in Celebration of India\'s '
            b"Independence\\n\\n*Capgemini India engaged employees with creative contests. ... "
            b"\\n\\nThe events undersc ored the company\xe2\x80\x99s commitment to fostering a "
            b"work environment where employees not only work together but also celebrate together, "
            b'creating a culture of unity and shared purpose."}',
        ),
    )

    response: LinkupContent = await client.async_content(url=url)

    assert isinstance(response, LinkupContent)
    assert response.content == (
        "# Capgemini Employees Walk Together in Celebration of India's Independence\n\n*Capgemini "
        "India engaged employees with creative contests. ... \n\nThe events undersc ored the "
        "company’s commitment to fostering a work environment where employees not only work "
        "together but also celebrate together, creating a culture of unity and shared purpose."
    )


@pytest.mark.asyncio
async def test_async_content_authentication_error(
    mocker: MockerFixture, client: LinkupClient
) -> None:
    url = (
        "https://www.thebridgechronicle.com/news/capgemini-employees-walk-together-in-celebration-"
        "of-indias-independence"
    )
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=403,
            content=b'{"message":"Forbidden resource","error":"Forbidden","statusCode":403}',
        ),
    )

    with pytest.raises(LinkupAuthenticationError):
        await client.async_content(url=url)


@pytest.mark.asyncio
async def test_async_content_invalid_request(mocker: MockerFixture, client: LinkupClient) -> None:
    url = "https://www.abcd.com"
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=400,
            content=b'{"message":["Cannot get content for URL \\"https://www.abcd.com\\""],'
            b'"error":"Bad Request","statusCode":400}',
        ),
    )

    with pytest.raises(LinkupInvalidRequestError):
        await client.async_content(url=url)


@pytest.mark.asyncio
async def test_async_content_unknown_error(mocker: MockerFixture, client: LinkupClient) -> None:
    url = "https://www.abcd.com"
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=500,
            content=b'{"message":"Something weird happened","error":"unknown","statusCode":500}',
        ),
    )

    with pytest.raises(LinkupUnknownError):
        await client.async_content(url=url)


def test_search_search_results(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b'{"results":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming '
            b'to revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-'
            b"based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-"
            b'access-for-ai/","content":"Linkup, a French startup providing AI with fast, ethical '
            b"access to online content, has secured \xe2\x82\xac3 million supported by leading "
            b"investors, including Seedcamp, Axeleo Capital, Motier Ventures, and a network of "
            b"prominent tech and media industry angels to further develop its sustainable "
            b"alternative to web scraping and address the challenges posed by AI-driven web "
            b'traffic."},{"name":"French Tech : Linkup, le moteur de recherche d\xc3\xa9di'
            b'\xc3\xa9 aux intelligences ...","url":"https://www.midilibre.fr/2024/11/18/french-'
            b"tech-linkup-le-moteur-de-recherche-dedie-aux-intelligences-artificielles-12331232."
            b'php","content":"La start-up Linkup, fond\xc3\xa9e d\xc3\xa9but 2024 par Philippe '
            b"Mizrahi, Denis Charrier et Boris Toledano, propose une avanc\xc3\xa9e r\xc3\xa9elle "
            b"dans l\xe2\x80\x99acc\xc3\xa8s des intelligences artificielles (IA) au contenu de "
            b'web."}]}',
        ),
    )

    response: Any = client.search(query=query, depth=depth, output_type=output_type)

    assert isinstance(response, LinkupSearchResults)
    assert isinstance(response.results, list)
    assert response.results
    assert isinstance(response.results[0], LinkupSearchResult)
    assert (
        response.results[0].name
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        response.results[0].url
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        response.results[0].content
        == "Linkup, a French startup providing AI with fast, ethical access to online content, has "
        "secured €3 million supported by leading investors, including Seedcamp, Axeleo Capital, "
        "Motier Ventures, and a network of prominent tech and media industry angels to further "
        "develop its sustainable alternative to web scraping and address the challenges posed by "
        "AI-driven web traffic."
    )


def test_search_sourced_answer(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "sourcedAnswer"

    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b'{"answer":"Linkup is a Paris-based startup that focuses on providing AI with '
            b"fast and ethical access to online content. The company aims to create a sustainable "
            b"alternative to web scraping by addressing the challenges posed by AI-driven web "
            b"traffic. Linkup has recently raised \xe2\x82\xac3 million to further develop its "
            b"platform, which serves as an intermediary between AI technologies and content "
            b'publishers, allowing AI to access content in a way that is legal and efficient.",'
            b'"sources":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming to '
            b'revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-based-'
            b"linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-"
            b'for-ai/","snippet":"Linkup, a French startup providing AI with fast, ethical access '
            b"to online content, has secured \xe2\x82\xac3 million supported by leading "
            b'investors."},{"name":"Linkup l\xc3\xa8ve 3 millions d\xe2\x80\x99euros pour faire '
            b'le pont entre IA et les ...","url":"https://www.frenchweb.fr/linkup-leve-3-millions-'
            b"deuros-pour-faire-le-pont-entre-ia-et-les-editeurs-de-contenus-dans-un-monde-post-"
            b'webscraping/449941","snippet":"Linkup, une start-up parisienne fond\xc3\xa9e en '
            b"2024, veut proposer un acc\xc3\xa8s maitris\xc3\xa9 et l\xc3\xa9gal aux diff"
            b'\xc3\xa9rents protagonistes."}]}',
        ),
    )

    response: Any = client.search(query=query, depth=depth, output_type=output_type)

    assert isinstance(response, LinkupSourcedAnswer)
    assert (
        response.answer
        == "Linkup is a Paris-based startup that focuses on providing AI with fast and ethical "
        "access to online content. The company aims to create a sustainable alternative to web "
        "scraping by addressing the challenges posed by AI-driven web traffic. Linkup has recently "
        "raised €3 million to further develop its platform, which serves as an intermediary "
        "between AI technologies and content publishers, allowing AI to access content in a way "
        "that is legal and efficient."
    )
    assert isinstance(response.sources, list)
    assert response.sources
    assert isinstance(response.sources[0], LinkupSource)
    assert (
        response.sources[0].name
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        response.sources[0].url
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        response.sources[0].snippet
        == "Linkup, a French startup providing AI with fast, ethical access to online content, has "
        "secured €3 million supported by leading investors."
    )


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
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "searchResults"

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b'{"results":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming '
            b'to revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-'
            b"based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-"
            b'access-for-ai/","content":"Linkup, a French startup providing AI with fast, ethical '
            b"access to online content, has secured \xe2\x82\xac3 million supported by leading "
            b"investors, including Seedcamp, Axeleo Capital, Motier Ventures, and a network of "
            b"prominent tech and media industry angels to further develop its sustainable "
            b"alternative to web scraping and address the challenges posed by AI-driven web "
            b'traffic."},{"name":"French Tech : Linkup, le moteur de recherche d\xc3\xa9di'
            b'\xc3\xa9 aux intelligences ...","url":"https://www.midilibre.fr/2024/11/18/french-'
            b"tech-linkup-le-moteur-de-recherche-dedie-aux-intelligences-artificielles-12331232."
            b'php","content":"La start-up Linkup, fond\xc3\xa9e d\xc3\xa9but 2024 par Philippe '
            b"Mizrahi, Denis Charrier et Boris Toledano, propose une avanc\xc3\xa9e r\xc3\xa9elle "
            b"dans l\xe2\x80\x99acc\xc3\xa8s des intelligences artificielles (IA) au contenu de "
            b'web."}]}',
        ),
    )

    response: Any = await client.async_search(query=query, depth=depth, output_type=output_type)

    assert isinstance(response, LinkupSearchResults)
    assert isinstance(response.results, list)
    assert response.results
    assert isinstance(response.results[0], LinkupSearchResult)
    assert (
        response.results[0].name
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        response.results[0].url
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        response.results[0].content
        == "Linkup, a French startup providing AI with fast, ethical access to online content, has "
        "secured €3 million supported by leading investors, including Seedcamp, Axeleo Capital, "
        "Motier Ventures, and a network of prominent tech and media industry angels to further "
        "develop its sustainable alternative to web scraping and address the challenges posed by "
        "AI-driven web traffic."
    )


@pytest.mark.asyncio
async def test_async_search_sourced_answer(mocker: MockerFixture, client: LinkupClient) -> None:
    query = "What is Linkup, the new French AI company?"
    depth = "standard"
    output_type = "sourcedAnswer"

    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b'{"answer":"Linkup is a Paris-based startup that focuses on providing AI with '
            b"fast and ethical access to online content. The company aims to create a sustainable "
            b"alternative to web scraping by addressing the challenges posed by AI-driven web "
            b"traffic. Linkup has recently raised \xe2\x82\xac3 million to further develop its "
            b"platform, which serves as an intermediary between AI technologies and content "
            b'publishers, allowing AI to access content in a way that is legal and efficient.",'
            b'"sources":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming to '
            b'revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-based-'
            b"linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-"
            b'for-ai/","snippet":"Linkup, a French startup providing AI with fast, ethical access '
            b"to online content, has secured \xe2\x82\xac3 million supported by leading "
            b'investors."},{"name":"Linkup l\xc3\xa8ve 3 millions d\xe2\x80\x99euros pour faire '
            b'le pont entre IA et les ...","url":"https://www.frenchweb.fr/linkup-leve-3-millions-'
            b"deuros-pour-faire-le-pont-entre-ia-et-les-editeurs-de-contenus-dans-un-monde-post-"
            b'webscraping/449941","snippet":"Linkup, une start-up parisienne fond\xc3\xa9e en '
            b"2024, veut proposer un acc\xc3\xa8s maitris\xc3\xa9 et l\xc3\xa9gal aux diff"
            b'\xc3\xa9rents protagonistes."}]}',
        ),
    )

    response: Any = await client.async_search(query=query, depth=depth, output_type=output_type)

    assert isinstance(response, LinkupSourcedAnswer)
    assert (
        response.answer
        == "Linkup is a Paris-based startup that focuses on providing AI with fast and ethical "
        "access to online content. The company aims to create a sustainable alternative to web "
        "scraping by addressing the challenges posed by AI-driven web traffic. Linkup has recently "
        "raised €3 million to further develop its platform, which serves as an intermediary "
        "between AI technologies and content publishers, allowing AI to access content in a way "
        "that is legal and efficient."
    )
    assert isinstance(response.sources, list)
    assert response.sources
    assert isinstance(response.sources[0], LinkupSource)
    assert (
        response.sources[0].name
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        response.sources[0].url
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        response.sources[0].snippet
        == "Linkup, a French startup providing AI with fast, ethical access to online content, has "
        "secured €3 million supported by leading investors."
    )


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