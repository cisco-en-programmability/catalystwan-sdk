# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.media_profile import MediaProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_profile import TranslationProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_rule import TranslationRuleParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.trunk_group import TrunkGroupParcel

from .dsp_farm import DspFarmParcel

AnyUcVoiceParcel = Annotated[
    Union[DspFarmParcel, MediaProfileParcel, TrunkGroupParcel, TranslationRuleParcel, TranslationProfileParcel],
    Field(discriminator="type_"),
]

__all__ = (
    "AnyUcVoiceParcel",
    "DspFarmParcel",
    "MediaProfileParcel",
    "TrunkGroupParcel",
    "TranslationProfileParcel",
    "TranslationRuleParcel",
)


def __dir__() -> "List[str]":
    return list(__all__)
