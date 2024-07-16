# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface

from catalystwan.api.templates.models.cisco_vpn_interface_model import (
    AccessList,
    CiscoVpnInterfaceModel,
    DhcpHelperV6,
    Encapsulation,
    Ip,
    Ipv4Secondary,
    Ipv6,
    Ipv6Vrrp,
    SecondaryIPv4Address,
    SecondaryIPv6Address,
    Static,
    StaticNat66,
    StaticPortForward,
    TrackingObject,
    Vrrp,
)

cisco_vpn_interface_complex = CiscoVpnInterfaceModel(
    template_name="cisco_vpn_interface_complex",
    template_description="cisco_vpn_interface_complex",
    if_name="GigabitEthernet0/0",
    interface_description="WAN interface",
    poe=True,
    ipv4_address="192.0.2.1/24",
    secondary_ipv4_address=[
        SecondaryIPv4Address(address=IPv4Interface("192.0.2.2/24")),
        SecondaryIPv4Address(address=IPv4Interface("192.0.2.3/24")),
    ],
    dhcp_ipv4_client=False,
    dhcp_distance=1,
    ipv6_address=IPv6Interface("2001:db8::1/64"),
    dhcp_ipv6_client=True,
    secondary_ipv6_address=[
        SecondaryIPv6Address(address=IPv6Interface("2001:db8::2/64")),
        SecondaryIPv6Address(address=IPv6Interface("2001:db8::3/64")),
    ],
    access_list_ipv4=[
        AccessList(direction="in", acl_name="ACL-INBOUND"),
        AccessList(direction="out", acl_name="ACL-OUTBOUND"),
    ],
    dhcp_helper=[IPv4Address("192.0.2.254")],
    dhcp_helper_v6=[DhcpHelperV6(address=IPv6Address("2001:db8::1"), vpn=0)],
    tracker=["Tracker1", "Tracker2"],
    auto_bandwidth_detect=True,
    iperf_server=IPv4Address("192.0.2.100"),
    nat=True,
    nat_choice="Interface",
    udp_timeout=30,
    tcp_timeout=60,
    nat_range_start=IPv4Address("192.0.2.100"),
    nat_range_end=IPv4Address("192.0.2.200"),
    overload=True,
    loopback_interface="Loopback0",
    prefix_length=24,
    enable=None,
    nat64=False,
    nat66=False,
    static_nat66=[
        StaticNat66(
            source_prefix=IPv6Interface("2001:db8:1234::/64"),
            translated_source_prefix="2001:db8:5678::/64",
            source_vpn_id=10,
        )
    ],
    static=[
        Static(
            source_ip=IPv4Address("192.0.2.1"),
            translate_ip=IPv4Address("203.0.113.1"),
            static_nat_direction="inside",
            source_vpn=10,
        )
    ],
    static_port_forward=[
        StaticPortForward(
            source_ip=IPv4Address("192.0.2.2"),
            translate_ip=IPv4Address("203.0.113.2"),
            static_nat_direction="outside",
            source_port=8080,
            translate_port=9090,
            proto="tcp",
            source_vpn=10,
        )
    ],
    enable_core_region=True,
    core_region="core",
    secondary_region="secondary-only",
    tloc_encapsulation=[Encapsulation(encap="ipsec", preference=100, weight=1)],
    border=True,
    per_tunnel_qos=True,
    per_tunnel_qos_aggregator=True,
    mode="hub",
    tunnels_bandwidth=1000,
    group=[1, 2],
    value="mpls",
    max_control_connections=5,
    control_connections=True,
    vbond_as_stun_server=True,
    exclude_controller_group_list=[3, 4],
    vmanage_connection_preference=100,
    port_hop=True,
    restrict=False,
    dst_ip=IPv4Address("198.51.100.14"),
    carrier="carrier1",
    nat_refresh_interval=30,
    hello_interval=10,
    hello_tolerance=30,
    bind="GigabitEthernet0/0",
    last_resort_circuit=False,
    low_bandwidth_link=False,
    tunnel_tcp_mss_adjust=1360,
    clear_dont_fragment=True,
    propagate_sgt=False,
    network_broadcast=True,
    all=False,
    bgp=True,
    dhcp=False,
    dns=True,
    icmp=True,
    sshd=True,
    netconf=False,
    ntp=True,
    ospf=False,
    stun=False,
    snmp=True,
    https=True,
    media_type="rj45",
    intrf_mtu=1500,
    mtu=1400,
    tcp_mss_adjust=1360,
    tloc_extension="100",
    load_interval=300,
    src_ip=IPv4Address("198.51.100.1"),
    xconnect="10",
    mac_address="00:0C:29:4B:55:3A",
    speed="1000",
    duplex="full",
    shutdown=False,
    arp_timeout=1200,
    autonegotiate=True,
    ip_directed_broadcast=False,
    icmp_redirect_disable=True,
    qos_adaptive=True,
    period=60,
    bandwidth_down=10000,
    dmin=5000,
    dmax=15000,
    bandwidth_up=5000,
    umin=2500,
    umax=7500,
    shaping_rate=5000,
    qos_map="default_qos_map",
    qos_map_vpn="vpn_qos_map",
    service_provider="ISP1",
    bandwidth_upstream=5000,
    bandwidth_downstream=10000,
    block_non_source_ip=True,
    rule_name="rewrite_rule_1",
    access_list_ipv6=[AccessList(direction="in", acl_name="ipv6_acl_1")],
    ip=[Ip(addr=IPv4Address("192.0.2.1"), mac="00:0C:29:4B:55:3A")],
    vrrp=[
        Vrrp(
            grp_id=1,
            priority=110,
            timer=100,
            track_omp=True,
            track_prefix_list="TRACKING_LIST",
            address=IPv4Address("192.0.2.254"),
            ipv4_secondary=[Ipv4Secondary(address=IPv4Address("192.0.2.253"))],
            tloc_change_pref=True,
            value=20,
            tracking_object=[TrackingObject(name=10, track_action="Decrement", decrement=20)],
        )
    ],
    ipv6_vrrp=[
        Ipv6Vrrp(
            grp_id=1,
            priority=110,
            timer=100,
            track_omp=True,
            track_prefix_list="TRACKING_LIST_IPV6",
            ipv6=[
                Ipv6(
                    ipv6_link_local=IPv6Address("fe80::1"),
                    prefix=IPv6Interface("2001:db8::/64"),
                )
            ],
        )
    ],
    enable_sgt_propagation=True,
    security_group_tag=0,
    trusted=True,
    enable_sgt_authorization_and_forwarding=True,
    enable_sgt_enforcement=True,
    enforcement_sgt=10001,
)
