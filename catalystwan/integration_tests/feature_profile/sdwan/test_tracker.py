# Copyright 2025 Cisco Systems, Inc. and its affiliates
from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI, TransportFeatureProfileAPI
from catalystwan.integration_tests.base import TestCaseBase, create_name_with_run_id
from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.trackers import Tracker, TrackerGroup
from catalystwan.models.configuration.feature_profile.sdwan.trackers.tracker_group import TrackerRefs


class TestTransportFeatureProfileTracker(TestCaseBase):
    api: TransportFeatureProfileAPI

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile(create_name_with_run_id("TestTransportModels"), "Description").id

    def test_create_tracker(self):
        tracker = Tracker(
            parcel_name="TestTracker",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        response = self.api.create_parcel(self.profile_uuid, tracker)

        assert response

    def test_create_tracker_group(self):
        tracker1 = Tracker(
            parcel_name="TestTracker1",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker1"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        tracker2 = Tracker(
            parcel_name="TestTracker2",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker2"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        tracker1_uuid = self.api.create_parcel(self.profile_uuid, tracker1).id
        tracker2_uuid = self.api.create_parcel(self.profile_uuid, tracker2).id
        tracker_group = TrackerGroup(
            parcel_name="TestTrackerGroup",
            parcel_description="Test Tracker Group Description",
            tracker_refs=[
                TrackerRefs(tracker_ref=RefIdItem(ref_id=Global[str](value=str(tracker1_uuid)))),
                TrackerRefs(tracker_ref=RefIdItem(ref_id=Global[str](value=str(tracker2_uuid)))),
            ],
        )

        response = self.api.create_parcel(self.profile_uuid, tracker_group)

        assert response

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()


class TestServiceFeatureProfileModels(TestCaseBase):
    api: ServiceFeatureProfileAPI

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.service
        cls.profile_uuid = cls.api.create_profile(create_name_with_run_id("TestProfileService"), "Description").id

    def test_create_tracker(self):
        tracker = Tracker(
            parcel_name="TestTracker",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        response = self.api.create_parcel(self.profile_uuid, tracker)

        assert response

    def test_create_tracker_group(self):
        tracker1 = Tracker(
            parcel_name="TestTracker1",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker1"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        tracker2 = Tracker(
            parcel_name="TestTracker2",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker2"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )

        tracker1_uuid = self.api.create_parcel(self.profile_uuid, tracker1).id
        tracker2_uuid = self.api.create_parcel(self.profile_uuid, tracker2).id
        tracker_group = TrackerGroup(
            parcel_name="TestTrackerGroup",
            parcel_description="Test Tracker Group Description",
            tracker_refs=[
                TrackerRefs(tracker_ref=RefIdItem(ref_id=Global[str](value=str(tracker1_uuid)))),
                TrackerRefs(tracker_ref=RefIdItem(ref_id=Global[str](value=str(tracker2_uuid)))),
            ],
        )

        response = self.api.create_parcel(self.profile_uuid, tracker_group)

        assert response

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
