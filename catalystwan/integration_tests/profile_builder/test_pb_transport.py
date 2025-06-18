# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address
from typing import Literal

from catalystwan.api.configuration_groups.parcel import Global, Variable
from catalystwan.integration_tests.base import TestCaseBase, create_name_with_run_id
from catalystwan.integration_tests.test_data import (
    bgp_parcel,
    cellular_controller_parcel,
    cellular_profile_parcel,
    gps_parcel,
    ospf_parcel,
    ospfv3ipv4_parcel,
    ospfv3ipv6_parcel,
)
from catalystwan.models.configuration.feature_profile.common import (
    AddressWithMask,
    AdvancedGre,
    FeatureProfileCreationPayload,
    SourceLoopback,
    TunnelSourceType,
)
from catalystwan.models.configuration.feature_profile.sdwan.trackers import Tracker, TrackerGroup
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import TransportVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    InterfaceCellularParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.gre import Basic, InterfaceGreParcel


class TestTransportFeatureProfileBuilder(TestCaseBase):
    def setUp(self) -> None:
        self.fp_name = create_name_with_run_id("FeatureProfileBuilderTransport")
        self.fp_description = "Transport feature profile"
        self.builder = self.session.api.builders.feature_profiles.create_builder("transport")
        self.builder.add_profile_name_and_description(
            feature_profile=FeatureProfileCreationPayload(name=self.fp_name, description=self.fp_description)
        )
        self.api = self.session.api.sdwan_feature_profiles.transport

    def test_when_build_profile_with_cellular_controller_and_subelements_expect_success(self):
        # Arrange
        parent_tag = self.builder.add_parcel_cellular_controller(cellular_controller_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, cellular_profile_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, gps_parcel)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def test_when_build_profile_with_vpn_and_routing_attached_expect_success(self):
        # Arrange
        service_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        vpn_tag = self.builder.add_parcel_vpn(service_vpn_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospf_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospfv3ipv4_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospfv3ipv6_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, bgp_parcel)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def test_when_vpn_interfaces_and_attached_tracker_expect_success(self):
        service_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        vpn_tag = self.builder.add_parcel_vpn(service_vpn_parcel)
        gre_parcel = InterfaceGreParcel(
            parcel_name="InterfaceGreParcel",
            parcel_description="Description",
            basic=Basic(
                address=AddressWithMask(
                    address=Global[IPv4Address](value=IPv4Address("39.5.0.97")),
                    mask=Variable(value="{{QPg11165441vY1}}"),
                ),
                if_name=Global[str](value="gre23"),
                tunnel_destination=Global[IPv4Address](value=IPv4Address("3.3.3.3")),
                clear_dont_fragment=Global[bool](value=True),
                description=Global[str](value="QsLBBBBBCF"),
                mtu=Global[int](value=1500),
                shutdown=Global[bool](value=True),
                tcp_mss_adjust=Global[int](value=600),
                tunnel_source_type=TunnelSourceType(
                    source_loopback=SourceLoopback(
                        tunnel_route_via=Global[str](value="xSVIxuF"),
                        tunnel_source_interface=Global[str](value="YnBabgxBUm"),
                    )
                ),
            ),
            advanced=AdvancedGre(application=Global[Literal["none", "sig"]](value="sig")),
        )
        gre_tag = self.builder.add_vpn_subparcel(vpn_tag, gre_parcel)
        tracker = Tracker(
            parcel_name="TestTracker1",
            parcel_description="Test Tracker Description",
            tracker_name=Global[str](value="TestTracker1"),
            interval=Global[int](value=100),
            endpoint_api_url=Global[str](value="https://example.com/api"),
        )
        self.builder.add_tracker(associate_tags=[gre_tag], tracker=tracker)
        report = self.builder.build()

        assert len(report.failed_parcels) == 0

    def test_when_vpn_interfaces_and_attached_tracker_group_expect_success(self):
        service_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        vpn_tag = self.builder.add_parcel_vpn(service_vpn_parcel)
        cellular_parcel = InterfaceCellularParcel(
            parcel_name="InterfaceCellularParcel",
            parcel_description="Description",
            encapsulation=[],
            interface_description=Global[str](value="CkmMzlz"),
            interface_name=Global[str](value="xnaohVUa"),
            nat=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            tunnel_interface=Global[bool](value=True),
        )
        cellular_tag = self.builder.add_vpn_subparcel(vpn_tag, cellular_parcel)
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
        tracker_group = TrackerGroup(
            parcel_name="TestTrackerGroup",
            parcel_description="Test Tracker Group Description",
            tracker_refs=[],
        )
        self.builder.add_tracker_group(
            associate_tags=[cellular_tag], group=tracker_group, trackers=[tracker1, tracker2]
        )
        report = self.builder.build()

        assert len(report.failed_parcels) == 0

    def test_when_shared_tracker_expect_success(self):
        service_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        vpn_tag = self.builder.add_parcel_vpn(service_vpn_parcel)
        gre_parcel = InterfaceGreParcel(
            parcel_name="InterfaceGreParcel",
            parcel_description="Description",
            basic=Basic(
                address=AddressWithMask(
                    address=Global[IPv4Address](value=IPv4Address("39.5.0.97")),
                    mask=Variable(value="{{QPg11165441vY1}}"),
                ),
                if_name=Global[str](value="gre23"),
                tunnel_destination=Global[IPv4Address](value=IPv4Address("3.3.3.3")),
                clear_dont_fragment=Global[bool](value=True),
                description=Global[str](value="QsLBBBBBCF"),
                mtu=Global[int](value=1500),
                shutdown=Global[bool](value=True),
                tcp_mss_adjust=Global[int](value=600),
                tunnel_source_type=TunnelSourceType(
                    source_loopback=SourceLoopback(
                        tunnel_route_via=Global[str](value="xSVIxuF"),
                        tunnel_source_interface=Global[str](value="YnBabgxBUm"),
                    )
                ),
            ),
            advanced=AdvancedGre(application=Global[Literal["none", "sig"]](value="sig")),
        )
        gre_tag = self.builder.add_vpn_subparcel(vpn_tag, gre_parcel)
        cellular_parcel = InterfaceCellularParcel(
            parcel_name="InterfaceCellularParcel",
            parcel_description="Description",
            encapsulation=[],
            interface_description=Global[str](value="CkmMzlz"),
            interface_name=Global[str](value="xnaohVUa"),
            nat=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            tunnel_interface=Global[bool](value=True),
        )
        cellular_tag = self.builder.add_vpn_subparcel(vpn_tag, cellular_parcel)
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
        tracker_group = TrackerGroup(
            parcel_name="TestTrackerGroup",
            parcel_description="Test Tracker Group Description",
            tracker_refs=[],
        )
        self.builder.add_tracker_group(
            associate_tags=set([cellular_tag]), group=tracker_group, trackers=[tracker1, tracker2]
        )
        self.builder.add_tracker(associate_tags=set([gre_tag]), tracker=tracker1)
        report = self.builder.build()

        assert len(report.failed_parcels) == 0

    def tearDown(self) -> None:
        target_profile = self.api.get_profiles().filter(profile_name=self.fp_name).single_or_default()
        if target_profile:
            # In case of a failed test, the profile might not have been created
            self.api.delete_profile(target_profile.profile_id)
