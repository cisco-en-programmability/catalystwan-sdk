from typing import Generic, List, Literal, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.application_priority import AnyApplicationPriorityParcel
from catalystwan.models.configuration.feature_profile.sdwan.cli import AnyCliParcel
from catalystwan.models.configuration.feature_profile.sdwan.dns_security import AnyDnsSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import AnyEmbeddedSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyServiceParcel
from catalystwan.models.configuration.feature_profile.sdwan.sig_security import AnySIGSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology import AnyTopologyParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import AnyTransportParcel

ParcelType = Literal[
    "aaa",
    "banner",
    "basic",
    "bfd",
    "global",
    "logging",
    "mrf",
    "ntp",
    "omp",
    "security",
    "snmp",
    "appqoe",
    "as-path",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/gre",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/multilink",
    "lan/vpn/interface/svi",
    "dhcp-server",
    "tracker",
    "trackergroup",
    "routing/bgp",
    "routing/eigrp",
    "routing/multicast",
    "routing/ospf",
    "routing/ospfv3/ipv4",
    "routing/ospfv3/ipv6",
    "wirelesslan",
    "switchport",
    "app-probe",
    "app-list",
    "color",
    "data-prefix",
    "expanded-community",
    "class",
    "data-ipv6-prefix",
    "ipv6-prefix",
    "mirror",
    "prefix",
    "policer",
    "preferred-color-group",
    "sla-class",
    "tloc",
    "standard-community",
    "security-localdomain",
    "security-fqdn",
    "security-ipssignature",
    "security-urllist",
    "security-urllist",
    "security-port",
    "security-protocolname",
    "security-geolocation",
    "security-zone",
    "security-localapp",
    "unified/advanced-inspection-profile",
    "unified/advanced-malware-protection",
    "unified/intrusion-prevention",
    "unified/ssl-decryption",
    "unified/ssl-decryption-profile",
    "unified/url-filtering",
    "management/vpn",
    "wan/vpn",
    "wan/vpn/interface/serial",
    "wan/vpn/interface/dsl-pppoe",
    "wan/vpn/interface/dsl-pppoa",
    "wan/vpn/interface/dsl-ipoe",
    "wan/vpn/interface/eth-pppoe",
    "wan/vpn/interface/gre",
    "wan/vpn/interface/cellular",
    "wan/vpn/interface/ethernet",
    "wan/vpn/interface/multilink",
    "config",
    "dns",
    "gps",
    "cellular-controller",
    "config",
    "sig",
    "policy-settings",
    "qos-policy",
    "hubspoke",
    "mesh",
    "custom-control",
]


AnyParcel = Annotated[
    Union[
        AnySystemParcel,
        AnyPolicyObjectParcel,
        AnyServiceParcel,
        AnyOtherParcel,
        AnyTransportParcel,
        AnyEmbeddedSecurityParcel,
        AnyCliParcel,
        AnyDnsSecurityParcel,
        AnySIGSecurityParcel,
        AnyApplicationPriorityParcel,
        AnyTopologyParcel,
    ],
    Field(discriminator="type_"),
]

T = TypeVar("T", bound=AnyParcel)


class Parcel(BaseModel, Generic[T]):
    parcel_id: str = Field(alias="parcelId")
    parcel_type: ParcelType = Field(alias="parcelType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: int = Field(alias="createdOn")
    last_updated_on: int = Field(alias="lastUpdatedOn")
    payload: T

    @model_validator(mode="before")
    def validate_payload(cls, data):
        data["payload"]["type_"] = data["parcelType"]
        return data


class Header(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    generated_on: int = Field(alias="generatedOn")


class ParcelInfo(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelSequence(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelCreationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


class ParcelAssociationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    parcel_id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


class ParcelId(BaseModel):
    id: str = Field(alias="parcelId")
