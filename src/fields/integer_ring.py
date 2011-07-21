class IntegerRingMeta(type):

    # Initialization.

    @staticmethod
    def init(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, (Z, int))
        if isinstance(b, Z):
            a._ = b._
        if isinstance(b, int):
            a._ = b

    @staticmethod
    def coerce(Z, a):
        assert isinstance(a, (Z, int))
        if isinstance(a, Z):
            return a
        return Z(a)

    # Arithmetic.

    @staticmethod
    def pos(Z, a):
        assert isinstance(a, Z)
        return Z(+a._)

    @staticmethod
    def neg(Z, a):
        assert isinstance(a, Z)
        return Z(-a._)

    @staticmethod
    def add(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return Z(a._ + b._)

    @staticmethod
    def sub(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return Z(a._ - b._)

    @staticmethod
    def mul(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return Z(a._ * b._)

    @staticmethod
    def divmod(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        if not b:
            raise ZeroDivisionError
        return Z(a._ // b._), Z(a._ % b._)

    @staticmethod
    def div(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return divmod(a, b)[0]

    @staticmethod
    def mod(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return divmod(a, b)[1]

    # Comparisons.

    @staticmethod
    def eq(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return a._ == b._

    @staticmethod
    def ne(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        return a._ != b._

    @staticmethod
    def nonzero(Z, a):
        assert isinstance(a, Z)
        return True if a._ else False

    # String representation.

    @staticmethod
    def str(Z, a):
        assert isinstance(a, Z)
        return "%s" % (str(a._), )

    @staticmethod
    def repr(Z, a):
        assert isinstance(a, Z)
        return "%s(%s)" % (Z.__name__, repr(a._), )

    # Other instance methods.

    @staticmethod
    def is_unit(Z, a):
        assert isinstance(a, Z)
        return a == 1 or a == -1

    # Other class methods.

    @staticmethod
    def gcd(Z, a, b):
        assert isinstance(a, Z)
        assert isinstance(b, Z)
        if not a and not b:
            raise ValueError
        def gcd_aux(a, b):
            if not b:
                return Z(a), Z(1), Z(0)
            q, r = divmod(a, b)
            d, k, l = gcd_aux(b, r)
            return d, l, k - q*l
        return gcd_aux(a, b)

    # Meta.

    def __new__(meta):
        return type.__new__(
            meta,
            'IntegerRing',
            (object,),
            {}
        )

    def __init__(cls):
        c = cls
        m = IntegerRingMeta
        _ = lambda _: m.coerce(c, _)
        # Initialization.
        c.__init__ = lambda a, b: m.init(c, a, b)
        # Arithmetic.
        c.__pos__ = lambda a: m.pos(c, _(a))
        c.__neg__ = lambda a: m.neg(c, _(a))
        c.__add__ = lambda a, b: m.add(c, _(a), _(b))
        c.__radd__ = lambda a, b: m.add(c, _(b), _(a))
        c.__sub__ = lambda a, b: m.sub(c, _(a), _(b))
        c.__rsub__ = lambda a, b: m.sub(c, _(b), _(a))
        c.__mul__ = lambda a, b: m.mul(c, _(a), _(b))
        c.__rmul__ = lambda a, b: m.mul(c, _(b), _(a))
        c.__divmod__ = lambda a, b: m.divmod(c, _(a), _(b))
        c.__rdivmod__ = lambda a, b: m.divmod(c, _(b), _(a))
        c.__div__ = lambda a, b: m.div(c, _(a), _(b))
        c.__rdiv__ = lambda a, b: m.div(c, _(b), _(a))
        c.__mod__ = lambda a, b: m.mod(c, _(a), _(b))
        c.__rmod__ = lambda a, b: m.mod(c, _(b), _(a))
        # Comparisons.
        c.__eq__ = lambda a, b: m.eq (c, _(a), _(b))
        c.__req__ = lambda a, b: m.eq (c, _(b),  _(a))
        c.__ne__ = lambda a, b: m.ne(c, _(a), _(b))
        c.__rne__ = lambda a, b: m.ne(c, _(b), _(a))
        c.__nonzero__ = lambda a: m.nonzero(c, _(a))
        # String representation.
        c.__str__ = lambda a: m.str(c, _(a))
        c.__repr__ = lambda a: m.repr(c, _(a))
        # Other instance methods.
        c.is_unit = lambda a: m.is_unit(c, _(a))
        # Other class methods.
        c.gcd = classmethod(lambda c, a, b: m.gcd(c, _(a), _(b)))

IntegerRing = IntegerRingMeta()
