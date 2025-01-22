# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional
from uuid import UUID

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.utils.device_model import DeviceModel

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class GeneralTemplate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = ""
    subTemplates: List[GeneralTemplate] = []

    templateId: str = ""
    templateType: str = ""


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

    template_name: str = Field(alias="templateName")
    template_description: str = Field(alias="templateDescription")
    general_templates: List[GeneralTemplate] = Field(alias="generalTemplates")
    device_role: str = Field(default="sdwan-edge", alias="deviceRole")
    device_type: DeviceModel = Field(alias="deviceType")
    security_policy_id: str = Field(default="", alias="securityPolicyId")
    policy_id: str = Field(default="", alias="policyId")

    def generate_payload(self) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        template = env.get_template(self.payload_path.name)
        output = template.render(self.model_dump())

        ast = env.parse(output)
        if meta.find_undeclared_variables(ast):
            logger.info(meta.find_undeclared_variables(ast))
            raise Exception("There are undeclared variables.")
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

    payload_path: Final[Path] = Path(__file__).parent / "device_template_payload.json.j2"

    @classmethod
    def get(self, name: str, session: ManagerSession) -> DeviceTemplate:
        device_template = session.api.templates.get(DeviceTemplate).filter(name=name).single_or_default()
        resp = session.get(f"dataservice/template/device/object/{device_template.id}").json()
        return DeviceTemplate(**resp)

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
