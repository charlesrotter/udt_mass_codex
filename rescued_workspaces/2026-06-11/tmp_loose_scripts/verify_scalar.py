import sympy as sp

r, t, th, ph, c, mu = sp.symbols('r t theta phi_a c mu', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r)
F = sp.Function('F')(r)   # the scalar matter field, F(r) static

g = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2)
gi = g.inv()
coords = [t,r,th,ph]; n=4

# Scalar field stress-energy for L = -1/2 (d phi)^2 - 1/2 mu^2 phi^2
# T_mn = d_m F d_n F - g_mn ( 1/2 g^ab d_a F d_b F + 1/2 mu^2 F^2 )
dF = [sp.diff(F, x) for x in coords]   # only r nonzero
kin = sp.Rational(1,2)*sum(gi[a,b]*dF[a]*dF[b] for a in range(n) for b in range(n))
pot = sp.Rational(1,2)*mu**2*F**2
T_low = sp.zeros(n,n)
for m in range(n):
    for nn in range(n):
        T_low[m,nn] = dF[m]*dF[nn] - g[m,nn]*(kin+pot)
T_mixed = sp.simplify(gi*T_low)
Ttt = sp.simplify(T_mixed[0,0]); Trr = sp.simplify(T_mixed[1,1])
d = sp.simplify(Ttt - Trr)
print("T^t_t =", Ttt)
print("T^r_r =", Trr)
print("T^t_t - T^r_r =", d)
# compare to -g^rr F'^2  = -(1/B) F'^2
print("-(1/B)F'^2 =", sp.simplify(-(1/B)*dF[1]**2))
print("equal to -g^rr F'^2:", sp.simplify(d - (-(1/B)*dF[1]**2))==0)

# Now substitute the UDT metric A=e^{-2P}, B=e^{2P} and let F=P (identify matter scalar with metric phi)
P = sp.Function('P')(r)
dsub = d.subs({A: sp.exp(-2*P), B: sp.exp(2*P), F: P})
print("\nWith UDT metric & F=phi:", sp.simplify(dsub.doit()))
