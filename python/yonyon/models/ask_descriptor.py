from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.ask_descriptor_method import AskDescriptorMethod
from ..types import UNSET, Unset
from typing import cast
from typing import Literal, cast

if TYPE_CHECKING:
  from ..models.ask_descriptor_meta import AskDescriptorMeta
  from ..models.ask_descriptor_results_item import AskDescriptorResultsItem





T = TypeVar("T", bound="AskDescriptor")



@_attrs_define
class AskDescriptor:
    """ Self-describing descriptor for the NLWeb query endpoint. Returned by GET /ask so an agent can learn how to call POST
    /ask without reading prose documentation.

        Attributes:
            field_meta (AskDescriptorMeta): NLWeb envelope metadata.
            answer (str): Human and agent readable instructions for calling this endpoint.
            method (AskDescriptorMethod): HTTP method to use for a real query.
            url (str): Absolute URL to POST a query to.
            streaming (bool): Whether the endpoint can stream Server-Sent Events.
            context (Literal['https://schema.org'] | Unset): JSON-LD context.
            query (str | Unset): Always empty on the descriptor; present so the descriptor and a real answer share one
                shape.
            results (list[AskDescriptorResultsItem] | Unset): Always empty on the descriptor.
     """

    field_meta: AskDescriptorMeta
    answer: str
    method: AskDescriptorMethod
    url: str
    streaming: bool
    context: Literal['https://schema.org'] | Unset = UNSET
    query: str | Unset = UNSET
    results: list[AskDescriptorResultsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.ask_descriptor_meta import AskDescriptorMeta # noqa: PLC0415
        from ..models.ask_descriptor_results_item import AskDescriptorResultsItem # noqa: PLC0415
        field_meta = self.field_meta.to_dict()

        answer = self.answer

        method = self.method.value

        url = self.url

        streaming = self.streaming

        context = self.context

        query = self.query

        results: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "_meta": field_meta,
            "answer": answer,
            "method": method,
            "url": url,
            "streaming": streaming,
        })
        if context is not UNSET:
            field_dict["@context"] = context
        if query is not UNSET:
            field_dict["query"] = query
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ask_descriptor_meta import AskDescriptorMeta # noqa: PLC0415
        from ..models.ask_descriptor_results_item import AskDescriptorResultsItem # noqa: PLC0415
        d = dict(src_dict)
        field_meta = AskDescriptorMeta.from_dict(d.pop("_meta"))




        answer = d.pop("answer")

        method = AskDescriptorMethod(d.pop("method"))




        url = d.pop("url")

        streaming = d.pop("streaming")

        context = cast(Literal['https://schema.org'] | Unset , d.pop("@context", UNSET))
        if context != 'https://schema.org'and not isinstance(context, Unset):
            raise ValueError(f"@context must match const 'https://schema.org', got '{context}'")

        query = d.pop("query", UNSET)

        _results = d.pop("results", UNSET)
        results: list[AskDescriptorResultsItem] | Unset = UNSET
        if _results is not UNSET:
            results = []
            for results_item_data in _results:
                results_item = AskDescriptorResultsItem.from_dict(results_item_data)



                results.append(results_item)


        ask_descriptor = cls(
            field_meta=field_meta,
            answer=answer,
            method=method,
            url=url,
            streaming=streaming,
            context=context,
            query=query,
            results=results,
        )


        ask_descriptor.additional_properties = d
        return ask_descriptor

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
