#!/usr/bin/env python3
"""
W2 ARM-2 — SCRIPT 4: SEAL-LAW JET-ENTRY ADJUDICATOR (fast companion
to w2_arm2_shaped_seal.py TRACK 2).  Date: 2026-06-11.  METRIC-LED.

QUESTION (FC-1 robustness): on the FULL axis-regular shaped class
  f = a(y) + b(y)(1-u) + b2(y)(1-u)^2,
  w = om(y)(1-u) + om2(y)(1-u)^2,        u = cos(theta), q = 0,
does the in-ansatz on-axis seal law  f^2 K -> 4 f_u(pole)^2/y^4
(mass_audit erratum of record) acquire dependence on ANY other jet —
the w transverse jets (om, om2), their radial derivatives, the second
f transverse jet (b2), or the radial f jets — at the singular order?

METHOD: exact rational arithmetic only (zero floating point); A (the
pole value of f) kept symbolic; every other jet at generic exact
rationals; per-term gcd-free trailing-coefficient axis limits in
v = 1 - u; Laurent order and leading coefficient in A extracted
polynomially.  Toggle test (om2 = b2 = 0 vs generic) at one point +
an independent second point with ALL jets different and om large
(om = 7/3 — far from the perturbative regime; principle 2 honored:
this is exact nonlinear evaluation, not linearization).

ADJUDICATION (pre-registered FC-1, recorded in all w2_arm2 scripts):
if the law at both points equals 4 B^2/y^4 exactly with zero ON-OFF
difference, the seal singularity is w-BLIND on the full class ->
scoped negative for FC-1 (premise set: static diagonal+w class,
q = 0, axis-regular polynomial-in-(1-u) profiles through order 2,
in-ansatz pole touchdown a -> 0 with transverse jets finite).
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"J-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, y, u, ph = sp.symbols('T y u phi')
xs = [T, y, u, ph]
v = sp.Symbol('v', positive=True)
A = sp.Symbol('A', real=True)
R = sp.Rational

def law_at(omv, om2v, bv, b2v, omp, om2p, bp, b2p,
           omp2, om2p2, bp2, b2p2, ap, ap2, yv):
    """Exact (singular order, leading Laurent coefficient in A) of
    K_axis for the full shaped class at rational jets, A symbolic."""
    a = sp.Function('a')(y); b = sp.Function('b')(y)
    b2f = sp.Function('b2')(y)
    om = sp.Function('om')(y); om2f = sp.Function('om2')(y)
    fF = a + b*(1 - u) + b2f*(1 - u)**2
    wF = om*(1 - u) + om2f*(1 - u)**2
    g = sp.diag(-fF, 1/fF, y**2*(1 + wF)**2/(1 - u**2),
                y**2*(1 - u**2)/(1 + wF)**2)
    guu = g.inv()
    Gam = [[[sp.cancel(sum(guu[a_, d]*(sp.diff(g[d, b_], xs[c])
            + sp.diff(g[d, c], xs[b_]) - sp.diff(g[b_, c], xs[d]))
            for d in range(4))/2) for c in range(4)] for b_ in range(4)]
           for a_ in range(4)]
    Riem = [[[[sp.diff(Gam[a_][b_][d2], xs[c])
               - sp.diff(Gam[a_][b_][c], xs[d2])
               + sum(Gam[a_][e][c]*Gam[e][b_][d2]
                     - Gam[a_][e][d2]*Gam[e][b_][c] for e in range(4))
               for d2 in range(4)] for c in range(4)]
              for b_ in range(4)] for a_ in range(4)]
    sub = {sp.Derivative(a, (y, 2)): ap2, sp.Derivative(a, y): ap,
           sp.Derivative(b, (y, 2)): bp2, sp.Derivative(b, y): bp,
           sp.Derivative(b2f, (y, 2)): b2p2, sp.Derivative(b2f, y): b2p,
           sp.Derivative(om, (y, 2)): omp2, sp.Derivative(om, y): omp,
           sp.Derivative(om2f, (y, 2)): om2p2,
           sp.Derivative(om2f, y): om2p,
           a: A, b: bv, b2f: b2v, om: omv, om2f: om2v, y: yv}
    tot = sp.Integer(0)
    for a_ in range(4):
        for b_ in range(4):
            for c in range(4):
                for d in range(4):
                    t1 = sum(g[a_, e]*Riem[e][b_][c][d]
                             for e in range(4))
                    if t1 == 0:
                        continue
                    fac = guu[a_, a_]*guu[b_, b_]*guu[c, c]*guu[d, d]
                    cv = t1.xreplace(sub).subs(u, 1 - v)
                    fv = fac.xreplace(sub).subs(u, 1 - v)
                    cn, cd = sp.fraction(sp.together(cv))
                    fn, fd = sp.fraction(sp.together(fv))
                    N = sp.Poly(cn, v, A)**2*sp.Poly(fn, v, A)
                    D = sp.Poly(cd, v, A)**2*sp.Poly(fd, v, A)
                    if N.is_zero:
                        continue
                    tN = min(m[0] for m in N.monoms())
                    tD = min(m[0] for m in D.monoms())
                    if tN > tD:
                        continue
                    assert tN == tD, "axis-divergent term (illegal)"
                    cN = sum(co*A**m[1] for m, co in N.terms()
                             if m[0] == tN)
                    cD = sum(co*A**m[1] for m, co in D.terms()
                             if m[0] == tD)
                    tot += sp.cancel(cN/cD)
    Kax = sp.cancel(sp.together(tot))
    n_, d_ = sp.fraction(Kax)
    pn = sp.Poly(n_, A); pd = sp.Poly(d_, A)
    tn = min(m[0] for m in pn.monoms())
    td = min(m[0] for m in pd.monoms())
    law = sp.cancel(pn.coeff_monomial(A**tn)/pd.coeff_monomial(A**td))
    return tn - td, law

# point 1, base jets (generic rationals), om2 = b2 = 0 vs ON:
base = dict(omv=R(2, 5), bv=R(-4, 3), omp=R(-5, 7), bp=R(2, 7),
            omp2=R(3, 4), bp2=R(-1, 6), ap=R(-7, 5), ap2=R(9, 4),
            yv=R(13, 10))
o1, l1 = law_at(om2v=R(0), b2v=R(0), om2p=R(0), b2p=R(0),
                om2p2=R(0), b2p2=R(0), **base)
o2, l2 = law_at(om2v=R(-1, 3), b2v=R(5, 9), om2p=R(4, 11),
                b2p=R(-3, 8), om2p2=R(-2, 9), b2p2=R(1, 5), **base)
pred1 = 4*base['bv']**2/base['yv']**4
check("1", o1 == -2 and o2 == -2,
      f"singular order A^(-2) with om2/b2 OFF and ON (got {o1}, {o2})")
check("2", sp.simplify(l2 - l1) == 0,
      "ON - OFF law difference = 0: the second transverse jets "
      "(b2, om2) and their radial derivatives do NOT enter the "
      "singular order")
check("3", sp.simplify(l1 - pred1) == 0 and sp.simplify(l2 - pred1) == 0,
      f"law = 4 B^2/y^4 = {pred1} exactly at point 1 (w-jet present: "
      f"om = 2/5, om' = -5/7, om'' = 3/4 — none enter)")

# point 2: all jets different, om LARGE (7/3 — nonperturbative):
base2 = dict(omv=R(7, 3), bv=R(1, 2), omp=R(5, 2), bp=R(-1, 9),
             omp2=R(-3, 5), bp2=R(2, 3), ap=R(11, 6), ap2=R(-4, 7),
             yv=R(3, 4))
o3, l3 = law_at(om2v=R(6, 7), b2v=R(-2, 5), om2p=R(1, 8),
                b2p=R(3, 10), om2p2=R(5, 12), b2p2=R(-1, 7), **base2)
pred2 = 4*base2['bv']**2/base2['yv']**4
check("4", o3 == -2 and sp.simplify(l3 - pred2) == 0,
      f"independent point 2 (om = 7/3, all jets new): order A^(-2), "
      f"law = 4 B^2/y^4 = {pred2} exactly. FC-1 ADJUDICATED: THE "
      f"IN-ANSATZ SEAL SINGULARITY LAW IS w-BLIND ON THE FULL "
      f"AXIS-REGULAR SHAPED CLASS (scoped negative; premise set in "
      f"header)")

print(f"\nSEAL-LAW ADJUDICATOR: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
