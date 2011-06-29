#!/usr/bin/env sage -python
# -*- encoding: UTF-8 -*-



from random import randrange

from sage.all import *



ERROR = None



########################################
# Accessors                            #
########################################


# Fields

def zero(K):
    return K(0)

def one(K):
    return K(1)

def two(K):
    return K(2)

def three(K):
    return K(3)


# Curves

def A(E):
    return E.a4()

def B(E):
    return E.a6()

def identity(E):
    K = field(E)
    return E.point((zero(K), one(K), zero(K)))

def field(E):
    return E.base_field()


# Curve points

def x(P):
    assert P != identity(P.curve())

    return P.xy()[0]

def y(P):
    assert P != identity(P.curve())

    return P.xy()[1]


# Lines on curves

def a(l):
    x, _ = l.base_ring()['x', 'y'].gens()
    return l.coefficient(x)

def b(l):
    _, y = l.base_ring()['x', 'y'].gens()
    return l.coefficient(y)

def c(l):
    return l.constant_coefficient()



########################################
# Predefined procedures                #
########################################


# Integers

def RandomInteger(n):
    assert type(n) == int

    return randrange(n)


# Finite fields

def RandomFiniteFieldElement(K):
    return K.random_element()

def FiniteFieldElementSquareRoot(K, a):
    assert a.base_ring() == K

    if a.is_square():
        return a.sqrt()
    else:
        return ERROR


# Curve points

def CurveFinitePoint(E, a, b):
    assert a.base_ring() == field(E)
    assert b.base_ring() == field(E)

    return E.point((a, b))

def CurvePointConjugate(E, P):
    assert P.curve() == E

    return -P


# Lines on curves

def LineOnCurve(E, a, b, c):
    assert a.base_ring() == field(E)
    assert b.base_ring() == field(E)
    assert c.base_ring() == field(E)

    K = field(E)
    x, y = K['x', 'y'].gens()
    return a*x + b*y + c



########################################
# General procedures                   #
########################################


# Line evaluation

def LineValueAtCurveFinitePoint(E, l, P):
    assert P.curve() == E
    assert l.base_ring() == field(E)

    assert P != identity(E)
    return a(l)*x(P) + b(l)*y(P) + c(l)


# Line creation

def VerticalLineThroughCurvePoint(E, P):
    assert P.curve() == E

    K = field(E)
    if P == identity(E):
        return LineOnCurve(E, zero(K), zero(K), one(K))
    else:
        a = x(P)
        return LineOnCurve(E, one(K), zero(K), -a)

def LineThroughDifferentCurveFinitePoints(E, P, Q):
    assert P.curve() == E
    assert Q.curve() == E

    assert P != identity(E) and Q != identity(E)
    assert P != Q
    K = field(E)
    a = x(P)
    b = y(P)
    c = x(Q)
    d = y(Q)
    if a == c:
        return LineOnCurve(E, one(K), zero(K), -a)
    else:
        lambda_ = (d - b)/(c - a)
        return LineOnCurve(E, lambda_, -one(K), -(lambda_*a - b))

def TangentLineThroughCurveFinitePoint(E, P):
    assert P.curve() == E

    assert P != identity(E)
    K = field(E)
    a = x(P)
    b = y(P)
    if b == zero(K):
        return LineOnCurve(E, one(K), zero(K), -a)
    else:
        lambda_ = (three(K)*a*a + A(E))/(two(K)*b)
        return LineOnCurve(E, lambda_, -one(K), -(lambda_*a - b))

def LineThroughCurvePoints(E, P, Q):
    assert P.curve() == E
    assert Q.curve() == E

    K = field(E)
    if P == identity(E) and Q == identity(E):
        return LineOnCurve(E, zero(K), zero(K), one(K))
    if P == identity(E):
        return VerticalLineThroughCurvePoint(E, Q)
    if Q == identity(E):
        return VerticalLineThroughCurvePoint(E, P)
    if P != Q:
        return LineThroughDifferentCurveFinitePoints(E, P, Q)
    else:
        return TangentLineThroughCurveFinitePoint(E, P)


# Curve point arithmetic

def AddCurvePoints(E, P, Q):
    assert P.curve() == E
    assert Q.curve() == E

    K = field(E)
    if P == identity(E):
        return Q
    if Q == identity(E):
        return P
    if P == CurvePointConjugate(E, Q):
        return identity(E)
    a = x(P)
    b = y(P)
    c = x(Q)
    d = y(Q)
    if P != Q:
        lambda_ = (d - b)/(c - a)
    else:
        lambda_ = (three(K)*a*a + A(E))/(two(K)*b)
    e = lambda_*lambda_ - a - c
    f = -lambda_*(e - a) - b
    return CurveFinitePoint(E, e, f)

def MultiplyCurvePoint(E, P, n):
    assert P.curve() == E
    assert type(n) == int

    K = field(E)
    if P == identity(E):
        return identity(E)
    if y(P) == zero(K):
        if n % 2 == 0:
            return identity(E)
        else:
            return P
    if n == 0:
        return identity(E)
    if n > 0:
        m = n
    else:
        m = -n
    R = identity(E)
    while m > 0:
        if m % 2 != 0:
            R = AddCurvePoints(E, R, P)
        P = AddCurvePoints(E, P, P)
        m = m // 2
    if n > 0:
        return R
    else:
        return CurvePointConjugate(E, R)


# Random curve point

def RandomCurveFinitePoint(E):
    K = field(E)
    c = cardinality(K)
    while True:
        a = RandomFiniteFieldElement(K)
        d = a*a*a + A(E)*a + B(E)
        if d == zero(K):
            if RandomInteger(2) == 0:
                return CurveFinitePoint(E, a, zero(K))
        else:
            b = FiniteFieldElementSquareRoot(K, d)
            if b != ERROR:
                if RandomInteger(2) == 0:
                    return CurveFinitePoint(E, a, b)
                else:
                    return CurveFinitePoint(E, a, -b)



########################################
# Miller algorithm                     #
########################################

def CombinePartialValues(E, A, U, V, u, v):
    assert A.curve() == E
    assert U.curve() == E
    assert V.curve() == E
    assert u.base_ring() == field(E)
    assert v.base_ring() == field(E)

    K = field(E)
    g = LineThroughCurvePoints(E, U, V)
    h = VerticalLineThroughCurvePoint(E, AddCurvePoints(E, U, V))
    s = LineValueAtCurveFinitePoint(E, g, A)
    t = LineValueAtCurveFinitePoint(E, h, A)
    if s == zero(K) or t == zero(K):
        return ERROR
    return u*v*(s/t)

def ComputeValue(E, n, P, R, A):
    assert type(n) == int
    assert P.curve() == E
    assert R.curve() == E
    assert A.curve() == E

    K = field(E)
    g = LineThroughCurvePoints(E, P, R)
    h = VerticalLineThroughCurvePoint(E, AddCurvePoints(E, P, R))
    s = LineValueAtCurveFinitePoint(E, g, A)
    t = LineValueAtCurveFinitePoint(E, h, A)
    if t == zero(K) or s == zero(K):
        return ERROR
    U = identity(E)
    V = P
    u = one(K)
    v = t/s
    while n > 0:
        if v == ERROR:
            return ERROR
        if n % 2 != 0:
            u = CombinePartialValues(E, A, U, V, u, v)
            U = AddCurvePoints(E, U, V)
            if u == ERROR:
                return ERROR
        v = CombinePartialValues(E, A, V, V, v, v)
        V = AddCurvePoints(E, V, V)
        n = n // 2
    return u

def WeilPairing(E, n, P, Q):
    assert type(n) == int
    assert P.curve() == E
    assert Q.curve() == E

    assert MultiplyCurvePoint(E, P, n) == identity(E)
    assert MultiplyCurvePoint(E, Q, n) == identity(E)
    K = field(E)
    if P == Q or P == identity(E) or Q == identity(E):
        return one(K)
    while True:
        R = RandomCurveFinitePoint(E)
        S = RandomCurveFinitePoint(E)
        R_ = AddCurvePoints(E, P, R)
        S_ = AddCurvePoints(E, Q, S)
        if R_ != identity(E) and S_ != identity(E):
            a = ComputeValue(E, n, P, R, S_)
            b = ComputeValue(E, n, P, R, S)
            c = ComputeValue(E, n, Q, S, R_)
            d = ComputeValue(E, n, Q, S, R)
            if a != ERROR and b != ERROR and c != ERROR and d != ERROR:
                return (a/b)*(d/c)



########################################
# Example usage                        #
########################################


def example(q, A, B, n):
    K = FiniteField(q, 't')
    E = EllipticCurve(K, [K(A), K(B)])
    for P in E:
        print P, n*P, MultiplyCurvePoint(E, P, n)

    L = [P for P in E if MultiplyCurvePoint(E, P, n) == identity(E)]
    l = len(L)
    M = [['']*(l+1) for _ in xrange(l+1)]
    for i, P in enumerate(L):
        if P != identity(E):
            M[0][i+1] = M[i+1][0] = '(%s, %s)' % (str(x(P)), str(y(P)))
        else:
            M[0][i+1] = M[i+1][0] = 'identity'
        for j, Q in enumerate(L):
            w = WeilPairing(E, n, P, Q)
            print type(w)
            assert w == P.weil_pairing(Q, Integer(n))
            M[i+1][j+1] = str(w)
        print '%5.1f%%' % (((i+1) * 100.) / l)
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

def example_finder():
    K = FiniteField(13, 't')
    for A in K:
        for B in K:
            print A, B
            try:
                E = EllipticCurve(K, [A, B])
                for P in E:
                    for Q in E:
                            n = lcm(P.order(), Q.order())
                            w = P.weil_pairing(Q, n)
                            if w != K(1) and w != K(-1):
                                print P, Q, n, w
            except ArithmeticError, e:
                print e

#example(13, 0, 3, 3)
example(13, 0, 5, 4)
#example(13, 7, 0, 6)
#example(19, 0, 16, 9)
#example(19, 3, 12, 6)
#example_finder()
