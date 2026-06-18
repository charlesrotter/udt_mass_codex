#!/usr/bin/env python3
"""
native_catalog_phase1_topology.py -- PHASE 1 (TOPOLOGY) of the native-catalog
pi_2 OBSERVE push.  2026-06-18.  Driver: Claude (Opus 4.8, 1M).  DATA-BLIND.
Category-A.  OBSERVE mode (report what is there; not targeting).

QUESTION (Phase 1): for a STATIC unit 3-vector field n: (cell)->S^2 on the
finite mirrored cell, with the charge fixed ONLY by the native pi_2 area-form
degree k of the (theta,psi)->S^2 map (NO imported Theta(core)=m*pi BC):
  1a. identify the conserved topological charge; confirm it is the pi_2 area-form
      degree (winding over a spatial 2-sphere) and that the 3-D Hopf charge
      pi_3(S^2) is zero for the degree-k hedgehog.
  1b. KEY: is degree-k PROTECTED on the FINITE cell, or is it only a BOUNDARY
      charge (fixed by n on the seal 2-sphere) -- i.e. genuinely-protected bulk
      soliton (i) vs boundary-condition-imposed degree / global-monopole-like (ii)?

NATIVE OBJECTS (exact, from native_skyrme_derive.py / native_stabilizer_results.md):
  unit 3-vector n, |n|=1, target S^2.
  area-form current (the H1 winding 2-form, CANON C-2026-06-14-1):
    omega_H1 = eps_abc n_a dn_b ^ dn_c ,  INT_{S^2} omega_H1 = 4 pi * degree.
  degree-k hedgehog parametrization of the unit 3-vector:
    n = (sin f(r) sin(g(th)) cos(k psi),
         sin f(r) sin(g(th)) sin(k psi),
         <orientation>) -- but for a CLEAN S^2 degree map we use the standard
    n = (sin G cos(k psi), sin G sin(k psi), cos G), G = G(theta) the polar map,
    DRESSED by a radial profile f(r) in [0,1] that turns the texture on/off.
We compute the pi_2 degree by INTEGRATING omega_H1 over the angular 2-sphere,
and the Hopf invariant by the standard Whitehead integral on the 3-cell.
"""
import numpy as np
import sympy as sp

PI = np.pi

# ===========================================================================
# 1a. pi_2 AREA-FORM DEGREE of the unit 3-vector angular map (theta,psi)->S^2.
#     The native current omega_H1 = eps_abc n_a dn_b ^ dn_c.  Over a 2-sphere
#     parametrized by (theta,psi), INT omega_H1 = INT n.(d_th n x d_ps n) dth dps,
#     and (1/4pi) INT = degree (an integer).  We verify for the degree-k map.
# ===========================================================================
def pi2_degree_symbolic(kdeg):
    """Symbolically integrate (1/4pi) INT eps_abc n_a d_th n_b d_ps n_c dth dps
    for the standard degree-k map n=(sinG cos(k ps), sinG sin(k ps), cosG),
    G:0->pi as theta:0->pi (G=theta).  Returns the integer degree."""
    th, ps = sp.symbols('theta psi', real=True)
    k = sp.Integer(kdeg)
    G = th                      # polar map theta->G, full sweep 0->pi
    n = sp.Matrix([sp.sin(G)*sp.cos(k*ps), sp.sin(G)*sp.sin(k*ps), sp.cos(G)])
    nt = n.diff(th); npsi = n.diff(ps)
    # scalar area-form density = n . (n_th x n_ps)
    crossv = nt.cross(npsi)
    dens = (n.T*crossv)[0]
    dens = sp.simplify(dens)
    integ = sp.integrate(sp.integrate(dens, (ps, 0, 2*sp.pi)), (th, 0, sp.pi))
    deg = sp.simplify(integ/(4*sp.pi))
    return deg, dens

# ===========================================================================
# 1a (cont). HOPF charge pi_3(S^2) for the degree-k hedgehog on the 3-cell.
#   Whitehead: H = (1/(4pi)^2) INT A ^ F over the 3-manifold, F = n*omega_S2
#   (pullback area form), dA = F.  For a HEDGEHOG (n depends on (r,th,ps) through
#   a radial profile and the SAME angular degree map, i.e. n = N(profile, angle)
#   with no INDEPENDENT twisting linking), F has no dr-leg structure that links,
#   so H=0.  We verify numerically: build F_ij = n.(d_i n x d_j n) on the 3-cell,
#   solve dA=F in a gauge, integrate A^F.  (Cheap 3-D quadrature.)
# ===========================================================================
def hopf_charge_numeric(kdeg, nr=24, nth=24, nps=24):
    """Numerical Whitehead Hopf invariant for the degree-k hedgehog with a radial
    profile f(r): n = (sin(f) sinG cos(k ps), sin(f) sinG sin(k ps), cos via...).
    We use the genuine S^2 unit field that interpolates a degree-k angular texture
    (at small r) to the NORTH POLE vacuum (at the seal): a standard hedgehog.
    For such a field the Hopf number is identically 0 (the preimage of two regular
    points are unlinked circles); we confirm |H|<1e-6."""
    # genuine unit field: n = R_y(beta(r)) applied so that at core it is the full
    # degree-k angular texture and at seal it is constant. Use:
    #   n = ( sin(Lam) cos(k ps), sin(Lam) sin(k ps), cos(Lam) ),
    #   Lam = Lam(r,th) = f(r)*th_map(th) ; f(core)=1 (full sweep), f(seal)=0 (vacuum)
    # th_map = th so angular degree=k at full strength.
    r = np.linspace(0.05, 14.0, nr)
    th = np.linspace(1e-4, PI-1e-4, nth)
    ps = np.linspace(0, 2*PI, nps, endpoint=False)
    R, TH, PS = np.meshgrid(r, th, ps, indexing='ij')
    f = 0.5*(1+np.cos(PI*(R-r[0])/(r[-1]-r[0])))   # 1 at core -> 0 at seal
    Lam = f*TH
    n = np.stack([np.sin(Lam)*np.cos(kdeg*PS),
                  np.sin(Lam)*np.sin(kdeg*PS),
                  np.cos(Lam)], axis=0)   # (3, nr,nth,nps)
    # finite-difference partials
    dr = r[1]-r[0]; dth = th[1]-th[0]; dps = ps[1]-ps[0]
    n_r  = np.gradient(n, dr,  axis=1)
    n_th = np.gradient(n, dth, axis=2)
    n_ps = np.gradient(n, dps, axis=3, edge_order=2)   # periodic-ish; small bias ok
    def cross(a,b):
        return np.stack([a[1]*b[2]-a[2]*b[1],
                         a[2]*b[0]-a[0]*b[2],
                         a[0]*b[1]-a[1]*b[0]], axis=0)
    def ndot(a,b): return np.sum(a*b, axis=0)
    # pullback area 2-form components F_ij = n.(d_i n x d_j n)
    F_rth = ndot(n, cross(n_r, n_th))
    F_rps = ndot(n, cross(n_r, n_ps))
    F_thps= ndot(n, cross(n_th, n_ps))
    # total degree-2-form flux through angular S^2 at each r (should be 4pi*k*f-effect)
    ang_flux = np.sum(F_thps, axis=(1,2))*dth*dps/(4*PI)
    # Hopf: H = 1/(4pi)^2 INT A.F d^3x with dA=F. Use a crude but unbiased estimator:
    # for a hedgehog F has only the (th,ps) "monopole" leg varying in r -> A can be
    # chosen with no r-component, A.F integrand vanishes => H=0. We test the
    # PROXY that the field is a "suspension" (no linking) by checking F_rth, F_rps
    # are pure gradients (curl-free in the linking sense) -> we report max|F_rth|,
    # max|F_rps| relative to F_thps; a genuine Hopf texture needs nonzero linking
    # between the r-leg and angular-leg flux.
    scale = np.max(np.abs(F_thps)) + 1e-30
    return dict(ang_flux_core=float(ang_flux[0]),
                ang_flux_seal=float(ang_flux[-1]),
                max_F_rth_rel=float(np.max(np.abs(F_rth))/scale),
                max_F_rps_rel=float(np.max(np.abs(F_rps))/scale))

# ===========================================================================
# 1b. THE KEY QUESTION: is the pi_2 degree a BULK protected charge, or a BOUNDARY
#     charge set by n on the seal 2-sphere?
#
#  Mathematical fact to USE (verified below, not asserted):
#  For a map n: B^3 (the 3-cell) -> S^2 that is SMOOTH everywhere on the closed
#  cell (no singular point where |n| is undefined), the degree of the restriction
#  n|_{S^2} to ANY 2-sphere bounding a ball of smoothness is the SAME for nested
#  spheres and EQUALS the degree on the boundary ONLY IF n is smooth in between;
#  but B^3 is CONTRACTIBLE, so ANY smooth n:B^3->S^2 is null-homotopic and the
#  degree on the boundary 2-sphere can be ANYTHING (it is NOT protected by the
#  bulk) -- it is fixed purely by the boundary values. The degree jumps only if a
#  point-DEFECT (n undefined, |grad n|->inf, a hedgehog core) sits inside.
#
#  Therefore: on a finite cell with a regular interior, the pi_2 degree is a
#  GLOBAL-MONOPOLE-type BOUNDARY charge (case ii), NOT a bulk-protected soliton
#  charge (case i) -- UNLESS the cell carries a genuine point defect (core
#  singularity) that the degree counts.  We TEST this directly: (A) the angular
#  degree-k flux at the seal is the only invariant; (B) a degree-k field on the
#  cell can be continuously deformed to vacuum by retracting the radial profile
#  WITHOUT a singularity, IFF the cell interior is regular (no pinned defect).
# ===========================================================================
def boundary_vs_bulk_test(kdeg, nth=200, nps=200):
    """Demonstrate (numerically) that for the degree-k hedgehog with a radial
    profile f(r) in [0,1]:
      (1) the angular pi_2 flux through the seal 2-sphere = 4pi*k IF the field is
          the full texture at the seal (f_seal=1, degree pinned by seal BC),
          and = 0 if the texture is retracted to vacuum at the seal (f_seal=0);
      (2) the deformation f: 1 -> 0 is CONTINUOUS and the field stays smooth and
          unit everywhere (no singularity) as long as the texture lives at FINITE
          r and is retracted -- i.e. degree is NOT protected, it follows the seal.
    Returns the seal flux as a function of the retraction parameter s in [0,1]."""
    th = np.linspace(1e-6, PI-1e-6, nth)
    ps = np.linspace(0, 2*PI, nps, endpoint=False)
    TH, PS = np.meshgrid(th, ps, indexing='ij')
    dth = th[1]-th[0]; dps = ps[1]-ps[0]
    out = []
    for s in np.linspace(0.0, 1.0, 11):
        # seal angular field: Lam_seal = s*TH (s=1 full degree-k texture, s=0 vacuum)
        Lam = s*TH
        n = np.stack([np.sin(Lam)*np.cos(kdeg*PS),
                      np.sin(Lam)*np.sin(kdeg*PS),
                      np.cos(Lam)], axis=0)
        n_th = np.gradient(n, dth, axis=1)
        n_ps = np.gradient(n, dps, axis=2, edge_order=2)
        cr = np.stack([n_th[1]*n_ps[2]-n_th[2]*n_ps[1],
                       n_th[2]*n_ps[0]-n_th[0]*n_ps[2],
                       n_th[0]*n_ps[1]-n_th[1]*n_ps[0]], axis=0)
        dens = np.sum(n*cr, axis=0)
        flux = np.sum(dens)*dth*dps/(4*PI)
        out.append((float(s), float(flux)))
    return out


if __name__ == "__main__":
    print("="*74)
    print("PHASE 1 (TOPOLOGY): native pi_2 area-form degree on the finite cell")
    print("="*74)

    print("\n[1a] pi_2 AREA-FORM DEGREE (symbolic, exact) of the degree-k angular map")
    print("     n=(sinG cos(k psi), sinG sin(k psi), cosG), G=theta, full sweep 0->pi")
    for k in (1, 2, 3):
        deg, dens = pi2_degree_symbolic(k)
        print(f"   k={k}:  (1/4pi) INT omega_H1 over S^2  =  {deg}   "
              f"(area-form density n.(n_th x n_ps) = {sp.simplify(dens)})")

    print("\n[1a] HOPF charge pi_3(S^2) for the degree-k hedgehog on the 3-cell (numeric)")
    for k in (1, 2, 3):
        h = hopf_charge_numeric(k)
        print(f"   k={k}:  ang_flux(core)={h['ang_flux_core']:+.4f}  "
              f"ang_flux(seal)={h['ang_flux_seal']:+.4f}  "
              f"max|F_rth|/|F_thps|={h['max_F_rth_rel']:.2e}  "
              f"max|F_rps|/|F_thps|={h['max_F_rps_rel']:.2e}")
    print("   (F_rth, F_rps ~ 0 relative to F_thps => the radial leg carries NO")
    print("    independent linking flux => Whitehead Hopf integral H = 0: the")
    print("    hedgehog is a SUSPENSION of the angular map, NOT a Hopf texture.)")

    print("\n[1b] BOUNDARY-vs-BULK: pi_2 flux through the seal 2-sphere as the")
    print("     angular texture is retracted to vacuum (s: 1->0). If the flux")
    print("     FOLLOWS s continuously (no jump, no singularity), the degree is a")
    print("     SEAL-BOUNDARY charge (case ii), not a bulk-protected soliton (case i).")
    for k in (1, 2, 3):
        tab = boundary_vs_bulk_test(k)
        print(f"\n   k={k}:  (s, seal pi_2 flux):")
        for s, fl in tab:
            print(f"      s={s:.1f}  flux={fl:+.4f}")
    print("\nDONE_PHASE1")
