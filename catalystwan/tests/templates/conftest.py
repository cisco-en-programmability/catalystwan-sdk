# Copyright 2026 Cisco Systems, Inc. and its affiliates
import json
from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture(scope="module")
def template_payload_dir() -> Path:
    return Path(Path(__file__).resolve().parent / "payload")


@pytest.fixture(scope="module")
def template_definition_loader(template_payload_dir) -> Callable[[str], dict]:

    def loader(path: str) -> dict:
        filepath = template_payload_dir / path
        return json.load(open(filepath))

    return loader
