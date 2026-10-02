# Copyright 2026 Cisco Systems, Inc. and its affiliates

import pytest
from pydantic import ValidationError

from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.preferred_color_group import (
    PreferredColorGroupParcel,
)


def test_create_preferred_color_group_parcel():
    # Arrange / Act
    parcel = PreferredColorGroupParcel(parcel_name="test")
    parcel.add_primary(["gold", "silver"], "direct-path")
    parcel.add_secondary(["bronze"], None)
    parcel.add_tertiary([], "all-paths")

    # Assert
    assert len(parcel.entries) == 1
    entry = parcel.entries[0]

    assert entry.primary_preference.color_preference is not None
    assert entry.primary_preference.color_preference.value == ["gold", "silver"]
    assert entry.primary_preference.path_preference is not None
    assert entry.primary_preference.path_preference.value == "direct-path"

    assert entry.secondary_preference is not None
    assert entry.secondary_preference.color_preference is not None
    assert entry.secondary_preference.color_preference.value == ["bronze"]
    assert entry.secondary_preference.path_preference is None

    assert entry.tertiary_preference is not None
    assert entry.tertiary_preference.color_preference is None
    assert entry.tertiary_preference.path_preference is not None
    assert entry.tertiary_preference.path_preference.value == "all-paths"


def test_index_error_on_creating_secondary_without_primary():
    parcel = PreferredColorGroupParcel(parcel_name="test")
    with pytest.raises(IndexError):
        parcel.add_secondary(["blue"], "all-paths")


def test_index_error_on_creating_teritary_without_secondary():
    parcel = PreferredColorGroupParcel(parcel_name="test")
    parcel.add_primary(["gold", "silver"], "direct-path")
    with pytest.raises(IndexError):
        parcel.add_tertiary(["blue"], "all-paths")


def test_validation_error_on_missing_one_of_preferences():
    parcel = PreferredColorGroupParcel(parcel_name="test")
    with pytest.raises(ValidationError):
        parcel.add_primary([], None)
