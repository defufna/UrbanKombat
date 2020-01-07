_num_names = ["one", "two", "three", "four", "five"]

def count(i):
    if i < 1:
        raise ValueError("only numbers greater than zero are supported")
    if i > len(_num_names):
        return str(i)
    return _num_names[i-1]

def detect_last(iterable):
    i = iter(iterable)

    try:
        prev = next(i)
    except StopIteration:
        return

    try:
        while True:
            current = next(i)
            yield (False, prev)
            prev = current
    except StopIteration:
        yield (True, prev)