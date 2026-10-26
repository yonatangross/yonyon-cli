from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_list import ProjectList
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    q: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["q"] = q

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/projects",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectList | None:
    if response.status_code == 200:
        response_200 = ProjectList.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,

) -> Response[Error | ProjectList]:
    """ List Yonatan's portfolio projects

     Returns Yonatan Gross's portfolio projects as JSON. Public, anonymous, CORS-open, rate-limited (10
    requests/IP/minute). Supports an optional `?q=` keyword filter (matched against project name +
    description) and opaque cursor pagination via `?limit=` (1-50) and `?cursor=`. The response carries
    `count`, `total`, `nextCursor`, `next_cursor`, and `has_more` (`nextCursor` is null on the last
    page).

    Args:
        q (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectList]
     """


    kwargs = _get_kwargs(
        q=q,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,

) -> Error | ProjectList | None:
    """ List Yonatan's portfolio projects

     Returns Yonatan Gross's portfolio projects as JSON. Public, anonymous, CORS-open, rate-limited (10
    requests/IP/minute). Supports an optional `?q=` keyword filter (matched against project name +
    description) and opaque cursor pagination via `?limit=` (1-50) and `?cursor=`. The response carries
    `count`, `total`, `nextCursor`, `next_cursor`, and `has_more` (`nextCursor` is null on the last
    page).

    Args:
        q (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectList
     """


    return sync_detailed(
        client=client,
q=q,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,

) -> Response[Error | ProjectList]:
    """ List Yonatan's portfolio projects

     Returns Yonatan Gross's portfolio projects as JSON. Public, anonymous, CORS-open, rate-limited (10
    requests/IP/minute). Supports an optional `?q=` keyword filter (matched against project name +
    description) and opaque cursor pagination via `?limit=` (1-50) and `?cursor=`. The response carries
    `count`, `total`, `nextCursor`, `next_cursor`, and `has_more` (`nextCursor` is null on the last
    page).

    Args:
        q (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectList]
     """


    kwargs = _get_kwargs(
        q=q,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = UNSET,
    limit: int | Unset = UNSET,
    cursor: str | Unset = UNSET,

) -> Error | ProjectList | None:
    """ List Yonatan's portfolio projects

     Returns Yonatan Gross's portfolio projects as JSON. Public, anonymous, CORS-open, rate-limited (10
    requests/IP/minute). Supports an optional `?q=` keyword filter (matched against project name +
    description) and opaque cursor pagination via `?limit=` (1-50) and `?cursor=`. The response carries
    `count`, `total`, `nextCursor`, `next_cursor`, and `has_more` (`nextCursor` is null on the last
    page).

    Args:
        q (str | Unset):
        limit (int | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectList
     """


    return (await asyncio_detailed(
        client=client,
q=q,
limit=limit,
cursor=cursor,

    )).parsed
