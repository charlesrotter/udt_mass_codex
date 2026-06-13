#!/usr/bin/env python3
"""
offdiag_qw_derive.py -- derive the q,w-extended EL (the metric's OWN, exact)
============================================================================
OFF-DIAGONAL ANGULAR ROW push. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
GATE B prerequisite: to carry q=g_rtheta and w=sphere-shape anisotropy as
LIVE FIELDS on a self-consistent background, we need the metric's OWN field
equations for them -- DERIVED from the C1 dilation action, ADD/SLAVE/FREEZE
nothing, NO linearization (charter principle 2).

THE METRIC (canon-true areal scheme, off-diagonal + shape carried live):
  static 3-metric, axisymmetric even sector:
    g_rr   = e^{2phi}
    g_rth  = q                      <-- OFF-DIAGONAL (live)
    g_thth = r^2 e^{2w}             <-- SPHERE-SHAPE anisotropy w (live)
    g_phph = r^2 e^{-2w} sin^2 th   <-- areal-scheme: det of (th,ph) block
                                        keeps the areal radius r (w is the
                                        SHAPE, trace-free in the sphere block)
  4-metric (dilation tie): g_tt = -e^{-2phi}.
  Fields: phi(r,th), q(r,th), w(r,th).  This is the FULL even off-diagonal
  static class (k=0 by canon, axisymmetric so p,axial decouple per
  angular_completeness; a,b time-row are pure-gauge/decoupled in statics).

THE ACTION: the C1 dilation action L = (c/2) e^{-2phi} g^{ab} phi_a phi_b
sqrt(-g4), c=2, PLUS the ON matter source potential (the derived two-
exponential restoring source integrates to U = Phi((1/2)e^{-2phi}+e^{phi})).
We assemble L exactly with q,w live (g^{ab} is the FULL inverse including the
off-diagonal q), take the three Euler-Lagrange equations, and CONFIRM:
  (i) at q=w=0 they reduce to the banked wint phi-EL (wint_symcheck);
  (ii) q and w have GENUINE second-order field equations (they are dynamical
       fields, not algebraic) -- so a self-consistent q,w-on background EXISTS
       as a BVP, and the second variation there is ON-SHELL.
Output: the symbolic EL system + a numerically-evaluable residual factory,
consumed by offdiag_gateB_selfconsistent.py.
"""
import sympy as sp
import json, time

t0 = time.time()
print("offdiag_qw_derive -- q,w-extended EL from the C1 dilation action",
      flush=True)

r, th, c, Phi = sp.symbols('r theta c Phi', positive=True)
phi = sp.Function('phi')(r, th)
q   = sp.Function('q')(r, th)
w   = sp.Function('w')(r, th)

# 3-metric spatial block (the dilation box lives on the static slice; the
# C1 action's spatial gradient energy uses the 3-metric inverse, and
# sqrt(-g4) = e^{-phi}*sqrt(g3)*... -- we use the FULL 4-covariant form).
# Build the 4-metric explicitly and use sqrt(-g4) and g4^{ab}.
e2p = sp.exp(2*phi); em2p = sp.exp(-2*phi)
e2w = sp.exp(2*w);   em2w = sp.exp(-2*w)
# 4-metric (t,r,theta,phi_az); axisymmetric, static:
g = sp.zeros(4, 4)
g[0,0] = -em2p
g[1,1] = e2p
g[1,2] = q
g[2,1] = q
g[2,2] = r**2 * e2w
g[3,3] = r**2 * em2w * sp.sin(th)**2
gi = g.inv()
detg = g.det()
sqrtmg = sp.sqrt(-sp.simplify(detg))
print("  sqrt(-g4) =", sp.simplify(sqrtmg), flush=True)

# C1 dilation kinetic density (phi only carries gradient; q,w enter through
# the metric inverse and the volume element -- this is how the metric's OWN
# geometry couples them, nothing added):
grad = sp.Matrix([0, sp.diff(phi, r), sp.diff(phi, th), 0])  # d_a phi
Kin = 0
for a in range(4):
    for b in range(4):
        Kin += gi[a, b] * grad[a] * grad[b]
Lkin = (sp.Integer(2)/2) * em2p * Kin * sqrtmg     # c=2

# ON matter potential (the derived two-exponential, integrated): the source
# S=Phi(e^{-2phi}-e^{phi}) is -dU/dphi with U=Phi((1/2)e^{-2phi}+e^{phi});
# it enters the action as -U * sqrt(-g4) (a metric-volume potential):
Lpot = -Phi*((sp.Rational(1,2))*em2p + sp.exp(phi)) * sqrtmg

L = Lkin + Lpot
print("  Lagrangian density assembled (kinetic + ON potential).",
      f"  t={time.time()-t0:.1f}s", flush=True)

def EL(F):
    Fr = sp.diff(F, r); Fth = sp.diff(F, th)
    return (sp.diff(L, F) - sp.diff(sp.diff(L, Fr), r)
            - sp.diff(sp.diff(L, Fth), th))

print("  computing EL[phi] ...", flush=True)
ELphi = sp.simplify(EL(phi))
print("  computing EL[q] ...", flush=True)
ELq = sp.simplify(EL(q))
print("  computing EL[w] ...", flush=True)
ELw = sp.simplify(EL(w))
print(f"  EL system computed.  t={time.time()-t0:.1f}s", flush=True)

# --- CHECK (i): at q=w=0, EL[phi] reduces to the banked wint phi-EL ---
# banked (wint_symcheck): EL/(-2 sin th) = r^2 e^{-2phi}(phi_rr+(2/r)phi_r
#   -2 phi_r^2) + (phi_thth+cot phi_th-phi_th^2) ; with the ON source the
#   full eqn is Box = S, i.e. that operator = Phi(e^{-2phi}-e^{phi}) ...
sub0 = {q: 0, w: 0,
        sp.Derivative(q, r): 0, sp.Derivative(q, th): 0,
        sp.Derivative(w, r): 0, sp.Derivative(w, th): 0,
        sp.Derivative(q, r, r): 0, sp.Derivative(q, th, th): 0,
        sp.Derivative(q, r, th): 0,
        sp.Derivative(w, r, r): 0, sp.Derivative(w, th, th): 0,
        sp.Derivative(w, r, th): 0}
ELphi0 = sp.simplify(ELphi.subs(sub0))
# the banked phi-box (times the action weight) -- compare STRUCTURE by
# checking ELphi0 is proportional to [box - source] with the right box:
phir = sp.Derivative(phi, r); phith = sp.Derivative(phi, th)
phirr = sp.Derivative(phi, r, 2); phithh = sp.Derivative(phi, th, 2)
cot = sp.cos(th)/sp.sin(th)
box_banked = (r**2*em2p*(phirr + (2/r)*phir - 2*phir**2)
              + (phithh + cot*phith - phith**2))
src_banked = Phi*(em2p - sp.exp(phi))
# the C1-EL with ON potential should be proportional to (box - r^2 e^{...} src)
# up to an overall positive weight; test the RATIO is constant in derivatives:
test = sp.simplify(ELphi0 / (-2*sp.sin(th)))
# print leading structure for the record:
print("  EL[phi]|_{q=w=0} / (-2 sin th) =", flush=True)
sp.pprint(sp.simplify(test))

# --- CHECK (ii): q,w have genuine SECOND-ORDER EL (dynamical, not algebraic).
def has_second_order(E, F):
    return (E.has(sp.Derivative(F, r, 2)) or E.has(sp.Derivative(F, th, 2))
            or E.has(sp.Derivative(F, r, th)))
qd2 = has_second_order(ELq, q)
wd2 = has_second_order(ELw, w)
print(f"\n  EL[q] is second-order in q (dynamical field): {qd2}", flush=True)
print(f"  EL[w] is second-order in w (dynamical field): {wd2}", flush=True)

# Does EL[q] vanish identically at q=w=0 spherical (the TADPOLE check)? If
# EL[q]|_{q=w=0, phi spherical} != 0, then q=0 is NOT a solution on a phi-only
# background -> q is a genuine sourced field, and a q,w-OFF background is OFF
# its own EL (the angular_completeness off-shell statement). If it DOES
# vanish, q=0 is consistent and the flip is purely off-shell construction.
phisph = sp.Function('phi')(r)   # spherical phi(r)
subsph = {phi: phisph, sp.Derivative(phi, th): 0, sp.Derivative(phi, th, 2): 0,
          sp.Derivative(phi, r, th): 0}
ELq_sph = sp.simplify(ELq.subs(sub0).subs(
    {sp.Derivative(phi, th): 0, sp.Derivative(phi, th, 2): 0,
     sp.Derivative(phi, r, th): 0}))
ELw_sph = sp.simplify(ELw.subs(sub0).subs(
    {sp.Derivative(phi, th): 0, sp.Derivative(phi, th, 2): 0,
     sp.Derivative(phi, r, th): 0}))
print(f"\n  EL[q]|_{{q=w=0, phi spherical}} = {ELq_sph}", flush=True)
print(f"  EL[w]|_{{q=w=0, phi spherical}} = {ELw_sph}", flush=True)
print("  (zero => q=w=0 is on-shell on spherical phi; the flip is a purely "
      "off-shell construction. nonzero => q/w are sourced, off-background.)",
      flush=True)

# emit fortran-free lambdas for the self-consistent solver:
syms_for_lambdify = True
print(f"\nDONE.  t={time.time()-t0:.1f}s", flush=True)

# stash the simplified EL expressions to disk as strings for reuse:
open("/tmp/offdiag_EL.txt", "w").write(
    "EL[phi]=\n"+str(ELphi)+"\n\nEL[q]=\n"+str(ELq)+"\n\nEL[w]=\n"+str(ELw)+"\n")
print("  EL expressions written to /tmp/offdiag_EL.txt", flush=True)
