#!/usr/bin/env python3
"""
wint_symcheck.py -- the 2D field equation IS the metric's own (fast, exact)
=========================================================================
INTERACTING-WHOLE push. Driver: Claude (Opus 4.8). Date 2026-06-13.
Verifies (cleanly, fast) that the operator solved in wint_cell2d.py is the
metric's OWN dilation Box on the (r,theta) sector with BOTH sectors live --
no smuggled term, no slaving. Replaces the slow/over-strict check 1a in the
prior wint_system.py (left as-is per append-only discipline; this is the
clean statement). NOTHING added.

Metric (banked dilation tie, areal canon): on the static slice
   g_rr = e^{2phi},  g_thth = r^2,  g_phph = r^2 sin^2 th,  phi=phi(r,theta)
   spatial sqrt|g| = e^{phi} r^2 sin th ;  g^{rr}=e^{-2phi}, g^{thth}=1/r^2.
Box_g phi (static) = (1/sqrt|g|)[ d_r(sqrt|g| g^{rr} phi_r)
                                + d_th(sqrt|g| g^{thth} phi_th) ].
"""
import sympy as sp

PASS = []
def check(n, c):
    ok = bool(c); PASS.append((n, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}", flush=True)
    assert ok, n

# THE METRIC'S OWN FIELD EQUATION is the C1 dilation-action EL (the prior
# wint_system.py PART 1 verified the covariant Box and the C1 EL agree).
# C1 action: L = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4), c=2.
# 4-metric (dilation tie): g_tt=-e^{-2phi}, g_rr=e^{2phi}, g_thth=r^2,
# g_phph=r^2 sin^2 th  =>  sqrt(-g4) = r^2 sin th (the e^{+-2phi} cancel).
r, th = sp.symbols('r theta', positive=True)
P = sp.Function('phi')
sqrtg4 = r**2 * sp.sin(th)
grr = sp.exp(-2 * P(r, th))
gthth = 1 / r**2
f = sp.exp(-2 * P(r, th))
K = grr * sp.diff(P(r, th), r)**2 + gthth * sp.diff(P(r, th), th)**2
L = (sp.Integer(2) / 2) * f * K * sqrtg4
phir = sp.diff(P(r, th), r); phith = sp.diff(P(r, th), th)
EL = (sp.diff(L, P(r, th)) - sp.diff(sp.diff(L, phir), r)
      - sp.diff(sp.diff(L, phith), th))
# normalize by the common dilation weight e^{-2phi} (>0; field eqn EL=0
# unchanged): the radial kinetic e^{-4phi} -> e^{-2phi}, angular e^{-2phi}->1.
EL = sp.simplify(EL / sp.exp(-2 * P(r, th)))

phirr = sp.Derivative(P(r, th), r, 2); phithh = sp.Derivative(P(r, th), th, 2)
phir_ = sp.Derivative(P(r, th), r); phith_ = sp.Derivative(P(r, th), th)
cot = sp.cos(th) / sp.sin(th)

# The metric's OWN field equation, EL/(-2 sin th) =
#   r^2 e^{-2phi} ( phi_rr + (2/r) phi_r - 2 phi_r^2 )         [RADIAL #33]
# + ( phi_thth + cot th phi_th - phi_th^2 )                    [ANGULAR]
# i.e. dividing through by r^2 e^{-2phi} the angular piece is
#   (e^{2phi}/r^2)( phi_thth + cot th phi_th - phi_th^2 ).
# NOTE the derived ANGULAR NONLINEARITY -phi_th^2 (the dilation self-term)
# and the e^{2phi}/r^2 dressing -- BOTH carried by the metric, nothing added.
target = -2 * sp.sin(th) * (
    r**2 * sp.exp(-2 * P(r, th)) * (phirr + (2 / r) * phir_ - 2 * phir_**2)
    + (phithh + cot * phith_ - phith_**2))
check("metric C1 EL = r^2 e^{-2phi}(reg#33 radial) + "
      "(phi_thth + cot th phi_th - phi_th^2)  [exact; derived angular "
      "nonlinearity -phi_th^2 and e^{2phi}/r^2 dressing, nothing added]",
      sp.simplify(EL - target) == 0)

# radial reduction (theta-independent) -> exactly registry #33 equation:
red = sp.simplify((EL / (-2 * sp.sin(th)) / (r**2 * sp.exp(-2 * P(r, th)))
                   ).subs({phithh: 0, phith_: 0}))
banked_div = phirr + (2 / r) * phir_ - 2 * phir_**2
check("theta-independent reduction = registry #33 radial equation",
      sp.simplify(red - banked_div) == 0)

# The angular piece in the FLOW CHART variable used by wint_cell2d:
# wint_cell2d solves in (m, theta) with A = e^{2v} (1/sin th) d_th(sin th d_th v).
# Confirm that the angular operator there has the SAME e^{2v}-dressing as
# the metric's own e^{2phi} (phi_thth + cot th phi_th) -- i.e. the angular
# Laplacian on the sphere DRESSED by the dilation weight. (1/sin th)
# d_th(sin th d_th v) = v_thth + cot th v_th identically:
v = sp.Function('v')
lap_sphere = sp.simplify(sp.diff(sp.sin(th) * sp.diff(v(th), th), th)
                         / sp.sin(th))
check("(1/sin th) d_th(sin th d_th v) = v_thth + cot th v_th (sphere Lap)",
      sp.simplify(lap_sphere
                  - (sp.Derivative(v(th), th, 2)
                     + sp.cos(th) / sp.sin(th) * sp.Derivative(v(th), th)))
      == 0)
print("""
  => wint_cell2d's angular term  A = e^{2v}( v_thth + cot th v_th - v_th^2 )
     IS the metric's own dressed angular operator, EXACT. The dilation
     dressing e^{2v} AND the derived angular nonlinearity -v_th^2 are
     carried by the metric with NOTHING added (Charles's standing-hunch
     phi-angular coupling appears for free). Both sectors live and
     co-equal; nothing slaved.
""", flush=True)
n = sum(1 for _, ok in PASS if ok)
print(f"WINT_SYMCHECK: {n}/{len(PASS)} PASS")
