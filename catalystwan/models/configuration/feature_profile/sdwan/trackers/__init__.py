# Copyright 2025 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.trackers.tracker import (
    EndpointTcpUdp,
    EndpointTrackerType,
    Tracker,
    TrackerIPv6,
)
from catalystwan.models.configuration.feature_profile.sdwan.trackers.tracker_group import (
    TrackerGroup,
    TrackerGroupIPv6,
    TrackerRefs,
)

AnyTrackerParcel = Annotated[
    Union[Tracker, TrackerIPv6, TrackerGroup, TrackerGroupIPv6],
    Field(discriminator="type_"),
]
__all__ = [
    "Tracker",
    "TrackerIPv6",
    "EndpointTcpUdp",
    "EndpointTrackerType",
    "TrackerGroup",
    "TrackerGroupIPv6",
    "TrackerRefs",
    "AnyTrackerParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
