def square(x):
    return x * x


def triple(x):
    return 3 * x


def identity(x):
    return x


def increment(x):
    return x + 1


def piecewise(f, g, b):
    """Returns the piecewise function h where:

    h(x) = f(x) if x < b,
           g(x) otherwise

    >>> def negate(x):
    ...     return -x
    >>> abs_value = piecewise(negate, identity, 0)
    >>> abs_value(6)
    6
    >>> abs_value(-1)
    1
    """
    "*** YOUR CODE HERE ***"
    def choose_function(x):
        """Return f(x) if x < b, g(x) otherwise"""
        if x < b:
            return f(x)
        else:
            return g(x)

    return choose_function


def product(n, term):
    """Return the product of the first n terms in a sequence.

    n    -- a positive integer
    term -- a function that takes one argument

    >>> product(3, identity) # 1 * 2 * 3
    6
    >>> product(5, identity) # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)   # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)   # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    """
    "*** YOUR CODE HERE ***"
    total = 1
    for i in range(1, n+1):
        total *= term(i)

    return total


def factorial(n):
    """Return n factorial for n >= 0 by calling product.

    >>> factorial(4)
    24
    >>> factorial(6)
    720
    """
    "*** YOUR CODE HERE ***"
    return product(n, identity)


from operator import add, mul


def accumulate(combiner, base, n, term):
    """Return the result of combining the first n terms in a sequence.

    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)   # 2 * 1^2 * 2^2 * 3^2
    72
    """
    "*** YOUR CODE HERE ***"
    total = base
    for i in range(1, n+1):
        total = combiner(term(i), total)

    return total


def summation_using_accumulate(n, term):
    """An implementation of summation using accumulate.

    >>> summation_using_accumulate(5, square)
    55
    >>> summation_using_accumulate(5, triple)
    45
    """
    "*** YOUR CODE HERE ***"
    return accumulate(add, 0, n, term)


def product_using_accumulate(n, term):
    """An implementation of product using accumulate.

    >>> product_using_accumulate(4, square)
    576
    >>> product_using_accumulate(6, triple)
    524880
    """
    "*** YOUR CODE HERE ***"
    return accumulate(product, 1, n, term)


def repeated(f, n):
    """Return the function that computes the nth application of f.

    >>> add_three = repeated(increment, 3)
    >>> add_three(5)
    8
    >>> repeated(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> repeated(square, 2)(5) # square(square(5))
    625
    >>> repeated(square, 4)(5) # square(square(square(square(5))))
    152587890625
    """
    "*** YOUR CODE HERE ***"
    def repeated_function(x):
        """Return f(...f(f(x))...)"""
        result = x
        for i in range(n):
            result = f(result)
        return result

    return repeated_function


def compose1(f, g):
    """Return a function h, such that h(x) = f(g(x))."""
    def h(x):
        return f(g(x))
    return h

###################
# Extra Questions #
###################


def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


def one(f):
    """Church numeral 1: same as successor(zero)"""
    "*** YOUR CODE HERE ***"
    return lambda x: f(x)


def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    "*** YOUR CODE HERE ***"
    return lambda x: f(f(x))


three = successor(two)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    "*** YOUR CODE HERE ***"
    test_function = increment
    test_x = 0
    church_start = zero
    int_start = 0

    while church_start(test_function)(test_x) != n(test_function)(test_x):
        church_start = successor(church_start)
        int_start += 1

    return int_start


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    "*** YOUR CODE HERE ***"
    total = m
    for i in range(church_to_int(n)):
        total = successor(total)

    return total


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    "*** YOUR CODE HERE ***"
    total = m
    for i in range(church_to_int(n) - 1):
        total = add_church(total, m)
    return total


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    "*** YOUR CODE HERE ***"
    total = m
    for i in range(church_to_int(n) - 1):
        total = mul_church(total, m)
    return total

