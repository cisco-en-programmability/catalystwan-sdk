# Copyright 2024 Cisco Systems, Inc. and its affiliates

import json
import unittest
from unittest.mock import MagicMock

from catalystwan.endpoints.configuration_settings import ConfigurationSettings, EnterpriseRootCA
from catalystwan.utils.session_type import ProviderView

CERT_CHAIN = (
    "-----BEGIN CERTIFICATE-----\n"
    "MIIBkTCB+wIJALa123456789...\n"
    "-----END CERTIFICATE-----\n"
    "-----BEGIN CERTIFICATE-----\n"
    "MIICljCCAX4CCQDU987654321...\n"
    "-----END CERTIFICATE-----"
)


class TestEnterpriseRootCA(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client.session_type = ProviderView
        self.settings = ConfigurationSettings(self.mock_client)

    def test_enterprise_root_ca_model_serialization(self):
        model = EnterpriseRootCA(enterprise_root_ca=CERT_CHAIN)
        dumped_json = model.model_dump_json(exclude_none=True, by_alias=True)
        data = json.loads(dumped_json)
        self.assertEqual(data["enterpriseRootCA"], CERT_CHAIN)
        self.assertNotIn("intermediateCA", data)

    def test_enterprise_root_ca_with_intermediate(self):
        model = EnterpriseRootCA(enterprise_root_ca=CERT_CHAIN, intermediate_ca="true")
        dumped_json = model.model_dump_json(exclude_none=True, by_alias=True)
        data = json.loads(dumped_json)
        self.assertEqual(data["enterpriseRootCA"], CERT_CHAIN)
        self.assertEqual(data["intermediateCA"], "true")

    def test_upload_enterprise_root_ca_request(self):
        payload = EnterpriseRootCA(enterprise_root_ca=CERT_CHAIN)
        expected_seq = [EnterpriseRootCA(enterprise_root_ca=CERT_CHAIN)]
        mock_response = MagicMock()
        mock_response.dataseq.return_value = expected_seq
        self.mock_client.request.return_value = mock_response

        res = self.settings.upload_enterprise_root_ca(payload)

        self.mock_client.request.assert_called_once()
        call_args, call_kwargs = self.mock_client.request.call_args
        method, url = call_args[0], call_args[1]
        self.assertEqual(method, "POST")
        self.assertIn("/settings/configuration/certificate/enterpriserootca", url)
        self.assertEqual(json.loads(call_kwargs["data"])["enterpriseRootCA"], CERT_CHAIN)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].enterprise_root_ca, CERT_CHAIN)

    def test_get_enterprise_root_ca_request(self):
        expected_seq = [EnterpriseRootCA(enterprise_root_ca=CERT_CHAIN)]
        mock_response = MagicMock()
        mock_response.dataseq.return_value = expected_seq
        self.mock_client.request.return_value = mock_response

        res = self.settings.get_enterprise_root_ca()

        self.mock_client.request.assert_called_once()
        call_args, _ = self.mock_client.request.call_args
        method, url = call_args[0], call_args[1]
        self.assertEqual(method, "GET")
        self.assertIn("/settings/configuration/certificate/enterpriserootca", url)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].enterprise_root_ca, CERT_CHAIN)
