import numpy as np

def deep_len(lst):
    """Returns the deep length of the list.

    >>> deep_len([1, 2, 3])     # normal list
    3
    >>> x = [1, [2, 3], 4]      # deep list
    >>> deep_len(x)
    4
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> deep_len(x)
    6
    """
    "*** YOUR CODE HERE ***"
    count = 0
    for e in lst:
        if type(e) == list:
            count += deep_len(e)
        else:
            count += 1
    return count


def interval(a, b):
    """Construct an interval from a to b."""
    "*** YOUR CODE HERE ***"
    return [a, b]


def lower_bound(x):
    """Return the lower bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[0]


def upper_bound(x):
    """Return the upper bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[1]


def str_interval(x):
    """Return a string representation of interval x.

    >>> str_interval(interval(-1, 2))
    '-1 to 2'
    """
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))


def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y.

    >>> str_interval(add_interval(interval(-1, 2), interval(4, 8)))
    '3 to 10'
    """
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)


def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y.

    >>> str_interval(mul_interval(interval(-1, 2), interval(4, 8)))
    '-8 to 16'
    """
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))


def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by any value in y.

    Division is implemented as the multiplication of x by the reciprocal of y.

    >>> str_interval(div_interval(interval(-1, 2), interval(4, 8)))
    '-0.25 to 0.5'
    >>> str_interval(div_interval(interval(4, 8), interval(-1, 2)))
    AssertionError
    """
    "*** YOUR CODE HERE ***"
    assert upper_bound(y) * lower_bound(y) >= 0, 'Divisor cannot span zero!'

    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)


def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y.

    >>> str_interval(sub_interval(interval(-1, 2), interval(4, 8)))
    '-9 to -2'
    """
    "*** YOUR CODE HERE ***"
    lower = lower_bound(x) - lower_bound(y)
    upper = upper_bound(x) - upper_bound(y)
    return interval(lower, upper)


def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))


def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))

# These two intervals give different results for parallel resistors:
"*** YOUR CODE HERE ***"


def multiple_references_explanation():
    return """The mulitple reference problem..."""


def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    "*** YOUR CODE HERE ***"
    def f(t):
        """Quadratic function with coefficients a, b, c."""
        return a*t*t + b*t + c

    mid = -b / (2*a)
    left, right = lower_bound(x), upper_bound(x)

    left_val, mid_val, right_val = f(left), f(mid), f(right)

    if left <= mid <= right:
        return interval(min(left_val, mid_val, right_val), max(left_val, mid_val, right_val))
    else:
        return interval(min(left_val, right_val), max(left_val, right_val))


def polynomial(x, c):
    """Return the interval that is the range of the polynomial defined by
    coefficients c, for domain interval x.

    >>> str_interval(polynomial(interval(0, 2), [-1, 3, -2]))
    '-3 to 0.125'
    >>> str_interval(polynomial(interval(1, 3), [1, -3, 2]))
    '0 to 10'
    >>> str_interval(polynomial(interval(0.5, 2.25), [10, 24, -6, -8, 3]))
    '18.0 to 23.0'
    """
    "*** YOUR CODE HERE ***"
    def factorial(k, n):
        """Factorial starting from n with k consecutives."""
        if n == 1:
            return k
        else:
            return k * factorial(k-1, n-1)

    def f(t):
        """Polynomial function with coefficients in list c."""
        k = len(c)
        result = 0
        for i in range(k):
            result += c[i] * pow(t, i)
        return result

    def make_df(n):
        """Higher order function that returns n th derivative of polynomial function."""
        def df(t):
            """n th derivatives of polynomial function"""
            k = len(c)
            result = 0
            for i in range(n, k):
                result += c[i] * pow(t, i-n) * factorial(i, n)
            return result
        return df

    # function for Newton's Method
    def improve(update, close, guess):
        while not close(guess):
            guess = update(guess)
        return guess

    def approx_eq(x, y, tolerance=1e-15):
        return abs(x - y) < tolerance

    def newton_update(f, df):
        def update(x):
            return x - f(x) / df(x)
        return update

    def find_zero(f, df, initial_guess):
        def near_zero(x):
            return approx_eq(f(x), 0)
        return improve(newton_update(f, df), near_zero, initial_guess)

    # values in two endpoints
    left, right = lower_bound(x), upper_bound(x)
    left_val, right_val = f(left), f(right)

    # values in the middle
    mid_val_lst = []
    for initial_guess in np.arange(left, right, (right-left)/10):
        mid = find_zero(make_df(1), make_df(2), initial_guess)
        if left <= mid <= right:
            mid_val_lst.append(f(mid))

    return interval(min(mid_val_lst + [left_val, right_val]), max(mid_val_lst + [left_val, right_val]))







