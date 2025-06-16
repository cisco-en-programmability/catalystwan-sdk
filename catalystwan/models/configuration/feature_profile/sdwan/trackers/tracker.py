# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

Protocol = Literal[
    "tcp",
    "udp",
]


class EndpointTcpUdp(BaseModel):
    port: Optional[Union[Variable, Global[int]]] = Field(default=None)
    protocol: Optional[Union[Variable, Global[Protocol]]] = Field(default=None)


EndpointTrackerType = Literal[
    "ipv6-interface",
    "ipv6-interface-icmp",
]


class Tracker(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["tracker"] = Field(default="tracker", exclude=True, frozen=True)
    tracker_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "trackerName"))
    tracker_type: Union[Default[Literal["endpoint"]], Variable, Global[Literal["endpoint"]]] = Field(
        default=Default[Literal["endpoint"]](value="endpoint"), validation_alias=AliasPath("data", "trackerType")
    )
    endpoint_api_url: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointApiUrl")
    )
    endpoint_dns_name: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointDnsName")
    )
    endpoint_ip: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointIp")
    )
    endpoint_tcp_udp: Optional[EndpointTcpUdp] = Field(
        default=None, validation_alias=AliasPath("data", "endpointTcpUdp"), description="Endpoint tcp/udp"
    )
    endpoint_tracker_type: Optional[
        Union[Variable, Default[Literal["static-route"]], Global[Literal["static-route"]]]
    ] = Field(default=None, validation_alias=AliasPath("data", "endpointTrackerType"))
    interval: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "interval")
    )
    multiplier: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "multiplier")
    )
    threshold: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "threshold")
    )


class TrackerIPv6(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["ipv6-tracker"] = Field(default="ipv6-tracker", exclude=True, frozen=True)
    endpoint_api_url: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointApiUrl")
    )
    endpoint_dns_name: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointDnsName")
    )
    endpoint_ip: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointIp")
    )
    endpoint_tracker_type: Optional[Union[Default[Literal["ipv6-interface"]], Global[EndpointTrackerType]]] = Field(
        default=None, validation_alias=AliasPath("data", "endpointTrackerType")
    )
    icmp_interval: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "icmpInterval")
    )
    interval: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "interval")
    )
    multiplier: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "multiplier")
    )
    threshold: Optional[Union[Default[int], Variable, Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "threshold")
    )
    tracker_name: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "trackerName")
    )
    tracker_type: Optional[Union[Default[Literal["endpoint"]], Variable, Global[Literal["endpoint"]]]] = Field(
        default=None, validation_alias=AliasPath("data", "trackerType")
    )
