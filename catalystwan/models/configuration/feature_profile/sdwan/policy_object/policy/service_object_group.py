# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase, _ParcelEntry
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class ServiceObjectGrouEntries(_ParcelEntry):
    object_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="objectGroup", serialization_alias="objectGroup"
    )


class ServiceObjectGroupParcel(_ParcelBase):
    type_: Literal["service-object-group"] = Field(default="service-object-group", exclude=True)
    entries: List[ServiceObjectGrouEntries] = Field(
        validation_alias=AliasPath("data", "entries"),
        description="object-group Entries",
    )
