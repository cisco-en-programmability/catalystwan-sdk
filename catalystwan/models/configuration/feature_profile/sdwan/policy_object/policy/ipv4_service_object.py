# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, _ParcelEntry
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class EntriesRef(_ParcelEntry):
    object_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="objectGroup", serialization_alias="objectGroup"
    )


ValueProtocol = Literal[
    "ahp",
    "eigrp",
    "esp",
    "gre",
    "icmp",
    "igmp",
    "ip",
    "ipinip",
    "nos",
    "ospf",
    "pcp",
    "pim",
    "tcp",
    "tcp-udp",
    "udp",
]


class SourcePortsLt(BaseModel):
    lt_value: Union[Variable, Global[int]] = Field(validation_alias="ltValue", serialization_alias="ltValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="lt"))


ValueTcpEq = Literal[
    "bgp",
    "chargen",
    "cmd",
    "daytime",
    "discard",
    "domain",
    "echo",
    "exec",
    "finger",
    "ftp",
    "ftp-data",
    "gopher",
    "hostname",
    "ident",
    "irc",
    "klogin",
    "kshell",
    "login",
    "lpd",
    "msrpc",
    "nntp",
    "onep-plain",
    "onep-tls",
    "pim-auto-rp",
    "pop2",
    "pop3",
    "smtp",
    "sunrpc",
    "syslog",
    "tacacs",
    "talk",
    "telnet",
    "time",
    "uucp",
    "whois",
    "www",
]


ValueUdpEq = Literal[
    "biff",
    "bootpc",
    "bootps",
    "discard",
    "dnsix",
    "domain",
    "echo",
    "isakmp",
    "mobile-ip",
    "nameserver",
    "netbios-dgm",
    "netbios-ns",
    "netbios-ss",
    "non500-isakmp",
    "ntp",
    "pim-auto-rp",
    "rip",
    "ripv6",
    "snmp",
    "snmptrap",
    "sunrpc",
    "syslog",
    "tacacs",
    "talk",
    "tftp",
    "time",
    "who",
    "xdmcp",
]


class SourcePortEqValueUdp(BaseModel):
    udp_eq_value: Union[Global[int], Global[ValueUdpEq], Variable] = Field(
        validation_alias="udpEqValue", serialization_alias="udpEqValue"
    )


ValueTcpUdpEq = Literal[
    "discard",
    "domain",
    "echo",
    "pim-auto-rp",
    "sunrpc",
    "syslog",
    "tacacs",
    "talk",
]


class SourcePortEqValueTcpUdp(BaseModel):
    tcp_udp_eq_value: Union[Global[int], Global[ValueTcpUdpEq], Variable] = Field(
        validation_alias="tcpUdpEqValue", serialization_alias="tcpUdpEqValue"
    )


SourcePortsEqValue = Union[SourcePortEqValueUdp, SourcePortEqValueTcpUdp]


class SourcePortsEq(BaseModel):
    eq_value: SourcePortsEqValue = Field(validation_alias="eqValue", serialization_alias="eqValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="eq"))


class SourcePortsGt(BaseModel):
    gt_value: Union[Variable, Global[int]] = Field(validation_alias="gtValue", serialization_alias="gtValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="gt"))


class Range(BaseModel):
    end: Union[Variable, Global[int]] = Field()
    start: Union[Variable, Global[int]] = Field()


class SourcePortsRange(BaseModel):
    range: Range = Field(description="Source Port Range")
    operator: Optional[Global[str]] = Field(default=None)


class DestinationPortsLt(BaseModel):
    lt_value: Union[Variable, Global[int]] = Field(validation_alias="ltValue", serialization_alias="ltValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="lt"))


class EqValueTcp(BaseModel):
    tcp_eq_value: Union[Global[int], Global[ValueTcpEq], Variable] = Field(
        validation_alias="tcpEqValue", serialization_alias="tcpEqValue"
    )


class EqValueUdp(BaseModel):
    udp_eq_value: Union[Global[int], Global[ValueUdpEq], Variable] = Field(
        validation_alias="udpEqValue", serialization_alias="udpEqValue"
    )


class EqValueTcpUdp(BaseModel):
    tcp_udp_eq_value: Union[Global[int], Global[ValueTcpUdpEq], Variable] = Field(
        validation_alias="tcpUdpEqValue", serialization_alias="tcpUdpEqValue"
    )


DestinationPortsEqValue = Union[EqValueTcp, EqValueUdp, EqValueTcpUdp]


class DestinationPortsEq(BaseModel):
    eq_value: DestinationPortsEqValue = Field(validation_alias="eqValue", serialization_alias="eqValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="eq"))


class DestinationPortsGt(BaseModel):
    gt_value: Union[Variable, Global[int]] = Field(validation_alias="gtValue", serialization_alias="gtValue")
    operator: Optional[Global[str]] = Field(default=Global[str](value="gt"))


class DestinationPorts(BaseModel):
    range: Range = Field(description="Destination Port Range")
    operator: Optional[Global[str]] = Field(default=None)


DestinationPortsOptions = Union[DestinationPorts, DestinationPortsEq, DestinationPortsGt, DestinationPortsLt]


ValueIcmpMsg = Literal[
    "alternate-address",
    "conversion-error",
    "echo",
    "echo-reply",
    "information-reply",
    "information-request",
    "mask-reply",
    "mask-request",
    "mobile-redirect",
    "parameter-problem",
    "redirect",
    "router-advertisement",
    "router-solicitation",
    "source-quench",
    "time-exceeded",
    "timestamp-reply",
    "timestamp-request",
    "traceroute",
    "unreachable",
]

SourcePorts = Union[
    SourcePortsGt,
    SourcePortsEq,
    SourcePortsRange,
]


class Entries(_ParcelEntry):
    destination_ports: Optional[DestinationPortsOptions] = Field(
        default=None, validation_alias="destinationPorts", serialization_alias="destinationPorts"
    )
    icmp_msg: Optional[Union[Global[Union[int, ValueIcmpMsg]], Variable]] = Field(
        default=None, validation_alias="icmpMsg", serialization_alias="icmpMsg"
    )
    protocol: Optional[Union[Global[int], Global[ValueProtocol]]] = Field(default=None)
    source_ports: Optional[SourcePorts] = Field(
        default=None, validation_alias="sourcePorts", serialization_alias="sourcePorts"
    )


EntiresOptions = Union[Entries, EntriesRef]


class Ipv4ServiceObjectParcel(_ParcelBase):
    type_: Literal["ipv4-service-object-group"] = Field(default="ipv4-service-object-group", exclude=True)
    entries: List[EntiresOptions] = Field(
        default_factory=list,
        validation_alias=AliasPath("data", "entries"),
        description="object-group Entries",
    )
