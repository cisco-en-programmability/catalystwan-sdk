# Copyright 2024 Cisco Systems, Inc. and its affiliates

import json
import unittest
from datetime import datetime, timezone
from uuid import UUID

from pydantic import ValidationError

from catalystwan.endpoints.configuration_group import (
    ConfigGroup,
    ConfigGroupCreationPayload,
    ConfigGroupCreationResponse,
    FeatureProfile,
    ProfileId,
    VariableData,
)


class TestConfigGroupModel(unittest.TestCase):
    def setUp(self):
        self.valid_uuid_str = "11111111-2222-3333-4444-555555555555"
        self.valid_uuid = UUID(self.valid_uuid_str)
        self.now = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self.base_config_group_data = {
            "id": self.valid_uuid_str,
            "name": "Branch_Config_Group",
            "description": "Branch configuration group",
            "solution": "sdwan",
            "profiles": None,
            "source": "vManage",
            "state": "deployed",
            "devices": [{"deviceId": "C8K-1"}],
            "createdBy": "admin",
            "lastUpdatedBy": "admin",
            "createdOn": "2024-01-01T12:00:00Z",
            "lastUpdatedOn": "2024-01-01T12:00:00Z",
            "version": 1,
            "numberOfDevices": 1,
            "numberOfDevicesUpToDate": 1,
            "origin": "user",
            "topology": None,
            "fullConfigCli": False,
        }

    def test_config_group_model_with_required_fields(self):
        cg = ConfigGroup.model_validate(self.base_config_group_data)
        self.assertIsInstance(cg.id, UUID)
        self.assertEqual(cg.id, self.valid_uuid)
        self.assertEqual(cg.name, "Branch_Config_Group")
        self.assertEqual(cg.description, "Branch configuration group")
        self.assertEqual(cg.solution, "sdwan")
        self.assertIsNone(cg.profiles)
        self.assertEqual(cg.source, "vManage")
        self.assertEqual(cg.state, "deployed")
        self.assertEqual(cg.devices, [{"deviceId": "C8K-1"}])
        self.assertEqual(cg.created_by, "admin")
        self.assertEqual(cg.last_updated_by, "admin")
        self.assertEqual(cg.version, 1)
        self.assertEqual(cg.number_of_devices, 1)
        self.assertEqual(cg.number_of_devices_up_to_date, 1)
        self.assertEqual(cg.origin, "user")
        self.assertIsNone(cg.topology)
        self.assertFalse(cg.full_config_cli)

    def test_config_group_id_is_required(self):
        data = dict(self.base_config_group_data)
        del data["id"]
        with self.assertRaises(ValidationError) as ctx:
            ConfigGroup.model_validate(data)
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("id",) and e["type"] == "missing" for e in errors))

    def test_config_group_invalid_uuid_rejected(self):
        data = dict(self.base_config_group_data)
        data["id"] = "not-a-valid-uuid"
        with self.assertRaises(ValidationError) as ctx:
            ConfigGroup.model_validate(data)
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("id",) and e["type"] == "uuid_parsing" for e in errors))

    def test_config_group_serialization(self):
        cg = ConfigGroup.model_validate(self.base_config_group_data)
        dumped_dict = cg.model_dump(by_alias=True)
        self.assertEqual(dumped_dict["id"], self.valid_uuid)
        self.assertEqual(dumped_dict["createdBy"], "admin")
        self.assertEqual(dumped_dict["numberOfDevices"], 1)

        dumped_json = json.loads(cg.model_dump_json(by_alias=True))
        self.assertEqual(dumped_json["id"], self.valid_uuid_str)
        self.assertEqual(dumped_json["createdBy"], "admin")
        self.assertEqual(dumped_json["lastUpdatedBy"], "admin")
        self.assertEqual(dumped_json["numberOfDevices"], 1)
        self.assertEqual(dumped_json["numberOfDevicesUpToDate"], 1)

    def test_config_group_with_feature_profiles(self):
        data = dict(self.base_config_group_data)
        data["profiles"] = [
            {
                "id": "fp-1234",
                "name": "System_Profile",
                "description": "System feature profile",
                "solution": "sdwan",
                "type": "system",
                "createdBy": "admin",
                "lastUpdatedBy": "admin",
                "createdOn": "2024-01-01T12:00:00Z",
                "lastUpdatedOn": "2024-01-01T12:00:00Z",
            }
        ]
        cg = ConfigGroup.model_validate(data)
        self.assertIsNotNone(cg.profiles)
        self.assertEqual(len(cg.profiles), 1)
        fp = cg.profiles[0]
        self.assertIsInstance(fp, FeatureProfile)
        self.assertEqual(fp.id, "fp-1234")
        self.assertEqual(fp.name, "System_Profile")
        self.assertEqual(fp.type, "system")
        self.assertEqual(fp.created_by, "admin")

    def test_config_group_creation_payload_does_not_require_id(self):
        profile_uuid = UUID("22222222-3333-4444-5555-666666666666")
        payload = ConfigGroupCreationPayload(
            name="New_Group",
            description="Creation payload without id",
            solution="sdwan",
            profiles=[ProfileId(id=profile_uuid)],
        )
        self.assertEqual(payload.name, "New_Group")
        self.assertEqual(payload.description, "Creation payload without id")
        self.assertEqual(payload.solution, "sdwan")
        self.assertFalse(hasattr(payload, "id"))
        self.assertEqual(len(payload.profiles), 1)
        self.assertEqual(payload.profiles[0].id, profile_uuid)

        dumped = payload.model_dump()
        self.assertNotIn("id", dumped)
        self.assertEqual(dumped["name"], "New_Group")

    def test_config_group_creation_response_uuid(self):
        resp = ConfigGroupCreationResponse.model_validate({"id": self.valid_uuid_str})
        self.assertIsInstance(resp.id, UUID)
        self.assertEqual(resp.id, self.valid_uuid)

    def test_profile_id_uuid(self):
        p = ProfileId.model_validate({"id": self.valid_uuid_str})
        self.assertIsInstance(p.id, UUID)
        self.assertEqual(p.id, self.valid_uuid)

    def test_variable_data_types(self):
        v_str = VariableData(name="var_str", value="test_value")
        self.assertEqual(v_str.value, "test_value")

        v_int = VariableData(name="var_int", value=42)
        self.assertEqual(v_int.value, 42)

        v_bool = VariableData(name="var_bool", value=True)
        self.assertIs(v_bool.value, True)

        v_list = VariableData(name="var_list", value=["a", 1, False])
        self.assertEqual(v_list.value, ["a", 1, False])

        v_none = VariableData(name="var_none")
        self.assertIsNone(v_none.value)
