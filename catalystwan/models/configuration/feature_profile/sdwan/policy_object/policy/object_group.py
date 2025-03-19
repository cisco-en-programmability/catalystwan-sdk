# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.models.configuration.feature_profile.common import ObjectGroupEntries


class ObjectGroupParcel(_ParcelBase):
    type_: Literal["object-group"] = Field(default="object-group", exclude=True)
    entries: List[ObjectGroupEntries] = Field(
        validation_alias=AliasPath("data", "entries"),
        description="object-group Entries",
    )
