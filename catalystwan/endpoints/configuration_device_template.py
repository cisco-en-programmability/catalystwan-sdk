# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Dict

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.templates.device_template.device_template import (
    CreateDeviceInputPayload,
    DeviceInputValues,
    DeviceTemplateConfigAttached,
)
from catalystwan.endpoints import APIEndpoints, get, post, view
from catalystwan.typed_list import DataSequence
from catalystwan.utils.session_type import ProviderView


class FeatureToCLIPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    device_specific_variables: Dict[str, str] = Field(alias="device")
    is_edited: bool = Field(alias="isEdited")
    is_master_edited: bool = Field(alias="isMasterEdited")
    is_RFS_required: bool = Field(alias="isRFSRequired")
    template_id: str = Field(alias="templateId")


class ConfigurationDeviceTemplate(APIEndpoints):
    @view({ProviderView})
    @post("/template/device/config/config/")
    def get_device_configuration_preview(self, payload: FeatureToCLIPayload) -> str:
        ...

    @get("/template/device/config/attached/{template_id}", resp_json_key="data")
    def get_device_config_attached(self, template_id: str) -> DataSequence[DeviceTemplateConfigAttached]:
        ...

    @post("/template/device/config/input/", resp_json_key="data")
    def create_device_input(self, payload: CreateDeviceInputPayload) -> DataSequence[DeviceInputValues]:
        ...
