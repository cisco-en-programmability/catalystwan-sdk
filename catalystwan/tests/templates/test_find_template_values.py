# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging

from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.utils.feature_template.find_template_values import find_template_values


def test_find_template_values():
    input_values = {
        "vpn-id": {"vipObjectType": "object", "vipType": "constant", "vipValue": 0},
        "name": {
            "vipObjectType": "object",
            "vipType": "ignore",
            "vipVariableName": "vpn_name",
        },
        "ecmp-hash-key": {
            "layer4": {
                "vipObjectType": "object",
                "vipType": "ignore",
                "vipValue": "false",
                "vipVariableName": "vpn_layer4",
            }
        },
        "nat64-global": {"prefix": {"stateful": {}}},
        "nat64": {
            "v4": {
                "pool": {
                    "vipType": "ignore",
                    "vipValue": [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey": ["name"],
                }
            }
        },
        "nat": {
            "natpool": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["name"],
            },
            "port-forward": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["source-port", "translate-port"],
            },
            "static": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["source-ip", "translate-ip"],
            },
        },
        "route-import": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["protocol"],
        },
        "route-export": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["protocol"],
        },
        "dns": {
            "vipType": "constant",
            "vipValue": [
                {
                    "role": {
                        "vipType": "constant",
                        "vipValue": "primary",
                        "vipObjectType": "object",
                    },
                    "dns-addr": {
                        "vipType": "variableName",
                        "vipValue": "",
                        "vipObjectType": "object",
                        "vipVariableName": "vpn_dns_primary",
                    },
                    "priority-order": ["dns-addr", "role"],
                },
                {
                    "role": {
                        "vipType": "constant",
                        "vipValue": "secondary",
                        "vipObjectType": "object",
                    },
                    "dns-addr": {
                        "vipType": "variableName",
                        "vipValue": "",
                        "vipObjectType": "object",
                        "vipVariableName": "vpn_dns_secondary",
                    },
                    "priority-order": ["dns-addr", "role"],
                },
            ],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["dns-addr"],
        },
        "host": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["hostname"],
        },
        "service": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["svc-type"],
        },
        "ip": {
            "route": {
                "vipType": "constant",
                "vipValue": [
                    {
                        "prefix": {
                            "vipObjectType": "object",
                            "vipType": "constant",
                            "vipValue": "0.0.0.0/0",
                            "vipVariableName": "vpn_ipv4_ip_prefix",
                        },
                        "next-hop": {
                            "vipType": "constant",
                            "vipValue": [
                                {
                                    "address": {
                                        "vipObjectType": "object",
                                        "vipType": "variableName",
                                        "vipValue": "",
                                        "vipVariableName": "vpn_next_hop_ip_address_0",
                                    },
                                    "distance": {
                                        "vipObjectType": "object",
                                        "vipType": "ignore",
                                        "vipValue": 1,
                                        "vipVariableName": "vpn_next_hop_ip_distance_0",
                                    },
                                    "priority-order": ["address", "distance"],
                                }
                            ],
                            "vipObjectType": "tree",
                            "vipPrimaryKey": ["address"],
                        },
                        "priority-order": ["prefix", "next-hop", "next-hop-with-track"],
                    }
                ],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["prefix"],
            },
            "gre-route": {},
            "ipsec-route": {},
            "service-route": {},
        },
        "ipv6": {},
        "omp": {
            "advertise": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["protocol"],
            },
            "ipv6-advertise": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["protocol"],
            },
        },
    }
    expected_values = {
        "vpn-id": 0,
        "dns": [
            {"role": "primary", "dns-addr": DeviceVariable(name="vpn_dns_primary")},
            {"role": "secondary", "dns-addr": DeviceVariable(name="vpn_dns_secondary")},
        ],
        "ip": {
            "route": [
                {
                    "prefix": "0.0.0.0/0",
                    "next-hop": [
                        {
                            "address": DeviceVariable(name="vpn_next_hop_ip_address_0"),
                        }
                    ],
                }
            ],
        },
    }
    # Act
    result = find_template_values(input_values)
    # Assert
    assert expected_values == result


def test_log_error_when_overwriting_existing_variable_value(caplog):
    input_values = {
        "if-name": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_name",
        },
        "description": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_desc",
        },
        "ip": {
            "value": {
                "vipObjectType": "object",
                "vipType": "variableName",
                "vipValue": "",
                "vipVariableName": "first_test_value_variable",
            },
            "address": {
                "vipObjectType": "object",
                "vipType": "variableName",
                "vipValue": "",
                "vipVariableName": "inet-if_ipv4_address",
            },
        },
        "tunnel-interface": {
            "color": {
                "value": {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "second_test_value_variable",
                },
                "restrict": {
                    "vipObjectType": "node-only",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_tunnel_color_restrict",
                },
            },
        },
    }

    expected_error_log = (
        "Overwriting existing value for field: 'value' in templated_values. "
        "Previous value: name='first_test_value_variable', new value: name='second_test_value_variable'."
    )
    # Act
    result = find_template_values(input_values)

    # Assert
    error_logs = [log.getMessage() for log in caplog.records if log.levelno == logging.ERROR]
    assert expected_error_log in error_logs
    assert isinstance(result.get("value"), DeviceVariable)
    assert result.get("value").name == "second_test_value_variable"


def test_log_error_when_overwriting_existing_top_level_global_value(caplog):
    input_values = {
        "if-name": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_name",
        },
        "description": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_desc",
        },
        "value": {
            "vipObjectType": "object",
            "vipType": "constant",
            "vipValue": "test_value",
            "vipVariableName": "first_test_value_variable",
        },
        "ip": {
            "address": {
                "vipObjectType": "object",
                "vipType": "variableName",
                "vipValue": "",
                "vipVariableName": "inet-if_ipv4_address",
            },
        },
        "tunnel-interface": {
            "color": {
                "value": {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "second_test_value_variable",
                },
                "restrict": {
                    "vipObjectType": "node-only",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_tunnel_color_restrict",
                },
            },
        },
    }

    expected_error_log = (
        "Overwriting existing value for field: 'value' in templated_values. "
        "Previous value: test_value, new value: name='second_test_value_variable'."
    )
    # Act
    result = find_template_values(input_values)

    # Assert
    error_logs = [log.getMessage() for log in caplog.records if log.levelno == logging.ERROR]

    assert expected_error_log in error_logs
    assert isinstance(result.get("value"), DeviceVariable)
    assert result.get("value").name == "second_test_value_variable"


def test_no_log_error_when_setting_value_first_time(caplog):
    input_values = {
        "if-name": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_name",
        },
        "description": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_desc",
        },
        "ip": {
            "address": {
                "vipObjectType": "object",
                "vipType": "variableName",
                "vipValue": "",
                "vipVariableName": "inet-if_ipv4_address",
            },
        },
        "tunnel-interface": {
            "color": {
                "value": {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "test_value_variable",
                },
                "restrict": {
                    "vipObjectType": "node-only",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_tunnel_color_restrict",
                },
            },
        },
    }

    # Act
    result = find_template_values(input_values)

    # Assert
    error_logs = [log.getMessage() for log in caplog.records if log.levelno == logging.ERROR]
    assert len(error_logs) == 0
    assert isinstance(result.get("value"), DeviceVariable)
    assert result.get("value").name == "test_value_variable"


def test_no_log_error_when_global_value_is_nested(caplog):
    input_values = {
        "if-name": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_name",
        },
        "description": {
            "vipObjectType": "object",
            "vipType": "variableName",
            "vipValue": "",
            "vipVariableName": "inet-if_desc",
        },
        "ip": {
            "address": {
                "vipObjectType": "object",
                "vipType": "variableName",
                "vipValue": "",
                "vipVariableName": "inet-if_ipv4_address",
            },
            "value": {
                "vipObjectType": "object",
                "vipType": "constant",
                "vipValue": "test_value",
                "vipVariableName": "first_test_value_variable",
            },
        },
        "tunnel-interface": {
            "color": {
                "value": {
                    "vipObjectType": "object",
                    "vipType": "variableName",
                    "vipValue": "",
                    "vipVariableName": "second_test_value_variable",
                },
                "restrict": {
                    "vipObjectType": "node-only",
                    "vipType": "ignore",
                    "vipValue": "false",
                    "vipVariableName": "vpn_if_tunnel_color_restrict",
                },
            },
        },
    }

    # Act
    result = find_template_values(input_values)

    # Assert
    error_logs = [log.getMessage() for log in caplog.records if log.levelno == logging.ERROR]
    assert len(error_logs) == 0
    assert isinstance(result.get("value"), DeviceVariable)
    assert result.get("value").name == "second_test_value_variable"
