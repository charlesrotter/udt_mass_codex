#!/usr/bin/env python3
"""
W3 VERIFIER — SCRIPT V2 (SEAL ENDPOINT + ROBUSTNESS COMPLETION).
Date: 2026-06-12.  Blind adversarial verifier on w3_seal_endpoint.py
(claim 2) and COMPLETING ADJUDICATOR for the dead w3_seal_robustness.py
probe (claim 5, P1/P2) — by TRACTABLE means: mpmath dps-40 numeric
layer integrals at a mu-ladder + exact-model linear fits.  NO
open-ended symbolic integrate (the failure mode that killed the probe
twice).

METHOD: for each atom (gg_th, gg_ph, rd, rr), each (l,l') pair, each
layer model f = mu + b x + c2 x^2 (x = 1-u; c2 = 0 linear anchor,
c2 = b/3 the probe's curved model, c2 = -b/4 hostile second curvature),
compute I(mu) = (1/2) Int_{-1}^{1} atom du at mu in a 6-rung ladder,
fit I = k1/mu + k2 ln(1/mu) + k3 + k4 mu ln(1/mu) + k5 mu exactly
(5x5 solve on rungs 1-5), VALIDATE on the held-out 6th rung.
Anchors: every linear-model fit must reproduce w3_seal_endpoint's
exact symbolic table (vv^T/2 rr block, -vv^T/(2b) frozen log, m=1 ln
diag (3/2b, 15/2b, 21/b), m=2 all-zero).

ATTACKS:
 B-1 independent exponent table (numeric route vs their symbolic);
 B-2 the chart family: the m=0 v-hat 1/mu coefficient along the chart
     law r(be) = (2-be)/(3-be) (al=1) — kappa = 0 at be = 2 (the
     PHI-ROOT chart, V1-A8) and kappa < 0 on the OPEN BAND be in
     (2,3): the forced-Dirichlet ruling fails on a chart BAND, not a
     measure-zero set (the divergence is attractive there: Coulomb
     species, no finite-action exclusion);
 C-1 (P1) curved-layer 1/mu exponent law + vv^T/2 block;
 C-2 (P2) the m=1 ln invariance: invariance across variants is
     EXACTLY the vanishing of the ln content of the correction
     combination C = 4 gg_th + 2 rd + rr (the rank-one square
     s2 (2R' - (fu/f)R)^2 / f, where on the linear model
     2R' - (fu/f)R = -(2A/sqrt(2x)) mu/f is mu-suppressed);
     adjudicate structural-vs-artifact on two curvatures.
     ALSO: the committed probe's check("P2", True, ...) is a VACUOUS
     assert (records `inv` in prose only) — named and resolved here.
"""
import sys, time
import mpmath as mp

t0 = time.time()
mp.mp.dps = 40
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

b = mp.mpf(1)

# normalized real harmonics: P_lm = s^m Q_lm(u), s = sqrt(1-u^2);
# everything below is built from the POLYNOMIAL part Q_lm so no sqrt
# or 0/0 ever appears in an integrand (the m-fold s-powers are folded
# in analytically):
#   s2 dRi dRj = s^{2m+2} Qi'Qj' - m u s^{2m} (Qi'Qj + Qj'Qi)
#                + m^2 u^2 s^{2m-2} Qi Qj
#   m^2 Ri Rj / s2 = m^2 s^{2m-2} Qi Qj
#   (dRi Rj + dRj Ri) = s^{2m}(Qi'Qj + Qj'Qi) - 2 m u s^{2m-2} Qi Qj
#   Ri Rj = s^{2m} Qi Qj
import sympy as sp
us = sp.Symbol('u')
QPOLY = {(0, 0): sp.Integer(1), (1, 0): us,
         (2, 0): (3*us**2 - 1)/2, (3, 0): (5*us**3 - 3*us)/2,
         (1, 1): sp.Integer(-1), (2, 1): -3*us,
         (3, 1): -(15*us**2 - 3)/2,
         (2, 2): sp.Integer(3), (3, 2): 15*us,
         (3, 3): sp.Integer(-15)}
NRM = {}
def nrm2(l, m):
    """exact 1/<P^2> with <.> = (1/2)Int du (rational)."""
    if (l, m) not in NRM:
        P2 = (1 - us**2)**m * QPOLY[(l, m)]**2
        NRM[(l, m)] = sp.Rational(1, 1)/(sp.integrate(P2, (us, -1, 1))/2)
    return NRM[(l, m)]

ATOMF = {}
def atom_funcs(mq, i_l, j_l):
    """mpmath-lambdified atom integrands (functions of u, mu, c2)."""
    key = (mq, i_l, j_l)
    if key in ATOMF:
        return ATOMF[key]
    Qi, Qj = QPOLY[(i_l, mq)], QPOLY[(j_l, mq)]
    dQi, dQj = sp.diff(Qi, us), sp.diff(Qj, us)
    NN = sp.sqrt(nrm2(i_l, mq)*nrm2(j_l, mq))   # rational^1/2, constant
    s2s = 1 - us**2
    mus, c2s = sp.symbols('mu_s c2_s')
    xs = 1 - us
    fs = mus + b*xs + c2s*xs**2
    fus = -(b + 2*c2s*xs)
    m = mq
    s2dd = (s2s**(m + 1)*dQi*dQj
            - m*us*s2s**m*(dQi*Qj + dQj*Qi)
            + m**2*us**2*s2s**(m - 1)*Qi*Qj) if m else s2s*dQi*dQj
    ggph = m**2*s2s**(m - 1)*Qi*Qj if m else sp.Integer(0)
    drr = (s2s**m*(dQi*Qj + dQj*Qi)
           - 2*m*us*s2s**(m - 1)*Qi*Qj) if m else (dQi*Qj + dQj*Qi)
    rrs = s2s**m*Qi*Qj
    exprs = {'gg_th': NN*s2dd/fs,
             'gg_ph': NN*ggph/fs,
             'rd': -NN*s2s*fus*drr/fs**2,
             'rr': NN*s2s*fus**2*rrs/fs**3}
    ATOMF[key] = {k: sp.lambdify((us, mus, c2s), e, modules='mpmath')
                  for k, e in exprs.items()}
    return ATOMF[key]

def atoms_at_mu(mq, i_l, j_l, mu, c2):
    """(gg_th, gg_ph, rd, rr) layer integrals, (1/2)Int du included."""
    fns = atom_funcs(mq, i_l, j_l)
    pts = [mp.mpf(-1), mp.mpf(0), 1 - mp.mpf('0.1')]
    xq = mp.mpf('0.1')
    while xq > 50*mu:
        xq = xq/10
        pts.append(1 - xq)
    pts += [1 - 10*mu, 1 - mu, mp.mpf(1)]
    pts = sorted(set(pts))
    out = {}
    for kind, fn in fns.items():
        out[kind] = mp.quad(lambda u: fn(u, mu, c2), pts)/2
    return out

MUS = [mp.mpf(10)**(-k) for k in (5, 6, 7, 8, 9, 10)]
def fit_laws(mq, i_l, j_l, c2):
    """fit I(mu) = k1/mu + k2 ln(1/mu) + k3 + k4 mu ln(1/mu) + k5 mu
    on rungs 1-5, validate on rung 6; returns dict kind ->
    (k1, k2, fit_ok)."""
    vals = {k: [] for k in ('gg_th', 'gg_ph', 'rd', 'rr')}
    for mu in MUS:
        a = atoms_at_mu(mq, i_l, j_l, mu, c2)
        for k in vals:
            vals[k].append(a[k])
    res = {}
    for k, ys in vals.items():
        A = mp.matrix([[1/mu, mp.log(1/mu), 1, mu*mp.log(1/mu), mu]
                       for mu in MUS[:5]])
        co = mp.lu_solve(A, mp.matrix(ys[:5]))
        mu6 = MUS[5]
        pred = (co[0]/mu6 + co[1]*mp.log(1/mu6) + co[2]
                + co[3]*mu6*mp.log(1/mu6) + co[4]*mu6)
        scl = max(abs(ys[5]), abs(co[0])/mu6, abs(co[1])*mp.log(1/mu6),
                  abs(co[2]), mp.mpf('1e-12'))
        ok = abs(pred - ys[5])/scl < mp.mpf('1e-6')
        res[k] = (co[0], co[1], ok)
    return res

TOL = mp.mpf('1e-7')
def zthr(R):
    sc = max(abs(R[a][0]) + abs(R[a][1]) for a in R)
    return mp.mpf('1e-6')*(1 + sc)
def near(a, bb, tol=TOL):
    return abs(a - bb) < tol*max(1, abs(bb))

# ---------------- B-1: linear-model anchor (m=0) ----------------
print("B-1: m=0 linear-model exponent table, numeric ladder ...",
      flush=True)
v = [mp.sqrt(2*l + 1) for l in range(4)]
okmu = oklog = okfit = True
rrmu = mp.matrix(4, 4); loglin = {at: mp.matrix(4, 4)
                                  for at in ('gg_th', 'rd', 'rr')}
for i in range(4):
    for j in range(i, 4):
        R = fit_laws(0, i, j, mp.mpf(0))
        okfit &= all(R[k][2] for k in R)
        # only rr carries 1/mu:
        zt = zthr(R)
        okmu &= (near(R['rr'][0], v[i]*v[j]/2)
                 and abs(R['gg_th'][0]) < zt and abs(R['rd'][0]) < zt)
        for at in loglin:
            loglin[at][i, j] = loglin[at][j, i] = R[at][1]
check("B1a", okfit and okmu,
      "LINEAR m=0: held-out-rung fits clean; ONLY the rr-atom carries "
      "1/mu and its block = v v^T/2 exactly (numeric route confirms "
      "W3S-B1/B2; the vv^T/(4 mu) seal law re-derived)")
okfz = all(near(loglin['gg_th'][i, j] + loglin['rd'][i, j]
                + loglin['rr'][i, j], -v[i]*v[j]/(2*b))
           for i in range(4) for j in range(4))
check("B1b", okfz,
      "LINEAR m=0: frozen ln(1/mu) block = -v v^T/(2b) (matches W3S-B4"
      " printed matrix; vv^T-aligned as VS1 banked).  NOTE OF RECORD: "
      "W3S-B3's caption 'rd+rr logs CANCEL EXACTLY' is FALSE (their "
      "own printout shows -vv^T/(2b)); the check passed only via an "
      "`... or True` — VACUOUS ASSERT, named in the hygiene table")
# dressed coefficients 2/3, 1/2 are pure rr-ratios -> follow from B1a;
# the v-hat-direction ln coefficient per chart (al=1):
def kap_ln(be):
    g_ = -(1 + be)/(3 - be); d_ = (1 - be)/(3 - be)
    r_ = (2 - be)/(3 - be)
    M = [[g_*loglin['gg_th'][i, j] + d_*loglin['rd'][i, j]
          + r_*loglin['rr'][i, j] for j in range(4)] for i in range(4)]
    vh = [vi/4 for vi in v]
    return sum(vh[i]*M[i][j]*vh[j] for i in range(4) for j in range(4))

# ---------------- B-2: the chart band attack ----------------
kap = lambda be: (2 - be)/(3 - be)
band = [kap(mp.mpf(2) + mp.mpf(k)/10) for k in range(1, 10)]
check("B2a", all(kk < 0 for kk in band) and kap(2) == 0
      and kap(mp.mpf('1.99')) > 0 and kap(mp.mpf('3.01')) > 0,
      "chart law kappa(be) = (2-be)/(3-be) (al=1): kappa < 0 on the "
      "OPEN BAND be in (2,3), zero at be=2 (the PHI-ROOT chart, "
      "V1-A8), positive outside [2,3] — the set where the forced-"
      "Dirichlet ruling fails is a BAND + its edge, not measure-zero")
kl2 = kap_ln(mp.mpf(2))
check("B2b", abs(kl2) > mp.mpf('1e-3'),
      f"phi-root chart (be=2): 1/mu coefficient = 0 but the v-hat ln "
      f"coefficient = {mp.nstr(kl2, 6)}/b != 0: the seal potential "
      "drops to ln class in the v-hat channel -> BOTH branches "
      "action-finite -> NO forced Dirichlet in this chart "
      "(S1's one forced condition is NOT chart-robust on C1-only)")
print(f"   v-hat ln coefficient across charts: be=0: "
      f"{mp.nstr(kap_ln(mp.mpf(0)), 6)}, be=1: "
      f"{mp.nstr(kap_ln(mp.mpf(1)), 6)}, be=2: {mp.nstr(kl2, 6)}, "
      f"be=2.5: {mp.nstr(kap_ln(mp.mpf('2.5')), 6)}")

# ---------------- B-3: m=1 / m=2 linear anchors ----------------
print("B-3: m=1 linear ladder ...", flush=True)
ok1 = True; lndiag = []
C_ln = []          # correction combination ln coefficients
for k, l in enumerate((1, 2, 3)):
    R = fit_laws(1, l, l, mp.mpf(0))
    zt = zthr(R)
    ok1 &= all(abs(R[a][0]) < zt for a in R) and all(R[a][2] for a in R)
    tot_frozen = R['gg_th'][1] + R['gg_ph'][1] + R['rd'][1] + R['rr'][1]
    lndiag.append(tot_frozen)
    C_ln.append(4*R['gg_th'][1] + 2*R['rd'][1] + R['rr'][1])
ref = [mp.mpf(3)/(2*b), mp.mpf(15)/(2*b), mp.mpf(21)/b]
check("B3a", ok1 and all(near(lndiag[k], ref[k]) for k in range(3)),
      "LINEAR m=1: no atom carries 1/mu; frozen ln diag = "
      "(3/2b, 15/2b, 21/b) — matches W3S-D1/D1b printed table")
check("B3b", all(abs(C_ln[k]) < mp.mpf('1e-6')*(1 + abs(lndiag[k])) for k in range(3)),
      "LINEAR m=1: correction combination C = 4gg+2rd+rr has ZERO ln "
      "content (numeric) — explains the variant-invariance: "
      "V-w = frozen - C/3, V-s = frozen - C/2, and on the linear "
      "model 2R'-(fu/f)R = -(2A/sqrt(2x)) mu/f is mu-suppressed")
print("B-3: m=2 ladder ...", flush=True)
R22 = fit_laws(2, 2, 2, mp.mpf(0))
check("B3c", all(abs(R22[a][0]) < zthr(R22) and abs(R22[a][1]) < zthr(R22)
                 for a in R22),
      "LINEAR m=2 (l=2 diag): no 1/mu, no ln — regular endpoint "
      "(W3S-D2 confirmed numerically)")

# ---------------- C: the dead robustness probe, completed ----------
for tagc, c2v in (("c2=+b/3", b/3), ("c2=-b/4", -b/4)):
    print(f"C: curved layer {tagc} ...", flush=True)
    okmu = okv = okfit = True
    for i in range(3):
        for j in range(i, 3):
            R = fit_laws(0, i, j, c2v)
            okfit &= all(R[k][2] for k in R)
            zt = zthr(R)
            okmu &= (abs(R['gg_th'][0]) < zt and abs(R['rd'][0]) < zt)
            okv &= near(R['rr'][0], v[i]*v[j]/2)
    check(f"P1-{tagc}", okfit and okmu and okv,
          f"CURVED ({tagc}) m=0 (l<=2): only rr carries 1/mu AND the "
          "block stays EXACTLY v v^T/2 — the exponent law and the "
          "dressed rationals 2/3 (V-w), 1/2 (V-s) are curvature-blind "
          "(P1 ADJUDICATED TRUE: the 1/mu integral localizes at "
          "x ~ mu/b where only b = -f_u(pole) survives)")
    okC = True; okln = True; drift = []
    for l in (1, 2, 3):
        R = fit_laws(1, l, l, c2v)
        zt = zthr(R)
        okln &= all(abs(R[a][0]) < zt for a in R)
        Cc = 4*R['gg_th'][1] + 2*R['rd'][1] + R['rr'][1]
        drift.append(Cc)
        okC &= abs(Cc) < zt
    check(f"P2-{tagc}", okln and okC,
          f"CURVED ({tagc}) m=1: still no 1/mu anywhere; correction-"
          f"combination ln content = {[mp.nstr(x, 4) for x in drift]} "
          "= 0 -> the ln-coefficient invariance across variants "
          "PERSISTS under layer curvature (P2 ADJUDICATED: STRUCTURAL "
          "IDENTITY, not a linear-model artifact; mechanism: "
          "2R'-(fu/f)R = -(2A/sqrt(2x))(mu - c2 x^2)/f kills the 1/x "
          "core of the square; ln-class classification unaffected "
          "either way)")

print(f"\nV2 ENDPOINT+ROBUSTNESS: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
