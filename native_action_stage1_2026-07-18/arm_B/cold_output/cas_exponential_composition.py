from sympy import Matrix, simplify, symbols
from sympy.functions import exp

a, b, k = symbols("a b k", real=True)


def P(delta):
    return Matrix([[exp(-k * delta), 0], [0, exp(k * delta)]])


print("P(a+b) - P(a)P(b) =")
print(simplify(P(a + b) - P(a) * P(b)))
print()
print("P(-a) - P(a)^(-1) =")
print(simplify(P(-a) - P(a).inv()))
print()
print("det(P(a)) =")
print(simplify(P(a).det()))
