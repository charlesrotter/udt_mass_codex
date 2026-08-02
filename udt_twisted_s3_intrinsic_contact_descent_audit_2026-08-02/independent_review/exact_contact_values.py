import sympy as s

points = [
    (s.Rational(1, 5), s.Rational(1, 7), s.Rational(1, 11)),
    (s.Rational(1, 3), -s.Rational(1, 5), s.Rational(1, 7)),
    (-s.Rational(2, 5), s.Rational(1, 4), s.Rational(1, 6)),
]
for point in points:
    x, y, z = point
    d = 1 + x*x + y*y + z*z
    q = ((1-x*x-y*y-z*z)/d, 2*x/d, 2*y/d, 2*z/d)
    u = s.factor(3 + q[0]**2 + 2*q[1]**2 + 4*q[2]**2 + 8*q[3]**2)
    print("point", point, "u", u, "decimal", s.N(u, 17))
    for lam in (-1, 0, 1):
        qt = s.factor(4*u**(-1-2*lam))
        qs = s.factor(4*u**(1-2*lam))
        print(lam, "QT", qt, "QS", qs, "Q", s.factor(qs-qt))
