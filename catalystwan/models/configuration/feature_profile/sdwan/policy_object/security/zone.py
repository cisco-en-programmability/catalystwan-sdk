# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry
from catalystwan.models.common import InterfaceStr, check_fields_exclusive


class SecurityZoneListEntry(_ParcelEntry):
    vpn: Optional[Global[str]] = Field(default=None)
    interface: Optional[Global[InterfaceStr]] = Field(default=None)

    @model_validator(mode="after")
    def check_vpn_xor_interface(self):
        check_fields_exclusive(self.__dict__, {"vpn", "interface"}, True)
        return self


class SecurityZoneListParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["security-zone"] = Field(default="security-zone", exclude=True)
    entries: List[SecurityZoneListEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_interface(self, interface: InterfaceStr):
        self.entries.append(
            SecurityZoneListEntry(
                interface=Global[InterfaceStr](value=interface),
            )
        )

    def add_vpn(self, vpn: Union[str, int]):
        self.entries.append(
            SecurityZoneListEntry(
                vpn=Global[str](value=str(vpn)),
            )
        )
