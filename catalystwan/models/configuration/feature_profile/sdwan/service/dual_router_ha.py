# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class RedundancyGroups(BaseModel):
    group_id: int = Field(ge=1, le=2, validation_alias="groupId", serialization_alias="groupId")
    vpn_ids: List[RefIdItem] = Field(validation_alias="vpnIds", serialization_alias="vpnIds")
    tag_name: Optional[str] = Field(
        default=None, pattern='^[^&<>! ",]+$', validation_alias="tagName", serialization_alias="tagName"
    )


class DualRouterHaParcel(_ParcelBase):
    type_: Literal["dual-router-ha"] = Field(default="dual-router-ha", exclude=True)
    enable_optimize_paths: Union[Global[bool], Default[bool]] = Field(
        validation_alias=AliasPath("data", "enableOptimizePaths"),
    )
    redundancy_groups: List[RedundancyGroups] = Field(
        validation_alias=AliasPath("data", "redundancyGroups"),
        description="Service VPN Id List",
    )
