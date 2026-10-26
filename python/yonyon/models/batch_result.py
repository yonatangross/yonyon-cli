from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.batch_result_status import BatchResultStatus






T = TypeVar("T", bound="BatchResult")



@_attrs_define
class BatchResult:
    """ 
        Attributes:
            op (str): The op that ran (or "(missing)" when none was supplied).
            status (BatchResultStatus): Per-operation outcome. An error here does not fail the batch.
            data (Any): The op's result payload (shape depends on op), or an { error, code } envelope when status is
                "error".
     """

    op: str
    status: BatchResultStatus
    data: Any
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        op = self.op

        status = self.status.value

        data = self.data


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "op": op,
            "status": status,
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        op = d.pop("op")

        status = BatchResultStatus(d.pop("status"))




        data = d.pop("data")

        batch_result = cls(
            op=op,
            status=status,
            data=data,
        )


        batch_result.additional_properties = d
        return batch_result

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
