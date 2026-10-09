# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator

from catalystwan.models.common import IntStr, check_any_of_fields
from catalystwan.models.policy.policy_definition import (
    DefinitionWithSequencesCommonBase,
    PLPEntryType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class RewritePolicyHeader(PolicyDefinitionBase):
    type: Literal["rewriteRule"] = "rewriteRule"


class RewritePolicyRule(BaseModel):
    class_: UUID = Field(serialization_alias="class", validation_alias="class")
    plp: str
    dscp: Optional[IntStr] = Field(default=None, ge=0, le=63)
    l2cos: Optional[IntStr] = Field(
        default=None, ge=0, le=7, serialization_alias="layer2Cos", validation_alias="layer2Cos"
    )
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("dscp", "l2cos", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        return None if value == "" else value

    @field_serializer("dscp", "l2cos")
    def none_to_empty_string(self, value):
        return "" if value is None else value

    @model_validator(mode="after")
    def check_dscp_or_l2cos(self):
        check_any_of_fields(self.__dict__, {"dscp", "l2cos"})
        return self


class RewritePolicyDefinition(BaseModel):
    rules: List[RewritePolicyRule] = []


class RewritePolicy(RewritePolicyHeader, DefinitionWithSequencesCommonBase):
    definition: RewritePolicyDefinition = RewritePolicyDefinition()

    def add_rule(self, class_map_ref: UUID, dscp: Optional[int], l2cos: Optional[int], plp: PLPEntryType) -> None:
        self.definition.rules.append(RewritePolicyRule(class_=class_map_ref, plp=plp, dscp=dscp, l2cos=l2cos))

    model_config = ConfigDict(populate_by_name=True)


class RewritePolicyEditPayload(RewritePolicy, PolicyDefinitionId):
    pass


class RewritePolicyGetResponse(RewritePolicy, PolicyDefinitionGetResponse):
    pass
