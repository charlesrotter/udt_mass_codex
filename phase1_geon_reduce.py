#!/usr/bin/env python3
"""
phase1_geon_reduce.py -- PHASE-1c step 1: SYMBOLIC O(A^2) coupled geon reduction.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A (borrow GR
numerics for tractability; impose NO physics, NO matter, NO scale). OBSERVE mode.
c=1.

THE COUPLED VACUUM SYSTEM (the genuine time-periodic geon, NO matter slot):
  We carry the held UDT diagonal background g_tt=-e^{-2 phi(r)}, g_rr=e^{2 phi(r)}
  (tie g_tt g_rr = -1 along grad phi, c=1) with phi(r) STATIC l=0, PLUS the
  Phase-0 physical l=2 even-parity transverse-traceless angular warp carrying the
  periodic DOF:
       g_thth = e^{...}-free angular block  r^2 (1 + A h(t,r) P2(theta))
       g_psps = r^2 sin^2(theta) (1 - A h(t,r) P2(theta))
  with h(t,r) = H(r) cos(w t)  (harmonic balance, k=1 retained; see C3 below).

  This is PURE VACUUM:  G_{mu nu}[g] = 0.  We expand in the wave amplitude A:
     phi  is O(A^2)   (the geon backreaction: sourced by the wave's own stress)
     h    is O(A^1)   (the wave)
  and project the vacuum equations into:
     * O(A^1) l=2 (P2) channel  -> the WAVE equation for H(r) on the phi background
                                    (at leading order phi=0 this is the Phase-1b
                                     flat l=2 operator; the phi-correction enters
                                     the wave eq at O(A^2), i.e. it shifts w(A)).
     * O(A^2) l=0 (time-averaged, angular-averaged) channel -> the EINSTEIN
       CONSTRAINT sourcing phi(r) from the time-averaged O(A^2) gravitational-wave
       stress.  This is the geon mechanism: <(grad h)^2>-type quadratic content of
       the wave is the ONLY source for phi.

  We DERIVE these two coupled radial relations symbolically here and hand the
  exact coefficient functions to the numerical solver (phase1_geon_solve.py).

REDUCTION CHOICES (tagged "chose or derived?", each with a relax-test):
  C1 [chose, forced]: background diagonal UDT tie g_tt g_rr = -1, phi STATIC l=0.
      Relax-test: the tie is the held UDT structure (charter); l=0 static is the
      Birkhoff sector for the averaged backreaction. Forced by the frame, not free.
  C2 [chose]: phi enters at O(A^2). Relax-test: this is the DEFINITION of the geon
      perturbative ordering (wave O(A), its stress O(A^2)); if phi had an O(A^0)
      or O(A^1) piece it would be either the (flat, m=0) static background or a
      linear tadpole that vanishes by parity. Verified below: the O(A^1) l=0 source
      is zero (no tadpole), so phi truly starts at O(A^2). DERIVED, not assumed.
  C3 [chose]: single time-harmonic h = H(r) cos(w t) (k=1). Relax-test: at O(A^2)
      cos^2(w t) = 1/2 + 1/2 cos(2 w t); the constant (DC) part sources the STATIC
      phi (kept), the 2w part would source an O(A^2) second-harmonic metric piece
      that does NOT feed back on H or on the DC phi at O(A^2) (it is O(A^2) and its
      backreaction on the wave is O(A^4)). So k=1 + DC phi is exact to O(A^2).
      Escalation (k=2 harmonic) only needed at O(A^4); flagged, not done here.
  C4 [chose]: angular ansatz = the SAME single P2 warp as Phase-0 (one master
      scalar). Relax-test: full Zerilli (H0,H1,H2,K) reduces to one gauge-invariant
      master; Phase-0 already matched. The O(A^2) l=0 source picks up the angular
      AVERAGE of P2^2 and (P2')^2 etc -- computed exactly below.

OUTPUT: exact symbolic
   (a) O(A^1) l=2 wave operator   L2[H; phi, w] = 0    (phi-dependence kept)
   (b) O(A^2) l=0 phi-source       S0[phi; H, w]  = 0   (time+angle averaged)
which the numerical solver discretizes (Chebyshev) and continues in amplitude A.
"""
import sympy as sp

# ---------------------------------------------------------------------------
# Symbols.  A = wave amplitude (continuation parameter).  phi is O(A^2): write
# phi = A^2 * F(r).  h = H(r) cos(w t) is O(A^1) carried with its own A.
# Full metric perturbation parameter is A; we expand G_{mu nu} to O(A^2).
# ---------------------------------------------------------------------------
t, r, th, ps = sp.symbols('t r theta psi', real=True)
A = sp.symbols('A')                       # wave amplitude / expansion param
w = sp.symbols('w', positive=True)
X = [t, r, th, ps]

H = sp.Function('H')(r)                    # wave radial profile (O(A^0) shape)
F = sp.Function('F')(r)                    # phi profile: phi(r) = A^2 F(r)

P2 = (3 * sp.cos(th)**2 - 1) / 2
h = A * H * sp.cos(w * t)                   # the O(A) wave
phi = A**2 * F                              # the O(A^2) backreaction

# Held UDT diagonal background WITH static phi, PLUS the l=2 TT angular warp.
g = sp.Matrix([
    [-sp.exp(-2 * phi), 0, 0, 0],
    [0, sp.exp(2 * phi), 0, 0],
    [0, 0, r**2 * (1 + h * P2), 0],
    [0, 0, 0, r**2 * sp.sin(th)**2 * (1 - h * P2)],
])


def einstein_tensor(g, X):
    """G_{mu nu} = R_{mu nu} - 1/2 g_{mu nu} R, computed exactly (vacuum target 0)."""
    n = len(X)
    ginv = g.inv()
    # Christoffel
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, c], X[b])
                                       + sp.diff(g[d, b], X[c])
                                       - sp.diff(g[b, c], X[d]))
                Gamma[a][b][c] = sp.Rational(1, 2) * s
    # Ricci
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][a]
            Ric[b, d] = sp.expand(s)
    Rs = sp.S(0)
    for a in range(n):
        for b in range(n):
            Rs += ginv[a, b] * Ric[a, b]
    Rs = sp.expand(Rs)
    G = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            G[a, b] = sp.expand(Ric[a, b] - sp.Rational(1, 2) * g[a, b] * Rs)
    return G, Ric, Rs


def series_A(expr, order):
    """coefficient of A^order in the A-series of expr (expr already has A)."""
    return sp.expand(sp.series(sp.expand(expr), A, 0, order + 1).removeO().coeff(A, order))


def time_avg(expr):
    """time-average over one period: <cos(w t)> = 0, <cos^2(w t)> = 1/2,
    <cos(2 w t)> = 0.  Implemented by replacing powers of cos(w t)."""
    e = sp.expand(expr)
    c = sp.cos(w * t)
    # replace cos^2 -> 1/2, cos^1 -> 0, and any residual cos(2 w t) -> 0
    e = e.rewrite(sp.cos)
    # collect as polynomial in c
    poly = sp.Poly(e, c) if e.has(c) else None
    if poly is None:
        # no explicit cos(w t): could still contain cos(2 w t) etc -> average 0 unless const
        # strip any cos(k w t) terms
        return _strip_time(e)
    out = sp.S(0)
    for (deg,), coeff in poly.terms():
        coeff = _strip_time(coeff)
        if deg == 0:
            out += coeff
        elif deg % 2 == 1:
            out += 0
        else:  # even power of cos -> central binomial / 2^deg
            from sympy import binomial, Rational
            avg = Rational(int(binomial(deg, deg // 2)), 2**deg)
            out += coeff * avg
    return sp.expand(out)


def _strip_time(e):
    """drop any explicit time-oscillating cos(k w t)/sin(k w t) (average 0),
    keep t-independent part."""
    e = sp.expand(e)
    if not e.has(t):
        return e
    # substitute oscillating funcs of t by 0 (they average to 0); keep constants
    return e.subs({sp.cos(w * t): 0, sp.sin(w * t): 0,
                   sp.cos(2 * w * t): 0, sp.sin(2 * w * t): 0}).doit()


if __name__ == "__main__":
    sp.init_printing()
    print("=" * 78)
    print("PHASE-1c step 1: SYMBOLIC O(A^2) COUPLED GEON REDUCTION (pure vacuum)")
    print("=" * 78)
    print("metric: g_tt=-e^{-2A^2 F}, g_rr=e^{2A^2 F}, l=2 TT warp A H cos(w t) P2")
    print("expanding G_{mu nu}=0 in A; phi=A^2 F (geon backreaction).\n")

    G, Ric, Rs = einstein_tensor(g, X)

    # -----------------------------------------------------------------
    # O(A^1): the WAVE equation. Take the traceless angular combination
    # C = G^th_th - G^ps_ps at O(A) (isolates the single l=2 master scalar).
    # -----------------------------------------------------------------
    ginv = g.inv()
    Gthth_up = sp.expand(ginv[2, 2] * G[2, 2])     # G^th_th
    Gpsps_up = sp.expand(ginv[3, 3] * G[3, 3])     # G^ps_ps
    Cwave = Gthth_up - Gpsps_up

    print("--- O(A^1): l=2 wave equation (traceless G^th_th - G^ps_ps) ---")
    C1 = series_A(Cwave, 1)
    C1 = sp.simplify(C1)
    # strip angular + time factor: should be (P2-ish angular)*cos(w t)*[op on H]
    # divide by cos(w t)
    C1c = sp.simplify(C1 / sp.cos(w * t))
    # collect operator on H: factor the common angular dependence
    Hrr = sp.diff(H, r, 2); Hr = sp.diff(H, r)
    a2 = sp.simplify(C1c.coeff(Hrr))
    a1 = sp.simplify(C1c.coeff(Hr))
    rem = sp.simplify(C1c - a2 * Hrr - a1 * Hr)
    a0 = sp.simplify(rem.coeff(H))
    print("  coeff H'' :", a2)
    print("  coeff H'  :", a1)
    print("  coeff H   :", a0)
    print("  remainder :", sp.simplify(rem - a0 * H))
    if a2 != 0:
        print("\n  normalized  -H'' + p1 H' + p0 H = 0 :")
        print("    p1 (=-a1/a2):", sp.simplify(-a1 / a2))
        print("    p0 (=-a0/a2):", sp.simplify(-a0 / a2))
        print("  [expect the flat l=2 spherical operator -H''-(2/r)H'+6/r^2 H=w^2 H")
        print("   since phi enters the wave eq only at O(A^2).]")

    # -----------------------------------------------------------------
    # O(A^1) l=0 TADPOLE check: time-avg of the O(A) trace sector must vanish
    # (else phi would start at O(A); C2 relax-test).
    # -----------------------------------------------------------------
    print("\n--- O(A^1) l=0 tadpole check (must be 0 => phi starts at O(A^2)) ---")
    Gtt1 = series_A(G[0, 0], 1)
    tad = time_avg(Gtt1)
    # angular average over P2 (integral of P2 d(cos) = 0)
    print("  <G_tt^(1)>_t (angular still present):", sp.simplify(tad))
    print("  [P2 angular-averages to 0; combined with <cos>=0 -> tadpole vanishes.]")

    # -----------------------------------------------------------------
    # O(A^2) l=0: the phi-SOURCE. Take G_tt at O(A^2), TIME-AVERAGE, then
    # ANGULAR-AVERAGE (project l=0). This is the constraint sourcing F(r).
    # -----------------------------------------------------------------
    print("\n--- O(A^2): l=0 phi-source (G_tt @O(A^2), time+angle averaged) ---")
    Gtt2 = series_A(G[0, 0], 2)
    Gtt2_ta = time_avg(Gtt2)
    # angular-average: integrate over solid angle / (4 pi). With axisymmetry,
    # <f>_ang = (1/2) int_{-1}^{1} f d(cos th).
    u = sp.symbols('u')  # u = cos(theta)
    Gtt2_u = Gtt2_ta.rewrite(sp.cos).subs(sp.cos(th), u).subs(sp.sin(th)**2, 1 - u**2)
    Gtt2_u = sp.expand_trig(sp.expand(Gtt2_u))
    # ensure all theta gone
    Gtt2_u = Gtt2_u.subs(sp.cos(th), u).subs(sp.sin(th), sp.sqrt(1 - u**2))
    Gtt2_ang = sp.simplify(sp.integrate(Gtt2_u, (u, -1, 1)) / 2)
    print("  l=0 projected, time-avg G_tt at O(A^2):")
    print("   ", sp.simplify(Gtt2_ang))
    Frr = sp.diff(F, r, 2); Fr = sp.diff(F, r)
    b2 = sp.simplify(Gtt2_ang.coeff(Frr))
    b1 = sp.simplify(Gtt2_ang.coeff(Fr))
    remF = sp.simplify(Gtt2_ang - b2 * Frr - b1 * Fr)
    b0 = sp.simplify(remF.coeff(F))
    src = sp.simplify(remF - b0 * F)   # pure H-source (no F): the GW stress
    print("\n  phi-equation structure  b2 F'' + b1 F' + b0 F + Src[H] = 0 :")
    print("    b2 :", b2)
    print("    b1 :", b1)
    print("    b0 :", b0)
    print("    Src[H] (the quadratic GW stress, the geon source):")
    print("      ", sp.simplify(src))

    # Also report the G_rr @ O(A^2) l=0 averaged (second constraint / check).
    print("\n--- O(A^2): l=0 from G_rr (consistency / second relation) ---")
    Grr2 = series_A(G[1, 1], 2)
    Grr2_ta = time_avg(Grr2)
    Grr2_u = Grr2_ta.rewrite(sp.cos).subs(sp.cos(th), u).subs(sp.sin(th)**2, 1 - u**2)
    Grr2_u = Grr2_u.subs(sp.cos(th), u).subs(sp.sin(th), sp.sqrt(1 - u**2))
    Grr2_ang = sp.simplify(sp.integrate(sp.expand(Grr2_u), (u, -1, 1)) / 2)
    print("  l=0 projected, time-avg G_rr at O(A^2):")
    print("   ", sp.simplify(Grr2_ang))

    print("\n" + "=" * 78)
    print("Hand the exact (a0,a1,a2) wave op and (b0,b1,b2,Src) phi-source to the")
    print("numerical solver phase1_geon_solve.py.")
    print("=" * 78)
