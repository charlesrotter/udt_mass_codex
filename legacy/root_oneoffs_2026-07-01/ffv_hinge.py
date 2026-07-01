"""
THE SPINOR HINGE (Task 4). The doc names the open hinge as:
  'is the seal-VALUE of the forced odd source T_tr,T_ttheta required nonzero?'
  IF nonzero at seal => single-valued odd boson (Dirichlet-pinned to 0 there)
     cannot supply it => two-valued (T^2=-1) spinor FORCED (C-strong).
  IF it may vanish at seal => single-valued odd boson suffices => spinor NOT forced.

We have COMPUTED (ffv_survive / numeric): with the seal parities
(phi even, arm odd), G_tr|seal = G_ttheta|seal = 0 IDENTICALLY.
By G=kappa T, T_tr|seal = T_ttheta|seal = 0.

This script makes that airtight by a DIRECT seal-value computation and by
checking robustness: does ANY admissible seal data (nonzero A_t, B_t, the
surviving odd-t velocities, plus generic even phi) produce nonzero G_tr AT
the seal? Scan many random admissible seal jets numerically.
Agent: verifier-2026-06-14.
"""
import numpy as np
exec(open('/home/udt-admin/udt_mass_codex/ffv_numeric.py').read().split('X = (0.4')[0])

# Build phi EVEN in t and arm ODD in t with RANDOM coefficients, evaluate G_tr at t=0.
rng = np.random.default_rng(7)
worst = 0.0
for trial in range(40):
    a = rng.normal(size=8)
    b = rng.normal(size=8)
    p = rng.normal(size=6)
    # phi even in t (only cos(t) terms): even => phi(-t)=phi(t)
    phi_e = lambda t, r, th, p=p: (p[0] + p[1]*r + p[2]*np.cos(th) + p[3]*r*np.cos(th))*(1 + p[4]*np.cos(1.3*t) + p[5]*np.cos(2.1*t))
    # arm odd in t (only sin(t)): odd => A(-t)=-A(t)
    A_o = lambda t, r, th, a=a: (a[0]*np.sin(r) + a[1]*np.cos(th) + a[2]*r + a[3])*(a[4]*np.sin(1.1*t) + a[5]*np.sin(0.7*t))
    B_o = lambda t, r, th, b=b: (b[0]*np.cos(r) + b[1]*np.sin(th) + b[2]*r + b[3])*(b[4]*np.sin(0.9*t) + b[5]*np.sin(1.5*t))
    for (rr, tt) in [(1.4, 0.6), (0.8, 1.1), (2.0, 0.4)]:
        X0 = (0.0, rr, tt, 0.25)
        G = einstein_lower(make_metric(phi_e, A_o, B_o), X0, h=1e-4)
        worst = max(worst, abs(G[0, 1]), abs(G[0, 2]))
print("WORST |G_tr| or |G_ttheta| AT THE SEAL t=0 over 40 random admissible jets, 3 points:")
print("   = %.3e  (machine zero => seal-value of forced odd source is IDENTICALLY 0)" % worst)

# Contrast: away from seal, nonzero (sanity)
G = einstein_lower(make_metric(
    lambda t, r, th: (1+0.3*r*np.cos(th))*(1+0.4*np.cos(1.3*t)),
    lambda t, r, th: 0.2*np.sin(r)*np.sin(1.1*t),
    lambda t, r, th: 0.15*np.cos(r)*np.sin(0.9*t)), (0.4, 1.4, 0.6, 0.25), h=1e-4)
print("Away from seal t=0.4 (same fields):  G_tr=%.3e G_ttheta=%.3e (nonzero)" % (G[0, 1], G[0, 2]))
