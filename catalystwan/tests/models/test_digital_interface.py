# Copyright 2025 Cisco Systems, Inc. and its affiliates
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import DigitalInterfaceParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.digital_interface import VoiceInterfaceTemplates, BasicSettings, LineCode, Framing, LineTermination, SwitchType, validate_basic_settings_values, VALIDATION_DIGITAL_INTERFACE_VIT_E1_BASIC_SETTINGS_REQUIREMENTS, VALIDATION_DIGITAL_INTERFACE_VIT_T1_BASIC_SETTINGS_REQUIREMENTS
import unittest
from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from pydantic import ValidationError

class TestDigitalInterfaceParcel(unittest.TestCase):
    def test_e1_configuration_valid(self):
        # Valid configuration for E1
        basic_settings = BasicSettings(
            line_code=Global[LineCode](value="ami"),
            framing=Global[Framing](value="crc4"),
            line_termination=Global[LineTermination](value="120-ohm"),
            framing_australia=Global[bool](value=True),
            delay_connect_timer=Global[int](value=5),
            network_side=Global[bool](value=True),
            port_range=Global[str](value="0/1"),
            switch_type=Global[SwitchType](value="primary-4ess"),
        )

        validate_basic_settings_values([basic_settings], VALIDATION_DIGITAL_INTERFACE_VIT_E1_BASIC_SETTINGS_REQUIREMENTS, "E1")

    def test_e1_configuration_invalid(self):
        # Invalid configuration for E1
        basic_settings = BasicSettings(
            line_code=Global[LineCode](value="b8zs"),  # Invalid for E1
            framing=Global[Framing](value="crc4"),
            line_termination=Global[LineTermination](value="120-ohm"),
            framing_australia=Global[bool](value=True),
            delay_connect_timer=Global[int](value=5),
            network_side=Global[bool](value=True),
            port_range=Global[str](value="0/1"),
            switch_type=Global[SwitchType](value="primary-4ess"),
        )

        with self.assertRaises(ValueError) as context:
            validate_basic_settings_values(
                [basic_settings], 
                VALIDATION_DIGITAL_INTERFACE_VIT_E1_BASIC_SETTINGS_REQUIREMENTS, 
                "E1"
            )
        
            # Assert the error message
            expected_message = "For E1 configuration, invalid value 'b8zs' for 'line_code'. Expected one of: {'ami', 'hdb3'}."
            self.assertEqual(str(context.exception), expected_message)