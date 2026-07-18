from sympy import Matrix, factor, symbols

u, v = symbols("u v", nonzero=True)
P = Matrix([[u, 0], [0, v]])
K = Matrix([[0, 1], [1, 0]])
expr = P.T * K * P - K

print("P^T K P - K =")
print(expr)
print()
print("Off-diagonal factor:")
print(factor(expr[0, 1]))
print()
print("Substitute uv=1:")
print(expr.subs(u * v, 1))
