"""This modules defines APIEndpoints class which is used to define
vManage API endpoint handlers in declarative way.
Just create a sub-class and define endpoints using using included decorators: request, view, versions.
Method decorated with @request has no body, as decorator constructs and sends request.
>>> from vmngclient.endpoints import APIEndpoints, versions, view, request, delete
>>> from vmngclient.utils.session_type import ProviderView
>>>
>>>
>>> class TenantBulkDeleteRequest(BaseModel):
>>>     password: str
>>>     tenant_id_list: List[str] = Field(alias="tenantIdList")
>>>
>>>
>>> class TenantTaskId(BaseModel):
>>>     id: str
>>>
>>>
>>> class TenantManagementAPI(APIEndpoints):
>>>     @versions(">=20.4")
>>>     @view({ProviderView})
>>>     @request(delete, "/tenant/bulk/async")
>>>     def delete_tenant_async_bulk(self, payload: TenantBulkDeleteRequest) -> TenantTaskId:
>>>         ...
>>>
To send request instantiate API with logged vManageSession:
>>> api = TenantManagementAPI(session)
>>> api.delete_tenant_async_bulk(TenantBulkDeleteRequest(password="p4s$w0rD", tenantIdList=["TNT00005"]))
"""
from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from inspect import _empty, isclass, signature
from io import BufferedReader
from string import Formatter
from typing import (
    Any,
    BinaryIO,
    ClassVar,
    Dict,
    Final,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    runtime_checkable,
)

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import BaseModel

from vmngclient.dataclasses import DataclassBase
from vmngclient.exceptions import APIEndpointError, APIRequestPayloadTypeError, APIVersionError, APIViewError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import AttrsInstance
from vmngclient.utils.creation_tools import asdict as attrs_asdict
from vmngclient.utils.session_type import SessionType

BASE_PATH: Final[str] = "/dataservice"
T = TypeVar("T")
logger = logging.getLogger(__name__)


@runtime_checkable
class CustomPayloadType(Protocol):
    def prepared(self) -> PreparedPayload:
        ...


ModelPayloadType = Union[AttrsInstance, BaseModel, Sequence[AttrsInstance], Sequence[BaseModel]]
PayloadType = Union[str, bytes, dict, ModelPayloadType, CustomPayloadType]
ReturnType = Union[bytes, str, dict, BaseModel, DataclassBase, DataSequence[BaseModel], DataSequence[DataclassBase]]
RequestParamsType = Union[Dict[str, str], BaseModel]


@dataclass
class TypeSpecifier:
    """Holds type information extracted from signature. Common for payload and return values. Used for documentation"""

    present: bool
    sequence_type: Optional[type] = None
    payload_type: Optional[type] = None


@dataclass
class APIEndpointRequestMeta:
    """Holds data for endpoints exctracted during decorating. Used for documentation"""

    http_request: str
    payload_spec: TypeSpecifier
    return_spec: TypeSpecifier


@dataclass(frozen=True)
class PreparedPayload:
    """Holds data prepared for sending in request"""

    data: Union[str, bytes, None] = None
    headers: Optional[Mapping[str, Any]] = None
    files: Optional[Dict[str, Tuple[str, BufferedReader]]] = None


class APIEndpointClientResponse(Protocol):
    """
    Interface to response object. Fits "requests.Response"
    but set of methods is minimal to allow easy migration to another client if needed
    """

    @property
    def text(self) -> str:
        ...

    @property
    def content(self) -> bytes:
        ...

    def dataobj(self, cls: Type[T], sourcekey: Optional[str]) -> T:
        ...

    def dataseq(self, cls: Type[T], sourcekey: Optional[str]) -> DataSequence[T]:
        ...

    def json(self) -> dict:
        ...


class APIEndpointClient(Protocol):
    """
    Interface to client object.
    We only need a 'request' function and few vmanage session properties obtained from server.
    Matched to fit "requests.Session" but migration to other client is possible.
    At his point not very clean as injection of custom kwargs is possible (and sometimes used)
    """

    def request(self, method: str, url: str, **kwargs) -> APIEndpointClientResponse:
        ...

    @property
    def api_version(self) -> Optional[Version]:
        ...

    @property
    def session_type(self) -> Optional[SessionType]:
        ...


class APIEndpoints:
    """
    Class to be used as base for all API endpoints.
    Injects BASE_PATH url prefix as it is common for all known vManage API endpoints.
    Introduces special keyword argument 'payload' in request call and handles sending of such object.
    """

    @classmethod
    def _prepare_payload(cls, payload: PayloadType) -> PreparedPayload:
        """Helper method to prepare data for sending based on type"""
        if isinstance(payload, (str, bytes)):
            return PreparedPayload(data=payload)
        elif isinstance(payload, dict):
            return PreparedPayload(data=json.dumps(payload), headers={"content-type": "application/json"})
        elif isinstance(payload, BaseModel):
            return cls._prepare_basemodel_payload(payload)
        elif isinstance(payload, AttrsInstance):
            return cls._prepare_attrs_payload(payload)
        elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
            return cls._prepare_sequence_payload(payload)
        elif isinstance(payload, CustomPayloadType):
            return payload.prepared()
        else:
            raise APIRequestPayloadTypeError(payload)

    @classmethod
    def _prepare_basemodel_payload(cls, payload: BaseModel) -> PreparedPayload:
        """Helper method to prepare BaseModel instance for sending"""
        return PreparedPayload(
            data=payload.json(exclude_none=True, by_alias=True), headers={"content-type": "application/json"}
        )

    @classmethod
    def _prepare_attrs_payload(cls, payload: AttrsInstance) -> PreparedPayload:
        """Helper method to prepare AttrsInstance for sending"""
        return PreparedPayload(data=json.dumps(attrs_asdict(payload)), headers={"content-type": "application/json"})

    @classmethod
    def _prepare_sequence_payload(cls, payload: Iterable[Union[BaseModel, AttrsInstance]]) -> PreparedPayload:
        """Helper method to prepare sequences for sending"""
        items = []
        for item in payload:
            if isinstance(item, BaseModel):
                items.append(item.dict(exclude_none=True, by_alias=True))
            elif isinstance(item, AttrsInstance):
                items.append(attrs_asdict(item))
        data = json.dumps(items)
        return PreparedPayload(data=data, headers={"content-type": "application/json"})

    @classmethod
    def _prepare_params(cls, params: RequestParamsType) -> Dict[str, Any]:
        """Helper method to prepare params for sending"""
        if isinstance(params, BaseModel):
            return params.dict(exclude_none=True, by_alias=True)
        return params

    def __init__(self, client: APIEndpointClient):
        self._client = client
        self._basepath = BASE_PATH

    def _request(
        self,
        method: str,
        url: str,
        payload: Optional[ModelPayloadType] = None,
        params: Optional[RequestParamsType] = None,
        **kwargs,
    ) -> APIEndpointClientResponse:
        """Prepares and sends request using client protocol"""
        _kwargs = dict(kwargs)
        if payload is not None:
            _kwargs.update(
                asdict(self._prepare_payload(payload), dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
            )  # optional fields set to None will not be inserted to _kwargs
        if params is not None:
            _kwargs.update({"params": self._prepare_params(params)})
        return self._client.request(method, self._basepath + url, **_kwargs)

    @property
    def _api_version(self) -> Optional[Version]:
        return self._client.api_version

    @property
    def _session_type(self) -> Optional[SessionType]:
        return self._client.session_type


class APIEndpointsDecorator:
    @classmethod
    def get_check_instance(cls, _self, *args, **kwargs) -> APIEndpoints:
        """Gets wrapped function instance (first argument)"""
        if not isinstance(_self, APIEndpoints):
            raise APIEndpointError("Only APIEndpointsDecorator instance methods can be annotated with @{cls} decorator")
        return _self


class versions(APIEndpointsDecorator):
    """
    Decorator to annotate endpoints with supported versions.
    Logs warning or raises exception when incompatibility found during runtime.
    """

    meta_lookup: ClassVar[Dict[Any, SpecifierSet]] = {}  # maps decorated method instance to it's supported verisions

    def __init__(self, supported_versions: str, raises: bool = False):
        self.supported_versions = SpecifierSet(supported_versions)
        self.raises = raises

    def __call__(self, func):
        self.meta_lookup[func] = self.supported_versions

        def wrapper(*args, **kwargs):
            """Executes each time decorated method is called"""
            _self = self.get_check_instance(*args, **kwargs)  # _self refers to APIEndpoints instance
            current = _self._api_version
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


class view(APIEndpointsDecorator):
    """
    Decorator to annotate endpoints with session type (view) restriction
    Logs warning or raises exception when incompatibility found during runtime.
    """

    meta_lookup: ClassVar[Dict[Any, Set[SessionType]]] = {}  # maps decorated method instance to it's allowed sessions

    def __init__(self, allowed_session_types: Set[SessionType], raises: bool = False):
        self.allowed_session_types = allowed_session_types
        self.raises = raises

    def __call__(self, func):
        self.meta_lookup[func] = self.allowed_session_types

        def wrapper(*args, **kwargs):
            """Executes each time decorated method is called"""
            _self = self.get_check_instance(*args, **kwargs)  # _self refers to APIEndpoints instance
            current = _self._session_type
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


class request(APIEndpointsDecorator):
    """
    Decorator to annotate endpoints with HTTP method, URL and optionally json key from which
    modelled data will be parsed (usually "data", but defaults to whole json payload).
    Additional kwargs can be injected which will be passed to request method (eg. custom headers)

    Decorated method parameters and return type annotations are checked:

        Parameters:

            "payload": argument with that name is used to send data in request
            usually it is user defined subclass of: pydantic.BaseModel
            other types are also supported please check: vmngclient.endpoints.PayloadType

            "params": argument with that name is used to generate url query string
            supports Dict[str, str] and pydantic.BaseModel

            other parameter must be strings and are used to format url.

        Return Type:

            supports types defined in: vmngclient.endpoints.ReturnType

    Raises:
        APIEndpointError: when decorated method has unsupported parameters or response type
    """

    forbidden_url_field_names = {"self", "payload", "params"}
    meta_lookup: ClassVar[
        Dict[Any, APIEndpointRequestMeta]
    ] = {}  # maps decorated method instance to it's meta information

    def __init__(self, http_method: str, url: str, resp_json_key: Optional[str] = None, **kwargs):
        self.http_method = http_method
        formatter = Formatter()
        url_field_names = {item[1] for item in formatter.parse(url) if item[1] is not None}
        if self.forbidden_url_field_names & url_field_names:
            APIEndpointError(f"One of forbidden fields names: {self.forbidden_url_field_names} found in url: {url}")
        self.url = url
        self.url_field_names = url_field_names
        self.resp_json_key = resp_json_key
        self.return_spec = TypeSpecifier(False)
        self.payload_spec = TypeSpecifier(False)
        self.kwargs = kwargs

    def specify_return_type(self) -> TypeSpecifier:
        """Specifies return type based on decorated method signature annotations.
        Does basic checking of annotated types so problems can be detected early.

        Raises:
            APIEndpointError: when signature contains unexpected return annotation

        Returns:
            TypeSpecifier: Specification of return type
        """
        annotation = self.sig.return_annotation
        if (type_origin := get_origin(annotation)) and isclass(type_origin) and issubclass(type_origin, DataSequence):
            if (
                (type_args := get_args(annotation))
                and (len(type_args) == 1)
                and isclass(type_args[0])
                and issubclass(type_args[0], (BaseModel, DataclassBase))
            ):
                return TypeSpecifier(True, DataSequence, type_args[0])
            raise APIEndpointError(f"Expected: {ReturnType} but return type {annotation}")
        elif isclass(annotation):
            try:
                if issubclass(annotation, (bytes, str, dict, BinaryIO, BaseModel, DataclassBase)):
                    return TypeSpecifier(True, None, annotation)
                elif annotation == _empty:
                    return TypeSpecifier(False)
                raise APIEndpointError(f"Expected: {ReturnType} but return type {annotation}")
            except TypeError:
                raise APIEndpointError(f"Expected: {ReturnType} but return type {annotation}")
        else:
            raise APIEndpointError(f"Expected: {ReturnType} but return type {annotation}")

    def specify_payload_type(self) -> TypeSpecifier:
        """Specifies payload type based on decorated method signature annotations.
        Does basic checking of annotated types for 'payload' so problems can be detected early.

        Raises:
            APIEndpointError: when signature contains unexpected payload annotation

        Returns:
            TypeSpecifier: Specification of payload type
        """
        payload_param = self.sig.parameters.get("payload")
        if not payload_param:
            return TypeSpecifier(False)
        annotation = payload_param.annotation
        if isclass(annotation):
            if issubclass(annotation, (bytes, str, dict, BinaryIO, BaseModel, DataclassBase, CustomPayloadType)):
                return TypeSpecifier(True, None, annotation)
            else:
                raise APIEndpointError(f"'payload' param must be annotated with supported type: {PayloadType}")
        elif (type_origin := get_origin(annotation)) and isclass(type_origin) and issubclass(type_origin, Sequence):
            if (
                (type_args := get_args(annotation))
                and (len(type_args) == 1)
                and isclass(type_args[0])
                and issubclass(type_args[0], (BaseModel, DataclassBase))
            ):
                return TypeSpecifier(True, annotation, type_args[0])
            raise APIEndpointError(f"Expected: {PayloadType} but found payload {annotation}")
        else:
            raise APIEndpointError(f"Expected: {PayloadType} but found payload {annotation}")

    def check_params(self):
        """Checks params in decorated method definition

        Raises:
            APIEndpointError: when decorated params not matching specification
        """
        parameters = self.sig.parameters

        if params_param := parameters.get("params"):
            if not (isclass(params_param.annotation) and issubclass(params_param.annotation, (BaseModel, Dict))):
                raise APIEndpointError(f"'params' param must be annotated with supported type: {RequestParamsType}")

        general_purpose_arg_names = {
            key for key in self.sig.parameters.keys() if key not in self.forbidden_url_field_names
        }
        if missing := self.url_field_names.difference(general_purpose_arg_names):
            raise APIEndpointError(f"Missing parameters: {missing} to format url: {self.url}")

        for parameter in [parameters.get(name) for name in self.url_field_names]:
            if not (isclass(parameter.annotation) and parameter.annotation == str):
                raise APIEndpointError(f"Parameter {parameter} used for url formatting must have 'str' type annotation")

        no_purpose_params = {
            parameters.get(name) for name in general_purpose_arg_names.difference(self.url_field_names)
        }
        if no_purpose_params:
            raise APIEndpointError(
                f"Parameters {no_purpose_params} are not used as "
                "request payload, request params nor to format url string!"
                "remove unused parameter or fix by changing argument to purposeful name 'payload' or 'params'"
            )

    def merge_args(self, positional_args: Tuple, keyword_args: Dict[str, Any]) -> Dict[str, Any]:
        """Merges decorated method args and kwargs into one dictionary.
        This is needed to identify all decorated method arguments by name inside wrapper body.
        We can learn all arguments names from signature.

        Returns: Dict[str, Any]: all passed args as keyword arguments (excluding "self")
        """
        all_args_names = [key for key in self.sig.parameters.keys()]
        all_args_dict = dict(zip(all_args_names, positional_args))
        all_args_dict.update(keyword_args)
        all_args_dict.pop("self", None)
        return all_args_dict

    def __call__(self, func):
        self.sig = signature(func)
        self.return_spec = self.specify_return_type()
        self.payload_spec = self.specify_payload_type()
        self.check_params()
        self.meta_lookup[func] = APIEndpointRequestMeta(
            http_request=f"{self.http_method} {self.url}", payload_spec=self.payload_spec, return_spec=self.return_spec
        )

        def wrapper(*args, **kwargs):
            """Executes each time decorated method is called"""
            _self = self.get_check_instance(*args, **kwargs)  # _self refers to APIEndpoints instance
            _kwargs = self.merge_args(args, kwargs)
            payload = _kwargs.get("payload")
            params = _kwargs.get("params")
            formatted_url = self.url.format(**_kwargs)
            response = _self._request(self.http_method, formatted_url, payload=payload, params=params, **self.kwargs)
            if self.return_spec.present:
                if issubclass(self.return_spec.payload_type, (BaseModel, DataclassBase)):
                    if self.return_spec.sequence_type == DataSequence:
                        return response.dataseq(self.return_spec.payload_type, self.resp_json_key)
                    else:
                        return response.dataobj(self.return_spec.payload_type, self.resp_json_key)
                elif issubclass(self.return_spec.payload_type, str):
                    return response.text
                elif issubclass(self.return_spec.payload_type, bytes):
                    return response.content
                elif issubclass(self.return_spec.payload_type, dict):
                    return response.json()

        return wrapper


get = "GET"
post = "POST"
put = "PUT"
delete = "DELETE"