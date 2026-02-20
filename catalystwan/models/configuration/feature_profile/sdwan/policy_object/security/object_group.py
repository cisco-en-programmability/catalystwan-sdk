# Copyright 2025 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network, IPv6Network
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, _ParcelEntry
from catalystwan.models.common import GeoLocation
from catalystwan.models.configuration.feature_profile.common import RefIdList

SequenceIpType = Literal[
    "ipv4",
    "ipv6",
]


class DataPrefix(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_value: Union[Global[List[IPv4Network]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )

    @classmethod
    def from_variable_name(cls, value: str) -> Self:
        return cls(ipv4_value=Variable(value=value))

    @classmethod
    def from_ipv4_networks(cls, value: List[IPv4Network]) -> Self:
        return cls(ipv4_value=Global[List[IPv4Network]](value=value))


class DataPrefixIpv6(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv6_value: Union[Global[List[IPv6Network]], Variable] = Field(
        validation_alias="ipv6Value", serialization_alias="ipv6Value"
    )

    @classmethod
    def from_variable_name(cls, value: str) -> Self:
        return cls(ipv6_value=Variable(value=value))

    @classmethod
    def from_ipv6_networks(cls, value: List[IPv6Network]) -> Self:
        return cls(ipv6_value=Global[List[IPv6Network]](value=value))


class Fqdn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    fqdn_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="fqdnValue", serialization_alias="fqdnValue"
    )

    @classmethod
    def from_variable_name(cls, value: str) -> Self:
        return cls(fqdn_value=Variable(value=value))

    @classmethod
    def from_domain_names(cls, value: List[str]) -> Self:
        return cls(fqdn_value=Global[List[str]](value=value))


class Port(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )

    @classmethod
    def from_variable_name(cls, value: str) -> Self:
        return cls(port_value=Variable(value=value))

    @classmethod
    def from_ports(cls, value: List[str]) -> Self:
        return cls(port_value=Global[List[str]](value=value))


class SecurityObjectGroupEntries(_ParcelEntry):
    model_config = ConfigDict(populate_by_name=True)
    data_prefix: Optional[DataPrefix] = Field(
        default=None, validation_alias="dataPrefix", serialization_alias="dataPrefix"
    )
    data_prefix_ipv6: Optional[DataPrefixIpv6] = Field(
        default=None, validation_alias="dataPrefixIpv6", serialization_alias="dataPrefixIpv6"
    )
    data_prefix_ipv6_list: Optional[RefIdList] = Field(
        default=None, validation_alias="dataPrefixIpv6List", serialization_alias="dataPrefixIpv6List"
    )
    data_prefix_list: Optional[RefIdList] = Field(
        default=None, validation_alias="dataPrefixList", serialization_alias="dataPrefixList"
    )
    fqdn: Optional[Fqdn] = Field(default=None)
    fqdn_list: Optional[RefIdList] = Field(default=None, validation_alias="fqdnList", serialization_alias="fqdnList")
    geo_location: Optional[Union[Variable, Global[List[GeoLocation]]]] = Field(
        default=None, validation_alias="geoLocation", serialization_alias="geoLocation"
    )
    geo_location_list: Optional[RefIdList] = Field(
        default=None, validation_alias="geoLocationList", serialization_alias="geoLocationList"
    )
    port: Optional[Port] = Field(default=None)
    port_list: Optional[RefIdList] = Field(default=None, validation_alias="portList", serialization_alias="portList")


class SecurityObjectGroupParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["security-object-group"] = Field(default="security-object-group", exclude=True)
    entries: List[SecurityObjectGroupEntries] = Field(
        validation_alias=AliasPath("data", "entries"), default_factory=list
    )
    sequence_ip_type: Optional[Global[SequenceIpType]] = Field(
        default=None, validation_alias="sequenceIpType", serialization_alias="sequenceIpType"
    )
