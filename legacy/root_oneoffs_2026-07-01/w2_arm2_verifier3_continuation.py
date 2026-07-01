#!/usr/bin/env python3
"""
W2 ARM-2 BLIND ADVERSARIAL VERIFIER — SCRIPT 3: THE CONTINUATION
EXHIBIT (claim 2).  Date: 2026-06-12.  Independent machinery.

ATTACKS (attack D of the verification charter):
 D1. EL equations derived from the COVARIANT C1 density
       L = -(c/2) sqrt(-g) g^{mu nu} phi_mu phi_nu,
       phi = -(1/2) ln f
     on the FULL static (f, q, w) P1 class (q off-diagonal kept,
     nothing reduced by hand), all three channels, exact; the arm
     verified its exhibits against the reduced density only (its I3
     EL_f/EL_w use L_full at q = 0; EL_q used L_P1 — here all three
     come from ONE covariant object).
 D2. Both exhibits (w = 0 and w = bump*sin^2 th) checked as exact
     statics of that covariant system.
 D3. JET-SCOPING STRENGTHENED: a C-infinity bump flat to ALL orders
     at the interface (exp(-1/x) species) — if it is also an exact
     static, the continuation failure is NOT a 2nd-order-jet artifact:
     even ALL-ORDER jet data fails to pin the bulk w.  (This UPGRADES
     the arm's "through 2nd order" scoping.)
 D4. The f-sector mirror statement: on the same class the f-channel
     interface jet (f, f_r)(r0) DOES pin the exterior uniquely within
     the spherical solution family (2-parameter family vs 2 jet
     numbers) — the asymmetry the arm asserts.
 D5. Axis regularity of the shaped exhibit (w ~ sin^2 th => w ~ th^2:
     quadratic closure, elementary-flatness compliant).
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V3-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th, ph = sp.symbols('T r theta phi')
c = sp.Symbol('c')
fq = sp.Function('f')(r, th)
qq = sp.Function('q')(r, th)
wq = sp.Function('w')(r, th)

# the full static P1 metric (q off-diagonal in (r, th)):
W = (1 + wq)**2
g = sp.Matrix([[-fq, 0, 0, 0],
               [0, 1/fq, qq, 0],
               [0, qq, r**2*W, 0],
               [0, 0, 0, r**2*sp.sin(th)**2/W]])
detg = sp.together(g.det())
sqrtmg = sp.sqrt(-detg)
gi = g.inv()
phi = -sp.log(fq)/2
phid = [sp.Integer(0), sp.diff(phi, r), sp.diff(phi, th), sp.Integer(0)]
quad = sum(gi[i, j]*phid[i]*phid[j] for i in range(4) for j in range(4))
# the native C1 density carries the dilation weight f (banked form,
# pde_p1 D-06 / ground-anchors C2: L = -(c/2) f sqrt(-g) (grad phi)^2):
L = -(c/2)*fq*sqrtmg*quad
check("D0", all(d.expr not in (qq, wq) for d in L.atoms(sp.Derivative)),
      "covariant C1 on the full (f,q,w) class: NO q- or w-derivative "
      "atom (pi_q = pi_w = 0 holds covariantly, not just reduced)")

def EL(L, field):
    e = sp.diff(L, field)
    for x in (r, th):
        e -= sp.diff(sp.diff(L, sp.Derivative(field, x)), x)
        e += sp.diff(sp.diff(L, sp.Derivative(field, (x, 2))), x, 2)
    return e

EL_f = EL(L, fq)
EL_q = EL(L, qq)
EL_w = EL(L, wq)
print(f"[t={time.time()-t0:.0f}s] covariant EL built.", flush=True)

# exhibits
Cs, am, r0, r1 = sp.symbols('C a_m r0 r1', positive=True)
fsol = Cs + am/r
bump = ((r - r0)**3*(r1 - r)**3)/(r1 - r0)**6
wII = bump*sp.sin(th)**2
# D3: the all-orders-flat bump (C^inf, supported in (r0, r1)):
wIII_core = sp.exp(-1/(r - r0))*sp.exp(-1/(r1 - r))*sp.sin(th)**2

for tag, wpick in (("I  (w=0)      ", sp.Integer(0)),
                   ("II (C2 bump)  ", wII),
                   ("III(flat bump)", wIII_core)):
    sub = {fq: fsol, qq: sp.Integer(0), wq: wpick}
    vals = [sp.simplify(e.subs(sub).doit()) for e in (EL_f, EL_q, EL_w)]
    check(f"D2-{tag.strip()}", all(vv == 0 for vv in vals),
          f"exhibit {tag}: EL_f = EL_q = EL_w = 0 from the COVARIANT "
          f"C1 (all three channels exact)")

# D3: all-orders flatness of the exp bump at the interface r = r0:
x = sp.Symbol('x', positive=True)
core = sp.exp(-1/x)
flat = all(sp.limit(sp.diff(core, x, n), x, 0, '+') == 0
           for n in range(0, 5))
check("D3a", flat,
      "exp(-1/(r-r0)) is flat to (at least) 4th order at r0+ (standard "
      "all-orders flatness): exhibit III matches exhibit I's interface "
      "jet TO ALL ORDERS")
mid = (r0 + r1)/2
val_mid = wIII_core.subs([(r, mid), (th, sp.pi/2)])
check("D3b", sp.simplify(val_mid) != 0 and
      sp.simplify(val_mid - sp.exp(-4/(r1 - r0))) == 0,
      f"exhibit III is nonzero in the bulk (midpoint value "
      f"e^(-4/(r1-r0))): UNIQUE CONTINUATION FAILS EVEN WITH ALL-ORDER "
      f"JET DATA — claim 2's 'through 2nd order' scoping can be "
      f"STRENGTHENED to all orders (amendment, favorable)")

# D4: the f-sector contrast: spherical family f = C + a/r; the
# interface jet (f, f_r)(r0) determines (C, a) uniquely:
F0, F1 = sp.symbols('F0 F1')
solset = sp.solve([sp.Eq(fsol.subs(r, r0), F0),
                   sp.Eq(sp.diff(fsol, r).subs(r, r0), F1)],
                  [Cs, am], dict=True)
check("D4", len(solset) == 1 and
      sp.simplify(solset[0][am] + F1*r0**2) == 0,
      "f-channel: the interface jet (f, f_r) pins the spherical "
      "exterior UNIQUELY (a = -F1 r0^2, C = F0 + F1 r0): the "
      "continuation asymmetry between the f- and w-channels is real")

# D5: axis regularity of the shaped exhibits:
for tag, wpick in (("II", wII), ("III", wIII_core)):
    w_ax = wpick.subs(th, 0)
    w_ax1 = sp.diff(wpick, th).subs(th, 0)
    w_ax2 = sp.diff(wpick, th, 2).subs(th, 0)
    check(f"D5-{tag}", sp.simplify(w_ax) == 0 and
          sp.simplify(w_ax1) == 0 and sp.simplify(w_ax2) != 0,
          f"exhibit {tag}: w = 0 on the axis with quadratic closure "
          f"(w ~ th^2): elementary-flatness compliant")

print(f"\nVERIFIER-3 (continuation): {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
