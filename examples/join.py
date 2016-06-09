def join(sequence, sep):
    result = ''
    for e in sequence[:-1]:
        result += e + sep
    result += sequence[-1]
    return result
