# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class TrackerRefs(BaseModel):
    tracker_ref: Optional[RefIdItem] = Field(default=None, validation_alias="trackerRef")


CombineBoolean = Literal[
    "and",
    "or",
]


class TrackerGroup(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["trackergroup"] = Field(default="trackergroup", exclude=True, frozen=True)
    combine_boolean: Union[Global[CombineBoolean], Variable, Default[Literal["or"]]] = Field(
        validation_alias=AliasPath("data", "combineBoolean")
    )
    tracker_group_name: Optional[Union[Variable, Global[str]]] = Field(
        validation_alias=AliasPath("data", "trackerGroupName")
    )
    tracker_refs: List[TrackerRefs] = Field(
        validation_alias=AliasPath("data", "trackerRefs"), description="trackers ref list"
    )


class TrackerGroupIPv6(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["ipv6-trackergroup"] = Field(default="ipv6-trackergroup", exclude=True, frozen=True)
    combine_boolean: Union[Global[CombineBoolean], Variable, Default[Literal["or"]]] = Field(
        validation_alias=AliasPath("data", "combineBoolean")
    )
    tracker_group_name: Optional[Union[Variable, Global[str]]] = Field(
        validation_alias=AliasPath("data", "trackerGroupName")
    )
    tracker_refs: List[TrackerRefs] = Field(
        validation_alias=AliasPath("data", "trackerRefs"), description="trackers ref list"
    )
