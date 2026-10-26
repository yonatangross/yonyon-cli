from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_accepted_op import JobAcceptedOp
from ..models.job_accepted_status import JobAcceptedStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="JobAccepted")



@_attrs_define
class JobAccepted:
    """ 202 Accepted body for POST /api/v1/jobs.

        Attributes:
            job_id (str): Opaque job identifier. Pass it to GET /api/v1/jobs/{jobId}.
            status (JobAcceptedStatus): Always accepted on 202.
            status_url (str): Absolute URL to poll for the result.
            op (JobAcceptedOp | Unset):
     """

    job_id: str
    status: JobAcceptedStatus
    status_url: str
    op: JobAcceptedOp | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        status = self.status.value

        status_url = self.status_url

        op: str | Unset = UNSET
        if not isinstance(self.op, Unset):
            op = self.op.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "job_id": job_id,
            "status": status,
            "status_url": status_url,
        })
        if op is not UNSET:
            field_dict["op"] = op

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = JobAcceptedStatus(d.pop("status"))




        status_url = d.pop("status_url")

        _op = d.pop("op", UNSET)
        op: JobAcceptedOp | Unset
        if isinstance(_op,  Unset):
            op = UNSET
        else:
            op = JobAcceptedOp(_op)




        job_accepted = cls(
            job_id=job_id,
            status=status,
            status_url=status_url,
            op=op,
        )


        job_accepted.additional_properties = d
        return job_accepted

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
