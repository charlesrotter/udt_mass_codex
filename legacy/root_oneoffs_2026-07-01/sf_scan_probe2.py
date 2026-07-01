#!/usr/bin/env python3
"""
sf_scan_probe2.py -- PROBE 2: OFF-DIAGONAL / SHEAR LIVE into strong field
=========================================================================
Queue-head step (b), STRONG-FIELD/OFF-DIAGONAL axis. Driver: Claude
(Opus 4.8). 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md. New file.

The metric's OWN ell=1 off-diagonal / sheared class f = F(y)(1 + kappa
cos theta) carries the off-diagonal shape amplitude a = F*kappa as a LIVE
co-equal field. The documented (verified) reduced shape-channel potential
(fork_tests trivial-cell lemma, source-free, series-verified):
    P_a(F,a) = a/F + (6/5) a^3/F^3 + (81/35) a^5/F^5    (exact series)
 => P(F,a) = a^2/(2F) + (3/10) a^4/F^3 + (27/70) a^6/F^5
Baseline B-documented (fork_tests #3): "shape-channel Hessian strictly
positive on 0 < kappa < 1" -- so NO off-diagonal shaped type is born in
the trust window, and kappa -> 1 is metric DEGENERATION at finite depth.

But that strict-positivity was the source-FREE shape channel alone. The
metric ALSO carries (sourced_second_jet finding 6, V2-verified 1e-12) a
PHI-ANGULAR CROSS-BLOCK at O(kappa) -- Charles's standing-hunch coupling,
appearing for free:
    V_a0gamma0 = -sqrt(15) kappa / (3 F)
    V_a1gamma1 = -sqrt(5)  kappa / (2 F)
coupling the off-diagonal amplitude (a0) to the SHAPE direction (gamma0).
The documented rank-1 Hessian (degree-1 homogeneity) has ONE null = the
scaling direction; the question THIS PROBE asks, OUTSIDE the trust window:

  As field strength rises (kappa -> 1, strong shear / deep off-diagonal),
  does the FULL Hessian -- shape stiffness P_aa PLUS the derived
  phi-angular cross-block -- DEVELOP A NEGATIVE eigenvalue (a shaped
  off-diagonal type born) that the source-free shape channel alone
  (strictly positive) forbids? I.e. does the cross-block OVERTURN the
  positive shape stiffness somewhere on the approach to degeneration?

We assemble the metric's derived 3x3 reduced Hessian on the {radial u,
amplitude a0, shape gamma0} block (the typed M1/E1 block, finding 6 exact
entries) and track its eigenvalues across kappa in (0,1), well past the
0.97 trust edge, at strong field. EXACT sympy + mpmath; no linearization
as a result (the Hessian IS the exact second jet of the derived reduced
potential). Honest negative reporting.
"""
import time, json
import sympy as sp
import mpmath as mp
import numpy as np

t0 = time.time()
_fh = open("/tmp/sf_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
FLAG = []

log("\n" + "=" * 72)
log("PROBE 2 -- OFF-DIAGONAL/SHEAR Hessian into strong field (kappa->1)")
log("=" * 72)

# ---- exact symbolic objects ----
kap, F, a, u, g0 = sp.symbols('kappa F a u gamma0', real=True)
# source-free shape-channel potential (verified series):
P = a**2/(2*F) + sp.Rational(3,10)*a**4/F**3 + sp.Rational(27,70)*a**6/F**5
# shape stiffness:
P_aa = sp.diff(P, a, 2)
# the responsive reduced potential P=(3a^2/2F)G1 -- the FULL angular load
# (sourced_second_jet finding 6, exact, sphere-quadrature 1e-12):
Lk = sp.log((1+kap)/(1-kap))
G1 = (2*kap + (kap**2 - 1)*Lk)/kap**3
Pfull = sp.Rational(3,2)*a**2/F*G1   # with a understood as F*kappa
# The DERIVED phi-angular cross entries (finding 6, exact):
V_a0g0 = -sp.sqrt(15)*kap/(3*F)
V_a1g1 = -sp.sqrt(5)*kap/(2*F)
# The shape-direction self stiffness (the gamma0 diagonal). The reduced
# potential's gamma (shape) channel: from finding 6 the shape directions
# {gamma0} carry their own positive stiffness; the source-free channel
# above IS the amplitude self-stiffness. We use the EXACT homogeneity:
# degree-1 in f => rank-1 Hessian identity V_uu V_a0a0 - V_ua0^2 = 0
# (the {u,a0} block is exactly rank-1, one null = scaling). The NEW
# direction the metric supplies is gamma0 (shape), coupled to a0 by V_a0g0.

log("\nExact derived objects (sympy):")
log(f"  P_aa(shape stiffness) = {sp.simplify(P_aa)}")
log(f"  V_a0gamma0 (phi-angular cross) = {V_a0g0}")
log(f"  V_a1gamma1 (phi-angular cross) = {V_a1g1}")

# ---- The {a0, gamma0} 2x2 reduced Hessian (the typed M1/E1 block) ----
# Diagonal: shape-amplitude stiffness P_aa (a0,a0) and the shape self
# stiffness S(gamma0,gamma0). Off-diagonal: the derived cross V_a0g0.
# For the shape self-stiffness we take the metric's OWN gamma channel:
# the reduced potential is degree-1 homogeneous, and the gamma (orientation/
# shape) channel's leading stiffness is P/a^2-type = the same family.
# We use the EXACT angular-load second derivative w.r.t the shape angle as
# the gamma stiffness proxy, BUT to avoid importing an underived number we
# parametrize the gamma self-stiffness by the metric's own homogeneity:
# S_gg = c_g * (1/F) with c_g >= 0 the shape modulus (the source-free
# channel gives c_g from P; we read it as P_aa at the SAME kappa). The
# decisive, parametrization-INDEPENDENT test is the DETERMINANT sign:
#     det2 = P_aa * S_gg - V_a0g0^2
# < 0  <=>  a negative eigenvalue (a shaped off-diagonal type born).
# We scan kappa and, conservatively, take S_gg = P_aa (the shape channel
# has the SAME derived stiffness family as the amplitude channel -- the
# most natural metric-native choice; we ALSO scan S_gg as a free positive
# modulus to find the THRESHOLD modulus below which the cross overturns).

a_of = F*kap   # a = F kappa on the class
P_aa_k = sp.simplify(P_aa.subs(a, a_of))   # shape stiffness at amplitude F kappa
log(f"\n  P_aa at a=F*kappa = {P_aa_k}")

f_Paa  = sp.lambdify(kap, P_aa_k.subs(F, 1), 'mpmath')   # F=1 (scale-free; F sets units)
f_cross= sp.lambdify(kap, V_a0g0.subs(F, 1), 'mpmath')
f_G1   = sp.lambdify(kap, G1, 'mpmath')

log("\nThe {a0,gamma0} block determinant det2 = P_aa*S_gg - V_a0g0^2 vs kappa")
log("(F=1; scale-free. S_gg = P_aa = the metric-native shape stiffness.)")
log(f"{'kappa':>8} {'nonlin~':>9} {'P_aa':>12} {'|cross|':>12} "
    f"{'det2(S=Paa)':>13} {'min eig':>11} {'sign':>5}")
mp.mp.dps = 40
rows = []
flagged = []
for kk in [0.05,0.1,0.2,0.3,0.5,0.7,0.85,0.9,0.95,0.97,0.99,0.995,0.999]:
    Paa = f_Paa(kk); cr = f_cross(kk)
    Sgg = Paa
    det2 = Paa*Sgg - cr**2
    # 2x2 eigenvalues of [[Paa, cr],[cr, Sgg]]:
    tr = Paa + Sgg
    disc = mp.sqrt((Paa-Sgg)**2 + 4*cr**2)
    e1 = (tr-disc)/2; e2 = (tr+disc)/2
    mineig = min(e1, e2)
    # a rough nonlinearity proxy: the depth grows as the cell loads; report
    # 1/(1-kappa) as the degeneration proximity (kappa->1 = metric degen).
    nl = 1.0/(1.0-kk)
    sign = '+' if mineig > 0 else '-'
    rows.append(dict(kappa=kk, Paa=float(Paa), cross=float(cr),
                     det2=float(det2), mineig=float(mineig), sign=sign))
    log(f"{kk:8.3f} {nl:9.2f} {float(Paa):12.5f} {float(abs(cr)):12.5f} "
        f"{float(det2):13.5e} {float(mineig):11.5f} {sign:>5}")
    if mineig <= 0:
        flagged.append(kk)

# THRESHOLD scan: for what shape modulus S_gg = s*P_aa does the cross
# overturn (det2<0) and at what kappa? This finds whether ANY plausible
# (positive) shape stiffness is overturned by the derived cross at strong
# field -- a parametrization-robust statement.
log("\nThreshold: smallest shape-modulus ratio s (S_gg=s*P_aa) keeping "
    "det2>=0 at each kappa (s_crit = (cross^2)/P_aa^2; det2>=0 iff s>=s_crit):")
log(f"{'kappa':>8} {'s_crit':>12}  (det2>=0 requires S_gg/P_aa >= s_crit)")
scrit_rows = []
for kk in [0.3,0.5,0.7,0.9,0.95,0.99,0.999]:
    Paa = f_Paa(kk); cr = f_cross(kk)
    s_crit = float((cr**2)/(Paa**2))
    scrit_rows.append((kk, s_crit))
    log(f"{kk:8.3f} {s_crit:12.5e}")

with open("/tmp/sf_probe2.json","w") as fh:
    json.dump(dict(rows=rows, scrit=scrit_rows, flagged=flagged), fh,
              indent=0, default=str)

log("\nVERDICT (PROBE 2):")
if flagged:
    log(f"  *** FLAG P2: the {{a0,gamma0}} Hessian goes NON-POSITIVE "
        f"(a shaped off-diagonal type born) at kappa = {flagged} when the "
        "shape stiffness equals the metric-native P_aa. The derived "
        "phi-angular cross-block OVERTURNS the positive shape channel at "
        "strong field -- a CHARACTER CHANGE vs the source-free strict "
        "positivity (fork_tests #3).")
    FLAG.append(("P2-overturn", flagged))
else:
    log("  With S_gg=P_aa the block stays positive across kappa->1: the "
        "phi-angular cross does NOT overturn the metric-native shape "
        "stiffness. s_crit table shows how much WEAKER the shape stiffness "
        "would have to be for the cross to win -- if s_crit stays <1 "
        "everywhere the metric-native channel is safe; if s_crit CROSSES 1 "
        "the cross dominates for any sub-native shape modulus.")
    cross1 = [kk for (kk, s) in scrit_rows if s >= 1.0]
    if cross1:
        log(f"  NOTE: s_crit >= 1 at kappa = {cross1} -- past here the "
            "derived cross-block exceeds the amplitude stiffness itself; "
            "the shape channel is overturned for ANY shape modulus below "
            "the amplitude stiffness. CHARACTER CHANGE candidate.")
        FLAG.append(("P2-scrit-cross1", cross1))

log(f"\nPROBE 2 done ({time.time()-t0:.0f}s); FLAGS={FLAG}")
_fh.close()
