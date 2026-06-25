# Delta_p_F — BLIND ADVERSARIAL VERIFIER VERDICT: PARTIALLY DERIVED / ASSEMBLED

Verifier: independent main-loop blind adversarial pass.
Agent id: dpf-blind-verifier (own sympy machinery; own seal/jet/charge
re-derivation; did NOT re-run the challenger's dpf_derive.py / dpf_adversary.py
as evidence — reproduced each load-bearing step independently).
Date: 2026-06-14. Script: `dpf_verify_indep.py` (14/14 PASS).
Log: `/tmp/dpf_verify.log`. New file (append-never-edit).

DATA-BLIND HELD: no lepton wall numbers loaded; contract 26fc757 NOT opened
(verified by grep of all three dpf scripts — only the dpf_verify_indep.py
docstring NAMES the contract, to assert it was not opened; no wall numbers
105.658 / 0.51099 / 1776.86 / 0.97767 / 1.93121 anywhere).

Prosecution stance: this is a PRIOR-CONFIRMING positive (a clean forced
ratio from the cohomological sector). Per the charter's hypothesis
discipline the verifier aimed its HARDEST attack here, default skeptical,
hunting for the {3,5,7} failure mode (banked-real pieces SPLICED to land on
a clean number). It found that mode, in part.

---

## OVERALL VERDICT: PARTIALLY DERIVED — the inter-sector ratio (5/3)e^{-1/18}
## is NOT a forced derivation. It is an ASSEMBLED product of pieces drawn
## from THREE separate, never-jointly-derived objects, gated on a
## reading-grade depth count. Several FACTORS are solidly banked; the
## PRODUCT and the depth d=2L are reading-grade. This is the SAME class of
## construction as the rejected {3,5,7}, softened by being honestly flagged.

The challenger's own document concedes the two crux points (dpf_results.md
lines 168-182, 220-226): d=2L is "HYPOTHESIS-GRADE", the multiplicative
assembly is "a composition, not a single closed junction solve." The
headline ("DERIVED", "fully forced", "a pure number, no free datum") is
nonetheless stronger than those concessions support. This verdict resolves
the gap on the side of the concessions.

---

## THE DECISIVE FINDING (kill-shot A, the crux)

**There is NO banked closed functional for the angular charge correction
P_F / Delta_p_F.** Grep of every banked source confirms the ONLY substantive
Delta_p_F datum anywhere is the single SCALAR in mass_audit item 3:
"Delta_p_F ~ -2.5% of p_F at gamma=1; 100% phi-angular-sourced; c=0 gives
Delta_p_F = 0 EXACTLY (P_F vanishes on spherical flows)." That is one number
and a vanishing condition — NOT a functional of (sector, c, gamma).

The genuine charge functional that DOES exist is the exterior_cavity object
`H(kappa) := -2 P_F = L/(2kappa) - 1`, with the degree-1 homogeneity
("screening") identity `P_FF - P_Fa^2/P_aa = 0`, in the (F, a) gauge. **That
functional carries NO SO(3) sector structure at all** — no A3, no S5, no
W(P). Conversely the W(P)=Tr(P)/12 weight lives ONLY in the spectrum doc's
operator-image readout (sec 17, itself a "candidate rule"), which NEVER
touches p_F, P_F, or the Misner-Sharp charge.

Verified by grep: in mass_audit, exterior_cavity, and ensembles (the charge
functional's homes) the strings W(P)/W(A3)/W(S5)/Tr(P)/alphabet occur **zero
times**; in the spectrum doc, p_F/Misner-Sharp occurs zero times in the
W(P) context. **The assembled product
`Delta_p_F = -p_F · W(P) · (c^2/gamma^2) · exp(-eta/2 · d)`
is the FIRST place these two independent machineries are multiplied
together, and that multiplication is ASSERTED, not produced by any
functional.** A genuine O(c^2) perturbation of the real P_F functional
`H(kappa)` was never carried out (the dpf push did not perturb it; it
multiplied banked scalars). The factorization is therefore UNVERIFIED at the
level it claims — it is a *splice of three objects*, not a *forced product*.

KILL-SHOT A test (dpf_verify_indep.py A2): alternative, equally-"natural"
multiplicative placements that obey ALL banked anchors (c=0 vanish, O(c^2),
negative sign) give DIFFERENT ratios — e.g. attenuating the WEIGHT instead of
the whole product gives S5/A3 = (5/3)e^{-7/18} = 1.130, not 1.577. The
banked anchors do NOT pin the product. **A: ASSEMBLED, not derived.**

---

## PER-KILL-SHOT VERDICTS

**A. THE MULTIPLICATIVE ASSEMBLY — REFUTED as a forced product.** No banked
functional yields the product; W(P) and p_F live in disjoint objects that
co-occur nowhere else; the genuine P_F functional (H(kappa)) was never
perturbed in c; alternative placements obeying the same anchors give
different ratios. A product of (individually) forced factors is NOT a forced
product. This is the {3,5,7} splice pattern, honestly flagged but present.

**B. THE d=2L JUNCTION COUNT — READING-GRADE, not forced (REFUTED as
derived).** A real same-minus Z2 mirror fold imposes one parity BC per
independent component; an order-L harmonic has 2L+1 components (m=-L..L), not
2L. "2L = count of (+-m) doublets, |m|=1..L, drop m=0" is ONE reading among
several equally defensible (2L+1, L+1, ...). No junction-condition
computation was done (the doc admits this). This is the SAME class of
unforced count the {3,5,7} verifier rejected as "depth=dim", merely shifted
by one (now depth=dim-1). For the A3->S5 step d=2L and d=dim happen to give
the SAME Delta_d=2 (so e^{-1/18} survives that particular swap), but d=L
gives Delta_d=1 => e^{-1/36}, a different number. d=2L is NOT forced.

**C. FLOOR + WEIGHT — PARTIALLY SOLID.** The c^2/gamma^2 angular floor is
FORCED: |X_t(0)|^2 = gamma^2 + c^2 is banked-exact (mass_audit:48), and
c^2/4 vs gamma^2/4 is reproduced independently. The c^2 scaling and the c->0
vanishing ARE a theorem of the jet norm (solidly banked, reproduced). W(P) as
a readout of the TRACELESS T8 (W_A3=1/4, W_S5=5/12, ratio 5/3) is forced
GIVEN the spectrum doc's candidate readout rule — but that rule is itself
"candidate"-grade upstream, and W(trace)=1/12 EXTRAPOLATES it to a direction
(the trace) that is NOT in T8. For the S5/A3 ratio the trace weight is
irrelevant, so 5/3 is clean conditional on the candidate readout.

**D. SEAL PLACEMENT — SOLID (but only licenses existence, not the formula).**
rho = b - f q a is sigma-ODD; the c-insertion (b*=-c) is genuinely the odd
part (reproduced independently); the parity dichotomy (odd->Dirichlet) and
Xi=dTheta EXACT (Stokes delivers content at the seal) are banked. So a
boundary charge correction, O(c^2), at the seal, in the odd/Dirichlet sector,
genuinely EXISTS. This does NOT dictate that it EQUALS the assembled product.
Placement solid; formula unproven.

**E. RATIO / DATA-BLIND — DATA-BLIND held; "forced" is CONDITIONAL.** No wall
number entered the construction; the contract was not opened; m and gamma do
cancel GIVEN the assembled form + d=2L, yielding a pure number. BUT
data-blind != forced: (5/3)e^{-1/18} is forced only conditional on (A) the
unforced assembly and (B) the unforced d=2L. Change either and the number
moves (d=L -> (5/3)e^{-1/36}). No leak; conditional forced-ness.

**F. ANTI-NUMEROLOGY VERDICT — SAME CLASS as {3,5,7}, softened by honesty.**
The construction is banked-real pieces combined to yield a clean number. It
is BETTER than {3,5,7} in three concrete ways: (1) no fake dim-7 / no L7 —
the alphabet is genuinely 1+3+5; (2) the c^2 floor + c->0 vanishing are a
real theorem, not invented; (3) the assembly and depth are FLAGGED
hypothesis-grade, not sold as forced (the headline overshoots, the body is
honest). It is the SAME class in one decisive way: the load-bearing
inter-sector number rides on a multiplicative splice of disjoint objects plus
a hand-chosen count, neither derived from a single computation.

---

## WHAT IS SOLIDLY BANKED (survives the attack)

- The c^2/gamma^2 angular floor and the EXACT c->0 vanishing — a theorem of
  the weld-jet norm |X_t(0)|^2 = gamma^2 + c^2 (mass_audit, reproduced).
  Delta_p_F IS 100% phi-angular-sourced and DOES vanish at c=0. (kill-shot A1,
  C, and the banked anchor — all reproduced.)
- The negative/screening sign — sign of the added interface action c^2/4>0
  (mass_audit item 1, reproduced).
- rho = -c - f q gamma is sigma-ODD; the c-channel is the odd/Dirichlet seal
  insertion; Xi=dTheta EXACT delivers angular content at the seal (Stokes).
  A boundary, O(c^2), odd-sector charge correction EXISTS. (kill-shot D.)
- W_S5/W_A3 = 5/3 — forced GIVEN the (candidate) Tr(P)/12 readout.
- The exp(-eta/2 d) attenuation FORM with rate eta/2 = q^2/4 = 1/36 (exact)
  IS the right per-e-fold rate IF the mechanism is per-rung transgression
  accumulation — but the DEPTH d it accumulates over is reading-grade.

## WHAT IS READING-GRADE / ASSEMBLED (does NOT survive as "derived")

- The MULTIPLICATIVE PRODUCT itself: -p_F·W·(c^2/gamma^2)·exp(-eta/2 d) is a
  splice of three disjoint banked objects (charge functional + operator
  readout + cohomology slope) that co-occur in NO single computation. Not a
  forced product. (kill-shot A — the crux.)
- d = 2L = dim-1: a junction COUNT reading, not a junction-condition
  computation; the same class the {3,5,7} verifier rejected. (kill-shot B.)
- Therefore the inter-sector ratio (5/3)e^{-1/18} is NOT a genuine forced
  data-blind PREDICTION; it is a data-blind CONSTRUCTION conditional on two
  reading-grade choices. (kill-shots A, B, E, F.)

## RECOMMENDATION

Do NOT bank (5/3)e^{-1/18} as a forced prediction. Bank ONLY: (i) Delta_p_F
exists, is O(c^2), 100% angular-sourced, vanishes at c=0 (theorem); (ii) it
is an odd/Dirichlet seal boundary charge correction (placement); (iii)
W_S5/W_A3=5/3 conditional on the candidate readout. The PRODUCT FORM and the
RATIO require: (a) an actual O(c^2) perturbation of the real P_F functional
H(kappa) showing the sector weight and the transgression attenuation EMERGE
from one computation (not spliced); and (b) a genuine same-minus
junction-condition count replacing the d=2L reading. Until both are done,
this is PARTIALLY DERIVED / ASSEMBLED — not the forced cohomological ratio
the headline claims.
