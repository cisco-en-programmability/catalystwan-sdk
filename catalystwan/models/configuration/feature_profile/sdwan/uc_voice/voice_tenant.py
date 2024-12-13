# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

BindInterface = Literal[
    "Both",
    "Control",
    "Disabled",
    "Media",
]


TransportType = Literal[
    "TCP",
    "TCP TLS",
    "UDP",
]


class VoiceTenantParcel(_ParcelBase):
    type_: Literal["voice-tenant"] = Field(default="voice-tenant", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    bind_interface: Union[Variable, Global[BindInterface], Default[Literal["Disabled"]]] = Field(
        validation_alias=AliasPath("data", "bindInterface")
    )
    transport_type: Union[Variable, Global[TransportType], Default[Literal["UDP"]]] = Field(
        validation_alias=AliasPath("data", "transportType")
    )
    voice_tenant_tag: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "voiceTenantTag"))
    bind_control_interface_name: Optional[Union[Variable, Global[str]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "bindControlInterfaceName"),
    )
    bind_media_interface_name: Optional[Union[Variable, Global[str]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "bindMediaInterfaceName"),
    )
