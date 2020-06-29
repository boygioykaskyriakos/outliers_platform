def func_max(f, g):
    return lambda x: max((f(x), g(x)))


def double(x):
    return 2*x


def square(x):
    return x*x


if __name__ == "__main__":
    h1 = func_max(double, square)
    assert h1(1) == 2
    assert h1(3) == 9
    h2 = func_max(double, abs)
    assert h2(-2) == 2
