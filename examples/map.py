def map(f, sequence):
    out = []
    for e in sequence:
        out.append(f(e))
    return out
