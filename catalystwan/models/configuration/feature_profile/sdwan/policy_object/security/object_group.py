# Copyright 2025 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, _ParcelEntry
from catalystwan.models.common import GeoLocation
from catalystwan.models.configuration.feature_profile.common import RefIdItem

SequenceIpType = Literal[
    "ipv4",
    "ipv6",
]


class DataPrefix(BaseModel):
    ipv4_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )


class DataPrefixIpv6(BaseModel):
    ipv6_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="ipv6Value", serialization_alias="ipv6Value"
    )


class Fqdn(BaseModel):
    fqdn_value: Union[Global[List[Union[str, Global[str]]]], Variable] = Field(
        validation_alias="fqdnValue", serialization_alias="fqdnValue"
    )


class Port(BaseModel):
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )


class SecurityObjectGroupEntries(_ParcelEntry):
    data_prefix: Optional[DataPrefix] = Field(
        default=None, validation_alias="dataPrefix", serialization_alias="dataPrefix"
    )
    data_prefix_ipv6: Optional[DataPrefixIpv6] = Field(
        default=None, validation_alias="dataPrefixIpv6", serialization_alias="dataPrefixIpv6"
    )
    data_prefix_ipv6_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="dataPrefixIpv6List", serialization_alias="dataPrefixIpv6List"
    )
    data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="dataPrefixList", serialization_alias="dataPrefixList"
    )
    fqdn: Optional[Fqdn] = Field(default=None)
    fqdn_list: Optional[RefIdItem] = Field(default=None, validation_alias="fqdnList", serialization_alias="fqdnList")
    geo_location: Optional[Union[Variable, Global[List[GeoLocation]]]] = Field(
        default=None, validation_alias="geoLocation", serialization_alias="geoLocation"
    )
    geo_location_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="geoLocationList", serialization_alias="geoLocationList"
    )
    port: Optional[Port] = Field(default=None)
    port_list: Optional[RefIdItem] = Field(default=None, validation_alias="portList", serialization_alias="portList")


class SecurityObjectGroupParcel(_ParcelBase):
    entries: List[SecurityObjectGroupEntries] = Field(
        validation_alias=AliasPath("data", "entries"), default_factory=list
    )
    sequence_ip_type: Optional[Global[SequenceIpType]] = Field(
        default=None, validation_alias="sequenceIpType", serialization_alias="sequenceIpType"
    )
