# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

DualTone = Literal[
    "Busy",
    "Disconnect",
    "Number Unobtainable",
    "Out of Service",
    "Reorder",
    "Ringback",
]


class SupervisoryCustomCPTone(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cadence: Union[Variable, Global[str]] = Field()
    dual_tone: Union[Variable, Global[DualTone]] = Field(validation_alias="dualTone", serialization_alias="dualTone")
    dualtone_frequency_in: Union[Variable, Global[int]] = Field(
        validation_alias="dualtoneFrequencyIn", serialization_alias="dualtoneFrequencyIn"
    )
    dualtone_frequency_out: Union[Variable, Global[int]] = Field(
        validation_alias="dualtoneFrequencyOut", serialization_alias="dualtoneFrequencyOut"
    )
    supervisory_name: Union[Variable, Global[str]] = Field(
        validation_alias="supervisoryName", serialization_alias="supervisoryName"
    )


class SupervisoryCustomDetectionParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cadence_variation: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="cadenceVariation", serialization_alias="cadenceVariation"
    )
    max_delay: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="maxDelay", serialization_alias="maxDelay"
    )
    max_deviation: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="maxDeviation", serialization_alias="maxDeviation"
    )
    max_power: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="maxPower", serialization_alias="maxPower"
    )
    min_power: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="minPower", serialization_alias="minPower"
    )
    min_power_twist: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="minPowerTwist", serialization_alias="minPowerTwist"
    )
    supervisory_number: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="supervisoryNumber", serialization_alias="supervisoryNumber"
    )


class SupervisoryDiconnectParcel(_ParcelBase):
    type_: Literal["supervisory-disconnect"] = Field(default="supervisory-disconnect", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    supervisory_custom_c_p_tone: Optional[List[SupervisoryCustomCPTone]] = Field(
        default=None,
        validation_alias=AliasPath("data", "supervisoryCustomCPTone"),
    )
    supervisory_custom_detection_params: Optional[List[SupervisoryCustomDetectionParams]] = Field(
        default=None,
        validation_alias=AliasPath("data", "supervisoryCustomDetectionParams"),
    )
