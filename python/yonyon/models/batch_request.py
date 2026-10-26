from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.batch_request_operations_item import BatchRequestOperationsItem





T = TypeVar("T", bound="BatchRequest")



@_attrs_define
class BatchRequest:
    """ 
        Attributes:
            operations (list[BatchRequestOperationsItem]): Between 1 and 10 read operations, executed in order.
     """

    operations: list[BatchRequestOperationsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_request_operations_item import BatchRequestOperationsItem # noqa: PLC0415
        operations = []
        for operations_item_data in self.operations:
            operations_item = operations_item_data.to_dict()
            operations.append(operations_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "operations": operations,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_request_operations_item import BatchRequestOperationsItem # noqa: PLC0415
        d = dict(src_dict)
        operations = []
        _operations = d.pop("operations")
        for operations_item_data in (_operations):
            operations_item = BatchRequestOperationsItem.from_dict(operations_item_data)



            operations.append(operations_item)


        batch_request = cls(
            operations=operations,
        )


        batch_request.additional_properties = d
        return batch_request

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
