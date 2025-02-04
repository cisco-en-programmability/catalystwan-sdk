# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import (
    AmpFileAlertLevel,
    AmpFileAnalysisFileTypes,
    AmpFileAnalysisServer,
    AmpFileReputationServer,
    PolicyModeType,
    VpnId,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)

OptionalAmpFileAnalysisServer = Literal["", AmpFileAnalysisServer]
OptionalAmpFileAlertLevel = Literal["", AmpFileAlertLevel]


class AdvancedMalwareProtectionDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    match_all_vpn: bool = Field(validation_alias="matchAllVpn", serialization_alias="matchAllVpn")
    file_reputation_cloud_server: AmpFileReputationServer = Field(
        validation_alias="fileReputationCloudServer", serialization_alias="fileReputationCloudServer"
    )
    file_reputation_est_server: AmpFileReputationServer = Field(
        validation_alias="fileReputationEstServer", serialization_alias="fileReputationEstServer"
    )
    file_reputation_alert: AmpFileAlertLevel = Field(
        validation_alias="fileReputationAlert", serialization_alias="fileReputationAlert"
    )
    file_analysis_enabled: Optional[bool] = Field(
        default=False, validation_alias="fileAnalysisEnabled", serialization_alias="fileAnalysisEnabled"
    )
    file_analysis_file_types: List[AmpFileAnalysisFileTypes] = Field(
        default_factory=list, validation_alias="fileAnalysisFileTypes", serialization_alias="fileAnalysisFileTypes"
    )
    file_analysis_alert: OptionalAmpFileAlertLevel = Field(
        default="", validation_alias="fileAnalysisAlert", serialization_alias="fileAnalysisAlert"
    )
    file_analysis_cloud_server: OptionalAmpFileAnalysisServer = Field(
        default="", validation_alias="fileAnalysisCloudServer", serialization_alias="fileAnalysisCloudServer"
    )
    target_vpns: List[VpnId] = Field(
        default_factory=list, validation_alias="targetVpns", serialization_alias="targetVpns"
    )


class AdvancedMalwareProtectionPolicy(PolicyDefinitionBase):
    type: Literal["advancedMalwareProtection"] = "advancedMalwareProtection"
    mode: PolicyModeType = "security"
    definition: AdvancedMalwareProtectionDefinition


class AdvancedMalwareProtectionPolicyEditPayload(AdvancedMalwareProtectionPolicy, PolicyDefinitionId):
    pass


class AdvancedMalwareProtectionPolicyGetResponse(AdvancedMalwareProtectionPolicy, PolicyDefinitionGetResponse):
    pass
