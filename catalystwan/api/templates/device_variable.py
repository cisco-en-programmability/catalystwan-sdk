# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional, Tuple

from pydantic import BaseModel, PrivateAttr

VariableObjectType = Literal["variable", "variableName"]


class DeviceVariable(BaseModel):
    name: str
    _object_type: VariableObjectType = PrivateAttr(default="variableName")
    _template_path: Optional[Tuple[str, ...]] = PrivateAttr(default=None)
