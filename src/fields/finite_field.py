import random
import itertools

from integer_ring import IntegerRing
from quotient_field import QuotientFieldMeta
from polynomial_ring import PolynomialRing


class FiniteFieldMeta(QuotientFieldMeta):

    # Other class methods.

    @staticmethod
    def cardinality(F):
        return IntegerRing(F.characteristic()._**F.dimension()._)

    @staticmethod
    def all_elements(F):
        for _ in itertools.product(*(xrange(F.characteristic()._) for _ in xrange(F.dimension()._))):
            if len(_) == 1:
                yield F(F.base_ring()(_[0]))
            else:
                yield F(F.base_ring()(list(_)))

    @staticmethod
    def random_element(F):
        if F.dimension() == IntegerRing(1):
            return F(random.randrange(F.characteristic()._))
        else:
            return F([
                random.randrange(F.characteristic()._)
                for _ in xrange(F.dimension()._)
            ])

    @staticmethod
    def sqrt(F, a):
        assert isinstance(a, F)
        if not a:
            return F(0)

        q = F.cardinality() - 1
        e = 0
        o = q
        while o % 2 == 0:
            e = e + 1
            o = o / 2

        def pow(a, n):
            if n == 0:
                return F(1)
            if n == 1:
                return F(a)
            if n % 2 == 0:
                return pow(a*a, n / 2)
            else:
                return pow(a*a, n / 2) * a

        nr = None
        while True:
            nr = F.random_element()
            if not nr:
                continue
            if pow(nr, q / 2) != 1:
                break

        def sqrt_aux(a):
            a_o = pow(a, o)
            d = 0
            while a_o != F(1):
                a_o = a_o*a_o
                d += 1
            if d == e:
                return None
            if d == 0:
                return pow(a, (o+1)/2)
            nr2ed1 = pow(nr, 1 << (e - d - 1))
            nr2ed = nr2ed1 * nr2ed1
            s = sqrt_aux(a * nr2ed)
            if s is not None:
                return s / nr2ed1
            else:
                return None

        return sqrt_aux(a)

    # Meta initialization.

    def __new__(meta, base_ring, modulus, characteristic, dimension):
        return type.__new__(
            meta,
            'FiniteField(%s,%s,%s,%s)' % (base_ring.__name__, repr(modulus), repr(characteristic), repr(dimension), ),
            (object, ),
            {}
        )

    def __init__(cls, base_ring, modulus, characteristic, dimension):
        c = cls
        m = FiniteFieldMeta
        _ = lambda _: m.coerce(c, _)
        # Inherited methods.
        super(m, c).__init__(base_ring, modulus)
        # Other class methods.
        c.cardinality = classmethod(lambda c: m.cardinality(c))
        c.all_elements = classmethod(lambda c: m.all_elements(c))
        c.random_element = classmethod(lambda c: m.random_element(c))
        c.sqrt = classmethod(lambda c, a: m.sqrt(c, _(a)))
        c.characteristic = classmethod(lambda c: IntegerRing(characteristic))
        c.dimension = classmethod(lambda c: IntegerRing(dimension))

def FiniteField(characteristic, dimension=IntegerRing(1), modulus=None):
    if dimension == 1:
        return FiniteFieldMeta(
            IntegerRing,
            characteristic,
            characteristic,
            dimension
        )
    else:
        return FiniteFieldMeta(
            PolynomialRing(QuotientField(IntegerRing, characteristic)),
            modulus,
            characteristic,
            dimension
        )
