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
    "app-list",
    "app-probe",
    "appqoe",
    "as-path",
    "banner",
    "basic",
    "bfd",
    "bgp",
    "cellular-controller",
    "class",
    "color",
    "config",
    "config",
    "custom-control",
    "data-ipv6-prefix",
    "data-prefix",
    "dhcp-server",
    "dns",
    "expanded-community",
    "ext-community",
    "global",
    "gps",
    "hubspoke",
    "ipv6-prefix",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/gre",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/multilink",
    "lan/vpn/interface/svi",
    "logging",
    "management/vpn",
    "management/vpn/interface/ethernet",
    "mesh",
    "mirror",
    "mrf",
    "ntp",
    "omp",
    "policer",
    "policy-settings",
    "preferred-color-group",
    "prefix",
    "qos-policy",
    "routing/bgp",
    "routing/eigrp",
    "routing/multicast",
    "routing/ospf",
    "routing/ospfv3/ipv4",
    "routing/ospfv3/ipv6",
    "security-fqdn",
    "security-geolocation",
    "security-ipssignature",
    "security-localapp",
    "security-localdomain",
    "security-port",
    "security-protocolname",
    "security-urllist",
    "security-urllist",
    "security-zone",
    "security",
    "sig",
    "sla-class",
    "snmp",
    "standard-community",
    "switchport",
    "tloc",
    "tracker",
    "trackergroup",
    "unified/advanced-inspection-profile",
    "unified/advanced-malware-protection",
    "unified/intrusion-prevention",
    "unified/ssl-decryption-profile",
    "unified/ssl-decryption",
    "unified/url-filtering",
    "wan/vpn",
    "wan/vpn/interface/cellular",
    "wan/vpn/interface/dsl-ipoe",
    "wan/vpn/interface/dsl-pppoa",
    "wan/vpn/interface/dsl-pppoe",
    "wan/vpn/interface/eth-pppoe",
    "wan/vpn/interface/ethernet",
    "wan/vpn/interface/gre",
    "wan/vpn/interface/multilink",
    "wan/vpn/interface/serial",
    "wirelesslan",
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
    parcel_id: Union[str, UUID] = Field(alias="parcelId")
    parcel_type: ParcelType = Field(alias="parcelType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: int = Field(alias="createdOn")
    last_updated_on: int = Field(alias="lastUpdatedOn")
    payload: T

    @model_validator(mode="before")
    def validate_payload(cls, data):
        if not isinstance(data, dict):
            return data
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
