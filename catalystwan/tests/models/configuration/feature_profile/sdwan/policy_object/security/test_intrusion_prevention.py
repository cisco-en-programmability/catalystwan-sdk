# Copyright 2026 Cisco Systems, Inc. and its affiliates
import json

from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.intrusion_prevention import (
    IntrusionPreventionParcel,
)


def test_parse_intrusion_prevention_with_signature_set_as_refid():
    # Arrange
    payload = {
        "name": "IntrusionPrevention-26.1",
        "description": "test message format",
        "data": {
            "signatureSet": {"refId": {"optionType": "global", "value": "d479c685-078f-4961-9daf-f29d09ba84a5"}},
            "inspectionMode": {"optionType": "global", "value": "detection"},
            "logLevel": {"optionType": "global", "value": "emergency"},
            "customSignature": {"optionType": "global", "value": False},
        },
    }
    parcel = IntrusionPreventionParcel.model_validate_json(json.dumps(payload))
    # Assert
    assert isinstance(parcel.signature_set, RefIdItem)
    assert parcel.signature_set.ref_id.value == "d479c685-078f-4961-9daf-f29d09ba84a5"
