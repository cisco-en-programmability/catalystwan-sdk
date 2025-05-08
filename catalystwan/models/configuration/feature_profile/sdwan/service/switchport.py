# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import Duplex, Speed


class StaticMacAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    mac_address: Union[Global[str], Variable] = Field(serialization_alias="macaddr", validation_alias="macaddr")
    vlan: Union[Global[int], Variable]
    interface_name: Optional[Union[Global[str], Variable]] = Field(
        serialization_alias="ifName", validation_alias="ifName", default=None
    )


SwitchportMode = Literal[
    "access",
    "trunk",
]


PortControl = Literal[
    "auto",
    "force-unauthorized",
    "force-authorized",
]

HostMode = Literal[
    "single-host",
    "multi-auth",
    "multi-host",
    "multi-domain",
]

ControlDirection = Literal[
    "both",
    "in",
]


class SwitchportInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface_name: Union[Global[str], Variable] = Field(serialization_alias="ifName", validation_alias="ifName")
    control_direction: Optional[Union[Global[ControlDirection], Default[None], Variable]] = Field(
        default=None, validation_alias="controlDirection", serialization_alias="controlDirection"
    )
    enable_dot1x: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="enableDot1x", serialization_alias="enableDot1x"
    )
    critical_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="criticalVlan", serialization_alias="criticalVlan"
    )
    duplex: Optional[Union[Global[Duplex], Default[None], Variable]] = Field(default=None)
    enable_periodic_reauth: Optional[Union[Variable, Default[None], Global[bool]]] = Field(
        default=None, validation_alias="enablePeriodicReauth", serialization_alias="enablePeriodicReauth"
    )
    enable_voice: Optional[Union[Variable, Default[None], Global[bool]]] = Field(
        default=None, validation_alias="enableVoice", serialization_alias="enableVoice"
    )
    guest_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="guestVlan", serialization_alias="guestVlan"
    )
    host_mode: Optional[Union[Global[HostMode], Default[None], Variable]] = Field(
        default=None, validation_alias="hostMode", serialization_alias="hostMode"
    )
    inactivity: Optional[Union[Global[int], Default[None], Variable]] = Field(default=None)
    mac_authentication_bypass: Optional[Union[Variable, Default[None], Global[bool]]] = Field(
        default=None, validation_alias="macAuthenticationBypass", serialization_alias="macAuthenticationBypass"
    )
    mode: Optional[Global[SwitchportMode]] = Field(default=None)
    pae_enable: Optional[Union[Variable, Default[None], Global[bool]]] = Field(
        default=None, validation_alias="paeEnable", serialization_alias="paeEnable"
    )
    port_control: Optional[Union[Global[PortControl], Default[None], Variable]] = Field(
        default=None, validation_alias="portControl", serialization_alias="portControl"
    )
    reauthentication: Optional[Union[Default[int], Global[int], Variable]] = Field(default=None)
    restricted_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="restrictedVlan", serialization_alias="restrictedVlan"
    )
    shutdown: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(default=None)
    speed: Optional[Union[Global[Speed], Default[None], Variable]] = Field(default=None)
    switchport_access_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="switchportAccessVlan", serialization_alias="switchportAccessVlan"
    )
    switchport_trunk_allowed_vlans: Optional[Union[Global[str], Default[None], Variable]] = Field(
        default=None, validation_alias="switchportTrunkAllowedVlans", serialization_alias="switchportTrunkAllowedVlans"
    )
    switchport_trunk_native_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="switchportTrunkNativeVlan", serialization_alias="switchportTrunkNativeVlan"
    )
    voice_vlan: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="voiceVlan", serialization_alias="voiceVlan"
    )


class SwitchportParcel(_ParcelBase):
    type_: Literal["switchport"] = Field(default="switchport", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    interface: List[SwitchportInterface] = Field(default_factory=list, validation_alias=AliasPath("data", "interface"))
    age_time: Union[Global[int], Variable, Default[int]] = Field(
        default=Default[int](value=300), validation_alias=AliasPath("data", "ageTime")
    )
    static_mac_address: List[StaticMacAddress] = Field(
        default_factory=list, validation_alias=AliasPath("data", "staticMacAddress")
    )
