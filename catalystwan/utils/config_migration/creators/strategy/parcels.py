from typing import List
from uuid import UUID

from catalystwan.models.configuration.config_migration import TransformedParcel
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.session import ManagerSession


class ParcelPusher:
    """
    Base class for pushing parcels to a feature profile.
    """

    def __init__(self, session: ManagerSession, profile_type: ProfileType):
        self.builder = session.api.builders.feature_profiles.create_builder(profile_type)

    def push(self, feature_profile: FeatureProfileCreationPayload, parcels: List[TransformedParcel]) -> UUID:
        raise NotImplementedError


class SimpleParcelPusher(ParcelPusher):
    """
    Simple implementation of ParcelPusher that creates parcels directly.
    Includes: Other and System feature profiles.
    """

    def push(self, feature_profile: FeatureProfileCreationPayload, parcels: List[TransformedParcel]) -> UUID:
        # Parcels don't have references to other parcels, so we can create them directly
        for transformed_parcel in parcels:
            self.builder.add_parcel(transformed_parcel.parcel)  # type: ignore
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()


class ServiceParcelPusher(ParcelPusher):
    """
    Parcel pusher for service feature profiles.
    """

    def push(self, feature_profile: FeatureProfileCreationPayload, parcels: List[TransformedParcel]) -> UUID:
        # Service feature profiles have references to other parcels, so we need to create them in order
        self._move_vpn_parcel_to_first_position(parcels)
        for transformed_parcel in parcels:
            self._resolve_and_add_parcel(transformed_parcel)
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()

    def _resolve_and_add_parcel(self, transformed_parcel: TransformedParcel) -> None:
        parcel = transformed_parcel.parcel
        if isinstance(parcel, LanVpnParcel):
            self.builder.add_parcel_vpn(parcel)  # type: ignore
        elif isinstance(
            parcel, (InterfaceEthernetParcel, InterfaceGreParcel, InterfaceIpsecParcel, InterfaceSviParcel)
        ):
            # TODO: Assiging logic
            # Every Service VPN parcel can have interface childs and
            # there can be multiple service VPNs in one feature profile
            pass
        else:
            self.builder.add_parcel(parcel)  # type: ignore

    def _move_vpn_parcel_to_first_position(self, parcels: List[TransformedParcel]) -> None:
        """Move the VPN parcel to the first position in the list.
        Without this there is posibility to add_parcel_vpn_interface with None tag."""
        parcels.sort(key=lambda x: x.parcel._get_parcel_type() == "lan/vpn", reverse=True)