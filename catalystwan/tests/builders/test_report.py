# Copyright 2025 Cisco Systems, Inc. and its affiliates
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport, handle_association_request
from catalystwan.exceptions import ManagerErrorInfo, ManagerHTTPError


def test_handle_association_request_when_http_error_expect_report_failed_parcel_info():
    report = FeatureProfileBuildReport(
        profile_name="test_profile",
        profile_uuid=UUID(int=0),
    )
    parcel = MagicMock(parcel_name="parcel_name", _get_parcel_type=MagicMock(return_value="parcel_type"))

    with handle_association_request(report, parcel):
        raise ManagerHTTPError(
            error_info=ManagerErrorInfo(
                message="Something went wrong",
                details="Something went wrong",
                code="500",
            )
        )

    assert report.failed_parcels[0].parcel_name == "parcel_name"
    assert report.failed_parcels[0].parcel_type == "parcel_type"
    assert report.failed_parcels[0].error_info.message == "Something went wrong"
    assert report.failed_parcels[0].error_info.details == "Something went wrong"
    assert report.failed_parcels[0].error_info.code == "500"


def test_handle_association_request_when_success_expect_no_failed_parcel_info():
    report = FeatureProfileBuildReport(
        profile_name="test_profile",
        profile_uuid=UUID(int=0),
    )
    parcel = MagicMock(parcel_name="parcel_name", _get_parcel_type=MagicMock(return_value="parcel_type"))

    with handle_association_request(report, parcel):
        pass

    assert report.failed_parcels == []


def test_handle_association_request_when_exception_expect_no_raise():
    report = FeatureProfileBuildReport(
        profile_name="test_profile",
        profile_uuid=UUID(int=0),
    )
    parcel = MagicMock(parcel_name="parcel_name", _get_parcel_type=MagicMock(return_value="parcel_type"))

    try:
        with handle_association_request(report, parcel):
            raise Exception("Something went wrong")
    except Exception:
        pytest.fail("Exception was propagated, but should have been suppressed")

    assert report.failed_parcels == []
