# BLIND VERIFIER — Energy Distribution Across the Three N=3 Directions

Verifier: Claude (Opus 4.8, 1M context), BLIND ADVERSARIAL pass.
Date: 2026-06-14. Target doc: `n3_direction_distribution_results.md`.
**DATA-BLIND**: no lepton/hadron masses, no Koide, no sqrt(2), no 45-deg
condition loaded, computed, or compared. NO spinor/Dirac/hbar/photon.
Discipline: INDEPENDENT machinery — I did NOT run any `n3_*.py` script; I wrote
my own sympy + V100-float64 GPU codes from scratch and re-derived everything.
Mandate: try hardest to RESCUE a cyclic-Z3 / native-sqrt(m) structure.

Independent scripts (this verifier, commit-grade):
- `verif_n3_angular_sympy.py` — closed-form L2 iso-generator angular tensor.
- `verif_n3_alt_operationalizations.py` — RESCUE attempt: 4 native readings of
  "the 3 directions" (iso-gens / orbital l=1 m-states / energy-density l=1
  decomposition / component overlap tensor), hunting for cyclic Z3.
- `verif_n3_L4_sympy.py` + `verif_n3_L4_recheck.py` — closed-form L4 cross-tensor.
- `verif_n3_gpu_3d.py` — independent 3D GPU inertia tensor + my own BVP profile
  solver; self-audit isotropy + axial-pattern + background scan.
- `verif_n3_L2L4_split.py` — L2-vs-L4 decomposition + profile-tail inspection.
- `verif_n3_tail_mechanism.py` — controlled-width profile: L_perp cell-divergence.
- `verif_n3_sqrt_rescue.py` — active hunt for a native sqrt(m) amplitude.

---

## DECISIVE VERDICTS (the two the mandate asks for)

**VERDICT 1 — does ANY native operationalization give cyclic Z3? NO.**
I independently computed FOUR distinct native readings of "the 3 N=3 directions":
(A) the 3 SO(3) iso-rotation generators (doc's choice); (B) the 3 orbital l=1
m-states (m=-1,0,+1) — *the legacy Koide operationalization* of
udt_canonical_geometry S13.11, explicitly different from the doc; (C) the l=1
spherical-harmonic decomposition of the soliton energy density; (D) the
target-component overlap tensor <n_a n_b>. EVERY ONE is a DIAGONAL tensor of the
form (X, X, Y) — two equal weights + one special on target-axis 3 — i.e. AXIAL
2+1. NONE is cyclic/Z3 (three equal weights related by 120deg with no special
axis). The reason is structural and unavoidable: the easy-axis hedgehog
n3=cosTheta(r) leaves an exact continuous SO(2) symmetry about target-axis 3, and
an axisymmetric field can only produce a 2+1 (axial) split, never a discrete
3-fold one. The cyclic-Z3 rescue FAILS under every native choice.
=> **AXIAL 2+1 IS ROBUST; cyclic-Z3 is NOT reachable in the bare winding sector.**

**VERDICT 2 — is sqrt(m) ever native to the winding sector? NO.**
Active rescue enumerated every native primitive: the unit vector n
(dimensionless), the winding number B (an integer COUNT), the iso-velocity omega
(1/time), the inertia Lambda (energy/omega^2), the topological/L4 current density
(an areal density whose square is an energy density), fluctuation amplitudes
(free without an hbar/zero-point input). The decisive structural fact: the L2+L4
action is built ENTIRELY from the dimensionless n and its derivatives — every
term is quadratic or quartic in d n — so it contains NO term linear in a
sqrt-of-density field carrying a mass coefficient. That linear-in-sqrt-density
mass term is exactly what a Dirac mass `m psi-bar psi` supplies (psi ~
sqrt-density). The bare winding sector hands back ENERGIES/INERTIAS, never a
primitive whose SQUARE is the mass. Writing omega = sqrt(E/Lambda) is a tautology
of any kinetic term, not a native sqrt(mass) STRUCTURE.
=> **sqrt(m) is NOT native to the bare winding sector; it is the spinor input the
computation deliberately omitted. CONFIRMED.**

**OVERALL: the result STANDS.** A cyclic three-fold (Koide-type) splitting and a
native sqrt(m) amplitude do NOT emerge from the single-cell L2+L4 hedgehog. Both
require an external ingredient (a spinor's sqrt-amplitude + spin multiplicity, or
an inter-cell/ensemble coupling treating the three on equal footing). I found one
nuance that makes the doc's specific *ratio narrative* less robust (below), but it
does not touch either decisive verdict — if anything it strengthens the
non-universality claim.

---

## CLAIM-BY-CLAIM

### CLAIM 1 (operationalization / cyclic-Z3): **CONFIRMED (axial robust)**
Independent sympy (`verif_n3_angular_sympy.py`) reproduces the L2 iso-generator
angular tensor EXACTLY and diagonal:
    INT|v_3|^2 dOmega = (8pi/3) sin^2 Theta              [matches doc, residual 0]
    INT|v_1|^2 = INT|v_2|^2 = (4pi/3)(cos 2Theta + 2)    [matches doc, residual 0]
    all off-diagonals identically 0.
RESCUE across alternative native operationalizations (`verif_n3_alt_*.py`):
- (B) orbital l=1 m-states (legacy Koide reading): Wx=Wy=(8pi/5)sin^2Theta,
  Wz=(32pi/15)sin^2Theta -> still 2+1 (z special). NOT cyclic.
- (C) energy-density l=1 dipole moments d_x=d_y=d_z=0 -> the anisotropy lives in
  l=0+l=2 (quadrupolar/axial), there is NO l=1 dipole that would pick three
  directions cyclically.
- (D) <n_a n_b> overlap = diag((4pi/3)sin^2Theta, (4pi/3)sin^2Theta, 4pi cos^2Theta)
  -> 2+1 again.
Every native choice is axial 2+1; full degeneracy (three equal) occurs only at
isolated radii (sin^2Theta=3/4). No native choice yields cyclic Z3.

### CLAIM 2 (no native sqrt(m)): **CONFIRMED** (see Verdict 2). No rescue found.

### CLAIM 3 (axial split + background-dependence): **CONFIRMED, with a nuance**
- Lambda_perp != Lambda_3 with perp-axes EXACTLY degenerate: my independent 3D
  GPU tensor gives |L11-L22|/L11 = 0 (machine zero) and off-diag ~1e-8
  (r-derivative noise) at every cell size and phi-depth tested.
- Easy-axis mechanism CONFIRMED in closed form (n3=cosTheta singles out axis 3).
- L4 cross-tensor also strictly diagonal axial 2+1 (`verif_n3_L4_recheck.py`:
  diag(4.73,4.73,2.24) at a test point, off-diag exactly 0 after proper angular
  integration; the apparent nonzero off-diag in my first L4 pass was an
  un-simplified-expression artifact, NOT real).
- Background-dependence CONFIRMED and is STRONGER than the doc states: with a
  controlled localized profile (`verif_n3_tail_mechanism.py`), L_3 saturates
  (cell-independent) while L_perp grows ~r_int^3 (1070 -> 2.09e6 as cell 8->100)
  via the cos^2Theta global-monopole tail -> ratio DIVERGES with cell size. At
  width~1, cell~8 the L2 ratio is ~429, consistent with the doc's order ~415.
- NUANCE (mild correction, not a refutation): the doc says the ratio
  monotonically "shrinks toward ~7" with phi-depth. In my full BVP the
  perp/along-3 ratio is NON-MONOTONIC and actually INVERTS (drops below 1 near
  p~0.75-1.5, then rises again: full ratio 1.63 ->1.04 ->0.75 ->0.52 ->2.63
  ->125 as p=0 ->0.5 ->1 ->1.5 ->2 ->3). So the SIGN (which is cheaper to spin)
  is itself background-dependent. This makes the doc's "Lambda_3 << Lambda_perp,
  easy-axis cheaper to spin" only a FLAT/shallow-cell statement, not a universal
  sign. It does NOT touch the verdicts: the ROBUST invariant is the axial 2+1
  PATTERN (perp exactly degenerate at all p), and the doc's headline conclusion
  (ratio is background-dependent, NOT a universal constant like sqrt2) is
  reinforced — the ratio is even less universal than the doc claimed.
- (Profile note: my full-BVP minimizer produced a WIDER profile than the doc's,
  so my flat-12L *full* ratio is ~1.6 not ~253. This is a profile-width
  difference, exactly the doc's own point that the ratio is profile/cell
  dependent; my analytic radial integral matches my GPU L2 to 4 digits, so the
  machinery is internally consistent.)

### CLAIM 4 (self-audit, isotropic reads isotropic): **CONFIRMED**
My independent integrator at the exact analytic isotropy point (sin^2Theta=3/4,
where the closed forms force M11=M33) returns an isotropic tensor to grid
precision: diag spread (max-min)/mean = 1.18e-4 -> 2.90e-5 -> 7.20e-6 as
nth=60 ->120 ->240 (converges ~1/n^2), off-diagonals at machine zero (~1e-16). An
isotropic case reads isotropic; the split in the profile run is physics, not an
integrator artifact.

### CLAIM 5 (L2 vs L4, deep-phi): **CONFIRMED with the same inversion nuance**
L2 carries the long-range (cell-divergent) split; L4 is soliton-localized in both
channels. Perp-axes stay exactly degenerate at every depth (no
re-3-splitting/cyclic). The ratio does NOT collapse monotonically to ~7 — it
inverts and recovers (above). float64 held cleanly through p=3.

---

## WHAT I TRIED TO BREAK AND COULD NOT
- Cyclic Z3 via 4 different native operationalizations (incl. the legacy Koide
  l=1 m-state reading) — all axial 2+1.
- A native sqrt(m): every primitive is dimensionless/count/velocity/energy; the
  action has no linear-in-sqrt-density mass term. Spinor-only.
- An off-diagonal / non-axial L4 contribution — vanishes exactly on integration.
- Isotropy-restoring artifact — integrator passes the covariant self-audit.

## WHAT I DID FIND (honest, minor)
- The doc's monotone "ratio shrinks toward ~7 with phi-depth" is wrong in detail:
  the ratio is non-monotonic and inverts. This WEAKENS the doc's specific
  "easy-axis always cheaper to spin" sign claim but STRENGTHENS its central
  "not a universal constant" claim. Recorded as a CONFIRMED-with-correction.

## DATA-BLIND CONFIRMATION
No lepton/hadron wall numbers, no Koide ratio, no sqrt(2), no 45-deg condition,
no spinor/Dirac/hbar/photon entered any verifier script or this document. The
pass was metric-led (independently re-derive the settled winding sector's
internal-direction structure) and adversarial (actively hunting cyclic-Z3 and
native-sqrt rescues), not target-led.
