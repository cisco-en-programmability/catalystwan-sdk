# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum


class PrintColors(Enum):
    RED_BACKGROUND = "\033[41m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    NONE = "\033[0m"
