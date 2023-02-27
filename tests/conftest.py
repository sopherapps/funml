from __future__ import annotations
from typing import List, Any

from funml import record, Enum


@record
class Student:
    name: str
    favorite_color: "Color"


@record
class Color:
    r: int
    g: int
    b: int
    a: List["Alpha"]


class Alpha(Enum):
    OPAQUE = None
    TRANSLUCENT = float


@record
class Department:
    seniors: list[str]
    juniors: List[str]
    locations: tuple[str, ...]
    misc: dict[str, Any]
    head: str
