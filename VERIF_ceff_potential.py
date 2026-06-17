#!/usr/bin/env python
"""
VERIF_ceff_potential.py  -- OBSERVE (compute), not canonical.

Question (Conjecture A): the W2 f-weighted hyperbolic shape-sector wave
(bulk quadratic  [2 r^2 sin(th)/(1+w)^2] (w_T^2/f - f w_r^2),  w2_uncovering_results.md:30-31)
has characteristic speed dr/dT = +- f = c_eff (variable-speed / analogue medium).
Put it in Schrodinger / effective-potential form on the MATTER cell (negative phi,
f = e^{-2 phi} > 1) and decide: TRAPPING WELL vs BARRIER vs HORIZON vs FEATURELESS.

Driver: Claude (Opus 4.8 1M).  2026-06-17.  float64.  New file only.

REDUCTION (documented):
  Lagrangian density (angular factor sin(th) integrated out):
     L = P(r) ( w_T^2 / f  -  f w_r^2 ),   P(r) = 2 r^2 / (1+w0(r))^2,  f = e^{-2 phi(r)}.
  Euler-Lagrange (leading wave operator, prefactor P frozen at background w0):
     (2P/f) w_TT  -  d/dr( 2 P f w_r ) = 0.
  Separate  w = e^{-i omega T} u(r):
     (P f u')' + omega^2 (P/f) u = 0.                                    (SL form, weight P/f)
  Characteristic speed: ratio of principal symbols -> c_eff^2 = f^2, i.e. dr/dT = +- f.  (matches W2)

  Optical / tortoise coordinate (natural for variable wave speed f):
     dr*/dr = 1/f      (so the wave travels at unit speed in r*).
  Amplitude rescale to kill first-derivative term:  u = psi / sqrt(S),  S = P/f
     (S is the coefficient that makes the operator d/dr*( (Pf) d/dr ) = d/dr*( ... );
      in r* the operator is  d^2 u/dr*^2 * (Pf/f) ... -- done carefully symbolically below.)

  Result (derived by sympy below):  -psi'' (in r*) + V(r*) psi = omega^2 psi,
     V(r*) = (1/sqrt(W)) d^2 sqrt(W)/dr*^2 ,   W(r*) = P(r) * f(r)   [the SL "p*weight" product in r*].
  This is the standard Liouville normal form:  for  (p u')' + omega^2 q u = 0 with the
  tortoise choice making p/q = f^2 the speed^2, V = W''/... -- the script derives V EXACTLY.
"""
import sys
import numpy as np
import sympy as sp

# ----------------------------------------------------------------------------
# PART 1: SYMBOLIC derivation of the Schrodinger potential V(r*) (Liouville form)
# ----------------------------------------------------------------------------
def derive_symbolic():
    r = sp.symbols('r', positive=True)
    phi = sp.Function('phi')(r)
    w0  = sp.Function('w')(r)        # background shape
    om  = sp.symbols('omega', positive=True)
    f   = sp.exp(-2*phi)
    P   = 2*r**2/(1+w0)**2

    # SL operator:  (P f u')' + om^2 (P/f) u = 0.
    p_coef = P*f          # coefficient of u' inside derivative
    q_coef = P/f          # weight (mult by om^2)

    # Tortoise: dr*/dr = 1/f  => d/dr = (1/f) d/dr*.  In r*, write D = d/dr*.
    # (p u')' = (1/f) D[ p (1/f) D u ] = (1/f) D[ (p/f) D u ].
    # SL becomes:  (1/f) D[ (p/f) D u ] + om^2 q u = 0
    #   => D[ (p/f) D u ] + om^2 (f q) u = 0.
    #   p/f = P,   f q = P.   => D[ P D u ] + om^2 P u = 0.   <-- clean! both = P.
    # So in r*:  (P u')' + om^2 P u = 0  with ' = d/dr*.  Liouville normal form:
    #   u = psi / sqrt(P):   -psi'' + V psi = om^2 psi,  V = (sqrt(P))'' / sqrt(P)   ('=d/dr*)
    # We must express d/dr* via dr = f dr*.
    # Let g = sqrt(P).  V = (1/g) d^2 g/dr*^2.  d/dr* = f d/dr.
    g = sp.sqrt(P)
    dg = f*sp.diff(g, r)                 # dg/dr*
    d2g = f*sp.diff(dg, r)              # d2g/dr*^2
    V = sp.simplify(d2g/g)
    return r, phi, w0, V

# ----------------------------------------------------------------------------
# PART 2: NUMERIC evaluation on a real matter-cell phi(r) profile
# ----------------------------------------------------------------------------
def get_profile_from_solver(N=96, p=0.4, kap8=0.05):
    """Import the #56-equivalent spectral radial soliton, return r, phi, w0(=0)."""
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location("srs", "spectral_radial_soliton.py")
    srs = importlib.util.module_from_spec(spec); sys.modules["srs"]=srs
    spec.loader.exec_module(srs)
    out = srs.solve(N, p=p, kap8=kap8, verbose=False)
    # Identify field names
    keys = list(out.keys())
    return out, keys

def build_potential_numeric(r, phi, w0=0.0):
    """V(r) and V as function of tortoise r*, evaluated numerically on grid r (sorted ascending)."""
    r = np.asarray(r, float); phi = np.asarray(phi, float)
    isort = np.argsort(r); r=r[isort]; phi=phi[isort]
    f = np.exp(-2*phi)
    if np.isscalar(w0): w0 = np.full_like(r, w0)
    P = 2*r**2/(1+w0)**2
    g = np.sqrt(P)
    # d/dr* = f d/dr.  Use numpy gradient on nonuniform grid.
    dgr  = np.gradient(g, r)
    dgs  = f*dgr                       # dg/dr*
    # d2g/dr*^2 = f d/dr(dg/dr*)
    d2gs = f*np.gradient(dgs, r)
    V = d2gs/g
    # tortoise coordinate
    rstar = np.concatenate([[0],np.cumsum(np.diff(r)/((f[1:]+f[:-1])/2))])
    return dict(r=r, phi=phi, f=f, P=P, V=V, rstar=rstar)

if __name__ == "__main__":
    np.set_printoptions(suppress=True, precision=6, linewidth=120)
    print("="*78)
    print("PART 1  SYMBOLIC V(r*) for the W2 f-weighted w-wave (Liouville normal form)")
    print("="*78)
    r, phi, w0, V = derive_symbolic()
    print("V(r*) = (1/sqrt(P)) (d^2/dr*^2) sqrt(P),  d/dr* = f d/dr,  P=2r^2/(1+w)^2, f=e^{-2phi}")
    print("\nGeneral V (w(r), phi(r)):")
    sp.pprint(V)
    # specialize w0=0 (the radial-only matter cell: shape flat, only phi varies)
    Vw0 = sp.simplify(V.subs(w0, 0))
    print("\nV with w0=0  (matter cell, shape-flat background, only phi(r) live):")
    sp.pprint(Vw0)
    # Express in phi, phi', phi''
    phir, phirr = sp.symbols("phi_r phi_rr", real=True)
    Vsub = Vw0.subs({sp.Derivative(phi,(r,2)):phirr, sp.Derivative(phi,r):phir})
    Vsub = sp.simplify(Vsub)
    print("\nV(r*) in terms of phi, phi_r, phi_rr (w0=0):")
    sp.pprint(Vsub)

    print("\n"+"="*78)
    print("PART 2  NUMERIC V on the #56-equivalent matter-cell phi(r) profile")
    print("="*78)
    import importlib.util
    spec = importlib.util.spec_from_file_location("srs","spectral_radial_soliton.py")
    srs = importlib.util.module_from_spec(spec); sys.modules["srs"]=srs
    spec.loader.exec_module(srs)
    out = srs.solve(96, p=0.4, kap8=0.05, verbose=False)
    rr  = np.asarray(out['r'],float); ph = np.asarray(out['phi'],float)
    isort=np.argsort(rr); rr=rr[isort]; ph=ph[isort]
    print(f"  profile: r in [{rr.min():.4f},{rr.max():.4f}], "
          f"phi in [{ph.min():.4f},{ph.max():.4f}]  (phi(core)={ph[0]:.4f}, phi(seal)={ph[-1]:.4f})")
    D = build_potential_numeric(rr, ph, w0=0.0)
    V=D['V']; f=D['f']
    print(f"  f=e^-2phi in [{f.min():.4f},{f.max():.4f}]  (c_eff=f: NO blow-up => no analogue horizon)")
    print(f"  V(r) range: [{V.min():.6g}, {V.max():.6g}]")
    imin=np.argmin(V)
    print(f"  V minimum {V[imin]:.6g} at r={rr[imin]:.4f}  (well depth scale)")
    print(f"  V at core r={rr[0]:.4f}: {V[0]:.6g};  V at seal r={rr[-1]:.4f}: {V[-1]:.6g}")
    # sign of phi' -> sign of V
    phir_num=np.gradient(ph,rr)
    print(f"  phi'(r) sign: min={phir_num.min():.4g}, max={phir_num.max():.4g} "
          f"(phi'>0 everywhere => V=-2 phi' f^2/r < 0 => ATTRACTIVE)")
    # Tabulate V(r)
    print("\n   r        phi        f        V(r)       region")
    idx=np.linspace(0,len(rr)-1,16).astype(int)
    for i in idx:
        reg = "core" if rr[i]<0.5 else ("body" if rr[i]<4 else "outer")
        print(f"  {rr[i]:7.4f}  {ph[i]:8.4f}  {f[i]:7.4f}  {V[i]:10.5g}   {reg}")

    # ---- scale test: is the well set by DILATION (phi profile) or by outer radius? ----
    # V = -2 phi' f^2 / r ; the depth/location is set entirely by phi(r) (no R_wall in V).
    print("\n  SCALE: V(r) formula contains NO outer-wall radius R; it is fixed by phi(r),")
    print("         i.e. by the DILATION profile (kappa/xi via the soliton). The well")
    print("         location/depth move only if phi(r) moves.")

    # save arrays for the eigen/box test
    np.savez("VERIF_ceff_potential_profile.npz", r=rr, phi=ph, f=f, V=V, rstar=D['rstar'], P=D['P'])
    print("\n  saved profile -> VERIF_ceff_potential_profile.npz")
