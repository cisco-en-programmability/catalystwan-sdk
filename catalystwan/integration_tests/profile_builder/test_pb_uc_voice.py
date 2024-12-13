# Copyright 2024 Cisco Systems, Inc. and its affiliates
from catalystwan.api.configuration_groups.parcel import Global, as_global, as_variable
from catalystwan.integration_tests.base import TestCaseBase, create_name_with_run_id
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import (
    AnalogInterfaceParcel,
    TranslationProfileParcel,
    TranslationRuleParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.analog_interface import (
    Association,
    ModuleType,
    SlotId,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_rule import Action, RuleSettings
from catalystwan.tests.builders.uc_voice import as_default


class TestUcVoiceFeatureProfileBuilder(TestCaseBase):
    def setUp(self) -> None:
        self.fp_name = create_name_with_run_id("FeatureProfileBuilderUcVoice")
        self.fp_description = "Transport feature profile"
        self.builder = self.session.api.builders.feature_profiles.create_builder("uc-voice")
        self.builder.add_profile_name_and_description(
            feature_profile=FeatureProfileCreationPayload(name=self.fp_name, description=self.fp_description)
        )
        self.api = self.session.api.sdwan_feature_profiles.transport
        self.tp = TranslationProfileParcel(
            parcel_name="TPP", parcel_description="TTP_Desc", translation_profile_settings=[]
        )
        self.tr_calling = TranslationRuleParcel(
            parcel_name="2",
            parcel_description="desc",
            rule_name=Global[int](value=2),
            rule_settings=[
                RuleSettings(
                    action=Global[Action](value="replace"),
                    match=Global[str](value="/123/"),
                    replacement_pattern=Global[str](value="/444/"),
                    rule_num=Global[int](value=2),
                )
            ],
        )
        self.tr_called = TranslationRuleParcel(
            parcel_name="4",
            parcel_description="desc",
            rule_name=Global[int](value=4),
            rule_settings=[
                RuleSettings(
                    action=Global[Action](value="replace"),
                    match=Global[str](value="/321/"),
                    replacement_pattern=Global[str](value="/4445/"),
                    rule_num=Global[int](value=4),
                )
            ],
        )

    def test_when_build_profile_with_translation_profile_and_rules_expect_success(self):
        # Arrange
        self.builder.add_translation_profile(self.tp, self.tr_calling, self.tr_called)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def test_when_build_profile_with_analog_interface_and_translation_profile_and_rules_assosiations_expect_success(
        self,
    ):
        # Arrange
        ai = AnalogInterfaceParcel(
            parcel_name="Ai",
            parcel_description="",
            enable=as_default(True),
            slot_id=as_global("0/1", SlotId),
            module_type=as_global("72 Port FXS", ModuleType),
            association=[
                Association(
                    port_range=as_variable("{{test}}"),
                    translation_profile=RefIdItem(ref_id=as_global("TPP")),
                    trunk_group=RefIdItem(ref_id=as_default(None)),
                    trunk_group_priority=as_default(None),
                    translation_rule_direction=as_default(None),
                )
            ],
        )
        self.builder.add_translation_profile(self.tp, self.tr_calling, self.tr_called)
        self.builder.add_parcel_with_associations(ai)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def tearDown(self) -> None:
        target_profile = self.api.get_profiles().filter(profile_name=self.fp_name).single_or_default()
        if target_profile:
            # In case of a failed test, the profile might not have been created
            self.api.delete_profile(target_profile.profile_id)
