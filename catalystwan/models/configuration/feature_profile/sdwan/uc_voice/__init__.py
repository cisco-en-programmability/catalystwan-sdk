# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.analog_interface import AnalogInterfaceParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.call_routing import CallRoutingParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.digital_interface import DigitalInterfaceParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.dsp_farm import DspFarmParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.media_profile import MediaProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.server_group import ServerGroupParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.srst import SrstParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.supervisory_disconnect import (
    SupervisoryDiconnectParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_profile import TranslationProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_rule import TranslationRuleParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.trunk_group import TrunkGroupParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.voice_global import VoiceGlobalParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.voice_tenant import VoiceTenantParcel

AnyUcVoiceParcel = Annotated[
    Union[
        AnalogInterfaceParcel,
        CallRoutingParcel,
        DigitalInterfaceParcel,
        DspFarmParcel,
        MediaProfileParcel,
        ServerGroupParcel,
        SrstParcel,
        SupervisoryDiconnectParcel,
        TranslationProfileParcel,
        TranslationRuleParcel,
        TrunkGroupParcel,
        VoiceGlobalParcel,
        VoiceTenantParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AnalogInterfaceParcel",
    "AnyUcVoiceParcel",
    "CallRoutingParcel",
    "DigitalInterfaceParcel",
    "DspFarmParcel",
    "MediaProfileParcel",
    "ServerGroupParcel",
    "SupervisoryDiconnectParcel",
    "SrstParcel",
    "TranslationProfileParcel",
    "TranslationRuleParcel",
    "TrunkGroupParcel",
    "VoiceGlobalParcel",
    "VoiceTenantParcel",
)


def __dir__() -> "List[str]":
    return list(__all__)
