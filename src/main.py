from fields.integer_ring import IntegerRing
from fields.quotient_field import QuotientField
from fields.polynomial_ring import PolynomialRing
from fields.finite_field import FiniteField
from elliptic_curve import EllipticCurve
from miller import *


def example(K, A, B, n):
    E = EllipticCurve(K, A, B)
    L = [P for P in E.all_elements() if MultiplyCurvePoint(E, P, n) == identity(E)]
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
        print '%5.1f%%' % (((i+1) * 100.) / l)
    W = [0]*(l+1)
    for i in xrange(l+1):
        for j in xrange(l+1):
            W[j] = max(W[j], len(M[i][j]))
    for i in xrange(l+1):
        for j in xrange(l+1):
            p = W[j] - len(M[i][j])
            print ';' + ' '*((p+1) // 2) + M[i][j] + ' '*(p // 2),
        print
    print

def example_finder():
    for q in xrange(200):
        if q % 2 == 0 or q % 3 == 0:
            continue
        try:
            K = FiniteField(q, 't')
        except ValueError:
            continue
        print "trying field", K
        for A in K:
            for B in K:
                try:
                    E = EllipticCurve(K, [A, B])
                except ArithmeticError:
                    continue
                print "trying curve", E
                for P in E:
                    for Q in E:
                        n = lcm(P.order(), Q.order())
                        w = P.weil_pairing(Q, n)
                        if w.multiplicative_order() > 2:
                            print "found", P, Q, n, w.multiplicative_order(), w

F13 = FiniteField(13)
#example(13, 0, 3, 3)
example(F13, 0, 5, 4)
#example(13, 7, 0, 6)
#example(19, 0, 16, 9)
#example(19, 3, 12, 6)
#example_finder()
