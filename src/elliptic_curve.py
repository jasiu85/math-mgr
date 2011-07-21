class EllipticCurveMeta(type):

    # Initialization.

    @staticmethod
    def init(E, a, b):
        assert isinstance(a, E)
        assert isinstance(b, (E, dict))
        if isinstance(b, E):
            a._ = {
                'x': b._['x'],
                'y': b._['y'],
            }
        if isinstance(b, dict):
            a._ = {
                'x': b.get('x'),
                'y': b.get('y'),
            }

    @staticmethod
    def coerce(E, a):
        assert isinstance(a, (E, dict)), "a is %s" % str(type(a))
        if isinstance(a, E):
            return a
        return E(a)

    # Arithmetic.

    @staticmethod
    def pos(E, a):
        assert isinstance(a, E)
        if a._['x'] is None and a._['y'] is None:
            return E({})
        return E({'x':+a._['x'], 'y':+a._['y']})

    @staticmethod
    def neg(E, a):
        assert isinstance(a, F)
        if a._['x'] is None and a._['y'] is None:
            return E({})
        return E({'x':+a._['x'], 'y':-a._['y']})

    # Comparisons.

    @staticmethod
    def eq(E, a, b):
        assert isinstance(a, E)
        assert isinstance(b, E)
        if a._['x'] is None and a._['y'] is None:
            return b._['x'] is None and b._['y'] is None
        if b._['x'] is None and b._['y'] is None:
            return a._['x'] is None and a._['y'] is None
        return a._ == b._

    @staticmethod
    def ne(E, a, b):
        assert isinstance(a, E)
        assert isinstance(b, E)
        if a._['x'] is None and a._['y'] is None:
            return not(b._['x'] is None and b._['y'] is None)
        if b._['x'] is None and b._['y'] is None:
            return not(a._['x'] is None and a._['y'] is None)
        return a._ != b._

    @staticmethod
    def nonzero(E, a):
        assert isinstance(a, E)
        return True if a._['x'] is not None and a._['y'] is not None else False

    # String representation.

    @staticmethod
    def str(E, a):
        assert isinstance(a, E)
        return "(%s,%s)" % (str(a._['x']), str(a._['y']), )

    @staticmethod
    def repr(E, a):
        assert isinstance(a, E)
        return "%s({'x':%s,'y':%s})" % (F.__name__, repr(a._['x']), repr(a._['y']), )

    # Other class methods.

    @staticmethod
    def all_elements(E):
        yield E({})
        F = E.base_field()
        for a in F.all_elements():
            b = F.sqrt(a*a*a + E.A()*a + E.B())
            if b is not None:
                yield E({'x':a, 'y':b})
                if b:
                    yield E({'x':a, 'y':-b})

    # Meta.

    def __new__(meta, base_field, A, B):
        return type.__new__(
            meta,
            'EllipticCurve(%s,%s,%s)' % (base_field.__name__, repr(A), repr(B)),
            (object,),
            {}
        )

    def __init__(cls, base_field, A, B):
        c = cls
        m = EllipticCurveMeta
        _ = lambda _: m.coerce(c, _)
        # Initialization.
        c.__init__ = lambda a, b: m.init(c, a, b)
        # Arithmetic.
        c.__pos__ = lambda a: m.pos(c, _(a))
        c.__neg__ = lambda a: m.neg(c, _(a))
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
        c.all_elements = classmethod(lambda c: m.all_elements(c))
        c.base_field = classmethod(lambda c: base_field)
        c.A = classmethod(lambda c: A)
        c.B = classmethod(lambda c: B)

def EllipticCurve(base_field, A, B):
    return EllipticCurveMeta(base_field, A, B)
