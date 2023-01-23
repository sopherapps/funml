"""Enumerable user-defined data types

Results in something like:

Initialization
--
>> enum(Color = e("RED") | e("BLUE").of({'h': str, 's': str}) | e("GREEN").of((int, str)))

Usage
--
>> r = Color.RED
>> g = Color.GREEN(6, "string")
>> b = Color.BLUE({'h': 'when', 's': 'how'})
"""
from typing import Type, Union, Tuple, Dict, Optional, Any

from funml import utils, types


def enum(**kwargs: "EnumMeta") -> type:
    """Creates an enum"""
    if len(kwargs) != 1:
        raise ValueError(f"required 1 key-word argument, got {len(kwargs)}")

    [(enum_name, enum_meta)] = kwargs.items()
    new_enum = type(enum_name, (Enum,), {})

    for k in enum_meta:
        name = f"{enum_name}.{k.name}"

        if isinstance(k.signature, (tuple, dict)):
            # each option is a subclass of the `new_enum`
            v = type(name, (new_enum,), {})
        else:
            v = new_enum(k.name)

        v._name = name
        v._signature = k.signature
        setattr(new_enum, k.name, v)

    return new_enum


def e(name: str) -> "EnumMeta":
    """A user-friendly way to create an EnumMeta"""
    return EnumMeta(name)


def _is_valid(
    value: Tuple[Any, ...],
    signature: Optional[Union[Tuple[Type, ...], Dict[str, Type]]],
) -> bool:
    """Checks to see if value is of given signature"""
    if signature is None:
        return True
    elif isinstance(signature, tuple) and isinstance(value, tuple):
        return all([utils.is_type(v, sig) for sig, v in zip(signature, value)])
    elif isinstance(signature, dict) and len(value) == 1 and isinstance(value[0], dict):
        return all(
            [
                utils.is_type(value[0].get(sig_key, None), sig_type)
                for sig_key, sig_type in signature.items()
            ]
        )
    return False


class Enum:
    """An enumerable data type"""

    _signature: Optional[Union[Tuple[Type, ...], Dict[str, Type]]] = None
    _name: str = ""

    def __init__(self, *args: Union[Any, Dict[str, Any], int]):
        if not _is_valid(args, self._signature):
            raise TypeError(
                f"expected data type passed to be {self._signature}, got {args}"
            )

        self._value = args

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def generate_case(self, expn: types.Expression):
        """Generates a case statement for pattern matching"""
        op = lambda *args: expn(**args)
        if self._value is not None:
            op = lambda arg: expn(arg._get_captured_value())

        return self._is_like, types.Expression(types.Operation(func=op))

    def __eq__(self, other: "Enum"):
        return (
            self.__class__ == other.__class__
            and self._name == other._name
            and self._value == other._value
        )

    def _is_like(self, other):
        """Checks that a value has the given pattern"""
        if not isinstance(other, Enum):
            return False

        return (
            self.__class__ == other.__class__
            and self._name == other._name
            and (self._value == other._value or _is_valid(other._value, self._value))
        )

    def _get_captured_value(self):
        """Gets the captured value for a given enum instance"""
        if isinstance(self._signature, tuple) and len(self.value) == 1:
            return self.value[0]
        return self.value


class EnumMeta:
    def __init__(self, name: str):
        self.name = name
        self.signature: Optional[Union[Tuple[Type, ...], Dict[str, Type]]] = None
        self.prev: Optional["EnumMeta"] = None

    def of(self, signature: Union[Tuple[Type, ...], Dict[str, Type]]):
        """Sets the data type of the associated data"""
        self.signature = signature
        return self

    def __or__(self, other: "EnumMeta") -> "EnumMeta":
        """'|' is used to combine EnumMeta into a linked list of enumMeta

        e.g. EnumMeta("P") | EnumMeta("O")
        """
        other.prev = self
        return other

    def __iter__(self):
        """Returns list of EnumMeta in reversed order starting from this one"""
        yield self

        curr = self.prev
        while curr is not None:
            yield curr
            curr = curr.prev
