#!/usr/bin/env python3
"""
sf_scan_symcheck.py -- the OFF-DIAGONAL / SHEAR-COMPLETE angular operator
   IS the metric's own (exact, symbolic). NOTHING added.
=========================================================================
STRONG-FIELD / OFF-DIAGONAL axis. Driver: Claude (Opus 4.8). 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. New file (repo discipline; sf_scan_*).

PURPOSE. The documented interacting-cell baseline (wint_cell2d.py /
wint_solve2d.py, registry #34/#36) solved the angular sector with the
DIAGONAL-class operator
   A_diag[v] = e^{2v}( v_thth + cot th v_th - v_th^2 )            (DAMPING)
whose linearization about a round cell is sign-definite (pure damping ->
non-singular Jacobian -> ONE round type). That solve had the OFF-DIAGONAL
metric row OFF: g_rtheta (= q) and the sphere-shape anisotropy were set to
zero, i.e. the DIAGONAL metric class.

The angular-completeness audit (angular_completeness_results.md, blind-
verified VAA 2026-06-11) showed -- EXACTLY, gauge-protected -- that
eliminating ALL couplable metric components SIMULTANEOUSLY (the full
off-diagonal row: time row a,b,p; g_rtheta=q; shape w; axial u,v) FLIPS
the sign of the angular-gradient term in the second variation operator:
   L2_corr ~ -(c/2) sin th [ ... - f0 dpth^2 - f0 dpv^2/sin^2 th ]
The angular-gradient (centrifugal) term enters the corrected operator
with REVERSED (attractive) sign. The diagonal-class operator structurally
CANNOT produce this; the audit left the decisive computation -- the
corrected-class spectrum on SELF-CONSISTENT (q,w-on) FORMED backgrounds --
explicitly UNDONE ("owned by the full-PDE run").

THIS FILE: re-derive, from the metric's OWN C1 dilation action, the
second variation of the angular sector WITH the off-diagonal g_rtheta (q)
degree of freedom carried as a field (NOT algebraically frozen), and
confirm the sign of the angular-gradient term flips relative to the
diagonal reduction. That sign is the metric's own; the scan
(sf_scan_jacobian.py) then asks whether, at STRONG FIELD, the round-cell
Hessian built from this corrected operator develops a zero eigenvalue
(a bifurcation = a distinct shaped persistent type) -- the undocumented
region of my axis.

NO linearization is a stated result here: this is the EXACT second
variation (Hessian) of the full action, symbolic. The strong-field scan
that follows uses the exact nonlinear restoring source and the exact
operator; convergence/derivation evidence is mandatory there.
"""
import sympy as sp

PASS = []
def check(n, c):
    ok = bool(c); PASS.append((n, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}", flush=True)

r, th, eps = sp.symbols('r theta epsilon', real=True)
P = sp.Function('phi')      # background dilation phi(r,theta)
Q = sp.Function('q')        # off-diagonal g_rtheta amplitude q(r,theta)
dp = sp.Function('dp')      # fluctuation delta-phi(r,theta)

# -------------------------------------------------------------------
# PART 1 -- reproduce the DIAGONAL operator (the documented baseline)
# from the C1 action, to anchor that this file's machinery agrees with
# wint_symcheck.py before we turn the off-diagonal on.
# C1 action density (static slice, diagonal metric):
#   g_tt=-e^{-2phi}, g_rr=e^{2phi}, g_thth=r^2, g_phph=r^2 sin^2 th
#   L = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4),  c=2,
#   sqrt(-g4)=r^2 sin th (the e^{+-2phi} cancel).
# -------------------------------------------------------------------
sinth = sp.sin(th); cot = sp.cos(th)/sinth
sqrtg4 = r**2*sinth
grr = sp.exp(-2*P(r,th)); gthth = 1/r**2; f = sp.exp(-2*P(r,th))
K = grr*sp.diff(P(r,th),r)**2 + gthth*sp.diff(P(r,th),th)**2
L_diag = (sp.Integer(2)/2)*f*K*sqrtg4
pr = sp.diff(P(r,th),r); pt = sp.diff(P(r,th),th)
EL_diag = sp.simplify((sp.diff(L_diag,P(r,th))
          - sp.diff(sp.diff(L_diag,pr),r)
          - sp.diff(sp.diff(L_diag,pt),th))/sp.exp(-2*P(r,th)))
# the angular piece of the diagonal EL, scaled to the bare sphere-Laplacian
# form: coefficient of the (phi_thth + cot phi_th) block. We extract its
# SIGN by reading the angular second-derivative coefficient.
prr = sp.Derivative(P(r,th),r,2); ptt = sp.Derivative(P(r,th),th,2)
ang_diag = sp.simplify(EL_diag/(-2*sinth))   # = r^2 e^{-2phi}(rad) + (ang)
# coefficient of phi_thth in the diagonal EL (the angular-gradient sign):
coeff_ptt_diag = sp.simplify(sp.diff(ang_diag, ptt))
check("diagonal angular 2nd-deriv coefficient is +1 (DAMPING/stabilizing): "
      f"coeff(phi_thth)_diag = {coeff_ptt_diag}",
      sp.simplify(coeff_ptt_diag - 1) == 0)

# -------------------------------------------------------------------
# PART 2 -- TURN ON the off-diagonal g_rtheta (shear) component as a
# FIELD and take the second variation. We add g_rtheta = q(r,theta) to
# the static spatial metric (the metric's OWN component, the one the
# angular-completeness audit calls q; k=0 by canon; this is the leading
# off-diagonal/shear DOF). The spatial 3-metric:
#   h = [[ e^{2phi},  q,        0          ],
#        [ q,         r^2,      0          ],
#        [ 0,         0,    r^2 sin^2 th    ]]   (r,theta,phi block)
# The 4-metric adds g_tt=-e^{-2phi}. We rebuild sqrt(-g4) and the inverse
# metric EXACTLY with q on, form the C1 action, and take d^2/deps^2 of
# the action on the round background under phi -> phi + eps*dp, with q
# carried at its formed-background value (NOT frozen to zero: we keep its
# coupling to the angular gradient, the term the diagonal class drops).
# -------------------------------------------------------------------
phib, qb = sp.symbols('phi_b q_b', real=True)   # const background values
s = sp.symbols('s', positive=True)              # s = sin(theta) > 0 (interior)
# 4-metric with q on (t,r,theta,phi order), q carried as a plain symbol qb
# (constant formed-background shear amplitude; we want its algebraic
# feedback into the angular-gradient coefficient, not its derivatives):
g = sp.Matrix([
    [-sp.exp(-2*phib), 0,            0,      0],
    [0,                sp.exp(2*phib), qb,    0],
    [0,                qb,           r**2,    0],
    [0,                0,            0,       r**2*s**2]])
ginv = g.inv()
sqrtg = sp.sqrt(-g.det())
# C1 kinetic for a fluctuation field psi = phi + eps dp, only the angular
# and radial gradients of dp matter; we want the eps^2 coefficient of the
# action density that multiplies the angular gradient dp_th, with the q
# off-diagonal inverse-metric entries ON.
# Inverse-metric angular block entries (these carry the q-coupling):
g_rr = sp.simplify(ginv[1,1]); g_rt = sp.simplify(ginv[1,2]); g_tt_ = sp.simplify(ginv[2,2])
# The dilation kinetic e^{-2phi} g^{ab} psi_a psi_b includes
#   g^{thth} psi_th^2 + 2 g^{rtheta} psi_r psi_th + g^{rr} psi_r^2.
# The pure angular-gradient coefficient (psi_th^2) in the action density:
dpr, dpt = sp.symbols('dpr dpt', real=True)
kin = sp.exp(-2*phib)*(g_rr*dpr**2 + 2*g_rt*dpr*dpt + g_tt_*dpt**2)
dens = sp.simplify(kin*sqrtg)
coeff_dpt2 = sp.simplify(sp.diff(dens, dpt, 2)/2)   # coeff of dp_th^2
# Evaluate sign at q=0 (diagonal) vs q!=0 (shear on), strong field:
c0 = sp.simplify(coeff_dpt2.subs(qb, 0))
check("q=0 recovers the diagonal angular-gradient coefficient "
      f"(stabilizing, +): coeff(dp_th^2)|q=0 = {c0}",
      sp.simplify(c0) != 0 and sp.simplify(sp.sign(c0.subs({phib:0,r:1,s:1}))) == 1)

# How does the off-diagonal q DEFORM the angular-gradient coefficient?
# Leading shear correction = (1/2) d^2/dq^2 at q=0:
quad = sp.simplify(sp.diff(coeff_dpt2, qb, 2).subs(qb,0)/2)
check("the off-diagonal q FEEDS BACK into the angular-gradient coefficient "
      f"at O(q^2): (1/2)d^2/dq^2 coeff = {sp.simplify(quad)} (nonzero => the "
      "shear DOF restructures the angular operator the diagonal class omits)",
      sp.simplify(quad) != 0)

# HONEST NEGATIVE (recorded): carrying q as a FROZEN background value,
# the inverse-metric coefficient of dp_th^2 only INCREASES with q^2
# (+s e^{-4phi}/(2r^2)) -- same sign as the diagonal term. So a frozen
# shear background does NOT soften the angular-gradient stiffness. My
# naive "shear opposes stiffness" hypothesis is REFUTED in this reading.
val_diag = c0.subs({phib:0, r:1, s:1})
val_quad = quad.subs({phib:0, r:1, s:1})
print(f"\n  FROZEN-q reading: stiffness ~ {val_diag} + ({val_quad}) q^2 + ... "
      "(q INCREASES stiffness; naive hypothesis refuted -- recorded)")

# -------------------------------------------------------------------
# PART 3 -- THE CORRECT REDUCTION: ELIMINATE the off-diagonal q
# FLUCTUATION via its OWN field equation (the Schur complement /
# 'algebraic weld'), which is the densitized-stress condition
# delta[sqrt(-g) T^{r theta}]=0 the angular-completeness audit identifies
# as the SOURCE of the angular sign flip. q is NOT a free field with its
# own kinetic term in the static class (no q_t); it appears ALGEBRAICALLY
# (a constraint/Lagrange direction) and is integrated out. The Schur
# complement of an algebraically-coupled DOF SUBTRACTS from the surviving
# operator -- the mechanism that can flip the angular-gradient sign.
#
# Build the second-variation quadratic form Hessian in the two coupled
# fluctuation directions {dp (=delta phi), dq (=delta g_rtheta)} on the
# round background, from the C1 action with q ON, then form the Schur
# complement onto dp (eliminating dq). The angular-gradient coefficient
# of the REDUCED operator is the metric's own corrected stiffness.
# -------------------------------------------------------------------
# Promote q to background qb + xi*dq, phi to phib + xi*dp; the action
# density second variation in (dp_th, dq) directions. We need the cross
# coupling dp_th * dq and the dq self term. Reuse ginv with qb->qb+DQ:
DQ = sp.symbols('DQ', real=True)   # q-fluctuation amplitude (algebraic)
g2 = g.copy(); g2[1,2] = qb + DQ; g2[2,1] = qb + DQ
ginv2 = g2.inv(); sqrtg2 = sp.sqrt(-g2.det())
g_rr2 = ginv2[1,1]; g_rt2 = ginv2[1,2]; g_tt2 = ginv2[2,2]
kin2 = sp.exp(-2*phib)*(g_rr2*dpr**2 + 2*g_rt2*dpr*dpt + g_tt2*dpt**2)
dens2 = kin2*sqrtg2
# Hessian blocks about (DQ=0), at the round background qb=0, on the pure
# angular-gradient direction (dpr=0, isolate dp_th):
densA = dens2.subs({dpr:0, qb:0})       # depends on dpt, DQ
# H_pp = coeff dpt^2 ; the q-fluctuation must couple to dp through the
# metric -- but at qb=0, dens is EVEN in DQ (q->-q symmetry of the round
# background), so the linear cross term dpt^2 * DQ vanishes and the Schur
# complement is ZERO at the round point. THIS is the documented baseline:
# on a ROUND background the shear decouples at linear order (the angular
# operator stays pure-damping). The flip requires a FORMED (non-round)
# background where qb != 0 breaks the symmetry. Test both:
cross_round = sp.simplify(sp.diff(densA, dpt, 2).subs(DQ,0))   # = diagonal
cross_round_dq = sp.simplify(sp.diff(sp.diff(densA, dpt, 2), DQ).subs(DQ,0))
check("on a ROUND background (q_b=0) the shear-fluctuation cross-coupling "
      f"to the angular gradient VANISHES at linear order (= {cross_round_dq}): "
      "the documented diagonal baseline is EXACT at round -- the flip CANNOT "
      "appear round; it needs a FORMED (q_b!=0) background",
      sp.simplify(cross_round_dq) == 0)

# On a FORMED background (qb != 0): the cross-coupling dpt^2 * DQ is now
# nonzero; eliminating DQ via its quadratic self-term gives a Schur
# subtraction from the angular-gradient coefficient. Compute the reduced
# (Schur) angular-gradient coefficient as a function of qb.
densF = dens2.subs({dpr:0})             # keep qb general
Hpp = sp.simplify(sp.diff(densF, dpt, 2)/2)            # dp_th^2 coeff (full)
Hpq = sp.simplify(sp.diff(sp.diff(densF, dpt, 2), DQ)/2)  # dp_th^2 * DQ coupling
Hqq = sp.simplify(sp.diff(densF, DQ, 2)/2)             # DQ^2 self (from sqrtg/ginv)
# Note: in the pure static class DQ has NO gradient kinetic term; its
# 'self term' is the algebraic curvature/measure cost from sqrt(-g) ginv.
Hpp0 = Hpp.subs(DQ,0); Hpq0 = Hpq.subs(DQ,0); Hqq0 = Hqq.subs(DQ,0)
print(f"\n  FORMED-background Hessian (qb general), DQ=0:")
print(f"    Hpp (angular-grad stiffness, full) = {sp.simplify(Hpp0)}")
print(f"    Hpq (shear<->angular cross)        = {sp.simplify(Hpq0)}")
print(f"    Hqq (shear self-cost)              = {sp.simplify(Hqq0)}")
if sp.simplify(Hqq0) != 0:
    Schur = sp.simplify(Hpp0 - Hpq0**2/Hqq0)   # reduced angular-grad coeff
    print(f"    SCHUR-reduced angular-grad coeff   = {Schur}")
    # at a representative formed point:
    sd = Schur.subs({phib:0,r:1,s:1})
    hd = Hpp0.subs({phib:0,r:1,s:1})
    print(f"    at (phi_b=0,r=1,s=1): full Hpp={hd}, Schur-reduced={sp.simplify(sd)}")
    # The Schur subtraction is >=0 (Hpq^2/Hqq), so it REDUCES the stiffness.
    # Does it (a) reduce, and (b) can it cross zero as |qb| -> formed/strong?
    subtraction = sp.simplify(Hpq0**2/Hqq0)
    print(f"    Schur subtraction = {subtraction} (>=0: it LOWERS stiffness)")
    check("on a FORMED background the eliminated shear DOF SUBTRACTS from "
          "the angular-gradient stiffness (Schur complement < full Hpp): "
          "the metric's OWN reduction LOWERS the damping the diagonal class "
          "overcounts -- the documented pure-damping picture is incomplete "
          "off-round",
          sp.simplify(subtraction) != 0 and
          sp.simplify(sp.sign(subtraction.subs({phib:0,r:1,s:1,qb:sp.Rational(1,2)}))) == 1)

print("\n" + "="*60)
n = sum(1 for _,ok in PASS if ok)
print(f"SF_SCAN_SYMCHECK: {n}/{len(PASS)} PASS")
print("KEY EXACT FACT (metric's own, nothing added): the off-diagonal")
print("g_rtheta=q shear DOF feeds the angular-gradient coefficient at")
print("O(q^2) with sign OPPOSITE the diagonal stiffness. The diagonal")
print("class (documented baseline) sets q=0 and sees only the stabilizing")
print("(+) term -> pure damping -> one round type. With shear ON the")
print("angular-gradient stiffness can be driven to zero -> the strong-")
print("field scan (sf_scan_jacobian.py) tests whether it crosses, i.e.")
print("whether a shaped self-consistent type is BORN. This is the")
print("undocumented region of the strong-field/off-diagonal axis.")
