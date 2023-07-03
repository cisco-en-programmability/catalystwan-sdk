from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from inspect import Signature, isclass, signature

# from pydoc import locate
from typing import (
    BinaryIO,
    Final,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Set,
    Type,
    TypedDict,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import BaseModel

from vmngclient.exceptions import APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import AttrsInstance, asdict
from vmngclient.utils.session_type import SessionType

BASE_PATH: Final[str] = "/dataservice"
T = TypeVar("T")
logger = logging.getLogger(__name__)
ModelPayloadType = Union[AttrsInstance, BaseModel, Sequence[AttrsInstance], Sequence[BaseModel]]
PayloadType = Union[None, str, bytes, dict, BinaryIO, ModelPayloadType]


@dataclass
class PayloadTypeSpecifier:
    is_dataseq: bool
    t: type


class PreparedPayload(TypedDict):
    data: Union[str, bytes]
    headers: Mapping[str, str]


def prepare_payload(payload: ModelPayloadType) -> PreparedPayload:
    if isinstance(payload, BaseModel):
        return _prepare_basemodel_payload(payload)
    if isinstance(payload, AttrsInstance):
        return _prepare_attrs_payload(payload)
    if isinstance(payload, (DataSequence, Sequence)):
        return _prepare_sequence_payload(payload)
    else:
        raise APIRequestPayloadTypeError(payload)


def _prepare_basemodel_payload(payload: BaseModel) -> PreparedPayload:
    return PreparedPayload(
        data=payload.json(exclude_none=True, by_alias=True), headers={"content-type": "application/json"}
    )


def _prepare_attrs_payload(payload: AttrsInstance) -> PreparedPayload:
    return PreparedPayload(data=json.dumps(asdict(payload)), headers={"content-type": "application/json"})


def _prepare_sequence_payload(payload: Iterable[Union[BaseModel, AttrsInstance]]) -> PreparedPayload:
    items = []
    for item in payload:
        if isinstance(item, BaseModel):
            items.append(item.dict(exclude_none=True, by_alias=True))
        elif isinstance(item, AttrsInstance):
            items.append(asdict(item))
        else:
            raise APIRequestPayloadTypeError(payload)
    data = json.dumps(items)
    return PreparedPayload(data=data, headers={"content-type": "application/json"})


class APIPRimitiveClientResponse(Protocol):
    @property
    def text(self) -> str:
        ...

    @property
    def content(self) -> bytes:
        ...

    def dataobj(self, cls: Type[T], sourcekey: Optional[str] = "data") -> T:
        ...

    def dataseq(self, cls: Type[T], sourcekey: Optional[str] = "data") -> DataSequence[T]:
        ...


class APIPrimitiveClient(Protocol):
    def request(self, method: str, url: str, **kwargs) -> APIPRimitiveClientResponse:
        ...

    @property
    def api_version(self) -> Optional[Version]:
        ...

    @property
    def session_type(self) -> Optional[SessionType]:
        ...


class APIPrimitiveBase:
    def __init__(self, client: APIPrimitiveClient):
        self._client = client
        self._basepath = BASE_PATH

    def _request(
        self, method: str, url: str, payload: Optional[ModelPayloadType] = None, **kwargs
    ) -> APIPRimitiveClientResponse:
        if payload is not None:
            kwargs.update(prepare_payload(payload))
        return self._client.request(method, self._basepath + url, **kwargs)

    def _get(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("GET", url, payload, **kwargs)

    def _put(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("PUT", url, payload, **kwargs)

    def _post(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("POST", url, payload, **kwargs)

    def _delete(self, url: str, payload: Optional[ModelPayloadType] = None, **kwargs) -> APIPRimitiveClientResponse:
        return self._request("DELETE", url, payload, **kwargs)

    @property
    def _api_version(self) -> Optional[Version]:
        return self._client.api_version

    @property
    def _session_type(self) -> Optional[SessionType]:
        return self._client.session_type


class VersionsDecorator:
    """
    Decorator to annotate api primitives methods with supported versions.
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, supported_versions: str, raises: bool = False):
        self.supported_versions = SpecifierSet(supported_versions)
        self.raises = raises

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @versions decorator")
            current = api._api_version
            supported = self.supported_versions
            if current and current not in supported:
                if self.raises:
                    raise APIVersionError(func, supported, current)
                else:
                    logger.warning(
                        f"vManage runs: {current} but {func.__qualname__} only supported for API versions: {supported}"
                    )
            return func(*args, **kwargs)

        return wrapper


class ViewDecorator:
    """
    Decorator to annotate api primitives methods with session type (view) restriction
    Logs warning or raises exception when incompatibility found.
    """

    def __init__(self, allowed_session_types: Set[SessionType], raises: bool = False):
        self.allowed_session_types = allowed_session_types
        self.raises = raises

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @view decorator")
            current = api._session_type
            allowed = self.allowed_session_types
            if current and current not in allowed:
                if self.raises:
                    raise APIViewError(func, allowed, current)
                else:
                    logger.warning(
                        f"Current view is: {current} but {func.__qualname__} only allowed for views: {allowed}"
                    )
            return func(*args, **kwargs)

        return wrapper


class RequestDecorator:
    def __init__(self, method: str, url: str, resp_json_key: Optional[str] = None, **kwargs):
        self.method = method
        self.url = url
        self.resp_json_key = resp_json_key

    def get_return_type(self, sig: Signature) -> PayloadTypeSpecifier:
        reta = sig.return_annotation
        if isclass(reta):
            return PayloadTypeSpecifier(is_dataseq=False, t=reta)
        elif (type_origin := get_origin(reta)) and type_origin == DataSequence:
            if (type_args := get_args(reta)) and isclass(type_args[0]):
                return PayloadTypeSpecifier(is_dataseq=True, t=type_args[0])
            raise TypeError(f"Methods annotaded with @requests should only return: {PayloadType} but {reta} found")
        else:
            raise TypeError(f"Methods annotaded with @requests should only return: {PayloadType} but {reta} found")

    def get_payload_type(self, sig: Signature) -> type:
        return str

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            api = args[0]
            if not isinstance(api, APIPrimitiveBase):
                raise TypeError("Only APIPrimitiveBase instance methods can be annotated with @request decorator")
            func_signature = signature(func)
            return_type_spec = self.get_return_type(func_signature)
            print(return_type_spec)
            breakpoint()

        return wrapper


versions = VersionsDecorator
view = ViewDecorator
request = RequestDecorator
get = "GET"
post = "POST"
put = "PUT"
delete = "DELETE"
