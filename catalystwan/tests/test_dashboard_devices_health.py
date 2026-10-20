# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock

from catalystwan.api.dashboard_api import DashboardAPI
from catalystwan.utils.dashboard import DeviceHealth, DevicesHealth


def _make_device_raw(index: int) -> dict:
    return {
        "name": f"vedge-{index}",
        "personality": "vedge",
        "uuid": f"uuid-{index}",
        "reachability": "reachable",
        "longitude": 0.0,
        "latitude": 0.0,
        "health": "green",
        "qoe": 10,
        "location": "Site 1",
        "site_id": "100",
        "system_ip": f"10.0.0.{index}",
        "device_type": "vedge",
        "local_system_ip": f"10.0.0.{index}",
        "device_model": "vedge-cloud",
        "software_version": "20.9.1",
        "cpu_load": 15.0,
        "memory_utilization": 30.0,
        "control_connections": 2,
        "control_connections_up": 2,
        "vsmart_control_connections": 2,
        "expected_vsmart_connections": 2,
        "has_geo_data": True,
        "uptime_date": 1600000000,
        "device_groups": [],
        "connected_vmanages": ["10.0.0.1"],
        "bfd_sessions_up": 4,
        "bfd_sessions": 4,
        "omp_peers": 2,
        "omp_peers_up": 2,
        "board_serial_number": 1234567,
        "chassis_number": f"chassis-{index}",
        "vpn_ids": [0, 512],
    }


class TestDashboardDevicesHealth(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.dashboard_api = DashboardAPI(self.mock_session)

    def test_get_devices_health_single_page(self):
        devices = [_make_device_raw(i) for i in range(10)]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"total_devices": 10, "devices": devices}
        self.mock_session.get.return_value = mock_resp

        res = self.dashboard_api.get_devices_health()

        self.mock_session.get.assert_called_once_with("/dataservice/health/devices", params=None)
        self.assertIsInstance(res, DevicesHealth)
        self.assertEqual(res.total_devices, 10)
        self.assertEqual(len(res.devices), 10)
        self.assertIsInstance(res.devices[0], DeviceHealth)
        self.assertEqual(res.devices[0].name, "vedge-0")

    def test_get_devices_health_auto_pagination_issue_41(self):
        """Reproduces and verifies fix for #41: total_devices=82, page 1 has 50, page 2 has 32."""
        page1_devices = [_make_device_raw(i) for i in range(50)]
        page2_devices = [_make_device_raw(i) for i in range(50, 82)]

        resp_page1 = MagicMock()
        resp_page1.json.return_value = {"total_devices": 82, "devices": page1_devices}

        resp_page2 = MagicMock()
        resp_page2.json.return_value = {"total_devices": 82, "devices": page2_devices}

        self.mock_session.get.side_effect = [resp_page1, resp_page2]

        res = self.dashboard_api.get_devices_health()

        self.assertEqual(self.mock_session.get.call_count, 2)
        # First call has no offset
        first_call_args, first_call_kwargs = self.mock_session.get.call_args_list[0]
        self.assertEqual(first_call_args[0], "/dataservice/health/devices")
        self.assertIsNone(first_call_kwargs["params"])

        # Second call paginates with offset=50, limit=50
        second_call_args, second_call_kwargs = self.mock_session.get.call_args_list[1]
        self.assertEqual(second_call_args[0], "/dataservice/health/devices")
        self.assertEqual(second_call_kwargs["params"], {"offset": 50, "limit": 50})

        self.assertEqual(res.total_devices, 82)
        self.assertEqual(len(res.devices), 82)
        self.assertEqual(res.devices[0].name, "vedge-0")
        self.assertEqual(res.devices[81].name, "vedge-81")

    def test_get_devices_health_explicit_limit_and_offset(self):
        devices = [_make_device_raw(i) for i in range(20)]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"total_devices": 100, "devices": devices}
        self.mock_session.get.return_value = mock_resp

        res = self.dashboard_api.get_devices_health(limit=20, offset=10)

        self.mock_session.get.assert_called_once_with("/dataservice/health/devices", params={"limit": 20, "offset": 10})
        self.assertEqual(res.total_devices, 100)
        self.assertEqual(len(res.devices), 20)

    def test_get_devices_health_site_id_filter(self):
        devices = [_make_device_raw(i) for i in range(5)]
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"total_devices": 5, "devices": devices}
        self.mock_session.get.return_value = mock_resp

        res = self.dashboard_api.get_devices_health(site_id="200")

        self.mock_session.get.assert_called_once_with("/dataservice/health/devices", params={"site-id": "200"})
        self.assertEqual(len(res.devices), 5)

    def test_get_devices_health_loop_protection_on_duplicate_data(self):
        """Ensures loop breaks if server ignores offset and repeats page 1 data."""
        page1_devices = [_make_device_raw(i) for i in range(50)]

        resp_page1 = MagicMock()
        resp_page1.json.return_value = {"total_devices": 100, "devices": page1_devices}

        # Server returns the same devices again on offset=50
        resp_page2 = MagicMock()
        resp_page2.json.return_value = {"total_devices": 100, "devices": page1_devices}

        self.mock_session.get.side_effect = [resp_page1, resp_page2]

        res = self.dashboard_api.get_devices_health()

        # Should terminate cleanly after seeing duplicate data instead of infinite looping
        self.assertEqual(self.mock_session.get.call_count, 2)
        self.assertEqual(len(res.devices), 50)

    def test_get_devices_health_auto_pagination_with_site_id(self):
        """Ensures site_id parameter is passed during subsequent pagination calls."""
        page1_devices = [_make_device_raw(i) for i in range(50)]
        page2_devices = [_make_device_raw(i) for i in range(50, 75)]

        resp_page1 = MagicMock()
        resp_page1.json.return_value = {"total_devices": 75, "devices": page1_devices}

        resp_page2 = MagicMock()
        resp_page2.json.return_value = {"total_devices": 75, "devices": page2_devices}

        self.mock_session.get.side_effect = [resp_page1, resp_page2]

        res = self.dashboard_api.get_devices_health(site_id="300")

        self.assertEqual(self.mock_session.get.call_count, 2)
        first_call_args, first_call_kwargs = self.mock_session.get.call_args_list[0]
        self.assertEqual(first_call_kwargs["params"], {"site-id": "300"})

        second_call_args, second_call_kwargs = self.mock_session.get.call_args_list[1]
        self.assertEqual(second_call_kwargs["params"], {"offset": 50, "limit": 50, "site-id": "300"})

        self.assertEqual(res.total_devices, 75)
        self.assertEqual(len(res.devices), 75)

    def test_get_devices_health_auto_paginate_disabled(self):
        """Ensures pagination does not happen if auto_paginate is False."""
        page1_devices = [_make_device_raw(i) for i in range(50)]
        resp_page1 = MagicMock()
        resp_page1.json.return_value = {"total_devices": 100, "devices": page1_devices}
        self.mock_session.get.return_value = resp_page1

        res = self.dashboard_api.get_devices_health(auto_paginate=False)

        self.mock_session.get.assert_called_once_with("/dataservice/health/devices", params=None)
        self.assertEqual(len(res.devices), 50)
        self.assertEqual(res.total_devices, 100)

    def test_get_devices_health_empty_response(self):
        """Ensures empty response is handled gracefully."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"total_devices": 0, "devices": []}
        self.mock_session.get.return_value = mock_resp

        res = self.dashboard_api.get_devices_health()

        self.mock_session.get.assert_called_once_with("/dataservice/health/devices", params=None)
        self.assertEqual(res.total_devices, 0)
        self.assertEqual(len(res.devices), 0)

    def test_get_devices_health_deduplicates_partial_overlapping_pages(self):
        """Ensures that overlapping devices across pages are deduplicated."""
        page1_devices = [_make_device_raw(0), _make_device_raw(1)]
        # Page 2 has device 1 (duplicate) and device 2 (new)
        page2_devices = [_make_device_raw(1), _make_device_raw(2)]

        resp_page1 = MagicMock()
        resp_page1.json.return_value = {"total_devices": 3, "devices": page1_devices}

        resp_page2 = MagicMock()
        resp_page2.json.return_value = {"total_devices": 3, "devices": page2_devices}

        self.mock_session.get.side_effect = [resp_page1, resp_page2]

        res = self.dashboard_api.get_devices_health()

        self.assertEqual(self.mock_session.get.call_count, 2)
        self.assertEqual(len(res.devices), 3)
        device_uuids = [d.uuid for d in res.devices]
        self.assertEqual(device_uuids, ["uuid-0", "uuid-1", "uuid-2"])
