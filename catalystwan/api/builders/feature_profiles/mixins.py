# Copyright 2023 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Dict, List, Set, Tuple
from uuid import UUID

from catalystwan.models.configuration.feature_profile.sdwan.trackers import Tracker, TrackerGroup


class TrackerMixin:
    def init_tracker(self) -> None:
        self._shared_trackers: Dict[str, UUID] = {}
        self._trackers: List[Tuple[Set[UUID], Tracker]] = []
        self._tracker_groups: List[Tuple[Set[UUID], TrackerGroup, List[Tracker]]] = []
        self._interface_tag_to_existing_tracker: Dict[UUID, Tuple[UUID, str]] = {}

    def _create_parcel(self, profile_uuid: UUID, tracker: Tracker | TrackerGroup) -> UUID:
        raise NotImplementedError()

    def create_trackers(self, profile_uuid: UUID) -> None:
        for tracker_group_tags, tracker_group, trackers in self._tracker_groups:
            trackers_uuids: List[UUID] = []
            for tracker_ in trackers:
                tracker_uuid = self._create_parcel(profile_uuid, tracker_)
                if tracker_uuid:
                    trackers_uuids.append(tracker_uuid)
                    self._shared_trackers[tracker_.parcel_name] = tracker_uuid

            for tracker_uuid in trackers_uuids:
                tracker_group.add_ref(tracker_uuid)

            tracker_group_uuid = self._create_parcel(profile_uuid, tracker_group)
            if tracker_group_uuid:
                for tag in tracker_group_tags:
                    self._interface_tag_to_existing_tracker[tag] = tracker_group_uuid, tracker_group._get_parcel_type()

        for tracker_tags, tracker in self._trackers:
            if tracker.parcel_name in self._shared_trackers:
                created_tracker_uuid = self._shared_trackers[tracker.parcel_name]
            else:
                created_tracker_uuid = self._create_parcel(profile_uuid, tracker)
            if created_tracker_uuid:
                for tag in tracker_tags:
                    self._interface_tag_to_existing_tracker[tag] = (created_tracker_uuid, tracker._get_parcel_type())
