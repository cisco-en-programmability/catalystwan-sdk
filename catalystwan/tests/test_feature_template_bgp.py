# Copyright 2024 Cisco Systems, Inc. and its affiliates

import unittest

from catalystwan.api.templates.models.cisco_bgp_model import CiscoBGPModel
from catalystwan.api.templates.models.supported import available_models
from catalystwan.utils.feature_template.choose_model import choose_model


class TestCiscoBGPModelSupport(unittest.TestCase):
    def test_bgp_model_in_available_models(self):
        self.assertIn("cisco_bgp", available_models)
        self.assertIs(available_models["cisco_bgp"], CiscoBGPModel)

    def test_choose_model_bgp(self):
        model = choose_model("cisco_bgp")
        self.assertIs(model, CiscoBGPModel)

    def test_bgp_model_type_attribute(self):
        self.assertEqual(CiscoBGPModel.type, "cisco_bgp")
