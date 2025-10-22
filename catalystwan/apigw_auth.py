# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from threading import RLock
from typing import Literal, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, PositiveInt
from requests import HTTPError, PreparedRequest, post
from requests.auth import AuthBase
from requests.exceptions import JSONDecodeError, Timeout

from catalystwan.abstractions import APIEndpointClient, AuthProtocol
from catalystwan.exceptions import ApiGwAuthTimeout, CatalystwanException
from catalystwan.response import auth_response_debug

LoginMode = Literal["machine", "user", "session"]


class ApiGwLogin(BaseModel):
    client_id: str
    client_secret: str
    org_name: str
    mode: Optional[LoginMode] = None
    username: Optional[str] = None
    session: Optional[str] = None
    tenant_user: Optional[bool] = None
    token_duration: PositiveInt = Field(default=60 * 30, description="in seconds")


class ApiGwAuth(AuthBase, AuthProtocol):
    """Attaches ApiGateway Authentication to the given Requests object.

    1. Get a bearer token by sending a POST request to the /apigw/login endpoint.
    2. Use the token in the Authorization header for subsequent requests.
    """

    def __init__(self, login: ApiGwLogin, logger: Optional[logging.Logger] = None, verify: Union[bool, str] = False):
        self.login = login
        self.token = ""
        self.org_registered: bool = False
        self.logger = logger or logging.getLogger(__name__)
        self.verify = verify
        self.session_count: int = 0
        self.request_timeout: int = 10
        self.lock: RLock = RLock()

    def __str__(self) -> str:
        return f"ApiGatewayAuth(mode={self.login.mode})"

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        with self.lock:
            self.handle_auth(request)
            self.build_digest_header(request)
        return request

    def handle_auth(self, request: PreparedRequest) -> None:
        if not self.org_registered:
            self.register(request)
        if self.token == "":
            self.authenticate(request)

    def authenticate(self, request: PreparedRequest):
        base_url = self.get_base_url(request)
        self.token = self.get_token(base_url, self.login, self.logger, self.verify, self.request_timeout)

    def register(self, request: PreparedRequest):
        base_url = self.get_base_url(request)
        self.register_org(base_url, self.login, self.logger, self.verify, self.request_timeout)
        self.org_registered = True

    def get_base_url(self, request: PreparedRequest):
        assert request.url is not None
        url = urlparse(request.url)
        base_url = f"{url.scheme}://{url.netloc}"  # noqa: E231
        return base_url

    def build_digest_header(self, request: PreparedRequest) -> None:
        header = {
            "sdwan-org": self.login.org_name,
            "Authorization": f"Bearer {self.token}",
        }
        request.headers.update(header)

    @staticmethod
    def get_token(
        base_url: str,
        apigw_login: ApiGwLogin,
        logger: Optional[logging.Logger] = None,
        verify: Union[bool, str] = False,
        timeout: int = 10,
    ) -> str:
        try:
            response = post(
                url=f"{base_url}/apigw/login",
                verify=verify,
                json=apigw_login.model_dump(exclude_none=True),
                timeout=timeout,
            )
            if logger is not None:
                logger.debug(auth_response_debug(response))
            response.raise_for_status()
            token = response.json()["token"]
        except JSONDecodeError:
            raise CatalystwanException(f"Incorrect response type from ApiGateway login request, ({response.text})")
        except HTTPError as ex:
            raise CatalystwanException(
                f"Problem with connection to ApiGateway login endpoint, ({ex}). Response: ({response.text})"
            )
        except Timeout as ex:
            raise ApiGwAuthTimeout(f"The request to the API GW login timeout, ({ex}).")
        except KeyError as ex:
            raise CatalystwanException(f"Not found token in login response from ApiGateway, ({ex})")
        else:
            if not token or not isinstance(token, str):
                raise CatalystwanException("Failed to get bearer token")
        return token

    @staticmethod
    def register_org(
        base_url: str,
        apigw_login: ApiGwLogin,
        logger: Optional[logging.Logger] = None,
        verify: Union[bool, str] = False,
        timeout: int = 10,
    ) -> None:
        try:
            payload = apigw_login.model_dump(include={"client_id", "client_secret", "org_name"})
            response = post(
                url=f"{base_url}/apigw/organization/registration",
                json=payload,
                verify=verify,
                timeout=timeout,
            )
            if logger is not None:
                logger.debug(auth_response_debug(response))

            response.raise_for_status()

        except HTTPError as ex:
            raise CatalystwanException(
                f"Problem with connecting to API GW organization registration endpoint, ({ex}).\
                  Response: ({response.text})"
            )
        except Timeout as ex:
            raise ApiGwAuthTimeout(f"The request to the API GW organization registration timeout, ({ex}).")
        except Exception as ex:
            raise CatalystwanException(f"Org registration to API-GW failed: {ex}")

    def logout(self, client: APIEndpointClient) -> None:
        return None

    def _clear(self) -> None:
        with self.lock:
            self.token = ""

    def increase_session_count(self) -> None:
        with self.lock:
            self.session_count += 1

    def decrease_session_count(self) -> None:
        with self.lock:
            self.session_count -= 1

    def clear(self, last_request: Optional[PreparedRequest]) -> None:
        with self.lock:
            # extract previously used jsessionid
            if last_request is None:
                token = None
            else:
                token = last_request.headers.get("Authorization")

            if self.token == "" or f"Bearer {self.token}" == token:
                # used auth was up-to-date, clear state
                return self._clear()
            else:
                # used auth was out-of-date, repeat the request with a new one
                return
