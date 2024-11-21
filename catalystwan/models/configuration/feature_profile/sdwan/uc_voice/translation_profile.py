# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

CallType = Literal[
    "called",
    "calling",
]


class TranslationProfileSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    call_type: Union[Variable, Global[CallType]] = Field(validation_alias="callType", serialization_alias="callType")
    translation_rule: Optional[RefIdItem] = Field(
        default=None, validation_alias="translationRule", serialization_alias="translationRule"
    )


class TranslationProfileParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["translation-profile"] = Field(default="translation-profile", exclude=True)
    translation_profile_settings: List[TranslationProfileSettings] = Field(
        validation_alias=AliasPath("data", "translationProfileSettings"),
        description="Translation Profile configuration",
    )
