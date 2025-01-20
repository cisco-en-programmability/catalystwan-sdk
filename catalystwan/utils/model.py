# Copyright 2024 Cisco Systems, Inc. and its affiliates
from functools import lru_cache
from inspect import isclass
from typing import Any, List, Optional, Type, Union

from pydantic import BaseModel
from typing_extensions import Annotated, get_args, get_origin


def resolve_nested_base_model_unions(
    annotation: Any, models_types: List[Type[BaseModel]] = list()
) -> List[Type[BaseModel]]:
    """given something like AnyParcel produces flat list of BaseModel sub-types present in that union

    Args:
        annotation (Any): Union of BaseModels (could be Annotated and nested)
        models_types (List[Type[BaseModel]], optional): used internally in recurence

    Raises:
        TypeError: when contents are not BaseModel (can be Annotated)

    Returns:
        List[Type[BaseModel]]: flat list of subclasses of BaseModel present in input
    """

    models_types = list(dict.fromkeys(models_types))

    if isclass(annotation):
        if issubclass(annotation, BaseModel):
            return [annotation]

    if get_origin(annotation) in [Annotated, Union]:
        for arg in get_args(annotation):
            models_types.extend(resolve_nested_base_model_unions(arg, models_types))
        return list(dict.fromkeys(models_types))

    return list()


@lru_cache
def get_model_type_field(model: Type[BaseModel]) -> Optional[str]:
    if type_field := model.model_fields.get("type"):
        if default_value := type_field.default:
            return str(default_value)
    return None
