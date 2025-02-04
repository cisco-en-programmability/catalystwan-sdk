# Copyright 2023 Cisco Systems, Inc. and its affiliates
import functools
from typing import Any, List, Optional, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from requests import PreparedRequest, Request, Response

from catalystwan.exceptions import ManagerErrorInfo, ManagerHTTPError
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel


def handle_build_report(func):
    """Wrapper to make creating report simple and keep it DRY."""

    @functools.wraps(func)
    def wrapper(self, profile_uuid: UUID, parcel: AnyParcel, *args, **kwargs) -> Optional[UUID]:
        try:
            uuid = func(self, profile_uuid, parcel, *args, **kwargs)
            self.build_report.add_created_parcel(parcel.parcel_name, uuid)
            return uuid
        except ManagerHTTPError as e:
            self.build_report.add_failed_parcel(
                parcel_name=parcel.parcel_name,
                parcel_type=parcel._get_parcel_type(),
                error=e,
            )
            return None

    return wrapper


class FailedRequestDetails(BaseModel):
    method: str
    url: str
    body: str

    @classmethod
    def from_request(cls, request: Union[Request, PreparedRequest, Any]) -> "FailedRequestDetails":
        if isinstance(request, (Request, PreparedRequest)):
            return cls(
                method=str(request.method),
                url=str(request.url),
                body=str(request.body if hasattr(request, "body") else ""),
            )
        return cls.as_empty()

    @classmethod
    def as_empty(cls) -> "FailedRequestDetails":
        return cls(method="", url="", body="")


class ResponseDetails(BaseModel):
    status_code: int
    reason: str

    @classmethod
    def from_response(cls, response: Union[Response, Any]) -> "ResponseDetails":
        if isinstance(response, Response):
            return cls(status_code=response.status_code, reason=response.reason)
        return cls.as_empty()

    @classmethod
    def as_empty(cls) -> "ResponseDetails":
        return cls(status_code=-1, reason="")


class FailedParcel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parcel_name: str = Field(serialization_alias="parcelName", validation_alias="parcelName")
    parcel_type: str = Field(serialization_alias="parcelType", validation_alias="parcelType")
    error_info: Union[ManagerErrorInfo, str] = Field(serialization_alias="errorInfo", validation_alias="errorInfo")
    request_details: Optional[FailedRequestDetails] = Field(
        default=None, serialization_alias="requestDetails", validation_alias="requestDetails"
    )
    response_details: Optional[ResponseDetails] = Field(
        default=None, serialization_alias="responseDetails", validation_alias="responseDetails"
    )

    @classmethod
    def from_error(
        cls,
        parcel_name: str,
        parcel_type: str,
        error: ManagerHTTPError,
    ):
        return cls(
            parcel_name=parcel_name,
            parcel_type=parcel_type,
            error_info=error.info,
            request_details=FailedRequestDetails.from_request(error.request),
            response_details=ResponseDetails.from_response(error.response),
        )


class FeatureProfileBuildReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    profile_name: str = Field(serialization_alias="profileName", validation_alias="profileName")
    profile_uuid: UUID = Field(serialization_alias="profileUuid", validation_alias="profileUuid")
    created_parcels: List[Tuple[str, UUID]] = Field(
        default_factory=list, serialization_alias="createdParcels", validation_alias="createdParcels"
    )
    failed_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="failedParcels", validation_alias="failedParcels"
    )

    def add_created_parcel(self, parcel_name: str, parcel_uuid: UUID) -> None:
        self.created_parcels.append((parcel_name, parcel_uuid))

    def add_failed_parcel(
        self,
        parcel_name: str,
        parcel_type: str,
        error: ManagerHTTPError,
    ) -> None:
        self.failed_parcels.append(
            FailedParcel.from_error(
                parcel_name=parcel_name,
                parcel_type=parcel_type,
                error=error,
            )
        )


def handle_build_report_for_failed_subparcel(
    build_report: FeatureProfileBuildReport, parent: AnyParcel, subparcel: AnyParcel
) -> None:
    parent_failed_to_create_message = (
        f"Parent parcel: {parent.parcel_name} failed to create. This subparcel is dependent on it."
    )
    build_report.failed_parcels.append(
        FailedParcel(
            parcel_name=subparcel.parcel_name,
            parcel_type=subparcel._get_parcel_type(),
            error_info=parent_failed_to_create_message,
        ),
    )
