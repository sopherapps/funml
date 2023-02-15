from __future__ import annotations
from typing import Optional, List, Any, Tuple, Dict

import pytest

from funml import record


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


# FIXME: record with also do defaults


def test_generic_alias_fields():
    """Fields with generic alias act as expected"""

    @record
    class Department:
        seniors: list[str]
        juniors: List[str]
        locations: tuple[str, ...]
        misc: dict[str, Any]

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
    )
    hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
    )

    another_security_dept = Department(
        seniors=["Joe", "Jane"],
        juniors=["Herbert", "Leo"],
        locations=("Kasasa", "Bujumbura", "Bugahya"),
        misc={"short_name": "ScDept"},
    )
    another_it_dept = Department(
        seniors=["Paul"],
        juniors=["Perry"],
        locations=("Kampala", "Cairo"),
        misc={"name": "IT Department"},
    )
    another_hr_dept = Department(
        seniors=["Stella", "Isingoma"],
        juniors=["Peter"],
        locations=("Katanga",),
        misc={"short_name": "HRDept"},
    )

    assert security_dept == another_security_dept
    assert it_dept == another_it_dept
    assert hr_dept == another_hr_dept

    assert security_dept != it_dept
    assert it_dept != hr_dept
    assert hr_dept != security_dept
