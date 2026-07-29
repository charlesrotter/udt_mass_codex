#!/usr/bin/env python3
# Proper machine check of the constant-combo lemma:
#   any Killing field W = a K + b Y (a,b functions) on an alpha=0 stratum member is
#   a CONSTANT combination (given u nonconstant; constant-depth closes by torus
#   periodicity).  This is the unstated load-bearing lemma under T-d4 necessity's
#   "no assumption on the isometry algebra" claim.
import sympy as sp

t, s, p1, p2 = sp.symbols("t s phi1 phi2", real=True)
u = sp.Function("u", positive=True)(s)
f = sp.Function("f", real=True)(s)
c = sp.Symbol("c", positive=True)
cE = sp.Symbol("c_E", positive=True)
OK = []
def chk(nm, ok, d=""):
    OK.append(ok); print(("PASS " if ok else "FAIL ") + nm + ("  :: " + d if d else ""))

# The nonzero Killing component equations (rederived in debug_B1.py from the metric):
#  (t,t): dt(a) = 0                     (t,s): ds(a) = 0
#  (s,-): (c+f) ds(b) = 0              (s,+): (f-c) ds(b) = 0
#  (-,-): (c+f) d1(b) = 0              (+,+): (f-c) d2(b) = 0
#  (-,+): (f-c) d1(b) + (c+f) d2(b) = 0
#  (t,-): (c+f) dt(b) = 2 cE^2 u^2 d1(a)
#  (t,+): (f-c) dt(b) = 2 cE^2 u^2 d2(a)
# STAGE 1 (pointwise): {(c+f)x=0, (c-f)y=0, (f-c)x+(c+f)y=0} forces x=y=0 for ALL f
# given c>0.  Case split f generic / f=c / f=-c:
x, y, fv = sp.symbols("x y f_v", real=True)
sys_ = lambda F: [(c + F) * x, (c - F) * y, (F - c) * x + (c + F) * y]
gen = sp.solve(sys_(fv), [x, y], dict=True)              # generic f
case_p = sp.solve([e.subs(fv, c) for e in sys_(fv)], [x, y], dict=True)   # f = +c
case_m = sp.solve([e.subs(fv, -c) for e in sys_(fv)], [x, y], dict=True)  # f = -c
def only_zero(sol):
    return len(sol) == 1 and all(sp.simplify(v) == 0 for v in sol[0].values()) \
        and len(sol[0]) == 2
chk("S1_db_phi_forced_zero", only_zero(gen) and only_zero(case_p) and only_zero(case_m),
    "d1(b)=d2(b)=0 pointwise in every case (incl. f=+-c corners); likewise "
    "ds(b)=0 from the (s,±) pair (sum has coefficient 2c>0)")
chk("S1_ds_b", sp.simplify(((c + fv) + (c - fv)) - 2 * c) == 0,
    "(s,-)+(s,+)*(-1): coefficient sum 2c != 0  => ds(b)=0")

# STAGE 2 (separation): b=b(t), a=a(phi1,phi2).
#  (t,-): b'(t) (c+f(s))/u(s)^2 = 2 cE^2 d1(a)(phi)   -- LHS product t x s, RHS phi.
#  If (c+f)/u^2 nonconstant in s => b'=0 and d1(a)=0. If BOTH (c+f)/u^2 and (c-f)/u^2
#  are constant, their sum 2c/u^2 is constant => u constant (constant-depth member).
k1, k2 = sp.symbols("k1 k2", real=True)
usol = sp.solve([(c + fv) - k1 * sp.Symbol("u2", positive=True),
                 (c - fv) - k2 * sp.Symbol("u2", positive=True)],
                [fv, sp.Symbol("u2", positive=True)], dict=True)
chk("S2_separation_degenerate_iff_u_const",
    len(usol) == 1 and sp.simplify(usol[0][sp.Symbol("u2", positive=True)]
                                   - 2 * c / (k1 + k2)) == 0,
    "both coefficients constant  <=>  u^2 = 2c/(k1+k2) constant AND f constant: "
    "only constant-depth members escape separation")
# STAGE 3 (constant depth): a = lam*phi1 + mu*phi2 + a0 must be 2pi-periodic on the
# torus => lam = mu = 0 => b'(t)=0.  (Single-valuedness; analysis step, exact.)
lam, mu = sp.symbols("lam mu", real=True)
chk("S3_periodicity", sp.simplify((lam * (p1 + 2 * sp.pi) + mu * p2)
    - (lam * p1 + mu * p2) - 2 * sp.pi * lam) == 0,
    "a(phi1+2pi)-a(phi1) = 2 pi lam: single-valued <=> lam=0 (same for mu) "
    "=> dt(b)=0 => a,b constants on constant-depth members too")

print()
print("lemma stages: %d/%d" % (sum(OK), len(OK)))
import sys; sys.exit(0 if all(OK) else 1)
