#!/usr/bin/env python3
"""Fully independent recomputation. Different structure from author's code.
Convention: signature -+++. Metric ds^2 = -e^{-2 f} dt^2 + e^{2 f} dr^2 + r^2 dOmega^2."""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta varphi', real=True)
coords = [t, r, th, ph]
f = sp.Function('f')(r)   # this is phi(r)

A = sp.exp(-2*f)   # |g_tt|
B = sp.exp(2*f)    # g_rr
g = sp.diag(-A, B, r**2, r**2*sp.sin(th)**2)
gi = g.inv()
n = 4

# Christoffel  Gamma^a_{bc} = 1/2 g^{ad}( d_b g_{dc} + d_c g_{db} - d_d g_{bc} )
Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            expr = sp.S(0)
            for d in range(n):
                expr += gi[a,d]*(sp.diff(g[d,c],coords[b]) + sp.diff(g[d,b],coords[c]) - sp.diff(g[b,c],coords[d]))
            Gam[a][b][c] = sp.simplify(expr/2)

# Ricci  R_{bd} = d_a Gam^a_{bd} - d_d Gam^a_{ba} + Gam^a_{ae}Gam^e_{bd} - Gam^a_{de}Gam^e_{ba}
Ric = sp.zeros(n,n)
for b in range(n):
    for d in range(n):
        expr = sp.S(0)
        for a in range(n):
            expr += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][b][a], coords[d])
            for e in range(n):
                expr += Gam[a][a][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][a]
        Ric[b,d] = sp.simplify(expr)

Rscal = sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
G = sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        G[a,b] = sp.simplify(Ric[a,b] - sp.Rational(1,2)*g[a,b]*Rscal)

# mixed G^a_b
Gmix = sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        Gmix[a,b] = sp.simplify(sum(gi[a,c]*G[c,b] for c in range(n)))

print("G^t_t      =", sp.simplify(Gmix[0,0]))
print("G^r_r      =", sp.simplify(Gmix[1,1]))
print("G^th_th    =", sp.simplify(Gmix[2,2]))
print("G^ph_ph    =", sp.simplify(Gmix[3,3]))
print("G^t_t - G^r_r =", sp.simplify(Gmix[0,0]-Gmix[1,1]))
print("off-diagonal G nonzero?:", any(sp.simplify(Gmix[i,j])!=0 for i in range(n) for j in range(n) if i!=j))

# ---- Schwarzschild check
M,Q = sp.symbols('M Q', positive=True)
fS = -sp.Rational(1,2)*sp.log(1-2*M/r)
print("\nSchwarzschild G^t_t   =", sp.simplify(Gmix[0,0].subs(f,fS).doit()))
print("Schwarzschild G^th_th =", sp.simplify(Gmix[2,2].subs(f,fS).doit()))

# ---- Reissner-Nordstrom check; 8piG T = G, so T^t_t = G^t_t/(8 pi)
fRN = -sp.Rational(1,2)*sp.log(1-2*M/r+Q**2/r**2)
TtRN = sp.simplify(Gmix[0,0].subs(f,fRN).doit()/(8*sp.pi))
TthRN = sp.simplify(Gmix[2,2].subs(f,fRN).doit()/(8*sp.pi))
print("\nRN T^t_t   =", TtRN)
print("RN T^th_th =", TthRN)
print("RN T^t_t + T^th_th =", sp.simplify(TtRN+TthRN))

# ---- scalar stress, independent: T_{mu nu} = d_mu psi d_nu psi - g_mu nu (1/2 (d psi)^2 + V)
psi = sp.Function('psi')(r); V = sp.Function('V')(psi)
dpsi = [sp.diff(psi,coords[i]) for i in range(n)]
X = sp.Rational(1,2)*sum(gi[i,j]*dpsi[i]*dpsi[j] for i in range(n) for j in range(n))
Tdown = sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        Tdown[a,b] = dpsi[a]*dpsi[b] - g[a,b]*(X+V)
Tsc_mix = [sp.simplify(sum(gi[a,c]*Tdown[c,a] for c in range(n))) for a in range(n)]
print("\nScalar T^t_t =", Tsc_mix[0])
print("Scalar T^r_r =", Tsc_mix[1])
print("Scalar T^t_t - T^r_r =", sp.simplify(Tsc_mix[0]-Tsc_mix[1]))

# ---- V-independence: match psi=f, residual difference
res_tt = sp.simplify(Gmix[0,0]/(8*sp.pi) - Tsc_mix[0].subs(psi,f).doit())
res_rr = sp.simplify(Gmix[1,1]/(8*sp.pi) - Tsc_mix[1].subs(psi,f).doit())
print("\n(res_tt - res_rr) with psi=f =", sp.simplify(res_tt-res_rr))
