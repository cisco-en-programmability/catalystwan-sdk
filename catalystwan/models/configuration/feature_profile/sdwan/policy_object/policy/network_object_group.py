# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, _ParcelEntry
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, ObjectGroupEntries, RefIdItem


class NetworkObjectGroupParcel(_ParcelBase):
    type_: Literal["network-object-group"] = Field(default="network-object-group", exclude=True)
    entries: List[ObjectGroupEntries] = Field(
        validation_alias=AliasPath("data", "entries"),
        description="object-group Entries",
    )
