# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .cflowd import CflowdParcel
from .node import NodeInfo
from .security_logging import SecurityLoggingParcel

AnyNetworkHierarchyParcel = Annotated[
    Union[CflowdParcel, SecurityLoggingParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "CflowdParcel",
    "SecurityLoggingParcel",
    "NodeInfo",
]


def __dir__() -> "List[str]":
    return list(__all__)
