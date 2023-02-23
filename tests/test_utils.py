from __future__ import annotations

import typing
from typing import List, Any

import funml.utils as fn_utils
from tests import inspect_stock_annotations, inspect_stringized_annotations


def test_generate_random_string():
    """Generates unique random strings"""
    names = [fn_utils.generate_random_string() for _ in range(8)]
    assert len(set(names)) == 8


def test_get_annotations_with_stock_annotations():
    """Adapted from the standard library: https://github.com/python/cpython/blob/main/Lib/test/test_inspect.py"""
    isa = inspect_stock_annotations
    assert fn_utils.get_cls_annotations(isa.MyClass) == {"a": int, "b": str}
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass) == {}

    assert fn_utils.get_cls_annotations(isa.MyClass, eval_str=True) == {
        "a": int,
        "b": str,
    }
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass, eval_str=True) == {}

    assert fn_utils.get_cls_annotations(isa.MyClass, eval_str=False) == {
        "a": int,
        "b": str,
    }
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass, eval_str=False) == {}


def test_get_annotations_with_stringized_annotations():
    """Adapted from the standard library: https://github.com/python/cpython/blob/main/Lib/test/test_inspect.py"""
    isa = inspect_stringized_annotations
    assert fn_utils.get_cls_annotations(isa.MyClass) == {
        "a": "int",
        "b": "str",
        "c": "tuple[str, ...]",
    }
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass) == {}

    assert fn_utils.get_cls_annotations(isa.MyClass, eval_str=True) == {
        "a": int,
        "b": str,
        "c": typing.Tuple[str, ...],
    }
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass, eval_str=True) == {}

    assert fn_utils.get_cls_annotations(isa.MyClass, eval_str=False) == {
        "a": "int",
        "b": "str",
        "c": "tuple[str, ...]",
    }
    assert fn_utils.get_cls_annotations(isa.UnannotatedClass, eval_str=False) == {}

    # test that local namespace lookups work
    assert fn_utils.get_cls_annotations(isa.MyClassWithLocalAnnotations) == {
        "x": "mytype"
    }
    assert fn_utils.get_cls_annotations(
        isa.MyClassWithLocalAnnotations, eval_str=True
    ) == {"x": int}


def test_get_cls_defaults():
    """get_cls_defaults returns the default values of a given class' attributes"""

    class Department:
        seniors: list[str] = ["John"]
        juniors: List[str]
        locations: tuple[str, ...] = ()
        misc: dict[str, Any] = {}
        head: str = "John"

    ann = fn_utils.get_cls_annotations(Department, eval_str=True)
    defaults = fn_utils.get_cls_defaults(Department, annotations=ann)
    assert defaults == {
        "seniors": ["John"],
        "locations": (),
        "misc": {},
        "head": "John",
    }


def test_right_pad_list():
    """right_pad_list pads a given list with the given fill_value"""
    test_data = [
        ([5, 6], "foo", 4, [5, 6, "foo", "foo"]),
        (
            (
                5,
                6,
            ),
            "foo",
            4,
            [5, 6, "foo", "foo"],
        ),
        ([5, 6], "foo", 1, [5, 6]),
        (
            (
                5,
                6,
            ),
            "foo",
            1,
            [5, 6],
        ),
    ]

    for items, fill_value, target_length, expected in test_data:
        padded_list = fn_utils.right_pad_list(
            items, fill_value=fill_value, target_length=target_length
        )
        assert padded_list == expected
