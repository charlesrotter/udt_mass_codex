import sympy as sp
h,nu,k,T,c,A,B12,B21,g1,g2 = sp.symbols('h nu k T c A B12 B21 g1 g2', positive=True)

# Two quantized MATTER levels, spacing h*nu = E2-E1 (UDT: Dirac Form-T levels).
# Thermal matter populations (Boltzmann):  N1/N2 = (g1/g2) exp(h nu/(k T))
N1_over_N2 = (g1/g2)*sp.exp(h*nu/(k*T))

# Rate balance (detailed balance) with a CLASSICAL radiation field of energy density u:
#   absorption  N1 B12 u   =   spontaneous N2 A  +  stimulated N2 B21 u
u = sp.symbols('u', positive=True)
bal = sp.Eq(N1_over_N2*B12*u, A + B21*u)        # divided through by N2
u_sol = sp.solve(bal, u)[0]
print("u(nu) raw            =", sp.simplify(u_sol))

# Consistency at the classical (high-T / Rayleigh-Jeans) limit forces  g1 B12 = g2 B21.
u1 = sp.simplify(u_sol.subs(B12, g2*B21/g1))
print("after g1 B12=g2 B21  =", u1)            # = (A/B21)/(e^{hnu/kT}-1)

# Match the classical EM mode density (Rayleigh-Jeans limit) -> A/B21 = 8 pi h nu^3 / c^3
u_planck = u1.subs(A, sp.Rational(8)*sp.pi*h*nu**3/c**3 * B21)
print("PLANCK u(nu)         =", sp.simplify(u_planck))

# (i) Rayleigh-Jeans limit hnu/kT -> 0  : should give classical 8 pi nu^2 k T / c^3 (no h)
rj = sp.series(u_planck, h, 0, 1).removeO()
print("RJ limit (h->0)      =", sp.simplify(rj))

# (ii) Turn OFF stimulated emission (B21 -> 0): the '-1' disappears -> Wien, NOT blackbody
u_wien = sp.simplify(u_sol.subs(B21,0).subs(B12, g2*B21/g1 + B12))  # keep B12; B21=0
u_wien = sp.simplify(u_sol.subs(B21,0))
print("Wien (no stim emit)  =", u_wien, "  (~ e^{-hnu/kT}, no blackbody '-1')")
