"""pattern matching using the match syntax

Usage
--
# enums
>> value = match(raw_value)
        | Option.SOME(v) <= fn(lambda v: v + 6)
        | Option.NONE    <= fn()

# records
>> value2 = match(raw_value2)
            | Color(r, g, ...) <= fn(lambda r, g: r + g)
            | ExamResult(total) <= fn(lambda v: v)

# lists
>> value3 = match(raw_value3)
            | l(_, 5, rest) <= fn(5)
            | l(8, 5, rest) <= fn(rest)

# combined
>> value = match(raw_value)
        | Option.SOME(v)     <= fn(lambda v: v + 6)
        | Option.NONE        <= fn()
        | Color(r, g, ...)   <= fn(lambda r, g: r + g)
        | ExamResult(total)  <= fn(lambda v: v)
        | l(_, 5, rest)     <= fn(5)
        | l(8, 5, rest) <= fn(rest)
"""
