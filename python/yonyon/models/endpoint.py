from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Endpoint")



@_attrs_define
class Endpoint:
    """ One endpoint that is live on this API today.

        Attributes:
            method (str): HTTP method the endpoint answers.
            path (str): Path relative to https://yonyon.ai.
            description (str):
     """

    method: str
    path: str
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        method = self.method

        path = self.path

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "method": method,
            "path": path,
            "description": description,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = d.pop("method")

        path = d.pop("path")

        description = d.pop("description")

        endpoint = cls(
            method=method,
            path=path,
            description=description,
        )


        endpoint.additional_properties = d
        return endpoint

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
