from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_root import ApiRoot
from ...models.error import Error
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiRoot | Error | None:
    if response.status_code == 200:
        response_200 = ApiRoot.from_dict(response.json())



        return response_200

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiRoot | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[ApiRoot | Error]:
    """ API root index

     Machine-readable index of the live public API surface: every endpoint with its method, the enforced
    rate limit, and pointers at this spec, the RFC 9727 api catalog, and the auth documentation. Public,
    anonymous, CORS-open, and rate-limited through the same limiter as every other endpoint, so the
    response carries live `RateLimit-*` and `X-RateLimit-*` values rather than only documenting them.
    Also sends `Link: <https://yonyon.ai/.well-known/api-catalog>; rel="api-catalog"` (RFC 9727). No
    authentication is required or accepted: this path always answers 200 and never sends a `WWW-
    Authenticate` challenge. See https://yonyon.ai/auth.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiRoot | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> ApiRoot | Error | None:
    """ API root index

     Machine-readable index of the live public API surface: every endpoint with its method, the enforced
    rate limit, and pointers at this spec, the RFC 9727 api catalog, and the auth documentation. Public,
    anonymous, CORS-open, and rate-limited through the same limiter as every other endpoint, so the
    response carries live `RateLimit-*` and `X-RateLimit-*` values rather than only documenting them.
    Also sends `Link: <https://yonyon.ai/.well-known/api-catalog>; rel="api-catalog"` (RFC 9727). No
    authentication is required or accepted: this path always answers 200 and never sends a `WWW-
    Authenticate` challenge. See https://yonyon.ai/auth.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiRoot | Error
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[ApiRoot | Error]:
    """ API root index

     Machine-readable index of the live public API surface: every endpoint with its method, the enforced
    rate limit, and pointers at this spec, the RFC 9727 api catalog, and the auth documentation. Public,
    anonymous, CORS-open, and rate-limited through the same limiter as every other endpoint, so the
    response carries live `RateLimit-*` and `X-RateLimit-*` values rather than only documenting them.
    Also sends `Link: <https://yonyon.ai/.well-known/api-catalog>; rel="api-catalog"` (RFC 9727). No
    authentication is required or accepted: this path always answers 200 and never sends a `WWW-
    Authenticate` challenge. See https://yonyon.ai/auth.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiRoot | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> ApiRoot | Error | None:
    """ API root index

     Machine-readable index of the live public API surface: every endpoint with its method, the enforced
    rate limit, and pointers at this spec, the RFC 9727 api catalog, and the auth documentation. Public,
    anonymous, CORS-open, and rate-limited through the same limiter as every other endpoint, so the
    response carries live `RateLimit-*` and `X-RateLimit-*` values rather than only documenting them.
    Also sends `Link: <https://yonyon.ai/.well-known/api-catalog>; rel="api-catalog"` (RFC 9727). No
    authentication is required or accepted: this path always answers 200 and never sends a `WWW-
    Authenticate` challenge. See https://yonyon.ai/auth.md.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiRoot | Error
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
