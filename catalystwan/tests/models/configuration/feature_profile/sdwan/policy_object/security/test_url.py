# Copyright 2026 Cisco Systems, Inc. and its affiliates
import json

from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url import URLParcel


def test_url_parcel_round_trip():
    # Arrange
    json_data = """
    {
        "name": "Forbidden",
        "description": "Uses new format with type field inside data structure > 20.15.2",
        "data": {
            "type": "urlblocked",
            "entries": [
                {
                    "pattern": {
                        "optionType": "global",
                        "value": "bbc.com"
                    }
                }
            ]
        }
    }
    """
    # Act
    validated_parcel = URLParcel.model_validate_json(json_data)
    serialized_data = validated_parcel.model_dump_json(by_alias=True, exclude_none=True)
    serialized_data_dict = json.loads(serialized_data)
    round_trip_parcel = URLParcel.model_validate_json(serialized_data)

    # Assert
    assert validated_parcel.subtype == "urlblocked"
    assert validated_parcel.legacy_subtype is None
    assert serialized_data_dict.get("data", {}).get("type") == "urlblocked"
    assert serialized_data_dict.get("type") is None
    assert round_trip_parcel.subtype == "urlblocked"
    assert round_trip_parcel.legacy_subtype is None
    assert validated_parcel == round_trip_parcel


def test_url_parcel_round_trip_legacy_type_field():
    json_data = """
    {
        "name": "Forbidden",
        "description": "Uses legacy format with type field on top level <= 20.15.2",
        "type": "urlblocked",
        "data": {
            "entries": [
                {
                    "pattern": {
                        "optionType": "global",
                        "value": "bbc.com"
                    }
                }
            ]
        }
    }
    """
    # Act
    validated_parcel = URLParcel.model_validate_json(json_data)
    serialized_data = validated_parcel.model_dump_json(by_alias=True, exclude_none=True)
    serialized_data_dict = json.loads(serialized_data)
    round_trip_parcel = URLParcel.model_validate_json(serialized_data)

    # Assert
    assert validated_parcel.subtype is None
    assert validated_parcel.legacy_subtype == "urlblocked"
    assert serialized_data_dict.get("data", {}).get("type") is None
    assert serialized_data_dict.get("type") == "urlblocked"
    assert round_trip_parcel.subtype is None
    assert round_trip_parcel.legacy_subtype == "urlblocked"
    assert validated_parcel == round_trip_parcel
