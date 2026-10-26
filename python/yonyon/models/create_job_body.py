from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_job_body_op import CreateJobBodyOp
from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateJobBody")



@_attrs_define
class CreateJobBody:
    """ 
        Attributes:
            op (CreateJobBodyOp): Which read to run.
            q (str | Unset): Keyword filter (only applied to the projects op).
     """

    op: CreateJobBodyOp
    q: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        op = self.op.value

        q = self.q


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "op": op,
        })
        if q is not UNSET:
            field_dict["q"] = q

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        op = CreateJobBodyOp(d.pop("op"))




        q = d.pop("q", UNSET)

        create_job_body = cls(
            op=op,
            q=q,
        )


        create_job_body.additional_properties = d
        return create_job_body

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
