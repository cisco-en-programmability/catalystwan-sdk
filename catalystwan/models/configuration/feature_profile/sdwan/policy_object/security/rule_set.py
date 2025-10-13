# Copyright 2025 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Network, IPv6Network
from typing import List, Optional, Union

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
from catalystwan.models.common import GeoLocation, IntStr, ProtocolName, SecurityBaseAction, SecuritySequenceIpType
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class SourceIp(BaseModel):
    ipv4_value: Union[Global[List[IPv4Network]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )


class SourceIpv6(BaseModel):
    ipv6_value: Union[Global[List[IPv6Network]], Variable] = Field(
        validation_alias="ipv6Value", serialization_alias="ipv6Value"
    )


class DestinationIp(BaseModel):
    ipv4_value: Union[Global[List[IPv4Network]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )


class DestinationIpv6(BaseModel):
    ipv6_value: Union[Global[List[IPv6Network]], Variable] = Field(
        validation_alias="ipv6Value", serialization_alias="ipv6Value"
    )


class DestinationFqdn(BaseModel):
    fqdn_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="fqdnValue", serialization_alias="fqdnValue"
    )


class SourcePort(BaseModel):
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )


class DestinationPort(BaseModel):
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )


class Sequences(BaseModel):
    action: Union[Global[SecurityBaseAction], Variable] = Field()
    sequence_id: Union[Variable, Global[IntStr]] = Field(
        validation_alias="sequenceId", serialization_alias="sequenceId"
    )
    sequence_name: Union[Variable, Global[str]] = Field(
        validation_alias="sequenceName", serialization_alias="sequenceName"
    )
    destination_data_ipv6_prefix_list: Optional[RefIdItem] = Field(
        default=None,
        validation_alias="destinationDataIpv6PrefixList",
        serialization_alias="destinationDataIpv6PrefixList",
    )
    destination_data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )
    destination_fqdn: Optional[DestinationFqdn] = Field(
        default=None, validation_alias="destinationFqdn", serialization_alias="destinationFqdn"
    )
    destination_fqdn_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationFqdnList", serialization_alias="destinationFqdnList"
    )
    destination_geo_location: Optional[Union[Variable, Global[List[GeoLocation]]]] = Field(
        default=None, validation_alias="destinationGeoLocation", serialization_alias="destinationGeoLocation"
    )
    destination_geo_location_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationGeoLocationList", serialization_alias="destinationGeoLocationList"
    )
    destination_ip: Optional[DestinationIp] = Field(
        default=None, validation_alias="destinationIp", serialization_alias="destinationIp"
    )
    destination_ipv6: Optional[DestinationIpv6] = Field(
        default=None, validation_alias="destinationIpv6", serialization_alias="destinationIpv6"
    )
    destination_object_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationObjectGroup", serialization_alias="destinationObjectGroup"
    )
    destination_port: Optional[DestinationPort] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )
    destination_port_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationPortList", serialization_alias="destinationPortList"
    )
    protocol: Optional[Global[List[str]]] = Field(default=None)
    protocol_name: Optional[Union[Variable, Global[List[ProtocolName]]]] = Field(
        default=None, validation_alias="protocolName", serialization_alias="protocolName"
    )
    protocol_name_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="protocolNameList", serialization_alias="protocolNameList"
    )
    sequence_ip_type: Optional[Global[SecuritySequenceIpType]] = Field(
        default=None, validation_alias="sequenceIpType", serialization_alias="sequenceIpType"
    )
    source_data_ipv6_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceDataIpv6PrefixList", serialization_alias="sourceDataIpv6PrefixList"
    )
    source_data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )
    source_geo_location: Optional[Union[Variable, Global[List[ProtocolName]]]] = Field(
        default=None, validation_alias="sourceGeoLocation", serialization_alias="sourceGeoLocation"
    )
    source_geo_location_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceGeoLocationList", serialization_alias="sourceGeoLocationList"
    )
    source_ip: Optional[SourceIp] = Field(default=None, validation_alias="sourceIp", serialization_alias="sourceIp")
    source_ipv6: Optional[SourceIpv6] = Field(
        default=None, validation_alias="sourceIpv6", serialization_alias="sourceIpv6"
    )
    source_object_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceObjectGroup", serialization_alias="sourceObjectGroup"
    )
    source_port: Optional[SourcePort] = Field(
        default=None, validation_alias="sourcePort", serialization_alias="sourcePort"
    )
    source_port_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourcePortList", serialization_alias="sourcePortList"
    )


class SecurityRuleSetParcel(_ParcelBase):
    sequences: List[Sequences] = Field(
        validation_alias=AliasPath("data", "sequences"), description="select definition of rule"
    )
