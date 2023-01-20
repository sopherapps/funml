"""lists that support functional programming concepts easily

Usage
---

# assignment

>> list1 = l(9, 7, 0)

# prepending data (immutably) i.e. new list is got

>> value = l(5, 6, list1)

# appending data (immutably) i.e. new list is got

>> value = l(list1, 7, 9)

# deleting data (immutably) i.e. new list is got
>> value = list1.filter(lambda v: v > 9)

# transforming data (immutably) i.e. new list is got
>> value = list1.map(lambda v: v + 9)

# destructuring list: the last argument gets all remaining items as one list
>> let(int, l(v, y, others)) <= list1

# iterating data
>> loop = fn(match(v)
            | l() <= fn()
            | l(head, tail) <= fn(
                                 lambda head: print(head),
                                 loop(tail),
                                 )
"""
