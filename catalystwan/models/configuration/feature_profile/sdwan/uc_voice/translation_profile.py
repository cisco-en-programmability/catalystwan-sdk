# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union
from uuid import UUID

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

    def set_ref_by_call_type(self, ref: UUID, ct: CallType) -> TranslationProfileSettings:
        """Set reference UUID to a calling or called rule item or create one and then set the UUID"""
        tps = None
        for tps_ in self.translation_profile_settings:
            if isinstance(tps_.call_type, Global) and tps_.call_type.value == ct:
                tps = tps_
        if tps is None:
            tps = TranslationProfileSettings(call_type=Global[CallType](value=ct))
            self.translation_profile_settings.append(tps)
        tps.translation_rule = RefIdItem.from_uuid(ref)
        return tps
