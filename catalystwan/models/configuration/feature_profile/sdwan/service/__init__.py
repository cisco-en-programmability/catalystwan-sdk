# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.routing import AnyRoutingParcel

from ..acl import AnyAclParcel
from .appqoe import AppqoeParcel
from .dhcp_server import LanVpnDhcpServerParcel
from .dual_router_ha import DualRouterHaParcel
from .eigrp import EigrpParcel
from .lan.ethernet import InterfaceEthernetParcel
from .lan.gre import InterfaceGreParcel
from .lan.ipsec import InterfaceIpsecParcel
from .lan.multilink import InterfaceMultilinkParcel
from .lan.svi import InterfaceSviParcel
from .lan.vpn import LanVpnParcel
from .multicast import MulticastParcel
from .route_policy import RoutePolicyParcel
from .service_chain import ServiceChainParcel
from .switchport import SwitchportParcel
from .wireless_lan import WirelessLanParcel

AnyTopLevelServiceParcel = Annotated[
    Union[
        AppqoeParcel,
        DualRouterHaParcel,
        EigrpParcel,
        LanVpnDhcpServerParcel,
        LanVpnParcel,
        MulticastParcel,
        RoutePolicyParcel,
        ServiceChainParcel,
        SwitchportParcel,
        WirelessLanParcel,
        # TrackerGroupData,
        # WirelessLanData,
        # SwitchportData
    ],
    Field(discriminator="type_"),
]

AnyLanVpnInterfaceParcel = Annotated[
    Union[
        InterfaceEthernetParcel,
        InterfaceGreParcel,
        InterfaceIpsecParcel,
        InterfaceSviParcel,
        InterfaceMultilinkParcel,
    ],
    Field(discriminator="type_"),
]

AnyAssociatoryParcel = Annotated[
    Union[
        MulticastParcel,
        # DHCP
    ],
    Field(discriminator="type_"),
]

AnyServiceParcel = Annotated[
    Union[AnyAclParcel, AnyTopLevelServiceParcel, AnyLanVpnInterfaceParcel, AnyRoutingParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "AnyLanVpnInterfaceParcel",
    "AnyServiceParcel",
    "AnyTopLevelServiceParcel",
    "AppqoeParcel",
    "InterfaceGreParcel",
    "InterfaceSviParcel",
    "LanVpnDhcpServerParcel",
    "LanVpnParcel",
    "ServiceChainParcel",
    "DualRouterHaParcel",
    "MulticastParcel",
    "OspfParcel",
    "Ospfv3IPv4Parcel",
    "Ospfv3IPv6Parcel",
    "RoutePolicyParcel",
    "SwitchportParcel",
    "WirelessLanParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
