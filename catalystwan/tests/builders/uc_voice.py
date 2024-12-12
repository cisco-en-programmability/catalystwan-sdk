# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from typing import List
from unittest.mock import MagicMock
from uuid import uuid4

from catalystwan.api.builders.feature_profiles.uc_voice import UcVoiceFeatureProfileBuilder
from catalystwan.api.configuration_groups.parcel import as_default, as_global
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class BaseModel:
    def __init__(self, **kwargs):
        self.model_fields_set = set(kwargs.keys())
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestUcVoiceFeatureProfileBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = UcVoiceFeatureProfileBuilder(session=MagicMock())
        self.builder._pushed_associable_parcels = {
            "p1_name": uuid4(),
            "p2_name": uuid4(),
        }

    def test_populate_association_with_matching_fields(self):
        association = [
            BaseModel(
                media_profile=RefIdItem(ref_id=as_global("p2_name")),
                server_group=RefIdItem(ref_id=as_global("p1_name")),
            ),
        ]

        self.builder._populate_association(association)

        # Assert that matching fields are updated
        self.assertEqual(
            association[0].media_profile.ref_id.value, str(self.builder._pushed_associable_parcels["p2_name"])
        )
        self.assertEqual(
            association[0].server_group.ref_id.value, str(self.builder._pushed_associable_parcels["p1_name"])
        )

    def test_populate_association_with_no_matching_fields(self):
        association = [BaseModel(translation_profile=RefIdItem(ref_id=as_global("non_matching_field")))]

        self.builder._populate_association(association)

        # Assert that no changes are made for non-matching fields
        self.assertEqual(association[0].translation_profile.ref_id, as_default(None))

    def test_populate_association_partial_matching_fields(self):
        association = [
            BaseModel(
                media_profile=RefIdItem(ref_id=as_global("p2_name")),
                supervisory_disconnect=RefIdItem(ref_id=as_global("non_existent_field")),
            )
        ]

        self.builder._populate_association(association)

        # Assert that only matching fields are updated
        self.assertEqual(
            association[0].media_profile.ref_id.value, str(self.builder._pushed_associable_parcels["p2_name"])
        )
        self.assertEqual(association[0].supervisory_disconnect.ref_id, as_default(None))

    def test_populate_association_with_empty_association(self):
        association: List[BaseModel] = []

        self.builder._populate_association(association)

        # Assert no errors occur and nothing is changed
        self.assertEqual(len(association), 0)

    def test_populate_association_with_no_pushed_parcels(self):
        self.builder._pushed_associable_parcels = {}

        association = [BaseModel(media_profile=RefIdItem(ref_id=as_global("p3_name")))]

        self.builder._populate_association(association)

        # Assert that fields are changed to default none when the name is missing
        self.assertEqual(association[0].media_profile.ref_id, as_default(None))
