import sympy as sp
# Verify the regular solution of -Psi'' + 6/r^2 Psi = w^2 Psi is Psi = r*j_2(w r).
r, w = sp.symbols('r omega', positive=True)
Psi = r*sp.jn(2, w*r)   # spherical Bessel j_2
lhs = -sp.diff(Psi, r, 2) + 6/r**2*Psi
res = sp.simplify(lhs - w**2*Psi)
print("residual of -Psi''+6/r^2 Psi - w^2 Psi with Psi=r j_2(wr):", res)

# Behaviour at core: j_2(x) ~ x^2/15 => Psi ~ r * (wr)^2/15 ~ r^3 = r^{l+1} with l=2. Good.
ser = sp.series(Psi, r, 0, 5).removeO()
print("Psi small-r series:", ser)
