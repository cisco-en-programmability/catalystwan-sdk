# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class VPNQoSScheduler(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    child_map_ref: UUID = Field(validation_alias="childMapRef", serialization_alias="childMapRef")
    vpn_list_ref: Optional[UUID] = Field(default=None, validation_alias="vpnListRef", serialization_alias="vpnListRef")
    bandwidth_rate: Optional[IntStr] = Field(
        default=None, validation_alias="bandwidthRate", serialization_alias="bandwidthRate", ge=8, le=100_000_000
    )
    shaping_rate: Optional[IntStr] = Field(
        default=None, validation_alias="shapingRate", serialization_alias="shapingRate", ge=8, le=100_000_000
    )


class VPNQoSMapPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vpn_qos_schedulers: List[VPNQoSScheduler] = Field(
        validation_alias="vpnQosSchedulers", serialization_alias="vpnQosSchedulers"
    )


class VPNQoSMapPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["vpnQosMap", "vpnQoSMap"] = "vpnQosMap"
    definition: VPNQoSMapPolicyDefinition


class VPNQoSMapPolicyEditPayload(VPNQoSMapPolicy, PolicyDefinitionId):
    pass


class VPNQoSMapPolicyGetResponse(VPNQoSMapPolicy, PolicyDefinitionGetResponse):
    pass
