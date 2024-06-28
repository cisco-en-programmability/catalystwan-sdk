# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Final, List

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.models.common import DeviceModel

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
    device_role: str = Field(default=None, alias="deviceRole")
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
