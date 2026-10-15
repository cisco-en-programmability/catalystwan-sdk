# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest

from catalystwan.endpoints.configuration_group import ConfigGroup


class TestConfigGroupModel(unittest.TestCase):
    def test_config_group_with_id(self):
        data = {
            "id": "11111111-2222-3333-4444-555555555555",
            "name": "Branch_Config_Group",
            "description": "Branch configuration group",
            "solution": "sdwan",
        }
        cg = ConfigGroup.model_validate(data)
        self.assertEqual(cg.id, "11111111-2222-3333-4444-555555555555")
        self.assertEqual(cg.name, "Branch_Config_Group")
        self.assertEqual(cg.description, "Branch configuration group")
        self.assertEqual(cg.solution, "sdwan")
        self.assertIsNone(cg.profiles)

    def test_config_group_without_id(self):
        data = {
            "name": "New_Config_Group",
            "solution": "sdwan",
        }
        cg = ConfigGroup.model_validate(data)
        self.assertIsNone(cg.id)
        self.assertEqual(cg.name, "New_Config_Group")
        self.assertIsNone(cg.description)

    def test_config_group_serialization(self):
        cg = ConfigGroup(id="abc-123", name="Serialized_Group", solution="sdwan")
        dumped = cg.model_dump()
        self.assertEqual(dumped["id"], "abc-123")
        self.assertEqual(dumped["name"], "Serialized_Group")
