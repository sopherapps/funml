"""Deals with conversion to and from JSON strings.
"""
import json
from typing import Any

from funml import Enum, Record
from funml.data.lists import IList


def to_json(value: Any) -> str:
    """Converts the type into a JSON string.

    Returns:
        the JSON string representation of this instance
    """
    if isinstance(value, Enum):
        return _enum_to_json(value)
    if isinstance(value, Record):
        return _record_to_json(value)
    if isinstance(value, IList):
        return _i_list_to_json(value)
    if isinstance(value, (tuple, list, set)):
        return f"[{', '.join([to_json(v) for v in value])}]"
    if isinstance(value, dict):
        items = [f'"{k}": {to_json(v)}' for k, v in value.items()]
        return f"{{{', '.join(items)}}}"
    return json.dumps(value)


def _enum_to_json(item: Enum) -> str:
    """Converts an enum into JSON string"""
    return f'"{item.name}: {to_json(item.value)}"'


def _record_to_json(item: Record) -> str:
    """Converts a record into JSON string"""
    items = [f'"{k}": {to_json(v)}' for k, v in item]
    return f"{{{', '.join(items)}}}"


def _i_list_to_json(item: IList) -> str:
    """Converts an iList into JSON string"""
    return to_json(list(item))


# def from_json(value: str) -> Any:
#     """Converts a JSON string into a type
#
#     Returns:
#         the instance got from the JSON string
#     """
#     if isinstance(value, Enum):
#         return _enum_from_json(value)
#     if isinstance(value, Record):
#         return _record_from_json(value)
#     if isinstance(value, IList):
#         return _i_list_from_json(value)
#     if isinstance(value, (tuple, list, set)):
#         return json.dumps([to_json(v) for v in value])
#     if isinstance(value, dict):
#         return json.dumps({k: to_json(v) for k, v in value.items()})
#     return json.dumps(value)
#
#
# def _enum_to_json(item: Enum) -> str:
#     """Converts an enum into JSON string"""
#     return f"{item.name}: {to_json(item.value)}"
#
#
# def _record_to_json(item: Record) -> str:
#     """Converts a record into JSON string"""
#     return json.dumps({k: to_json(v) for k, v in item})
#
#
# def _i_list_to_json(item: IList) -> str:
#     """Converts an iList into JSON string"""
#     return to_json(list(item))
