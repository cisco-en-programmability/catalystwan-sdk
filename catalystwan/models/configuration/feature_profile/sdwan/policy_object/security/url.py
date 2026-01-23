# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, ConfigDict, Field, model_serializer

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry

URLListSubtype = Literal["urlallowed", "urlblocked"]


class BaseURLListEntry(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str]


class URLParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    subtype: Optional[URLListSubtype] = Field(  # field name must not clash with any of aliases
        default=None,
        validation_alias=AliasPath("data", "type"),
        # serialization alias handled by _BaseParcel model serializer
        description="must be used only for versions > 20.15.2",
    )
    legacy_subtype: Optional[URLListSubtype] = Field(  # field name must not clash with any of aliases
        exclude=True,
        default=None,
        validation_alias="type",
        serialization_alias="type",
        description="must be used only for versions <= 20.15.2",
    )
    type_: Literal["security-urllist"] = Field(default="security-urllist", exclude=True)
    entries: List[BaseURLListEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_url(self, pattern: str):
        self.entries.append(BaseURLListEntry(pattern=Global[str](value=pattern)))

    def use_legacy_subtype(self):
        if self.subtype is not None:
            self.legacy_subtype = self.subtype
            self.subtype = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler, info):
        serialized = _ParcelBase.envelope_parcel_data(self, handler, info)
        if self.legacy_subtype:
            serialized["type"] = self.legacy_subtype
        return serialized
