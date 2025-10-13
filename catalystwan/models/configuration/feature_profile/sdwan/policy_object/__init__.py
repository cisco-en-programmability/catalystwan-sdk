# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy.app_probe import AppProbeMapItem, AppProbeParcel
from .policy.application_list import ApplicationFamilyListEntry, ApplicationListEntry, ApplicationListParcel
from .policy.as_path import AsPathParcel
from .policy.color_list import ColorEntry, ColorParcel
from .policy.data_prefix import DataPrefixEntry, DataPrefixParcel
from .policy.expanded_community_list import ExpandedCommunityParcel
from .policy.extended_community import ExtendedCommunityParcel
from .policy.fowarding_class import FowardingClassParcel, FowardingClassQueueEntry
from .policy.ipv6_data_prefix import IPv6DataPrefixEntry, IPv6DataPrefixParcel
from .policy.ipv6_prefix_list import IPv6PrefixListEntry, IPv6PrefixListParcel
from .policy.mirror import MirrorParcel
from .policy.policer import PolicerEntry, PolicerParcel
from .policy.prefered_group_color import Preference, PreferredColorGroupEntry, PreferredColorGroupParcel
from .policy.prefix_list import PrefixListEntry, PrefixListParcel
from .policy.service_object_group import ServiceObjectGroupParcel
from .policy.sla_class import SLAClassListEntry, SLAClassParcel
from .policy.standard_community import StandardCommunityEntry, StandardCommunityParcel
from .policy.tloc_list import TlocEntry, TlocParcel
from .security.aip import AdvancedInspectionProfileParcel
from .security.amp import AdvancedMalwareProtectionParcel
from .security.application_list import (
    SecurityApplicationFamilyListEntry,
    SecurityApplicationListEntry,
    SecurityApplicationListParcel,
)
from .security.data_prefix import SecurityDataPrefixEntry, SecurityDataPrefixParcel
from .security.fqdn import FQDNDomainParcel, FQDNListEntry
from .security.geolocation_list import GeoLocationListEntry, GeoLocationListParcel
from .security.identity import IdentityEntry, IdentityParcel
from .security.intrusion_prevention import IntrusionPreventionParcel
from .security.ips_signature import IPSSignatureListEntry, IPSSignatureParcel
from .security.local_domain import LocalDomainListEntry, LocalDomainParcel
from .security.object_group import SecurityObjectGroupEntries, SecurityObjectGroupParcel
from .security.protocol_list import ProtocolListEntry, ProtocolListParcel
from .security.scalable_group_tag import ScalableGroupTagEntry, ScalableGroupTagParcel
from .security.security_port import SecurityPortListEntry, SecurityPortParcel
from .security.ssl_decryption import SslDecryptionParcel
from .security.ssl_decryption_profile import SslDecryptionProfileParcel
from .security.url import BaseURLListEntry, URLAllowParcel, URLBlockParcel, URLParcel
from .security.url_filtering import UrlFilteringParcel
from .security.zone import SecurityZoneListEntry, SecurityZoneListParcel

AnyPolicyObjectParcel = Annotated[
    Union[
        AdvancedInspectionProfileParcel,
        AdvancedMalwareProtectionParcel,
        AppProbeParcel,
        ApplicationListParcel,
        AsPathParcel,
        ColorParcel,
        DataPrefixParcel,
        ExpandedCommunityParcel,
        ExtendedCommunityParcel,
        FQDNDomainParcel,
        FowardingClassParcel,
        GeoLocationListParcel,
        IPSSignatureParcel,
        IPv6DataPrefixParcel,
        IPv6PrefixListParcel,
        IdentityParcel,
        IntrusionPreventionParcel,
        LocalDomainParcel,
        MirrorParcel,
        PolicerParcel,
        PreferredColorGroupParcel,
        PrefixListParcel,
        ProtocolListParcel,
        SLAClassParcel,
        ScalableGroupTagParcel,
        SecurityApplicationListParcel,
        SecurityDataPrefixParcel,
        SecurityPortParcel,
        SecurityZoneListParcel,
        ServiceObjectGroupParcel,
        SslDecryptionParcel,
        SslDecryptionProfileParcel,
        StandardCommunityParcel,
        TlocParcel,
        URLParcel,
        UrlFilteringParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AdvancedInspectionProfileParcel",
    "AdvancedMalwareProtectionParcel",
    "AnyPolicyObjectParcel",
    "ApplicationFamilyListEntry",
    "ApplicationListEntry",
    "ApplicationListParcel",
    "AppProbeEntry",
    "AppProbeMapItem",
    "AppProbeParcel",
    "AsPathParcel",
    "BaseURLListEntry",
    "ColorEntry",
    "ColorParcel",
    "DataPrefixEntry",
    "DataPrefixParcel",
    "ExpandedCommunityParcel",
    "ExtendedCommunityParcel",
    "FallbackBestTunnel",
    "FowardingClassParcel",
    "FowardingClassQueueEntry",
    "FQDNDomainParcel",
    "FQDNListEntry",
    "GeoLocationListEntry",
    "GeoLocationListParcel",
    "IdentityEntry",
    "IdentityEntry",
    "IdentityParcel",
    "IdentityParcel",
    "IntrusionPreventionParcel",
    "IPSSignatureListEntry",
    "IPSSignatureParcel",
    "IPv6DataPrefixEntry",
    "IPv6DataPrefixParcel",
    "IPv6PrefixListEntry",
    "IPv6PrefixListParcel",
    "LocalDomainListEntry",
    "LocalDomainParcel",
    "MirrorParcel",
    "PolicerEntry",
    "PolicerParcel",
    "Preference",
    "PreferredColorGroupEntry",
    "PreferredColorGroupParcel",
    "PrefixListEntry",
    "PrefixListParcel",
    "ProtocolListEntry",
    "ProtocolListParcel",
    "ScalableGroupTagEntry",
    "ScalableGroupTagParcel",
    "ServiceObjectGroupParcel",
    "SecurityApplicationFamilyListEntry",
    "SecurityApplicationListEntry",
    "SecurityApplicationListParcel",
    "SecurityDataPrefixEntry",
    "SecurityDataPrefixParcel",
    "SecurityObjectGroupEntries",
    "SecurityObjectGroupParcel",
    "SecurityPortListEntry",
    "SecurityPortParcel",
    "SecurityZoneListEntry",
    "SecurityZoneListParcel",
    "SLAAppProbeClass",
    "SLAClassCriteria",
    "SLAClassListEntry",
    "SLAClassParcel",
    "SslDecryptionParcel",
    "SslDecryptionProfileParcel",
    "StandardCommunityEntry",
    "StandardCommunityParcel",
    "TlocEntry",
    "TlocParcel",
    "URLAllowParcel",
    "URLBlockParcel",
    "URLParcel",
)


def __dir__() -> "List[str]":
    return list(__all__)
