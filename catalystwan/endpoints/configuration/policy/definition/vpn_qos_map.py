# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.vpn_qos_map import (
    VPNQoSMapPolicy,
    VPNQoSMapPolicyEditPayload,
    VPNQoSMapPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyVPNQoSMapDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/vpnqosmap")
    def create_policy_definition(self, payload: VPNQoSMapPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/vpnqosmap/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/vpnqosmap/{id}")
    def edit_policy_definition(self, id: UUID, payload: VPNQoSMapPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/vpnqosmap", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/vpnqosmap/{id}")
    def get_policy_definition(self, id: UUID) -> VPNQoSMapPolicyGetResponse:
        ...

    @post("/template/policy/definition/vpnqosmap/preview")
    def preview_policy_definition(self, payload: VPNQoSMapPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/vpnqosmap/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
