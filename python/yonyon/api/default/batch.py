from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.batch_request import BatchRequest
from ...models.batch_response import BatchResponse
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: BatchRequest,
    idempotency_key: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/batch",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BatchResponse | Error | None:
    if response.status_code == 200:
        response_200 = BatchResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BatchResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BatchRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[BatchResponse | Error]:
    """ Run up to 10 read operations in one request

     Runs up to 10 read-only operations in a single round-trip. Each operation is `{ "op":
    "projects"|"services"|"about", "params": { "q"?: string } }`; only `projects` uses `q` (a keyword
    filter). Every operation is read-only and idempotent, so an optional `Idempotency-Key` request
    header is accepted and echoed on the response. A per-operation failure (e.g. an unknown op) is
    reported inline with `status: "error"` and never fails the whole batch. Public, anonymous, CORS-
    open, rate-limited (10 requests/IP/minute).

    Args:
        idempotency_key (str | Unset):
        body (BatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchResponse | Error]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: BatchRequest,
    idempotency_key: str | Unset = UNSET,

) -> BatchResponse | Error | None:
    """ Run up to 10 read operations in one request

     Runs up to 10 read-only operations in a single round-trip. Each operation is `{ "op":
    "projects"|"services"|"about", "params": { "q"?: string } }`; only `projects` uses `q` (a keyword
    filter). Every operation is read-only and idempotent, so an optional `Idempotency-Key` request
    header is accepted and echoed on the response. A per-operation failure (e.g. an unknown op) is
    reported inline with `status: "error"` and never fails the whole batch. Public, anonymous, CORS-
    open, rate-limited (10 requests/IP/minute).

    Args:
        idempotency_key (str | Unset):
        body (BatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchResponse | Error
     """


    return sync_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BatchRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[BatchResponse | Error]:
    """ Run up to 10 read operations in one request

     Runs up to 10 read-only operations in a single round-trip. Each operation is `{ "op":
    "projects"|"services"|"about", "params": { "q"?: string } }`; only `projects` uses `q` (a keyword
    filter). Every operation is read-only and idempotent, so an optional `Idempotency-Key` request
    header is accepted and echoed on the response. A per-operation failure (e.g. an unknown op) is
    reported inline with `status: "error"` and never fails the whole batch. Public, anonymous, CORS-
    open, rate-limited (10 requests/IP/minute).

    Args:
        idempotency_key (str | Unset):
        body (BatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchResponse | Error]
     """


    kwargs = _get_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BatchRequest,
    idempotency_key: str | Unset = UNSET,

) -> BatchResponse | Error | None:
    """ Run up to 10 read operations in one request

     Runs up to 10 read-only operations in a single round-trip. Each operation is `{ "op":
    "projects"|"services"|"about", "params": { "q"?: string } }`; only `projects` uses `q` (a keyword
    filter). Every operation is read-only and idempotent, so an optional `Idempotency-Key` request
    header is accepted and echoed on the response. A per-operation failure (e.g. an unknown op) is
    reported inline with `status: "error"` and never fails the whole batch. Public, anonymous, CORS-
    open, rate-limited (10 requests/IP/minute).

    Args:
        idempotency_key (str | Unset):
        body (BatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchResponse | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
