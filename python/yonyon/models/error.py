from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset






T = TypeVar("T", bound="Error")



@_attrs_define
class Error:
    """ Typed error envelope returned for every non-2xx response.

        Attributes:
            error (str): Human-readable message.
            code (ErrorCode): Stable machine-readable error token.
            retry_after (int | Unset): Seconds to wait before retrying (present on rate_limited).
            docs (str | Unset): Link to this OpenAPI document.
     """

    error: str
    code: ErrorCode
    retry_after: int | Unset = UNSET
    docs: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code.value

        retry_after = self.retry_after

        docs = self.docs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "error": error,
            "code": code,
        })
        if retry_after is not UNSET:
            field_dict["retry_after"] = retry_after
        if docs is not UNSET:
            field_dict["docs"] = docs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error")

        code = ErrorCode(d.pop("code"))




        retry_after = d.pop("retry_after", UNSET)

        docs = d.pop("docs", UNSET)

        error = cls(
            error=error,
            code=code,
            retry_after=retry_after,
            docs=docs,
        )


        error.additional_properties = d
        return error

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
