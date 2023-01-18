"""Enumerable user-defined data types

Results in something like:

Initialization
--
enum(Color = e("RED") | e("BLUE").of({'h': str, 's': str}) | e("GREEN").of((int, str)))

Usage
--
r = Color.RED
g = Color.GREEN(6, "string")
b = Color.BLUE({'h': 'when', 's': 'how'})
"""
from typing import Type, Union, Tuple, Dict, Optional, Any


def enum(**kwargs: "EnumMeta") -> type:
    """Creates an enum"""
    if len(kwargs) != 1:
        raise ValueError(f"required 1 key-word argument, got {len(kwargs)}")

    [(enum_name, enum_meta)] = kwargs.items()
    new_enum = type(enum_name, (Enum,), {})

    for v, k in enumerate(enum_meta):
        if isinstance(
            k.signature,
            tuple,
        ):
            v = classmethod(lambda cls, *args: cls(k.name, args))
            v.__annotations__ = {"args": k.signature, "return": new_enum}
        elif isinstance(k.signature, dict):
            v = classmethod(lambda cls, arg: cls(k.name, arg))
            v.__annotations__ = {"arg": k.signature, "return": new_enum}
        else:
            v = new_enum(k.name, v)

        setattr(new_enum, k.name, v)

    return new_enum


def e(name: str) -> "EnumMeta":
    """A user-friendly way to create an EnumMeta"""
    return EnumMeta(name)


class Enum:
    """An enumerable data type"""

    def __init__(self, name: str, value: Union[Tuple[Any, ...], Dict[str, Any], int]):
        self.__value = value
        self.__name = name

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__value

    def __eq__(self, other: "Enum"):
        return (
            self.__class__ == other.__class__
            and self.__name == other.__name
            and self.__value == other.__value
        )

    def __le__(self, other: Any) -> bool:
        """'<=' is the match operator."""
        if isinstance(other, Enum):
            return self == other
        return False


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
