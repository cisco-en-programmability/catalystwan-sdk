# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class Pool(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_oripv6prefix: Union[Variable, Global[str]] = Field(
        validation_alias="ipv4Oripv6prefix", serialization_alias="ipv4Oripv6prefix"
    )
    pool_tag: Union[Variable, Global[int]] = Field(validation_alias="poolTag", serialization_alias="poolTag")


CallFowardAction = Literal[
    "all",
    "busy",
    "noan",
]


class CallForward(BaseModel):
    action: Union[Variable, Global[CallFowardAction]] = Field()
    digit_string: Union[Variable, Global[str]] = Field(
        validation_alias="digitString", serialization_alias="digitString"
    )
    phone_profile: Union[Variable, Global[int]] = Field(
        validation_alias="phoneProfile", serialization_alias="phoneProfile"
    )
    timeout: Optional[Union[Variable, Default[int], Global[int]]] = Field(default=None)


class TranslationProfile(BaseModel):
    ref_id: Union[Default[None], Global[str]] = Field(validation_alias="refId", serialization_alias="refId")


TranslationProfileDirection = Literal[
    "incoming",
    "outgoing",
]


class TranslationAndMediaProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    media_profile: Optional[RefIdItem] = Field(
        default=None, validation_alias="mediaProfile", serialization_alias="mediaProfile"
    )
    phone_profile: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="phoneProfile", serialization_alias="phoneProfile"
    )
    translation_profile: Optional[TranslationProfile] = Field(
        default=None, validation_alias="translationProfile", serialization_alias="translationProfile"
    )
    translation_profile_direction: Optional[
        Union[Variable, Default[None], Global[TranslationProfileDirection]]
    ] = Field(
        default=None, validation_alias="translationProfileDirection", serialization_alias="translationProfileDirection"
    )


class SrstParcel(_ParcelBase):
    type_: Literal["srst"] = Field(default="srst", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    max_dn: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "maxDn"))
    max_phones: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "maxPhones"))
    pool: List[Pool] = Field(
        validation_alias=AliasPath("data", "pool"),
        description="Voice register pool",
    )
    call_forward: Optional[List[CallForward]] = Field(
        default=None,
        validation_alias=AliasPath("data", "callForward"),
        description="Call forward option",
    )
    filename: Optional[Union[Default[None], Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "filename")
    )
    moh: Optional[Union[Default[bool], Global[bool]]] = Field(default=None, validation_alias=AliasPath("data", "moh"))
    system_message: Optional[Union[Default[None], Global[str]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "systemMessage"),
    )
    translation_and_media_profile: Optional[List[TranslationAndMediaProfile]] = Field(
        default=None,
        validation_alias=AliasPath("data", "translationAndMediaProfile"),
        description="translationProfile ID Refs and mediaProfile ID Refs",
    )
