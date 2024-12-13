# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

VoiceInterfaceTemplates = Literal[
    "1 Port E1",
    "1 Port T1",
    "2 Port E1",
    "2 Port T1",
    "4 Port E1",
    "4 Port T1",
    "8 Port E1",
    "8 Port T1",
]

ModuleLocation = Literal[
    "0/1",
    "0/2",
    "0/3",
    "1/0",
    "2/0",
]

ClockType = Literal[
    "line",
    "network",
    "primary",
    "secondary",
]


class Interface(BaseModel):
    port_id: Union[Variable, Global[int], Default[None]] = Field(
        validation_alias="portId", serialization_alias="portId"
    )
    clock_type: Optional[Union[Variable, Default[None], Global[ClockType]]] = Field(
        default=None, validation_alias="clockType", serialization_alias="clockType"
    )


Framing = Literal[
    "crc4",
    "no-crc4",
    "crc4",
    "esf",
    "sf",
]


LineCode = Literal[
    "ami",
    "b8zs",
    "hdb3",
]


CableLengthType = Literal[
    "long",
    "short",
]


Value = Literal[
    "-15",
    "-22.5",
    "-7.5",
    "0",
]

CableLengthValue = Literal[
    "110",
    "220",
    "330",
    "440",
    "550",
    "660",
]


LineTermination = Literal[
    "120-ohm",
    "75-ohm",
]


SwitchType = Literal[
    "primary-4ess",
    "primary-5ess",
    "primary-dms100",
    "primary-net5",
    "primary-ni",
    "primary-ntt",
    "primary-qsig",
]


class BasicSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    delay_connect_timer: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="delayConnectTimer", serialization_alias="delayConnectTimer"
    )
    framing: Union[Variable, Global[Framing], Default[Framing]] = Field()
    line_code: Union[Variable, Default[LineCode], Global[LineCode]] = Field(
        validation_alias="lineCode", serialization_alias="lineCode"
    )
    network_side: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias="networkSide", serialization_alias="networkSide"
    )
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    switch_type: Union[Variable, Global[SwitchType], Default[SwitchType]] = Field(
        validation_alias="switchType", serialization_alias="switchType"
    )
    cable_length: Optional[Union[Variable, Default[Literal["0"]], Global[CableLengthValue]]] = Field(
        default=None, validation_alias="cableLength", serialization_alias="cableLength"
    )
    cable_length_type: Optional[Union[Variable, Default[Literal["long"]], Global[CableLengthType]]] = Field(
        default=None, validation_alias="cableLengthType", serialization_alias="cableLengthType"
    )
    framing_australia: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="framingAustralia", serialization_alias="framingAustralia"
    )
    line_termination: Optional[Union[Variable, Default[Literal["120-ohm"]], Global[LineTermination]]] = Field(
        default=None, validation_alias="lineTermination", serialization_alias="lineTermination"
    )
    timeslots: Optional[Global[str]] = Field(default=None)


TypeAndTimerType = Literal[
    "T200",
    "T203",
    "T301",
    "T303",
    "T306",
    "T309",
    "T310",
    "T321",
]


class TypeAndTimer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    timer: Union[Variable, Global[int]] = Field()
    type: Union[Variable, Global[TypeAndTimerType]] = Field()


class IsdnTimer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias="portRange", serialization_alias="portRange"
    )
    type_and_timer: Optional[List[TypeAndTimer]] = Field(
        default=None,
        validation_alias="typeAndTimer",
        serialization_alias="typeAndTimer",
        description="list of ISDN Type and Timers",
    )


Plan = Literal[
    "data",
    "isdn",
    "national",
    "privacy",
    "reserved/10",
    "reserved/11",
    "reserved/12",
    "reserved/13",
    "reserved/14",
    "reserved/2",
    "reserved/5",
    "reserved/6",
    "reserved/7",
    "telex",
    "unknown",
]

IsdnMapType = Literal[
    "abbreviated",
    "international",
    "national",
    "reserved/5",
    "subscriber",
    "unknown",
]


class IsdnMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    digit_range: Union[Variable, Global[str]] = Field(validation_alias="digitRange", serialization_alias="digitRange")
    plan: Union[Variable, Default[None], Global[Plan]] = Field()
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    type: Union[Variable, Default[None], Global[IsdnMapType]] = Field()


class Shutdown(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    controller: Union[Variable, Default[bool], Global[bool]] = Field()
    port_id: Union[Variable, Global[int], Default[None]] = Field(
        validation_alias="portId", serialization_alias="portId"
    )
    serial: Union[Variable, Default[bool], Global[bool]] = Field()
    voice_port: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias="voicePort", serialization_alias="voicePort"
    )


CompandType = Literal[
    "a-law",
    "u-law",
]


class LineParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    attenuation: Optional[Union[Variable, Default[int], Global[int]]] = Field(default=None)
    call_progress_tone: Optional[Union[Variable, Global[None], Default[None]]] = Field(
        default=None, validation_alias="callProgressTone", serialization_alias="callProgressTone"
    )
    compand_type: Optional[Union[Variable, Default[CompandType], Global[CompandType]]] = Field(
        default=None, validation_alias="compandType", serialization_alias="compandType"
    )
    echo_canceller: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="echoCanceller", serialization_alias="echoCanceller"
    )
    gain: Optional[Union[Variable, Default[int], Global[int]]] = Field(default=None)
    voice_activity_detection: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="voiceActivityDetection", serialization_alias="voiceActivityDetection"
    )


OutgoingIeType = Literal[
    "called-number",
    "called-subaddr",
    "caller-number",
    "caller-subaddr",
    "connected-number",
    "connected-subaddr",
    "display",
    "extended-facility",
    "facility",
    "high-layer-compat",
    "low-layer-compat",
    "network-facility",
    "notify-indicator",
    "progress-indicator",
    "redirecting-number",
    "user-user",
]


class OutgoingIe(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    type: Union[Variable, Global[List[OutgoingIeType]]] = Field()


TranslationProfileDirection = Literal[
    "incoming",
    "outgoing",
]


class Association(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    translation_profile: Optional[RefIdItem] = Field(
        default=None, validation_alias="translationProfile", serialization_alias="translationProfile"
    )
    translation_profile_direction: Optional[
        Union[Variable, Default[None], Global[TranslationProfileDirection]]
    ] = Field(
        default=None, validation_alias="translationProfileDirection", serialization_alias="translationProfileDirection"
    )
    trunk_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="trunkGroup", serialization_alias="trunkGroup"
    )
    trunk_group_priority: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="trunkGroupPriority", serialization_alias="trunkGroupPriority"
    )


class DigitalInterfaceParcel(_ParcelBase):
    type_: Literal["digital-interface"] = Field(default="digital-interface", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    basic_settings: List[BasicSettings] = Field(
        validation_alias=AliasPath("data", "basicSettings"), description="add basic setting"
    )
    dsp_hairpin: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias=AliasPath("data", "dspHairpin"),
    )
    interface: List[Interface] = Field(
        validation_alias=AliasPath("data", "interface"), description="Configure Digital voice card interface"
    )
    isdn_timer: List[IsdnTimer] = Field(
        validation_alias=AliasPath("data", "isdnTimer"), description="list of ISDN Timers"
    )
    module_location: Union[Variable, Global[ModuleLocation]] = Field(
        validation_alias=AliasPath("data", "moduleLocation")
    )
    shutdown: List[Shutdown] = Field(
        validation_alias=AliasPath("data", "shutdown"), description="list of shutdown options"
    )
    association: Optional[List[Association]] = Field(
        default=None,
        validation_alias=AliasPath("data", "associations"),
        description="Select Trunk Group and Translation Profile associations",
    )
    isdn_map: Optional[List[IsdnMap]] = Field(
        default=None, validation_alias=AliasPath("data", "isdnMap"), description="list of ISDN map"
    )
    line_params: Optional[List[LineParams]] = Field(
        default=None, validation_alias=AliasPath("data", "lineParams"), description="list of line parameters"
    )
    outgoing_ie: Optional[List[OutgoingIe]] = Field(
        default=None, validation_alias=AliasPath("data", "outgoingIe"), description="list of outgoing IEs and messages"
    )
    voice_interface_templates: Optional[Global[VoiceInterfaceTemplates]] = Field(
        default=None, validation_alias="voiceInterfaceTemplates"
    )
