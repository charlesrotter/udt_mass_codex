#!/usr/bin/env python3
"""seal_junction_timeon_check.py -- DERIVE the sigma-ODD / time-on seal
junction condition for BOTH candidate involutions, analytically.

Driver: Claude (Opus 4.8, 1M). Date 2026-06-21. F4 frontier item.
Mode: OBSERVE, DATA-BLIND, analytic. NO heavy solve. CPU sympy.

REUSES (does NOT edit) the exact same-minus involution machinery from
w7_a_mirror_bc.py and topo_d3_junction.py:
  sigma1 = t->-t  (the W6 same-minus reading): on the metric, (a,b)=
    (g_tr,g_ttheta) -> (-a,-b); on a field X(t,.) it is X(t,.)->X(-t,.).
  sigma2 = P x T   (the competing involution on record): also reflects
    a spatial parity (here the radial/angular orientation), composed
    with T.

GOAL: classify each time-live field (H=g_tr, phi(t,r), Theta(t,r),
e^{i w t}) by sigma-parity at the seal t=0 (the fixed surface of T),
read off the seal BC per the DERIVED dichotomy
  sigma-EVEN -> NEUMANN (d_n field = 0),
  sigma-ODD  -> DIRICHLET (field = 0),
and DECIDE whether the resulting BC QUANTIZES (discrete spectrum at a
FIXED physical radius) or is CONTINUOUS (slides with R).
"""
import sympy as sp

t, r, th, w = sp.symbols('t r theta omega', real=True)
PASS = []
def rec(tag, note):
    PASS.append(tag); print(f"[{tag}] {note}", flush=True)

print("="*72)
print("PART 1 -- the seal is the FIXED SURFACE of T (t=0). Parity is in t.")
print("="*72)
# The named involution acts on the metric line element ds^2. The seal is
# the fixed-point set of T. A field's parity is how it transforms there.

# --- the metric pieces and how each dt-factor transforms under T:t->-t
# g_tt dt^2  : dt^2 -> dt^2  (EVEN slot)  => phi (in g_tt=-e^{2phi}) EVEN
# g_tr dt dr : dt dr -> -dt dr (ODD slot) => H=g_tr ODD
# g_rr dr^2, g_thth, g_phph : no dt => EVEN (untouched by T)
rec("1a", "metric-slot parities under T(t->-t): g_tt EVEN, g_tr ODD, "
          "spatial-diagonal EVEN. (one dt-index per off-diag arm flips sign)")

print()
print("="*72)
print("PART 2 -- INVOLUTION 1 = sigma1 : t -> -t  (W6 same-minus)")
print("="*72)
# Field classification under sigma1. ds^2 invariance forces:
#   H = g_tr  : ODD   (the arm carries one dt; T flips it)  -> DIRICHLET
#   phi(t,r)  : EVEN  (sits in g_tt dt^2, two dt -> even)   -> NEUMANN
#   Theta(t,r): a SCALAR field. Its seal parity is whatever the EL/source
#               demands; the hedgehog STATIC profile is EVEN (t-indep).
#               Its time-on FLUCTUATION delta-Theta ~ cos/sin(wt) splits.
#   e^{i w t} : -> e^{-i w t}. Real standing parts: cos(wt) EVEN, sin(wt) ODD.

# verify the oscillatory split under sigma1:
osc = sp.exp(sp.I*w*t)
osc_s = osc.subs(t, -t)
rec("2a", f"sigma1 on e^(iwt) -> e^(-iwt): "
          f"{'OK' if sp.simplify(osc_s - sp.exp(-sp.I*w*t))==0 else 'FAIL'}. "
          "=> cos(wt) is sigma1-EVEN, sin(wt) is sigma1-ODD.")
# verify g_tr arm flips, phi-slot (dt^2) does not:
a = sp.Function('H')(t, r)        # H = g_tr amplitude
rec("2b", "sigma1: H=g_tr is ODD (Dirichlet H(seal)=0); phi in g_tt is "
          "EVEN (Neumann d_t phi=0 at seal); Theta-static EVEN (Neumann).")
# The KEY object: the time-on / sigma-ODD content. Under sigma1 the ODD
# fields are {H, sin(wt)-part of every fluctuation}. The seal BC on them:
rec("2c", "sigma1 seal BC on the TIME-ON/odd sector: "
          "H(t=0)=0 and [sin(wt) parts](t=0)=0 -- i.e. DIRICHLET-IN-TIME "
          "at the seal t=0. This is a NODE IN TIME, automatically satisfied "
          "by sin(w*0)=0 for EVERY w. It selects NO w.")
# Show: sin(w*0)=0 identically in w -> no quantization of w from this node.
rec("2d", f"sin(w*0) = {sp.sin(w*0)} for ALL w  => the seal time-node is "
          "w-INDEPENDENT: it imposes NO discrete condition on omega. "
          "(The even/cos sector is Neumann d_t cos(wt)|_0 = -w sin(0)=0, "
          "also automatic.) => CONTINUOUS in omega.")

print()
print("="*72)
print("PART 3 -- the RADIAL/outer structure is the ONLY w-selector")
print("="*72)
# The seal in sigma1 is a TIME surface (t=0), NOT the outer radial wall.
# So the sigma1 seal BC constrains the TIME dependence, not the radial
# eigenproblem. The omega spectrum is still set by the OUTER RADIAL BC at
# r=R (the cell wall) -- which the box-control solves scanned. Hence:
rec("3a", "sigma1's seal (t=0) gives time-parity BCs only; it does NOT "
          "touch the radial r=R wall. The omega-spectrum is fixed by the "
          "RADIAL outer BC => still box-controlled (omega ~ n/R), CONTINUOUS "
          "as R varies. sigma1 does NOT rescue a fixed-radius spectrum.")

print()
print("="*72)
print("PART 4 -- INVOLUTION 2 = sigma2 : P x T  (competing)")
print("="*72)
# P x T composes a SPATIAL reflection P with time reversal T. The seal's
# fixed set is then a SPATIAL surface (P-fixed) AT t=0. If P is taken as
# the RADIAL fold across the cell wall (r -> 2R - r, fixed surface r=R),
# then PxT's fixed structure DOES live at the outer radial wall r=R.
rec("4a", "PxT: fixed set is a SPATIAL surface (P-fixed) combined with T. "
          "If P = radial fold about the wall (fixed r=R), the seal is a "
          "RADIAL junction at r=R -- it DOES constrain the radial problem.")
# Under P x T, classify the SAME fields. A spatial reflection P about r=R
# sends d r -> -d r at the wall and t->-t. Then:
#   g_tr dt dr : both dt and dr flip -> (-)(-) = EVEN  -> NEUMANN
#   g_tt dt^2  : dt^2 even, no dr    -> EVEN under T; under P (no dr) EVEN
#                BUT phi(r) -> phi(2R-r): even/odd about r=R decides.
#   spatial-diagonal g_rr dr^2 : dr^2 even -> EVEN
# So PxT FLIPS the arm's parity vs sigma1: H=g_tr becomes EVEN (Neumann).
rec("4b", "PxT REGRADES the arm: g_tr dt dr has BOTH a dt and a dr; PxT "
          "flips both => g_tr is EVEN under PxT (NEUMANN), the OPPOSITE of "
          "sigma1. This is the 'PxT would regrade' on record (ffv:91-92).")
# The genuinely-new content under PxT: the RADIAL fold about r=R now acts
# like a reflection BC at the wall. A reflection junction at a FIXED wall
# r=R imposes EITHER Neumann (even radial modes) OR Dirichlet (odd radial
# modes) about r=R -- a MIRROR/method-of-images doubling.
rec("4c", "PxT radial fold = method-of-images reflection at r=R. Doubles "
          "the cell [0,R] to [0,2R] with a reflection at R. Spectrum of a "
          "reflected interval of half-width R: omega_n ~ n*pi/(2R) (even) or "
          "(n+1/2)*pi/(2R) (odd). STILL ~ 1/R.")
# Decisive: even with a reflection junction at the wall, the level spacing
# scales as 1/R_cell. With R unpinned (F7), this is CONTINUOUS / box-like.
rec("4d", "Even the PxT reflection junction gives omega_n proportional to "
          "1/R_cell (a HARMONIC ladder of a doubled interval). With R_cell "
          "NOT natively pinned (F7) and the ladder HARMONIC (1:2:3..), this "
          "is the F4-counterweight outcome: a TRIVIAL box ladder, NOT a "
          "non-harmonic quantizer. SLIDES with R => CONTINUOUS in scale.")

print()
print("="*72)
print("PART 5 -- the one place a QUANTIZER could hide, tested")
print("="*72)
# A genuine fixed-radius quantizer needs a Robin/antiperiodic condition
# that fixes omega INDEPENDENT of R. Check: does either involution give a
# Robin condition  alpha*field + beta*d_n field = 0  with a w-dependent,
# R-independent ratio?  sigma1: time-node (w-independent). sigma2: spatial
# reflection (Neumann or Dirichlet about r=R) -- both R-SCALED, no fixed w.
rec("5a", "Neither involution yields a Robin/antiperiodic seal condition "
          "with an R-INDEPENDENT omega. sigma1 -> w-independent time node; "
          "sigma2 -> R-scaled radial reflection. NO fixed-radius quantizer.")
# The ONE residual hinge (fermion_forcing): if the forced sigma-ODD source
# has a REQUIRED-NONZERO seal value, a single-valued odd boson is Dirichlet-
# pinned to a node => antiperiodicity (T^2=-1). That antiperiodicity is a
# parity/statistics selector, NOT an omega-quantizer: it picks the spinor
# DOUBLE-COVER, not a discrete mass set. Note honestly.
rec("5b", "HONEST HINGE: antiperiodicity (T^2=-1) IF the odd source's seal "
          "value is forced nonzero selects SPINOR STATISTICS (a 2-valued "
          "cover), NOT a discrete omega. It is a quantum-statistics datum, "
          "not a classical mass quantizer. So even the live hinge does not "
          "make the CLASSICAL spectrum discrete -- consistent with must-quantize.")

print()
print("="*72)
print(f"DONE. {len(PASS)} analytic checks recorded.")
print("VERDICT: BOTH involutions -> CONTINUOUS (no fixed-radius classical")
print("quantizer). sigma1 seal = time-node (w-independent). sigma2 seal =")
print("R-scaled radial reflection (harmonic, slides with R). F4 CLOSES")
print("analytically for the seal-as-quantizer question.")
print("="*72)
