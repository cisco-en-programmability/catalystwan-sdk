# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry


class ScalableGroupTagEntry(_ParcelEntry):
    sgt_name: Global[str] = Field(validation_alias="sgtName", serialization_alias="sgtName")
    tag: Global[str]


class ScalableGroupTagParcel(_ParcelBase):
    type_: Literal["security-scalablegrouptag"] = Field(default="security-scalablegrouptag")
    entries: List[ScalableGroupTagEntry] = Field(validation_alias=AliasPath("data", "entries"), default_factory=list)

    def add_entry(self, sgt_name: str, tag: str):
        self.entries.append(
            ScalableGroupTagEntry(
                sgt_name=Global[str](value=sgt_name),
                tag=Global[str](value=tag),
            )
        )
