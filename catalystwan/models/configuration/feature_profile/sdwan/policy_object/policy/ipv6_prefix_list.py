# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Address, IPv6Interface
from typing import List, Literal, Optional

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry
from catalystwan.models.common import Ipv6GePrefixRangeLen, Ipv6LePrefixRangeLen, Ipv6PrefixLen


class IPv6PrefixListEntry(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    ipv6_address: Global[IPv6Address] = Field(serialization_alias="ipv6Address", validation_alias="ipv6Address")
    ipv6_prefix_length: Global[Ipv6PrefixLen] = Field(
        serialization_alias="ipv6PrefixLength", validation_alias="ipv6PrefixLength", ge=0, le=128
    )
    le_range_prefix_length: Optional[Global[Ipv6LePrefixRangeLen]] = Field(
        default=None, serialization_alias="leRangePrefixLength", validation_alias="leRangePrefixLength"
    )
    ge_range_prefix_length: Optional[Global[Ipv6GePrefixRangeLen]] = Field(
        default=None, serialization_alias="geRangePrefixLength", validation_alias="geRangePrefixLength"
    )


class IPv6PrefixListParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["ipv6-prefix"] = Field(default="ipv6-prefix", exclude=True)
    entries: List[IPv6PrefixListEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ipv6_network: IPv6Interface, ge: Optional[int] = None, le: Optional[int] = None):
        le_ = Global[Ipv6LePrefixRangeLen](value=le) if le is not None else None
        ge_ = Global[Ipv6GePrefixRangeLen](value=ge) if ge is not None else None
        self.entries.append(
            IPv6PrefixListEntry(
                ipv6_address=Global[IPv6Address](value=ipv6_network.network.network_address),
                ipv6_prefix_length=Global[Ipv6PrefixLen](value=ipv6_network.network.prefixlen),
                le_range_prefix_length=le_,
                ge_range_prefix_length=ge_,
            )
        )
