#!/usr/bin/env python3
"""
Fixed-metric reciprocal-plane selector theorem (constant-alpha family).

Preregistered targets T1-T6 of
udt_alpha_plane_selector_theorem_2026-07-28/PREREGISTRATION.md.

Fully symbolic (sympy). Free symbols: u, f, b, chi, df, db, dchi, alpha, c_E
(u > 0, b > 0 on principal orbits; c_E real nonzero; the rest real).
Transverse derivation X follows the parent's rules:

    X(u) = -2*chi*u,   X(f) = df,   X(b) = db,   X(chi) = dchi,
    X(alpha) = X(c_E) = X(m) = X(n) = 0   (family constants / constant line
                                           coefficients).

dchi is declared for completeness but is never load-bearing: every certificate
quantity is first order in X applied to Gram entries, which are chi-free.

CONVENTIONS (stated per the T2 caution in the dispatch):
  * A Killing vector Z = z0*K + z1*W is the COLUMN (z0, z1)^T in the ordered
    basis (K, W) of the plane span(K, W).
  * G_P is the Gram matrix of g restricted to the plane in that basis;
    D_P = G_P^{-1} X(G_P) acts on columns by left multiplication.
  * K = (1,0)^T.  D_P(K) = column 0 of D_P = (D[0,0], D[1,0])^T, so K is an
    eigenvector of D_P  iff  the entry D_P[1,0] (row 1 = W-component,
    column 0 = image of K) vanishes; the eigenvalue is then D_P[0,0].
  * Certificate C(P): (i) |det G_P| constant on the connected principal-orbit
    region (pointwise jet criterion: X(det G_P) = 0); (ii) K an eigenvector of
    D_P; (iii) eigenvalue pair exactly (-2*chi, +2*chi).

Every symbolic check is a zero-residual sympy test (simplify/cancel/equals),
never an eyeball.  Any failure is recorded as-is (falsifier F-C fires); no
massaging.  Exit code 0 iff every check passes.
"""

import json
import os
import random
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Symbols and the transverse derivation X
# ----------------------------------------------------------------------------
u, b = sp.symbols('u b', positive=True)
f, df, db, chi, dchi, alpha = sp.symbols('f df db chi dchi alpha', real=True)
c_E = sp.Symbol('c_E', real=True, nonzero=True)
m, n = sp.symbols('m n', real=True)          # constant candidate-line coeffs
sig = sp.Symbol('sigma', real=True)          # F-D basis-change shear
lam = sp.Symbol('lam', real=True, nonzero=True)  # F-D basis-change scale
cc = sp.Symbol('c_X', real=True, nonzero=True)   # F-D X-rescaling

RULES = {u: -2 * chi * u, f: df, b: db, chi: dchi}


def X(expr):
    """The transverse derivation on rational expressions in (u, f, b, chi)."""
    e = sp.sympify(expr)
    return sp.expand(sum(rate * sp.diff(e, s) for s, rate in RULES.items()))


def XM(M):
    return M.applyfunc(X)


def zero(e):
    """Robust exact zero test; returns True only on a proven zero residual."""
    e = sp.sympify(e)
    e2 = sp.cancel(sp.together(sp.expand(e)))
    if e2 == 0:
        return True
    e3 = sp.simplify(e2)
    if e3 == 0:
        return True
    e4 = sp.simplify(sp.trigsimp(e3))
    if e4 == 0:
        return True
    r = e4.equals(0)
    return bool(r) if r is not None else False


def mzero(M):
    return all(zero(x) for x in M)


checks = []


def record(name, ok, note):
    checks.append({"name": name, "pass": bool(ok), "note": note})
    print(("PASS" if ok else "FAIL"), name, "::", note)


# ----------------------------------------------------------------------------
# Shared objects
# ----------------------------------------------------------------------------
Q = 1 / u - alpha ** 2 * u          # g(V,V) on the family
S = b * u + f ** 2                  # the area invariant of span(K,Y)

# ============================================================================
# T1 — registered plane span(K,V)
# ============================================================================
G_KV = sp.Matrix([[-c_E ** 2 * u, -alpha * c_E * u],
                  [-alpha * c_E * u, Q]])
record("T1_det_GKV", zero(G_KV.det() + c_E ** 2),
       "det G_KV = -c_E**2 exactly (constant; all alpha, all metrics)")

D_KV = sp.simplify(G_KV.inv() * XM(G_KV))
record("T1_K_eigenvector", zero(D_KV[1, 0]),
       "D_KV[1,0] = 0: K=(1,0) is an eigenvector of D_KV for symbolic alpha")
record("T1_K_rate", zero(D_KV[0, 0] + 2 * chi),
       "K-eigenvalue = -2*chi exactly")
record("T1_trace_zero", zero(sp.trace(D_KV)),
       "tr D_KV = 0 exactly")
record("T1_second_rate", zero(D_KV[1, 1] - 2 * chi),
       "second eigenvalue = +2*chi (upper-triangular => diagonal entries)")
record("T1_offdiag_parent_D1", zero(D_KV[0, 1] + 4 * alpha * chi / c_E),
       "D_KV[0,1] = -4*alpha*chi/c_E: matches parent D1 sec.3 exactly")

# ============================================================================
# T2 — second plane span(K,Y): K-eigenline leg
# ============================================================================
G_KY = sp.Matrix([[-c_E ** 2 * u, -alpha * c_E * u * f],
                  [-alpha * c_E * u * f, Q * f ** 2 + b]])
record("T2_det_GKY", zero(G_KY.det() + c_E ** 2 * S),
       "det G_KY = -c_E**2*(b*u + f**2) exactly")

D_KY = sp.simplify(G_KY.inv() * XM(G_KY))
off = D_KY[1, 0]
record("T2_off_entry_formula",
       zero(off + alpha * c_E * df * u ** 2 / S),
       "(D_KY)[1,0] = -alpha*c_E*df*u**2/(b*u+f**2) exactly "
       "[convention: row 1 = Y-component of D_KY(K); K eigenvector iff = 0]")
record("T2_off_cleared", zero(off * S + alpha * c_E * df * u ** 2),
       "cleared form: (D_KY)[1,0]*(b*u+f**2) + alpha*c_E*df*u**2 = 0")

S_pos = sp.sympify(S).is_positive
if S_pos is None:
    S_pos = bool((b * u).is_positive and (f ** 2).is_nonnegative)
record("T2_denominator_positive", bool(S_pos),
       "b*u + f**2 > 0 on principal orbits (u>0, b>0) -- with c_E != 0 and "
       "u > 0 this gives: K eigenvector of D_KY at a point IFF alpha*df = 0 "
       "there")

# ============================================================================
# T3 — second plane: area leg
# ============================================================================
XS = X(S)
record("T3_XS_formula", zero(XS - (db * u - 2 * chi * u * b + 2 * f * df)),
       "X(b*u+f**2) = db*u - 2*chi*u*b + 2*f*df exactly")
record("T3_trace_is_dlogdet", zero(sp.trace(D_KY) - XS / S),
       "tr D_KY = X(b*u+f**2)/(b*u+f**2) = X(log|det G_KY|)")
record("T3_jacobi", zero(X(G_KY.det()) / G_KY.det() - XS / S),
       "X(det G_KY)/det G_KY = X(S)/S (Jacobi/consistency)")
record("T3_Xdet", zero(X(G_KY.det()) + c_E ** 2 * XS),
       "X(det G_KY) = -c_E**2 * X(S): |det G_KY| constant iff X(b*u+f**2)=0")

# ============================================================================
# T5 — alpha = 0 sub-case (diagonal response)
# ============================================================================
D0 = sp.simplify(D_KY.subs(alpha, 0))
record("T5a0_diagonal", zero(D0[0, 1]) and zero(D0[1, 0]),
       "alpha=0: D_KY is diagonal, so the K-eigenline leg passes trivially")
record("T5a0_K_rate", zero(D0[0, 0] + 2 * chi),
       "alpha=0: K-eigenvalue = -2*chi always")
E = f ** 2 / u + b
record("T5a0_E_identity", zero(E - S / u),
       "f**2/u + b = (b*u+f**2)/u exactly")
record("T5a0_second_rate_log", zero(D0[1, 1] - X(E) / E),
       "alpha=0: second eigenvalue = X(ln(f**2/u + b))")
record("T5a0_rate_decomposition", zero(X(E) / E - (XS / S + 2 * chi)),
       "X(ln(f**2/u+b)) = X(ln(b*u+f**2)) + 2*chi exactly")
record("T5a0_founded_iff", zero(D0[1, 1] - 2 * chi - XS / S),
       "second eigenvalue - 2*chi = X(S)/S: founded rate +2*chi IFF "
       "X(b*u+f**2)=0 -- the SAME exceptional condition governs the area leg "
       "(T3) and the rate leg at alpha=0 (coincidence noted explicitly)")

# T5 assembly (logical, backed by the identities above; recorded as verdicts)
t5b1_backing = all(c["pass"] for c in checks if c["name"].startswith(("T1_", "T2_")))
record("T5_branch_alpha_nonzero", t5b1_backing,
       "alpha != 0: span(K,V) passes C everywhere (T1); span(K,Y) violates "
       "leg (ii) at every principal point with df != 0 -- nonempty open set "
       "by T4 (Cartan, prose deliverable) -- hence C selects span(K,V) "
       "uniquely.  [Implication assembled from T1_*, T2_*; u>0, c_E!=0, S>0]")
t5b2_backing = all(c["pass"] for c in checks if c["name"].startswith(("T3_", "T5a0_")))
record("T5_branch_alpha_zero", t5b2_backing,
       "alpha = 0: span(K,Y) passes C iff X(b*u+f**2) == 0 on the connected "
       "principal region (legs (i) and (iii) both reduce to it; leg (ii) "
       "automatic).  Exceptional stratum = {alpha=0 and b*u+f**2 constant}; "
       "there BOTH planes satisfy C and the certificate is silent.")

# ============================================================================
# Witness control — parent sec.6 (alpha=0, f=cos 2eta, u=1+eps(1-f^2),
# b=(1-f^2)/u, X = d/deta)
# ============================================================================
eta = sp.Symbol('eta', real=True)
eps = sp.Symbol('epsilon', positive=True)
fw = sp.cos(2 * eta)
uw = 1 + eps * (1 - fw ** 2)
bw = (1 - fw ** 2) / uw
phiw = -sp.log(uw) / 2                     # u = e^{-2 phi}
chiw = sp.diff(phiw, eta)                  # chi = X(phi) = -u'/(2u)
dfw = sp.diff(fw, eta)                     # = -2*sin(2*eta)
dbw = sp.diff(bw, eta)

record("W_df_convention", zero(dfw + 2 * sp.sin(2 * eta)),
       "witness df = -2*sin(2*eta) (X = d/deta)")
record("W_on_stratum", zero(sp.simplify(bw * uw + fw ** 2 - 1)),
       "witness: b*u + f**2 = 1 EXACTLY -- the witness lies on the "
       "exceptional stratum (alpha=0, S constant)")

wsub = {u: uw, f: fw, b: bw, chi: chiw, df: dfw, db: dbw, alpha: 0}

# direct d/deta certificate for both planes (independent of the jet formalism)
GKVw = sp.Matrix([[-c_E ** 2 * uw, 0], [0, 1 / uw]])
DKVw = sp.simplify(GKVw.inv() * GKVw.diff(eta))
okKV = (zero(GKVw.det() + c_E ** 2) and zero(DKVw[0, 1]) and
        zero(DKVw[1, 0]) and zero(DKVw[0, 0] + 2 * chiw) and
        zero(DKVw[1, 1] - 2 * chiw))
record("W_KV_full_certificate", okKV,
       "witness span(K,V): det = -c_E**2 const, K eigenvector, rates "
       "(-2chi, +2chi) -- full certificate PASSES (direct d/deta)")

GKYw = sp.Matrix([[-c_E ** 2 * uw, 0], [0, fw ** 2 / uw + bw]])
DKYw = sp.simplify(GKYw.inv() * GKYw.diff(eta))
okKY = (zero(GKYw.det() + c_E ** 2) and zero(DKYw[0, 1]) and
        zero(DKYw[1, 0]) and zero(DKYw[0, 0] + 2 * chiw) and
        zero(DKYw[1, 1] - 2 * chiw))
record("W_KY_full_certificate", okKY,
       "witness span(K,Y): det = -c_E**2*(b*u+f**2) = -c_E**2 const, K "
       "eigenvector, rates (-2chi, +2chi) -- full certificate PASSES: both "
       "planes satisfy C on the witness (certificate silent, as frozen)")

record("W_formalism_consistency", mzero(sp.simplify(D_KY.subs(wsub)) - DKYw),
       "general jet-symbol D_KY specialized to the witness equals the direct "
       "d/deta computation (internal consistency of the derivation operator)")

# Bonus control: parent sec.6 identity.  HONESTY NOTE (recorded, not hidden):
# a first version of this check asserted det D_KY + 4*chi**2 =
# alpha**2*u**2*df**2 on the WHOLE X(S)=0 stratum and FAILED; hand
# re-derivation shows the correct general stratum identity carries 1/S:
#     det D_KY + 4*chi**2 = alpha**2*u**2*df**2 / (b*u+f**2)   on X(S)=0.
# The parent's sec.6 form (no 1/S) is stated for ITS witness, where
# b*u+f**2 = 1, and is exact there.  The failure was in this script's own
# mis-generalized auxiliary target, NOT in any preregistered T1-T6 formula
# and NOT in the parent; falsifier F-C does not fire.  Both corrected
# statements are now checked.
db_stratum = sp.solve(sp.Eq(XS, 0), db)[0]
Dc = sp.simplify(D_KY.subs(db, db_stratum))
record("parent6_identity_general_stratum",
       zero(Dc.det() + 4 * chi ** 2
            - alpha ** 2 * u ** 2 * df ** 2 / S.subs(db, db_stratum)),
       "on X(b*u+f**2)=0: det D_KY + 4*chi**2 = "
       "alpha**2*u**2*df**2/(b*u+f**2) exactly (general form; reduces to "
       "parent sec.6 when b*u+f**2 = 1; for alpha*df != 0 the rates leave "
       "the founded pair even where the area stays constant)")
wsubA = {u: uw, f: fw, b: bw, chi: chiw, df: dfw, db: dbw}  # alpha symbolic
DKYa = sp.simplify(D_KY.subs(wsubA))
record("parent6_identity_on_witness",
       zero(DKYa.det() + 4 * chiw ** 2 - alpha ** 2 * uw ** 2 * dfw ** 2),
       "on the parent sec.6 witness profile with SYMBOLIC alpha (where "
       "b*u+f**2 = 1): det D_KY + 4*chi**2 = alpha**2*u**2*df**2 exactly, "
       "confirming the parent's stated identity verbatim")

# ============================================================================
# T6 (cheap attempt only) — constant-area leg for W = m V + n Y
# ============================================================================
zline = m + n * f
gKK = -c_E ** 2 * u
gKW = -alpha * c_E * u * zline
gWW = Q * zline ** 2 + n ** 2 * b
G_KW = sp.Matrix([[gKK, gKW], [gKW, gWW]])
detW = sp.factor(sp.simplify(G_KW.det()))
record("T6_det_formula",
       zero(detW + c_E ** 2 * (zline ** 2 + n ** 2 * b * u)),
       "det G(K, m*V+n*Y) = -c_E**2*((m+n*f)**2 + n**2*b*u) exactly "
       "(alpha drops out)")
record("T6_parent4_crosscheck",
       zero(detW - (-c_E ** 2 * zline ** 2 - u * b * c_E ** 2 * n ** 2)),
       "matches parent sec.4 det G(T,Z) at T=K (r=s=0, Delta=0)")
record("T6_Xdet_record",
       zero(X(detW) + c_E ** 2 * (2 * m * n * df + n ** 2 * XS)),
       "X(det) = -c_E**2*(2*m*n*df + n**2*X(b*u+f**2)).  RECORD ONLY: "
       "vanishes iff n = 0 (the registered plane, always) or n != 0 with "
       "2*m*df + n*X(b*u+f**2) = 0 pointwise; alpha and c_E play no role.  "
       "On the exceptional stratum (df relevant): with X(S)=0 the condition "
       "is m*n*df = 0.  NO claim beyond this record.")

# ============================================================================
# F-D — presentation covariance of the certificate
# ============================================================================
# In-plane basis change fixing K:  (K, Y) -> (K, sigma*K + lam*Y), lam != 0.
Sb = sp.Matrix([[1, sig], [0, lam]])
Gp = sp.simplify(Sb.T * G_KY * Sb)
Dp = sp.simplify(Gp.inv() * XM(Gp))
record("FD_basis_det", zero(Gp.det() - lam ** 2 * G_KY.det()),
       "in-plane basis change (K fixed, W -> sigma*K + lam*W): det scales by "
       "the constant lam**2 -- constancy of |det| is invariant")
record("FD_basis_similarity", mzero(Dp - sp.simplify(Sb.inv() * D_KY * Sb)),
       "D transforms by constant similarity D -> S^-1 D S: eigenvalues "
       "invariant, K-eigenline condition invariant (D'[1,0] = D[1,0]/lam)")
record("FD_offentry_scaling", zero(Dp[1, 0] - D_KY[1, 0] / lam),
       "explicit: D'[1,0] = D[1,0]/lam, zero iff D[1,0] zero")
Dscaled = D_KY.subs({chi: cc * chi, df: cc * df, db: cc * db},
                    simultaneous=True)
record("FD_X_rescaling", mzero(sp.simplify(Dscaled - cc * D_KY)),
       "X -> c*X rescales D linearly (chi, df, db -> c*(...)): eigenvector "
       "conditions and the rate-pair condition (eigenvalues = -+2*chi) are "
       "X-normalization covariant")

# ============================================================================
# Numeric spot checks (>= 6 admissible random jet points)
# ============================================================================
random.seed(20260728)


def rq(lo, hi):
    return sp.Rational(random.randint(int(lo * 100), int(hi * 100)), 100)


def rq_nonzero(lo, hi):
    while True:
        v = rq(lo, hi)
        if v != 0:
            return v


TOL = sp.Float('1e-12')
NONZ = sp.Float('1e-6')
numeric = []
num_ok = True

# Set A: alpha != 0, df != 0 (4 points)
for i in range(4):
    pt = {u: rq(sp.Rational(1, 5), 3), b: rq(sp.Rational(1, 5), 3),
          f: rq(-2, 2), df: rq_nonzero(-2, 2), db: rq(-2, 2),
          chi: rq_nonzero(-2, 2), alpha: rq_nonzero(-2, 2),
          c_E: rq_nonzero(sp.Rational(1, 2), 3)}
    offv = sp.Float(off.subs(pt))
    tgt = sp.Float((-alpha * c_E * df * u ** 2 / S).subs(pt))
    xdet = sp.Float(X(G_KY.det()).subs(pt))
    xsv = sp.Float(XS.subs(pt))
    res = {
        "point": {str(k): str(v) for k, v in pt.items()},
        "set": "A (alpha!=0, df!=0)",
        "T1_det_resid": float(abs(sp.Float((G_KV.det() + c_E ** 2).subs(pt)))),
        "T1_eigvec_resid": float(abs(sp.Float(D_KV[1, 0].subs(pt)))),
        "T1_rates_resid": float(abs(sp.Float((D_KV[0, 0] + 2 * chi).subs(pt)))
                                + abs(sp.Float((D_KV[1, 1] - 2 * chi).subs(pt)))),
        "T2_formula_resid": float(abs(offv - tgt)),
        "T2_K_eigvec_of_DKY_broken": bool(abs(offv) > NONZ),
        "T2_offvalue": float(offv),
        "T3_trace_resid": float(abs(sp.Float((sp.trace(D_KY) - XS / S).subs(pt)))),
        "T3_XdetGKY": float(xdet),
        "T3_area_nonconstant_flag": bool(abs(xdet) > NONZ),
        "XS_value": float(xsv),
    }
    ok = (res["T1_det_resid"] < TOL and res["T1_eigvec_resid"] < TOL and
          res["T1_rates_resid"] < TOL and res["T2_formula_resid"] < TOL and
          res["T2_K_eigvec_of_DKY_broken"] and res["T3_trace_resid"] < TOL and
          (res["T3_area_nonconstant_flag"] == (abs(xsv) > NONZ)))
    res["pass"] = bool(ok)
    num_ok = num_ok and ok
    numeric.append(res)

# Set B: alpha = 0, X(S) != 0 (3 points)
nb = 0
while nb < 3:
    pt = {u: rq(sp.Rational(1, 5), 3), b: rq(sp.Rational(1, 5), 3),
          f: rq(-2, 2), df: rq(-2, 2), db: rq_nonzero(-2, 2),
          chi: rq_nonzero(-2, 2), alpha: sp.Integer(0),
          c_E: rq_nonzero(sp.Rational(1, 2), 3)}
    xsv = sp.Float(XS.subs(pt))
    if abs(xsv) <= NONZ:
        continue
    nb += 1
    lam2 = sp.Float(D0[1, 1].subs(pt))
    pred = sp.Float((2 * chi + XS / S).subs(pt))
    xdet = sp.Float(X(G_KY.det()).subs(pt))
    res = {
        "point": {str(k): str(v) for k, v in pt.items()},
        "set": "B (alpha=0, X(S)!=0)",
        "T5a0_offdiag_resid": float(abs(sp.Float(D0[0, 1].subs(pt)))
                                    + abs(sp.Float(D0[1, 0].subs(pt)))),
        "T5a0_K_eigvec_of_DKY_holds": True,
        "T5a0_lam2_vs_2chi_plus_XSoverS_resid": float(abs(lam2 - pred)),
        "T5a0_rate_not_founded_flag": bool(abs(lam2 - sp.Float((2 * chi).subs(pt))) > NONZ),
        "T3_XdetGKY": float(xdet),
        "T3_area_nonconstant_flag": bool(abs(xdet) > NONZ),
        "XS_value": float(xsv),
    }
    ok = (res["T5a0_offdiag_resid"] < TOL and
          res["T5a0_lam2_vs_2chi_plus_XSoverS_resid"] < TOL and
          res["T5a0_rate_not_founded_flag"] and
          res["T3_area_nonconstant_flag"])
    res["pass"] = bool(ok)
    num_ok = num_ok and ok
    numeric.append(res)

record("NUMERIC_spot_checks", num_ok,
       "7 random admissible jet points (4 with alpha*df != 0: K-eigenline of "
       "span(K,Y) numerically broken, T2 formula confirmed; 3 with alpha=0, "
       "X(S) != 0: K-eigenline holds but area nonconstant and second rate "
       "off the founded value) -- all symbolic verdicts confirmed "
       "numerically; residuals < 1e-12, nonzero flags > 1e-6")

# ============================================================================
# Summary
# ============================================================================
all_pass = all(c["pass"] for c in checks)
summary = {
    "package": "udt_alpha_plane_selector_theorem_2026-07-28",
    "script": "derive_alpha_plane_selector.py",
    "date": "2026-07-28",
    "conventions": ("basis (K,W) columns; D = G^-1 X(G) acts left; K "
                    "eigenvector iff D[1,0] = 0; X-rules X(u)=-2*chi*u, "
                    "X(f)=df, X(b)=db, X(chi)=dchi (unused), "
                    "X(alpha)=X(c_E)=X(m)=X(n)=0"),
    "checks": checks,
    "numeric_points": numeric,
    "all_pass": bool(all_pass),
    "falsifier_FC_fired": bool(not all_pass),
}
out_path = os.path.join(HERE, "DERIVATION_RESULT.json")
with open(out_path, "w") as fh:
    json.dump(summary, fh, indent=2)
print()
print(json.dumps(summary, indent=2))
sys.exit(0 if all_pass else 1)
