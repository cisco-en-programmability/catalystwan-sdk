# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

SlotId = Literal[
    "0/1",
    "0/2",
    "0/3",
    "1/0",
    "1/1",
    "2/0",
    "2/1",
    "3/0",
]

ModuleType = Literal[
    "12 Port FXO",
    "16 Port FXS",
    "2 Port FXO",
    "2 Port FXS",
    "24 Port FXS",
    "4 Port FXO",
    "4 Port FXS",
    "72 Port FXS",
    "8 Port FXS",
]

SignalChoice = Literal[
    "DID",
    "GroundStart",
    "LoopStart",
]


DidType = Literal[
    "Delay dial",
    "Immediate",
    "Wink start",
]


class VoiceCardBasic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    shutdown: Union[Variable, Default[bool], Global[bool]] = Field()
    signal_choice: Union[Variable, Global[SignalChoice], Default[Literal["loopStart"]]] = Field(
        validation_alias="signalChoice", serialization_alias="signalChoice"
    )
    description: Optional[Union[Variable, Default[None], Global[str]]] = Field(default=None)
    did_type: Optional[Union[Variable, Default[None], Global[DidType]]] = Field(
        default=None, validation_alias="didType", serialization_alias="didType"
    )


class VoiceCardStationID(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    station_name: Union[Variable, Global[str]] = Field(
        validation_alias="stationName", serialization_alias="stationName"
    )
    station_number: Union[Variable, Global[str]] = Field(
        validation_alias="stationNumber", serialization_alias="stationNumber"
    )


CompandType = Literal[
    "A-law",
    "U-law",
]


Impedance = Literal[
    "600c",
    "600r",
    "900c",
    "900r",
    "complex1",
    "complex2",
    "complex3",
    "complex4",
    "complex5",
    "complex6",
]


CallProgressTone = Literal[
    "Argentina",
    "Australia",
    "Austria",
    "Belgium",
    "Brazil",
    "Canada",
    "Chile",
    "China",
    "Columbia",
    "Custom 1",
    "Custom 2",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Egypt",
    "Finland",
    "France",
    "Germany",
    "Ghana",
    "Greece",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "Jordan",
    "Kenya",
    "Korea Republic",
    "Kuwait",
    "Lebanon",
    "Luxembourg",
    "Malaysia",
    "Malta",
    "Mexico",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Oman",
    "Pakistan",
    "Panama",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Russian Federation",
    "Saudi Arabia",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "Spain",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "Turkey",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Venezuela",
    "Zimbabwe",
]


class LineParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    attenuation: Union[Variable, Default[int], Global[int]] = Field()
    call_progress_tone: Union[Variable, Global[CallProgressTone]] = Field(
        validation_alias="callProgressTone", serialization_alias="callProgressTone"
    )
    compand_type: Union[Variable, Global[CompandType], Default[Literal["U-law"]]] = Field(
        validation_alias="compandType", serialization_alias="compandType"
    )
    echo_canceller: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias="echoCanceller", serialization_alias="echoCanceller"
    )
    gain: Union[Variable, Default[int], Global[int]] = Field()
    impedance: Union[Global[Impedance], Default[Literal["600r"]], Variable] = Field()
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    voice_activity_detection: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias="voiceActivityDetection", serialization_alias="voiceActivityDetection"
    )


SupervisoryDisconnect = Literal[
    "Anytone",
    "Dualtone",
    "signal",
]


SupervisoryDisconnectDualtone = Literal[
    "Mid call",
    "Pre Connect",
]

DialType = Literal[
    "dtmf",
    "mf",
    "pulse",
]


DetectionDelayBatteryReversal = Literal[
    "Answer",
    "Both",
    "Detection Delay",
]


class TuningParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    detection_delay: Union[Variable, Global[int]] = Field(
        validation_alias="detectionDelay", serialization_alias="detectionDelay"
    )
    detection_delay_battery_reversal: Union[Variable, Global[DetectionDelayBatteryReversal]] = Field(
        validation_alias="detectionDelayBatteryReversal", serialization_alias="detectionDelayBatteryReversal"
    )
    dial_delay: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="dialDelay", serialization_alias="dialDelay"
    )
    dial_type: Union[Global[DialType], Variable, Default[Literal["dtmf"]]] = Field(
        validation_alias="dialType", serialization_alias="dialType"
    )
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    supervisory_disconnect: Union[Global[SupervisoryDisconnect], Default[Literal["signal"]], Variable] = Field(
        validation_alias="supervisoryDisconnect", serialization_alias="supervisoryDisconnect"
    )
    timing_guard_out: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="timingGuardOut", serialization_alias="timingGuardOut"
    )
    timing_hookflash_out: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="timingHookflashOut", serialization_alias="timingHookflashOut"
    )
    timing_sup_disconnect: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="timingSupDisconnect", serialization_alias="timingSupDisconnect"
    )
    supervisory_disconnect_dualtone: Optional[Union[Variable, Global[SupervisoryDisconnectDualtone]]] = Field(
        default=None,
        validation_alias="supervisoryDisconnectDualtone",
        serialization_alias="supervisoryDisconnectDualtone",
    )


LoopLength = Literal[
    "Long",
    "Short",
]


DcOffSet = Literal[
    "10-volts",
    "20-volts",
    "24-volts",
    "30-volts",
    "35-volts",
]


class TuningParamsFxs(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    loop_length: Union[Variable, Global[LoopLength], Default[Literal["Short"]]] = Field(
        validation_alias="loopLength", serialization_alias="loopLength"
    )
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    pulse_digit_detection: Union[Variable, Default[bool], Global[bool]] = Field(
        validation_alias="pulseDigitDetection", serialization_alias="pulseDigitDetection"
    )
    ren: Union[Variable, Global[int]] = Field()
    ring: Union[Variable, Default[int], Global[int]] = Field()
    timing_hookflash_in: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="timingHookflashIn", serialization_alias="timingHookflashIn"
    )
    dc_off_set: Optional[Union[Variable, Global[DcOffSet]]] = Field(
        default=None, validation_alias="dcOffSet", serialization_alias="dcOffSet"
    )
    timing_hookflash_out_sup: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="timingHookflashOutSup", serialization_alias="timingHookflashOutSup"
    )


CallerMode = Literal[
    "BT",
    "DTMF",
    "FSK",
]

DtmfModeSelectionEnd = Literal[
    "#",
    "*",
    "A",
    "B",
    "C",
    "D",
]

AlertOptions = Literal[
    "Line-Reversal",
    "Pre-ring",
    "Ring 1",
    "Ring 2",
    "Ring 3",
    "Ring 4",
]


class CallerId(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    alert_options: Optional[Union[Global[AlertOptions], Variable, Default[None]]] = Field(
        default=None, validation_alias="alertOptions", serialization_alias="alertOptions"
    )
    caller_dsp_pre_allocate: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="callerDspPreAllocate", serialization_alias="callerDspPreAllocate"
    )
    caller_id_block: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="callerIdBlock", serialization_alias="callerIdBlock"
    )
    caller_id_format: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="callerIdFormat", serialization_alias="callerIdFormat"
    )
    caller_mode: Optional[Union[Variable, Global[CallerMode], Default[None]]] = Field(
        default=None, validation_alias="callerMode", serialization_alias="callerMode"
    )
    dtmf_codes: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias="dtmfCodes", serialization_alias="dtmfCodes"
    )
    dtmf_mode_selection_end: Optional[Union[Variable, Global[DtmfModeSelectionEnd], Default[None]]] = Field(
        default=None, validation_alias="dtmfModeSelectionEnd", serialization_alias="dtmfModeSelectionEnd"
    )
    dtmf_mode_selection_start: Optional[Union[Variable, Global[DtmfModeSelectionEnd], Default[None]]] = Field(
        default=None, validation_alias="dtmfModeSelectionStart", serialization_alias="dtmfModeSelectionStart"
    )
    enable: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(default=None)


class DidTimer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    answer_winkwidth: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="answerWinkwidth", serialization_alias="answerWinkwidth"
    )
    clear_wait: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="clearWait", serialization_alias="clearWait"
    )
    dial_pulse_min_delay: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="dialPulseMinDelay", serialization_alias="dialPulseMinDelay"
    )
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    wait_before_wink: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="waitBeforeWink", serialization_alias="waitBeforeWink"
    )
    wink_duration: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="winkDuration", serialization_alias="winkDuration"
    )


class ConnectionPlar(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    connection_plar: Union[Variable, Global[str]] = Field(
        validation_alias="connectionPlar", serialization_alias="connectionPlar"
    )
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    connection_plar_opx: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias="connectionPlarOpx", serialization_alias="connectionPlarOpx"
    )


TranslationRuleDirection = Literal[
    "incoming",
    "outgoing",
]


class Association(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_range: Union[Variable, Global[str]] = Field(validation_alias="portRange", serialization_alias="portRange")
    supervisory_disconnect: Optional[RefIdItem] = Field(
        default=None, validation_alias="supervisoryDisconnect", serialization_alias="supervisoryDisconnect"
    )
    translation_profile: Optional[RefIdItem] = Field(
        default=None, validation_alias="translationProfile", serialization_alias="translationProfile"
    )
    translation_rule_direction: Optional[Union[Variable, Global[TranslationRuleDirection], Default[None]]] = Field(
        default=None, validation_alias="translationRuleDirection", serialization_alias="translationRuleDirection"
    )
    trunk_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="trunkGroup", serialization_alias="trunkGroup"
    )
    trunk_group_priority: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="trunkGroupPriority", serialization_alias="trunkGroupPriority"
    )


class AnalogInterfaceParcel(_ParcelBase):
    type_: Literal["analog-interface"] = Field(default="analog-interface", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    enable: Union[Variable, Default[bool], Global[bool]] = Field(validation_alias=AliasPath("data", "enable"))
    slot_id: Union[Variable, Global[SlotId]] = Field(validation_alias=AliasPath("data", "slotId"))
    association: Optional[List[Association]] = Field(
        default=None,
        validation_alias=AliasPath("data", "association"),
        description="Association",
    )
    caller_id: Optional[List[CallerId]] = Field(default=None, validation_alias=AliasPath("data", "callerId"))
    connection_plar: List[ConnectionPlar] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "connectionPlar"),
        description="Connection plar",
    )
    did_timer: List[DidTimer] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "didTimer"),
        description="DID timer",
    )
    line_params: List[LineParams] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "lineParams"),
        description="Configure of voice card station Id",
    )
    module_type: Global[ModuleType] = Field(validation_alias=AliasPath("data", "moduleType"))
    tuning_params: List[TuningParams] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "tuningParams"),
        description="Configure of voice card station Id",
    )
    tuning_params_fxs: List[TuningParamsFxs] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "tuningParamsFxs"),
        description="Configure of voice card station Id",
    )
    voice_card_basic: List[VoiceCardBasic] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "voiceCardBasic"),
        description="Configure of voice card",
    )
    voice_card_station_i_d: List[VoiceCardStationID] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "voiceCardStationID"),
        description="Configure of voice card station Id",
    )
