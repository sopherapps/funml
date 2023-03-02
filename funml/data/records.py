"""Schema types for similar records.

Typical Usage:

    ```python
    import funml as ml

    @ml.record
    class Color:
        r: int
        g: int
        b: int
        a: int = 1

    blue = Color(r=0, g=0, b=255, a=1)
    red = Color(r=255, g=0, b=0, a=1)
    green = Color(r=0, g=255, b=0)

    print(blue)
    # prints: {'r': 0, 'g': 0, 'b': 255, 'a': 1}

    print(red)
    # prints: {'r': 255, 'g': 0, 'b': 0, 'a': 1}

    print(green)
    # prints: {'r': 0, 'g': 255, 'b': 0, 'a': 1}
    ```
"""
import dataclasses
import importlib
import inspect
import re
from typing import (
    Dict,
    Any,
    Type,
    Callable,
    Tuple,
    TypeVar,
    Optional,
    Mapping,
    Set,
    List,
    Union,
    ForwardRef,
)

from typing_extensions import dataclass_transform

from funml import utils, types


_compound_type_regex = re.compile(r"tuple|list|set|dict")
_compound_type_generic_type_map = {
    "tuple": "Tuple",
    "dict": "Dict",
    "list": "List",
    "set": "Set",
}
_default_globals = {
    "Tuple": Tuple,
    "Dict": Dict,
    "Set": Set,
    "List": List,
    "Union": Union,
}


R = TypeVar("R", bound="Record")


def to_dict(v: "Record") -> Dict[str, Any]:
    """Converts a record into a dictionary.

    Args:
        v: the `Record` to convert to dict

    Returns:
        the dictionary representation of the record

    Example:
        ```python
        import funml as ml


        @ml.record
        class Department:
            seniors: list[str]
            juniors: List[str]
            locations: tuple[str, ...]
            misc: dict[str, Any]
            head: str

        sc_dept = Department(
            seniors=["Joe", "Jane"],
            juniors=["Herbert", "Leo"],
            locations=("Kasasa", "Bujumbura", "Bugahya"),
            misc={"short_name": "ScDept"},
            head="John",
        )

        data = ml.to_dict(sc_dept)
        print(data)
        ```
    """
    return dict(v)


@dataclass_transform(
    field_specifiers=(dataclasses.Field, dataclasses.field),
)
def record(cls: Type[R]) -> Type[R]:
    """Creates a Schema type to create similar records.

    Used usually as a decorator inplace of @dataclass
    on dataclass-like classes to make them ml-functional.

    It creates a Schema for similar objects that contain a given
    set of attributes. For example, it can create a `Book` schema
    whose attributes include `author`, `title`, `isbn` etc.

    Args:
        cls: the class to transform into a record

    Returns:
        A class which can act as a record of the particular schema \
        set by the attributes.

    Example:
        ```python
        import funml as ml

        @ml.record
        class Color:
            red: int
            green: int
            blue: int
            alpha: int = 1

        indigo = Color(red=75, green=0, blue=130)

        print(indigo)
        # prints {'red': 75, 'green': 0, 'blue': 130, 'alpha': 1}
        ```
    """
    _annotations = cls.__annotations__

    return dataclasses.dataclass(
        type(
            cls.__name__,
            (
                Record,
                cls,
            ),
            {
                "__annotations__": _annotations,
                "__slots__": tuple(_annotations.keys()),
                "__defaults__": _get_cls_defaults(cls, _annotations=_annotations),
                "__is_normalized__": False,
                "__module_path__": cls.__module__,
            },
        ),
        init=False,
        repr=False,
    )


def _is_valid(kwargs: Dict[str, Any], annotations: Dict[str, Any]):
    """validates the key-word arguments passed to record when initializing"""
    if len(kwargs) > len(annotations):
        return False

    return all([utils.is_type(v, annotations.get(k, None)) for k, v in kwargs.items()])


class Record(types.MLType):
    """A Schema type for creating similar records.

    Basically, any unique record type subclasses Record, sets
    the expected attributes and then is used to create new instances
    of that record type.

    Make sure you don't access the `__annotations__` class property directly as it may not have
    all annotations normalized from string to their actual types yet. Instead use the `get_annotations` class method.

    This type is usually not used directly but rather we use the [@record](funml.record) decorator

    Example:

        ```python
        import funml as ml

        @ml.record
        class Color:
            r: int
            g: int
            b: int
            a: int = 1
        ```

    Args:
        kwargs: the data for the current record instance.

    Raises:
        TypeError: the data passed is does not correspond to the expected annotations.
    """

    __defaults__: Dict[str, Any] = {}
    __is_normalized__: bool = False
    __module_path__: str

    def __init__(self, **kwargs: Any):
        frame = inspect.currentframe()
        try:
            self._normalize(
                _globals=dict(frame.f_back.f_globals),
                _locals=dict(frame.f_back.f_locals),
            )
        finally:
            del frame

        kwargs = {**self.__defaults__, **kwargs}
        self.__attrs = kwargs

        if not _is_valid(kwargs, self.__annotations__):
            raise TypeError(
                f"expected key-word arguments of signature {self.__annotations__}, got {kwargs}"
            )

        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get_annotations(
        cls, _globals: Dict[str, Any], _locals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gets the annotations of this record.

        Args:
            _globals: the dict containing any global variables relevant for the current context
            _locals: the dict containing any local variables relevant for the current context

        Returns:
            the dict of the annotations of this class with each annotation evaluated from string to its right type.
        """
        cls._normalize(_globals, _locals)
        return cls.__annotations__

    @classmethod
    def _normalize(cls, _globals: Dict[str, Any], _locals: Dict[str, Any]):
        """Normalizes any lazy imports in annotations and the dependent variables"""
        if not cls.__is_normalized__:
            module = importlib.import_module(cls.__module_path__)
            _globals.update(_default_globals)
            _globals.update(getattr(module, "__dict__", {}))
            _annotations = {}

            for key, value in cls.__annotations__.items():
                if isinstance(value, str):
                    value = _parse_lazy_type(_to_generic(value), _globals, _locals)

                value = _evaluate_forward_refs(value, _globals, _locals)
                _annotations[key] = value

            cls.__annotations__ = _annotations
            cls._validate_class_defaults()
            cls.__dataclass_fields__ = _annotations
            cls.__is_normalized__ = True

    @classmethod
    def _validate_class_defaults(cls):
        """Checks whether the class default values are valid with regards to the annotations"""
        for k, v in cls.__defaults__.items():
            type_ = cls.__annotations__[k]

            if not utils.is_type(v, type_):
                raise TypeError(
                    f"attribute {k} should be of type {type_}; got default: {v}"
                )

    def _is_like(self, other) -> bool:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        if not isinstance(other, Record) or self.__class__ != other.__class__:
            return False

        for k, v in self.__attrs.items():
            if getattr(other, k, None) != v:
                return False

        return True

    def generate_case(self, do: types.Operation) -> Tuple[Callable, types.Expression]:
        """See Base Class: [`MLType`][funml.types.MLType]"""
        return self._is_like, types.Expression(
            types.Operation(func=lambda *args: do(*args))
        )

    def __str__(self):
        """A readable representation of this type."""
        return f"{self.__attrs}"

    def __repr__(self):
        return f"{self.__class__.__name__}{self.__attrs}"

    def __iter__(self):
        return ((k, v) for k, v in self.__attrs.items())


def _to_generic(annotation: str) -> str:
    """Converts a future annotation like list[str] to a generic annotation e.g. List[str]

    This is just for compatibility when it comes to python < 3.10

    Args:
        annotation: the annotation in its string form

    Returns:
        the annotation in string form showcasing its Generic equivalent
    """
    union_args = annotation.split("|")
    if len(union_args) > 1:
        annotation = f"Union[{','.join(union_args)}]"

    return _compound_type_regex.sub(
        lambda v: _compound_type_generic_type_map[v.string[v.start() : v.end()]],
        annotation,
    )


def _parse_lazy_type(
    value: str,
    __globals: Optional[Dict[str, Any]] = ...,
    __locals: Optional[Mapping[str, Any]] = ...,
):
    """Converts a type value expressed as a string into its python value."""
    try:
        value = value.strip("'")
        return eval(value, __globals, __locals)
    except TypeError as exp:
        if "not subscriptable" in f"{exp}":
            # ignore types that are not supported in the given version
            return Any
        raise exp


def _evaluate_forward_refs(
    type_: Type,
    __globals: Optional[Dict[str, Any]] = ...,
    __locals: Optional[Mapping[str, Any]] = ...,
) -> Type:
    """Evaluates any forward refs in the given type"""
    try:
        type_.__args__ = tuple(
            _evaluate_forward_refs(arg, __globals, __locals) for arg in type_.__args__
        )
    except AttributeError:
        if isinstance(type_, ForwardRef):
            return eval(type_.__forward_arg__, __globals, __locals)
    return type_


def _get_cls_defaults(cls: type, _annotations: Dict[str, type]) -> Dict[str, Any]:
    """Retrieves all default values of a class attributes.

    Args:
        cls: the class
        _annotations: the annotations of the class

    Returns:
        a dictionary of attributes and their default values
    """
    defaults = {}

    for attr, type_ in _annotations.items():
        try:
            defaults[attr] = getattr(cls, attr)
        except AttributeError:
            pass

    return defaults
