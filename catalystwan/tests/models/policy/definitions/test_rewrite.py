# Copyright 2026 Cisco Systems, Inc. and its affiliates
import json
from uuid import uuid4

import pytest
from pydantic import ValidationError

from catalystwan.models.policy.definition.rewrite import RewritePolicy


def test_parse_rewrite_rule():
    # Arrange
    payload = {
        "name": "test-l2cos-missing",
        "type": "rewriteRule",
        "description": "test-l2cos-missing",
        "definition": {
            "rules": [
                {"class": "67fb3d77-9b63-4c0b-85dd-49101a3d58a6", "plp": "high", "dscp": "5", "layer2Cos": ""},
                {"class": "67fb3d77-9b63-4c0b-85dd-49101a3d58a6", "plp": "low", "dscp": "", "layer2Cos": "3"},
            ]
        },
    }
    # Act
    rewrite = RewritePolicy.model_validate_json(json.dumps(payload))
    # Assert
    assert len(rewrite.definition.rules) == 2


def test_create_rewrite_rules():
    # Arrange / Act
    rewrite = RewritePolicy(name="test")
    rewrite.add_rule(class_map_ref=uuid4(), dscp=63, l2cos=1, plp="high")
    rewrite.add_rule(class_map_ref=uuid4(), dscp=0, l2cos=None, plp="low")
    rewrite.add_rule(class_map_ref=uuid4(), dscp=None, l2cos=2, plp="low")
    # Assert
    assert len(rewrite.definition.rules) == 3


def test_create_rewrite_rule_raises_when_no_dscp_nor_l2cos():
    # Arrange
    rewrite = RewritePolicy(name="test")
    # Act / Assert
    with pytest.raises(ValidationError):
        rewrite.add_rule(class_map_ref=uuid4(), dscp=None, l2cos=None, plp="high")
