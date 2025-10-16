# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Optional
from pydantic import AliasPath, BaseModel, ConfigDict, Field
from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase, as_default, as_global


class NewHostMappingItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    host_name: Global[str] = Field(
        validation_alias="hostName",
        serialization_alias="hostName",
        description="Hostname",
    )
    list_of_ip: Global[List[str]] = Field(
        validation_alias="listOfIp",
        serialization_alias="listOfIp",
        description="List of IP addresses",
    )


class NextHopItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    address: Global[str] = Field(
        validation_alias="address",
        serialization_alias="address",
        description="Next hop IP address",
    )
    distance: Optional[Default[int]] = Field(
        default=as_default(1),
        validation_alias="distance",
        serialization_alias="distance",
        description="Administrative distance",
    )


class Prefix(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    ip_address: Global[str] = Field(
        validation_alias="ipAddress",
        serialization_alias="ipAddress",
        description="IP address",
    )
    subnet_mask: Global[str] = Field(
        validation_alias="subnetMask",
        serialization_alias="subnetMask",
        description="Subnet mask",
    )


class Ipv4RouteItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    prefix: Prefix = Field(
        validation_alias="prefix",
        serialization_alias="prefix",
        description="IP prefix",
    )
    gateway: Optional[Default[str]] = Field(
        default=as_default("nextHop"),
        validation_alias="gateway",
        serialization_alias="gateway",
        description="Gateway type",
    )
    next_hop: Optional[List[NextHopItem]] = Field(
        default=None,
        validation_alias="nextHop",
        serialization_alias="nextHop",
        description="Next hop addresses",
    )
    distance: Optional[Default[int]] = Field(
        default=as_default(1),
        validation_alias="distance",
        serialization_alias="distance",
        description="Administrative distance",
    )


class Ipv6Prefix(BaseModel):
    """IPv6 prefix configuration."""
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    address: Global[str] = Field(
        validation_alias="address",
        description="IPv6 prefix address",
    )


class Ipv6NextHopItem(BaseModel):
    """IPv6 next hop configuration."""
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    address: Global[str] = Field(
        validation_alias="address",
        description="IPv6 next hop address",
    )
    distance: Optional[Default[int]] = Field(
        default=as_default(1),
        validation_alias="distance",
        description="Administrative distance",
    )


class Ipv6RouteItem(BaseModel):
    """IPv6 static route configuration."""
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    prefix: Ipv6Prefix = Field(
        validation_alias="prefix",
        description="Destination IPv6 prefix",
    )
    next_hop: Optional[List[Ipv6NextHopItem]] = Field(
        default=None,
        validation_alias="nextHop",
        description="IPv6 next hop addresses",
    )


class _BaseVpnParcel(_ParcelBase):
    """
    Base class for VPN parcels with common host mapping and routing methods.
    This abstract base class provides shared functionality for both WAN VPN (VPN 0)
    and Management VPN (VPN 512) configurations.
    """

    # These fields will be defined in child classes
    new_host_mapping: Optional[List[NewHostMappingItem]] = None
    ipv4_route: Optional[List[Ipv4RouteItem]] = None
    ipv6_route: Optional[List[Ipv6RouteItem]] = None

    def add_host_mapping(self, hostname: str, ip_addresses: List[str]) -> NewHostMappingItem:
        """
        Add a static hostname to IP address mapping.
        Args:
            hostname: The hostname to map
            ip_addresses: List of IP addresses for the hostname
        Returns:
            NewHostMappingItem: The created host mapping item 
        Example:
            >>> vpn.add_host_mapping("vbond", ["10.1.1.1", "10.2.2.2"])
        """
        item = NewHostMappingItem(
            host_name=as_global(hostname),
            list_of_ip=Global[List[str]](value=ip_addresses)
        )

        if self.new_host_mapping:
            self.new_host_mapping.append(item)
        else:
            self.new_host_mapping = [item]

        return item

    def add_ipv4_route(
        self,
        ip_address: str,
        subnet_mask: str,
        next_hops: List[tuple],
        gateway: str = "nextHop",
        distance: int = 1
    ) -> Ipv4RouteItem:
        """
        Add an IPv4 static route.
        Args:
            ip_address: Destination IP address
            subnet_mask: Subnet mask
            next_hops: List of tuples (next_hop_ip, distance)
            gateway: Gateway type (default: "nextHop")
            distance: Administrative distance
        Returns:
            Ipv4RouteItem: The created route item
        Example:
            >>> vpn.add_ipv4_route("192.168.1.0", "255.255.255.0", [("10.1.1.1", 1)])
        """
        next_hop_items = []
        for next_hop_ip, next_hop_distance in next_hops:
            next_hop_items.append(
                NextHopItem(
                    address=as_global(next_hop_ip),
                    distance=as_default(next_hop_distance)
                )
            )

        route = Ipv4RouteItem(
            prefix=Prefix(
                ip_address=as_global(ip_address),
                subnet_mask=as_global(subnet_mask)
            ),
            gateway=as_default(gateway),
            next_hop=next_hop_items,
            distance=as_default(distance)
        )

        if self.ipv4_route:
            self.ipv4_route.append(route)
        else:
            self.ipv4_route = [route]
        return route

    def add_ipv6_route(
        self,
        prefix: str,
        next_hops: List[tuple],
    ) -> Ipv6RouteItem:
        """
        Add an IPv6 static route.
        Args:
            prefix: Destination IPv6 prefix (e.g., "2001:db8::/64")
            next_hops: List of (next_hop_ipv6, distance) tuples
        Returns:
            Ipv6RouteItem: The created route item
        Example:
            >>> vpn.add_ipv6_route("2001:db8::/64", [("2001:db8::1", 1)])
        """
        next_hop_items = [
            Ipv6NextHopItem(
                address=as_global(nh_ip),
                distance=as_default(nh_distance)
            )
            for nh_ip, nh_distance in next_hops
        ]

        item = Ipv6RouteItem(
            prefix=Ipv6Prefix(address=as_global(prefix)),
            next_hop=next_hop_items
        )

        if self.ipv6_route:
            self.ipv6_route.append(item)
        else:
            self.ipv6_route = [item]

        return item


class WanVpn(_BaseVpnParcel):
    """
    WAN VPN Parcel for Transport Feature Profile.
    This parcel configures VPN 0 (WAN/Transport VPN) which is used for
    WAN connectivity and transport-side configurations.
    """
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    vpn_id: Optional[Default[int]] = Field(
        default=as_default(0),
        validation_alias=AliasPath("data", "vpnId"),
        description="VPN ID (0 for WAN/Transport)",
    )
    enhance_ecmp_keying: Optional[Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "enhanceEcmpKeying"),
        description="Enable enhanced ECMP keying",
    )
    new_host_mapping: Optional[List[NewHostMappingItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "newHostMapping"),
        description="Static hostname to IP mappings",
    )
    ipv4_route: Optional[List[Ipv4RouteItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "ipv4Route"),
        description="IPv4 static routes",
    )
    ipv6_route: Optional[List[Ipv6RouteItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "ipv6Route"),
        description="IPv6 static routes",
    )
    service: Optional[List] = Field(
        default=None,
        validation_alias=AliasPath("data", "service"),
        description="Services configuration",
    )


class ManagementVpn(_BaseVpnParcel):
    """
    Management VPN Parcel for Transport Feature Profile.
    This parcel configures VPN 512 (Management VPN) which is used for
    out-of-band management connectivity.
    """
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    vpn_id: Optional[Default[int]] = Field(
        default=as_default(512),
        validation_alias=AliasPath("data", "vpnId"),
        description="VPN ID (512 for Management)",
    )
    new_host_mapping: Optional[List[NewHostMappingItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "newHostMapping"),
        description="Static hostname to IP mappings",
    )
    ipv4_route: Optional[List[Ipv4RouteItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "ipv4Route"),
        description="IPv4 static routes",
    )
    ipv6_route: Optional[List[Ipv6RouteItem]] = Field(
        default=None,
        validation_alias=AliasPath("data", "ipv6Route"),
        description="IPv6 static routes",
    )
