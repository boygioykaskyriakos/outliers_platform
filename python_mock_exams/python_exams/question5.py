import numpy as np
from copy import copy


def balance(init_sum, int_rate, tfl, tax_rate, M):
    s = copy(init_sum)
    for m in range(M):
        # calculate balance of month with interest rate
        monthly_interest = s*int_rate/100
        # calculate tax if applicable
        if s > tfl:
            monthly_tax = (s-tfl) * tax_rate/100
        else:
            monthly_tax = 0

        s += monthly_interest-monthly_tax

    return s


if __name__ == "__main__":
    np.testing.assert_almost_equal(balance(10000, 1, 20000, 1, 2), 10201)
    np.testing.assert_almost_equal(balance(25000, 2, 20000, 1, 2), 25904.5)
    np.testing.assert_almost_equal(balance(19800, 2, 20000, 1, 2), 20597.96)


