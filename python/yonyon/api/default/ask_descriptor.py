from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.ask_descriptor import AskDescriptor
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    query: str | Unset = UNSET,
    streaming: bool | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["query"] = query

    params["streaming"] = streaming


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/ask",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AskDescriptor | None:
    if response.status_code == 200:
        response_200 = AskDescriptor.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AskDescriptor]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    streaming: bool | Unset = UNSET,

) -> Response[AskDescriptor]:
    """ NLWeb endpoint descriptor

     Returns a small JSON descriptor of how to call POST /ask. Fetch this first if you are discovering
    the endpoint programmatically. Also accepts ?query= for a GET query and ?streaming=true to request
    SSE.

    Args:
        query (str | Unset):
        streaming (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AskDescriptor]
     """


    kwargs = _get_kwargs(
        query=query,
streaming=streaming,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    streaming: bool | Unset = UNSET,

) -> AskDescriptor | None:
    """ NLWeb endpoint descriptor

     Returns a small JSON descriptor of how to call POST /ask. Fetch this first if you are discovering
    the endpoint programmatically. Also accepts ?query= for a GET query and ?streaming=true to request
    SSE.

    Args:
        query (str | Unset):
        streaming (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AskDescriptor
     """


    return sync_detailed(
        client=client,
query=query,
streaming=streaming,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    streaming: bool | Unset = UNSET,

) -> Response[AskDescriptor]:
    """ NLWeb endpoint descriptor

     Returns a small JSON descriptor of how to call POST /ask. Fetch this first if you are discovering
    the endpoint programmatically. Also accepts ?query= for a GET query and ?streaming=true to request
    SSE.

    Args:
        query (str | Unset):
        streaming (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AskDescriptor]
     """


    kwargs = _get_kwargs(
        query=query,
streaming=streaming,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    query: str | Unset = UNSET,
    streaming: bool | Unset = UNSET,

) -> AskDescriptor | None:
    """ NLWeb endpoint descriptor

     Returns a small JSON descriptor of how to call POST /ask. Fetch this first if you are discovering
    the endpoint programmatically. Also accepts ?query= for a GET query and ?streaming=true to request
    SSE.

    Args:
        query (str | Unset):
        streaming (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AskDescriptor
     """


    return (await asyncio_detailed(
        client=client,
query=query,
streaming=streaming,

    )).parsed
