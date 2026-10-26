from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.batch_request_operations_item_op import BatchRequestOperationsItemOp
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.batch_request_operations_item_params import BatchRequestOperationsItemParams





T = TypeVar("T", bound="BatchRequestOperationsItem")



@_attrs_define
class BatchRequestOperationsItem:
    """ 
        Attributes:
            op (BatchRequestOperationsItemOp): Which read to run.
            params (BatchRequestOperationsItemParams | Unset):
     """

    op: BatchRequestOperationsItemOp
    params: BatchRequestOperationsItemParams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_request_operations_item_params import BatchRequestOperationsItemParams # noqa: PLC0415
        op = self.op.value

        params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "op": op,
        })
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_request_operations_item_params import BatchRequestOperationsItemParams # noqa: PLC0415
        d = dict(src_dict)
        op = BatchRequestOperationsItemOp(d.pop("op"))




        _params = d.pop("params", UNSET)
        params: BatchRequestOperationsItemParams | Unset
        if isinstance(_params,  Unset):
            params = UNSET
        else:
            params = BatchRequestOperationsItemParams.from_dict(_params)




        batch_request_operations_item = cls(
            op=op,
            params=params,
        )


        batch_request_operations_item.additional_properties = d
        return batch_request_operations_item

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
