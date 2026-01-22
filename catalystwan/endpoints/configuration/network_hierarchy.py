# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelCreationResponse
from catalystwan.models.configuration.network_hierarchy.cflowd import CflowdParcel
from catalystwan.models.configuration.network_hierarchy.node import NodeInfo
from catalystwan.models.configuration.network_hierarchy.security_logging import SecurityLoggingParcel
from catalystwan.typed_list import DataSequence


class NetworkHierarchy(APIEndpoints):
    @get("/v1/network-hierarchy")
    @versions(">=20.10")
    def list_nodes(self) -> DataSequence[NodeInfo]: ...

    @post("/v1/network-hierarchy/{node_id}/network-settings/cflowd")
    @versions(">20.12")
    def create_cflowd(self, node_id: UUID, payload: CflowdParcel) -> ParcelCreationResponse: ...

    @get("/v1/network-hierarchy/{node_id}/network-settings/cflowd", resp_json_key="data")
    @versions(">20.12")
    def get_cflowd(self, node_id: UUID) -> DataSequence[Parcel[CflowdParcel]]: ...

    @delete("/v1/network-hierarchy/{node_id}/network-settings/cflowd/{parcel_id}")
    @versions(">20.12")
    def delete_cflowd(self, node_id: UUID, parcel_id: UUID) -> None: ...

    @post("/v1/network-hierarchy/{node_id}/network-settings/security-logging")
    @versions(">20.12")
    def create_security_logging(self, node_id: UUID, payload: SecurityLoggingParcel) -> ParcelCreationResponse: ...

    @get("/v1/network-hierarchy/{node_id}/network-settings/security-logging", resp_json_key="data")
    @versions(">20.12")
    def get_security_logging(self, node_id: UUID) -> DataSequence[Parcel[SecurityLoggingParcel]]: ...

    @put("/v1/network-hierarchy/{node_id}/network-settings/security-logging/{parcel_id}")
    @versions(">20.12")
    def edit_security_logging(
        self, node_id: UUID, payload: SecurityLoggingParcel, parcel_id: UUID
    ) -> ParcelCreationResponse: ...

    @delete("/v1/network-hierarchy/{node_id}/network-settings/security-logging/{parcel_id}")
    @versions(">20.12")
    def delete_security_logging(self, node_id: UUID, parcel_id: UUID) -> None: ...
