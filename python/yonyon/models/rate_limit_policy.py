from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.rate_limit_policy_scope import RateLimitPolicyScope






T = TypeVar("T", bound="RateLimitPolicy")



@_attrs_define
class RateLimitPolicy:
    """ The rate limit actually enforced on this API, as machine-readable JSON.

        Attributes:
            requests (int): Requests allowed per window.
            window_seconds (int): Window length in seconds.
            scope (RateLimitPolicyScope): What the window is keyed on.
     """

    requests: int
    window_seconds: int
    scope: RateLimitPolicyScope
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        requests = self.requests

        window_seconds = self.window_seconds

        scope = self.scope.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "requests": requests,
            "window_seconds": window_seconds,
            "scope": scope,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        requests = d.pop("requests")

        window_seconds = d.pop("window_seconds")

        scope = RateLimitPolicyScope(d.pop("scope"))




        rate_limit_policy = cls(
            requests=requests,
            window_seconds=window_seconds,
            scope=scope,
        )


        rate_limit_policy.additional_properties = d
        return rate_limit_policy

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
