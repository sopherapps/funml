"""Enumerable user-defined data types

Results in something like:

Initialization
--
>> Color = enum("Color")\
                .opt("RED")\
                .opt("BLUE", shape={'h': str, 's': str})\
                .opt("GREEN", shape=(int, str)))

Usage
--
>> r = Color.RED
>> g = Color.GREEN(6, "string")
>> b = Color.BLUE({'h': 'when', 's': 'how'})
"""
from typing import Type, Union, Tuple, Dict, Optional, Any

from funml import utils, types


def enum(enum_name: str) -> Type["Enum"]:
    """Creates an enum"""
    return type(enum_name, (Enum,), {})


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


class Enum(types.MLType):
    """An enumerable data type"""

    signature: Optional[Union[Tuple[Type, ...], Dict[str, Type]]] = None
    _name: str = ""

    def __init__(self, *args: Union[Any, Dict[str, Any], int]):
        if not _is_valid(args, self.signature):
            raise TypeError(
                f"expected data type passed to be {self.signature}, got {args}"
            )

        self._value = args

    @classmethod
    def opt(
        cls,
        name: str,
        shape: Optional[Union[Type, Tuple[Type, ...], Dict[str, Type]]] = None,
    ) -> Type["Enum"]:
        """Adds a given option to the enum"""
        dotted_name = f"{cls.__name__}.{name}"
        signature = shape
        if not isinstance(signature, (dict, tuple, type(None))):
            # transform stuff like shape=int into shape=(int,)
            signature = (signature,)

        if signature is None:
            opt_value = cls(name)
        else:
            # each option is a subclass of this enum class
            opt_value = type(dotted_name, (cls,), {})

        opt_value._name = dotted_name
        opt_value.signature = signature

        setattr(cls, name, opt_value)
        return cls

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def generate_case(self, expn: types.Expression):
        """Generates a case statement for pattern matching"""
        op = lambda *args: expn(*args)
        if self._value is not None:
            op = lambda arg: expn(_get_enum_captured_value(arg))

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


def _get_enum_captured_value(instance: Enum):
    """Gets the captured value for a given enum instance"""
    if isinstance(instance.signature, tuple) and len(instance.value) == 1:
        return instance.value[0]
    return instance.value
