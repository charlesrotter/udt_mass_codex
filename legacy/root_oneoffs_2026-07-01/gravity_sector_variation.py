#!/usr/bin/env python3
"""
gravity_sector_variation.py
Re-derivation of UDT's gravitational field equations carrying EVERY term.
Adversarial re-do of udt_field_equations_derivation_results.md.

OBSERVE mode: report what is there. No targeted verdict.

Constructor: Claude Opus 4.8 (1M), agent for udt_mass_codex, 2026-06-18.

Action under suspicion:
    S = int d^4x sqrt(-g) [ f(phi) R + L_matter ],   f(phi) = c(phi)^4/(16 pi G)
with c(phi) = c0 e^{-2 phi}  =>  f(phi) = (c0^4/16 pi G) e^{-8 phi}.

The doc wrote the field eqn as G_mu_nu = (8 pi G / c^4) T, i.e. divided by f
as if CONSTANT. Honest variation of a NON-MINIMAL coupling f(phi) R gives
extra (g_mu_nu Box - nabla_mu nabla_nu) f terms that DO NOT vanish in vacuum.

We compute three things:
  (1) The general scalar-tensor field equations (textbook identity, verified
      structurally) so the (gBox - nabla nabla)f terms are explicit.
  (2) For the SSS UDT metric with phi SLAVED to the metric (c=c0 e^{-2phi},
      phi appearing IN g_tt), compute the FULL EOM from the action density
      reduced on the metric ansatz -- the honest "minisuperspace" variation.
  (3) Conformal transformation to Einstein frame: does f R reduce to R-tilde
      plus a scalar kinetic term? Where does the c^4 reappear?
"""

import sympy as sp

sp.init_printing()

# ---------------------------------------------------------------------------
# Coordinates and the SSS metric (CANON C-2026-06-18-1)
# CHOSE: static, spherical, diagonal, areal-r.  phi = phi(r).
# ---------------------------------------------------------------------------
t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
phi = sp.Function('phi')(r)         # the dilation field, phi(r)
c0, G = sp.symbols('c0 G', positive=True)

# metric form g = diag(-e^{-2phi} c0^2, e^{2phi}, r^2, r^2 sin^2 th)
gtt = -sp.exp(-2*phi)*c0**2
grr =  sp.exp( 2*phi)
gthth = r**2
gpp = r**2 * sp.sin(th)**2

coords = [t, r, th, ph]
g = sp.diag(gtt, grr, gthth, gpp)
ginv = g.inv()
detg = sp.simplify(g.det())
sqrtmg = sp.sqrt(-detg)
print("=== METRIC ===")
print("g_tt =", gtt, "  g_rr =", grr)
print("sqrt(-g) =", sp.simplify(sqrtmg))

# ---------------------------------------------------------------------------
# Christoffel, Riemann, Ricci, Ricci scalar  (native, full GR machinery as a MINE)
# ---------------------------------------------------------------------------
n = 4
Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for cc in range(n):
            s = 0
            for d in range(n):
                s += ginv[a,d]*(sp.diff(g[d,b],coords[cc]) + sp.diff(g[d,cc],coords[b]) - sp.diff(g[b,cc],coords[d]))
            Gamma[a][b][cc] = sp.simplify(s/2)

# Ricci tensor
Ric = sp.zeros(n,n)
for b in range(n):
    for d in range(n):
        s = 0
        for a in range(n):
            s += sp.diff(Gamma[a][b][d], coords[a])
            s -= sp.diff(Gamma[a][b][a], coords[d])
            for e in range(n):
                s += Gamma[a][a][e]*Gamma[e][b][d]
                s -= Gamma[a][d][e]*Gamma[e][b][a]
        Ric[b,d] = sp.simplify(s)

Rscalar = sp.simplify(sum(ginv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
print("\n=== RICCI SCALAR R ===")
print("R =", Rscalar)

# Einstein tensor mixed G^a_b
Gmix = sp.zeros(n,n)
Gdown = Ric - sp.Rational(1,2)*g*Rscalar
for a in range(n):
    for b in range(n):
        Gmix[a,b] = sp.simplify(sum(ginv[a,c]*Gdown[c,b] for c in range(n)))
print("\n=== EINSTEIN TENSOR (mixed) ===")
print("G^t_t =", sp.simplify(Gmix[0,0]))
print("G^r_r =", sp.simplify(Gmix[1,1]))
print("G^th_th =", sp.simplify(Gmix[2,2]))
print("G^t_t - G^r_r =", sp.simplify(Gmix[0,0]-Gmix[1,1]))

# ---------------------------------------------------------------------------
# f(phi) and its covariant derivative terms  (g_mu_nu Box - nabla_mu nabla_nu) f
# This is the SUSPECT, DROPPED term.  Compute it on this metric.
# ---------------------------------------------------------------------------
fsym = sp.Function('f')
f = sp.exp(-8*phi) * c0**4/(16*sp.pi*G)   # f(phi)=c^4/16piG, c=c0 e^{-2phi}

# nabla_mu nabla_nu f  = partial_mu partial_nu f - Gamma^l_{mu nu} partial_l f
df = [sp.diff(f, coords[mu]) for mu in range(n)]
HessDown = sp.zeros(n,n)   # nabla_mu nabla_nu f (lower indices)
for mu in range(n):
    for nu in range(n):
        s = sp.diff(df[nu], coords[mu])
        for l in range(n):
            s -= Gamma[l][mu][nu]*df[l]
        HessDown[mu,nu] = sp.simplify(s)

# Box f = g^{mu nu} nabla_mu nabla_nu f
Boxf = sp.simplify(sum(ginv[mu,nu]*HessDown[mu,nu] for mu in range(n) for nu in range(n)))
print("\n=== d'Alembertian of f ===")
print("Box f =", Boxf)

# The scalar-tensor extra term, lower indices:  E_mu_nu = (g_mu_nu Box - nabla_mu nabla_nu) f
Edown = sp.zeros(n,n)
for mu in range(n):
    for nu in range(n):
        Edown[mu,nu] = sp.simplify(g[mu,nu]*Boxf - HessDown[mu,nu])
# mixed
Emix = sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        Emix[a,b] = sp.simplify(sum(ginv[a,c]*Edown[c,b] for c in range(n)))
print("\n=== EXTRA SCALAR-TENSOR TERM  E^a_b = (g Box - nabla nabla) f / f  (mixed, divided by f for comparison to G) ===")
for a in range(n):
    print(f"E^{a}_{a}/f =", sp.simplify(Emix[a,a]/f))

# ---------------------------------------------------------------------------
# THE FULL VACUUM FIELD EQUATION (T=0):
#   f G_mu_nu + (g_mu_nu Box - nabla_mu nabla_nu) f = 0
# i.e.  G^a_b + E^a_b / f = 0  .  Show it is NOT just G^a_b = 0.
# ---------------------------------------------------------------------------
print("\n=== FULL VACUUM EOM components:  f*G^a_b + E^a_b = 0   (divide by f) ===")
EOM = {}
for a in range(n):
    expr = sp.simplify(Gmix[a,a] + Emix[a,a]/f)
    EOM[a] = expr
    print(f"[tt,rr,thth,pp][{a}]:  G^a_a + E^a_a/f =", expr)

print("\n=== tt - rr of the FULL equation (vacuum) ===")
ttmrr = sp.simplify((Gmix[0,0]+Emix[0,0]/f) - (Gmix[1,1]+Emix[1,1]/f))
print("(G+E/f)^t_t - (G+E/f)^r_r =", ttmrr)
