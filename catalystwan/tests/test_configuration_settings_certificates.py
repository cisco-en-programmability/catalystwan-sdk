# Copyright 2024 Cisco Systems, Inc. and its affiliates

import json
import unittest
from unittest.mock import MagicMock

from catalystwan.endpoints.configuration_settings import Certificate, ConfigurationSettings


class TestConfigurationSettingsCertificates(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.settings = ConfigurationSettings(self.mock_client)

    def test_certificate_model_minimal_serialization(self):
        cert = Certificate(certificate_signing="enterprise")
        payload_json = cert.model_dump_json(exclude_none=True, by_alias=True)
        data = json.loads(payload_json)
        self.assertEqual(data, {"certificateSigning": "enterprise"})
        self.assertNotIn("validityPeriod", data)
        self.assertNotIn("email", data)

    def test_certificate_model_full_serialization(self):
        cert = Certificate(
            certificate_signing="cisco",
            validity_period="1Y",
            retrieve_interval="60",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )
        payload_json = cert.model_dump_json(exclude_none=True, by_alias=True)
        data = json.loads(payload_json)
        self.assertEqual(
            data,
            {
                "certificateSigning": "cisco",
                "validityPeriod": "1Y",
                "retrieveInterval": "60",
                "firstName": "Jane",
                "lastName": "Doe",
                "email": "jane@example.com",
            },
        )

    def test_edit_certificates_sends_post_with_correct_payload(self):
        cert = Certificate(certificate_signing="enterprise")
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"certificateSigning": "enterprise"}]}
        self.mock_client.request.return_value = mock_response

        self.settings.edit_certificates(cert)

        self.mock_client.request.assert_called_once()
        call_args, call_kwargs = self.mock_client.request.call_args
        method, url = call_args[0], call_args[1]

        self.assertEqual(method, "POST")
        self.assertIn("/settings/configuration/certificate", url)
        self.assertEqual(json.loads(call_kwargs["data"]), {"certificateSigning": "enterprise"})
