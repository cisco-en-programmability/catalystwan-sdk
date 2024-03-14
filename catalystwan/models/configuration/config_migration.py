# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.api.templates.device_template.device_template import DeviceTemplate
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo, AnyPolicyListInfo
from catalystwan.models.policy.centralized import CentralizedPolicyInfo
from catalystwan.models.policy.localized import LocalizedPolicyInfo
from catalystwan.models.policy.security import AnySecurityPolicyInfo

AnyParcel = Annotated[
    Union[
        AnySystemParcel,
        AnyPolicyObjectParcel,
    ],
    Field(discriminator="type_"),
]


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    centralized_policies: List[CentralizedPolicyInfo] = Field(
        default=[], serialization_alias="centralizedPolicies", validation_alias="centralizedPolicies"
    )
    localized_policies: List[LocalizedPolicyInfo] = Field(
        default=[], serialization_alias="localizedPolicies", validation_alias="localizedPolicies"
    )
    security_policies: List[AnySecurityPolicyInfo] = Field(
        default=[], serialization_alias="securityPolicies", validation_alias="securityPolicies"
    )
    policy_definitions: List[AnyPolicyDefinitionInfo] = Field(
        default=[], serialization_alias="policyDefinitions", validation_alias="policyDefinitions"
    )
    policy_lists: List[AnyPolicyListInfo] = Field(
        default=[], serialization_alias="policyLists", validation_alias="policyLists"
    )


class UX1Templates(BaseModel):
    feature_templates: List[FeatureTemplateInformation] = Field(
        default=[], serialization_alias="featureTemplates", validation_alias="featureTemplates"
    )
    device_templates: List[DeviceTemplate] = Field(
        default=[], serialization_alias="deviceTemplates", validation_alias="deviceTemplates"
    )


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    topology_groups: List[TopologyGroup] = Field(
        default=[], serialization_alias="topologyGroups", validation_alias="topologyGroups"
    )
    config_groups: List[ConfigGroup] = Field(
        default=[], serialization_alias="configurationGroups", validation_alias="configurationGroups"
    )
    policy_groups: List[ConfigGroup] = Field(
        default=[], serialization_alias="policyGroups", validation_alias="policyGroups"
    )
    feature_profiles: List[FeatureProfileCreationPayload] = Field(
        default=[], serialization_alias="featureProfiles", validation_alias="featureProfiles"
    )
    profile_parcels: List[AnyParcel] = Field(
        default=[], serialization_alias="profileParcels", validation_alias="profileParcels"
    )
