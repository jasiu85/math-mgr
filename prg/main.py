from fields.integer_ring import IntegerRing
from fields.quotient_field import QuotientField
from fields.polynomial_ring import PolynomialRing
from fields.finite_field import FiniteField
from elliptic_curve import EllipticCurve
from miller import *


def ec_point_coords(E, P):
    if P == identity(E):
        return (-1, -1)
    return (x(P)._._, y(P)._._)


def example(E, n):
    L = [P for P in E.all_elements() if MultiplyCurvePoint(E, P, n) == identity(E)]
    L.sort(key=lambda P: ec_point_coords(E, P))
    l = len(L)
    M = [['']*(l+1) for _ in xrange(l+1)]
    for i, P in enumerate(L):
        if P != identity(E):
            M[0][i+1] = M[i+1][0] = '(%s, %s)' % (str(x(P)), str(y(P)))
        else:
            M[0][i+1] = M[i+1][0] = 'identity'
        for j, Q in enumerate(L):
            w = WeilPairing(E, n, P, Q)
            M[i+1][j+1] = str(w)
    W = [0]*(l+1)
    for i in xrange(l+1):
        for j in xrange(l+1):
            W[j] = max(W[j], len(M[i][j]))
    for i in xrange(l+1):
        for j in xrange(l+1):
            p = W[j] - len(M[i][j])
            print ' '*((p+1) // 2) + M[i][j] + ' '*(p // 2),
        print
    print


example(EllipticCurve(FiniteField(13), 0, 5), 4)
example(EllipticCurve(FiniteField(13), 7, 0), 6)
example(EllipticCurve(FiniteField(17), 16, 0), 2)
example(EllipticCurve(FiniteField(19), 0, 16), 9)
example(EllipticCurve(FiniteField(19), 3, 12), 6)
