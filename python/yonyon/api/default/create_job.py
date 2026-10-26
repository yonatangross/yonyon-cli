from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_job_body import CreateJobBody
from ...models.error import Error
from ...models.job_accepted import JobAccepted
from typing import cast



def _get_kwargs(
    *,
    body: CreateJobBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/jobs",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | JobAccepted | None:
    if response.status_code == 202:
        response_202 = JobAccepted.from_dict(response.json())



        return response_202

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | JobAccepted]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobBody,

) -> Response[Error | JobAccepted]:
    """ Start an async read job

     Accepts a read operation and returns 202 Accepted with a Location header and a job_id in the body.
    Poll GET /api/v1/jobs/{jobId} for the result. The public API is read-only, so the job always
    succeeds or fails on the poll; there is no queue to cancel.

    Args:
        body (CreateJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | JobAccepted]
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
    body: CreateJobBody,

) -> Error | JobAccepted | None:
    """ Start an async read job

     Accepts a read operation and returns 202 Accepted with a Location header and a job_id in the body.
    Poll GET /api/v1/jobs/{jobId} for the result. The public API is read-only, so the job always
    succeeds or fails on the poll; there is no queue to cancel.

    Args:
        body (CreateJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | JobAccepted
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateJobBody,

) -> Response[Error | JobAccepted]:
    """ Start an async read job

     Accepts a read operation and returns 202 Accepted with a Location header and a job_id in the body.
    Poll GET /api/v1/jobs/{jobId} for the result. The public API is read-only, so the job always
    succeeds or fails on the poll; there is no queue to cancel.

    Args:
        body (CreateJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | JobAccepted]
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
    body: CreateJobBody,

) -> Error | JobAccepted | None:
    """ Start an async read job

     Accepts a read operation and returns 202 Accepted with a Location header and a job_id in the body.
    Poll GET /api/v1/jobs/{jobId} for the result. The public API is read-only, so the job always
    succeeds or fails on the poll; there is no queue to cancel.

    Args:
        body (CreateJobBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | JobAccepted
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
