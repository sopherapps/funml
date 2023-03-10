from copy import copy
from datetime import date

import funml as ml


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
    a: int = 1


def main():
    """Main program"""

    """
    Primitive Expressions
    """
    unit = ml.val(lambda v: v)
    is_even = ml.val(lambda v: v % 2 == 0)
    mul = ml.val(lambda args: args[0] * args[1])
    superscript = ml.val(lambda num, power=1: num**power)
    get_month = ml.val(lambda value: value.month)
    is_num = ml.val(lambda v: isinstance(v, (int, float)))
    is_exp = ml.val(lambda v: isinstance(v, BaseException))
    if_else = lambda check=unit, do=unit, else_do=unit: ml.val(
        lambda *args, **kwargs: (
            ml.match(check(*args, **kwargs))
            .case(True, do=lambda: do(*args, **kwargs))
            .case(False, do=lambda: else_do(*args, **kwargs))
        )()
    )

    """
    High Order Expressions
    """
    factorial = lambda v, accum=1: (
        ml.match(v <= 0)
        .case(True, do=ml.val(accum))
        .case(False, do=lambda num, ac=0: factorial(num - 1, accum=num * ac)())
    )
    # currying expressions is possible
    cube = superscript(power=3)
    get_item_types = ml.ireduce(lambda x, y: f"{type(x)}, {type(y)}")
    nums_type_err = ml.val(
        lambda args: TypeError(f"expected numbers, got {get_item_types(args)}")
    )
    is_seq_of_nums = ml.ireduce(lambda x, y: x and is_num(y), True)
    to_result = ml.val(lambda v: ml.Result.ERR(v) if is_exp(v) else ml.Result.OK(v))

    try_multiply = (
        if_else(check=is_seq_of_nums, do=mul, else_do=nums_type_err) >> to_result
    )

    result_to_option = ml.if_ok(ml.Option.SOME, strict=False) >> ml.if_err(
        lambda *args: ml.Option.NONE, strict=False
    )
    to_date_enum = ml.val(
        lambda v: (
            ml.match(v.month)
            .case(1, do=ml.val(Date.January(v)))
            .case(2, do=ml.val(Date.February(v)))
            .case(3, do=ml.val(Date.March(v)))
            .case(4, do=ml.val(Date.April(v)))
            .case(5, do=ml.val(Date.May(v)))
            .case(6, do=ml.val(Date.June(v)))
            .case(7, do=ml.val(Date.July(v)))
            .case(8, do=ml.val(Date.August(v)))
            .case(9, do=ml.val(Date.September(v)))
            .case(10, do=ml.val(Date.October(v)))
            .case(11, do=ml.val(Date.November(v)))
            .case(12, do=ml.val(Date.December(v)))
        )()
    )
    get_month_str = get_month >> (
        ml.match()
        .case(1, do=ml.val("JAN"))
        .case(2, do=ml.val("FEB"))
        .case(3, do=ml.val("MAR"))
        .case(4, do=ml.val("APR"))
        .case(5, do=ml.val("MAY"))
        .case(6, do=ml.val("JUN"))
        .case(7, do=ml.val("JUL"))
        .case(8, do=ml.val("AUG"))
        .case(9, do=ml.val("SEP"))
        .case(10, do=ml.val("OCT"))
        .case(11, do=ml.val("NOV"))
        .case(12, do=ml.val("DEC"))
    )

    """
    Data
    """
    dates = [
        date(200, 3, 4),
        date(2009, 1, 16),
        date(1993, 12, 29),
        date(2004, 10, 13),
        date(2020, 9, 5),
        date(2004, 5, 7),
        date(1228, 8, 18),
    ]
    dates = ml.val(dates)
    nums = ml.val(ml.l(12, 3, 45, 7, 8, 6, 3))
    data = ml.l((2, 3), ("hey", 7), (5, "y"), (8.1, 6))
    blue = Color(r=0, g=0, b=255)

    """
    Pipeline Creation and Execution
    """
    dates_as_enums = dates >> ml.imap(to_date_enum) >> ml.execute()
    print(f"\ndates as enums: {dates_as_enums}")

    print(f"\nfirst date enum: {dates_as_enums[0]}")

    months_as_str = dates >> ml.imap(get_month_str) >> ml.execute()
    print(f"\nmonths of dates as str:\n{months_as_str}")

    print(f"\ncube of 5: {cube(5)}")

    even_nums_pipeline = nums >> ml.ifilter(is_even)
    # here `even_nums_pipeline` is a `Pipeline` instance
    print(even_nums_pipeline)

    factorials_list = (
        copy(even_nums_pipeline)
        >> ml.imap(lambda v: f"factorial for {v}: {factorial(v)}")
        >> ml.execute()
    )
    # we created a new pipeline by coping the previous one
    # otherwise we would be mutating the old pipeline.
    # Calling ml.execute(), we get an actual iterable of strings
    print(factorials_list)

    factorials_str = (
        even_nums_pipeline
        >> ml.imap(lambda v: f"factorial for {v}: {factorial(v)}")
        >> ml.ireduce(lambda x, y: f"{x}\n{y}")
        >> ml.execute()
    )
    # here after calling ml.execute(), we get one string as output
    print(factorials_str)

    print(f"blue: {blue}")

    data = ml.val(data) >> ml.imap(try_multiply) >> ml.execute()
    print(f"\nafter multiplication:\n{data}")

    data_as_options = ml.val(data) >> ml.imap(result_to_option) >> ml.execute()
    print(f"\ndata as options: {data_as_options}")

    data_as_actual_values = (
        ml.val(data) >> ml.ifilter(ml.is_ok) >> ml.imap(ml.if_ok(unit)) >> ml.execute()
    )
    print(f"\ndata as actual values: {data_as_actual_values}")


if __name__ == "__main__":
    main()
