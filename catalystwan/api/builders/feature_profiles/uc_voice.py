# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_build_report
from catalystwan.api.feature_profile_api import UcVoiceFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.uc_voice import UcVoiceFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import (
    AnyUcVoiceParcel,
    TranslationProfileParcel,
    TranslationRuleParcel,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


@dataclass
class TranslationProfile:
    tpp: TranslationProfileParcel
    calling: Optional[TranslationRuleParcel] = None
    called: Optional[TranslationRuleParcel] = None


class UcVoiceFeatureProfileBuilder:
    """
    A class for building UcVoice feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = UcVoiceFeatureProfileAPI(session)
        self._endpoints = UcVoiceFeatureProfile(session)
        self._independent_items: List[AnyUcVoiceParcel] = []
        self._translation_profiles: List[TranslationProfile] = []

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile.

        Args:
            name (str): The name of the feature profile.
            description (str): The description of the feature profile.

        Returns:
            None
        """
        self._profile = feature_profile

    def add_parcel(self, parcel: AnyUcVoiceParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnySystemParcel): The parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def add_translation_profile(
        self,
        tpp: TranslationProfileParcel,
        calling: Optional[TranslationRuleParcel] = None,
        called: Optional[TranslationRuleParcel] = None,
    ):
        if not calling and not called:
            raise ValueError("There must be at least one translation rule to create a translation profile")
        self._translation_profiles.append(TranslationProfile(tpp=tpp, called=called, calling=calling))

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the feature profile.

        Returns:
            UUID: The UUID of the created feature profile.
        """

        profile_uuid = self._endpoints.create_uc_voice_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._independent_items:
            self._create_parcel(profile_uuid, parcel)
        for tp in self._translation_profiles:
            self._create_translation_profile(profile_uuid, tp)

        return self.build_report

    @handle_build_report
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyUcVoiceParcel) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel).id

    def _create_translation_profile(self, profile_uuid: UUID, tp: TranslationProfile):
        if tp.called:
            called_uuid = self._create_parcel(profile_uuid, tp.called)
            if called_uuid:
                tp.tpp.set_ref_by_call_type(called_uuid, "called")
        if tp.calling:
            calling_uuid = self._create_parcel(profile_uuid, tp.calling)
            if calling_uuid:
                tp.tpp.set_ref_by_call_type(calling_uuid, "calling")
        self._create_parcel(profile_uuid, tp.tpp)
