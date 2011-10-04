#!/usr/bin/python
# -*- encoding: UTF-8 -*-



import random

from fields.integer_ring import IntegerRing
from line import Line



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

def cardinality(K):
    return K.cardinality()


# Curves

def A(E):
    return E.A()

def B(E):
    return E.B()

def identity(E):
    return E({})

def field(E):
    return E.base_field()


# Curve points

def x(P):
    return P._['x']

def y(P):
    return P._['y']


# Lines on curves

def a(l):
    return l._['a']

def b(l):
    return l._['b']

def c(l):
    return l._['c']



########################################
# Predefined procedures                #
########################################


# Integers

def RandomInteger(n):
    return IntegerRing(random.randrange(n))


# Finite fields

def RandomFiniteFieldElement(K):
    return K.random_element()

def FiniteFieldElementSquareRoot(K, a):
    return K.sqrt(a)


# Curve points

def CurveFinitePoint(E, a, b):
    return E({'x':a, 'y':b})

def CurvePointConjugate(E, P):
    if P._['x'] is None and P._['y'] is None:
        return E({})
    else:
        return E({'x': x(P), 'y': -y(P)})


# Lines on curves

def LineOnCurve(E, a, b, c):
    return Line({'a':a, 'b':b, 'c':c})



########################################
# General procedures                   #
########################################


# Line evaluation

def LineValueAtCurveFinitePoint(E, l, P):
    assert P != identity(E)
    return a(l)*x(P) + b(l)*y(P) + c(l)


# Line creation

def VerticalLineThroughCurvePoint(E, P):
    K = field(E)
    if P == identity(E):
        return LineOnCurve(E, zero(K), zero(K), one(K))
    else:
        a = x(P)
        return LineOnCurve(E, one(K), zero(K), -a)

def LineThroughDifferentCurveFinitePoints(E, P, Q):
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
    R = identity(E)
    while n != 0:
        if n % 2 != 0:
            R = AddCurvePoints(E, R, P)
        P = AddCurvePoints(E, P, P)
        n = n // 2
    return R


# Random curve point

def RandomCurveFinitePoint(E):
    K = field(E)
    while True:
        a = RandomFiniteFieldElement(K)
        d = a*a*a + A(E)*a + B(E)
        if d == zero(K):
            if RandomInteger(2) == 0:
                return CurveFinitePoint(E, a, zero(K))
        else:
            b = FiniteFieldElementSquareRoot(K, d)
            if b is not ERROR:
                if RandomInteger(2) == 0:
                    return CurveFinitePoint(E, a, b)
                else:
                    return CurveFinitePoint(E, a, -b)



########################################
# Miller algorithm                     #
########################################

def CombinePartialValues(E, A, U, V, u, v):
    K = field(E)
    g = LineThroughCurvePoints(E, U, V)
    h = VerticalLineThroughCurvePoint(E, AddCurvePoints(E, U, V))
    s = LineValueAtCurveFinitePoint(E, g, A)
    t = LineValueAtCurveFinitePoint(E, h, A)
    if s == zero(K) or t == zero(K):
        return ERROR
    return u*v*(s/t)

def ComputeValue(E, n, P, R, A):
    K = field(E)
    g = LineThroughCurvePoints(E, P, R)
    h = VerticalLineThroughCurvePoint(E, AddCurvePoints(E, P, R))
    s = LineValueAtCurveFinitePoint(E, g, A)
    t = LineValueAtCurveFinitePoint(E, h, A)
    if s == zero(K) or t == zero(K):
        return ERROR
    U = identity(E)
    V = P
    u = one(K)
    v = t/s
    while n != 0:
        if v is ERROR:
            return ERROR
        if n % 2 != 0:
            u = CombinePartialValues(E, A, U, V, u, v)
            U = AddCurvePoints(E, U, V)
            if u is ERROR:
                return ERROR
        v = CombinePartialValues(E, A, V, V, v, v)
        V = AddCurvePoints(E, V, V)
        n = n // 2
    return u

def WeilPairing(E, n, P, Q):
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
            if a is not ERROR and b is not ERROR and c is not ERROR and d is not ERROR:
                return (a/b)*(d/c)
