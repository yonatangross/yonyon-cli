from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.ask_stream_start_meta import AskStreamStartMeta





T = TypeVar("T", bound="AskStreamStart")



@_attrs_define
class AskStreamStart:
    """ Payload of the `start` event. Echoes the accepted query.

        Attributes:
            field_meta (AskStreamStartMeta): NLWeb envelope metadata.
            query (str): The query as the server parsed it.
     """

    field_meta: AskStreamStartMeta
    query: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.ask_stream_start_meta import AskStreamStartMeta # noqa: PLC0415
        field_meta = self.field_meta.to_dict()

        query = self.query


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "_meta": field_meta,
            "query": query,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ask_stream_start_meta import AskStreamStartMeta # noqa: PLC0415
        d = dict(src_dict)
        field_meta = AskStreamStartMeta.from_dict(d.pop("_meta"))




        query = d.pop("query")

        ask_stream_start = cls(
            field_meta=field_meta,
            query=query,
        )


        ask_stream_start.additional_properties = d
        return ask_stream_start

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
