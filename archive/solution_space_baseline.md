# Solution-Space Baseline — the documented "expected"

Created 2026-06-13 (queue-head step (a), HANDOFF item 1). Append-only.

PURPOSE. The queue head (HANDOFF item 1) is an open-ended scan of the
whole-metric solution space to FIND UNEXPECTED REGIONS — places where the
metric does something NOT already documented. "Unexpected" is only
meaningful against a stated yardstick. This file is that yardstick: it
states plainly, with exact pointers, what the solution space is ALREADY
DOCUMENTED to do, and — equally important — the PREMISE SET under which
each fact was established, so the scanners can tell where the baseline
genuinely does NOT yet constrain anything. A departure counts only if it
LEAVES the premise set under which the baseline fact was proven; inside
that premise set the registry already settled the behavior.

This file invents no physics, makes no new claims, and is not a result.
It is a synthesis of banked registry entries (NEGATIVES_REGISTRY.md) and
their results docs. Every line carries its source.

Governing frame: CRITICAL_UNIVERSE_FRAME.md (the metric is primary and
generates the dilation field; the universe is the metric curving a finite
mass-energy; particles exist at one critical amount; SOLVE THE WHOLE
METRIC, both sectors co-equal, add nothing, slave nothing). The GOAL
(HANDOFF top): formation / topology / properties of PARTICLES (= closed
cells), NOT cavity interiors.

---

## The baseline facts (each with source + premise set)

### B1. The trivial round bulk interior — exactly ONE round type; the bulk angular operator is pure damping (no bulk angular source)

WHAT: With both sectors live and coupled two-way (radial-phi = registry
#33; angular = the metric's own e^{2phi}/r^2-dressed operator
phi_thth + cot th phi_th - phi_th^2, the derived phi-angular coupling,
NOTHING added) iterated to mutual self-consistency, the bulk interior
settles to a ROUND cell from EVERY angular seed (Legendre l=1..4, amp up
to 1.0 -> theta-variance ~1e-13..1e-16). The round-cell Jacobian is
NON-SINGULAR across the whole E-family (min|eig| 0.015 -> 0.145, monotone,
never 0): NO bifurcation, so NO shaped bulk type can be born. The one type
is a smooth continuum in the partition energy E. The angular nonlinearity
-v_theta^2 linearizes to EXACTLY ZERO about the round background =>
sign-definite PURE DAMPING; there is no bulk angular source.

SOURCE: registry #34 (wint_results.md; scripts wint_symcheck.py 3/3,
wint_cell2d.py 6/6; blind verifier ab889812658d33162). Reinforced for the
CLOSED cell by registry #36 (wcc_results.md; see B3): the angular
bifurcation gap is positive and bounded away from zero (min ~0.65 over the
E-family) under every seal closure.

PREMISE SET (where this binds): ON two-exponential source S =
Phi(e^{-2v} - e^{v}) (w_alg PART E); flow-chart Neumann-Neumann closure;
INTERIOR / trust-window scope (NOT closed to the seal f->0 in #34);
BULK dynamical angular sector; static / self-consistent settle; single
cell; axisymmetric even sector; q=1/3, N=3 held; rho = r.

WHERE IT DOES NOT CONSTRAIN: the BOUNDARY / topological angular sector at
the seal (a different sector — that is the H1 area form, see B4); any
multiplicity of types from boundary/topology or whole-universe tiling;
anything outside the static self-consistent bulk (nonstationary, shear,
off-diagonal). #34 explicitly names the seal/boundary closure as the
genuine open edge; #36 closed the DYNAMICAL part of that edge but not the
cohomological part.

### B2. The single-cell compactness CONTINUUM — no discrete pinning; absolute size scale-free

WHAT (two distinct facts):

(B2a) ABSOLUTE SIZE IS SCALE-FREE (theorem). Under r->lr, M->lM, t->lt
(c, G fixed) every closure / regularity condition (center, MS/dilation
tie, mirror-fold seal, Dirichlet+Neumann boundary, finite action, scalar
EOM) is rescale-invariant; absolute size is a provably FREE one-parameter
family; absolute scale = one observational input; the horizon
c^2 = 2GM/r* relates M and r* and fixes neither. Charles's literal "one
absolute mass" is NOT delivered by (c,G) closure.

(B2b) DIMENSIONLESS COMPACTNESS IS A CONTINUUM, NOT DISCRETE (first-class
NEGATIVE). The whole-profile ODE is the metric's own static scalar
equation Box phi = (1/r^2) d/dr(r^2 e^{-2phi} phi') = 0; the full derived
closure is center regularity + outer Dirichlet + outer Neumann
(over-determination +1). BUT +1 over a system with a conserved first
integral yields a 1-PARAMETER CURVE, not a discrete set. On the ON
two-exponential whole-profile equation v_mm = Phi(e^{-2v} - e^{v}) the
first integral (1/2)v_m^2 + (Phi/2)e^{-2v} + Phi e^{v} = E is a restoring
well (U_min = 3Phi/2 at v=0); every bounded orbit has TWO turning points
AUTOMATICALLY, so inner-regularity and outer-Neumann nodes impose nothing;
the only non-automatic condition is the Dirichlet depth, a CONTINUOUS
BIJECTION depth<->E. A continuum of compactness X (one per E) closes; X is
NOT pinned. The #32 flat-member single Gelfand-Bratu root (s tanh s = 1)
was a FROZEN-LENGTH artifact (Dirichlet-Dirichlet at externally-frozen M);
freeing M turns the isolated fold into a continuous (M,s) curve.

SOURCE: registry #32 (B2a, theorem-grade, agent a5a4c7c001ca41275) and
registry #33 (B2b, NEGATIVE, blind verifier ab72b577c0c705d75); both in
w_whole_results.md. Scripts w_whole_gm_derive.py 2/2, w_whole_gm_scan.py
6/6, w_whole_gm_hostile.py 8/8.

PREMISE SET: (c,G) classical closure; SINGLE closed cell; both sectors at
the derived ON two-exponential whole-profile equation; angular numbers
q=1/3, N=3 held; mirror-fold parity center; CR-87 Dirichlet+Neumann pair;
static.

WHERE IT DOES NOT CONSTRAIN (explicitly stated in #33): does NOT block
discreteness from (i) an INTEGER CELL-TILING condition (N cells of width L
tiling a closed universe of fixed tau-extent T -> L = T/N discrete; needs
T fixed by an un-derived closure) or (ii) hbar entering the partition.
CONDITIONS-CHANGED trigger: a closure that fixes total universe extent T,
or hbar entering. So the MULTI-CELL / ensemble axis and any quantum input
are outside this baseline.

### B3. The singular SEAL / same-minus mirror fold — D=0 crease, sigma:(a,b)->(-a,-b), parity dichotomy

WHAT: The seal is the locus D=0 (D = r^2 W - f q^2, the static-slice
reading; with the time row on, D = the determinant factor f D(1+a^2) +
(b - f q a)^2). It is a MIRROR FOLD, not a curvature-singularity edge.
Decisive exact identity (class-general): det g4 = -(r sin)^2 /
[f(1+w)^2] [ f D (1+a^2) + (b - f q a)^2 ], so on D=0,
det g4 = -(r sin)^2 (b - f q a)^2 / [f(1+w)^2] != 0 — the static
(a=b=0) degeneracy LIFTS for any (a,b) with b != f q a. D=0 is exactly
the fixed-point set of the same-minus involution sigma: (a,b)->(-a,-b)
(Charles's "frame-symmetric, no observer" crease). Geodesics cross D=0
smoothly with the time row on (signature preserved, Christoffels finite)
= a FOLD; the static slice's Gamma ~ 1/D edge is the measure-zero crease.
The genuine fold BC is a PARITY DICHOTOMY at the D=0 crease (normal
rho = b - f q a): sigma-EVEN -> Neumann; sigma-ODD -> Dirichlet. The
crease BC ALONE does NOT quantize (W7 B-4); the OUTER finite-cell wall
does (= registry #1 box-control). The Neumann fold reproduces the
"narrowing"; the Dirichlet tower is the equally-legitimate wide band.

SOURCE: registry #30-as-re-amended by W6 (w6_results.md, independent
verifier a091cecbdfdb2c1ef; scripts w6_flux_*.py and verifier engine);
registry #31/W8 (w8_results.md) for the parity-dichotomy / non-quantizing
verdict; w7_a_mirror_bc.py (7/7) for the fold BC; registry #1
(open_domain_discreteness_results.md, W7 re-confirmation w7_results.md)
for "the outer wall quantizes, the crease labels parity."

PREMISE SET: verdict class-general via the exact determinant identity;
exact finite-K VALUES member-numerical (C=0 ell=2 family, q* + generic q,
constant and same-minus-stationary time rows); time-dependent physics
HYPOTHESIS-GRADE; static diagonal+w class for the BC reading.

WHERE IT DOES NOT CONSTRAIN: the FULL nonstationary structure of the fold
quotient (the crease character is established with the time row on, but
the time-dependent dynamics ON the fold is hypothesis-grade and is exactly
where #36/W6 point the discreteness reopening — "cell-count discreteness
REOPENS in the quotient/mirror structure of the fold, driven by f_T, on
the NONSTATIONARY phi-angular sector"). So the nonstationary fold sector
is an open frontier, not baseline-settled.

### B4. The COHOMOLOGICAL area form / EXACT boundary transgression — where q=1/3, N=3, eta=1/18 live (topological, NOT dynamical)

WHAT: The closed cell's STRUCTURE is TOPOLOGICAL (cohomological), not
dynamical. Solved as one BVP (interior + seal mirror-fold closure, both
sectors live, two-way), it supports NO dynamical angular structure — ONE
ROUND body even closed (the angular bifurcation gap is positive and
bounded away from zero under every seal closure; min ~0.65; no lobed seed
persists). The H1 area form omega_H1 is a COHOMOLOGICAL datum:
integral(omega_H1) = 4 pi (topological invariant); and
d ln f ^ omega_H1 = d[(ln f) omega_H1] is an EXACT BOUNDARY TRANSGRESSION,
invisible to the bulk EL, delivered AT THE CLOSURE. THIS IS WHY q=1/3,
N=3 (the area-form discreteness) are REAL yet never appear in any
dynamical spectrum — cohomology vs eigenvalues, different objects. The
geometry splits into a trivial round dynamical body + a non-trivial
TOPOLOGICAL 2-form at the seal; ALL real structure (the discreteness, the
numbers that worked: q=1/3, N=3, eta=1/18) is in the topological part.
This is the only NATIVE discreteness the program has ever produced.

SOURCE: registry #36 (wcc_results.md; exact sympy 6/6; blind verifier
a035deeb280d8bbf9; scripts wcc_closed_cell.py, wcc_seal_spectrum.py,
wcc_topology_at_crease.py). The q=1/3, eta=1/18, N=3 derivations are
banked geometric results (HANDOFF must-not-lose; particles_types_results.md
#35 confirms the solid re-derivations stand: N=3, q=1/3, eta=1/18,
W(P)=Tr(P)/12, p_F=gamma/2).

PREMISE SET: ON two-exponential source (w_alg PART E, load-bearing); the
spectral (dynamical) test is LINEAR (finite-amplitude folds not excluded
by theorem, none found by continuation); D3 orientation reading. NOTE the
#37 CORRECTION: the transgression is sigma-EVEN and glues SYMMETRICALLY
(sigma = time-reversal touches only the time row; r, theta, phi, f,
omega_H1 all sigma-invariant) — NOT the sigma-odd/Dirichlet reading #36
first used; topology is dynamics-invisible because the transgression is
EXACT, not by parity.

WHERE IT DOES NOT CONSTRAIN: the area form fixes the intrinsic chi=2/4pi
class (N=3, q=1/3) but does NOT by itself fix the particle-TYPE COUNT
(that needs the matter-cell core closure — see B5, PARKED). It is a
SINGLE-cell, static, closed-interior datum; ensembles, nonstationary
delivery, and exterior/medium coupling of the area form are untested.

### B5. Topology — genus rigid g=0; winding/Chern family fork-dependent on the matter-cell core closure (PARKED — note, do not pursue)

WHAT: GENUS is rigid g=0 (sphere): axis regularity => two index-+1 poles
=> chi=2 => g=0 uniquely; NO genus family. A WINDING/CHERN family is
genuinely POSSIBLE and is FORK-DEPENDENT on the matter-cell CORE closure
(finite action does NOT cut winding; chi=0 for all closed orientable
3-manifolds cannot decide): core caps r->0 => S^3 (H^2=0) => ONE rigid
class; finite second seal => S^2xS^1 (H^2=Z) => integer (Chern) family;
p-fold twist => L(p,q) (H^2=Z/p) => finite p-family. The intrinsic
chi=2/4pi class (where N=3, q=1/3 live) survives every branch.

SOURCE: registry #37 (topo_results.md; blind verifier ab449c89, 2nd
verifier pending on the doubling fork; scripts topo_classes_zoo.py,
topo_d3_junction.py, topo_doubling_fork.py).

PREMISE SET: HYPOTHESIS-GRADE — the matter-cell core closure (areal r at
phi->-inf) is UNDERIVED; the winding family is a possibility tree hinging
on that one open fact, not a delivered count.

PARKED (Charles, 2026-06-13): #37 STANDS as a banked result, but PURSUING
the core-closure derivation is judged a likely-wrong rabbit hole. Do NOT
pursue it (nor the #37 2nd-verifier) without Charles's explicit go. It is
recorded here for completeness of the baseline ONLY; it is not a scan
target.

### B6. Absolute scale-freedom — only c and G are scale-free; tested quantities are dimensionless RATIOS

WHAT: With only c and G, the solved PIECES are scale-free: rescale mass +
length + time together (c, G unchanged) and you get a family. The
quantities we test against data are dimensionless RATIOS (= the wall
numbers); absolute scale is normally set by ONE observation. The horizon
condition c^2 = 2GM/r* relates M and r* and fixes neither. 7.004
(dilation depth at the CMB boundary) = ln(1+z_CMB) via 1+z = e^phi is an
OBSERVATIONAL anchor at the size level (X free) unless some closure forces
the compactness. (This is B2a re-stated at the level of the whole program:
it is WHY the data-blind test is on ratios, not absolute masses.)

SOURCE: registry #32 (w_whole_results.md, theorem-grade); HANDOFF
must-not-lose (the data-blind test is the six lepton wall RATIOS, contract
26fc757); CRITICAL_UNIVERSE_FRAME.md "the one open, checkable thread."

PREMISE SET: only c and G in the closure (no hbar); single-cell pieces;
classical.

WHERE IT DOES NOT CONSTRAIN: whether the WHOLE closed metric (as opposed
to the solved pieces) carries a ruler the pieces do not show — Charles's
bet (a) — remains open; closures that introduce T (tiling) or hbar are
outside scope (#33). Multi-cell / whole-universe closure is the named
place a non-scale-free ruler could appear.

---

## What is, and is NOT, settled — at a glance

SETTLED (do not re-document; departures inside these premise sets are not
"unexpected"):
- The static, single-cell, two-way BULK interior is exactly one round
  type, a smooth E-continuum; bulk angular operator is pure damping (B1,
  #34/#36).
- The single-cell whole-profile closure does NOT pin absolute size (B2a/
  B6, #32 theorem) and does NOT pin dimensionless compactness — a
  continuum in E (B2b, #33 negative).
- The seal is a same-minus mirror FOLD (not an edge); its crease BC is a
  parity dichotomy (Neumann/even, Dirichlet/odd) and does NOT by itself
  quantize; the outer box does (B3, #30/W6, #31/W8, #1/W7).
- The real structure (q=1/3, N=3, eta=1/18) is COHOMOLOGICAL — the H1
  area form (integral 4pi) and an EXACT closure transgression — and is
  invisible to every dynamical spectrum (B4, #36). This is the ONLY
  native discreteness in the program.
- Genus is rigid g=0 (B5, #37). [Winding family open but PARKED.]

NOT YET CONSTRAINED BY THE BASELINE (the scan frontier — see table):
nonstationary / time-dependent dynamics; multi-cell / ensemble closure;
the exterior / medium side; strong-field / off-diagonal (shear, q-on)
regimes. Each baseline fact above was proven under STATIC, SINGLE-CELL,
(mostly) DIAGONAL, INTERIOR/trust-window or closed-but-static premises.
The scan deliberately steps OUTSIDE those premises.

---

## Axis table — what baseline already covers vs. the open scan frontier

| Scan axis | What the baseline ALREADY covers (and from where) | Where the baseline does NOT yet constrain (the open frontier) |
|---|---|---|
| NONSTATIONARY / time-dependent | Crease character WITH the time row on is established: D=0 is a fold, det g4 != 0, geodesics cross smoothly, degeneracy lifts off the static slice via (b - f q a)^2 ∝ f_T (B3, #30/W6). Static shaped matter under any time dependence (C1 alone) eliminated by theorem (registry #22). | The actual TIME-DEPENDENT DYNAMICS on/near the fold quotient is HYPOTHESIS-GRADE only (#30/W6 premises). #36/W6 explicitly point cell-count discreteness reopening to "the NONSTATIONARY phi-angular sector, driven by f_T" — the orchestra frame. No baseline behavior is documented for genuine f_T-driven evolution; registry #22's single reopening route is the native w-stiffness sector. This is Charles's prime discreteness suspect (phi-angular). PRIME open axis. |
| MULTI-CELL / ensemble | Single-cell closure exhausted: scale-free size (B2a/#32) and compactness continuum (B2b/#33). #33 NAMES the open door: integer cell-tiling (N cells of width L = T/N) could re-discretize X IF a closure fixes total universe extent T. Registry #1/W7 box-control re-confirmed on a finite-mirrored-cell ENSEMBLE (the outer wall quantizes; no native absolute scale). | Whether closing the WHOLE (multi-cell / universe) metric introduces a ruler the single-cell pieces lack (Charles's bet (a), B6) is OPEN. The tiling closure (does the closed universe force an integer count of critical cells?) is UN-DERIVED. Ensemble interactions beyond box-separation, and whether T is fixed by closure, are unconstrained. |
| EXTERIOR / medium | The mirrored finite-cell canon (no spatial infinity; universe and matter cells are finite mirrored domains) frames the exterior as a mirror, not vacuum (CANON; memory charles-exterior-field-picture). Several legacy exterior negatives (#3/#5 weld modes) were re-graded under the mirror exterior (E0 > 0 global). | The medium-forms-cells / recycling-loop / two-threshold stable-vs-transient picture (memory) is NOT translated into a solved whole-metric exterior coupling. How the exterior/medium SETS the critical amount, delivers the area-form transgression, or couples cells is undocumented at the whole-metric level. Open. |
| STRONG-FIELD / off-diagonal (shear, q-on) | The q* branch and Delta_w surface are four-way characterized (W3/W4/W5/W-ALG, #30): exact-solvable per-ray structures (Liouville/Tzitzeica/Poschl-Teller), the 1.90-class ratio = 2pi^2/(3G*) exactly, wall count = deg(Delta_w in u^2) rising with ell. With the time row on, D=0 is a fold (B3). Static off-diagonal shaped cells eliminated by theorem in the constrained class (#21). The insulating-WALL discreteness reading at D=0 is REFUTED (#30: g^{thth}=1/D blows up, Neumann turning not a wall). | These characterizations are FROZEN-f / off-shell-background / static-class or member-numerical (#30 premises). The fully two-way, unfrozen, strong-field off-diagonal (large shear, q-on, deep core toward phi->-inf) solution is not mapped; whether documented invariants (finite K, the 1.90 ratio, the exact-solvable species) persist there is open. The deep core (r > a^3 W/a_u^2 band where u* is real is the OUTER band only; u* absent in the deep core) is a named gap. |

---

## How to use this file (for the scanners, step (b)/(c))

1. A flagged region is a candidate ONLY if it LEAVES the premise set of the
   baseline fact it appears to contradict. Re-read the premise set before
   calling anything "unexpected."
2. The four axes above are ordered by how little the baseline constrains
   them. The static single-cell interior is NOT a scan target (known
   trivial, B1). Charles's standing hunch and the #36/W6 reopening both
   point hardest at the NONSTATIONARY phi-angular sector.
3. Every flagged anomaly gets a blind pass (real vs numerical artifact vs
   already-documented-here) before banking (step (c)). "Already documented
   here" = it falls inside a baseline premise set above.
4. Discipline (binding): do NOT retreat to the easy interior, do NOT match
   mass numbers, do NOT invent mechanisms. B5 (topology core closure) is
   PARKED — note it, do not pursue without Charles.
