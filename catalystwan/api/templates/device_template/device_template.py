# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


TemplateType = Literal["file", "template"]  # file == cli, template == feature


def str_to_uuid(s: str) -> Optional[UUID]:
    try:
        return UUID(s)
    except ValueError:
        return None


class GeneralTemplate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str = Field(default="")

    sub_templates: List[GeneralTemplate] = Field(
        default=[], serialization_alias="subTemplates", validation_alias="subTemplates"
    )
    template_id: str = Field(default="", serialization_alias="templateId", validation_alias="templateId")
    template_type: str = Field(default="", serialization_alias="templateType", validation_alias="templateType")


class DeviceTemplate(BaseModel):
    """
    ## Example:

    >>> templates = [
            "default_system", # Cisco System
            "default_logging", # Cisco Logging
            "default_banner", # Banner
        ]
    >>> device_template = DeviceTemplate(
            template_name="python",
            template_description="python",
            general_templates=templates
        )
    >>> session.api.templates.create(device_template)
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    template_name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    template_description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")
    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    device_role: str = Field(default="sdwan-edge", serialization_alias="deviceRole", validation_alias="deviceRole")
    config_type: Optional[str] = Field(
        default="template", serialization_alias="configType", validation_alias="configType"
    )
    factory_default: Optional[bool] = Field(
        default=False, serialization_alias="factoryDefault", validation_alias="factoryDefault"
    )
    policy_id: str = Field(default="", serialization_alias="policyId", validation_alias="policyId")
    feature_template_uid_range: Optional[List] = Field(
        default=[], serialization_alias="featureTemplateUidRange", validation_alias="featureTemplateUidRange"
    )

    connection_preference_required: Optional[bool] = Field(
        default=True,
        serialization_alias="connectionPreferenceRequired",
        validation_alias="connectionPreferenceRequired",
    )
    connection_preference: Optional[bool] = Field(
        default=True, serialization_alias="connectionPreference", validation_alias="connectionPreference"
    )

    general_templates: List[GeneralTemplate] = Field(
        default=[], serialization_alias="generalTemplates", validation_alias="generalTemplates"
    )
    security_policy_id: str = Field(
        default="", serialization_alias="securityPolicyId", validation_alias="securityPolicyId"
    )
    voice_policy_id: Optional[str] = Field(
        default=None, serialization_alias="voicePolicyId", validation_alias="voicePolicyId"
    )
    template_configuration_edited: Optional[str] = Field(
        default=None, serialization_alias="templateConfigurationEdited", validation_alias="templateConfigurationEdited"
    )
    template_configuration: Optional[str] = Field(
        default=None, serialization_alias="templateConfiguration", validation_alias="templateConfiguration"
    )
    rid: Optional[int] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")
    cli_type: Optional[str] = Field(default=None, serialization_alias="cliType", validation_alias="cliType")
    copy_edited: Optional[bool] = Field(default=None, serialization_alias="copyEdited", validation_alias="copyEdited")

    def get_security_policy_uuid(self) -> Optional[UUID]:
        return str_to_uuid(self.security_policy_id)

    def get_policy_uuid(self) -> Optional[UUID]:
        return str_to_uuid(self.policy_id)

    def generate_payload(self) -> str:
        output = self.model_dump_json(by_alias=True)
        return output

    @field_validator("general_templates", mode="before")
    @classmethod
    def parse_templates(cls, value):
        output = []
        for template in value:
            if isinstance(template, str):
                output.append(GeneralTemplate(name=template))
            else:
                output.append(template)
        return output

    @classmethod
    def get(self, name: str, session: ManagerSession) -> DeviceTemplate:
        device_template = session.api.templates.get(DeviceTemplate).filter(name=name).single_or_default()
        resp = session.get(f"dataservice/template/device/object/{device_template.id}").json()
        return DeviceTemplate(**resp)

    def associate_feature_template(self, template_type: str, template_uuid: UUID) -> None:
        self.general_templates.append(
            GeneralTemplate(name="", template_id=str(template_uuid), template_type=template_type)
        )

    def associate_security_policy(self, security_policy_uuid: UUID) -> None:
        self.security_policy_id = str(security_policy_uuid)

    def associate_policy(self, policy_uuid: UUID) -> None:
        self.policy_id = str(policy_uuid)

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class DeviceSpecificValue(BaseModel):
    property: str


class DeviceTemplateConfigAttached(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    host_name: Optional[str] = Field(None, serialization_alias="host-name", validation_alias="host-name")
    device_ip: Optional[str] = Field(None, serialization_alias="deviceIP", validation_alias="deviceIP")
    local_system_ip: Optional[str] = Field(
        None, serialization_alias="local-system-ip", validation_alias="local-system-ip"
    )
    site_id: Optional[str] = Field(None, serialization_alias="site-id", validation_alias="site-id")
    device_groups: Optional[List[str]] = Field(
        None, serialization_alias="device-groups", validation_alias="device-groups"
    )
    uuid: Optional[str] = Field(None, serialization_alias="uuid", validation_alias="uuid")
    personality: Optional[str] = Field(None, serialization_alias="personality", validation_alias="personality")
    config_cloudx_mode: Optional[str] = Field(
        None, serialization_alias="configCloudxMode", validation_alias="configCloudxMode"
    )


class CreateDeviceInputPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    template_id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    device_ids: List[str] = Field(serialization_alias="deviceIds", validation_alias="deviceIds")
    is_edited: bool = Field(serialization_alias="isEdited", validation_alias="isEdited")
    is_master_edited: bool = Field(serialization_alias="isMasterEdited", validation_alias="isMasterEdited")


class DeviceInputValues(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    csv_device_ip: str = Field(validation_alias="csv-deviceIP", serialization_alias="csv-deviceIP")
    csv_device_id: str = Field(validation_alias="csv-deviceId", serialization_alias="csv-deviceId")
    csv_host_name: str = Field(validation_alias="csv-host-name", serialization_alias="csv-host-name")
    csv_status: str = Field(validation_alias="csv-status", serialization_alias="csv-status")

    @property
    def values(self) -> Dict[str, Any]:
        return self.__pydantic_extra__ or dict()
