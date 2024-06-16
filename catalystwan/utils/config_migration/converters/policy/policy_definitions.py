# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type, Union, cast
from uuid import UUID

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.common import DeviceAccessProtocolPort, int_range_str_validator
from catalystwan.models.configuration.config_migration import (
    PolicyConvertContext,
    SslDecryptioneResidues,
    SslProfileResidues,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.dns_security.dns import DnsParcel, TargetVpns
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.aip import (
    AdvancedInspectionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.amp import (
    AdvancedMalwareProtectionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.intrusion_prevention import (
    IntrusionPreventionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption import (
    CaCertBundle,
    SslDecryptionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption_profile import (
    SslDecryptionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url_filtering import (
    BlockPageAction,
    UrlFilteringParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import (
    Criteria,
    Origin,
    Protocol,
    RoutePolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import DeviceAccessIPv4Parcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.policy import AnyPolicyDefinition
from catalystwan.models.policy.definition.access_control_list import AclPolicy
from catalystwan.models.policy.definition.access_control_list_ipv6 import AclIPv6Policy
from catalystwan.models.policy.definition.aip import AdvancedInspectionProfilePolicy
from catalystwan.models.policy.definition.amp import AdvancedMalwareProtectionPolicy
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.device_access import DeviceAccessPolicy
from catalystwan.models.policy.definition.device_access_ipv6 import DeviceAccessIPv6Policy
from catalystwan.models.policy.definition.dns_security import DnsSecurityPolicy, TargetVpn
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.intrusion_prevention import IntrusionPreventionPolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.models.policy.definition.route_policy import RoutePolicy
from catalystwan.models.policy.definition.ssl_decryption import SslDecryptionPolicy
from catalystwan.models.policy.definition.ssl_decryption_utd_profile import SslDecryptionUtdProfilePolicy
from catalystwan.models.policy.definition.url_filtering import UrlFilteringPolicy
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.utils import convert_varname

logger = logging.getLogger(__name__)

Input = AnyPolicyDefinition
Output = Optional[
    Annotated[
        Union[
            CustomControlParcel,
            HubSpokeParcel,
            MeshParcel,
            Ipv4AclParcel,
            Ipv6AclParcel,
            AdvancedInspectionProfileParcel,
            AdvancedMalwareProtectionParcel,
            IntrusionPreventionParcel,
            SslDecryptionParcel,
            SslDecryptionProfileParcel,
            UrlFilteringParcel,
            DnsParcel,
            DeviceAccessIPv6Parcel,
            DeviceAccessIPv4Parcel,
            RoutePolicyParcel,
        ],
        Field(discriminator="type_"),
    ]
]


def _get_parcel_name_desc(policy_definition: AnyPolicyDefinition) -> Dict[str, Any]:
    return dict(parcel_name=policy_definition.name, parcel_description=policy_definition.description)


def as_num_ranges_list(p: str) -> List[Union[int, Tuple[int, int]]]:
    """
    applicable to acl source/destination port list
    "1 2-5 6 7 20-22" -> [1 (2,5) 6 7 (20,22)]

    """
    num_list: List[Union[int, Tuple[int, int]]] = []
    for val in p.split():
        low, hi = int_range_str_validator(val, False)
        if hi is None:
            num_list.append(low)
        else:
            num_list.append((hi, low))
    return num_list


def as_num_list(ports_list: List[Union[int, Tuple[int, int]]]) -> List[int]:
    """
    applicable to device access port list
    [(30, 35), 80] -> [30 31 32 33 34 35 80]
    """
    num_list: List[int] = []
    for val in ports_list:
        if isinstance(val, int):
            num_list.append(val)
        elif isinstance(val, tuple):
            num_list.extend(range(val[1], val[0] + 1))
    num_list = sorted(list(set(num_list)))
    return num_list


def conditional_split(s: str, seps: List[str]) -> List[str]:
    """
    split s by first sep found in seps
    """
    for sep in seps:
        if sep in s:
            return s.split(sep)
    raise CatalystwanConverterCantConvertException(f"None of the separators {seps} found in {s}")


def advanced_malware_protection(
    in_: AdvancedMalwareProtectionPolicy, uuid: UUID, context: PolicyConvertContext
) -> AdvancedMalwareProtectionParcel:
    if not in_.definition.file_reputation_alert:
        raise CatalystwanConverterCantConvertException("AMP file reputation alert shall not be an empty str.")

    if vpn_list := in_.definition.target_vpns:
        context.amp_target_vpns_id[uuid] = vpn_list

    definition_dump = in_.definition.model_dump(exclude={"target_vpns"})
    return AdvancedMalwareProtectionParcel.create(**_get_parcel_name_desc(in_), **definition_dump)


def control(in_: ControlPolicy, uuid: UUID, context) -> CustomControlParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {ControlPolicy.__name__}")
    out = CustomControlParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def dns_security(in_: DnsSecurityPolicy, uuid: UUID, context: PolicyConvertContext) -> DnsParcel:
    vpn_id_to_map = context.get_vpn_id_to_vpn_name_map()

    if umbrella_data := in_.definition.umbrella_data:
        context.dns_security_umbrella_data[uuid] = umbrella_data.ref

    _target_vpns = (
        [target_vpn_convert(target_vpn, vpn_id_to_map) for target_vpn in in_.definition.target_vpns]
        if in_.definition.target_vpns
        else None
    )

    _local_domain_bypass_list = (
        in_.definition.local_domain_bypass_list.ref if in_.definition.local_domain_bypass_list else None
    )

    return DnsParcel.create(
        **_get_parcel_name_desc(in_),
        **in_.definition.model_dump(exclude={"local_domain_bypass_list", "umbrella_data", "target_vpns"}),
        target_vpns=_target_vpns,
        local_domain_bypass_list=_local_domain_bypass_list,
    )


def target_vpn_convert(target_vpn: TargetVpn, vpn_id_to_map: Dict[Union[str, int], List[str]]) -> TargetVpns:
    vpn_names = []
    for vpn in target_vpn.vpns:
        if not (mapped_name := vpn_id_to_map.get(vpn)):
            raise CatalystwanConverterCantConvertException(f"Cannot find the TargetVPN with id: {vpn}")

        vpn_names.extend(mapped_name)

    return TargetVpns.create(**target_vpn.model_dump(exclude={"vpns"}), vpns=vpn_names)


def hubspoke(in_: HubAndSpokePolicy, uuid: UUID, context: PolicyConvertContext) -> HubSpokeParcel:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
    out = HubSpokeParcel(**_get_parcel_name_desc(in_))
    out.target.vpn.value.extend(target_vpns)
    for isubdef in in_.definition.sub_definitions:
        osites: List[str] = []
        ohubs: List[str] = []
        for ispoke in isubdef.spokes:
            osites.extend(context.sites_by_list_id[ispoke.site_list])
            for ihub in ispoke.hubs:
                ohubs.extend(context.sites_by_list_id[ihub.site_list])
        ospoke = out.add_spoke(isubdef.name, list(set(osites)))
        ospoke.add_hub_site(list(set(ohubs)), 1)
        out.selected_hubs.value = list(set(ohubs))
    return out


def ipv4acl(in_: AclPolicy, uuid: UUID, context) -> Ipv4AclParcel:
    out = Ipv4AclParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        out_seq = out.add_sequence(name=in_seq.sequence_name, id=in_seq.sequence_id, base_action=in_seq.base_action)
        for in_entry in in_seq.match.entries:
            if in_entry.field == "destinationDataPrefixList" and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "destinationIp":
                if in_entry.vip_variable_name is not None:
                    varname = convert_varname(in_entry.vip_variable_name)
                    out_seq.match_destination_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_destination_data_prefix(IPv4Interface(in_entry.value))

            elif in_entry.field == "destinationPort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "dscp":
                out_seq.match_dscp([int(s) for s in in_entry.value.split()])

            elif in_entry.field == "packetLength":
                low, hi = int_range_str_validator(in_entry.value, False)
                if hi is None:
                    out_seq.match_packet_length(low)
                else:
                    out_seq.match_packet_length((low, hi))

            elif in_entry.field == "plp":
                logger.warning(
                    f"{Ipv4AclParcel.__name__} has no field matching plp found in {AclPolicy.__name__}: {in_.name}"
                )

            elif in_entry.field == "protocol":
                protocols: List[int] = []
                for val in in_entry.value.split():
                    low, hi = int_range_str_validator(val, False)
                    if hi is None:
                        protocols.append(low)
                    else:
                        protocols.extend(range(low, hi + 1))
                out_seq.match_protocol(protocols)

            elif in_entry.field == "sourceDataPrefixList" and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "sourceIp":
                if in_entry.vip_variable_name is not None:
                    varname = convert_varname(in_entry.vip_variable_name)
                    out_seq.match_source_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_source_data_prefix(IPv4Interface(in_entry.value))

            elif in_entry.field == "sourcePort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "tcp":
                out_seq.match_tcp()

    return out


def ipv6acl(in_: AclIPv6Policy, uuid: UUID, context) -> Ipv6AclParcel:
    out = Ipv6AclParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def device_access_ipv6(
    in_: DeviceAccessIPv6Policy, uuid: UUID, context: PolicyConvertContext
) -> DeviceAccessIPv6Parcel:
    out = DeviceAccessIPv6Parcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        port_str = next(e.value for e in in_seq.match.entries if e.field == "destinationPort")
        port = cast(DeviceAccessProtocolPort, int(port_str))
        seq = out.add_sequence(
            id=in_seq.sequence_id,
            name=in_seq.sequence_name,
            destination_port=port,
            base_action=in_seq.base_action,
        )
        for in_entry in in_seq.match.entries:
            if in_entry.field == "destinationDataIpv6PrefixList":
                if in_entry.ref:
                    seq.match_destination_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "destinationIpv6":
                d_network_ipv6 = conditional_split(in_entry.value, [",", " "])
                seq.match_destination_data_prefixes([IPv6Interface(v) for v in d_network_ipv6])
            elif in_entry.field == "destinationPort":
                destination_port = cast(DeviceAccessProtocolPort, int(in_entry.value))
                seq.match_destination_port(destination_port)
            elif in_entry.field == "sourceDataIpv6PrefixList":
                if in_entry.ref:
                    seq.match_source_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "sourceIpv6":
                s_network_ipv6 = conditional_split(in_entry.value, [",", " "])
                seq.match_source_data_prefixes([IPv6Interface(v) for v in s_network_ipv6])
            elif in_entry.field == "sourcePort":
                seq.match_source_ports(as_num_list(as_num_ranges_list(in_entry.value)))
    return out


def device_access_ipv4(in_: DeviceAccessPolicy, uuid: UUID, context: PolicyConvertContext) -> DeviceAccessIPv4Parcel:
    out = DeviceAccessIPv4Parcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        port_str = next(e.value for e in in_seq.match.entries if e.field == "destinationPort")
        port = cast(DeviceAccessProtocolPort, int(port_str))
        seq = out.add_sequence(
            id=in_seq.sequence_id,
            name=in_seq.sequence_name,
            destination_port=port,
            base_action=in_seq.base_action,
        )
        for in_entry in in_seq.match.entries:
            if in_entry.field == "destinationDataPrefixList":
                if in_entry.ref:
                    seq.match_destination_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "destinationIp":
                if in_entry.value is not None:
                    d_network_ipv6 = conditional_split(in_entry.value, [",", " "])
                    seq.match_destination_data_prefixes([IPv4Interface(v) for v in d_network_ipv6])
                elif in_entry.vip_variable_name is not None:
                    seq.match_destination_data_prefix_variable(in_entry.vip_variable_name)
            elif in_entry.field == "sourceDataPrefixList":
                if in_entry.ref:
                    seq.match_source_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "sourceIp":
                if in_entry.value is not None:
                    s_network_ipv6 = conditional_split(in_entry.value, [",", " "])
                    seq.match_source_data_prefixes([IPv4Interface(v) for v in s_network_ipv6])
                elif in_entry.vip_variable_name is not None:
                    seq.match_source_data_prefix_variable(in_entry.vip_variable_name)
            elif in_entry.field == "sourcePort":
                seq.match_source_ports(as_num_list(as_num_ranges_list(in_entry.value)))
    return out


def route(in_: RoutePolicy, uuid: UUID, context: PolicyConvertContext) -> RoutePolicyParcel:
    out = RoutePolicyParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        sequence_ip_type = in_seq.sequence_ip_type
        if sequence_ip_type is not None:
            protocol = "BOTH" if sequence_ip_type == "all" else sequence_ip_type.upper()
        out_seq = out.add_sequence(
            id_=in_seq.sequence_id,
            name=in_seq.sequence_name,
            base_action=in_seq.base_action,
            protocol=cast(Protocol, protocol),
        )

        for in_entry in in_seq.match.entries:
            if in_entry.field == "asPath":
                out_seq.match_as_path_list(in_entry.ref)
            elif in_entry.field == "expandedCommunity":
                out_seq.match_community_list(expanded_community_list=in_entry.ref)
            elif in_entry.field == "advancedCommunity":
                # Advanced matches to standard, because it has a list of UUIDs and a match flag
                out_seq.match_community_list(
                    standard_community_list=in_entry.refs, criteria=cast(Criteria, in_entry.match_flag.upper())
                )
            elif in_entry.field == "extCommunity":
                out_seq.match_ext_community_list(in_entry.ref)
            elif in_entry.field == "localPreference":
                # Local preference is matches to bgp
                out_seq.match_bgp_local_preference(in_entry.value)
            elif in_entry.field == "metric":
                out_seq.match_metric(in_entry.value)
            elif in_entry.field == "ompTag":
                out_seq.match_omp_tag(in_entry.value)
            elif in_entry.field == "ospfTag":
                out_seq.match_ospf_tag(in_entry.value)
            elif in_entry.field == "address":
                if sequence_ip_type == "ipv4":
                    out_seq.match_ipv4_address(in_entry.ref)
                elif sequence_ip_type == "ipv6":
                    out_seq.match_ipv6_address(in_entry.ref)
            elif in_entry.field == "nextHop":
                if sequence_ip_type == "ipv4":
                    out_seq.match_ipv4_next_hop(in_entry.ref)
                elif sequence_ip_type == "ipv6":
                    out_seq.match_ipv6_next_hop(in_entry.ref)

        community_additive = any(
            [action.value for action in in_seq.actions[0].parameter if action.field == "communityAdditive"]
        )

        for in_action in in_seq.actions[0].parameter:
            if in_action.field == "asPath":
                out_seq.associate_as_path_action(in_action.value.prepend)
            elif in_action.field == "community":
                if in_action.value:
                    out_seq.associate_community_action(community_additive, in_action.value)
                if in_action.vip_variable_name:
                    out_seq.associate_community_variable_action(community_additive, in_action.vip_variable_name)
            elif in_action.field == "localPreference":
                out_seq.associate_local_preference_action(in_action.value)
            elif in_action.field == "metric":
                out_seq.associate_metric_action(in_action.value)
            elif in_action.field == "metricType":
                out_seq.associate_metric_type_action(in_action.value)
            elif in_action.field == "ospfTag":
                out_seq.associate_ospf_tag_action(in_action.value)
            elif in_action.field == "origin":
                origin = "Incomplete" if in_action.value == "incomplete" else in_action.value.upper()
                out_seq.associate_origin_action(cast(Origin, origin))
            elif in_action.field == "ompTag":
                out_seq.associate_omp_tag_action(in_action.value)
            elif in_action.field == "weight":
                out_seq.associate_weight_action(in_action.value)
            elif in_action.field == "nextHop":
                if isinstance(in_action.value, IPv4Address):
                    out_seq.associate_ipv4_next_hop_action(in_action.value)
                if isinstance(in_action.value, IPv6Address):
                    out_seq.associate_ipv6_next_hop_action(in_action.value)
    return out


def mesh(in_: MeshPolicy, uuid: UUID, context: PolicyConvertContext) -> MeshParcel:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
    mesh_sites: List[str] = []
    for region in in_.definition.regions:
        for site_list in region.site_lists:
            mesh_sites.extend(context.sites_by_list_id[site_list])
    out = MeshParcel(**_get_parcel_name_desc(in_))
    out.target.vpn.value = target_vpns
    out.sites.value = mesh_sites
    return out


def ssl_decryption(in_: SslDecryptionPolicy, uuid: UUID, context: PolicyConvertContext) -> SslDecryptionParcel:
    definition_dump = in_.definition.settings.model_dump(
        exclude={"certificate_lifetime", "ca_cert_bundle", "unknown_status"}
    )
    certificate_lifetime = str(in_.definition.settings.certificate_lifetime)
    ca_cert_bundle = CaCertBundle.create(**in_.definition.settings.ca_cert_bundle.model_dump())
    unknown_status = (
        in_.definition.settings.unknown_status
        if in_.definition.settings.certificate_revocation_status != "none"
        else None
    )

    if in_.definition.sequences or in_.definition.profiles:
        context.ssl_decryption_residues[uuid] = SslDecryptioneResidues(
            sequences=in_.definition.sequences, profiles=in_.definition.profiles
        )

    return SslDecryptionParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        ca_cert_bundle=ca_cert_bundle,
        certificate_lifetime=certificate_lifetime,
        unknown_status=unknown_status,
    )


def ssl_profile(
    in_: SslDecryptionUtdProfilePolicy, uuid: UUID, context: PolicyConvertContext
) -> SslDecryptionProfileParcel:
    definition_dump = in_.definition.model_dump(
        exclude={"filtered_url_white_list", "filtered_url_black_list", "url_white_list", "url_black_list"}
    )

    url_allowed_list = in_.definition.url_white_list.ref if in_.definition.url_white_list else None
    url_blocked_list = in_.definition.url_black_list.ref if in_.definition.url_black_list else None

    if in_.definition.filtered_url_black_list or in_.definition.filtered_url_white_list:
        context.ssl_profile_residues[uuid] = SslProfileResidues(
            filtered_url_black_list=in_.definition.filtered_url_black_list,
            filtered_url_white_list=in_.definition.filtered_url_white_list,
        )

    return SslDecryptionProfileParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        url_allowed_list=url_allowed_list,
        url_blocked_list=url_blocked_list,
    )


def advanced_inspection_profile(
    in_: AdvancedInspectionProfilePolicy, uuid: UUID, context: PolicyConvertContext
) -> AdvancedInspectionProfileParcel:
    intrusion_prevention_ref = in_.definition.intrusion_prevention.ref if in_.definition.intrusion_prevention else None
    url_filtering_ref = in_.definition.url_filtering.ref if in_.definition.url_filtering else None
    advanced_malware_protection_ref = (
        in_.definition.advanced_malware_protection.ref if in_.definition.advanced_malware_protection else None
    )
    ssl_decryption_profile_ref = (
        in_.definition.ssl_utd_decrypt_profile.ref if in_.definition.ssl_utd_decrypt_profile else None
    )

    return AdvancedInspectionProfileParcel.create(
        **_get_parcel_name_desc(in_),
        tls_decryption_action=in_.definition.tls_decryption_action,
        intrusion_prevention=intrusion_prevention_ref,
        url_filtering=url_filtering_ref,
        advanced_malware_protection=advanced_malware_protection_ref,
        ssl_decryption_profile=ssl_decryption_profile_ref,
    )


def url_filtering(in_: UrlFilteringPolicy, uuid: UUID, context: PolicyConvertContext) -> UrlFilteringParcel:
    block_page_action_map: Dict[str, BlockPageAction] = {"text": "text", "redirectUrl": "redirect-url"}
    definition_dump = in_.definition.model_dump(
        exclude={"target_vpns", "url_white_list", "url_black_list", "logging", "block_page_action"}
    )

    if vpns := in_.definition.target_vpns:
        context.url_filtering_target_vpns[uuid] = vpns

    block_page_action = block_page_action_map[in_.definition.block_page_action]
    # below references are a references to v1 objects,
    # during push the references shall be transformed to point v2 objects
    url_allowed_list = (
        RefIdItem(ref_id=as_global(str(in_.definition.url_white_list.ref))) if in_.definition.url_white_list else None
    )
    url_blocked_list = (
        RefIdItem(ref_id=as_global(str(in_.definition.url_black_list.ref))) if in_.definition.url_black_list else None
    )

    out = UrlFilteringParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        block_page_action=block_page_action,
        url_allowed_list=url_allowed_list,
        url_blocked_list=url_blocked_list,
    )
    return out


def intrusion_prevention(
    in_: IntrusionPreventionPolicy, uuid: UUID, context: PolicyConvertContext
) -> IntrusionPreventionParcel:
    if vpn_list := in_.definition.target_vpns:
        context.intrusion_prevention_target_vpns_id[uuid] = vpn_list

    definition_dump = in_.definition.model_dump(exclude={"target_vpns", "logging"})
    signature_white_list = definition_dump.pop("signature_white_list", None)
    signature_allowed_list = signature_white_list.get("ref") if signature_white_list else None

    return IntrusionPreventionParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        signature_allowed_list=signature_allowed_list,
    )


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AclPolicy: ipv4acl,
    AclIPv6Policy: ipv6acl,
    ControlPolicy: control,
    HubAndSpokePolicy: hubspoke,
    MeshPolicy: mesh,
    AdvancedInspectionProfilePolicy: advanced_inspection_profile,
    AdvancedMalwareProtectionPolicy: advanced_malware_protection,
    IntrusionPreventionPolicy: intrusion_prevention,
    SslDecryptionPolicy: ssl_decryption,
    SslDecryptionUtdProfilePolicy: ssl_profile,
    UrlFilteringPolicy: url_filtering,
    DnsSecurityPolicy: dns_security,
    DeviceAccessIPv6Policy: device_access_ipv6,
    DeviceAccessPolicy: device_access_ipv4,
    RoutePolicy: route,
}


def _not_supported(in_: Input, *args, **kwargs) -> None:
    logger.warning(f"Not Supported Conversion of Policy Definition: '{in_.type}' '{in_.name}'")


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    return _not_supported


def convert(in_: Input, uuid: UUID, context: PolicyConvertContext) -> Output:
    result = _find_converter(in_)(in_, uuid, context)
    if result is not None:
        result.model_validate(result)
    return result
