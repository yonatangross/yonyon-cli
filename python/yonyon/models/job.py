from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.job_op import JobOp
from ..models.job_status import JobStatus
from typing import cast

if TYPE_CHECKING:
  from ..models.job_result import JobResult





T = TypeVar("T", bound="Job")



@_attrs_define
class Job:
    """ Polled job result from GET /api/v1/jobs/{jobId}.

        Attributes:
            job_id (str):
            status (JobStatus): Jobs on this API complete on the first poll.
            op (JobOp):
            result (JobResult): The read result (projects list, services markdown, or about markdown).
     """

    job_id: str
    status: JobStatus
    op: JobOp
    result: JobResult
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.job_result import JobResult # noqa: PLC0415
        job_id = self.job_id

        status = self.status.value

        op = self.op.value

        result = self.result.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "job_id": job_id,
            "status": status,
            "op": op,
            "result": result,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_result import JobResult # noqa: PLC0415
        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = JobStatus(d.pop("status"))




        op = JobOp(d.pop("op"))




        result = JobResult.from_dict(d.pop("result"))




        job = cls(
            job_id=job_id,
            status=status,
            op=op,
            result=result,
        )


        job.additional_properties = d
        return job

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
