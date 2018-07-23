__all__ = ('pow',)


def pow(a, x, m):
    res = 1
    while x:
        if x & 1 == 1:
            res = res * a % m
        a = a * a % m
        x >>= 1
    return res
