# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network
from typing import List, Literal, Optional

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry
from catalystwan.models.common import Ipv4GePrefixRangeLen, Ipv4LePrefixRangeLen, Ipv4PrefixLen


class PrefixListEntry(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_address: Global[IPv4Address] = Field(serialization_alias="ipv4Address", validation_alias="ipv4Address")
    ipv4_prefix_length: Global[Ipv4PrefixLen] = Field(
        serialization_alias="ipv4PrefixLength", validation_alias="ipv4PrefixLength"
    )
    le_range_prefix_length: Optional[Global[Ipv4LePrefixRangeLen]] = Field(
        default=None, serialization_alias="leRangePrefixLength", validation_alias="leRangePrefixLength"
    )
    ge_range_prefix_length: Optional[Global[Ipv4GePrefixRangeLen]] = Field(
        default=None, serialization_alias="geRangePrefixLength", validation_alias="geRangePrefixLength"
    )


class PrefixListParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["prefix"] = Field(default="prefix", exclude=True)
    entries: List[PrefixListEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ipv4_network: IPv4Network, le: Optional[int] = None, ge: Optional[int] = None):
        le_ = Global[Ipv4LePrefixRangeLen](value=le) if le is not None else None
        ge_ = Global[Ipv4GePrefixRangeLen](value=ge) if ge is not None else None
        self.entries.append(
            PrefixListEntry(
                ipv4_address=Global[IPv4Address](value=ipv4_network.network_address),
                ipv4_prefix_length=Global[int](value=ipv4_network.prefixlen),
                le_range_prefix_length=le_,
                ge_range_prefix_length=ge_,
            )
        )
