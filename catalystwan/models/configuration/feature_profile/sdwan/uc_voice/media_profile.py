# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import MpDtmf, MpVoiceCodec


class MediaProfileParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["media-profile"] = Field(default="media-profile", exclude=True)
    codec: Global[List[MpVoiceCodec]] = Field(validation_alias=AliasPath("data", "codec"))
    dtmf: Union[Variable, Global[List[MpDtmf]], Default[List[MpDtmf]]] = Field(
        validation_alias=AliasPath("data", "dtmf")
    )
    media_profile_number: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "mediaProfileNumber"))
