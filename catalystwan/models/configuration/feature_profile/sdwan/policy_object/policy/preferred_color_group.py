# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry
from catalystwan.models.common import TLOCColor, check_any_of_fields

PathPreference = Literal[
    "direct-path",
    "multi-hop-path",
    "all-paths",
]


class Preference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    color_preference: Optional[Global[List[TLOCColor]]] = Field(
        default=None, serialization_alias="colorPreference", validation_alias="colorPreference"
    )
    path_preference: Optional[Global[PathPreference]] = Field(
        default=None, serialization_alias="pathPreference", validation_alias="pathPreference"
    )

    @model_validator(mode="after")
    def check_color_or_path(self):
        check_any_of_fields(self.__dict__, {"color_preference", "path_preference"})
        return self


class PreferredColorGroupEntry(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    primary_preference: Preference = Field(
        serialization_alias="primaryPreference", validation_alias="primaryPreference"
    )
    secondary_preference: Optional[Preference] = Field(
        default=None, serialization_alias="secondaryPreference", validation_alias="secondaryPreference"
    )
    tertiary_preference: Optional[Preference] = Field(
        default=None, serialization_alias="tertiaryPreference", validation_alias="tertiaryPreference"
    )

    @model_validator(mode="after")
    def check_preference_precedence(self) -> "PreferredColorGroupEntry":
        if not self.secondary_preference and self.tertiary_preference:
            raise IndexError("Preference Entry has to have a secondary prefrence when assigning tertiary preference.")
        return self

    @field_validator("secondary_preference", "tertiary_preference", mode="before")
    @classmethod
    def remove_empty_preferences(cls, value):
        """handle a situation when server returns empty json object: '{}'"""
        if not value:
            return None
        return value


class PreferredColorGroupParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["preferred-color-group"] = Field(default="preferred-color-group", exclude=True)
    entries: List[PreferredColorGroupEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    @staticmethod
    def _create_preference(color_preference: List[TLOCColor], path_preference: Optional[PathPreference]) -> Preference:
        _color_preference = None
        _path_preference = None
        if color_preference:
            _color_preference = Global[List[TLOCColor]](value=color_preference)
        if path_preference:
            _path_preference = Global[PathPreference](value=path_preference)
        return Preference(color_preference=_color_preference, path_preference=_path_preference)

    def add_primary(self, color_preference: List[TLOCColor], path_preference: Optional[PathPreference]):
        self.entries.append(
            PreferredColorGroupEntry(
                primary_preference=PreferredColorGroupParcel._create_preference(color_preference, path_preference),
                secondary_preference=None,
                tertiary_preference=None,
            )
        )

    def add_secondary(self, color_preference: List[TLOCColor], path_preference: Optional[PathPreference]):
        preferred_color = self.entries[0]
        if preferred_color.primary_preference is None:
            raise IndexError("Preference Entry has to have a primary prefrence when assigning secondary preference.")
        preferred_color.secondary_preference = PreferredColorGroupParcel._create_preference(
            color_preference, path_preference
        )

    def add_tertiary(self, color_preference: List[TLOCColor], path_preference: Optional[PathPreference]):
        preferred_color = self.entries[0]
        if preferred_color.primary_preference is None or preferred_color.secondary_preference is None:
            raise IndexError(
                "Preference Entry has to have a primary and secondary prefrence when assigning secondary preference."
            )
        preferred_color.tertiary_preference = PreferredColorGroupParcel._create_preference(
            color_preference, path_preference
        )
