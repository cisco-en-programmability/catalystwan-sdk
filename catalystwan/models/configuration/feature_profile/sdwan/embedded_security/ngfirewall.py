# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Network
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, ValidationError, model_validator
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, as_global, as_variable
from catalystwan.models.common import GeoLocation, ProtocolName, SecurityBaseAction
from catalystwan.models.configuration.feature_profile.common import RefIdItem, RefIdList

DefaultAction = Literal["pass", "drop"]
SequenceType = Literal["ngfirewall"]
AipActionType = Literal["advancedInspectionProfile"]
SequenceActionType = Literal["log", "connectionEvents"]


class Ipv4Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ipv4_value: Union[Global[List[IPv4Network]], Variable] = Field(
        validation_alias="ipv4Value", serialization_alias="ipv4Value"
    )

    @classmethod
    def create_with_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(ipv4_value=as_global(ip_networks))

    @classmethod
    def create_with_variable(cls, variable_name: str) -> Self:
        return cls(ipv4_value=as_variable(variable_name))


class FqdnMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    fqdn_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="fqdnValue", serialization_alias="fqdnValue"
    )

    @classmethod
    def from_domain_names(cls, domain_names: List[str]) -> Self:
        return cls(fqdn_value=as_global(domain_names))


class PortMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    port_value: Union[Global[List[str]], Variable] = Field(
        validation_alias="portValue", serialization_alias="portValue"
    )

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(port_value=as_global(ports))


class SourceDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_data_prefix_list: RefIdList = Field(
        validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )

    @classmethod
    def create(cls, source_data_prefix_list: List[UUID]) -> Self:
        return cls(source_data_prefix_list=RefIdList.from_uuids(uuids=source_data_prefix_list))


class DestinationDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_data_prefix_list: RefIdList = Field(
        validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_data_prefix_list=RefIdList.from_uuids(uuids=uuids))


class DestinationFqdnList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_fqdn_list: RefIdList = Field(
        validation_alias="destinationFqdnList", serialization_alias="destinationFqdnList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_fqdn_list=RefIdList.from_uuids(uuids=uuids))


class SourceGeoLocationList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_geo_location_list: RefIdList = Field(
        validation_alias="sourceGeoLocationList", serialization_alias="sourceGeoLocationList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_geo_location_list=RefIdList.from_uuids(uuids=uuids))


class DestinationGeoLocationList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_geo_location_list: RefIdList = Field(
        validation_alias="destinationGeoLocationList", serialization_alias="destinationGeoLocationList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_geo_location_list=RefIdList.from_uuids(uuids=uuids))


class SourcePortList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_port_list: RefIdList = Field(validation_alias="sourcePortList", serialization_alias="sourcePortList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_port_list=RefIdList.from_uuids(uuids=uuids))


class DestinationPortList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_port_list: RefIdList = Field(
        validation_alias="destinationPortList", serialization_alias="destinationPortList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_port_list=RefIdList.from_uuids(uuids))


class SourceScalableGroupTagList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_scalable_group_tag_list: RefIdList = Field(
        validation_alias="sourceScalableGroupTagList", serialization_alias="sourceScalableGroupTagList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_scalable_group_tag_list=RefIdList.from_uuids(uuids))


class DestinationScalableGroupTagList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_scalable_group_tag_list: RefIdList = Field(
        validation_alias="destinationScalableGroupTagList", serialization_alias="destinationScalableGroupTagList"
    )

    @classmethod  # from_uuids
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(destination_scalable_group_tag_list=RefIdList.from_uuids(uuids))


class SourceIdentityList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_list: RefIdList = Field(
        validation_alias="sourceIdentityList", serialization_alias="sourceIdentityList"
    )

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(source_identity_list=RefIdList.from_uuids(uuids))


class ProtocolNameList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol_name_list: RefIdList = Field(validation_alias="protocolNameList", serialization_alias="protocolNameList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(protocol_name_list=RefIdList.from_uuids(uuids))


class AppList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_list: RefIdList = Field(validation_alias="appList", serialization_alias="appList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(app_list=RefIdList.from_uuids(uuids))


class AppListFlat(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_list_flat: RefIdList = Field(validation_alias="appListFlat", serialization_alias="appListFlat")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(app_list_flat=RefIdList.from_uuids(uuids))


class RuleSetList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    rule_set_list: RefIdList = Field(validation_alias="ruleSetList", serialization_alias="ruleSetList")

    @classmethod
    def create(cls, uuids: List[UUID]) -> Self:
        return cls(rule_set_list=RefIdList.from_uuids(uuids))


class SourceSecurityGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_security_group: RefIdList = Field(
        validation_alias="sourceSecurityGroup", serialization_alias="sourceSecurityGroup"
    )


class DestinationSecurityGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_security_group: RefIdList = Field(
        validation_alias="destinationSecurityGroup", serialization_alias="destinationSecurityGroup"
    )


class SourceIp(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_ip: Ipv4Match = Field(validation_alias="sourceIp", serialization_alias="sourceIp")

    @classmethod
    def from_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(source_ip=Ipv4Match.create_with_ip_networks(ip_networks))

    @classmethod
    def from_variable(cls, variable_name: str) -> Self:
        return cls(source_ip=Ipv4Match.create_with_variable(variable_name))


class DestinationIp(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_ip: Ipv4Match = Field(validation_alias="destinationIp", serialization_alias="destinationIp")

    @classmethod
    def from_ip_networks(cls, ip_networks: List[IPv4Network]) -> Self:
        return cls(destination_ip=Ipv4Match.create_with_ip_networks(ip_networks))

    @classmethod
    def from_variable(cls, variable_name: str) -> Self:
        return cls(destination_ip=Ipv4Match.create_with_variable(variable_name))


class DestinationFqdn(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_fqdn: FqdnMatch = Field(validation_alias="destinationFqdn", serialization_alias="destinationFqdn")

    @classmethod
    def from_domain_names(cls, domain_names: List[str]) -> Self:
        return cls(destination_fqdn=FqdnMatch.from_domain_names(domain_names))


class SourcePort(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_port: PortMatch = Field(validation_alias="sourcePort", serialization_alias="sourcePort")

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(source_port=PortMatch.from_str_list(ports))


class DestinationPort(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_port: PortMatch = Field(validation_alias="destinationPort", serialization_alias="destinationPort")

    @classmethod
    def from_str_list(cls, ports: List[str]) -> Self:
        return cls(destination_port=PortMatch.from_str_list(ports))


class SourceGeoLocation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_geo_loacation: Union[Global[List[GeoLocation]], Variable] = Field(
        validation_alias="sourceGeoLocation", serialization_alias="sourceGeoLocation"
    )

    @classmethod
    def from_geo_locations_list(cls, locations: List[GeoLocation]) -> Self:
        return cls(source_geo_loacation=Global[List[GeoLocation]](value=locations))


class DestinationGeoLocation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_geo_loacation: Union[Global[List[GeoLocation]], Variable] = Field(
        validation_alias="destinationGeoLocation", serialization_alias="destinationGeoLocation"
    )

    @classmethod
    def from_geo_locations_list(cls, locations: List[GeoLocation]) -> Self:
        return cls(destination_geo_loacation=Global[List[GeoLocation]](value=locations))


class SourceIdentityUser(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_user: Global[List[str]] = Field(
        validation_alias="sourceIdentityUser", serialization_alias="sourceIdentityUser"
    )


class SourceIdentityUserGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_identity_user_group: Global[List[str]] = Field(
        validation_alias="sourceIdentityUserGroup", serialization_alias="sourceIdentityUserGroup"
    )


class App(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app: Global[List[str]]


class AppFamily(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_family: Global[List[str]] = Field(validation_alias="appFamily", serialization_alias="appFamily")


class Protocol(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol: Global[List[str]]

    @classmethod
    def from_protocol_id_list(cls, ids: List[str]) -> Self:
        return cls(protocol=as_global(ids))


class ProtocolNameMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol_name: Global[List[ProtocolName]] = Field(
        validation_alias="protocolName", serialization_alias="protocolName"
    )

    @classmethod
    def from_protocol_name_list(cls, protocols: List[ProtocolName]) -> Self:
        return cls(protocol_name=Global[List[ProtocolName]](value=protocols))


MatchEntry = Union[
    App,
    AppFamily,
    AppList,
    AppListFlat,
    DestinationDataPrefixList,
    DestinationFqdn,
    DestinationFqdnList,
    DestinationGeoLocation,
    DestinationGeoLocationList,
    DestinationIp,
    DestinationPort,
    DestinationPortList,
    DestinationScalableGroupTagList,
    DestinationSecurityGroup,
    Protocol,
    ProtocolNameList,
    ProtocolNameMatch,
    RuleSetList,
    SourceDataPrefixList,
    SourceGeoLocation,
    SourceGeoLocationList,
    SourceIdentityList,
    SourceIdentityUser,
    SourceIdentityUserGroup,
    SourceIp,
    SourcePort,
    SourcePortList,
    SourceScalableGroupTagList,
    SourceSecurityGroup,
]


class AipAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type: Global[AipActionType] = Field(
        default=Global[AipActionType](value="advancedInspectionProfile"),
        validation_alias="type",
        serialization_alias="type",
    )
    parameter: RefIdItem

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(parameter=RefIdItem.from_uuid(uuid))


class LogAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type: Optional[Global[SequenceActionType]] = Field(default=None)
    parameter: Global[str] = Field(default=Global[str](value="true"))

    @classmethod
    def from_sequence_action(cls, action_type: SequenceActionType) -> Self:
        return cls(type=Global[SequenceActionType](value=action_type))


class Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    entries: List[MatchEntry]

    @classmethod
    def create(cls, entries: Optional[List[MatchEntry]] = None) -> Self:
        return cls(entries=entries if entries else [])


class NgFirewallSequence(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    sequence_id: Global[str] = Field(validation_alias="sequenceId", serialization_alias="sequenceId")
    sequence_name: Global[str] = Field(validation_alias="sequenceName", serialization_alias="sequenceName")
    base_action: Global[SecurityBaseAction] = Field(
        default=Global[SecurityBaseAction](value="drop"),
        validation_alias="baseAction",
        serialization_alias="baseAction",
    )
    sequence_type: Global[SequenceType] = Field(
        default=Global[SequenceType](value="ngfirewall"),
        validation_alias="sequenceType",
        serialization_alias="sequenceType",
    )
    match: Match
    actions: List[Union[LogAction, AipAction]] = Field(
        default_factory=list, validation_alias="actions", min_length=0, max_length=2, serialization_alias="actions"
    )
    disable_sequence: Global[bool] = Field(
        default=Global[bool](value=False),
        validation_alias="disableSequence",
        serialization_alias="disableSequence",
    )

    def add_log_action(self) -> None:
        self.actions.append(LogAction())

    def add_aip_action(self, aip_uuid: UUID) -> None:
        self.actions.append(AipAction.from_uuid(aip_uuid))

    @model_validator(mode="after")
    def validate_model(self):
        if len(self.actions) > len(set(map(type, self.actions))):
            raise ValidationError(
                f"NGFirewall sequence cannot contain actions with the same type. Sequence actions: {self.actions}"
            )

        return self

    @classmethod
    def create(
        cls,
        sequence_id: int,
        sequence_name: str,
        base_action: SecurityBaseAction,
        disable_sequence: bool = False,
        match: Optional[Match] = None,
        actions: Optional[List[Union[LogAction, AipAction]]] = None,
    ) -> Self:
        return cls(
            sequence_id=Global[str](value=str(sequence_id)),
            sequence_name=Global[str](value=sequence_name),
            base_action=Global[SecurityBaseAction](value=base_action),
            match=match if match else Match.create(),
            actions=actions if actions else [],
            disable_sequence=Global[bool](value=disable_sequence),
        )


class NgfirewallParcel(_ParcelBase):
    type_: Literal["unified/ngfirewall"] = Field(default="unified/ngfirewall", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    default_action_type: Global[DefaultAction] = Field(validation_alias=AliasPath("data", "defaultActionType"))
    sequences: List[NgFirewallSequence] = Field(validation_alias=AliasPath("data", "sequences"))
    contains_tls: Optional[bool] = Field(
        default=False, validation_alias="containsTls", serialization_alias="containsTls"
    )
    contains_utd: Optional[bool] = Field(
        default=False, validation_alias="containsUtd", serialization_alias="containsUtd"
    )
    optimized: Optional[bool] = Field(default=True)

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        default_action_type: DefaultAction,
        sequences: List[NgFirewallSequence],
        contains_tls: bool = False,
        contains_utd: bool = False,
    ) -> Self:
        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            default_action_type=Global[DefaultAction](value=default_action_type),
            sequences=sequences,
            contains_utd=contains_utd,
            contains_tls=contains_tls,
        )
