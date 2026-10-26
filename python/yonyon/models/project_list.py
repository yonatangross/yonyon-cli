from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.project import Project





T = TypeVar("T", bound="ProjectList")



@_attrs_define
class ProjectList:
    """ A cursor-paginated page of projects.

        Attributes:
            count (int): Number of projects in this page.
            total (int): Total projects across all pages for the current filter.
            nextCursor (None | str): Opaque base64url cursor for the next page, or null when this is the last page.
            next_cursor (None | str): Snake_case alias of nextCursor, for agents that look up next_cursor.
            has_more (bool): True when another page is available. Equivalent to next_cursor != null.
            projects (list[Project]):
     """

    count: int
    total: int
    nextCursor: None | str
    next_cursor: None | str
    has_more: bool
    projects: list[Project]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.project import Project # noqa: PLC0415
        count = self.count

        total = self.total

        nextCursor: None | str
        nextCursor = self.nextCursor

        next_cursor: None | str
        next_cursor = self.next_cursor

        has_more = self.has_more

        projects = []
        for projects_item_data in self.projects:
            projects_item = projects_item_data.to_dict()
            projects.append(projects_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "count": count,
            "total": total,
            "nextCursor": nextCursor,
            "next_cursor": next_cursor,
            "has_more": has_more,
            "projects": projects,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project import Project # noqa: PLC0415
        d = dict(src_dict)
        count = d.pop("count")

        total = d.pop("total")

        def _parse_nextCursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        nextCursor = _parse_nextCursor(d.pop("nextCursor"))


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))


        has_more = d.pop("has_more")

        projects = []
        _projects = d.pop("projects")
        for projects_item_data in (_projects):
            projects_item = Project.from_dict(projects_item_data)



            projects.append(projects_item)


        project_list = cls(
            count=count,
            total=total,
            nextCursor=nextCursor,
            next_cursor=next_cursor,
            has_more=has_more,
            projects=projects,
        )


        project_list.additional_properties = d
        return project_list

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
