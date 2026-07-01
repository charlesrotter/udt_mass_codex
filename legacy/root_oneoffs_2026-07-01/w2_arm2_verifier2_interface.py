#!/usr/bin/env python3
"""
W2 ARM-2 BLIND ADVERSARIAL VERIFIER — SCRIPT 2: THE INTERFACE LAYER.
Date: 2026-06-12.  Independent machinery (own engine, own mollifiers,
exact integrals on the TRUE metric, not frozen coefficients).

ATTACKS (claims 1 and parts of 5):
 C1. Independent re-derivation of the linear-in-w_rr Riemann
     coefficients and the orthonormal +-f/(1+w) sheet strengths.
 C2. FULL Ricci census of the sheet: the arm checked Ric_rr only.
     Does the w_rr sheet appear in OTHER Ricci components (Ric_thth,
     Ric_phph) and in the scalar curvature?  (If Ric_thth carries the
     delta, the sheet is NOT source-free in the Einstein/Israel sense
     — it is a Ricci-carrying anisotropic-stress sheet, not pure Weyl.
     This feeds the attack-C adjudication on what "the metric forbids
     it" can legitimately mean without field equations.)
 C3. Kretschmann quadratic weight 8 f^2/(1+w)^2 independently; EXACT
     layer integral of K on the TRUE kinked metric (f = C + a/r
     spherical exterior, w = piecewise mollified kink) — symbolic in
     eps, NOT frozen-coefficient: confirm the 1/eps divergence and
     extract the exact constant.
 C4. MOLLIFIER DEPENDENCE of the "96": rerun with the quintic
     smoothstep; show the constant is 8 F^2/(1+w)^2 * int m''^2 and
     that the CUBIC minimizes int m''^2 (=12) over the clamped class —
     i.e. 96 is the floor, divergence is mollifier-robust.
 C5. "Even discontinuous w costs zero C1 action": independent layer
     action on the true integrand (f_theta != 0 so the w-term is
     live), including a jump PASSING NEAR w = -1 (the caveat hunt:
     the claim needs 1+w bounded away from 0 on the layer).
 C6. The C1 EL system is distributionally BLIND to the kink: EL_w is
     algebraic and vanishes on f_th = 0; EL_f's w-coupling multiplies
     f_th^2 — a kinked/discontinuous w on a spherical-f exterior IS an
     exact distributional solution of the full C1 EL system.  (This
     sharpens attack C: the metric's own field equations raise NO
     objection; only the curvature-regularity demand does.)
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th, ph = sp.symbols('T r theta phi')
xs = [T, r, th, ph]

def riem_all(gdd):
    gi = gdd.inv()
    n = 4
    Gam = [[[sp.cancel(sum(gi[a, d]*(sp.diff(gdd[d, b], xs[c])
            + sp.diff(gdd[d, c], xs[b]) - sp.diff(gdd[b, c], xs[d]))
            for d in range(n))/2) for c in range(n)] for b in range(n)]
           for a in range(n)]
    Rud = [[[[sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
              + sum(Gam[a][e][c]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][c]
                    for e in range(n)) for d in range(n)]
             for c in range(n)] for b in range(n)] for a in range(n)]
    Rdd = [[[[sum(gdd[a, e]*Rud[e][b][c][d] for e in range(n))
              for d in range(n)] for c in range(n)] for b in range(n)]
           for a in range(n)]
    return gi, Rud, Rdd

fr_ = sp.Function('f')(r); wr_ = sp.Function('w')(r)
g = sp.diag(-fr_, 1/fr_, r**2*(1 + wr_)**2,
            r**2*sp.sin(th)**2/(1 + wr_)**2)
gi, Rud, Rdd = riem_all(g)
w2 = sp.Derivative(wr_, (r, 2))

# C1: linear coefficients
co_th = sp.simplify(sp.diff(Rdd[1][2][1][2], w2))
co_ph = sp.simplify(sp.diff(Rdd[1][3][1][3], w2))
check("C1a", sp.simplify(co_th + r**2*(1 + wr_)) == 0 and
      sp.simplify(co_ph - r**2*sp.sin(th)**2/(1 + wr_)**3) == 0,
      "dR_{r th r th}/dw_rr = -r^2(1+w); dR_{r ph r ph}/dw_rr = "
      "+r^2 sin^2 th/(1+w)^3 (independent engine)")
nonlin = any(sp.diff(Rdd[a][b][c][d], w2, 2) != 0
             for a in range(4) for b in range(4)
             for c in range(4) for d in range(4))
check("C1b", not nonlin, "w_rr enters every Riemann component linearly")
on_th = sp.simplify(co_th*fr_/(r**2*(1 + wr_)**2))
on_ph = sp.simplify(co_ph*fr_*(1 + wr_)**2/(r**2*sp.sin(th)**2))
check("C1c", sp.simplify(on_th + fr_/(1 + wr_)) == 0 and
      sp.simplify(on_ph - fr_/(1 + wr_)) == 0,
      "orthonormal sheet strengths -+ f/(1+w): equal-and-opposite "
      "(trace-free pair) confirmed")

# C2: FULL Ricci + scalar census (the arm checked Ric_rr only)
Ric = [[sp.together(sum(Rud[e][a][e][b] for e in range(4)))
        for b in range(4)] for a in range(4)]
ric_w2 = {(a, b): sp.simplify(sp.diff(Ric[a][b], w2))
          for a in range(4) for b in range(4)
          if sp.diff(Ric[a][b], w2) != 0}
print("   Ricci components carrying w_rr:",
      {k: sp.simplify(v) for k, v in ric_w2.items()})
check("C2a", sp.simplify(sp.diff(Ric[1][1], w2)) == 0,
      "Ric_rr blind to w_rr (arm's check reproduced)")
co_thth = sp.simplify(sp.diff(Ric[2][2], w2))
co_phph = sp.simplify(sp.diff(Ric[3][3], w2))
check("C2b", sp.simplify(co_thth + fr_*(1 + wr_)*r**2) == 0 and
      sp.simplify(co_phph - fr_*r**2*sp.sin(th)**2/(1 + wr_)**3) == 0,
      "BUT Ric_thth and Ric_phph DO carry the w_rr delta: "
      "dRic_thth/dw_rr = -f r^2 (1+w), dRic_phph/dw_rr = "
      "+f r^2 sin^2 th/(1+w)^3 — the sheet is RICCI-CARRYING "
      "(anisotropic-stress species, NOT pure Weyl). In GR/Israel terms "
      "a vacuum w_r-kink would be FORBIDDEN BY THE FIELD EQUATIONS; "
      "here no field equation exists in this channel (C6), so the "
      "arm's 'pure-shear sheet' wording is about the Riemann pair "
      "only, and the load is carried entirely by the curvature-"
      "regularity demand")
Rsc = sp.simplify(sum(gi[a, a]*Ric[a][a] for a in range(4)))
check("C2c", sp.simplify(sp.diff(Rsc, w2)) == 0,
      "scalar curvature R is w_rr-BLIND (orthonormal theta/phi Ricci "
      "deltas cancel in the trace): the sheet is trace-free, "
      "delta-R = 0 — so even an R-based density would not see it")

# C3: K quadratic weight + EXACT layer integral on the TRUE metric
K = sp.Integer(0)
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                t1 = Rdd[a][b][c][d]
                if t1 == 0:
                    continue
                K += t1**2*gi[a, a]*gi[b, b]*gi[c, c]*gi[d, d]
co_K = sp.cancel(sp.together(sp.diff(K, w2, 2)/2))
check("C3a", sp.simplify(co_K - 8*fr_**2/(1 + wr_)**2) == 0,
      "K contains 8 f^2/(1+w)^2 w_rr^2 (independent engine)")
# STRUCTURAL quadraticity: every Riemann component is linear in w_rr
# (C1b) and every inverse-metric weight is w_rr-free, so K = K0 +
# K1 w_rr + K2 w_rr^2 EXACTLY with K2 = co_K:
check("C3s", all(not gi[i, i].has(w2) for i in range(4)),
      "inverse-metric weights are w_rr-free => K is EXACTLY quadratic "
      "in w_rr (with C1b); decomposition K0 + K1 w_rr + K2 w_rr^2")
K1 = sp.diff(K, w2).subs(w2, 0)
# exact layer integral on the true kinked metric: f = C + a/r,
# w = k*eps*m(s), s = (r-r0)/eps, cubic mollifier; dr = eps ds;
# w_rr = (k/eps) m''(s):
#   K2-term: int K2 (k/eps)^2 m''^2 eps ds = (k^2/eps) int K2 m''^2 ds
#   K1-term: int K1 (k/eps) m'' eps ds   = k int K1 m'' ds = O(1)
#   K0-term: O(eps).
# Leading order needs the eps -> 0 layer value of K2 and finiteness of
# K1 on the layer — both computed EXACTLY at a rational point:
Cs, am, kk, eps, r0 = sp.symbols('C a_m k epsilon r0', positive=True)
s = sp.Symbol('s')
m_cub = 3*s**2 - 2*s**3
Rt = sp.Rational
bg = {Cs: Rt(6, 5), am: Rt(3, 7), r0: Rt(2), th: sp.pi/3}
fex = (Cs + am/r).subs(bg)
layer_sub = {
    sp.Derivative(fr_, (r, 2)): sp.diff(fex, r, 2),
    sp.Derivative(fr_, r): sp.diff(fex, r), fr_: fex,
    sp.Derivative(wr_, r): kk*sp.diff(m_cub, s),   # w_r = k m'(s)
    wr_: kk*eps*m_cub}
K2_layer = sp.cancel(co_K.xreplace(layer_sub).subs(r, r0 + eps*s)
                     .subs(bg))
K2_lim = sp.cancel(K2_layer.subs(eps, 0))
F0v = fex.subs(r, r0).subs(bg)
check("C3b", sp.simplify(K2_lim - 8*F0v**2) == 0,
      "eps -> 0 layer value of K2 on the TRUE kinked metric (radial "
      "f-dependence live) = 8 f(r0)^2 exactly")
lead = sp.integrate(K2_lim*sp.diff(m_cub, s, 2)**2, (s, 0, 1))*kk**2
pred = 96*F0v**2*kk**2
check("C3c", sp.simplify(lead - pred) == 0,
      f"leading layer integral = (k^2/eps) int K2 m''^2 ds = "
      f"96 f(r0)^2 k^2/eps (= {pred}/eps at the rational point): the "
      f"1/eps divergence and the arm's constant confirmed on the true "
      f"metric (frozen-coefficient step validated)")
K1_layer = sp.cancel(sp.together(K1.xreplace(layer_sub)
                     .subs(r, r0 + eps*s).subs(bg)))
K1_lim = sp.cancel(K1_layer.subs(eps, 0))
check("C3d", K1_lim.subs([(s, Rt(1, 3)), (kk, Rt(2, 7))]).is_finite,
      "the linear-in-w_rr layer term is FINITE at eps -> 0 (its "
      "contribution is O(1), subleading): no hidden divergence beats "
      "or cancels the quadratic one")

# C4: mollifier dependence of the constant; cubic minimality
m_qui = 6*s**5 - 15*s**4 + 10*s**3
i_cub = sp.integrate(sp.diff(m_cub, s, 2)**2, (s, 0, 1))
i_qui = sp.integrate(sp.diff(m_qui, s, 2)**2, (s, 0, 1))
check("C4a", i_cub == 12 and sp.simplify(i_qui - sp.Rational(120, 7)) == 0,
      f"int m''^2: cubic = 12, quintic = 120/7 (~17.14): the '96' = "
      f"8*12 is MOLLIFIER-SPECIFIC; the quintic kink gives 960/7 "
      f"(~137) — the LAW is int K ~ [8 F^2/(1+w)^2 int m''^2] "
      f"[w_r]^2/eps, constant not universal")
# cubic minimizes int m''^2 over m(0)=0, m(1)=1, m'(0)=m'(1)=0:
# EL of int m''^2 is m'''' = 0 -> cubic; verify by perturbation:
tdv = sp.Symbol('t')
pert = s**2*(1 - s)**2          # vanishes with derivative at both ends
i_pert = sp.integrate(sp.diff(m_cub + tdv*pert, s, 2)**2, (s, 0, 1))
check("C4b", sp.simplify(sp.diff(i_pert, tdv).subs(tdv, 0)) == 0 and
      sp.simplify(sp.diff(i_pert, tdv, 2)) > 0,
      "the cubic is the STRICT MINIMIZER of int m''^2 in the clamped "
      "class (first variation 0, second variation > 0): 96 F^2 [w_r]^2"
      "/((1+w)^2 eps) is the FLOOR over mollifiers — the divergence "
      "claim is mollifier-robust (strengthens the arm's I-2f)")

# C5: layer action with the TRUE integrand, w-term live (f_th != 0)
c = sp.Symbol('c')
F0, Fth, w0, J = sp.symbols('F0 F_theta w0 J', positive=True)
# C1 density angular part on the layer with w = -1 + delta + J*s
# (jump passing NEAR the singular shape w = -1): delta -> 0 limit:
delta = sp.Symbol('delta', positive=True)
integ = Fth**2/(F0*(-1 + delta + J*s + 1)**2)   # 1/(delta + J s)^2
S_lay = sp.integrate(-(c/8)*sp.sin(th)*integ*eps, (s, 0, 1))
S_fin = sp.simplify(S_lay)
lim_eps = sp.limit(S_fin, eps, 0)
lim_delta = sp.limit(S_fin/eps, delta, 0)
check("C5b", sp.simplify(lim_eps) == 0,
      "w-JUMP through the layer at FIXED offset from w = -1: layer "
      "action -> 0 with eps (claim 1c reproduced on the live "
      "integrand)")
check("C5c", any(lim_delta.has(x) for x in (sp.oo, -sp.oo, sp.zoo)),
      f"CAVEAT FOUND: if the jump path TOUCHES w = -1 the per-eps "
      f"layer action diverges (got {lim_delta}); 'even discontinuous "
      f"w costs zero action' requires 1 + w bounded away from 0 on "
      f"the layer — an unstated premise of I-1c (minor, but should "
      f"be recorded)")

# C6: the kinked configuration is an exact distributional solution
fq = sp.Function('f')(r, th); wq = sp.Function('w')(r, th)
L = -(c/8)*sp.sin(th)*(r**2*sp.diff(fq, r)**2
    + sp.diff(fq, th)**2/(fq*(1 + wq)**2))
EL_w = sp.diff(L, wq)
check("C6a", sp.simplify(EL_w - (c/4)*sp.sin(th)*sp.diff(fq, th)**2
      / (fq*(1 + wq)**3)) == 0 and
      [d for d in L.atoms(sp.Derivative) if d.expr == wq] == [],
      "EL_w is ALGEBRAIC, proportional to f_th^2: vanishes "
      "identically on spherical f for ANY w — kinked, even "
      "discontinuous w solves the w-equation exactly")
pith = sp.diff(L, sp.Derivative(fq, th))
check("C6b", sp.simplify(pith + (c/4)*sp.sin(th)*sp.diff(fq, th)
      / (fq*(1 + wq)**2)) == 0,
      "pi_f^theta carries the w-dressing ONLY multiplied by f_th: "
      "on spherical f the f-equation never sees w — the kinked "
      "configuration is an EXACT DISTRIBUTIONAL SOLUTION of the "
      "full C1 EL system. The metric's own field equations raise "
      "no objection to the kink; ONLY the (unbanked) curvature-"
      "integrability demand does. [attack-C input]")

print(f"\nVERIFIER-2 (interface): {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
