class QuotientFieldMeta(type):

    # Initialization.

    @staticmethod
    def init(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, (F, F.base_ring(), int, )), "b is %s" % str(type(b))
        if isinstance(b, F):
            a._ = b._
        if isinstance(b, F.base_ring()):
            a._ = b % F.modulus()
        if isinstance(b, int):
            a._ = F.base_ring()(b) % F.modulus()

    @staticmethod
    def coerce(F, a):
        assert isinstance(a, (F, F.base_ring(), int)), "a is %s" % str(type(a))
        if isinstance(a, F):
            return a
        return F(a)

    # Arithmetic.

    @staticmethod
    def pos(F, a):
        assert isinstance(a, F)
        return F(+a._)

    @staticmethod
    def neg(F, a):
        assert isinstance(a, F)
        return F(-a._)

    @staticmethod
    def add(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return F(a._ + b._)

    @staticmethod
    def sub(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return F(a._ - b._)

    @staticmethod
    def mul(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return F(a._ * b._)

    @staticmethod
    def divmod(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        if not b:
            raise ZeroDivisionError
        d, k, l = F.base_ring().gcd(b._, F.modulus())
        if not d.is_unit():
            raise ValueError, "reducible modulus"
        return F(a._ * (k / d)), F(0)

    @staticmethod
    def div(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return divmod(a, b)[0]

    @staticmethod
    def mod(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return divmod(a, b)[1]

    # Comparisons.

    @staticmethod
    def eq(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return a._ == b._

    @staticmethod
    def ne(F, a, b):
        assert isinstance(a, F)
        assert isinstance(b, F)
        return a._ != b._

    @staticmethod
    def nonzero(F, a):
        assert isinstance(a, F)
        return True if a._ else False

    # String representation.

    @staticmethod
    def str(F, a):
        assert isinstance(a, F)
        return "%s" % (str(a._), )

    @staticmethod
    def repr(F, a):
        assert isinstance(a, F)
        return "%s(%s)" % (F.__name__, repr(a._), )

    # Other class methods.

    @staticmethod
    def gcd(F, a, b):
        assert isinstance(a, F), "a is %s" % str(type(a))
        assert isinstance(b, F)
        if not a and not b:
            raise ValueError
        return F(1), F(1)/(a+a), F(1)/(b+b)

    # Meta.

    def __new__(meta, base_ring, modulus):
        return type.__new__(
            meta,
            'QuotientField(%s,%s)' % (base_ring.__name__, repr(modulus), ),
            (object,),
            {},
        )

    def __init__(cls, base_ring, modulus):
        c = cls
        m = QuotientFieldMeta
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
        c.__eq__ = lambda a, b: m.eq(c, _(a), _(b))
        c.__req__ = lambda a, b: m.eq(c, _(b), _(a))
        c.__ne__ = lambda a, b: m.ne(c, _(a), _(b))
        c.__rne__ = lambda a, b: m.ne(c, _(b), _(a))
        c.__nonzero__ = lambda a: m.nonzero(c, _(a))
        # String representation.
        c.__str__ = lambda a: m.str(c, _(a))
        c.__repr__ = lambda a: m.repr(c, _(a))
        # Other class methods.
        c.gcd = classmethod(lambda c, a, b: m.gcd(c, _(a), _(b)))
        c.base_ring = classmethod(lambda c: base_ring)
        c.modulus = classmethod(lambda c: modulus)

def QuotientField(base_ring, modulus):
    return QuotientFieldMeta(base_ring, modulus)
