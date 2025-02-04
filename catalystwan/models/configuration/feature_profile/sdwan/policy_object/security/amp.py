# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import (
    AmpFileAlertLevel,
    AmpFileAnalysisFileTypes,
    AmpFileAnalysisServer,
    AmpFileReputationServer,
)


class AdvancedMalwareProtectionParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["unified/advanced-malware-protection"] = Field(
        default="unified/advanced-malware-protection", exclude=True
    )
    description: str = "advancedMalwareProtection"
    match_all_vpn: Global[Literal[True]] = Field(
        default=Global[Literal[True]](value=True), validation_alias=AliasPath("data", "matchAllVpn")
    )
    file_reputation_cloud_server: Global[AmpFileReputationServer] = Field(
        validation_alias=AliasPath("data", "fileReputationCloudServer")
    )
    file_reputation_est_server: Global[AmpFileReputationServer] = Field(
        validation_alias=AliasPath("data", "fileReputationEstServer")
    )
    file_reputation_alert: Global[AmpFileAlertLevel] = Field(
        default=Global[AmpFileAlertLevel](value="critical"),
        validation_alias=AliasPath("data", "fileReputationAlert"),
    )
    file_analysis_enabled: Global[bool] = Field(
        default=Global[bool](value=False), validation_alias=AliasPath("data", "fileAnalysisEnabled")
    )
    file_analysis_cloud_server: Optional[Global[AmpFileAnalysisServer]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisCloudServer")
    )
    file_analysis_file_types: Optional[Global[List[AmpFileAnalysisFileTypes]]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisFileTypes")
    )
    file_analysis_alert: Optional[Global[AmpFileAlertLevel]] = Field(
        default=None, validation_alias=AliasPath("data", "fileAnalysisAlert")
    )

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        file_reputation_cloud_server: AmpFileReputationServer,
        file_reputation_est_server: AmpFileReputationServer,
        file_reputation_alert: AmpFileAlertLevel,
        file_analysis_enabled: bool = False,
        file_analysis_alert: Optional[AmpFileAlertLevel] = None,
        file_analysis_cloud_server: Optional[AmpFileAnalysisServer] = None,
        file_analysis_file_types: List[AmpFileAnalysisFileTypes] = [],
    ):
        _file_analysis_alert = Global[AmpFileAlertLevel](value=file_analysis_alert) if file_analysis_alert else None
        _file_analysis_cloud_server = (
            Global[AmpFileAnalysisServer](value=file_analysis_cloud_server) if file_analysis_cloud_server else None
        )
        _file_analysis_file_types = (
            Global[List[AmpFileAnalysisFileTypes]](value=file_analysis_file_types) if file_analysis_file_types else None
        )

        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            file_reputation_cloud_server=Global[AmpFileReputationServer](value=file_reputation_cloud_server),
            file_reputation_est_server=Global[AmpFileReputationServer](value=file_reputation_est_server),
            file_analysis_alert=_file_analysis_alert,
            file_analysis_cloud_server=_file_analysis_cloud_server,
            file_reputation_alert=Global[AmpFileAlertLevel](value=file_reputation_alert),
            file_analysis_enabled=Global[bool](value=file_analysis_enabled),
            file_analysis_file_types=_file_analysis_file_types,
        )
