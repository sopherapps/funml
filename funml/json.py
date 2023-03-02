"""Deals with conversion to and from JSON strings.
"""
import inspect
import json
import typing
from typing import Any, TypeVar, Type, Mapping, Tuple, Union, Dict

from funml import Enum, Record
from funml.data.lists import IList
from funml.utils import right_pad_list, extract_type


def to_json(value: Any) -> str:
    """Converts the type into a JSON string.

    Args:
        value: the value to convert to a JSON string

    Returns:
        the JSON string representation of this instance

    Example:
        ```python
        import funml as ml


        @ml.record
        class Student:
            name: str
            favorite_color: "Color"

        @ml.record
        class Color:
            r: int
            g: int
            b: int
            a: "Alpha"

        class Alpha(ml.Enum):
            OPAQUE = None
            TRANSLUCENT = float

        items = [
            ml.l(
                True,
                Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
                Color(r=55, g=40, b=9, a=Alpha.TRANSLUCENT(0.4)),
            ),
            Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
            Alpha.TRANSLUCENT(0.4),
        ]

        for item in items:
            item_json = ml.to_json(item)
            print(item_json)
        ```
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
    if isinstance(item.value, str):
        return f'"{item.name}: \\"{item.value}\\""'
    return f'"{item.name}: {to_json(item.value)}"'


def _record_to_json(item: Record) -> str:
    """Converts a record into JSON string"""
    items = [f'"{k}": {to_json(v)}' for k, v in item]
    return f"{{{', '.join(items)}}}"


def _i_list_to_json(item: IList) -> str:
    """Converts an iList into JSON string"""
    return to_json(list(item))


T = TypeVar("T")
Q = TypeVar("Q")


def from_json(type_: Type[T], value: str, strict: bool = True) -> T:
    """Converts a JSON string into the given type.

    If strict is True, an error is returned if the JSON string cannot be converted into
    the type, else if strict is False and an error occurs,
    the default python primitive is str, dict etc.
    is returned.

    Args:
        type_: the typing annotation to which the JSON string is to be converted to
        value: the JSON string
        strict: whether the JSON string should be strictly converted to the given type
            or left as the default primitive python objects

    Returns:
        the instance got from the JSON string

    Raises:
        ValueError: unable to deserialize JSON to given type

    Example:
        ```python
        import funml as ml


        @ml.record
        class Student:
            name: str
            favorite_color: "Color"

        @ml.record
        class Color:
            r: int
            g: int
            b: int
            a: "Alpha"

        class Alpha(ml.Enum):
            OPAQUE = None
            TRANSLUCENT = float

        items = [
            (
                ml.IList[Color],
                (
                "["
                '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": "Alpha.OPAQUE: \\"OPAQUE\\""}}, '
                '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}}'
                "]"
                )
            ),
            (Color, '{"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}'),
            (Alpha, "Alpha.TRANSLUCENT: 0.4"),
        ]

        # setting strict to False can allow any json string to be converted to a python object,
        # first attempting to convert it to the provided type, and if it fails,
        # the output of an ordinary json.loads call is returned.
        #
        # However, when strict is True, ValueError's will be raised
        # if the json string can't be converted into the given type
        strict = True

        for type_, item_json in items:
            item = ml.from_json(type_=type_, value=item_json, strict=strict)
            print(item)
        ```
    """
    actual_type = extract_type(type_)
    frame = inspect.currentframe()

    try:
        _globals = frame.f_back.f_globals
        _locals = frame.f_back.f_locals

        if issubclass(actual_type, Enum):
            return _enum_from_json(
                actual_type, value, strict, _globals=_globals, _locals=_locals
            )
        if issubclass(actual_type, Record):
            return _record_from_json(
                actual_type, value, strict, _globals=_globals, _locals=_locals
            )
        if issubclass(actual_type, IList):
            return _i_list_from_json(
                type_, value, strict, _globals=_globals, _locals=_locals
            )

        obj = json.loads(value)
        if strict:
            return _cast_to_annotation(
                type_, value=obj, _globals=_globals, _locals=_locals
            )
        else:
            return _try_cast_to_annotation(
                type_, value=obj, _globals=_globals, _locals=_locals
            )
    finally:
        del frame


def _enum_from_json(
    type_: Type[Enum],
    value: str,
    strict: bool,
    _globals: Dict[str, Any] = ...,
    _locals: Dict[str, Any] = ...,
) -> Union[Enum, Any]:
    """Converts a JSON string to an Enum.

    If strict is True, an error is raised if JSON cannot be turned into the Enum
    else it returns the default python object that would be got from parsing the
    JSON in python, in case an error occurs.

    Raises:
        ValueError: unable to deserialize JSON to given type
    """
    try:
        # enum json value has '"' at the beginning and at the end thus the stripping
        value_as_str = value.strip('"')
        full_name, data = value_as_str.split(": ", maxsplit=1)
        enum_name, name = full_name.split(".", maxsplit=1)

        if enum_name != type_.__name__:
            raise ValueError(
                f"expected enum of type {enum_name}, got enum of type {type_.__name__}"
            )

        variant = getattr(type_, name)

        if variant.signature is not None:
            data = json.loads(data)
            data = _cast_to_signature(variant.signature, data, _globals, _locals)

            if isinstance(variant.signature, tuple):
                return variant(*data)

            return variant(data)

        return variant
    except Exception as exp:
        if strict:
            raise ValueError(
                f"unable to deserialize JSON {value} to {type_}. The following error occurred: {exp}"
            )
        return value


def _record_from_json(
    type_: Type[Record],
    value: str,
    strict: bool,
    _globals: Dict[str, Any] = ...,
    _locals: Dict[str, Any] = ...,
) -> Union[Record, Any]:
    """Converts a JSON string to a record

    If strict is True, an error is raised if JSON cannot be turned into the Enum
    else it returns the default python object that would be got from parsing the
    JSON in python, in case an error occurs.

    Raises:
        ValueError: unable to deserialize JSON to given type
    """
    try:
        obj = json.loads(value)

        try:
            parsed_obj = _cast_to_signature(
                type_.get_annotations(_globals, _locals), obj, _globals, _locals
            )
            return type_(**parsed_obj)
        except Exception as exp:
            if strict:
                raise exp
            return obj

    except Exception as exp:
        raise ValueError(
            f"unable to deserialize JSON {value} to {type_}. The following error occurred: {exp}"
        )


def _i_list_from_json(
    type_: Type[IList[T]],
    value: str,
    strict: bool,
    _globals: Dict[str, Any] = ...,
    _locals: Dict[str, Any] = ...,
) -> Union[IList[T], IList[Any]]:
    """Converts a JSON string to an IList.

    If strict is True, an error is raised if JSON cannot be turned into the Enum
    else it returns the default python object that would be got from parsing the
    JSON in python, in case an error occurs.

    Raises:
        ValueError: unable to deserialize JSON to given type
    """
    try:
        items = json.loads(value)
        item_type = getattr(type_, "__args__", (Any,))[0]

        if strict:
            return IList(
                *[_cast_to_annotation(item_type, v, _globals, _locals) for v in items]
            )

        return IList(
            *[_try_cast_to_annotation(item_type, v, _globals, _locals) for v in items]
        )
    except Exception as exp:
        raise ValueError(
            f"unable to deserialize JSON {value} to IList. The following error occurred: {exp}"
        )


def _cast_to_signature(
    signature: Union[Tuple[Type, ...], Dict[str, Type], Type],
    value: Any,
    _globals: Dict[str, Any],
    _locals: Dict[str, Any],
) -> Any:
    """Attempts to cast a value to a given signature.

    Useful when deserializing.

    Args:
        signature: the expected shape of the value
        value: the value to cast to a given shape

    Returns:
        the value cast to the given signature
    """
    try:
        if isinstance(signature, tuple):
            padded_sig = right_pad_list(signature, len(value), Any)
            return tuple(
                [
                    _cast_to_signature(type_, v, _globals, _locals)
                    for type_, v in zip(padded_sig, value)
                ]
            )
        elif isinstance(signature, dict):
            return {
                k: _cast_to_signature(signature[k], v, _globals, _locals)
                for k, v in value.items()
            }

        return _cast_to_annotation(signature, value, _globals, _locals)
    except Exception as exp:
        return value


def _try_cast_to_annotation(
    annotation: Type[T], value: Any, _globals: Dict[str, Any], _locals: Dict[str, Any]
) -> Union[T, Any]:
    """Tries to cast a given value to a given type, or returns the original value if it fails."""
    try:
        return _cast_to_annotation(annotation, value, _globals, _locals)
    except Exception as exp:
        return value


def _cast_to_annotation(
    annotation: Type[T], value: Any, _globals: Dict[str, Any], _locals: Dict[str, Any]
) -> T:
    """Casts a given value to a given type annotation"""
    actual_type = extract_type(annotation)

    if issubclass(actual_type, Record) and isinstance(value, dict):
        parsed_data = _cast_to_signature(
            actual_type.get_annotations(_globals, _locals), value, _globals, _locals
        )
        return actual_type(**parsed_data)

    elif issubclass(actual_type, Enum) and isinstance(value, str):
        return _enum_from_json(actual_type, value, True, _globals, _locals)

    elif issubclass(actual_type, IList):
        type_ = getattr(annotation, "__args__", (Any,))[0]
        return actual_type(
            *[_cast_to_annotation(type_, v, _globals, _locals) for v in value]
        )

    elif issubclass(actual_type, Mapping):
        v_type = getattr(annotation, "__args__", (Any, Any))
        return actual_type(
            {
                k: _cast_to_annotation(v_type, v, _globals, _locals)
                for k, v in value.items()
            }
        )

    elif actual_type in (tuple, Tuple):
        args = getattr(annotation, "__args__", (Any,))
        padded_args = right_pad_list(args, len(value), Any)
        return tuple(
            [
                _cast_to_annotation(type_, v, _globals, _locals)
                for type_, v in zip(padded_args, value)
            ]
        )

    elif issubclass(actual_type, (list, set)):
        type_ = getattr(annotation, "__args__", (Any,))[0]
        return actual_type(
            [_cast_to_annotation(type_, v, _globals, _locals) for v in value]
        )

    if actual_type not in (Any, ..., object) and actual_type != type(value):
        raise TypeError(
            f"value {value} should be of type: {actual_type}, got {type(value)}"
        )

    return value
