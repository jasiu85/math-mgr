class PolynomialRingMeta(type):

    # Initialization.

    @staticmethod
    def init(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, (R, R.base_field(), list, int))
        if isinstance(b, R):
            a._ = [_ for _ in b._]
        if isinstance(b, R.base_field()):
            a._ = [b]
        if isinstance(b, list):
            a._ = [R.base_field()(_) for _ in b]
        if isinstance(b, int):
            a._ = [R.base_field()(b)]
        while a._ and not a._[-1]:
            a._.pop()

    @staticmethod
    def coerce(R, a):
        assert isinstance(a, (R, R.base_field(), list, int))
        if isinstance(a, R):
            return a
        return R(a)

    # Arithmetic.

    @staticmethod
    def pos(R, a):
        assert isinstance(a, R)
        return R([+a._[k] for k in xrange(a.deg()+1)])

    @staticmethod
    def neg(R, a):
        assert isinstance(a, R)
        return R([-a._[k] for k in xrange(a.deg()+1)])

    @staticmethod
    def add(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        c_deg = max(a.deg(), b.deg())
        c = [None]*(c_deg+1)
        for k in xrange(c_deg+1):
            c[k] = (
                (a._[k] if k <= a.deg() else R.base_field()(0))
                +
                (b._[k] if k <= b.deg() else R.base_field()(0))
            )
        return R(c)

    @staticmethod
    def sub(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        c_deg = max(a.deg(), b.deg())
        c = [None]*(c_deg+1)
        for k in xrange(c_deg+1):
            c[k] = (
                (a._[k] if k <= a.deg() else R.base_field()(0))
                -
                (b._[k] if k <= b.deg() else R.base_field()(0))
            )
        return R(c)

    @staticmethod
    def mul(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        if not a or not b:
            return R(0)
        c_deg = a.deg() + b.deg()
        c = [R.base_field()(0)]*(c_deg+1)
        for k in xrange(a.deg()+1):
            for l in xrange(b.deg()+1):
                c[k+l] = c[k+l] + a._[k]*b._[l]
        return R(c)

    @staticmethod
    def divmod(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        if not b:
            raise ZeroDivisionError
        def divmod_aux(a, b):
            if a.deg() < b.deg():
                return [], a._
            c = a._[-1] / b._[-1]
            q, r = divmod_aux(
                (
                    a
                    -
                    R(
                        [R.base_field()(0)]*(a.deg() - b.deg())
                        +
                        [c*b._[k] for k in xrange(b.deg()+1)]
                    )
                ),
                b
            )
            q.append(c)
            return q, r
        q, r = divmod_aux(a, b)
        return R(q), R(r)

    @staticmethod
    def div(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        return divmod(a, b)[0]

    @staticmethod
    def mod(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        return divmod(a, b)[1]

    # Comparisons.

    @staticmethod
    def eq(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        return a._ == b._

    @staticmethod
    def ne(R, a, b):
        assert isinstance(a, R)
        assert isinstance(b, R)
        return a._ != b._

    @staticmethod
    def nonzero(R, a):
        assert isinstance(a, R)
        return True if a._ else False

    # String representation.

    @staticmethod
    def str(R, a):
        assert isinstance(a, R)
        return "%s" % (
            " + ".join(
                "(%s)x^%s" % (str(_), str(k), )
                for k, _ in enumerate(a._)
            ),
        )

    @staticmethod
    def repr(R, a):
        assert isinstance(a, R)
        return "%s(%s)" % (R.__name__, repr(a._), )

    # Other instance methods.

    def deg(R, a):
        assert isinstance(a, R)
        return len(a._) - 1

    def is_unit(R, a):
        assert isinstance(a, R)
        return a.deg() == 0

    # Other class methods.

    @staticmethod
    def gcd(R, a, b):
        assert isinstance(a, R), "a is %s" % str(type(a))
        assert isinstance(b, R)
        if not a and not b:
            raise ValueError
        def gcd_aux(a, b):
            if not b:
                return R(a), R(1), R(0)
            q, r = divmod(a, b)
            d, k, l = gcd_aux(b, r)
            return d, l, k - q*l
        return gcd_aux(a, b)

    # Meta.

    def __new__(meta, base_field):
        return type.__new__(
            meta,
            'PolynomialRing(%s)' % (base_field.__name__),
            (object,),
            {}
        )

    def __init__(cls, base_field):
        c = cls
        m = PolynomialRingMeta
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
        # Other instance methods.
        c.is_unit = lambda a: m.is_unit(c, _(a))
        c.deg = lambda a: m.deg(c, _(a))
        # Other class methods.
        c.gcd = classmethod(lambda c, a, b: m.gcd(c, _(a), _(b)))
        c.base_field = classmethod(lambda c: base_field)

def PolynomialRing(base_field):
    return PolynomialRingMeta(base_field)
