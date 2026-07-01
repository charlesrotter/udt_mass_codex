#!/usr/bin/env python3
"""
W2 ARM-2 BLIND ADVERSARIAL VERIFIER — SCRIPT 1: K_axis AND THE SEAL LAW.
Date: 2026-06-11.  Verifier agent (independent machinery; no code shared
with the w2_arm2_* scripts beyond sympy itself).

ATTACKS:
 A1. The +4 coefficient and the convention chain om = w_thth(pole):
     independent GAUSS-EQUATION route — pole Gauss curvature of the
     shaped 2-sphere computed from the 2D first-fundamental-form
     formula (no 4D engine), then the Gauss equation
     K_intrinsic = R_(th ph th ph)^(4) + K_th K_ph (extrinsic products)
     re-derives the claimed unique w-jet carrier component.
 A2. INDEPENDENT LIMIT METHOD #1 (the arm used gcd-free trailing-
     coefficient limits): per-term sympy SERIES in v = 1-u to order 1.
     A divergent term silently zeroed by the arm's tN>=tD logic would
     appear here as a v^(-n) pole.  A kept symbolic -> exact K_axis(A)
     -> Laurent in A via series: singular order and law coefficient.
 A3. INDEPENDENT LIMIT METHOD #2: mpmath dps=60 Richardson theta->0 on
     the FULL generic-(f,w) Kretschmann (the v_kretsch3 route
     transformed to the shaped class), evaluated at finite theta with
     NO limit machinery at all; compared against the claimed completed
     square AND against wrong-coefficient alternatives (+2, +8 on the
     w-jet; the factor-2 convention trap).
 B.  FC-1 robustness: THIRD-order transverse jets (b3, om3 on), exact
     rational evaluation, A -> 0 Laurent by exact evaluation at
     nested rational scales (v << A): does the singular law stay
     4 B^2/y^4?
Conventions: u = cos(theta); axis-regular class f = a + b(1-u) + ...,
w = om(1-u) + ...; f_u(pole) = -b; om = w_thth(pole); R-areal, static,
signature (-,+,+,+).  q != 0 is OUT OF SCOPE here (reported as scope,
not contradiction, per the arm's premise set).
"""
import sys, time
import sympy as sp
from mpmath import mp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V1-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# =====================================================================
# A1. Gauss-equation route to the +4 coefficient (no 4D engine at all)
# =====================================================================
th = sp.Symbol('theta', positive=True)
y, A, B, Om = sp.symbols('y A B Om', positive=True)
w2s = Om*(1 - sp.cos(th))            # om = w_thth(pole): d^2/dth^2 at 0
check("conv", sp.simplify(sp.diff(w2s, th, 2).subs(th, 0) - Om) == 0,
      "convention chain: w = om(1-cos th) has w_thth(pole) = om EXACTLY")
E = y**2*(1 + w2s)**2                 # g_thth of the shaped 2-sphere
G = y**2*sp.sin(th)**2/(1 + w2s)**2   # g_phph
SEG = y**2*sp.sin(th)                 # sqrt(EG) exactly ((1+w)^2 cancels)
check("A1s", sp.simplify(E*G - SEG**2) == 0, "sqrt(EG) = y^2 sin th")
KG = -sp.diff(sp.diff(G, th)/SEG, th)/(2*SEG)
KG_pole = sp.cancel(sp.series(sp.cancel(sp.together(KG)), th, 0, 1)
                    .removeO().subs(th, 0))
check("A1a", sp.simplify(KG_pole - (1 + 4*Om)/y**2) == 0,
      f"pole Gauss curvature of the shaped 2-sphere = (1 + 4 om)/y^2 "
      f"EXACTLY (independent 2D route; got {KG_pole}) — the +4 is real")
# Gauss equation: K_G = R^(4)_(th^ ph^ th^ ph^) + k_th k_ph, with the
# r = const sphere's orthonormal extrinsic curvatures in the static
# shaped 4-metric (normal n = sqrt(f) d_r, rho = r canon, r = y):
r = sp.Symbol('r', positive=True)
wfull = sp.Function('w')(r, th); ffull = sp.Function('f')(r, th)
h_th = r**2*(1 + wfull)**2
h_ph = r**2*sp.sin(th)**2/(1 + wfull)**2
k_th = sp.sqrt(ffull)*sp.diff(h_th, r)/(2*h_th)   # orthonormal K^th_th
k_ph = sp.sqrt(ffull)*sp.diff(h_ph, r)/(2*h_ph)
# on the axis-regular class at the pole: w and w_r vanish on the axis
prod = sp.together(sp.expand(k_th*k_ph))
pole_sub = {d: 0 for d in prod.atoms(sp.Derivative) if d.expr == wfull}
pole_sub.update({wfull: 0, ffull: A})
kk = sp.simplify(prod.xreplace(pole_sub).subs(r, y))
check("A1b", sp.simplify(kk - A/y**2) == 0,
      "extrinsic product at the pole = f/y^2 (w, w_r vanish on axis)")
R_thph_pred = sp.simplify(KG_pole - kk)
check("A1c", sp.simplify(R_thph_pred - ((1 - A) + 4*Om)/y**2) == 0,
      "Gauss equation => R_(th^ ph^ th^ ph^)(pole) = [(1-f) + 4 w_thth]"
      "/y^2 — the claimed unique w-jet carrier RE-DERIVED with no 4D "
      "curvature engine (claim 3 component identification)")

# =====================================================================
# shared independent 4D engine (written from scratch for this verifier)
# =====================================================================
def curvature(g, coords):
    n = len(coords)
    gi = g.inv()
    Gm = {}
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                expr = sum(gi[a, d]*(sp.diff(g[d, b], coords[c])
                       + sp.diff(g[d, c], coords[b])
                       - sp.diff(g[b, c], coords[d])) for d in range(n))
                Gm[(a, b, c)] = sp.cancel(expr/2)
    def Gam(a, b, c):
        return Gm[(a, b, c)] if c >= b else Gm[(a, c, b)]
    Rd = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(c+1, n):
                    expr = (sp.diff(Gam(a, b, d), coords[c])
                            - sp.diff(Gam(a, b, c), coords[d])
                            + sum(Gam(a, e, c)*Gam(e, b, d)
                                  - Gam(a, e, d)*Gam(e, b, c)
                                  for e in range(n)))
                    Rd[(a, b, c, d)] = expr
    Rdddd = {}
    for (a, b, c, d), val in Rd.items():
        Rdddd[(a, b, c, d)] = sum(g[a, e]*Rd.get((e, b, c, d), 0)
                                  for e in range(n))
    return gi, Rdddd

def kretschmann_terms(g, coords):
    """list of (idx, R_abcd, inverse-metric weight) over the FULL index
    range (diagonal metric), using antisymmetry to fill c<->d, a<->b."""
    gi, Rl = curvature(g, coords)
    n = len(coords)
    terms = []
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if c < d:
                        comp = Rl.get((a, b, c, d), 0)
                    elif c > d:
                        comp = -Rl.get((a, b, d, c), 0)
                    else:
                        continue
                    comp = sp.together(comp)
                    if comp == 0:
                        continue
                    terms.append(((a, b, c, d), comp,
                                  gi[a, a]*gi[b, b]*gi[c, c]*gi[d, d]))
    return terms

# engine validation: Schwarzschild in u-coordinates
T, u, ph = sp.symbols('T u phi')
M = sp.Symbol('M', positive=True)
fs = 1 - 2*M/y
gS = sp.diag(-fs, 1/fs, y**2/(1 - u**2), y**2*(1 - u**2))
KS = sum(t**2*wgt for _, t, wgt in kretschmann_terms(gS, [T, y, u, ph]))
check("E1", sp.simplify(KS - 48*M**2/y**6) == 0,
      "independent engine validated: Schwarzschild K = 48 M^2/y^6")

# =====================================================================
# A2. INDEPENDENT LIMIT METHOD #1: per-term sympy series in v = 1-u,
#     A symbolic, all other jets exact rationals.  Detects any
#     divergent term the arm's trailing-coefficient logic could have
#     silently zeroed (a v^(-n) pole shows up in the series).
# =====================================================================
print(f"[t={time.time()-t0:.0f}s] A2: building reduced-class K terms "
      f"(A symbolic) ...", flush=True)
R = sp.Rational
v = sp.Symbol('v', positive=True)
af = sp.Function('a')(y); bf = sp.Function('b')(y); omf = sp.Function('om')(y)
fF = af + bf*(1 - u)
wF = omf*(1 - u)
g_red = sp.diag(-fF, 1/fF, y**2*(1 + wF)**2/(1 - u**2),
                y**2*(1 - u**2)/(1 + wF)**2)
terms = kretschmann_terms(g_red, [T, y, u, ph])
rat_d = {sp.Derivative(af, (y, 2)): R(9, 4), sp.Derivative(af, y): R(-7, 5),
       sp.Derivative(bf, (y, 2)): R(-1, 6), sp.Derivative(bf, y): R(2, 7),
       sp.Derivative(omf, (y, 2)): R(3, 4), sp.Derivative(omf, y): R(-5, 7),
       bf: R(-4, 3), omf: R(2, 5)}
yv_sub = {y: R(13, 10)}
rat = dict(rat_d); rat[y] = R(13, 10)
Kax = sp.Integer(0)
divergent = []
for i, (idx, comp, wgt) in enumerate(terms):
    expr = (comp**2*wgt).xreplace(rat_d).xreplace({af: A}).subs(yv_sub)\
        .subs(u, 1 - v)
    ser = sp.series(sp.cancel(sp.together(expr)), v, 0, 1)
    # any v^{-n} pole => divergent term
    lead = ser.removeO()
    pol = sp.Poly(sp.together(lead).as_numer_denom()[1], v)
    if pol.degree() > 0 and sp.cancel(lead*v**0).has(v) and \
       sp.limit(lead, v, 0) in (sp.oo, -sp.oo, sp.zoo):
        divergent.append(idx)
        continue
    Kax += sp.cancel(lead.subs(v, 0) if not lead.has(v)
                     else sp.limit(lead, v, 0))
check("A2a", len(divergent) == 0,
      f"NO divergent term on the axis (series method; {len(terms)} "
      f"nonzero index blocks scanned) — nothing was silently zeroed")
Kax = sp.cancel(sp.together(Kax))
# claimed completed square at these rationals (om = 2/5, b = -4/3, ...):
K_claim = (rat[sp.Derivative(af, (y, 2))]**2
           + 4*rat[sp.Derivative(af, y)]**2/rat[y]**2
           + 4*((1 - A) + 4*R(2, 5))**2/rat[y]**4
           + 4*R(-4, 3)**2/(A**2*rat[y]**4))
check("A2b", sp.simplify(Kax - K_claim) == 0,
      "K_axis(A) by the SERIES method = the claimed completed square "
      "a''^2 + 4a'^2/y^2 + 4[(1-A)+4om]^2/y^4 + 4b^2/(A^2 y^4) EXACTLY "
      "(independent of the trailing-coefficient machinery)")
# Laurent in A by series (independent of Poly trailing logic):
serA = sp.series(sp.expand(Kax*A**2), A, 0, 1).removeO()
law_coeff = serA.subs(A, 0)
check("A2c", sp.simplify(law_coeff - 4*R(-4, 3)**2/rat[y]**4) == 0,
      f"Laurent: A^2 K_axis -> {law_coeff} = 4 b^2/y^4; the w-jet "
      f"(om = 2/5 != 0) does NOT enter the singular order (FC-1)")
# om-derivative non-entry probe: om' and om'' were nonzero rationals
# above; rerun with om', om'' changed and CONFIRM K_axis identical:
rat2 = dict(rat_d); rat2[sp.Derivative(omf, y)] = R(17, 3)
rat2[sp.Derivative(omf, (y, 2))] = R(-23, 2)
Kax2 = sp.Integer(0)
for idx, comp, wgt in terms:
    expr = (comp**2*wgt).xreplace(rat2).xreplace({af: A}).subs(yv_sub)\
        .subs(u, 1 - v)
    lead = sp.series(sp.cancel(sp.together(expr)), v, 0, 1).removeO()
    Kax2 += sp.cancel(lead.subs(v, 0) if not lead.has(v)
                      else sp.limit(lead, v, 0))
check("A2d", sp.simplify(sp.cancel(sp.together(Kax2)) - Kax) == 0,
      "om' and om'' changed (-5/7 -> 17/3, 3/4 -> -23/2): K_axis "
      "UNCHANGED — no radial om-derivatives enter (claim 3)")

# =====================================================================
# A3. INDEPENDENT LIMIT METHOD #2: mpmath Richardson theta->0 on the
#     generic-(f,w) Kretschmann at FINITE theta (v_kretsch3 transform).
# =====================================================================
print(f"[t={time.time()-t0:.0f}s] A3: generic (f,w) engine for mpmath "
      f"...", flush=True)
mp.dps = 60
ths = sp.Symbol('th', positive=True)
fg = sp.Function('f')(y, ths); wg = sp.Function('w')(y, ths)
g_gen = sp.diag(-fg, 1/fg, y**2*(1 + wg)**2,
                y**2*sp.sin(ths)**2/(1 + wg)**2)
K_gen = sum(t**2*wgt for _, t, wgt in
            kretschmann_terms(g_gen, [T, y, ths, ph]))
# flatten derivatives to symbols (map built from the expression's OWN
# Derivative atoms, so canonical variable ordering is irrelevant)
syms = {}
repl = {}
for d in K_gen.atoms(sp.Derivative):
    base = d.expr
    name = 'F' if base == fg else 'W'
    cnt = {y: 0, ths: 0}
    for var, n in d.variable_count:
        cnt[var] += n
    key = (name, cnt[y], cnt[ths])
    if key not in syms:
        syms[key] = sp.Symbol(f'{name}_{cnt[y]}{cnt[ths]}')
    repl[d] = syms[key]
for base, name in ((fg, 'F'), (wg, 'W')):
    syms[(name, 0, 0)] = sp.Symbol(f'{name}_00')
    repl[base] = syms[(name, 0, 0)]
K_flat = K_gen.xreplace(repl)
assert not K_flat.atoms(sp.Derivative), "unflattened derivatives remain"
argsyms = [y, ths] + [syms[k] for k in sorted(syms)]
Kfun = sp.lambdify(argsyms, K_flat, 'mpmath')

def K_at(yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v, thv):
    """profiles f = a + b(1-cos th), w = om(1-cos th) at finite theta."""
    cv, sv = mp.cos(thv), mp.sin(thv)
    vals = {('F', 0, 0): Av + Bv*(1 - cv),
            ('F', 1, 0): A1v + B1v*(1 - cv),
            ('F', 2, 0): A2v + B2v*(1 - cv),
            ('F', 0, 1): Bv*sv, ('F', 0, 2): Bv*cv,
            ('F', 1, 1): B1v*sv,
            ('W', 0, 0): Omv*(1 - cv), ('W', 1, 0): Om1v*(1 - cv),
            ('W', 2, 0): Om2v*(1 - cv),
            ('W', 0, 1): Omv*sv, ('W', 0, 2): Omv*cv,
            ('W', 1, 1): Om1v*sv}
    return Kfun(yv, thv, *[vals[k] for k in sorted(vals)])

def K_square(yv, Av, A2v, A1v, Bv, Omv):
    return (A2v**2 + 4*A1v**2/yv**2 + 4*((1 - Av) + 4*Omv)**2/yv**4
            + 4*Bv**2/(yv**4*Av**2))

cases = [
    ("generic",  1.3, 0.8, -2.1, 3.3, 0.9, 1.7, -0.4, 0.6, 1.1, -0.7),
    ("om large", 0.75, 1.6, 1.2, -0.8, -1.3, 0.5, 2.0, 7.0/3, -1.9, 0.3),
    ("seal-ish", 0.9, 0.004, -40.0, 3500.0, 2.5, 30.0, -55.0, 0.8,
     12.0, -3.0),
]
all_ok = True
discrim_ok = True
for name, yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v in cases:
    yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v = map(
        mp.mpf, (yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v))
    k1 = K_at(yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v,
              mp.mpf('1e-2'))
    k2 = K_at(yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v,
              mp.mpf('5e-3'))
    k4 = K_at(yv, Av, A1v, A2v, Bv, B1v, B2v, Omv, Om1v, Om2v,
              mp.mpf('2.5e-3'))
    ke = (4*k2 - k1)/3
    ke2 = (4*k4 - k2)/3            # second Richardson rung
    kc = K_square(yv, Av, A2v, A1v, Bv, Omv)
    rel = abs(ke2 - kc)/abs(kc)
    all_ok &= rel < mp.mpf('1e-4')
    # wrong-coefficient discrimination (+2, +8 instead of +4; and the
    # factor-2 om-convention trap) — at the two points where the w-jet
    # term is not buried by the seal-dominant b^2/A^2 term:
    if name != "seal-ish":
        for coeff in (2, 8):
            kbad = (A2v**2 + 4*A1v**2/yv**2
                    + 4*((1 - Av) + coeff*Omv)**2/yv**4
                    + 4*Bv**2/(yv**4*Av**2))
            discrim_ok &= abs(ke2 - kbad)/abs(kc) > 100*rel
    print(f"   {name}: K(Richardson) = {mp.nstr(ke2, 12)}, "
          f"claimed = {mp.nstr(kc, 12)}, rel = {mp.nstr(rel, 3)}")
check("A3a", all_ok,
      "mpmath dps=60 Richardson theta->0 (NO limit machinery) matches "
      "the claimed completed square at all 3 points incl. a seal-ish "
      "A = 0.004 and a nonperturbative om = 7/3")
check("A3b", discrim_ok,
      "discrimination: the +2 and +8 alternatives (factor-2 convention "
      "traps) are EXCLUDED by >100x the residual at every point")

# =====================================================================
# B. FC-1 robustness: ORDER-3 transverse jets, exact rationals
#    Method (independent of the arm's Poly trailing-coefficient code
#    AND of sympy series): (i) singular order by exact nested-rational
#    evaluation A = 10^-j, v = 10^-(2j+6) (pure rational arithmetic,
#    no limits); (ii) full K_axis(A_i) at fixed rational A by
#    single-variable cancel-and-substitute limits, om3/b3 toggled.
# =====================================================================
print(f"[t={time.time()-t0:.0f}s] B: order-3 jet class ...", flush=True)
b2f = sp.Function('b2')(y); b3f = sp.Function('b3')(y)
om2f = sp.Function('om2')(y); om3f = sp.Function('om3')(y)
fF3 = af + bf*(1 - u) + b2f*(1 - u)**2 + b3f*(1 - u)**3
wF3 = omf*(1 - u) + om2f*(1 - u)**2 + om3f*(1 - u)**3
g3 = sp.diag(-fF3, 1/fF3, y**2*(1 + wF3)**2/(1 - u**2),
             y**2*(1 - u**2)/(1 + wF3)**2)
terms3 = kretschmann_terms(g3, [T, y, u, ph])
rat3 = {sp.Derivative(af, (y, 2)): R(9, 4), sp.Derivative(af, y): R(-7, 5),
        sp.Derivative(bf, (y, 2)): R(-1, 6), sp.Derivative(bf, y): R(2, 7),
        sp.Derivative(b2f, (y, 2)): R(1, 5), sp.Derivative(b2f, y): R(-3, 8),
        sp.Derivative(b3f, (y, 2)): R(-5, 11), sp.Derivative(b3f, y): R(7, 9),
        sp.Derivative(omf, (y, 2)): R(3, 4), sp.Derivative(omf, y): R(-5, 7),
        sp.Derivative(om2f, (y, 2)): R(-2, 9), sp.Derivative(om2f, y): R(4, 11),
        sp.Derivative(om3f, (y, 2)): R(8, 5), sp.Derivative(om3f, y): R(-6, 13),
        bf: R(-4, 3), b2f: R(5, 9), b3f: R(-7, 4),
        omf: R(2, 5), om2f: R(-1, 3), om3f: R(9, 2)}
zero3 = {b3f: R(0), om3f: R(0), sp.Derivative(b3f, y): R(0),
         sp.Derivative(b3f, (y, 2)): R(0), sp.Derivative(om3f, y): R(0),
         sp.Derivative(om3f, (y, 2)): R(0)}
rat3_off = dict(rat3); rat3_off.update(zero3)
subbed_on, subbed_off = [], []
for idx, comp, wgt in terms3:
    for store, rr in ((subbed_on, rat3), (subbed_off, rat3_off)):
        e = (comp**2*wgt).xreplace(rr).xreplace({af: A})
        store.append(e.subs(yv_sub).subs(u, 1 - v))
# (i) singular order, nested rationals (no limit machinery at all):
pred = 4*R(-4, 3)**2/R(13, 10)**4
errs = []
for j in (4, 6, 8):
    Aval = R(1, 10**j); vval = R(1, 10**(2*j + 6))
    tot = sum(e.subs([(A, Aval), (v, vval)]) for e in subbed_on)
    errs.append(abs(sp.N((tot*Aval**2 - pred)/pred, 20)))
check("B1", errs[0] > errs[1] > errs[2] and errs[2] < sp.N(R(1, 10**12), 5),
      f"ORDER-3 JETS ON (b3 = -7/4, om3 = 9/2, radial derivs on): "
      f"A^2 K -> 4 b^2/y^4 by exact nested-rational evaluation "
      f"(rel errs {[sp.N(e, 3) for e in errs]} -> 0): the singular "
      f"law is STILL w-BLIND with cubic transverse jets — FC-1 "
      f"robustness EXTENDED beyond the arm's order-2 premise")
# (ii) on/off toggle at the REGULAR order: at fixed rational A the
# difference K_on(v) - K_off(v) is exact-rational; if the order-3
# jets are absent from the axis curvature the difference is O(v):
Afix = R(1, 2)
diffs = []
for jv in (10, 20, 30):
    vval = R(1, 10**jv)
    don = sum(e.subs([(A, Afix), (v, vval)]) for e in subbed_on)
    doff = sum(e.subs([(A, Afix), (v, vval)]) for e in subbed_off)
    diffs.append(abs(sp.N(don - doff, 25)))
r1 = diffs[0]/diffs[1] if diffs[1] != 0 else sp.oo
r2 = diffs[1]/diffs[2] if diffs[2] != 0 else sp.oo
expo1 = sp.N(sp.log(r1, 10)/10, 5)
expo2 = sp.N(sp.log(r2, 10)/10, 5)
check("B2", diffs[0] < sp.N(R(1, 10**6), 5) and expo1 > 0.9 and
      expo2 > 0.9,
      f"b3/om3 ON-OFF difference at A = 1/2 vanishes at the axis with "
      f"measured scaling exponent {expo1}, {expo2} (= O(v^2); diffs "
      f"{[sp.N(d, 3) for d in diffs]}): the third transverse jets "
      f"vanish from the WHOLE axis curvature (regular order "
      f"included) — O(v^2) evidence grade")
# and K(v) approaches the order-2 completed square at the same rate:
K_sq = (R(9, 4)**2 + 4*R(-7, 5)**2/R(13, 10)**2
        + 4*((1 - Afix) + 4*R(2, 5))**2/R(13, 10)**4
        + 4*R(-4, 3)**2/(Afix**2*R(13, 10)**4))
errs2 = []
for jv in (10, 20):
    vval = R(1, 10**jv)
    don = sum(e.subs([(A, Afix), (v, vval)]) for e in subbed_on)
    errs2.append(abs(sp.N(don - K_sq, 25)))
check("B3", errs2[0] < sp.N(R(1, 10**6), 5) and errs2[1] < errs2[0],
      f"and K_on(v) -> the ORDER-2 completed square at A = 1/2 "
      f"(errs {[sp.N(e2, 3) for e2 in errs2]}): the order-3 class "
      f"adds nothing to the axis curvature at this A")
print(f"   (scope note: q != 0 NOT tested — any q-on seal result is "
      f"new scope, not contradiction, per the arm's premise set)")

print(f"\nVERIFIER-1 (K_axis/seal law): {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
