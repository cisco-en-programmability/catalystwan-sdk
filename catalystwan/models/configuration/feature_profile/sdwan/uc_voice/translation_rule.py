# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase

Action = Literal[
    "reject",
    "replace",
]


class RuleSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    action: Optional[Global[Action]] = Field(default=None)
    match: Optional[Global[str]] = Field(default=None)
    replacement_pattern: Optional[Global[str]] = Field(
        default=None, validation_alias="replacementPattern", serialization_alias="replacementPattern"
    )
    rule_num: Optional[Global[int]] = Field(default=None, validation_alias="ruleNum", serialization_alias="ruleNum")


class TranslationRuleParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["translation-rule"] = Field(default="translation-rule", exclude=True)
    rule_settings: List[RuleSettings] = Field(
        validation_alias=AliasPath("data", "ruleSettings"),
        description="Translation Rule configuration",
    )
    rule_name: Optional[Global[int]] = Field(default=None, validation_alias="ruleName", serialization_alias="ruleName")
