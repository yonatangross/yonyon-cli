from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.chat_request import ChatRequest
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: ChatRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/chat",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ChatRequest,

) -> Response[Error | str]:
    """ Ask a question about Yonatan Gross (streaming)

     Streams a grounded answer about Yonatan's work, projects, services, and experience. Public and rate-
    limited (10 requests/IP/minute). No authentication required. Browser-facing: requests must carry an
    Origin matching the host (CSRF). For server-side agents, prefer POST /ask.

    Args:
        body (ChatRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ChatRequest,

) -> Error | str | None:
    """ Ask a question about Yonatan Gross (streaming)

     Streams a grounded answer about Yonatan's work, projects, services, and experience. Public and rate-
    limited (10 requests/IP/minute). No authentication required. Browser-facing: requests must carry an
    Origin matching the host (CSRF). For server-side agents, prefer POST /ask.

    Args:
        body (ChatRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ChatRequest,

) -> Response[Error | str]:
    """ Ask a question about Yonatan Gross (streaming)

     Streams a grounded answer about Yonatan's work, projects, services, and experience. Public and rate-
    limited (10 requests/IP/minute). No authentication required. Browser-facing: requests must carry an
    Origin matching the host (CSRF). For server-side agents, prefer POST /ask.

    Args:
        body (ChatRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ChatRequest,

) -> Error | str | None:
    """ Ask a question about Yonatan Gross (streaming)

     Streams a grounded answer about Yonatan's work, projects, services, and experience. Public and rate-
    limited (10 requests/IP/minute). No authentication required. Browser-facing: requests must carry an
    Origin matching the host (CSRF). For server-side agents, prefer POST /ask.

    Args:
        body (ChatRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
