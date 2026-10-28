# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from requests import PreparedRequest

from catalystwan.apigw_auth import ApiGwAuth, ApiGwLogin, ApiGwRegister, _login_to_register
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

    def test_login_validation_missing_client_id_raises(self):
        with self.assertRaises(ValueError):
            ApiGwLogin(client_secret="csec", org_name="cisco")

    def test_login_validation_missing_client_secret_raises(self):
        with self.assertRaises(ValueError):
            ApiGwLogin(client_id="cid", org_name="cisco")

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

    @patch("catalystwan.apigw_auth.post")
    def test_token_auth_does_not_trigger_registration_or_login(self, mock_post):
        login = ApiGwLogin(org_name="cisco", token="token-123")
        auth = ApiGwAuth(login=login)

        request = PreparedRequest()
        request.url = "https://example.com/dataservice/device"
        request.headers = {}

        processed = auth(request)
        mock_post.assert_not_called()
        self.assertEqual(processed.headers.get("Authorization"), "Bearer token-123")
        self.assertEqual(processed.headers.get("sdwan-org"), "cisco")

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

    @patch("catalystwan.apigw_auth.post")
    def test_credentials_registration_and_login_flow(self, mock_post):
        mock_reg_resp = MagicMock()
        mock_reg_resp.raise_for_status.return_value = None

        mock_login_resp = MagicMock()
        mock_login_resp.raise_for_status.return_value = None
        mock_login_resp.json.return_value = {"token": "received-bearer-token"}

        mock_post.side_effect = [mock_reg_resp, mock_login_resp]

        login = ApiGwLogin(
            client_id="test-client-id",
            client_secret="test-client-secret",
            org_name="cisco",
            tenant_user=True,
        )
        auth = ApiGwAuth(login=login)

        request = PreparedRequest()
        request.url = "https://example.com/dataservice/device"
        request.headers = {}

        processed = auth(request)

        self.assertEqual(mock_post.call_count, 2)
        _, reg_kwargs = mock_post.call_args_list[0]
        self.assertEqual(reg_kwargs["url"], "https://example.com/apigw/organization/registration")
        self.assertEqual(
            reg_kwargs["json"],
            {
                "client_id": "test-client-id",
                "client_secret": "test-client-secret",
                "org_name": "cisco",
                "is_tenant": True,
            },
        )
        _, login_kwargs = mock_post.call_args_list[1]
        self.assertEqual(login_kwargs["url"], "https://example.com/apigw/login")
        self.assertEqual(login_kwargs["json"]["client_id"], "test-client-id")
        self.assertEqual(login_kwargs["json"]["client_secret"], "test-client-secret")

        self.assertEqual(auth.token, "received-bearer-token")
        self.assertTrue(auth.org_registered)
        self.assertEqual(processed.headers.get("Authorization"), "Bearer received-bearer-token")
        self.assertEqual(processed.headers.get("sdwan-org"), "cisco")

    def test_login_to_register_valid(self):
        login = ApiGwLogin(
            client_id="cid",
            client_secret="csec",
            org_name="cisco",
            tenant_user=True,
        )
        register_model = _login_to_register(login)
        self.assertIsInstance(register_model, ApiGwRegister)
        self.assertEqual(register_model.client_id, "cid")
        self.assertEqual(register_model.client_secret, "csec")
        self.assertEqual(register_model.org_name, "cisco")
        self.assertTrue(register_model.is_tenant)

    def test_login_to_register_missing_credentials_raises(self):
        login = ApiGwLogin(org_name="cisco", token="bearer-token")
        with self.assertRaises(CatalystwanException) as ctx:
            _login_to_register(login)
        self.assertIn("cannot be registered without client_id and client_secret", str(ctx.exception))

    def test_register_missing_credentials_raises(self):
        login = ApiGwLogin(org_name="cisco", token="sample-token")
        auth = ApiGwAuth(login=login)
        request = PreparedRequest()
        request.url = "https://example.com/dataservice/device"

        with self.assertRaises(CatalystwanException) as ctx:
            auth.register(request)
        self.assertIn("cannot be registered without client_id and client_secret", str(ctx.exception))

    def test_register_org_missing_credentials_raises(self):
        login = ApiGwLogin(org_name="cisco", token="sample-token")
        with self.assertRaises(CatalystwanException) as ctx:
            ApiGwAuth.register_org("https://example.com", login)
        self.assertIn("cannot be registered without client_id and client_secret", str(ctx.exception))

    @patch.object(ManagerSession, "_fetch_server_info")
    def test_create_apigw_session_with_token(self, mock_server_info):
        mock_server_info.return_value = MagicMock()
        session = create_apigw_session(url="example.com", org_name="cisco", token="token-123")
        self.assertIsInstance(session, ManagerSession)
        self.assertIsInstance(session.auth, ApiGwAuth)
        self.assertEqual(session.auth.token, "token-123")
        self.assertEqual(session.auth.login.org_name, "cisco")
