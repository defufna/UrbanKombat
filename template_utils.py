_num_names = ["one", "two", "three", "four", "five"]

def count(i):
    if i < 1:
        raise ValueError("only numbers greater than zero are supported")
    if i > len(_num_names):
        return str(i)
    return _num_names[i-1]

collective_nouns = (
    (5, "group"),
    (10, "mob"),
    (25, "horde")
)

def collective_phrase(count):
    global collective_nouns

    if count < collective_nouns[0][0]:
        return "are"
    
    for min_count, noun in collective_nouns:
        if count > min_count:
            break
    
    return "is a {} of".format(noun)

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