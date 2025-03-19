# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .cybervision import CyberVisonParcel
from .thousandeyes import ThousandEyesParcel
from .ucse import UcseParcel

AnyOtherParcel = Annotated[
    Union[ThousandEyesParcel, UcseParcel, CyberVisonParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "CyberVisonParcel",
    "ThousandEyesParcel",
    "UcseParcel",
    "AnyOtherParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
