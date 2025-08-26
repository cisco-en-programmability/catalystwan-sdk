# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import IkeCiphersuite, IkeGroup, IkeMode, IpsecCiphersuite, IpsecTunnelMode, PfsGroup
from catalystwan.models.configuration.feature_profile.common import (
    AddressAndMaskWithDefault,
    AddressWithMask,
    TunnelApplication,
)


class InterfaceIpsecParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["wan/vpn/interface/ipsec"] = Field(default="wan/vpn/interface/ipsec", exclude=True, frozen=True)
    address: Optional[AddressAndMaskWithDefault] = Field(
        default=None,
        validation_alias=AliasPath("data", "address"),
        description="""
            This filed is required in version < 20.14 (default: 1500).
            In version >=20.14 it is optional, as it can be replaced by ipv6_address.
        """,
    )
    ipv6_address: Optional[Union[Global[str], Global[IPv6Interface], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "ipv6Address"),
        description="This field is supported from version 20.14",
    )
    application: Union[Variable, Global[TunnelApplication]] = Field(validation_alias=AliasPath("data", "application"))
    clear_dont_fragment: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=False),
        validation_alias=AliasPath("data", "clearDontFragment"),
        description="Required if address is provided (default: False). None otherwise.",
    )
    if_description: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    dpd_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=10), validation_alias=AliasPath("data", "dpdInterval")
    )
    dpd_retries: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=3), validation_alias=AliasPath("data", "dpdRetries")
    )
    if_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "ifName"))
    ike_ciphersuite: Union[Variable, Global[IkeCiphersuite], Default[IkeCiphersuite]] = Field(
        default=Default[IkeCiphersuite](value="aes256-cbc-sha1"), validation_alias=AliasPath("data", "ikeCiphersuite")
    )
    ike_group: Union[Global[IkeGroup], Default[IkeGroup], Variable] = Field(
        default=Default[IkeGroup](value="16"), validation_alias=AliasPath("data", "ikeGroup")
    )
    ike_local_id: Union[Variable, Global[str], Default[None]] = Field(
        validation_alias=AliasPath("data", "ikeLocalId"), default=Default[None](value=None)
    )
    ike_rekey_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=14400), validation_alias=AliasPath("data", "ikeRekeyInterval")
    )
    ike_remote_id: Union[Variable, Global[str], Default[None], Global[IPv4Address]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "ikeRemoteId")
    )
    ike_version: Union[Global[int], Default[int]] = Field(
        default=Default[int](value=1), validation_alias=AliasPath("data", "ikeVersion")
    )
    ipsec_ciphersuite: Union[Variable, Global[IpsecCiphersuite], Default[IpsecCiphersuite]] = Field(
        default=Default[IpsecCiphersuite](value="aes256-gcm"), validation_alias=AliasPath("data", "ipsecCiphersuite")
    )
    ipsec_rekey_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=3600), validation_alias=AliasPath("data", "ipsecRekeyInterval")
    )
    ipsec_replay_window: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=512), validation_alias=AliasPath("data", "ipsecReplayWindow")
    )
    mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "mtu"),
        description="Required if address is provided (default: 1500). None otherwise.",
    )
    mtu_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "mtuV6"),
        description="Required if ipv6_address is provided (default: Default[None]). None otherwise.",
    )
    multiplexing: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "multiplexing"),
        description="This field is supported from version 20.14 (default False)",
    )
    perfect_forward_secrecy: Union[Variable, Default[PfsGroup], Global[PfsGroup]] = Field(
        default=Default[PfsGroup](value="group-16"),
        validation_alias=AliasPath("data", "perfectForwardSecrecy"),
    )
    pre_shared_secret: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "preSharedSecret"))
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=True), validation_alias=AliasPath("data", "shutdown")
    )
    tcp_mss_adjust: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "tcpMssAdjust"),
        description="Required if address is provided (default: Default[None]). None otherwise.",
    )
    tcp_mss_adjust_v6: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "tcpMssAdjustV6"),
        description="Required if ipv6_address is provided (default: Default[None]). None otherwise.",
    )
    tunnel_mode: Optional[Union[Global[IpsecTunnelMode], Default[IpsecTunnelMode]]] = Field(
        validation_alias=AliasPath("data", "tunnelMode"),
        default=None,
    )
    tunnel_destination: Optional[AddressWithMask] = Field(
        validation_alias=AliasPath("data", "tunnelDestination"), default=None
    )
    tunnel_destination_v6: Optional[Union[Global[str], Global[IPv6Address], Variable]] = Field(
        default=None,
        validation_alias=AliasPath("data", "tunnelDestinationV6"),
        description="Required if ipv6_address is provided. None otherwise.",
    )
    tunnel_source: Optional[AddressWithMask] = Field(default=None, validation_alias=AliasPath("data", "tunnelSource"))
    tunnel_source_v6: Optional[Union[Global[str], Variable]] = Field(
        validation_alias=AliasPath("data", "tunnelSourceV6"), default=None
    )
    ike_mode: Optional[Union[Variable, Global[IkeMode], Default[IkeMode]]] = Field(
        default=Default[IkeMode](value="main"), validation_alias=AliasPath("data", "ikeMode")
    )
    tracker: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tracker")
    )
    tunnel_route_via: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelRouteVia")
    )
    tunnel_source_interface: Optional[Union[Variable, Global[str], Global[IPv4Interface]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelSourceInterface")
    )
