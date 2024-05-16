# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .bgp import WanRoutingBgpParcel as BGPParcel
from .cellular_controller import CellularControllerParcel
from .cellular_profile import CellularProfileParcel
from .gps import GpsParcel
from .t1e1controller import T1E1ControllerParcel
from .vpn import ManagementVpnParcel, TransportVpnParcel
from .wan.interface.gre import InterfaceGreParcel
from .wan.interface.ipsec import InterfaceIpsecParcel
from .wan.interface.protocol_over import (
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
)
from .wan.interface.t1e1serial import T1E1SerialParcel

AnyTransportVpnSubParcel = Annotated[
    Union[
        T1E1SerialParcel,
        InterfaceEthPPPoEParcel,
        InterfaceDslPPPoEParcel,
        InterfaceDslPPPoAParcel,
        InterfaceDslIPoEParcel,
        InterfaceGreParcel,
        InterfaceIpsecParcel,
    ],
    Field(discriminator="type_"),
]
AnyTransportVpnParcel = Annotated[Union[ManagementVpnParcel, TransportVpnParcel], Field(discriminator="type_")]
AnyTransportSuperParcel = Annotated[
    Union[
        T1E1ControllerParcel,
        CellularControllerParcel,
        CellularProfileParcel,
        BGPParcel,
        T1E1ControllerParcel,
        GpsParcel,
    ],
    Field(discriminator="type_"),
]
AnyTransportParcel = Annotated[
    Union[AnyTransportSuperParcel, AnyTransportVpnParcel, AnyTransportVpnSubParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "BGPParcel",
    "CellularControllerParcel",
    "ManagementVpnParcel",
    "TransportVpnParcel",
    "AnyTransportParcel",
    "AnyTransportSuperParcel",
    "AnyTransportVpnSubParcel",
    "T1E1ControllerParcel",
    "T1E1SerialParcel",
    "InterfaceDslPPPoAParcel",
    "InterfaceDslPPPoEParcel",
    "InterfaceEthPPPoEParcel",
    "InterfaceIpsecParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
