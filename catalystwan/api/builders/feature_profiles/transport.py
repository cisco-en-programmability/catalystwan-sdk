# Copyright 2023 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID, uuid4

from catalystwan.api.builders.feature_profiles.mixins import TrackerMixin
from catalystwan.api.builders.feature_profiles.report import (
    FeatureProfileBuildReport,
    hande_failed_sub_parcel,
    handle_association_request,
    handle_create_parcel,
)
from catalystwan.api.feature_profile_api import TransportFeatureProfileAPI
from catalystwan.endpoints.configuration.feature_profile.sdwan.transport import TransportFeatureProfile
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.parcel import ParcelAssociationPayload
from catalystwan.models.configuration.feature_profile.sdwan.routing import AnyRoutingParcel
from catalystwan.models.configuration.feature_profile.sdwan.trackers import Tracker, TrackerGroup
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    AnyTransportParcel,
    AnyTransportSuperParcel,
    AnyTransportVpnParcel,
    AnyTransportVpnSubParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import CellularProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsParcel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class TransportAndManagementProfileBuilder(TrackerMixin):
    """
    A class for building system feature profiles.
    """

    def __init__(self, session: ManagerSession) -> None:
        """
        Initialize a new instance of the Service class.

        Args:
            session (ManagerSession): The ManagerSession object used for API communication.
            profile_uuid (UUID): The UUID of the profile.
        """
        self._profile: FeatureProfileCreationPayload
        self._api = TransportFeatureProfileAPI(session)
        self._endpoints = TransportFeatureProfile(session)
        self._independent_items: List[AnyTransportSuperParcel] = []
        self._independent_items_vpns: Dict[UUID, AnyTransportVpnParcel] = {}
        self._independent_items_cellular_controllers: Dict[UUID, CellularControllerParcel] = {}
        self._dependent_items_on_vpns: Dict[UUID, List[Tuple[UUID, AnyTransportVpnSubParcel]]] = defaultdict(list)
        self._dependent_routing_items_on_vpns: Dict[UUID, List[AnyRoutingParcel]] = defaultdict(list)
        self._dependent_items_on_cellular_controllers: Dict[
            UUID, List[Union[CellularProfileParcel, GpsParcel]]
        ] = defaultdict(list)
        # Trackers
        self.init_tracker()

    def add_profile_name_and_description(self, feature_profile: FeatureProfileCreationPayload) -> None:
        """
        Adds a name and description to the feature profile.

        Args:
            name (str): The name of the feature profile.
            description (str): The description of the feature profile.

        Returns:
            None
        """
        self._profile = feature_profile

    def add_parcel(self, parcel: AnyTransportSuperParcel) -> None:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnyTransportSuperParcel): The parcel to add.

        Returns:
            None
        """
        self._independent_items.append(parcel)

    def add_parcel_routing_attached(self, vpn_tag: UUID, parcel: AnyRoutingParcel) -> None:
        """
        Adds a routing parcel to the feature profile.

        Args:
            parcel (AnyRoutingParcel): The parcel to add.

        Returns:
            None
        """
        logger.debug(f"Attaching routing {parcel.parcel_name} with to VPN with tag {vpn_tag}")
        self._dependent_routing_items_on_vpns[vpn_tag].append(parcel)

    def add_parcel_vpn(self, parcel: AnyTransportVpnParcel) -> UUID:
        """
        Adds a VPN parcel to the builder.

        Args:
            parcel (LanVpnParcel): The VPN parcel to add.

        Returns:
            UUID: The UUID tag of the added VPN parcel.
        """
        vpn_tag = uuid4()
        logger.debug(f"Adding VPN parcel {parcel.parcel_name} with tag {vpn_tag}")
        self._independent_items_vpns[vpn_tag] = parcel
        return vpn_tag

    def add_parcel_cellular_controller(self, parcel: CellularControllerParcel) -> UUID:
        """
        Adds a cellular controller parcel to the builder.

        Args:
            parcel (CellularControllerParcel): The cellular controller parcel to add.

        Returns:
            UUID: The UUID tag of the added cellular controller parcel.
        """
        cellular_controller_tag = uuid4()
        logger.debug(f"Adding cellular controller parcel {parcel.parcel_name} with tag {cellular_controller_tag}")
        self._independent_items_cellular_controllers[cellular_controller_tag] = parcel
        return cellular_controller_tag

    def add_cellular_controller_subparcel(
        self, cellular_controller_tag: UUID, parcel: Union[CellularProfileParcel, GpsParcel]
    ) -> None:
        """
        Adds a subparcel to the cellular controller parcel.

        Args:
            cellular_controller_tag (UUID): The UUID of the cellular controller.
            parcel (Union[CellularProfileParcel, GpsParcel]): The subparcel to add.

        Returns:
            None
        """
        self._dependent_items_on_cellular_controllers[cellular_controller_tag].append(parcel)

    def add_vpn_subparcel(self, vpn_tag: UUID, parcel: AnyTransportVpnSubParcel) -> UUID:
        """
        Adds a parcel to the feature profile.

        Args:
            parcel (AnyTransportVpnSubParcel): The parcel to add.

        Returns:
            None
        """
        subparcel_tag = uuid4()
        logger.debug(f"Adding vpn sub-parcel {parcel.parcel_name} with tag {vpn_tag}")
        self._dependent_items_on_vpns[vpn_tag].append((subparcel_tag, parcel))
        return subparcel_tag

    def add_tracker(self, associate_tags: Set[UUID], tracker: Tracker) -> None:
        """
        Adds a tracker parcel to the feature profile.

        Args:
            associate_tags (Set[UUID]): The UUIDs of the interfaces to which the tracker should be added.
            tracker (Tracker): The tracker parcel to add.

        Returns:
            None
        """
        self._trackers.append((associate_tags, tracker))

    def add_tracker_group(self, associate_tags: Set[UUID], group: TrackerGroup, trackers: List[Tracker]) -> None:
        self._tracker_groups.append((associate_tags, group, trackers))

    def build(self) -> FeatureProfileBuildReport:
        """
        Builds the feature profile.

        Returns:
            UUID: The UUID of the created feature profile.
        """

        profile_uuid = self._endpoints.create_transport_feature_profile(self._profile).id
        self.build_report = FeatureProfileBuildReport(profile_uuid=profile_uuid, profile_name=self._profile.name)
        for parcel in self._independent_items:
            self._create_parcel(profile_uuid, parcel)

        self.create_trackers(profile_uuid=profile_uuid)

        for vpn_tag, vpn_parcel in self._independent_items_vpns.items():
            vpn_uuid = self._create_parcel(profile_uuid, vpn_parcel)
            for vpn_subparcel_tag, vpn_subparcel in self._dependent_items_on_vpns[vpn_tag]:
                if vpn_uuid is None:
                    hande_failed_sub_parcel(self.build_report, vpn_parcel, vpn_subparcel)
                else:
                    vpn_subparcel_uuid = self._create_parcel(profile_uuid, vpn_subparcel, vpn_uuid)

                    # Associate tracker with VPN interface if it exists
                    if vpn_subparcel_tag in self._interface_tag_to_existing_tracker and vpn_subparcel_uuid:
                        tracker_uuid, tracker_type = self._interface_tag_to_existing_tracker[vpn_subparcel_tag]
                        vpn_subparcel_type = (
                            vpn_subparcel._get_parcel_type().replace("wan/vpn/", "").replace("management/vpn/", "")
                        )
                        with handle_association_request(self.build_report, vpn_subparcel):
                            self._endpoints.associate_tracker_with_vpn_interface(
                                profile_uuid,
                                vpn_uuid,
                                vpn_subparcel_type,
                                vpn_subparcel_uuid,
                                tracker_type,
                                ParcelAssociationPayload(parcel_id=tracker_uuid),
                            )

            for routing_parcel in self._dependent_routing_items_on_vpns[vpn_tag]:
                if vpn_uuid is None:
                    hande_failed_sub_parcel(self.build_report, vpn_parcel, routing_parcel)
                else:
                    routing_uuid = self._create_parcel(profile_uuid, routing_parcel)
                    if not routing_uuid:
                        continue
                    with handle_association_request(self.build_report, routing_parcel):
                        self._endpoints.associate_with_vpn(
                            profile_uuid,
                            vpn_uuid,
                            routing_parcel._get_parcel_type(),
                            payload=ParcelAssociationPayload(parcel_id=routing_uuid),
                        )

        for cellular_controller_tag, cellular_controller_parcel in self._independent_items_cellular_controllers.items():
            controller_uuid = self._create_parcel(profile_uuid, cellular_controller_parcel)
            for cellular_subparcel in self._dependent_items_on_cellular_controllers[cellular_controller_tag]:
                if controller_uuid is None:
                    hande_failed_sub_parcel(self.build_report, cellular_controller_parcel, cellular_subparcel)
                else:
                    parcel_uuid = self._create_parcel(profile_uuid, cellular_subparcel)
                    if not parcel_uuid:
                        continue
                    with handle_association_request(self.build_report, cellular_subparcel):
                        self._endpoints.associate_with_cellular_controller(
                            profile_uuid,
                            controller_uuid,
                            cellular_subparcel._get_parcel_type(),
                            ParcelAssociationPayload(parcel_id=parcel_uuid),
                        )

        return self.build_report

    @handle_create_parcel
    def _create_parcel(self, profile_uuid: UUID, parcel: AnyTransportParcel, vpn_uuid: Optional[None] = None) -> UUID:
        return self._api.create_parcel(profile_uuid, parcel, vpn_uuid).id
