from datetime import date
from typing import Any

import funml as ml


def main():
    """Main program"""
    # define some data types
    class Date(ml.Enum):
        January = date
        February = date
        March = date
        April = date
        May = date
        June = date
        July = date
        August = date
        September = date
        October = date
        November = date
        December = date

    @ml.record
    class Color:
        r: int
        g: int
        b: int
        a: int

    # defining a number of functions
    is_even = lambda v: v % 2 == 0
    is_not_number = lambda v: not isinstance(v, (int, float))
    multiply = lambda x, y: x * y
    superscript = lambda num, power: num**power
    accumulated_factorial = (
        lambda num, accum: accum
        if num <= 0
        else accumulated_factorial(num - 1, num * accum)
    )
    get_month = lambda value: value.month

    # ml.Result
    get_type_str = lambda v: f"{type(v)}"
    make_type_err = lambda *args: ml.Result.ERR(
        TypeError(f"expected numbers, got {', '.join(ml.l(*args).map(get_type_str))}")
    )
    try_multiply = (
        lambda x, y: make_type_err(x, y)
        if any(ml.l(x, y).map(is_not_number))
        else ml.Result.OK(multiply(x, y))
    )

    # Option
    result_to_option = (
        ml.match()
        .case(ml.Result.ERR(Exception), do=lambda: ml.Option.NONE)
        .case(ml.Result.OK(Any), do=lambda v: ml.Option.SOME(v))
    )

    # some pattern matching
    to_date_enum = lambda date_value: (
        ml.match(date_value.month)
        .case(
            1,
            do=lambda: Date.January(date_value),
        )
        .case(
            2,
            do=lambda: Date.February(date_value),
        )
        .case(
            3,
            do=lambda: Date.March(date_value),
        )
        .case(
            4,
            do=lambda: Date.April(date_value),
        )
        .case(
            5,
            do=lambda: Date.May(date_value),
        )
        .case(
            6,
            do=lambda: Date.June(date_value),
        )
        .case(
            7,
            do=lambda: Date.July(date_value),
        )
        .case(
            8,
            do=lambda: Date.August(date_value),
        )
        .case(
            9,
            do=lambda: Date.September(date_value),
        )
        .case(
            10,
            do=lambda: Date.October(date_value),
        )
        .case(
            11,
            do=lambda: Date.November(date_value),
        )
        .case(
            12,
            do=lambda: Date.December(date_value),
        )
    )()

    # combine a number of functions into bigger ones
    cube = ml.let(int, power=3) >> superscript
    factorial = ml.let(int, accum=1) >> accumulated_factorial
    get_month_str = ml.val(get_month) >> (
        ml.match()
        .case(1, do=lambda: "JAN")
        .case(2, do=lambda: "FEB")
        .case(3, do=lambda: "MAR")
        .case(4, do=lambda: "APR")
        .case(5, do=lambda: "MAY")
        .case(6, do=lambda: "JUN")
        .case(7, do=lambda: "JUL")
        .case(8, do=lambda: "AUG")
        .case(9, do=lambda: "SEP")
        .case(10, do=lambda: "OCT")
        .case(11, do=lambda: "NOV")
        .case(12, do=lambda: "DEC")
    )

    dates = [
        date(200, 3, 4),
        date(2009, 1, 16),
        date(1993, 12, 29),
        date(2004, 10, 13),
        date(2020, 9, 5),
        date(2004, 5, 7),
        date(1228, 8, 18),
    ]

    nums = ml.l(12, 3, 45, 7, 8, 6, 3)

    dates_as_enums = ml.l(*dates).map(to_date_enum)
    print(f"\ndates as enums: {dates_as_enums}")

    print(f"\nfirst date enum: {dates_as_enums[0]}")

    months_as_str = ml.l(*dates).map(get_month_str)
    print(f"\nmonths of dates as str:\n{months_as_str}")

    print(f"\ncube of 5: {cube(5)}")

    factorials_str = nums.filter(is_even).map(
        lambda v: f"factorial for {v}: {factorial(v)}"
    )
    print("\n".join(factorials_str))

    blue = Color(r=0, g=0, b=255, a=1)
    print(f"blue: {blue}")

    data = ml.l((2, 3), ("hey", 7), (5, "y"), (8.1, 6)).map(lambda x: try_multiply(*x))
    print(f"\nafter multiplication:\n{data}")

    data_as_options = data.map(result_to_option)
    print(f"\ndata as options: {data_as_options}")


if __name__ == "__main__":
    main()
