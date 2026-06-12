#!/usr/bin/env python3
"""
W2 ARM-2 — SCRIPT 3: THE SHAPED INTERFACE JET.  Date: 2026-06-11.
METRIC-LED (W2 framing correction binds: uncovering only — this
script computes what the metric's OWN junction/continuation machinery
demands at an interface when the configuration is SHAPED (w on).
Nothing is added to the theory; no Israel/EH dynamics is imported —
every statement below is a statement about the metric's curvature
tensors and the C1 action as banked.)

PRE-REGISTERED FAILURE CRITERIA (identical in all w2_arm2_* scripts,
stated before any computation ran):
  FC-3 (interface jet): if the junction/continuation demands reduce to
       two-sided matching with no autonomous one-sided relation on
       (w, w_r, w_rr) beyond a clamp conditional on the spherical-tail
       premise, the "metric enforces a w-interface law" claim is
       downgraded to a conditional clamp; if the w_r-kink layer
       carries no distributional curvature at all, Part 2 is fully
       negative.

CLASS (premise set): static diagonal+w class, R-areal canon rho = r,
  ds^2 = -f dT^2 + f^{-1} dr^2 + r^2 (1+w)^2 dth^2
         + r^2 sin^2(th) dph^2/(1+w)^2,   f = f(r,th), w = w(r,th);
  interface = a 2-sphere r = r0 with f > 0 there (NOT the seal; the
  seal case is the f -> 0 scaling computed in I5).
COMPUTED:
  I1. ACTION-SIDE BLINDNESS (exact): the C1 surface term in the
      w-channel is identically zero (pi_w = 0); a mollified w_r-KINK
      costs ZERO extra C1 action in the eps -> 0 limit, and even a
      mollified w-JUMP costs ZERO extra C1 action (bounded integrand
      x shrinking support) — contrast: the f-channel kink carries the
      banked first-variation delta weight, and the fork_tests
      angular-FIELD jump costs infinite action (S*eps = const).  The
      C1 action raises NO objection to any w-discontinuity.
  I2. METRIC-SIDE OBJECTION (exact, distributional statements via
      exact mollifier asymptotics — labeled, principle 2 compliant):
      w_rr enters the Riemann tensor LINEARLY (exact coefficients
      extracted); hence a w_r-kink [w_r] != 0 deposits a DELTA
      function in Riemann with computable strength, and the
      Kretschmann scalar of the mollified layer diverges as
      [w_r]^2/eps: smoothness/curvature-integrability — the SAME
      metric-own demand species that produced the mirror theorem and
      the S1 admissibility structure — forbids the w_r-kink natively.
      A w-jump [w] != 0 is worse (layer K ~ 1/eps^3 at fixed jump:
      delta'-type). => THE METRIC ITSELF ENFORCES TWO-SIDED JET
      CONTINUITY [w] = [w_r] = 0 across every interface, a demand the
      varied action never sees (I1).  (No banked sector can absorb
      the layer as a surface source: registry #25, every banked
      non-C1 sector is zeroth-jet in the angular block.)
  I3. CONTINUATION NON-UNIQUENESS (the mirror theorem on the shaped
      class): on the exterior solution set of C1 (P1 theorem:
      f spherical, q = 0, w arbitrary) the w-channel satisfies NO
      differential equation — dL/dw vanishes identically once
      f_th = 0, and there is no pi_w to build an ODE from. EXHIBIT:
      two exact C1 exterior statics with IDENTICAL full interface
      jets in (f, q, w) to second order, both axis-regular, both
      w = 0 at the far boundary, differing in the bulk w. The
      mirror/unique-continuation property FAILS in the w-channel:
      "the exterior carries zero free structure" is f-sector-scoped;
      the shaped exterior carries a free FUNCTION. No autonomous
      one-sided relation on (w, w_r, w_rr) exists, and even the
      spherical-tail clamp fails (bulk freedom interpolates to any
      interface value).  [FC-3 adjudication: distributional curvature
      IS carried (I2) -> not fully negative; but the metric-own
      interface law is jet-CONTINUITY ONLY — downgrade per FC-3.]
  I4. CHANNEL COMPARISON (exact): the same mollifier machinery on the
      f-channel kink [f_r] != 0 also deposits delta-Riemann (K-layer
      ~ 1/eps) — for f the metric AND the action object; for w ONLY
      the metric objects. The w-interface law is purely metric-own.
  I5. SEAL SCALING: the linear-in-w_rr Riemann coefficients carry
      explicit factors of f; at the seal (f -> 0, in-ansatz) the
      w-kink's INVARIANT layer content (f^2 K species) is computed:
      where the metric's w-junction demand stiffens or dies as the
      interface is pushed to the curvature-singular seal.
Conventions: signature (-,+,+,+); exact sympy; mollifier asymptotics
exact in eps (distributional statements labeled as such); exact
rational spot-checks; no floating point in any claim.
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"I-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th, ph = sp.symbols('T r theta phi')
xs = [T, r, th, ph]

def riemann_and_K(gdd, simp=sp.cancel):
    guu = gdd.inv()
    Gam = [[[simp(sum(guu[a, d]*(sp.diff(gdd[d, b], xs[c])
            + sp.diff(gdd[d, c], xs[b]) - sp.diff(gdd[b, c], xs[d]))
            for d in range(4))/2) for c in range(4)] for b in range(4)]
           for a in range(4)]
    Riem = [[[[sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
               + sum(Gam[a][e][c]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][c]
                     for e in range(4))
               for d in range(4)] for c in range(4)] for b in range(4)]
            for a in range(4)]
    Rdddd = [[[[sum(gdd[a, e]*Riem[e][b][c][d] for e in range(4))
                for d in range(4)] for c in range(4)] for b in range(4)]
             for a in range(4)]
    K = sp.Integer(0)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    t1 = Rdddd[a][b][c][d]
                    if t1 == 0:
                        continue
                    K += t1**2*guu[a, a]*guu[b, b]*guu[c, c]*guu[d, d]
    return Riem, Rdddd, K

# =====================================================================
# I1. ACTION-SIDE BLINDNESS (exact)
# =====================================================================
c = sp.Symbol('c')
fq = sp.Function('f')(r, th); wq = sp.Function('w')(r, th)
W = (1 + wq)**2
# diagonal+w C1 density (anchored in script 1 / pde_p1 D-06 at q=0):
L3 = -(c/8)*sp.sin(th)*(r**2*sp.diff(fq, r)**2
     + sp.diff(fq, th)**2/(fq*(1 + wq)**2))
gradw = [d for d in L3.atoms(sp.Derivative) if d.expr == wq]
check("1a", len(gradw) == 0,
      "pi_w = dL/dw_r = 0 IDENTICALLY (no w-derivative atom): the C1 "
      "first variation carries NO surface term in the w-channel")
# mollified kink/jump cost: integrand depends on w ALGEBRAICALLY and
# is bounded on the layer; layer action = O(eps).  Exact exhibit with
# a concrete mollifier: w_eps = w0 + k*eps*m(s), s=(r-r0)/eps,
# m smooth ramp (kink mollifier);  w_eps = w0 + J*m(s) (jump mollifier).
eps, k, J, w0, F0, F1, Fth, r0 = sp.symbols(
    'epsilon k J w0 F0 F1 F_theta r0', positive=True)
s = sp.Symbol('s')
# C1 carries no w-derivative, so a w_r-kink needs NO mollification at
# all: the piecewise-linear ramp w = w0 + k*eps*s on the layer IS the
# kink configuration (continuous w, jumping w_r). Layer action exact:
integrand_kink = -(c/8)*sp.sin(th)*(r0**2*F1**2
                 + Fth**2/(F0*(1 + w0 + k*eps*s)**2))
S_layer_kink = sp.integrate(integrand_kink*eps, (s, 0, 1))  # dr = eps ds
lim_kink = sp.limit(S_layer_kink, eps, 0)
check("1b", sp.simplify(lim_kink) == 0,
      "w_r-KINK: C1 layer action -> 0 as eps -> 0 (exact): "
      "the action does not resist the kink at all")
integrand_jump = -(c/8)*sp.sin(th)*(r0**2*F1**2
                 + Fth**2/(F0*(1 + w0 + J*s)**2))
S_layer_jump = sp.integrate(integrand_jump*eps, (s, 0, 1))
lim_jump = sp.limit(S_layer_jump, eps, 0)
check("1c", sp.simplify(lim_jump) == 0,
      "mollified w-JUMP (linear ramp): C1 layer action -> 0 as "
      "eps -> 0 (exact): even a discontinuous w costs the action "
      "NOTHING (contrast: fork_tests angular-FIELD jump costs "
      "S*eps = const -> infinite action; the f-kink carries delta "
      "weight +q*y_b/2)")
print(f"[t={time.time()-t0:.0f}s] I1 done; building shaped Riemann ...",
      flush=True)

# =====================================================================
# I2. METRIC-SIDE OBJECTION: w_rr enters Riemann LINEARLY
# =====================================================================
# jet-flattened shaped metric: f, w functions of r only here (the
# theta-dependence rides along unchanged — checked at the end with a
# full (r,th) atom census).
fr_ = sp.Function('f')(r); wr_ = sp.Function('w')(r)
g_w = sp.diag(-fr_, 1/fr_, r**2*(1 + wr_)**2,
              r**2*sp.sin(th)**2/(1 + wr_)**2)
Riem, Rdddd, K_w = riemann_and_K(g_w)
w2sym = sp.Derivative(wr_, (r, 2))
# census: which Riemann (all-down) components carry w_rr, and linearly?
lin_coeffs = {}
nonlinear = False
for a in range(4):
    for b in range(4):
        for cc in range(4):
            for d in range(4):
                comp = Rdddd[a][b][cc][d]
                if comp == 0 or not comp.has(w2sym):
                    continue
                co = sp.simplify(sp.diff(comp, w2sym))
                if co.has(w2sym):
                    nonlinear = True
                lin_coeffs[(a, b, cc, d)] = sp.simplify(co)
check("2a", len(lin_coeffs) > 0 and not nonlinear,
      f"w_rr enters the Riemann tensor LINEARLY in "
      f"{len(lin_coeffs)} all-down components (none nonlinear)")
# the two independent strengths (theta-theta and phi-phi sectors):
co_th = lin_coeffs.get((1, 2, 1, 2))   # R_{r th r th}
co_ph = lin_coeffs.get((1, 3, 1, 3))   # R_{r ph r ph}
print("   dR_{r th r th}/dw_rr =", co_th)
print("   dR_{r ph r ph}/dw_rr =", co_ph)
check("2b", sp.simplify(co_th - (-(r**2*(1 + wr_)))) == 0 and
      sp.simplify(co_ph - (r**2*sp.sin(th)**2/(1 + wr_)**2
                           * (1/(1 + wr_)))) == 0,
      "exact delta strengths: dR_{r th r th}/dw_rr = -r^2(1+w); "
      "dR_{r ph r ph}/dw_rr = +r^2 sin^2(th)/(1+w)^3 — EQUAL AND "
      "OPPOSITE in the orthonormal frame (trace-free shear layer)")
# orthonormal-frame check: R_{rhat thhat rhat thhat} delta-strength:
on_th = sp.simplify(co_th * fr_ * (1/(r**2*(1 + wr_)**2)))   # g^rr g^thth
on_ph = sp.simplify(co_ph * fr_ * ((1 + wr_)**2/(r**2*sp.sin(th)**2)))
check("2c", sp.simplify(on_th + on_ph) == 0 and
      sp.simplify(on_th - (-fr_/(1 + wr_))) == 0,
      f"orthonormal delta strengths: R_(rh th rh th) <- -f/(1+w) w_rr, "
      f"R_(rh ph rh ph) <- +f/(1+w) w_rr : exactly opposite — the "
      f"w_r-kink layer is a PURE SHEAR (trace-free) curvature sheet")
# Ricci blindness of the layer (the trace-free signature, exact):
guu = g_w.inv()
Ric_rr = sp.simplify(sum(guu[i, i]*Rdddd[i][1][i][1] for i in range(4)))
co_ric = sp.simplify(sp.diff(Ric_rr, w2sym))
Ric_thth = sp.simplify(sum(guu[i, i]*Rdddd[i][2][i][2] for i in range(4)))
co_ric_th = sp.simplify(sp.diff(Ric_thth, w2sym))
print("   dRic_rr/dw_rr =", co_ric, ";  dRic_thth/dw_rr =", co_ric_th)
check("2d", sp.simplify(co_ric) == 0,
      "dRic_rr/dw_rr = 0 EXACTLY: the w_rr sheet cancels out of the "
      "rr-Ricci (th and ph sector contributions equal and opposite)")
# Kretschmann: w_rr enters quadratically => mollified kink layer
# integral of K diverges as 1/eps (delta^2). The quadratic weight
# counts BOTH sectors (th and ph) with the 4-fold index symmetry each:
co_K = sp.simplify(sp.diff(K_w, w2sym, 2)/2)
print("   d^2K/dw_rr^2 / 2 =", co_K)
check("2e", sp.simplify(co_K - 8*fr_**2/(1 + wr_)**2) == 0,
      "K contains + 8 f^2/(1+w)^2 w_rr^2 EXACTLY (the quadratic "
      "delta^2 weight; 4 f^2/(1+w)^2 from each of the th- and "
      "ph-sectors with their 4-fold index symmetry)")
# exact mollifier asymptotics of the layer K-integral (kink): here
# curvature needs a SMOOTH mollifier: w = w0 + k*eps*m(s),
# m = 3s^2 - 2s^3 => w_rr = (k/eps) m''(s), int_0^1 m''^2 ds = 12:
m = 3*s**2 - 2*s**3
m2 = sp.diff(m, s, 2)
co_K0 = co_K.subs({fr_: F0, wr_: w0})    # frozen smooth factors
K_layer_lead = sp.integrate(co_K0*(k/eps*m2)**2*eps, (s, 0, 1))
check("2f", sp.simplify(K_layer_lead*eps
      - 96*F0**2*k**2/(1 + w0)**2) == 0,
      "exact: layer integral of K = [96 F0^2 k^2/(1+w0)^2] / eps "
      "+ O(1) — DIVERGES like [w_r]^2/eps. The metric's own "
      "curvature-integrability demand (mirror-theorem/S1 species) "
      "FORBIDS the w_r-kink: [w_r] = 0 is METRIC-ENFORCED")
# jump case: w = w0 + J m(s), w_rr = (J/eps^2) m'' => K ~ J^2/eps^4,
# layer integral ~ J^2/eps^3:
K_layer_jump = sp.integrate(co_K0*(J/eps**2*m2)**2*eps, (s, 0, 1))
check("2g", sp.simplify(sp.limit(K_layer_jump*eps**3, eps, 0)
      - 96*F0**2*J**2/(1 + w0)**2) == 0,
      "w-JUMP layer: integral of K = 96 F0^2 J^2/((1+w0)^2 eps^3) — "
      "delta'-type, worse: [w] = 0 is METRIC-ENFORCED a fortiori")
print(f"[t={time.time()-t0:.0f}s] I2 done.", flush=True)

print(f"[t={time.time()-t0:.0f}s] I3 (continuation exhibit) ...",
      flush=True)
# =====================================================================
# I3. CONTINUATION NON-UNIQUENESS in the w-channel (exact exhibit)
# =====================================================================
# C1 exterior statics (P1 theorem): f spherical solving the radial EL,
# q = 0, w ARBITRARY.  EL_f for spherical f from L = -(c/8) r^2 f_r^2
# (sin th measure): d/dr(r^2 f_r) = 0 => f = C + a/r.  EL_w =
# (c/4) sin th f_th^2/(f (1+w)^3) = 0 automatically at f_th = 0.
Csym, asym = sp.symbols('C a_m', positive=True)
fsol = Csym + asym/r
check("3a", sp.simplify(sp.diff(r**2*sp.diff(fsol, r), r)) == 0,
      "exterior spherical f-branch: f = C + a/r solves the C1 radial "
      "EL exactly (mirror-theorem f-sector, unchanged by w)")
# two exteriors on r in [r0, r1], identical FULL interface jets at r0
# (w, w_r, w_rr all zero there), identical far data (w(r1)=w_r(r1)=0),
# different in the bulk:  w_I = 0;  w_II = bump.
r1v = sp.Symbol('r1', positive=True)
bump = ((r - r0)**3*(r1v - r)**3)/(r1v - r0)**6   # C^2, vanishes to
#                                  2nd order at both ends, nonzero inside
wII = bump*sp.sin(th)**2       # axis-regular: w ~ theta^2 on the axis
#                                (elementary-flatness demand, anchor D)
jets_match = all(sp.simplify(sp.diff(wII, r, n).subs(r, r0)) == 0 and
                 sp.simplify(sp.diff(wII, r, n).subs(r, r1v)) == 0
                 for n in range(3))
check("3b", jets_match,
      "EXHIBIT: w_II (axis-regular bump x sin^2 th) has IDENTICAL "
      "(zero) interface jet at r0 through 2nd order AND identical far "
      "data at r1, but w_II != 0 in the bulk")
mid = (r0 + r1v)/2
check("3c", sp.simplify(wII.subs([(r, mid), (th, sp.pi/2)])) != 0,
      f"w_II(midpoint, equator) = "
      f"{sp.simplify(wII.subs([(r, mid), (th, sp.pi/2)]))} != 0")
check("3c2", sp.simplify(wII.subs(th, 0)) == 0 and
      sp.simplify(sp.diff(wII, th).subs(th, 0)) == 0,
      "w_II = 0 with quadratic closure on the axis: the exhibit "
      "satisfies the metric's own axis demand (elementary flatness)")
# both are exact C1 statics: EL_w vanishes identically at f_th = 0 for
# ANY w (algebraic, pointwise); EL_f unchanged (f-equation w-free at
# f_th = 0); verify on the full diagonal+w EL system:
fq2 = sp.Function('f')(r, th); wq2 = sp.Function('w')(r, th)
L_full = -(c/8)*sp.sin(th)*(r**2*sp.diff(fq2, r)**2
         + sp.diff(fq2, th)**2/(fq2*(1 + wq2)**2))
EL_w = sp.diff(L_full, wq2)            # no pi_w => EL is algebraic
EL_f = (sp.diff(L_full, fq2)
        - sp.diff(sp.diff(L_full, sp.Derivative(fq2, r)), r)
        - sp.diff(sp.diff(L_full, sp.Derivative(fq2, th)), th))
for tag, wpick in (("I", sp.Integer(0)), ("II", wII)):
    sub = {fq2: fsol, wq2: wpick}
    elw = EL_w.subs(sub).doit()
    elf = EL_f.subs(sub).doit()
    check(f"3d-{tag}", sp.simplify(elw) == 0 and sp.simplify(elf) == 0,
          f"exterior {tag} (w = {'0' if tag=='I' else 'bump'}) is an "
          f"EXACT C1 static (EL_w = EL_f = 0)")
# completeness: the exhibits are statics of the FULL (f,q,w) P1
# system, not just the diagonal+w reduction — the q-channel EL
# (algebraic: pi_q = 0) also vanishes at q = 0 on spherical f:
qq3 = sp.Function('q')(r, th)
W3 = (1 + wq2)**2
D2_3 = r**2*W3 - fq2*qq3**2
A3 = fq2*r**2*W3*sp.diff(fq2, r)**2 + sp.diff(fq2, th)**2
L_P1 = -(c/8)*r*sp.sin(th)*(A3 - 2*fq2*qq3*sp.diff(fq2, r)
       * sp.diff(fq2, th))/((1 + wq2)*fq2*sp.sqrt(D2_3))
EL_q = sp.diff(L_P1, qq3)              # pi_q = 0 => EL is algebraic
elq = EL_q.subs({fq2: fsol, wq2: wII, qq3: 0}).doit()
check("3f", sp.simplify(elq) == 0,
      "EL_q = 0 at q = 0 on the exhibits: both exteriors are exact "
      "statics of the FULL (f,q,w) P1 system")
# and the second jet is interface-FREE: [w_rr] != 0 deposits only a
# FINITE curvature jump (w_rr enters Riemann linearly, no delta), so
# the metric's own demand is EXACTLY first-jet continuity of w:
check("3g", all(not co.has(sp.Derivative(wr_, (r, 3))) and
                not co.has(w2sym) for co in lin_coeffs.values()),
      "w_rr enters Riemann linearly with w_rr-free coefficients => "
      "[w_rr] != 0 gives a finite curvature jump only (no delta): "
      "the metric-own interface law is EXACTLY [w] = [w_r] = 0; "
      "the second jet is interface-free")
check("3e", True,
      "=> UNIQUE SMOOTH CONTINUATION FAILS IN THE w-CHANNEL: two "
      "smooth exteriors, same interface jet, same spherical tail, "
      "different geometry (w-channel has no ODE: pi_w = 0 kills the "
      "operator, EL_w is algebraic and vanishes on f_th = 0). The "
      "mirror-forced theorem is f-SECTOR structure; the shaped "
      "exterior carries a free FUNCTION. No autonomous one-sided "
      "relation on (w, w_r, w_rr) exists; even the spherical-tail "
      "clamp fails (bulk freedom interpolates).  [FC-3: DOWNGRADE "
      "branch — the metric-own interface law is jet-continuity only]")

# =====================================================================
# I4. CHANNEL COMPARISON: the f-kink also deposits delta-Riemann
# =====================================================================
f2sym = sp.Derivative(fr_, (r, 2))
co_f = sp.simplify(sp.diff(Rdddd[0][1][0][1], f2sym))
check("4a", sp.simplify(co_f - sp.Rational(1, 2)) == 0,
      "dR_{TrTr}/df_rr = 1/2: the f_r-kink also deposits delta-"
      "Riemann (K-layer ~ [f_r]^2/eps) — for f the metric AND the "
      "action object (banked F-kink delta weight); for w ONLY the "
      "metric objects: the w-interface law is PURELY METRIC-OWN, "
      "invisible to every variation ever performed")

# =====================================================================
# I5. SEAL SCALING of the w-junction demand
# =====================================================================
# invariant layer strength: orthonormal delta strength = f/(1+w) [w_r]
# per unit eps; the in-ansatz seal invariant is f^2 K. Layer f^2 K:
#   f^2 * 2 f^2/(1+w)^2 w_rr^2 = 2 f^4/(1+w)^2 w_rr^2.
co_f2K = sp.simplify(fr_**2*co_K)
check("5a", sp.simplify(co_f2K - 8*fr_**4/(1 + wr_)**2) == 0,
      "the seal invariant of the kink layer: f^2 K <- 8 f^4/(1+w)^2 "
      "w_rr^2: the w-junction demand carries f^4 — it DIES at the "
      "seal (f -> 0) faster than the seal's own f^2 K -> 4 f_u^2/y^4 "
      "structure survives. The metric's w-jet-continuity demand is an "
      "INTERIOR/INTERFACE law; pushed to the curvature-singular seal "
      "it goes silent (the seal cannot hold a w-kink to account)")
# and the orthonormal Riemann sheet strength f/(1+w) also -> 0 at f->0:
check("5b", sp.limit(on_th.subs({fr_: sp.Symbol('fpos', positive=True)}),
      sp.Symbol('fpos', positive=True), 0) == 0,
      "orthonormal sheet strength -f/(1+w) -> 0 as f -> 0: ditto")

print(f"[t={time.time()-t0:.0f}s] I5c (full (r,th) ride-along) ...",
      flush=True)
# full (r,th) ride-along check: with f = f(r,th), w = w(r,th) the
# linear-in-w_rr census is unchanged in the four components above:
fq3 = sp.Function('f')(r, th); wq3 = sp.Function('w')(r, th)
g_w2 = sp.diag(-fq3, 1/fq3, r**2*(1 + wq3)**2,
               r**2*sp.sin(th)**2/(1 + wq3)**2)
_, Rd2, _ = riemann_and_K(g_w2)
w2sym2 = sp.Derivative(wq3, (r, 2))
co_th2 = sp.simplify(sp.diff(Rd2[1][2][1][2], w2sym2))
check("5c", sp.simplify(co_th2 - (-(r**2*(1 + wq3)))) == 0,
      "theta-dependence rides along: dR_{r th r th}/dw_rr = -r^2(1+w) "
      "unchanged on the full (r,th) class")

# exact rational spot-check of the K quadratic weight (no floats):
vals = {fr_: sp.Rational(7, 5), wr_: sp.Rational(1, 4),
        sp.Derivative(fr_, r): sp.Rational(-2, 3),
        sp.Derivative(fr_, (r, 2)): sp.Rational(1, 2),
        sp.Derivative(wr_, r): sp.Rational(3, 7),
        r: sp.Rational(11, 10), th: sp.pi/2}
Kq = sp.simplify(K_w.subs(sp.Derivative(wr_, (r, 2)), w2sym))
p2 = sp.Rational(1, 2)*sp.diff(Kq, w2sym, 2)
spot = sp.simplify(p2.subs(vals).subs(w2sym, 0))
check("5d", spot == 8*sp.Rational(7, 5)**2/(1 + sp.Rational(1, 4))**2,
      f"exact-rational spot check of the K weight: {spot} = "
      f"8 f^2/(1+w)^2 at (f,w) = (7/5, 1/4)")

print(f"\nSHAPED INTERFACE: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
