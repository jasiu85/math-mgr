class LineMeta(type):

    # Initialization.

    @staticmethod
    def init(L, a, b):
        assert isinstance(a, L)
        assert isinstance(b, (L, dict))
        if isinstance(b, L):
            a._ = {
                'a': b._['a'],
                'b': b._['b'],
                'c': b._['c'],
            }
        if isinstance(b, dict):
            a._ = {
                'a': b['a'],
                'b': b['b'],
                'c': b['c'],
            }

    # Meta initialization.

    def __new__(meta):
        return type.__new__(
            meta,
            'Line',
            (object,),
            {}
        )

    def __init__(cls):
        c = cls
        m = LineMeta
        # Initialization.
        c.__init__ = lambda a, b: m.init(c, a, b)

Line = LineMeta()
