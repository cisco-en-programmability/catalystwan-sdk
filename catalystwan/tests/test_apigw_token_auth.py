# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from requests import PreparedRequest

from catalystwan.apigw_auth import ApiGwAuth, ApiGwLogin
from catalystwan.exceptions import CatalystwanException
from catalystwan.session import ManagerSession, create_apigw_session


class TestApiGwTokenAuth(unittest.TestCase):
    def test_login_validation_with_token(self):
        login = ApiGwLogin(org_name="cisco", token="sample-bearer-token")
        self.assertEqual(login.token, "sample-bearer-token")
        self.assertIsNone(login.client_id)
        self.assertIsNone(login.client_secret)

    def test_login_validation_with_credentials(self):
        login = ApiGwLogin(client_id="cid", client_secret="csec", org_name="cisco")
        self.assertEqual(login.client_id, "cid")
        self.assertEqual(login.client_secret, "csec")
        self.assertIsNone(login.token)

    def test_login_validation_missing_both_raises(self):
        with self.assertRaises(ValueError):
            ApiGwLogin(org_name="cisco")

    def test_auth_with_token_attaches_headers(self):
        login = ApiGwLogin(org_name="cisco", token="sample-bearer-token")
        auth = ApiGwAuth(login=login)

        request = PreparedRequest()
        request.url = "https://example.com/dataservice/device"
        request.headers = {}

        processed = auth(request)
        self.assertEqual(processed.headers.get("Authorization"), "Bearer sample-bearer-token")
        self.assertEqual(processed.headers.get("sdwan-org"), "cisco")
        self.assertTrue(auth.org_registered)

    def test_auth_with_token_expiration_raises_helpful_error(self):
        login = ApiGwLogin(org_name="cisco", token="expired-token")
        auth = ApiGwAuth(login=login)

        request = PreparedRequest()
        request.url = "https://example.com/dataservice/device"
        request.headers = {"Authorization": "Bearer expired-token"}

        # Simulate 401 handling where session clears the token
        auth.clear(request)
        self.assertEqual(auth.token, "")

        # Next call to handle_auth / authenticate should raise CatalystwanException
        with self.assertRaises(CatalystwanException) as ctx:
            auth(request)
        self.assertIn("cannot be refreshed without client_id and client_secret", str(ctx.exception))

    @patch.object(ManagerSession, "_fetch_server_info")
    def test_create_apigw_session_with_token(self, mock_server_info):
        mock_server_info.return_value = MagicMock()
        session = create_apigw_session(url="example.com", org_name="cisco", token="token-123")
        self.assertIsInstance(session, ManagerSession)
        self.assertIsInstance(session.auth, ApiGwAuth)
        self.assertEqual(session.auth.token, "token-123")
        self.assertEqual(session.auth.login.org_name, "cisco")
