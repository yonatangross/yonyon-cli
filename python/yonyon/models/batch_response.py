from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.batch_result import BatchResult





T = TypeVar("T", bound="BatchResponse")



@_attrs_define
class BatchResponse:
    """ 
        Attributes:
            count (int): Number of operations run (equals results.length).
            results (list[BatchResult]):
     """

    count: int
    results: list[BatchResult]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_result import BatchResult # noqa: PLC0415
        count = self.count

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "count": count,
            "results": results,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_result import BatchResult # noqa: PLC0415
        d = dict(src_dict)
        count = d.pop("count")

        results = []
        _results = d.pop("results")
        for results_item_data in (_results):
            results_item = BatchResult.from_dict(results_item_data)



            results.append(results_item)


        batch_response = cls(
            count=count,
            results=results,
        )


        batch_response.additional_properties = d
        return batch_response

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
