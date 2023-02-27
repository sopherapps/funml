from __future__ import annotations

from collections.abc import Callable
from os import PathLike
from typing import Optional, List, Any

import pytest

from funml import record, to_dict, Enum, to_json, from_json


def test_records_created():
    """record creates distinct records"""

    @record
    class Color:
        r: int
        g: int
        b: int
        a: int

    blue = Color(r=0, g=0, b=255, a=1)
    red = Color(r=255, g=0, b=0, a=1)
    green = Color(r=0, g=255, b=0, a=1)

    another_blue = Color(r=0, g=0, b=255, a=1)
    another_red = Color(r=255, g=0, b=0, a=1)
    another_green = Color(r=0, g=255, b=0, a=1)

    assert blue == another_blue
    assert green == another_green
    assert red == another_red

    assert blue != green
    assert red != blue
    assert green != red


def test_unexpected_fields():
    """Unexpected fields throw error"""

    @record
    class Color:
        r: int
        g: int
        b: int
        a: Optional[int]

    try:
        _ = Color(r=56, g=4, b=45)  # no error
    except Exception as exc:
        assert False, f"'Color' raised an exception {exc}"

    with pytest.raises(TypeError):
        _ = Color(r=56, o=45, a=5)


def test_no_extra_fields():
    """No extra fields are allowed"""

    @record
    class Color:
        r: int
        g: int
        b: int
        a: int

    with pytest.raises(TypeError):
        _ = Color(r=56, g=4, b=45, a=5, y=0)


def test_records_with_defaults():
    """Records that have default values act as expected."""

    @record
    class Department:
        seniors: list[str] = ["John"]
        juniors: List[str]
        locations: tuple[str, ...] = ()
        misc: dict[str, Any] = {}
        head: str = "John"

    mostly_default_record = Department(juniors=[])
    security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
    )
    it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        head="Paul",
    )

    assert mostly_default_record == Department(
        juniors=[], seniors=["John"], locations=(), misc={}, head="John"
    )
    assert security_dept == Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
        head="John",
    )
    assert it_dept == Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        head="Paul",
    )


def test_generic_alias_fields():
    """Fields with generic alias act as expected"""

    @record
    class Department:
        seniors: list[str]
        juniors: List[str]
        locations: tuple[str, ...]
        misc: dict[str, Any]
        is_active: bool | None
        description: ...
        func: Callable[[int], Any]
        path: bytes | PathLike[bytes] | str = ""
        branch: "Branch"

    class Branch(Enum):
        HeadOffice = None
        Arua = None
        Nebbi = None

    echo = lambda v: v

    security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
        is_active=False,
        description="security",
        func=echo,
        branch=Branch.Arua,
    )
    it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        is_active=True,
        description="it",
        func=echo,
        branch=Branch.Nebbi,
    )
    hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
        is_active=False,
        description=4,
        func=echo,
        branch=Branch.HeadOffice,
    )

    another_security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
        is_active=False,
        description="security",
        func=echo,
        branch=Branch.Arua,
    )
    another_it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        is_active=True,
        description="it",
        func=echo,
        branch=Branch.Nebbi,
    )
    another_hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
        is_active=False,
        description=4,
        func=echo,
        branch=Branch.HeadOffice,
    )

    assert security_dept == another_security_dept
    assert it_dept == another_it_dept
    assert hr_dept == another_hr_dept

    assert security_dept != it_dept
    assert it_dept != hr_dept
    assert hr_dept != security_dept


def test_dict():
    """record can be cast to dict using to_dict"""

    @record
    class Department:
        seniors: list[str]
        juniors: List[str]
        locations: tuple[str, ...]
        misc: dict[str, Any]
        head: str

    test_data = [
        dict(
            seniors=["Joe", "Jane"],
            juniors=["Herbert", "Leo"],
            locations=("Kasasa", "Bujumbura", "Bugahya"),
            misc={"short_name": "ScDept"},
            head="John",
        ),
        dict(
            seniors=["Paul"],
            juniors=["Perry"],
            locations=("Kampala", "Cairo"),
            misc={"name": "IT Department"},
            head="Jane",
        ),
        dict(
            seniors=["Stella", "Isingoma"],
            juniors=["Peter"],
            locations=("Katanga",),
            misc={"short_name": "HRDept"},
            head="Peter",
        ),
    ]

    for data in test_data:
        dept = Department(**data)
        assert to_dict(dept) == data


def test_to_json():
    """to_json transforms record into a JSON string representation of record"""

    @record
    class Student:
        name: str
        favorite_color: "Color"

    @record
    class Color:
        r: int
        g: int
        b: int
        a: "Alpha"

    class Alpha(Enum):
        OPAQUE = None
        TRANSLUCENT = float

    test_data = [
        (
            Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
            '{"r": 8, "g": 4, "b": 78, "a": "Alpha.OPAQUE: \\"OPAQUE\\""}',
        ),
        (
            Color(r=55, g=40, b=9, a=Alpha.TRANSLUCENT(0.4)),
            '{"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}',
        ),
        (
            Student(
                name="John Doe",
                favorite_color=Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
            ),
            '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": "Alpha.OPAQUE: \\"OPAQUE\\""}}',
        ),
        (
            Student(
                name="Jane Doe",
                favorite_color=Color(r=55, g=40, b=9, a=Alpha.TRANSLUCENT(0.4)),
            ),
            '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}}',
        ),
    ]

    for item, expected in test_data:
        assert to_json(item) == expected


def test_from_json_strict():
    """from_json with strict transforms a JSON string representation into an Record, raising ValueError if it can't"""

    @record
    class Student:
        name: str
        favorite_color: "Color"

    @record
    class Color:
        r: int
        g: int
        b: int
        a: "Alpha"

    class Alpha(Enum):
        OPAQUE = None
        TRANSLUCENT = float

    test_data = [
        (
            Color,
            '{"r": 8, "g": 4, "b": 78, "a": "Alpha.OPAQUE: \\"OPAQUE\\""}',
            Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
        ),
        (
            Color,
            '{"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}',
            Color(r=55, g=40, b=9, a=Alpha.TRANSLUCENT(0.4)),
        ),
        (
            Student,
            '{"name": "John Doe", "favorite_color": {"r": 8, "g": 4, "b": 78, "a": "Alpha.OPAQUE: \\"OPAQUE\\""}}',
            Student(
                name="John Doe",
                favorite_color=Color(r=8, g=4, b=78, a=Alpha.OPAQUE),
            ),
        ),
        (
            Student,
            '{"name": "Jane Doe", "favorite_color": {"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}}',
            Student(
                name="Jane Doe",
                favorite_color=Color(r=55, g=40, b=9, a=Alpha.TRANSLUCENT(0.4)),
            ),
        ),
    ]

    for cls, item, expected in test_data:
        assert from_json(cls, item) == expected


def test_from_json_not_strict():
    """non-strict from_json transforms a JSON string representation into an Record,
    returning the default json-parsed value if an error occurs"""

    @record
    class Student:
        name: str
        favorite_color: "Color"

    @record
    class Color:
        r: int
        g: int
        b: int
        a: "Alpha"

    class Alpha(Enum):
        OPAQUE = None
        TRANSLUCENT = float

    test_data = [
        (
            Color,
            '["r", 8, "g", 4, "b", 78, "a", "Alpha.OPAQUE: \\"OPAQUE\\""]',
            ["r", 8, "g", 4, "b", 78, "a", 'Alpha.OPAQUE: "OPAQUE"'],
        ),
        (Color, '"foo"', "foo"),
        (
            Student,
            '{"name": "John Doe", "favorite_color": 9}',
            {"name": "John Doe", "favorite_color": 9},
        ),
        (
            Student,
            '{"name": 90, "favorite_color": {"r": 55, "g": 40, "b": 9, "a": "Alpha.TRANSLUCENT: 0.4"}}',
            {
                "name": 90,
                "favorite_color": {
                    "r": 55,
                    "g": 40,
                    "b": 9,
                    "a": "Alpha.TRANSLUCENT: 0.4",
                },
            },
        ),
    ]

    for cls, item, expected in test_data:
        assert from_json(cls, item, strict=False) == expected

        with pytest.raises(ValueError, match=r"unable to deserialize JSON.*"):
            from_json(cls, item)
