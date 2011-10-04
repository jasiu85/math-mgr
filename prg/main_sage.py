#!/usr/bin/env sage -python
# -*- encoding: UTF-8 -*-


from sage.all import *


def ec_point_coords(E, P):
    if P == E.abelian_group().identity():
        return (-1, -1)
    xy = P.xy()
    return (int(xy[0]), int(xy[1]))


def example(q, A, B, n):
    K = FiniteField(q, 't')
    E = EllipticCurve(K, [K(A), K(B)])
    L = [P for P in E if n*P == E.abelian_group().identity()]
    L.sort(key=lambda P: ec_point_coords(E, P))
    l = len(L)
    M = [['']*(l+1) for _ in xrange(l+1)]
    for i, P in enumerate(L):
        if P != E.abelian_group().identity():
            M[0][i+1] = M[i+1][0] = '(%s, %s)' % (P.xy())
        else:
            M[0][i+1] = M[i+1][0] = 'identity'
        for j, Q in enumerate(L):
            w = P.weil_pairing(Q, Integer(n))
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

#example(13, 0, 3, 3)
example(13, 0, 5, 4)
#example(13, 7, 0, 6)
#example(19, 0, 16, 9)
#example(19, 3, 12, 6)
#example_finder()
