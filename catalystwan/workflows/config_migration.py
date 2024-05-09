# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from collections import defaultdict
from typing import Callable
from uuid import UUID, uuid4

from catalystwan.api.policy_api import POLICY_LIST_ENDPOINTS_MAP
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.models.configuration.config_migration import (
    DeviceTemplateWithInfo,
    TransformedConfigGroup,
    TransformedFeatureProfile,
    TransformedParcel,
    TransformHeader,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.converters.feature_template import create_parcel_from_template
from catalystwan.utils.config_migration.converters.policy.policy_lists import PolicyListConversionError
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert as convert_policy_list
from catalystwan.utils.config_migration.creators.config_pusher import UX2ConfigPusher, UX2ConfigRollback
from catalystwan.utils.config_migration.reverters.config_reverter import UX2ConfigReverter
from catalystwan.utils.config_migration.steps.transform import (
    CISCO_VPN_SERVICE,
    CISCO_VPN_TRANSPORT_AND_MANAGEMENT,
    merge_parcels,
    resolve_template_type,
)

logger = logging.getLogger(__name__)

SUPPORTED_TEMPLATE_TYPES = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    # "cisco_bfd",
    # "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    # "bgp",
    # "cisco_bgp",
    "cisco_thousandeyes",
    "ucse",
    "dhcp",
    "cisco_dhcp_server",
    "cisco_vpn",
    "cisco_vpn_interface_gre",
    "vpn-vsmart-interface",
    "vpn-vedge-interface",
    "vpn-vmanage-interface",
    "cisco_vpn_interface",
    "cisco_vpn_interface_ipsec",
    "vpn-interface-svi",
    "cisco_ospf",
    "switchport",
    "cisco_wireless_lan",
    "cisco_multicast",
    "cisco_pim",
    "cisco_igmp",
    "cisco_IGMP",
    "igmp",
    "pim",
    "multicast",
    "cedge_igmp",
    "cedge_multicast",
    "cedge_pim",
    "vpn-interface-t1-e1",
    "vpn-interface-ethpppoe",
    "vpn-interface-pppoe",
    "vpn-interface-pppoa",
    "vpn-interface-ipoe",
]

FEATURE_PROFILE_SYSTEM = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    # "cisco_bfd",
    # "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    # "bgp",
    # "cisco_bgp",
    "cisco_snmp",
]

FEATURE_PROFILE_TRANSPORT = [
    "dhcp",
    "cisco_dhcp_server",
    "dhcp-server",
    "vpn-interface-t1-e1",
    "vpn-interface-ethpppoe",
    "vpn-interface-pppoe",
    "vpn-interface-pppoa",
    "vpn-interface-ipoe",
    CISCO_VPN_TRANSPORT_AND_MANAGEMENT,
]

FEATURE_PROFILE_OTHER = [
    "cisco_thousandeyes",
    "ucse",
]

FEATURE_PROFILE_SERVICE = [
    "cisco_vpn_interface_gre",
    "vpn-vsmart-interface",
    "vpn-vedge-interface",
    "vpn-vmanage-interface",
    "cisco_vpn_interface",
    "cisco_vpn_interface_ipsec",
    "vpn-interface-svi",
    "cisco_ospf",
    "switchport",
    "cisco_wireless_lan",
    "cisco_multicast",
    "cisco_pim",
    "cisco_igmp",
    "cisco_IGMP",
    "igmp",
    "pim",
    "multicast",
    "cedge_igmp",
    "cedge_multicast",
    "cedge_pim",
    CISCO_VPN_SERVICE,
]


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info(f"{task} {completed}/{total}")


def transform(ux1: UX1Config) -> UX2Config:
    ux2 = UX2Config()
    subtemplates_mapping = defaultdict(set)
    # Create Feature Profiles and Config Group
    for dt in ux1.templates.device_templates:
        templates = dt.get_flattened_general_templates()
        # Create Feature Profiles
        fp_system_uuid = uuid4()
        transformed_fp_system = TransformedFeatureProfile(
            header=TransformHeader(
                type="system",
                origin=fp_system_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_system",
                description="system",
            ),
        )
        fp_other_uuid = uuid4()
        transformed_fp_other = TransformedFeatureProfile(
            header=TransformHeader(
                type="other",
                origin=fp_other_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_other",
                description="other",
            ),
        )
        fp_service_uuid = uuid4()
        transformed_fp_service = TransformedFeatureProfile(
            header=TransformHeader(
                type="service",
                origin=fp_service_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_service",
                description="service",
            ),
        )
        fp_transport_and_management_uuid = uuid4()
        transformed_fp_transport_and_management = TransformedFeatureProfile(
            header=TransformHeader(
                type="transport",
                origin=fp_transport_and_management_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_transport_and_management",
                description="transport_and_management",
            ),
        )

        for template in templates:
            # Those feature templates IDs are real UUIDs and are used to map to the feature profiles
            if template.templateType == "cisco_vpn":
                resolve_template_type(template, ux1)
            template_uuid = UUID(template.templateId)
            if template.templateType in FEATURE_PROFILE_SYSTEM:
                transformed_fp_system.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_OTHER:
                transformed_fp_other.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_SERVICE:
                transformed_fp_service.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_TRANSPORT:
                transformed_fp_transport_and_management.header.subelements.add(template_uuid)
            # Map subtemplates
            if len(template.subTemplates) > 0:
                subtemplates_mapping[template_uuid] = set(
                    [UUID(subtemplate.templateId) for subtemplate in template.subTemplates]
                )

        transformed_cg = TransformedConfigGroup(
            header=TransformHeader(
                type="config_group",
                origin=UUID(dt.template_id),
                subelements=set([fp_system_uuid, fp_other_uuid, fp_service_uuid, fp_transport_and_management_uuid]),
            ),
            config_group=ConfigGroupCreationPayload(
                name=dt.template_name,
                description=dt.template_description,
                solution="sdwan",
                profiles=[],
            ),
        )
        # Add to UX2
        ux2.feature_profiles.append(transformed_fp_system)
        ux2.feature_profiles.append(transformed_fp_other)
        ux2.feature_profiles.append(transformed_fp_service)
        ux2.feature_profiles.append(transformed_fp_transport_and_management)
        ux2.config_groups.append(transformed_cg)

    for ft in ux1.templates.feature_templates:
        if ft.template_type in SUPPORTED_TEMPLATE_TYPES:
            parcel = create_parcel_from_template(ft)
            ft_template_uuid = UUID(ft.id)
            transformed_parcel = TransformedParcel(
                header=TransformHeader(
                    type=parcel._get_parcel_type(),
                    origin=ft_template_uuid,
                    subelements=subtemplates_mapping[ft_template_uuid],
                ),
                parcel=parcel,
            )
            # Add to UX2. We can indentify the parcels as subelements of the feature profiles by the UUIDs
            ux2.profile_parcels.append(transformed_parcel)

    # Policy Lists
    for policy_list in ux1.policies.policy_lists:
        try:
            policy_parcel = convert_policy_list(policy_list)
            header = TransformHeader(type=policy_parcel._get_parcel_type(), origin=policy_list.list_id)
            ux2.profile_parcels.append(TransformedParcel(header=header, parcel=policy_parcel))
        except PolicyListConversionError as e:
            logger.warning(f"{policy_list.type} {policy_list.list_id} {policy_list.name} was not converted: {e}")

    ux2 = merge_parcels(ux2)
    return ux2


def collect_ux1_config(session: ManagerSession, progress: Callable[[str, int, int], None] = log_progress) -> UX1Config:
    ux1 = UX1Config()

    """Collect Policies"""
    policy_api = session.api.policy

    progress("Collecting Policy Info", 0, 1)
    policy_definition_types_and_ids = [
        (policy_type, info.definition_id) for policy_type, info in policy_api.definitions.get_all()
    ]
    progress("Collecting Policy Info", 1, 1)

    policy_list_types = POLICY_LIST_ENDPOINTS_MAP.keys()
    for i, policy_list_type in enumerate(policy_list_types):
        ux1.policies.policy_lists.extend(policy_api.lists.get(policy_list_type))
        progress("Collecting Policy Lists", i + 1, len(policy_list_types))

    for i, type_and_id in enumerate(policy_definition_types_and_ids):
        ux1.policies.policy_definitions.append(policy_api.definitions.get(*type_and_id))
        progress("Collecting Policy Definitions", i + 1, len(policy_definition_types_and_ids))

    progress("Collecting Centralized Policies", 0, 1)
    ux1.policies.centralized_policies = policy_api.centralized.get().data
    progress("Collecting Centralized Policies", 1, 1)

    progress("Collecting Localized Policies", 0, 1)
    ux1.policies.localized_policies = policy_api.localized.get().data
    progress("Collecting Localized Policies", 1, 1)

    progress("Collecting Security Policies", 0, 1)
    ux1.policies.security_policies = policy_api.security.get().root
    progress("Collecting Security Policies", 1, 1)

    """Collect Templates"""
    template_api = session.api.templates

    progress("Collecting Feature Templates", 0, 1)
    ux1.templates.feature_templates = [t for t in template_api.get_feature_templates()]
    progress("Collecting Feature Templates", 1, 1)

    device_templates_information = template_api.get_device_templates()
    for i, device_template_information in enumerate(device_templates_information):
        device_template = template_api.get_device_template(device_template_information.id)
        device_template_with_info = DeviceTemplateWithInfo.from_merged(device_template, device_template_information)
        ux1.templates.device_templates.append(device_template_with_info)
        progress("Collecting Device Templates", i + 1, len(device_templates_information))

    return ux1


def push_ux2_config(
    session: ManagerSession, config: UX2Config, progress: Callable[[str, int, int], None] = log_progress
) -> UX2ConfigRollback:
    config_pusher = UX2ConfigPusher(session, config, progress)
    rollback = config_pusher.push()
    return rollback


def rollback_ux2_config(
    session: ManagerSession,
    rollback_config: UX2ConfigRollback,
    progress: Callable[[str, int, int], None] = log_progress,
) -> bool:
    config_reverter = UX2ConfigReverter(session)
    status = config_reverter.rollback(rollback_config, progress)
    return status
