# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase


class AddressList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    address: Union[Variable, Global[str]] = Field()
    port: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)
    preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)


HuntScheme = Literal[
    "none",
    "round-robin",
]


class HuntStopRule(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    response_code_end: Union[Variable, Global[int]] = Field(
        validation_alias="responseCodeEnd", serialization_alias="responseCodeEnd"
    )
    response_code_start: Union[Variable, Global[int]] = Field(
        validation_alias="responseCodeStart", serialization_alias="responseCodeStart"
    )
    rule_id: Union[Variable, Global[int]] = Field(validation_alias="ruleId", serialization_alias="ruleId")


class ServerGroupParcel(_ParcelBase):
    type_: Literal["server-group"] = Field(default="server-group", exclude=True)
    model_config = ConfigDict(populate_by_name=True)
    server_group_id: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "serverGroupId"))
    address_list: Optional[List[AddressList]] = Field(
        default=None,
        validation_alias=AliasPath("data", "addressList"),
    )
    hunt_scheme: Optional[Union[Variable, Global[HuntScheme], Default[Literal["none"]]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "huntScheme"),
    )
    hunt_stop_rule: Optional[List[HuntStopRule]] = Field(
        default=None,
        validation_alias=AliasPath("data", "huntStopRule"),
    )
    shutdown: Optional[Union[Variable, Default[bool], Global[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "shutdown")
    )
