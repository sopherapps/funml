from __future__ import annotations

from collections.abc import Callable
from os import PathLike
from pathlib import PurePath
from typing import Optional, List, Any

import pytest

from funml import record, to_dict


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

    echo = lambda v: v

    security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
        is_active=False,
        description="security",
        func=echo,
    )
    it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        is_active=True,
        description="it",
        func=echo,
    )
    hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
        is_active=False,
        description=4,
        func=echo,
    )

    another_security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
        is_active=False,
        description="security",
        func=echo,
    )
    another_it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
        is_active=True,
        description="it",
        func=echo,
    )
    another_hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
        is_active=False,
        description=4,
        func=echo,
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
