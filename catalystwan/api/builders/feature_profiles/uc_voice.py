# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Union
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.configuration_groups.parcel import as_default
from catalystwan.api.feature_profile_api import UcVoiceFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.uc_voice import UcVoiceFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import (
    AnalogInterfaceParcel,
    AnyUcVoiceParcel,
    CallRoutingParcel,
    DigitalInterfaceParcel,
    MediaProfileParcel,
    ServerGroupParcel,
    SrstParcel,
    TranslationProfileParcel,
    TranslationRuleParcel,
    TrunkGroupParcel,
    VoiceGlobalParcel,
    VoiceTenantParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.analog_interface import (
    Association as AnalogInterfaceAssociation,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.call_routing import (
    Association as CallRoutingAssociation,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.digital_interface import (
    Association as DigitalInterfaceAssociation,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


ParcelWithAssociations = Union[CallRoutingParcel, DigitalInterfaceParcel, AnalogInterfaceParcel]
Association = Union[List[DigitalInterfaceAssociation], List[AnalogInterfaceAssociation], List[CallRoutingAssociation]]


@dataclass
class TranslationProfile:
    tpp: TranslationProfileParcel
    calling: Optional[TranslationRuleParcel] = None
    called: Optional[TranslationRuleParcel] = None


def is_uuid(uuid: Optional[Union[str, UUID]]) -> bool:
    if isinstance(uuid, UUID) or uuid is None:
        return True
    try:
        UUID(uuid)
        return True
    except ValueError:
        return False


class UcVoiceFeatureProfileBuilder:
    """
    A class for building UC Voice feature profiles with a modular approach.

    This class provides methods to construct, associate, and manage various parcels and
    configurations required for UC Voice feature profiles.
    """

    ASSOCIABLE_PARCELS = (
        MediaProfileParcel,
        ServerGroupParcel,
        SrstParcel,
        TranslationProfileParcel,
        TranslationRuleParcel,
        TrunkGroupParcel,
        VoiceGlobalParcel,
        VoiceTenantParcel,
    )

    ASSOCIATON_FIELDS = {
        "media_profile",
        "server_group",
        "translation_profile",
        "trunk_group",
        "voice_tenant",
        "supervisory_disconnect",
    }

    def __init__(self, session: ManagerSession) -> None:
        """
        Initializes a new instance of the UC Voice Feature Profile Builder.

        Args:
            session (ManagerSession): The session object used for API communication.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = UcVoiceFeatureProfileAPI(session)
        self._endpoints = UcVoiceFeatureProfile(session)
        self._independent_parcels: List[AnyUcVoiceParcel] = []
        self._translation_profiles: List[TranslationProfile] = []
        self._pushed_associable_parcels: Dict[str, UUID] = {}  # Maps parcel names to their created UUIDs.
        self._parcels_with_associations: List[ParcelWithAssociations] = []

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile being built.

        Args:
            feature_profile (FeatureProfileCreationPayload): The feature profile payload containing
                the name and description.
        """
        self._profile = feature_profile

    def add_independent_parcel(self, parcel: AnyUcVoiceParcel) -> None:
        """
        Adds an independent parcel to the feature profile.

        Args:
            parcel (AnyUcVoiceParcel): The parcel to be added. Parcels are independent configurations
                that do not require associations with other parcels.
        """
        self._independent_parcels.append(parcel)

    def add_translation_profile(
        self,
        tpp: TranslationProfileParcel,
        calling: Optional[TranslationRuleParcel] = None,
        called: Optional[TranslationRuleParcel] = None,
    ) -> None:
        """
        Adds a translation profile to the feature profile.

        Args:
            tpp (TranslationProfileParcel): The main translation profile parcel.
            calling (Optional[TranslationRuleParcel]): The calling rule parcel. Optional.
            called (Optional[TranslationRuleParcel]): The called rule parcel. Optional.

        Raises:
            ValueError: If neither a calling nor a called rule is provided.
        """
        if not calling and not called:
            raise ValueError("There must be at least one translation rule to create a translation profile.")
        self._translation_profiles.append(TranslationProfile(tpp=tpp, called=called, calling=calling))

    def add_parcel_with_associations(self, parcel: ParcelWithAssociations) -> None:
        """
        Adds a parcel with associations to the feature profile.

        Args:
            parcel (ParcelWithAssociations): A parcel that includes associations with other entities.
                Associations are relationships between parcels and other resources.
        """
        self._parcels_with_associations.append(parcel)

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the complete UC Voice feature profile.

        This method creates the feature profile on the system and processes all added parcels
        and translation profiles, resolving associations as needed.

        Returns:
            FeatureProfileBuildReport: A report containing the details of the created feature profile.
        """
        profile_uuid = self._endpoints.create_uc_voice_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)

        # Create independent parcels
        for ip in self._independent_parcels:
            parcel_uuid = self._create_parcel(profile_uuid, ip)
            if parcel_uuid and isinstance(ip, self.ASSOCIABLE_PARCELS):
                self._pushed_associable_parcels[ip.parcel_name] = parcel_uuid

        # Create translation profiles
        for tp in self._translation_profiles:
            parcel_uuid = self._create_translation_profile(profile_uuid, tp)
            if parcel_uuid:
                self._pushed_associable_parcels[tp.tpp.parcel_name] = parcel_uuid

        # Create parcels with associations
        for pwa in self._parcels_with_associations:
            if pwa.association:
                self._populate_association(pwa.association)
            self._create_parcel(profile_uuid, pwa)

        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyUcVoiceParcel) -> UUID:
        """
        Internal method to create a parcel.

        Args:
            profile_uuid (UUID): The UUID of the feature profile being built.
            parcel (AnyUcVoiceParcel): The parcel to create.

        Returns:
            UUID: The UUID of the created parcel.
        """
        return self._api.create_parcel(profile_uuid, parcel).id

    def _create_translation_profile(self, profile_uuid: UUID, tp: TranslationProfile) -> UUID:
        """
        Internal method to create a translation profile.

        Args:
            profile_uuid (UUID): The UUID of the feature profile being built.
            tp (TranslationProfile): The translation profile to create.

        Returns:
            UUID: The UUID of the created translation profile parcel.
        """
        if tp.called:
            if called_uuid := self._create_parcel(profile_uuid, tp.called):
                tp.tpp.set_ref_by_call_type(called_uuid, "called")
        if tp.calling:
            if calling_uuid := self._create_parcel(profile_uuid, tp.calling):
                tp.tpp.set_ref_by_call_type(calling_uuid, "calling")
        return self._create_parcel(profile_uuid, tp.tpp)

    def _populate_association(self, association: Association) -> None:
        """
        Resolves associations for a parcel.

        Updates references in the parcel's associations to use the actual UUIDs of previously
        created parcels.

        Args:
            association (Association): A list of associations to resolve.
        """
        for model in association:
            for field_name in self.ASSOCIATON_FIELDS.intersection(model.model_fields_set):
                attr = getattr(model, field_name)
                if isinstance(attr, RefIdItem):
                    if is_uuid(attr.ref_id.value) or attr.ref_id.value is None:
                        continue
                    resolved_uuid = self._pushed_associable_parcels.get(attr.ref_id.value)
                    if resolved_uuid:
                        attr.ref_id.value = str(resolved_uuid)
                    else:
                        logger.warning(
                            f"Unresolved reference in field '{field_name}' with value '{attr.ref_id.value}' "
                            f"for model '{model.__class__.__name__}'. Setting to Default[None]."
                        )
                        attr.ref_id = as_default(None)
