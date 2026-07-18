from sympy import Matrix, Rational, simplify, sqrt, symbols
from sympy.functions import exp, log

u = symbols("u", positive=True)
v = symbols("v", positive=True)
phi = Rational(1, 2) * log(v / u)

lhs = Matrix([[u, 0], [0, v]])
rhs = sqrt(u * v) * Matrix([[exp(-phi), 0], [0, exp(phi)]])
reciprocal = Matrix([[exp(-phi), 0], [0, exp(phi)]])

print("diag(u,v) - sqrt(uv) * diag(exp(-phi), exp(phi)) =")
print(simplify(lhs - rhs))
print()
print("determinant of reciprocal factor =")
print(simplify(reciprocal.det()))
