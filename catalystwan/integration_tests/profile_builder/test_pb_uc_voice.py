# Copyright 2025 Cisco Systems, Inc. and its affiliates
from uuid import uuid4

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global, as_variable
from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import (
    AnalogInterfaceParcel,
    MediaProfileParcel,
    SrstParcel,
    TranslationProfileParcel,
    TranslationRuleParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.analog_interface import (
    Association as AnalogAssociation,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.analog_interface import ModuleType, SlotId
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.call_routing import (
    Association as CallRoutingAssociation,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.call_routing import CallRoutingParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.digital_interface import (
    Association as DigitalInterfaceAssociation,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.digital_interface import (
    BasicSettings,
    CableLengthType,
    CableLengthValue,
    DigitalInterfaceParcel,
    Framing,
    LineCode,
    ModuleLocation,
    SwitchType,
    VoiceInterfaceTemplates,
)
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.srst import Association as SrstAssociation
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.srst import Pool
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.translation_rule import Action, RuleSettings
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.trunk_group import TrunkGroupParcel
from catalystwan.tests.builders.uc_voice import as_default


class TestUcVoiceFeatureProfileBuilder(TestCaseBase):
    def setUp(self) -> None:
        self.feature_profile_name = f"FeatureProfileBuilderUcVoice_{str(uuid4())[:5]}"
        self.feature_profile_description = "UC Voice feature profile"

        self.builder = self.session.api.builders.feature_profiles.create_builder("uc-voice")
        self.builder.add_profile_name_and_description(
            feature_profile=FeatureProfileCreationPayload(
                name=self.feature_profile_name, description=self.feature_profile_description
            )
        )

        self.api = self.session.api.sdwan_feature_profiles.uc_voice

        self.translation_profile = TranslationProfileParcel(
            parcel_name="TranslationProfile",
            parcel_description="TranslationProfileDescription",
            translation_profile_settings=[],
        )

        self.translation_profile2 = TranslationProfileParcel(
            parcel_name="TranslationProfile2",
            parcel_description="TranslationProfileDescription",
            translation_profile_settings=[],
        )

        self.translation_rule_calling = TranslationRuleParcel(
            parcel_name="TranslationRuleCalling",
            parcel_description="Description",
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

        self.translation_rule_called = TranslationRuleParcel(
            parcel_name="TranslationRuleCalled",
            parcel_description="Description",
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

        self.media_profile = MediaProfileParcel(
            parcel_name="MediaProfile",
            parcel_description="MediaProfileDescription",
            codec=as_global(["g711ulaw"]),
            dtmf=Variable(value="{{test_1}}"),
            media_profile_number=Variable(value="{{test_2}}"),
        )

        self.trunk_group = TrunkGroupParcel(
            parcel_name="TrunkGroup",
            parcel_description="TrunkGroupDescription",
            hunt_scheme_method=as_default(None),
            max_calls_in=as_default(None),
            max_calls_out=as_default(None),
            max_retries=as_default(None),
            hunt_scheme_channel=as_default(None),
            hunt_scheme_direction=as_default(None),
        )

    def test_build_profile_with_translation_profile_and_rules(self):
        self.builder.add_translation_profile(
            self.translation_profile, self.translation_rule_calling, self.translation_rule_called
        )

        report = self.builder.build()

        assert len(report.failed_parcels) == 0, "Failed to build feature profile with translation profile and rules."

    def test_build_profile_with_translation_profile_and_same_rules_references(self):
        self.builder.add_translation_profile(
            self.translation_profile, self.translation_rule_calling, self.translation_rule_called
        )

        self.builder.add_translation_profile(
            self.translation_profile2, self.translation_rule_calling, self.translation_rule_called
        )

        report = self.builder.build()

        assert len(report.failed_parcels) == 0, "Failed to build feature profile with translation profile and rules."

    def test_build_profile_with_trunk_group(self):
        self.builder.add_associable_parcel(self.trunk_group)

        report = self.builder.build()

        assert len(report.failed_parcels) == 0, "Failed to build feature profile with trunk group parcel."

    def test_build_profile_with_digital_interface_translation_profile_and_trunk_group(self):
        digital_interface = DigitalInterfaceParcel(
            parcel_name="DigitalInterfaceParcel",
            parcel_description="DigitalInterfaceParcel",
            shutdown=[],
            isdn_timer=[],
            interface=[],
            line_params=[],
            outgoing_ie=[],
            dsp_hairpin=as_default(False),
            module_location=as_global("0/1", ModuleLocation),
            voice_interface_templates=as_global("1 Port T1", VoiceInterfaceTemplates),
            basic_settings=[
                BasicSettings(
                    delay_connect_timer=as_default(20),
                    framing=as_default("esf", Framing),
                    line_code=as_default("b8zs", LineCode),
                    network_side=as_default(False),
                    port_range=as_global("0-0"),
                    switch_type=as_default("primary-ni", SwitchType),
                    cable_length=as_default("0", CableLengthValue),
                    cable_length_type=as_default("long", CableLengthType),
                    timeslots=as_global("1-24"),
                )
            ],
            association=[
                DigitalInterfaceAssociation(
                    port_range=as_global("0-0"),
                    translation_profile=RefIdItem(ref_id=as_global(self.translation_profile.parcel_name)),
                    trunk_group=RefIdItem(ref_id=as_global(self.trunk_group.parcel_name)),
                    translation_profile_direction=as_default(None),
                    trunk_group_priority=as_default(None),
                )
            ],
        )

        self.builder.add_associable_parcel(self.trunk_group)
        self.builder.add_translation_profile(
            self.translation_profile, self.translation_rule_calling, self.translation_rule_called
        )
        self.builder.add_parcel_with_associations(digital_interface)

        report = self.builder.build()

        assert (
            len(report.failed_parcels) == 0
        ), "Failed to build feature profile with digital interface, trunk group, and translation profile associations."

    def test_build_profile_with_analog_interface_and_translation_profile_and_rules_associations(self):
        analog_interface = AnalogInterfaceParcel(
            parcel_name="AnalogInterface",
            parcel_description="",
            enable=as_default(True),
            slot_id=as_global("0/1", SlotId),
            module_type=as_global("72 Port FXS", ModuleType),
            association=[
                AnalogAssociation(
                    port_range=as_variable("{{test}}"),
                    translation_profile=RefIdItem(ref_id=as_global("TranslationProfile")),
                    trunk_group=RefIdItem(ref_id=as_default(None)),
                    trunk_group_priority=as_default(None),
                    translation_rule_direction=as_default(None),
                )
            ],
        )

        self.builder.add_translation_profile(
            self.translation_profile, self.translation_rule_calling, self.translation_rule_called
        )
        self.builder.add_parcel_with_associations(analog_interface)

        report = self.builder.build()

        assert (
            len(report.failed_parcels) == 0
        ), "Failed to build feature profile with analog interface and translation profile associations."

    def test_build_profile_with_srts_and_media_profile_associations(self):
        srst = SrstParcel(
            parcel_name="Srst",
            parcel_description="SrstDescription",
            max_dn=Global[int](value=3),
            max_phones=Global[int](value=3),
            pool=[
                Pool(
                    ipv4_oripv6prefix=Variable(value="{{test_4}}"),
                    pool_tag=as_global(1),
                )
            ],
            association=[
                SrstAssociation(
                    media_profile=RefIdItem(ref_id=as_global(self.media_profile.parcel_name)),
                )
            ],
        )

        self.builder.add_associable_parcel(self.media_profile)
        self.builder.add_parcel_with_associations(srst)

        report = self.builder.build()

        assert (
            len(report.failed_parcels) == 0
        ), "Failed to build feature profile with SRST and media profile associations."

    def test_build_profile_with_call_routing(self):
        call_routing = CallRoutingParcel(
            parcel_name="CallRoutingParcel",
            parcel_description="CallRoutingDescription",
            dial_peer_tag_prefix=Default[None](value=None),
            port_module_location=RefIdItem(ref_id=Default[None](value=None)),
            voice=[],
            modem_pass_through=[],
            fax_protocol=[],
            association=[
                CallRoutingAssociation(
                    dial_peer_range=as_global("1"),
                    media_profile=RefIdItem(ref_id=as_global(self.media_profile.parcel_name)),
                    translation_profile=RefIdItem(ref_id=as_global(self.translation_profile.parcel_name)),
                    trunk_group=RefIdItem(ref_id=as_global(self.trunk_group.parcel_name)),
                )
            ],
        )
        self.builder.add_parcel_with_associations(call_routing)

        report = self.builder.build()

        assert len(report.failed_parcels) == 0, "Failed to build feature profile with Call Routing parcel."

    def tearDown(self) -> None:
        profile = self.api.get_profiles().filter(profile_name=self.feature_profile_name).single_or_default()
        if profile:
            self.api.delete_profile(profile.profile_id)
