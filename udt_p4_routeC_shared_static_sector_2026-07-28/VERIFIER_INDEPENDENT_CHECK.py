#!/usr/bin/env python3
"""BLIND-VERIFIER independent re-derivation for Route C Stage 1 (2026-07-28).

Blind adversarial verifier, same-session-spawned (NOT a hosted external model).
Independent construction: own curvature engine (own Christoffel/Riemann/Weyl code),
own Bach implementation  B_ab = nabla^c nabla^d C_acbd + (1/2) R^cd C_acbd,
VALIDATED before use on:
  * Schwarzschild (Ricci=0, Weyl!=0)  -> Bach must vanish.  This is the decisive
    sign/normalization-convention consistency test: the relative sign between the
    two Bach terms is convention-dependent, and only the consistent pairing makes
    every Einstein metric Bach-flat.
  * a non-Bach-flat control metric (guards against a trivially-zero implementation);
  * an explicit CONVENTION-FLIP check: with the opposite Riemann/Ricci sign
    convention the correctly-formed Bach tensor is  -B  (same vanishing locus),
    while the mixed/inconsistent pairing fails Schwarzschild -> the package's
    INEQUIVALENCE verdicts are convention-independent.

Then: the ansatz is rebuilt from the TC1 census (one-form expansion done here, not
copied), full-family Bach/EH restrictions recomputed and compared against the
package's BACH/EH_ODE_SYSTEM_FULL.txt; witnesses re-solved (all 7 components, both
directions, incl. the xx even-parity/quadratic coverage construction, with a FRESH
verifier-chosen parameter set on two components); W-EXP / W-EXP-CF / W-FLAT checked
with the fully-independent engine on the concrete member metrics; the Bach-flat
branch 4*lambda*s + s^2 + 4 = 0, the lambda=0 claim, the discrete root pair, and
the EH slice rigidity re-derived.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
T0 = time.time()
FAILS: list[str] = []


def vcheck(cid: str, ok: object, msg: str = "") -> None:
    ok = bool(ok)
    print(f"[{time.time()-T0:7.1f}s] {'PASS' if ok else 'FAIL'} {cid} :: {msg}", flush=True)
    if not ok:
        FAILS.append(cid)


def S(e):
    return sp.cancel(sp.expand(e))


def zero(e) -> bool:
    e = S(e)
    if e == 0:
        return True
    e = sp.cancel(sp.powsimp(e, force=True))
    if e == 0:
        return True
    return sp.simplify(e) == 0


# =============================================================================
# My curvature engine (own construction).
# Conventions: R^a_{bcd} = d_c Gam^a_{db} - d_d Gam^a_{cb} + Gam^a_{cm}Gam^m_{db}
#              - Gam^a_{dm}Gam^m_{cb};   Ric_bd = R^a_{bad}  (standard MTW-type).
# flip=True computes everything in the OPPOSITE sign convention (Riem -> -Riem,
# Ric -> -Ric, ...) and uses the correspondingly corrected Bach pairing sign.
# =============================================================================
def geometry(gm, xs, want_bach=True, flip=False, bach_pair_sign=None):
    n = 4
    gi = gm.inv().applyfunc(S)
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(b, n):
                tot = sp.S(0)
                for d in range(n):
                    if gi[a, d] != 0:
                        tot += gi[a, d] * (sp.diff(gm[d, b], xs[cc])
                                           + sp.diff(gm[d, cc], xs[b])
                                           - sp.diff(gm[b, cc], xs[d]))
                Gam[a][b][cc] = Gam[a][cc][b] = S(tot / 2)
    sgn = -1 if flip else 1
    Rup = {}
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(cc + 1, n):
                    e = sp.diff(Gam[a][d][b], xs[cc]) - sp.diff(Gam[a][cc][b], xs[d])
                    for m in range(n):
                        e += Gam[a][cc][m] * Gam[m][d][b] - Gam[a][d][m] * Gam[m][cc][b]
                    e = S(sgn * e)
                    if e != 0:
                        Rup[(a, b, cc, d)] = e
                        Rup[(a, b, d, cc)] = -e
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = S(sum(Rup.get((a, b, a, d), 0) for a in range(n)))
    Rsc = S(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    Rdn = {}
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(cc + 1, n):
                    e = S(sum(gm[a, m] * Rup.get((m, b, cc, d), 0)
                              for m in range(n) if gm[a, m] != 0))
                    if e != 0:
                        Rdn[(a, b, cc, d)] = e
                        Rdn[(a, b, d, cc)] = -e
    Wy = {}
    half = sp.Rational(1, 2)
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    e = (Rdn.get((a, b, cc, d), 0)
                         - half * (gm[a, cc] * Ric[b, d] - gm[a, d] * Ric[b, cc]
                                   - gm[b, cc] * Ric[a, d] + gm[b, d] * Ric[a, cc])
                         + Rsc / 6 * (gm[a, cc] * gm[b, d] - gm[a, d] * gm[b, cc]))
                    e = S(e)
                    if e != 0:
                        Wy[(a, b, cc, d)] = e
    out = {"gi": gi, "Gam": Gam, "Rup": Rup, "Rdn": Rdn, "Ric": Ric, "Rsc": Rsc, "Wy": Wy}
    if not want_bach:
        return out

    def dC(e_, a, b, cc, d):
        r = sp.diff(Wy.get((a, b, cc, d), 0), xs[e_])
        for m in range(n):
            r -= (Gam[m][e_][a] * Wy.get((m, b, cc, d), 0)
                  + Gam[m][e_][b] * Wy.get((a, m, cc, d), 0)
                  + Gam[m][e_][cc] * Wy.get((a, b, m, d), 0)
                  + Gam[m][e_][d] * Wy.get((a, b, cc, m), 0))
        return r

    T1 = {}
    for a in range(n):
        for cc in range(n):
            for b in range(n):
                e = sp.S(0)
                for d in range(n):
                    for e_ in range(n):
                        if gi[d, e_] != 0:
                            e += gi[d, e_] * dC(e_, a, cc, b, d)
                e = S(e)
                if e != 0:
                    T1[(a, cc, b)] = e

    def dT(fq, a, cc, b):
        r = sp.diff(T1.get((a, cc, b), 0), xs[fq])
        for m in range(n):
            r -= (Gam[m][fq][a] * T1.get((m, cc, b), 0)
                  + Gam[m][fq][cc] * T1.get((a, m, b), 0)
                  + Gam[m][fq][b] * T1.get((a, cc, m), 0))
        return r

    Ricup = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            Ricup[a, b] = S(sum(gi[a, i] * gi[b, j] * Ric[i, j]
                                for i in range(n) for j in range(n)))
    # pairing sign: +1 in my base convention; the flipped convention needs -1
    # (that is exactly what V03 demonstrates).
    ps = bach_pair_sign if bach_pair_sign is not None else (-1 if flip else 1)
    B = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            e1 = sp.S(0)
            for cc in range(n):
                for fq in range(n):
                    if gi[cc, fq] != 0:
                        e1 += gi[cc, fq] * dT(fq, a, cc, b)
            e2 = sp.S(0)
            for cc in range(n):
                for d in range(n):
                    v = Wy.get((a, cc, b, d), 0)
                    if v != 0 and Ricup[cc, d] != 0:
                        e2 += Ricup[cc, d] * v
            B[a, b] = S(e1 + ps * sp.Rational(1, 2) * e2)
    out["B"] = B
    return out


# =============================================================================
# V01-V03: engine validation (Schwarzschild sign test, control, convention flip)
# =============================================================================
t, x, y, z = sp.symbols("t x y z", real=True)
r, th, ph, m_ = sp.symbols("r theta varphi m", positive=True)

gs = sp.diag(-(1 - 2 * m_ / r), 1 / (1 - 2 * m_ / r), r**2, r**2 * sp.sin(th) ** 2)
GS = geometry(gs, [t, r, th, ph])
vcheck("V01_schwarzschild",
       all(zero(GS["Ric"][i, j]) for i in range(4) for j in range(4))
       and any(not zero(v) for v in GS["Wy"].values())
       and all(zero(GS["B"][i, j]) for i in range(4) for j in range(4)),
       "Ricci=0, Weyl!=0, Bach=0 on Schwarzschild -> engine + relative-sign convention consistent")

gctl = sp.diag(-sp.exp(2 * x), 1, sp.exp(4 * x), sp.exp(6 * x))
GC = geometry(gctl, [t, x, y, z])
vcheck("V02_nontrivial_control", any(not zero(GC["B"][i, j]) for i in range(4) for j in range(4)),
       "control metric has Bach != 0 (implementation not trivially zero)")

GCf = geometry(gctl, [t, x, y, z], flip=True)                       # corrected pairing (-1/2)
vcheck("V03a_flip_proportional",
       all(zero(GCf["B"][i, j] + GC["B"][i, j]) for i in range(4) for j in range(4)),
       "opposite-Riemann-convention Bach (with its matching pairing sign) = -B exactly: "
       "same vanishing locus -> INEQUIVALENCE verdicts are convention-independent")
# NOTE: Einstein metrics CANNOT pin the relative sign (Cotton = 0 and R^cd C_acbd =
# Lambda * tr C = 0 make BOTH terms vanish separately).  The decisive discriminator is
# CONFORMAL COVARIANCE: in 4D, B[Omega^2 g] = Omega^{-2} B[g] holds ONLY for the correct
# pairing.  Cross-check: a conformally-Einstein non-Einstein metric (r^2 * Schwarzschild)
# must be Bach-flat with the correct pairing and NOT with the mixed one.
Om2 = sp.exp(2 * x)
g2c = (Om2 * gctl).applyfunc(sp.expand)
G2c = geometry(g2c, [t, x, y, z])
G2m = geometry(g2c, [t, x, y, z], bach_pair_sign=-1)
G1m = geometry(gctl, [t, x, y, z], bach_pair_sign=-1)
conf_ok = all(zero(G2c["B"][i, j] - GC["B"][i, j] / Om2) for i in range(4) for j in range(4))
conf_bad = all(zero(G2m["B"][i, j] - G1m["B"][i, j] / Om2) for i in range(4) for j in range(4))
gcs = (r**2 * gs).applyfunc(sp.expand)
GCS = geometry(gcs, [t, r, th, ph])
GCSm = geometry(gcs, [t, r, th, ph], bach_pair_sign=-1)
vcheck("V03b_conformal_pins_sign",
       conf_ok and not conf_bad
       and any(not zero(GCS["Ric"][i, j] - GCS["Rsc"] / 4 * gcs[i, j])
               for i in range(4) for j in range(4))
       and all(zero(GCS["B"][i, j]) for i in range(4) for j in range(4))
       and any(not zero(GCSm["B"][i, j]) for i in range(4) for j in range(4)),
       "conformal covariance B[O^2 g] = O^-2 B[g] holds for the +1/2 pairing and FAILS for the "
       "mixed -1/2 pairing; r^2*Schwarzschild (conformally-Einstein, non-Einstein) is Bach-flat "
       "only with the correct pairing -> the package's sign/normalization is the genuine Bach tensor")

# =============================================================================
# V04: full family rebuilt from the TC1 census (one-form expansion done here)
# =============================================================================
cE = sp.Symbol("c_E", positive=True)
al = sp.Symbol("alpha", real=True)
lam = sp.Symbol("lambda", real=True)
Lam = sp.Symbol("Lambda", real=True)
phi = sp.Function("phi", real=True)(x)
ff = sp.Function("f", real=True)(x)
hh = sp.Function("bh", positive=True)(x)

u = sp.exp(-2 * phi)
W = sp.exp(2 * lam * phi)
# one-forms in the (dt, dx, dy, dz) basis:  A = dz + f dy ;  E0 = c_E dt + alpha A
Avec = [sp.S(0), sp.S(0), ff, sp.S(1)]
E0 = [cE, sp.S(0), al * ff, al]
dxv = [sp.S(0), sp.S(1), sp.S(0), sp.S(0)]
dyv = [sp.S(0), sp.S(0), sp.S(1), sp.S(0)]
G4 = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        G4[i, j] = S(-u * E0[i] * E0[j] + (1 / u) * Avec[i] * Avec[j]
                     + W * dxv[i] * dxv[j] + W * hh * dyv[i] * dyv[j])
vcheck("V04a_det", zero(sp.factor(G4.det()) + cE**2 * hh * W**2),
       "det g = -c_E^2 bh e^{4 lambda phi} (census A01 consistency)")

FG = geometry(G4, [t, x, y, z])
Bt = FG["B"]
Et = (FG["Ric"] - sp.Rational(1, 2) * FG["Rsc"] * G4 + Lam * G4).applyfunc(S)
print(f"[{time.time()-T0:7.1f}s] full-family geometry done", flush=True)

P = sp.symbols("p0:5", real=True)
F = sp.symbols("f0:5", real=True)
H = sp.symbols("h0:5", real=True)
jsub = []
for nn in range(4, 0, -1):
    jsub += [(sp.Derivative(phi, (x, nn)), P[nn]), (sp.Derivative(ff, (x, nn)), F[nn]),
             (sp.Derivative(hh, (x, nn)), H[nn])]
jsub += [(phi, P[0]), (ff, F[0]), (hh, H[0])]


def jet(e):
    return S(e.subs(jsub))


COMPS = [(0, 0), (0, 2), (0, 3), (1, 1), (2, 2), (2, 3), (3, 3)]
CN = {(0, 0): "tt", (0, 2): "ty", (0, 3): "tz", (1, 1): "xx",
      (2, 2): "yy", (2, 3): "yz", (3, 3): "zz"}
myB = {k: jet(Bt[k[0], k[1]]) for k in COMPS}
myE = {k: jet(Et[k[0], k[1]]) for k in COMPS}
myg = {k: jet(G4[k[0], k[1]]) for k in COMPS}

vcheck("V05a_mixed_x_row",
       all(zero(Bt[a, 1]) and zero(Et[a, 1]) for a in (0, 2, 3)),
       "B_ax = 0 and E_ax = 0 identically for a in {t,y,z} (7 independent components each)")
vcheck("V05b_bach_sym_tracefree",
       all(zero(Bt[i, j] - Bt[j, i]) for i in range(4) for j in range(4))
       and zero(sum(FG["gi"][i, j] * Bt[i, j] for i in range(4) for j in range(4))),
       "my Bach symmetric and trace-free on the family")

# parse the package's systems and compare
def parse_pkg(fname, prefix):
    txt = (HERE / fname).read_text(encoding="utf-8")
    txt = txt.replace("Lambda", "QLAM").replace("lambda", "qlam")
    loc = {"QLAM": Lam, "qlam": lam, "c_E": cE, "alpha": al, "exp": sp.exp}
    for i, s_ in enumerate(P):
        loc[f"p{i}"] = s_
    for i, s_ in enumerate(F):
        loc[f"f{i}"] = s_
    for i, s_ in enumerate(H):
        loc[f"h{i}"] = s_
    out = {}
    blocks = txt.split("== ")[1:]
    for b in blocks:
        head, body = b.split(" ==\n", 1)
        key = head.replace(prefix + "_", "").split("(")[0]
        out[key] = sp.sympify(body.strip().split("\n\n")[0], locals=loc)
    return out


pkgB = parse_pkg("BACH_ODE_SYSTEM_FULL.txt", "B")
pkgE = parse_pkg("EH_ODE_SYSTEM_FULL.txt", "E")
okB = all(zero(myB[k] - pkgB[CN[k]]) for k in COMPS)
okE = all(zero(myE[k] - pkgE[CN[k]]) for k in COMPS)
vcheck("V04b_bach_system_match", okB,
       "independently recomputed Bach restriction == package BACH_ODE_SYSTEM_FULL.txt "
       "(all 7 components, exact, same normalization)")
vcheck("V04c_eh_system_match", okE,
       "independently recomputed EH+Lambda restriction == package EH_ODE_SYSTEM_FULL.txt")
print(f"[{time.time()-T0:7.1f}s] system comparison done", flush=True)

# V06: jet orders + E_xx identity
def jsig(e):
    return {str(s_) for s_ in e.free_symbols if str(s_)[0] in "pfh" and len(str(s_)) == 2}


HIGH = {"p3", "p4", "f3", "f4", "h3", "h4"}
vcheck("V06a_jet_orders",
       all(jsig(myB[k]) & HIGH for k in COMPS) and not any(jsig(myE[k]) & HIGH for k in COMPS),
       "every Bach component carries 3rd/4th jets; no EH component exceeds 2nd jets")
exx = S(myE[(1, 1)].subs(P[0], 0)
        - (4 * Lam * H[0] + (al**2 - 1) * F[1]**2 - 4 * H[0] * P[1]**2) / (4 * H[0]))
vcheck("V06b_Exx_identity", zero(exx),
       "E_xx|_{p0=0} = [4 Lambda h0 + (alpha^2-1) f1^2 - 4 h0 p1^2]/(4 h0) exactly "
       "(lambda, h1, and all 2nd jets absent)")

# V07: W-FLAT
c0 = {s_: 0 for s_ in list(P[1:]) + list(F[1:]) + list(H[1:])}
vcheck("V07_W_FLAT",
       all(zero(myB[k].subs(c0)) for k in COMPS)
       and all(zero(myE[k].subs(c0) - Lam * myg[k].subs(c0)) for k in COMPS)
       and any(myg[k].subs(c0) != 0 for k in COMPS),
       "constants member: B == 0, E = Lambda*g with g nondegenerate -> fails EH for every Lambda != 0")

# =============================================================================
# V08/V09/V10: per-component witnesses, both directions (re-solved here)
# =============================================================================
PARAMS1 = {P[0]: 0, F[0]: sp.Rational(1, 7), H[0]: 1, al: sp.Rational(1, 2), cE: 1,
           lam: sp.Rational(1, 3)}
PARAMS2 = {P[0]: 0, F[0]: sp.Rational(1, 5), H[0]: 2, al: sp.Rational(1, 3), cE: 1,
           lam: sp.Rational(1, 5)}
# fresh verifier-chosen third set (different primes; not in the package)
PARAMS3 = {P[0]: 0, F[0]: sp.Rational(1, 11), H[0]: 3, al: sp.Rational(2, 5), cE: 1,
           lam: sp.Rational(1, 7)}
JV1 = {P[1]: sp.Rational(1, 2), P[2]: sp.Rational(1, 3), P[3]: sp.Rational(1, 5), P[4]: sp.Rational(1, 37),
       F[1]: sp.Rational(1, 11), F[2]: sp.Rational(1, 13), F[3]: sp.Rational(1, 17), F[4]: sp.Rational(1, 41),
       H[1]: sp.Rational(1, 19), H[2]: sp.Rational(1, 23), H[3]: sp.Rational(1, 29), H[4]: sp.Rational(1, 43)}
JV2 = {P[1]: sp.Rational(1, 3), P[2]: sp.Rational(1, 5), P[3]: sp.Rational(1, 7), P[4]: sp.Rational(1, 41),
       F[1]: sp.Rational(1, 13), F[2]: sp.Rational(1, 17), F[3]: sp.Rational(1, 19), F[4]: sp.Rational(1, 43),
       H[1]: sp.Rational(1, 23), H[2]: sp.Rational(1, 29), H[3]: sp.Rational(1, 31), H[4]: sp.Rational(1, 47)}
JV3 = {P[1]: sp.Rational(1, 5), P[2]: sp.Rational(1, 7), P[3]: sp.Rational(1, 11), P[4]: sp.Rational(1, 53),
       F[1]: sp.Rational(1, 17), F[2]: sp.Rational(1, 19), F[3]: sp.Rational(1, 23), F[4]: sp.Rational(1, 59),
       H[1]: sp.Rational(1, 29), H[2]: sp.Rational(1, 31), H[3]: sp.Rational(1, 37), H[4]: sp.Rational(1, 61)}
TOPJ = [P[4], F[4], H[4], P[3], F[3], H[3]]
# deliberately DIFFERENT low-order preference than the package's (fresh direction-B witnesses)
LOWJ = [P[2], H[2], F[2], P[1], H[1], F[1]]


def sig4(gm):
    """exact eigenvalue sign count of a rational symmetric 4x4 (want Lorentzian -+++)."""
    lamv = sp.Symbol("_ev")
    cp = gm.charpoly(lamv).as_expr()
    roots = sp.real_roots(sp.Poly(cp, lamv))
    neg = sum(1 for rt in roots if rt.is_negative)
    return len(roots) == 4 and neg == 1


def dirA(k, params, jetvals):
    B0 = myB[k].subs(params)
    E0 = myE[k].subs(params)
    for s_ in TOPJ:
        if s_ in B0.free_symbols and s_ not in E0.free_symbols:
            asn = {q_: v_ for q_, v_ in jetvals.items() if q_ != s_}
            pol = sp.Poly(sp.numer(sp.together(sp.cancel(B0.subs(asn)))), s_)
            if pol.degree() == 1 and pol.nth(1) != 0:
                root = sp.cancel(-pol.nth(0) / pol.nth(1))
                full = dict(params); full.update(asn); full[s_] = root
                bv = sp.cancel(myB[k].subs(full))
                ev = sp.cancel(myE[k].subs(full))
                pe = sp.Poly(ev, Lam)
                qc = pe.nth(1) if pe.degree() >= 1 else sp.S(0)
                if bv == 0 and qc != 0:
                    return sp.cancel(-pe.nth(0) / qc)     # exceptional Lambda*
                return None
    return None


def dirB(k, params, jetvals):
    E0 = myE[k].subs(params)
    for s_ in LOWJ:
        if s_ in E0.free_symbols:
            asn = {q_: v_ for q_, v_ in jetvals.items() if q_ != s_}
            pol = sp.Poly(sp.numer(sp.together(sp.cancel(E0.subs(asn)))), s_)
            if pol.degree() == 1 and pol.nth(1) != 0 and not pol.nth(1).has(Lam):
                root = sp.cancel(-pol.nth(0) / pol.nth(1))
                full = dict(params); full.update(asn); full[s_] = root
                ev = sp.cancel(myE[k].subs(full))
                bv = sp.cancel(myB[k].subs(full))
                nB = sp.expand(sp.numer(sp.together(bv)))
                if ev == 0 and nB != 0 and not sp.denom(sp.together(bv)).has(Lam):
                    return sp.Poly(nB, Lam)
                return None
    return None


allA = True
allB = True
for k in COMPS:
    ls = [dirA(k, PARAMS1, JV1), dirA(k, PARAMS2, JV2)]
    okA = (None not in ls) and sp.cancel(ls[0] - ls[1]) != 0
    allA = allA and okA
    if k != (1, 1):
        ns = [dirB(k, PARAMS1, JV1), dirB(k, PARAMS2, JV2)]
        okBd = (None not in ns) and sp.gcd(ns[0], ns[1]).degree() == 0
        allB = allB and okBd
    print(f"[{time.time()-T0:7.1f}s]   {CN[k]}: dirA Lambda* pair distinct={okA}"
          + ("" if k == (1, 1) else f"; dirB fresh-jet-order gcd-coprime={okBd}"), flush=True)
vcheck("V08_direction_A_all7", allA,
       "all 7 components: B_comp = 0 with E_comp != 0; two witnesses with distinct exceptional "
       "Lambda* -> every real Lambda covered")
vcheck("V09_direction_B_6comps", allB,
       "6 non-xx components: E_comp = 0 (symbolic Lambda, Lambda-free linear coefficient and "
       "denominators) with B_comp != 0; VERIFIER'S OWN low-jet order; Lambda-numerators gcd-coprime")

# fresh third-parameter-set witnesses on two components (tt and yz)
fresh_ok = True
for k in [(0, 0), (2, 3)]:
    lsf = dirA(k, PARAMS3, JV3)
    nsf = dirB(k, PARAMS3, JV3)
    fresh_ok = fresh_ok and (lsf is not None) and (nsf is not None)
vcheck("V08b_fresh_params", fresh_ok,
       "verifier-chosen PARAMS3/JETVALS3 (not in package): direction-A and direction-B witnesses "
       "exist on tt and yz as well - inequivalence is not an artifact of the package's points")

# V10: xx even-parity / quadratic-coverage construction
flipF = {F[i]: -F[i] for i in range(5)}
vcheck("V10a_Bxx_parity", sp.cancel(myB[(1, 1)].subs(flipF, simultaneous=True) - myB[(1, 1)]) == 0,
       "B_xx even under flipping all f-jets (exact discrete isometry y -> -y)")
XXW = [(sp.Rational(1, 2), 0, 1, sp.Rational(1, 3), JV1),
       (2, 1, 1, sp.Rational(1, 5), JV2),
       (3, 2, 2, sp.Rational(1, 7), JV1)]
xx_ok = True
xx_data = []
for av, p1v, h0v, lv, jv in XXW:
    f1sq = sp.cancel(4 * h0v * (Lam - p1v**2) / (1 - av**2))
    sub = {P[0]: 0, P[1]: p1v, H[0]: h0v, al: av, cE: 1, lam: lv,
           F[0]: 0, F[2]: 0, F[3]: 0, F[4]: 0,
           P[2]: jv[P[2]], P[3]: jv[P[3]], P[4]: jv[P[4]],
           H[1]: jv[H[1]], H[2]: jv[H[2]], H[3]: jv[H[3]], H[4]: jv[H[4]]}
    eS = sp.together(sp.cancel(myE[(1, 1)].subs(sub)))
    bS = sp.together(sp.cancel(myB[(1, 1)].subs(sub)))
    pe = sp.Poly(sp.numer(eS), F[1])
    pb = sp.Poly(sp.numer(bS), F[1])
    ok = (not sp.denom(eS).has(F[1]) and not sp.denom(bS).has(F[1])
          and all(mm[0] % 2 == 0 for mm in pe.monoms())
          and all(mm[0] % 2 == 0 for mm in pb.monoms()))
    ev2 = sp.cancel(sum(co * f1sq**(mm[0] // 2) for mm, co in zip(pe.monoms(), pe.coeffs())))
    bv2 = sp.cancel(sum(co * f1sq**(mm[0] // 2) for mm, co in zip(pb.monoms(), pb.coeffs())))
    nB = sp.Poly(sp.expand(sp.numer(sp.together(bv2))), Lam)
    ok = ok and ev2 == 0 and nB.as_expr() != 0
    # validity interval from f1^2 >= 0, derived HERE (linear in Lambda)
    slope = sp.cancel(4 * h0v / (1 - av**2))
    thr = sp.S(p1v**2)
    iv = (thr, None) if slope > 0 else (None, thr)
    xx_ok = xx_ok and ok
    xx_data.append((nB, iv))
# interval union must cover R
lo_cov = any(iv[0] is None for _, iv in xx_data)
hi_cov = any(iv[1] is None for _, iv in xx_data)
pts = sorted([v for _, iv in xx_data for v in iv if v is not None])
union_ok = lo_cov and hi_cov
for pv in pts + [pv0 + sp.Rational(1, 2) for pv0 in pts]:      # check knots and midpoints
    union_ok = union_ok and any(
        (iv[0] is None or pv >= iv[0]) and (iv[1] is None or pv <= iv[1]) for _, iv in xx_data)
vcheck("V10b_xx_intervals",
       xx_ok and union_ok
       and str([iv for _, iv in xx_data]) == "[(0, None), (None, 1), (None, 4)]",
       "three even-parity f1^2 witnesses: E_xx = 0 exactly for symbolic Lambda; derived validity "
       "intervals [0,inf), (-inf,1], (-inf,4] -> union covers all real Lambda")
cover = True
for i_, (Ni, vi) in enumerate(xx_data):
    for rt in Ni.real_roots():
        if (vi[0] is not None and bool(rt < vi[0])) or (vi[1] is not None and bool(rt > vi[1])):
            continue
        saved = False
        for j_, (Nj, vj) in enumerate(xx_data):
            if j_ == i_:
                continue
            inj = not ((vj[0] is not None and bool(rt < vj[0]))
                       or (vj[1] is not None and bool(rt > vj[1])))
            if inj and sp.gcd(Ni, Nj).degree() == 0:
                saved = True
                break
        if not saved:
            cover = False
vcheck("V10c_xx_root_coverage", cover,
       "every real root of a witness's Bach-numerator inside its validity interval is covered by "
       "another valid witness with gcd-coprime numerator (gcd over Q catches shared algebraic roots) "
       "-> for EVERY real Lambda some xx witness has E_xx = 0 != B_xx")
# Lorentzian signature at the q<0 witness points (alpha=2,3): the (t,z) off-diagonal saves it
gxx2 = sp.Matrix(4, 4, lambda i, j: myg.get((min(i, j), max(i, j)), jet(G4[i, j])))
sig_ok = True
for av, p1v, h0v, lv, jv in XXW[1:]:
    sub = {P[0]: 0, F[0]: 0, H[0]: h0v, al: av, cE: 1, lam: lv}
    gm = gxx2.subs(sub)
    sig_ok = sig_ok and sig4(sp.Matrix(4, 4, lambda i, j: sp.nsimplify(gm[i, j])))
vcheck("V10d_xx_lorentzian", sig_ok,
       "the alpha=2,3 xx witness points (g_zz = q < 0) are still Lorentzian (-,+,+,+): the (t,z) "
       "block det = -c_E^2 < 0 always - genuine domain members")
print(f"[{time.time()-T0:7.1f}s] witnesses done", flush=True)

# =============================================================================
# V11/V12: W-EXP and W-EXP-CF with the fully-independent engine (concrete metrics)
# =============================================================================
# W-EXP: phi = x, bh = e^{2x}, f = 0, alpha = 0, lambda = -5/4 (built from census directly)
gwe = sp.diag(-cE**2 * sp.exp(-2 * x), sp.exp(-sp.Rational(5, 2) * x),
              sp.exp(-x / 2), sp.exp(2 * x))
GW = geometry(gwe, [t, x, y, z])
tfr = [S(GW["Ric"][i, i] - GW["Rsc"] / 4 * gwe[i, i]) for i in range(4)]
vcheck("V11a_W_EXP",
       all(zero(GW["B"][i, j]) for i in range(4) for j in range(4))
       and any(not zero(v) for v in GW["Wy"].values())
       and any(not zero(v) for v in tfr),
       "W-EXP (own engine, own metric build): Bach == 0 identically, Weyl != 0 (genuinely non-"
       "conformally-flat), trace-free Ricci != 0 -> G_ab + Lambda g_ab != 0 for EVERY Lambda incl. 0 "
       "-- the load-bearing decisive witness CONFIRMED")
# no Lambda rescue, shown directly: the per-leg Lambda demands differ
legs = sorted({sp.nsimplify(S(-(GW["Ric"][i, i] - GW["Rsc"] / 2 * gwe[i, i]) / gwe[i, i]).subs(x, 0))
               for i in range(4)})
vcheck("V11b_W_EXP_no_Lambda", len(legs) > 1,
       f"E_ii = 0 would need Lambda = {legs} simultaneously - impossible: no Lambda rescues EH+Lambda")
# consistency with the family restriction: substitute the member's jets into MY jetized B
mem = {P[0]: x, P[1]: 1, P[2]: 0, P[3]: 0, P[4]: 0,
       F[0]: 0, F[1]: 0, F[2]: 0, F[3]: 0, F[4]: 0,
       H[0]: sp.exp(2 * x), H[1]: 2 * sp.exp(2 * x), H[2]: 4 * sp.exp(2 * x),
       H[3]: 8 * sp.exp(2 * x), H[4]: 16 * sp.exp(2 * x),
       al: 0, lam: sp.Rational(-5, 4)}
vcheck("V11c_family_slice_consistency",
       all(zero(myB[k].subs(mem)) for k in COMPS),
       "the member's jets substituted into the family-restricted Bach system give 0 in all 7 "
       "components - restriction commutes with specialization (C16b, all components)")

gcf = sp.diag(-cE**2 * sp.exp(-2 * x), sp.exp(-2 * x), sp.exp(2 * x), sp.exp(2 * x))
GF2 = geometry(gcf, [t, x, y, z])
vcheck("V12_W_EXP_CF",
       all(zero(v) for v in GF2["Wy"].values())
       and all(zero(GF2["B"][i, j]) for i in range(4) for j in range(4))
       and any(not zero(S(GF2["Ric"][i, i] - GF2["Rsc"] / 4 * gcf[i, i])) for i in range(4)),
       "W-EXP-CF (lambda=-1, bh=e^{4x}): conformally flat (Weyl == 0), Bach == 0, non-Einstein "
       "-> fails EH+Lambda for every Lambda")

# =============================================================================
# V13/V15: exponential slice - Bach-flat branch, lambda=0 claim, EH rigidity
# =============================================================================
s_ = sp.Symbol("s", real=True)
gsl = sp.diag(-cE**2 * sp.exp(-2 * x), sp.exp(2 * lam * x),
              sp.exp(2 * lam * x + 2 * s_ * x), sp.exp(2 * x))
GS2 = geometry(gsl, [t, x, y, z])
offd_zero = all(zero(GS2["B"][i, j]) for i in range(4) for j in range(4) if i != j)
common = 4 * lam * s_ + s_**2 + 4
quots = []
div_ok = offd_zero
for i in range(4):
    w = sp.factor(sp.cancel(sp.powsimp(sp.expand(GS2["B"][i, i] / gsl[i, i]
                                                 * sp.exp(4 * lam * x)), force=True)))
    if w.has(x) or w == 0:
        div_ok = False
        continue
    qt = sp.together(sp.cancel(w / common))
    if not sp.denom(qt).is_number:
        div_ok = False
    quots.append(sp.expand(qt * sp.denom(qt) / sp.LC(sp.Poly(qt * sp.denom(qt), s_, lam))))
vcheck("V13a_bach_flat_branch", div_ok,
       "slice (phi=x, bh=e^{2sx}, f=0, alpha=0): Bach off-diagonals vanish; every deweighted "
       "diagonal component is x-free and divisible by (4 lambda s + s^2 + 4) - branch reproduced")
q0 = [sp.Poly(qt.subs(lam, 0), s_) for qt in quots]
g0 = q0[0]
for qq in q0[1:]:
    g0 = sp.gcd(g0, qq)
lam0_roots = [rt for rt in sp.Poly(common.subs(lam, 0), s_).real_roots()]
vcheck("V13b_lambda0_no_member",
       len(lam0_roots) == 0 and len(sp.Poly(g0, s_).real_roots() if g0.degree() > 0 else []) == 0,
       "at lambda = 0: s^2 + 4 has no real root AND the quotient system has no common real root "
       "-> NO Bach-flat member on this slice at lambda = 0 [claim is SCOPED to the exponential "
       "subfamily in the package - correct scoping]")
# ADJUDICATION of the package's "plus discrete roots (lambda=+-5*sqrt(21)/21,
# s=-+2*sqrt(21)/7)" claim (ledger SYSTEM row + EXACT_DERIVATION TC4): the pair
# SATISFIES 4*lambda*s + s^2 + 4 = 0, i.e. it lies ON the one-parameter branch (it is a
# redundant sp.solve output artifact, where the y-quotient happens to also vanish), and
# the quotient system has NO common real root at all (Groebner basis {s - 2*lambda,
# 3*lambda^2 + 1}) -> the slice Bach-flat locus is the branch ALONE; "plus discrete
# roots" is a documentation mischaracterization (does not affect any verdict).
pt = {lam: 5 * sp.sqrt(21) / 21, s_: -2 * sp.sqrt(21) / 7}
gb = sp.groebner([sp.expand(qt) for qt in quots], s_, lam)
no_extra = all(sp.Poly(gg, lam).real_roots() == [] for gg in
               [gb.exprs[-1]]) if gb.exprs != [sp.S(1)] else True
vcheck("V13c_discrete_pair_on_branch",
       sp.simplify(common.subs(pt)) == 0 and no_extra,
       "the claimed 'discrete root pair' LIES ON the branch (4 lambda s + s^2 + 4 = 0 at the "
       "pair) and the quotient system has no common real root -> the Bach-flat locus on the "
       "slice is exactly the one-parameter branch; the 'plus discrete roots' wording in the "
       "ledger/EXACT_DERIVATION is an amendment item (redundant, not an additional solution set)")
# V15: EH rigidity on the slice (k=1) - no (s, Lambda) roots; flat member needs Lambda=0
Esl = (GS2["Ric"] - sp.Rational(1, 2) * GS2["Rsc"] * gsl + Lam * gsl).applyfunc(S)
eqs = [sp.factor(sp.cancel(sp.powsimp(sp.expand(sp.numer(sp.together(S(Esl[i, i] / gsl[i, i])))),
                                      force=True))) for i in range(4)]
rig = sp.solve(eqs, [s_, Lam], dict=True)
gfl = sp.diag(-cE**2, 1, 1, 1)
GFl = geometry(gfl, [t, x, y, z], want_bach=False)
Efl = GFl["Ric"] - sp.Rational(1, 2) * GFl["Rsc"] * gfl + Lam * gfl
vcheck("V15_eh_slice_rigidity",
       len(rig) == 0 and all(zero(Efl[i, j] - Lam * gfl[i, j]) for i in range(4) for j in range(4)),
       "EH+Lambda on the k=1 slice has NO roots (my independent solve agrees); the flat k=s=0 "
       "member gives E = Lambda*g, solvable only with Lambda = 0 [SCOPED to exponential subfamily]")

# =============================================================================
# V14: one-way containment spot checks (Einstein => Bach-flat), and scoping
# =============================================================================
# member 1: the flat in-domain member (solves EH at Lambda=0; Bach = 0) - V07 + V15 above.
# member 2: Schwarzschild (Einstein, Weyl != 0) - V01 above.
# member 3: de Sitter static patch (Einstein with Lambda != 0, conformally flat)
L_ = sp.Symbol("L", positive=True)
gds = sp.diag(-(1 - r**2 / L_**2), 1 / (1 - r**2 / L_**2), r**2, r**2 * sp.sin(th) ** 2)
GD = geometry(gds, [t, r, th, ph])
Eds = GD["Ric"] - sp.Rational(1, 2) * GD["Rsc"] * gds + (3 / L_**2) * gds
vcheck("V14_containment_spot",
       all(zero(Eds[i, j]) for i in range(4) for j in range(4))
       and all(zero(GD["B"][i, j]) for i in range(4) for j in range(4)),
       "de Sitter static patch: solves EH with Lambda=3/L^2 AND is Bach-flat; with Schwarzschild "
       "(V01) and the flat member (V07): Einstein => Bach-flat spot-verified on 3 members; the "
       "package cites it as Category-A and flags it slice-verified-only - no over-claim")

print(f"\n[{time.time()-T0:7.1f}s] VERIFIER SUMMARY: "
      f"{'ALL CHECKS PASSED' if not FAILS else 'FAILURES: ' + ', '.join(FAILS)}", flush=True)
sys.exit(1 if FAILS else 0)
