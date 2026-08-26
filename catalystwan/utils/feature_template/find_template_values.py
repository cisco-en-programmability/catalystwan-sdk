# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import Any, Dict, List, Optional, Union

from catalystwan.api.templates.device_variable import DeviceVariable

logger = logging.getLogger(__name__)


class _TreeValueList(list):
    """List of tree values with mapping-style access for a single item."""

    def __getitem__(self, key):
        if isinstance(key, str):
            if len(self) != 1:
                raise KeyError(key)
            item = super().__getitem__(0)
            if not isinstance(item, dict):
                raise KeyError(key)
            return item[key]
        return super().__getitem__(key)


def find_template_values(
    template_definition: dict,
    templated_values: Optional[dict] = None,
    target_key: str = "vipType",
    target_key_default_values: List[str] = ["ignore", "notIgnore"],
    target_key_for_template_value: str = "vipValue",
    path: Optional[List[str]] = None,
    _template_path_prefix: Optional[List[str]] = None,
) -> Dict[str, Union[str, list, dict]]:
    """Based on provided template definition generates a dictionary with template fields and values

    Args:
        template_definition: template definition provided as dict
        templated_values: dictionary, empty at the beginning and filed out with names of fields as keys
            and values of those fields as values
        target_key: name of the key specifying if field is used in template, defaults to 'vipType'
        target_key_default_values: list of values of the target key indicating
            that a field is not used in template, defaults to ['ignore', 'notIgnore']
        target_key_for_template_value: name of the key specifying value of field used in template,
            defaults to 'vipValue'
        path: a list of keys indicating current path, defaults to None
    Returns:
        templated_values: dictionary containing template fields as key and values assigned to those fields as values
    """
    if path is None:
        path = []
    if _template_path_prefix is None:
        _template_path_prefix = []
    if templated_values is None:
        templated_values = {}
    # if value object is reached, try to extract the value
    if target_key in template_definition:
        if template_definition[target_key] in target_key_default_values:
            return templated_values

        value = template_definition[target_key]  # vipType
        template_value = template_definition.get(target_key_for_template_value)

        field_key = path[-1]
        if value in ["variableName", "variable"]:
            # For example this is the current dictionary:
            # field_key is "dns-addr"
            # {
            #     "vipType": "variableName",
            #     "vipValue": "",
            #     "vipObjectType": "object",
            #     "vipVariableName": "vpn_dns_primary",
            # }
            # vipType is "variableName" so we need to return
            # {"dns-addr": DeviceVariable(name="vpn_dns_primary")}
            if var_name := template_definition.get("vipVariableName"):
                new_value = DeviceVariable(name=var_name)
                new_value._object_type = value
                new_value._template_path = tuple(_template_path_prefix + path)
                current_nesting = get_nested_dict(templated_values, path[:-1])
                current_nesting[field_key] = new_value
            return templated_values

        if template_value is None:
            return template_definition

        if template_definition["vipObjectType"] == "list":
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = []
            for item in template_value:
                current_nesting[field_key].append(process_list_value(item))
        elif template_definition["vipObjectType"] != "tree":
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = template_value
        elif isinstance(template_value, dict):
            find_template_values(
                value,
                templated_values,
                target_key,
                target_key_default_values,
                target_key_for_template_value,
                path,
                _template_path_prefix,
            )
        elif isinstance(template_value, list):
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = _TreeValueList()
            for item in template_value:
                item_path_prefix = _template_path_prefix + get_list_item_template_path(
                    template_definition,
                    item,
                    path,
                    target_key,
                    target_key_for_template_value,
                )
                item_value = find_template_values(
                    item,
                    {},
                    target_key,
                    target_key_default_values,
                    target_key_for_template_value,
                    path=[],
                    _template_path_prefix=item_path_prefix,
                )
                if item_value:
                    current_nesting[field_key].append(item_value)
        return templated_values

    # iterate the dict to extract values and assign them to their fields
    for key in ordered_item_keys(template_definition):
        value = template_definition[key]
        if isinstance(value, dict) and value not in target_key_default_values:
            find_template_values(
                value,
                templated_values,
                target_key,
                target_key_default_values,
                target_key_for_template_value,
                path + [key],
                _template_path_prefix,
            )
    return templated_values


def ordered_item_keys(item: dict) -> List[str]:
    """Return payload keys in schema order, followed by any unlisted keys."""
    priority_order = item.get("priority-order", [])
    if not isinstance(priority_order, list):
        priority_order = []
    return [key for key in priority_order if key in item] + [key for key in item if key not in priority_order]


def get_list_item_template_path(
    tree_definition: dict,
    item: Any,
    path: List[str],
    target_key: str,
    target_key_for_template_value: str,
) -> List[str]:
    """Build a stable path for a tree-list item from its concrete primary keys."""
    item_path = list(path)
    if not isinstance(item, dict):
        return item_path

    primary_keys = tree_definition.get("vipPrimaryKey", [])
    if not isinstance(primary_keys, list):
        return item_path

    for key in ordered_item_keys(item):
        if key not in primary_keys:
            continue
        field = item.get(key)
        if not isinstance(field, dict):
            continue

        field_type = field.get(target_key)
        if field_type == "constant":
            value = field.get(target_key_for_template_value)
        elif field_type in ("variableName", "variable"):
            value = field.get("vipVariableName")
        else:
            continue

        if value is not None and not isinstance(value, (dict, list)):
            item_path.append(str(value))

    return item_path


def get_nested_dict(d: dict, path: List[str], populate: bool = True):
    current_dict = d
    for path_key in path:
        if path_key not in current_dict and populate:
            current_dict[path_key] = {}
        current_dict = current_dict[path_key]
    return current_dict


def process_list_value(
    item: Any,
    target_key: str = "vipType",
    target_key_for_template_value: str = "vipValue",
):
    if isinstance(item, dict):
        if target_key in item:
            if item["vipObjectType"] == "list":
                result = []
                for nested_item in item[target_key_for_template_value]:
                    result.append(process_list_value(nested_item))
                return result
            elif item["vipObjectType"] == "tree":
                return find_template_values(item[target_key_for_template_value])
            else:
                return item[target_key_for_template_value]
        else:
            return find_template_values(item)
    else:
        return item
