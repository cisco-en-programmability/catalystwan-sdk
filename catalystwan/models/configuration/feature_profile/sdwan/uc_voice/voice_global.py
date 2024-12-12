# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

IpFormat = Literal[
    "ipv4",
    "ipv6",
]


class TrustedPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ip: Optional[Union[Variable, Default[None], Global[str]]] = Field(default=None)
    ip_format: Optional[Union[Variable, Default[None], Global[IpFormat]]] = Field(
        default=None, validation_alias="ipFormat", serialization_alias="ipFormat"
    )


class ClockPrioritySorting(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    clock_priority: Optional[Global[int]] = Field(
        default=None, validation_alias="clockPriority", serialization_alias="clockPriority"
    )
    clock_priority_sorting_port: Optional[Union[Variable, Default[None], Global[str]]] = Field(
        default=None, validation_alias="clockPrioritySortingPort", serialization_alias="clockPrioritySortingPort"
    )


class VoiceGlobalParcel(_ParcelBase):
    type_: Literal["voice-global"] = Field(default="voice-global", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    clock_priority_sorting: Optional[List[ClockPrioritySorting]] = Field(
        default=None,
        validation_alias=AliasPath("data", "clockPrioritySorting"),
        description="Clock Priority Sorting",
    )
    source_interface: Optional[Union[Variable, Default[None], Global[str]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "sourceInterface"),
    )
    sync: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "sync")
    )
    trusted_prefix_list: Optional[List[TrustedPrefixList]] = Field(
        default=None,
        validation_alias=AliasPath("data", "trustedPrefixList"),
        description="Prefix List",
    )
    wait_to_restore: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "waitToRestore"),
    )
