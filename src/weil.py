# -*- encoding: UTF-8 -*-


import functools
import itertools


class Fp(object):

    class Element(object):

        @staticmethod
        def mod(a, b):
            if b == 0:
                raise ZeroDivisionError
            if a % b == 0:
                return 0
            if b > 0:
                return a % b
            if b < 0:
                return a % b - b

        @staticmethod
        def div(a, b):
            return (a - Fp.Element.mod(a, b)) // b

        @staticmethod
        def gcd(a, b):
            if b == 0:
                return (a, 1, 0)
            d, k, l = Fp.Element.gcd(b, Fp.Element.mod(a, b))
            # d == k*b + l*(a % b)
            # a % b = a - q*b
            # d == k*b + l*(a - q*b)
            # d == k*b + l*a - l*q*b)
            # d == l*a + (k - l*q)*b
            return (d, l, k - l*Fp.Element.div(a, b))

        def __init__(self, a, p):
            self.a = a%p
            self.p = p

        def __str__(self):
            return "%d (mod %d)" % (self.a, self.p)

        def __add__(self, other):
            return self.__class__(self.a + other.a, self.p)

        def __sub__(self, other):
            return self.__class__(self.a - other.a, self.p)

        def __mul__(self, other):
            return self.__class__(self.a * other.a, self.p)

        def __div__(self, other):
            d, k, l = Fp.Element.gcd(other.a, self.p)
            if d != 1:
                raise ZeroDivisionError
            return self.__class__(self.a*k, self.p)


    @staticmethod
    def is_prime(n):
        if n % 2 == 0:
            return False
        if n % 3 == 0:
            return False
        d = 4
        while d*d <= n:
            if n % d == 0 or n % (d+2) == 0:
                return False
            d += 6
        return True

    def __init__(self, p):
        assert Fp.is_prime(p)
        self.p = p

    def __call__(self, a):
        assert isinstance(a, int)
        return Fp.Element(a, self.p)


class Polynomial(object):

    @staticmethod
    def verify_idx_and_coeff(field, idx_and_coeff):
        idx, coeff = idx_and_coeff
        assert isinstance(coeff, field)
        assert isinstance(idx, int)
        assert idx >= 0
        return idx_and_coeff

    @classmethod
    def X(cls, field):
        return cls(field, {1: field(1)})

    def __init__(self, *list_args):
        if len(list_args) == 1:
            self.field = list_args[0].field
            self.coeffs = copy(list_args[0].coeffs)
            return
        else:
            field, arg = list_args
        self.field = field
        if isinstance(arg, self.field):
            if arg == self.field(0):
                self.coeffs = {}
            else:
                self.coeffs = {0: arg}
        else:
            items = arg
            if isinstance(arg, dict):
                items = arg.iteritems()
            self.coeffs = dict(
                itertools.ifilter(
                    lambda (idx, coeff): coeff != self.field(0),
                    itertools.imap(
                        lambda (idx, coeffs): (idx, reduce(lambda x, y: x+y[1], coeffs, self.field(0))),
                        itertools.groupby(
                            itertools.imap(
                                functools.partial(self.__class__.verify_idx_and_coeff, self.field),
                                items
                            ),
                            lambda (idx, coeff): idx
                        )
                    )
                )
            )

    def __str__(self):
        if self.deg() == -1:
            return str(self.field(0))
        return ' + '.join(
            (
                (str(coeff) if (coeff != self.field(1) or idx == 0) else '')
                +
                (('X^{%d}' % idx) if idx > 1 else ('X' if idx == 1 else ''))
            )
            for idx, coeff in self.coeffs.iteritems()
        )

    def deg(self):
        if self.coeffs:
            return max(self.coeffs.keys())
        else:
            return -1

    def __getitem__(self, idx):
        return self.coeffs.get(idx, self.field(0))

    def keys(self):
        return self.coeffs.keys()

    def iterkeys(self):
        return self.coeffs.iterkeys()

    def values(self):
        return self.coeffs.values()

    def itervalues(self):
        return self.coeffs.itervalues()

    def items(self):
        return self.coeffs.items()

    def iteritems(self):
        return self.coeffs.iteritems()

    def __iter__(self):
        return self.iteritems()

    def __neg__(self):
        return self.__class__(
            self.field,
            itertools.imap(
                lambda (idx, coeff): (idx, -coeff),
                self.iteritems()
            )
        )

    def __add__(self, other):
        if isinstance(other, self.field):
            return self + self.__class__(self.field, {0: other})
        elif isinstance(other, self.__class__):
            return self.__class__(
                self.field,
                itertools.chain(self.iteritems(), other.iteritems())
            )
        else:
            return NotImplemented

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, self.field):
            return self * self.__class__(self.field, {0: other})
        elif isinstance(other, self.__class__):
            return self.__class__(
                self.field,
                itertools.imap(
                    lambda ((idx1, coeff1), (idx2, coeff2)): (idx1+idx2, coeff1*coeff2),
                    itertools.product(self.iteritems(), other.iteritems())
                )
            )
        else:
            return NotImplemented

    def div_mod(self, other):
        q = self.__class__(self.field, {})
        m = self.__class__(self)
        while m.deg() >= other.deg():
            digit = m[m.deg()] / other[other.deg()]
            shift = self.__class__(self.field, {(m.deg() - other.deg()): self.field(1)})
            q = q + digit*shift
            m = m - digit*shift*other
        return (q, m)

    def __div__(self, other):
        return self.div_mod(other)[0]

    def __mod__(self, other):
        return self.div_mod(other)[1]


F7 = Fp(7)

Polynomial(F7.Element, {1: F7(1)})

X = Polynomial.X(F7.Element)

print (X*X + F7(2)*X + F7(1)) / (X + F7(1))
