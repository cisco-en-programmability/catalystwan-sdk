# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import Literal, Union

import pytest
from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.exceptions import ModelNotFound
from catalystwan.models.configuration.feature_profile.parcel import find_type, list_types
from catalystwan.models.configuration.feature_profile.sdwan.topology import (
    AnyTopologyParcel,
    CustomControlParcel,
    HubSpokeParcel,
    MeshParcel,
)


def test_list_types():
    observed_types = list_types(AnyTopologyParcel)
    assert set(observed_types) == {MeshParcel, HubSpokeParcel, CustomControlParcel}


def test_find_type():
    observed_type = find_type("mesh", AnyTopologyParcel)
    assert observed_type == MeshParcel


def test_find_type_raises_when_no_match():
    with pytest.raises(ModelNotFound):
        find_type("unknown", AnyTopologyParcel)


def test_find_type_raises_for_bogus_param():
    with pytest.raises(ModelNotFound):
        find_type("unknown", None)


def test_find_type_custom():
    # Arrange
    class CustomParcel(_ParcelBase):
        type_: Literal["custom"] = Field(default="custom", exclude=True)

    CustomUnion = Annotated[
        Union[
            MeshParcel,
            CustomParcel,
        ],
        Field(discriminator="type_"),
    ]
    # Act
    observed_type = find_type("custom", CustomUnion)
    # Assert
    assert observed_type == CustomParcel
