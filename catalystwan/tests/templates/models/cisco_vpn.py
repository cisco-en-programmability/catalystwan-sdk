# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore

from catalystwan.api.templates.models.cisco_vpn_model import (
    Advertise,
    CiscoVPNModel,
    Dns,
    DnsIpv6,
    GreRoute,
    Host,
    IpsecRoute,
    Ipv6Advertise,
    Natpool,
    NextHop,
    NextHopv6,
    Pool,
    PortForward,
    PrefixList,
    RouteExport,
    RouteExportRedistribute,
    RouteImport,
    RouteImportFrom,
    RouteImportFromRedistribute,
    RouteImportRedistribute,
    Routev4,
    Routev6,
    Service,
    ServiceRoute,
    Static,
    SubnetStatic,
)

cisco_vpn_basic = CiscoVPNModel(
    template_name="cisco_vpn_basic", template_description="Primitive", device_models=["vedge-C8000V"]
)  # type: ignore


cisco_vpn_complex = CiscoVPNModel(
    template_name="cisco_vpn_complex",
    template_description="cisco_vpn_complex",
    device_models=["vedge-cloud"],
    vpn_name="test_vpn_name",
    omp_admin_distance_ipv4=10,
    omp_admin_distance_ipv6=100,
    route_v4=[Routev4(prefix="prefixv4", next_hop=[NextHop(address="1.1.1.1")])],
    route_v6=[Routev6(prefix="prefixv6", next_hop=[NextHopv6(address="2.2.2.2")], nat="NAT64")],
    dns=[Dns(dns_addr="1.1.1.1"), Dns(dns_addr="2.2.2.2", role="secondary")],
    dns_ipv6=[DnsIpv6(dns_addr="30a8:b25e:3db5:fe9f:231f:7478:4181:9234")],
    host=[Host(hostname="test_hostname", ip=["1.1.1.1"])],
    service=[
        Service(
            svc_type="appqoe",
            address=["1.1.1.1"],
            interface="Gig0/0/1",
            track_enable=False,
        ),
        Service(
            svc_type="FW",
            address=["1.1.122.1", "2.2.2.2"],
            interface="Gig0/0/2",
            track_enable=True,
        ),
        Service(
            svc_type="IDP",
            address=["1.1.122.2", "3.2.2.2"],
            interface="Gig0/0/3",
            track_enable=False,
        ),
    ],
    service_route=[
        ServiceRoute(prefix="service_route", vpn=1),
        ServiceRoute(prefix="service_route100", vpn=100),
    ],
    gre_route=[
        GreRoute(prefix="gre_route", vpn=100),
        GreRoute(prefix="gre_route2", vpn=2, interface=["Gig0/0/1", "ge0/0"]),
    ],
    ipsec_route=[
        IpsecRoute(prefix="ipsec-prefix", vpn=10, interface=["ge0/0", "Gig0/0/1"]),
        IpsecRoute(prefix="prefix-2", vpn=100),
    ],
    advertise=[
        Advertise(
            protocol="aggregate",
            route_policy="route-policy",
            protocol_sub_type=["external"],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entry",
                    aggregate_only=True,
                    region="access",
                )
            ],
        )
    ],
    ipv6_advertise=[
        Ipv6Advertise(
            protocol="aggregate",
            route_policy="route-policyv6",
            protocol_sub_type=["external"],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entryv6",
                    aggregate_only=False,
                    region="core",
                )
            ],
        ),
        Ipv6Advertise(
            protocol="connected",
            route_policy="route-policyv6-connected",
            protocol_sub_type=["external"],
            prefix_list=[
                PrefixList(
                    prefix_entry="prefix_entryv6-connected",
                    aggregate_only=True,
                    region="access",
                )
            ],
        ),
    ],
    pool=[
        Pool(
            name="pool",
            start_address="1.1.1.1",
            end_address="10.10.10.10",
            overload=False,
            leak_from_global=True,
            leak_from_global_protocol="connected",
            leak_to_global=False,
        )
    ],
    natpool=[
        Natpool(
            name=1,
            prefix_length=24,
            range_start="10",
            range_end="100",
            overload="false",
            direction="inside",
            tracker_id=10,
        ),
        Natpool(name=2, prefix_length=24, range_start="10", range_end="100", overload="true", direction="outside"),
    ],
    static=[
        Static(
            pool_name=1,
            source_ip="1.1.1.1",
            translate_ip="1.1.1.2",
            static_nat_direction="inside",
            tracker_id=1,
        ),
        Static(
            pool_name=2,
            source_ip="2.1.1.1",
            translate_ip="2.1.1.2",
            static_nat_direction="inside",
        ),
    ],
    subnet_static=[
        SubnetStatic(
            source_ip_subnet="1.1.1.1",
            translate_ip_subnet="2.2.2.2",
            prefix_length=24,
            static_nat_direction="outside",
        ),
        SubnetStatic(
            source_ip_subnet="1.1.2.1",
            translate_ip_subnet="2.3.2.2",
            prefix_length=24,
            static_nat_direction="inside",
            tracker_id=10,
        ),
    ],
    port_forward=[
        PortForward(
            pool_name=1,
            source_port=1000,
            translate_port=2000,
            source_ip="1.1.1.1",
            translate_ip="2.2.2.2",
            proto="tcp",
        ),
        PortForward(
            pool_name=2,
            source_port=1000,
            translate_port=2000,
            source_ip="1.1.4.1",
            translate_ip="2.2.3.2",
            proto="udp",
        ),
    ],
    route_import=[
        RouteImport(
            protocol="bgp",
            protocol_sub_type=["external"],
            route_policy="test_route_policy",
            redistribute=[
                RouteImportRedistribute(
                    protocol="eigrp",
                    route_policy="test_route_policy",
                )
            ],
        )
    ],
    route_import_from=[
        RouteImportFrom(
            source_vpn=1,
            protocol="connected",
            protocol_sub_type=["external"],
            route_policy="test_route_policy",
            redistribute=[RouteImportFromRedistribute(protocol="bgp")],
        ),
        RouteImportFrom(
            source_vpn=100,
            protocol="bgp",
            protocol_sub_type=["external"],
            route_policy="test_route_policy",
            redistribute=[
                RouteImportFromRedistribute(
                    protocol="eigrp",
                    route_policy="test_route_policy",
                )
            ],
        ),
    ],
    route_export=[
        RouteExport(
            protocol="static",
            protocol_sub_type=["external"],
            redistribute=[
                RouteExportRedistribute(
                    protocol="ospf",
                    route_policy="test_route_policy",
                )
            ],
        )
    ],
)
