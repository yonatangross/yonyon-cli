from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.api_version_root_status import ApiVersionRootStatus
from ..types import UNSET, Unset
from typing import cast
from typing import Literal, cast

if TYPE_CHECKING:
  from ..models.endpoint import Endpoint
  from ..models.rate_limit_policy import RateLimitPolicy





T = TypeVar("T", bound="ApiVersionRoot")



@_attrs_define
class ApiVersionRoot:
    """ Index of one major version of the REST surface, served at GET /api/v1.

        Attributes:
            name (str):
            version (int):
            code (Literal['api_version_root']):
            status (ApiVersionRootStatus): Lifecycle of this version. `stable` until a Deprecation/Sunset header says
                otherwise.
            auth (str):
            rate_limit (RateLimitPolicy): The rate limit actually enforced on this API, as machine-readable JSON.
            endpoints (list[Endpoint]):
            openapi (str):
            docs (str):
            message (str | Unset):
            api_root (str | Unset):
     """

    name: str
    version: int
    code: Literal['api_version_root']
    status: ApiVersionRootStatus
    auth: str
    rate_limit: RateLimitPolicy
    endpoints: list[Endpoint]
    openapi: str
    docs: str
    message: str | Unset = UNSET
    api_root: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.endpoint import Endpoint # noqa: PLC0415
        from ..models.rate_limit_policy import RateLimitPolicy # noqa: PLC0415
        name = self.name

        version = self.version

        code = self.code

        status = self.status.value

        auth = self.auth

        rate_limit = self.rate_limit.to_dict()

        endpoints = []
        for endpoints_item_data in self.endpoints:
            endpoints_item = endpoints_item_data.to_dict()
            endpoints.append(endpoints_item)



        openapi = self.openapi

        docs = self.docs

        message = self.message

        api_root = self.api_root


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "version": version,
            "code": code,
            "status": status,
            "auth": auth,
            "rate_limit": rate_limit,
            "endpoints": endpoints,
            "openapi": openapi,
            "docs": docs,
        })
        if message is not UNSET:
            field_dict["message"] = message
        if api_root is not UNSET:
            field_dict["api_root"] = api_root

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.endpoint import Endpoint # noqa: PLC0415
        from ..models.rate_limit_policy import RateLimitPolicy # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        code = cast(Literal['api_version_root'] , d.pop("code"))
        if code != 'api_version_root':
            raise ValueError(f"code must match const 'api_version_root', got '{code}'")

        status = ApiVersionRootStatus(d.pop("status"))




        auth = d.pop("auth")

        rate_limit = RateLimitPolicy.from_dict(d.pop("rate_limit"))




        endpoints = []
        _endpoints = d.pop("endpoints")
        for endpoints_item_data in (_endpoints):
            endpoints_item = Endpoint.from_dict(endpoints_item_data)



            endpoints.append(endpoints_item)


        openapi = d.pop("openapi")

        docs = d.pop("docs")

        message = d.pop("message", UNSET)

        api_root = d.pop("api_root", UNSET)

        api_version_root = cls(
            name=name,
            version=version,
            code=code,
            status=status,
            auth=auth,
            rate_limit=rate_limit,
            endpoints=endpoints,
            openapi=openapi,
            docs=docs,
            message=message,
            api_root=api_root,
        )


        api_version_root.additional_properties = d
        return api_version_root

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
