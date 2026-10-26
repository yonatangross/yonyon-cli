from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.ask_request_prefer import AskRequestPrefer





T = TypeVar("T", bound="AskRequest")



@_attrs_define
class AskRequest:
    """ 
        Attributes:
            query (str): The natural-language question.
            prefer (AskRequestPrefer | Unset):
     """

    query: str
    prefer: AskRequestPrefer | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.ask_request_prefer import AskRequestPrefer # noqa: PLC0415
        query = self.query

        prefer: dict[str, Any] | Unset = UNSET
        if not isinstance(self.prefer, Unset):
            prefer = self.prefer.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "query": query,
        })
        if prefer is not UNSET:
            field_dict["prefer"] = prefer

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ask_request_prefer import AskRequestPrefer # noqa: PLC0415
        d = dict(src_dict)
        query = d.pop("query")

        _prefer = d.pop("prefer", UNSET)
        prefer: AskRequestPrefer | Unset
        if isinstance(_prefer,  Unset):
            prefer = UNSET
        else:
            prefer = AskRequestPrefer.from_dict(_prefer)




        ask_request = cls(
            query=query,
            prefer=prefer,
        )


        ask_request.additional_properties = d
        return ask_request

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
