# Copyright 2026 Cisco Systems, Inc. and its affiliates
import pytest

from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import Sequence


@pytest.mark.parametrize("export_first", [False, True])
def test_community_and_export_to_use_separate_actions(export_first):
    sequence = Sequence()
    vpns = ["gold_vpn1_tron", "gold_vpn14_oga"]

    if export_first:
        sequence.associate_export_to_action(vpns)
        sequence.associate_community_action("99:999")
    else:
        sequence.associate_community_action("99:999")
        sequence.associate_export_to_action(vpns)

    assert sequence.model_dump(by_alias=True, exclude_none=True)["actions"] == [
        {
            "set": [
                {
                    "community": {
                        "optionType": "global",
                        "value": "99:999",
                    }
                }
            ]
        },
        {
            "exportTo": {
                "optionType": "global",
                "value": vpns,
            }
        },
    ]


def test_export_to_action_updates_existing_entry():
    sequence = Sequence()

    sequence.associate_export_to_action(["vpn1"])
    sequence.associate_export_to_action(["vpn2"])

    assert sequence.actions is not None
    assert len(sequence.actions) == 1
    export_to = sequence.actions[0].export_to
    assert export_to is not None
    assert export_to.value == ["vpn2"]
