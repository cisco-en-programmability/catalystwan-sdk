# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

VoiceType = Literal[
    "pots",
    "sip",
]

TranslationRuleDirection = Literal[
    "incoming",
    "outgoing",
]

FwdDigitChoice = Literal[
    "all",
    "none",
    "some",
]

TransportChoice = Literal[
    "tcp",
    "udp",
]


class Voice(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dialpeertag: Union[Variable, Global[int]] = Field()
    call_type: Optional[Global[TranslationRuleDirection]] = Field(
        default=None, validation_alias="callType", serialization_alias="callType"
    )
    description: Optional[Union[Variable, Default[None], Global[str]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "description"),
    )
    destination_address: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias="destinationAddress", serialization_alias="destinationAddress"
    )
    fwd_digit_choice: Optional[Union[Variable, Global[FwdDigitChoice]]] = Field(
        default=None, validation_alias="fwdDigitChoice", serialization_alias="fwdDigitChoice"
    )
    num_digits: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="numDigits", serialization_alias="numDigits"
    )
    number_pattern: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias="numberPattern", serialization_alias="numberPattern"
    )
    port: Optional[Union[Variable, Global[str]]] = Field(default=None)
    preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)
    prefix: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)
    transport_choice: Optional[Union[Variable, Global[TransportChoice], Default[None]]] = Field(
        default=None, validation_alias="transportChoice", serialization_alias="transportChoice"
    )
    type: Optional[Global[VoiceType]] = Field(default=None)


Fallback = Literal[
    "G.711alaw",
    "G.711ulaw",
    "None",
]


class ModemPassThrough(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dial_peer_range: Union[Variable, Global[str]] = Field(
        validation_alias="dialPeerRange", serialization_alias="dialPeerRange"
    )
    protocol: Union[Variable, Global[Fallback]] = Field()


Primary = Literal[
    "Fax Pass-through G711alaw",
    "Fax Pass-through G711alaw No ECM",
    "Fax Pass-through G711ulaw",
    "Fax Pass-through G711ulaw No ECM",
    "None",
    "T.38 Fax Relay Version 0",
    "T.38 Fax Relay Version 0 NSE",
    "T.38 Fax Relay Version 0 NSE No ECM",
    "T.38 Fax Relay Version 0 NSE Rate 14.4",
    "T.38 Fax Relay Version 0 NSE Rate 14.4 No ECM",
    "T.38 Fax Relay Version 0 NSE Rate 9.6",
    "T.38 Fax Relay Version 0 NSE Rate 9.6 No ECM",
    "T.38 Fax Relay Version 0 NSE force",
    "T.38 Fax Relay Version 0 NSE force No ECM",
    "T.38 Fax Relay Version 0 NSE force Rate 14.4",
    "T.38 Fax Relay Version 0 NSE force Rate 14.4 No ECM",
    "T.38 Fax Relay Version 0 NSE force Rate 9.6",
    "T.38 Fax Relay Version 0 NSE force Rate 9.6 No ECM",
    "T.38 Fax Relay Version 0 No ECM",
    "T.38 Fax Relay Version 0 Rate 14.4",
    "T.38 Fax Relay Version 0 Rate 14.4 No ECM",
    "T.38 Fax Relay Version 0 Rate 9.6 No ECM",
    "T.38 Fax Relay Version 3",
    "T.38 Fax Relay Version 3 NSE",
    "T.38 Fax Relay Version 3 NSE force",
]


class FaxProtocol(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dial_peer_range: Union[Variable, Global[str]] = Field(
        validation_alias="dialPeerRange", serialization_alias="dialPeerRange"
    )
    primary: Union[Variable, Global[Primary]] = Field()
    fallback: Optional[Union[Variable, Global[Fallback]]] = Field(default=None)
    high_speed: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="highSpeed", serialization_alias="highSpeed"
    )
    low_speed: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="lowSpeed", serialization_alias="lowSpeed"
    )


class Association(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dial_peer_range: Union[Variable, Global[str]] = Field(
        validation_alias="dialPeerRange", serialization_alias="dialPeerRange"
    )
    media_profile: Optional[RefIdItem] = Field(
        default=None, validation_alias="mediaProfile", serialization_alias="mediaProfile"
    )
    server_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="serverGroup", serialization_alias="serverGroup"
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
    voice_tenant: Optional[RefIdItem] = Field(
        default=None, validation_alias="voiceTenant", serialization_alias="voiceTenant"
    )


class CallRoutingParcel(_ParcelBase):
    type_: Literal["call-routing"] = Field(default="call-routing", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    association: Optional[List[Association]] = Field(
        default=None,
        validation_alias=AliasPath("data", "association"),
        description="Association",
    )
    dial_peer_tag_prefix: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "dialPeerTagPrefix"),
    )
    fax_protocol: Optional[List[FaxProtocol]] = Field(
        default=None,
        validation_alias=AliasPath("data", "faxProtocol"),
        description="Configure fax protocol",
    )
    modem_pass_through: Optional[List[ModemPassThrough]] = Field(
        default=None,
        validation_alias=AliasPath("data", "modemPassThrough"),
        description="Configure of Modem Pass-Through",
    )
    port_module_location: Optional[RefIdItem] = Field(
        default=None,
        validation_alias=AliasPath("data", "portModuleLocation"),
    )
    voice: Optional[List[Voice]] = Field(
        default=None,
        validation_alias=AliasPath("data", "voice"),
        description="POTS/Voip voice type",
    )
