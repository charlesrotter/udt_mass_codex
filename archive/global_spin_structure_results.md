# Does the GLOBAL Topology of the Doubled Cell FORCE a Fermionic (T^2=-1) Spin Structure? — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (gated,
authorized by Charles). This is the GLOBAL/topological companion to
fermion_forcing_results.md (result #46), which closed the LOCAL seal-value
route AGAINST forcing a spinor (the forced sigma-ODD source vanishes at the
seal, so a single-valued field suffices locally; NEGATIVES_REGISTRY #46).

Frame: w6_results.md / #42 (the seal is the time-reversal involution
sigma: t->-t, ANGULAR sector untouched); #37 (spatial cross-section genus
rigid g=0 = S^2; a winding/Chern family is fork-dependent) AND its
VERIFIER CORRECTION (the area-form transgression is sigma-EVEN, glues
SYMMETRICALLY — sigma touches ONLY the time row; r, theta, phi, f,
omega_H1 are all sigma-invariant); wcc_results.md ~159/168 (orientability
of the fold flagged UNSETTLED — "a geometric reading, not a theorem"). A
spinor is a section of the SPIN bundle; spin structures exist iff w_2 = 0
and form a torsor over H^1(M; Z_2); around a loop a spinor is PERIODIC
(T^2=+1) or ANTIPERIODIC (T^2=-1, the genuine fermion).

**No mass / ratio / data.** All statements are TOPOLOGICAL/analytic facts
about the doubled-cell manifold. No spinor is imported and asserted forced;
we DERIVE which spin structures EXIST / are ADMITTED / are FORCED-or-not.

THE QUESTION: result #46 showed the LOCAL seal-value argument does NOT
force a two-valued (T^2=-1) spinor. Does the GLOBAL topology of the
time-reversal-DOUBLED cell force ANTIPERIODIC (T^2=-1, spinorial) boundary
conditions / a genuine spin structure — a global obstruction the local
argument can't see?

Script (commit-grade, this push):
- `global_spin_structure.py` — sympy orientation-Jacobian check + the
  cohomology/holonomy reasoning, cross-checked on the concrete
  product/double models. (V100/mpmath unneeded; pure topology.)

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | Single cell body = collar I_r x S^2 (radial interval x genus-0 sphere) | DERIVED | #37 SOLID: axis regularity => two index-+1 poles => chi=2 => g=0 unique |
| P2 | sigma = (t -> -t); seal = its FIXED surface; ANGULAR sector untouched | DERIVED | w6/#42; #37 verifier correction (sigma touches ONLY the time row) |
| P3 | Doubling = glue cell to its MIRROR copy across the seal (boundary-double) | DERIVED frame / CHOSE the boundary-double construction | the same-minus mirror IS this gluing; "double across the fixed surface" is the construction the fold names |
| P4 | Spin structure theory: exists iff w_2=0; torsor over H^1(M;Z_2); loop holonomy +/-1 = periodic/antiperiodic | DERIVED (standard) | textbook spin-geometry |
| P5 | TIME direction GLOBAL shape: interval vs circle | **NOT FIXED — the analysis FORKS on it; reported both** | the canon time row is HYPERBOLIC/propagating (C-2026-06-13-1), NOT canonically closed; "time closes into S^1" is an EXTRA, UNDERIVED assumption |
| P6 | q = 1 - 2/N = 1/3 is the SLOPE of the EXACT, sigma-EVEN transgression Theta=(ln f)omega_H1 in the H^2 sector | DERIVED | h1_types_results.md; #37 verifier correction (sigma-EVEN) |
| P7 | Identification "q=1/3 fractional => projective => antiperiodic spin" | **NOT ASSUMED — under test** | tested and reported, not posited |

---

## 1. ORIENTABILITY OF THE TIME-REVERSAL FOLD (settles the wcc/#37 flag)

The pure reflection across the fixed surface, R: (t,r,theta,phi) ->
(-t,r,theta,phi), has coordinate Jacobian determinant **-1** (sympy, exact;
one coordinate, t, flips). So the LOCAL reflection across t=0 is
orientation-reversing IN A SINGLE CHART.

But the DOUBLE is not a single chart: it is the boundary-double
M = X u_{seal} X-bar, gluing the cell X to a MIRROR copy X-bar across the
fixed surface. **Standard fact: the double of an orientable manifold-with-
boundary is ORIENTABLE** (it is a closed manifold that bounds; the mirror
copy carries the reversed orientation and the two orientations match across
the gluing exactly because the gluing is the boundary identity). The fold
being a reflection is precisely what makes the canonical orientation of the
double globally CONSISTENT.

What the wcc/#37 "orientation-reversal reading" actually saw: under t->-t
the timelike frame leg e^0 -> -e^0, so the 4-VOLUME FORM flips sign ON ONE
SHEET. That is a sign on the single-sheet volume form (and on the sigma-ODD
time-row entries g_tr, g_ttheta), NOT a global non-orientability of the
doubled manifold. The metric's sigma-ODD time row is a sign on two metric
COMPONENTS, not a reversal of the coordinate orientation dt^dr^dtheta^dphi.

> **VERDICT 1 [DERIVED]: the time-reversal DOUBLE is ORIENTABLE** (it is the
> boundary-double of an orientable cell). The flagged "orientation-reversal"
> was a single-sheet volume-form sign, consistent with orientability of the
> whole. This RESOLVES the wcc ~159/168 / #37 flag in the orientable
> direction, at the level of the involution's action on coordinates (a full
> same-minus junction-form computation would be the next refinement, but the
> boundary-double construction already settles orientability).

---

## 2. THE MANIFOLD, w_2, AND H^1(M; Z_2) (does a spin structure exist? how many?)

The doubled cell M = (double of I_r x S^2 along the seal), TIMES the time
direction. The discriminating objects are w_2(M) (existence) and
H^1(M;Z_2) (the torsor / count of spin structures). Two GLOBAL shapes,
forking on P5 (does time close?):

- **(a) interval time:** M ~ I_t x I_r x S^2, homotopy type **S^2**.
- **(b) circle time** (would require an EXTRA time-identification, NOT in
  canon): M ~ S^1_t x I_r x S^2, homotopy type **S^1 x S^2**.

**w_2 (existence of ANY spin structure):**
- TS^2: w_2(S^2) = e(TS^2) mod 2 = chi(S^2) mod 2 = 2 mod 2 = **0**.
  (The Euler number 2 is EVEN, so S^2 admits a spin structure.)
- S^1 and I are parallelizable (total SW class 1); by Whitney
  w(M) = w(S^2), so **w_2(M) = 0 in EVERY shape.**

> **A SPIN STRUCTURE EXISTS on the doubled cell, in every candidate global
> shape. [DERIVED]** (Weak claim: EXISTS.)

**H^1(M; Z_2) (count = |H^1|; the periodic-vs-antiperiodic choice):**
- shape (a) ~ S^2: **H^1(S^2; Z_2) = 0** => the spin structure is UNIQUE,
  and it is the PERIODIC (T^2=+1) one. **The antiperiodic / fermionic
  structure does NOT EVEN EXIST** when time is an interval.
- shape (b) ~ S^1 x S^2: **H^1(S^1 x S^2; Z_2) = Z_2** => TWO spin
  structures, PERIODIC (T^2=+1) and ANTIPERIODIC (T^2=-1) around the time
  circle. **The fermionic structure is ADMITTED** when time closes.

> **VERDICT 2 [DERIVED]: whether a fermionic (T^2=-1) spin structure even
> EXISTS is FORK-DEPENDENT on whether the TIME direction CLOSES into a
> circle. Interval time => H^1=0 => only periodic => NO fermion option.
> Circle time => H^1=Z_2 => fermionic structure ADMITTED (not yet forced).**

The canon weighs HERE: C-2026-06-13-1 makes the diagonal sector strictly
HYPERBOLIC in time (a propagating wave equation, finite real wave speeds),
i.e. TIME IS A PROPAGATION DIRECTION, not a canonically compactified one.
The finite-cell mirror (C-2026-06-10-2) is the RADIAL phi -> -phi structure,
NOT a time identification. So under the CURRENT banked structure the
default is shape (a) (interval time), in which the antiperiodic structure is
not even admitted. Closing time into a circle is an EXTRA, UNDERIVED
assumption (P5).

---

## 3. THE HOLONOMY / ANTIPERIODICITY TEST (the load-bearing one)

The candidate fermion-forcing loop is "go through the seal to the mirror
sheet and back," which applies sigma twice (= sigma^2). The decisive
topological fact:

**sigma: t -> -t is a genuine INVOLUTION on the manifold: sigma^2 = id.**
The round trip through the seal is the IDENTITY as a map. For antiperiodicity
to be FORCED, a field would have to be required to pick up a sign (-1) around
some loop — which can ONLY happen on a NON-CONTRACTIBLE loop.

- **shape (a) interval time:** the through-seal-and-back loop is
  CONTRACTIBLE (the seal is the t=0 face; slide the crossing point off the
  face and the loop bounds a disk). A contractible loop has trivial Z_2
  holonomy: **holonomy = +1 is FORCED for every field, spinor or not.**
  Antiperiodicity CANNOT be required. NO fermion forced globally.
- **shape (b) circle time:** the loop that goes ALL THE WAY AROUND the time
  circle (through the seal AND through the far identification) is NON-
  contractible (the generator of pi_1). ITS Z_2 holonomy is EXACTLY the free
  choice labelled by H^1(;Z_2)=Z_2: +1 = periodic, -1 = antiperiodic. The
  topology ADMITS both and FORCES neither.

> **VERDICT 3 [DERIVED]: GLOBAL consistency does NOT force T^2=-1.** The
> mirror fold is a REFLECTION (it creates a fixed SURFACE), not a twist; it
> does not by itself create a non-contractible loop carrying a sign. For
> interval time the round-trip loop is contractible (holonomy +1 forced); for
> circle time the antiperiodic structure is ADMITTED but the periodic-vs-
> antiperiodic choice is a FREE Z_2, unforced by the topology.

This is the precise GLOBAL echo of #46's LOCAL result: locally the forced
sigma-ODD source's seal-value is zero (sigma-ODD => vanishes at the fixed
surface); globally the seal round-trip is sigma^2 = id on a contractible
loop. **The FOLD ITSELF — local or global — does not force the fermion's
two-valuedness.** The global view does not rescue the spinor that the local
view lost; it CORROBORATES the negative and pinpoints exactly what WOULD be
needed (a non-contractible time loop AND a physical selector picking -1).

---

## 4. SELECTION ANALYSIS (if it EXISTS, is the fermionic one PICKED OUT?)

Even in shape (b) where the antiperiodic structure is ADMITTED, is it
SELECTED by the banked physics?

- **Seal Dirichlet/odd parity (wcc P6):** the sigma-ODD sector obeys
  DIRICHLET at the seal (field = seal value, odd part = node). This pins a
  single-valued odd field to ZERO at the fixed surface — it does NOT, by
  itself, demand a sign-twisted (antiperiodic) global section. #46 already
  showed this lands on "single-valued odd boson suffices." No selection of
  antiperiodic from the seal parity.
- **Time-reversal Kramers structure:** a genuine Kramers (T^2=-1) condition
  WOULD select the antiperiodic structure — but Kramers T^2=-1 is precisely
  the spinorial assumption UNDER TEST; it cannot be invoked to select itself
  without circularity. The geometry gives sigma^2=+1 (Part 3), the BOSONIC
  Kramers (T^2=+1), not the fermionic one. To get T^2=-1 one must ADD a
  half-integer / projective representation — an IMPORT, not a derivation.
- **q=1/3 projective charge:** treated in Part 5; it does not select.

> **VERDICT 4 [DERIVED]: even where ADMITTED (circle time), the fermionic
> spin structure is NOT SELECTED by any banked physical condition.** The
> seal parity selects single-valued/Dirichlet (=> periodic-compatible); the
> geometric time-reversal squares to +1 (bosonic Kramers); selecting T^2=-1
> requires importing a half-integer representation. The choice is UNFORCED.

---

## 5. q = 1/3 CONNECTION

Claim under test (P7): fractional charge q=1/3 signals projective / double-
cover structure, hence the antiperiodic spin structure.

What q=1/3 actually IS (banked, h1_types_results.md): q = 1 - 2/N = 1/3 is
the SLOPE in d ln f = -q d ln r, the public charge of the area-form
transgression Theta = (ln f) omega_H1, whose curvature Xi = dTheta =
-q (dr/r)^omega_H1 is EXACT (zero period over any closed cycle, by Stokes),
lives in the RADIAL x ANGULAR (H^2) sector, and — per the #37 VERIFIER
CORRECTION — is sigma-EVEN (omega_H1 sigma-invariant; the transgression
glues SYMMETRICALLY).

Spin structures, by contrast, live in **H^1(M; Z_2)** (a Z_2 datum on a
1-cycle, the time loop), and antiperiodicity is a HALF-integer / Z_2 sign.
q=1/3 is:
- a 1/3, not a 1/2 (no Z_2 half-period);
- sigma-EVEN, not the odd sector that could carry a fold twist;
- EXACT (no nontrivial period), so it carries no holonomy;
- in H^2, the WRONG cohomological slot for a spin structure (which is H^1).

> **VERDICT 5 [DERIVED negative]: q=1/3 does NOT correspond to / select the
> antiperiodic spin structure.** It is an EVEN, EXACT, H^2 charge in a
> different cohomological slot from H^1(;Z_2) where spin structures live; it
> is not a Z_2 spin datum and does not sit on the time circle that would
> carry antiperiodicity. The "fractional => projective => fermion" heuristic
> does NOT go through on the present (banked) derivation of q.
>
> CAVEAT (honest, scoped): this rests on the #37 verifier's sigma-EVEN
> re-grading of omega_H1 (which SUPERSEDED the earlier wcc-D3 sigma-ODD
> reading). IF a future same-minus junction computation re-grades the
> transgression's radial factor as sigma-ODD/orientation-reversing, the q
> datum would move to the odd/Dirichlet sector and a q-spin tie could reopen.
> Under the CURRENT banked facts, it does not.

---

## 6. SCOPE LADDER — what is established vs open

| Level | Statement | Status |
|-------|-----------|--------|
| EXISTS (weak) | a spin structure exists on the doubled cell (w_2=0) | **YES, DERIVED** (every shape) |
| ORIENTABLE | the doubled cell is orientable | **YES, DERIVED** (settles wcc/#37 flag) |
| ADMITTED (medium) | an ANTIPERIODIC (T^2=-1) spin structure is admitted | **ONLY IF time CLOSES into a circle** (H^1=Z_2); for interval time H^1=0 and it is NOT EVEN ADMITTED. "Time closes" is UNDERIVED (canon time is hyperbolic/propagating). |
| FORCED | global consistency FORCES antiperiodicity | **NO, DERIVED** (round-trip loop sigma^2=id, contractible for interval time; free Z_2 for circle time) |
| SELECTED | the physics PICKS OUT the fermionic structure where admitted | **NO, DERIVED** (seal parity => single-valued/periodic-compatible; geometric T squares to +1; q=1/3 wrong slot) |

---

## 7. VERDICT

**(1) Orientable / does a spin structure exist?** YES to both [DERIVED].
The time-reversal double is the boundary-double of an orientable cell, hence
ORIENTABLE; w_2 = 0 (S^2 Euler number 2 is even), so a spin structure
EXISTS in every candidate global shape. The wcc/#37 orientability flag is
resolved (the flagged "orientation reversal" was a single-sheet volume-form
sign, not a global non-orientability).

**(2) Does global consistency FORCE antiperiodicity (T^2=-1)?** NO
[DERIVED]. The seal is a REFLECTION (sigma: t->-t, an involution; sigma^2 =
id), creating a fixed surface, not a twist. The "through the seal and back"
loop is sigma^2 = id; for interval time it is CONTRACTIBLE, forcing
holonomy = +1 for every field; for circle time the antiperiodic option is a
FREE Z_2 choice, unforced. The mirror fold does not create a non-contractible
sign-carrying loop. **The global topology corroborates #46's local negative,
it does not overturn it.**

**(3) Is the fermionic structure FORCED / SELECTED or merely ADMITTED?**
At most ADMITTED, and only conditionally. For the DEFAULT banked structure
(interval/hyperbolic time) it is NOT EVEN ADMITTED (H^1=0). Closing time
into a circle (an UNDERIVED extra assumption) would ADMIT it, but then it is
one of two and is NOT SELECTED by the seal parity (which favours
single-valued/Dirichlet), by the geometric time-reversal (which squares to
+1, the bosonic Kramers), or by q=1/3.

**(4) q=1/3 connection?** NONE, on the banked derivation [DERIVED negative].
q=1/3 is the slope of an EVEN, EXACT, H^2 transgression — the wrong
cohomology slot (spin lives in H^1;Z_2), not a Z_2 half-period, not on the
time circle. It does not correspond to or select the antiperiodic spin
structure. (Scoped caveat: would reopen only if a junction computation
re-grades omega_H1 as sigma-ODD, currently superseded.)

**OVERALL VERDICT: a fermionic (T^2=-1) spin structure is NOT FORCED and NOT
SELECTED by the global topology of the time-reversal-doubled cell. A spin
structure EXISTS (w_2=0) and the doubled cell is ORIENTABLE; the
antiperiodic one is merely ADMITTED, and only IF the time direction closes
into a circle — which is itself UNDERIVED (canon time is hyperbolic). The
mirror fold, being a reflection (sigma^2=id), forces holonomy +1 on the
contractible round-trip loop. The GLOBAL route does not rescue the spinor the
LOCAL route (#46) lost: BOTH the local seal-value and the global holonomy say
the time-reversal fold ITSELF does not force the fermion's two-valuedness.**

Tag: METRIC-LED observation ("what spin structures does the derived doubled
topology carry?"), not TEMPLATE-LED ("can the metric make a spinor?"). The
result is a DERIVED NEGATIVE on forcing/selection plus a DERIVED POSITIVE on
existence+orientability. It deliberately STOPS at ADMITTED-conditionally and
names the two underived hinges (does time close? is there a physical T^2=-1
selector?) rather than narrating convergence to "the fermion."

CONSEQUENCE FOR THE PROGRAM (honest): with both the LOCAL (#46) and the
GLOBAL (this) routes giving the time-reversal FOLD no power to force the
fermion's two-valuedness, the remaining live candidates for sqrt(m)/the
spinor are the ones #46 named that are NOT the fold: the Hopf-squaring
n = psi-dag sigma psi (spinor as the SQUARE ROOT of the winding field, a
DIFFERENT mechanism), and a physical T^2=-1 selector that would have to come
from OUTSIDE the seal topology. The fold is not the fermion's origin.

---

## PREMISE-SCOPED NEGATIVE (proposed for NEGATIVES_REGISTRY)

THE GLOBAL TOPOLOGY OF THE TIME-REVERSAL DOUBLED CELL DOES NOT FORCE OR
SELECT A FERMIONIC (T^2=-1) SPIN STRUCTURE. Doubled cell is ORIENTABLE
(boundary-double of orientable cell) and ADMITS a spin structure (w_2=0,
S^2 Euler number even). H^1(M;Z_2) = 0 for interval/hyperbolic time (unique
PERIODIC structure; antiperiodic not even admitted) and = Z_2 only if the
time direction is closed into a circle (then antiperiodic ADMITTED but
UNFORCED, a free Z_2). The through-seal round trip is sigma^2 = id
(involution), contractible for interval time => holonomy +1 forced. q=1/3 is
an EVEN, EXACT, H^2 transgression slope — wrong cohomology slot for spin
(H^1;Z_2) — and does not select the antiperiodic structure. PREMISES: P1
(I_r x S^2 cell, #37); P2 (sigma = t->-t, angular untouched, #42/#37
correction); P3 (boundary-double construction); P5 (time INTERVAL by default
— canon time hyperbolic C-2026-06-13-1; "time closes" is an extra underived
assumption, reported as a fork); P6 (q=1/3 = even/exact/H^2 transgression,
#37 verifier correction). The Hopf-squaring (n = psi-dag sigma psi) and an
external physical T^2=-1 selector are NOT addressed (out of scope, not
refuted). DATA-BLIND. Pending Charles + blind verifier.

---

## BLIND VERIFIER — PENDING. Attack here:

1. **ORIENTABILITY (Part 1).** Challenge "boundary-double of orientable =>
   orientable." Is the seal genuinely a fixed-surface boundary along which a
   standard double is taken, or does the same-minus junction (g_tr,g_ttheta
   sign flip) implement an orientation-reversing IDENTIFICATION that makes a
   NON-orientable (mirror/Klein-type) glue? Do the actual same-minus
   junction condition across D=0 (the wcc-flagged computation) and confirm or
   refute that the coordinate orientation form glues consistently. If the
   physical gluing is orientation-reversing, w_1 != 0 and the whole spin
   analysis changes.
2. **w_2 and H^1 (Part 2).** Recompute w_2(M) and H^1(M;Z_2) independently
   for BOTH shapes. Confirm S^2 Euler number is even (=> spin) and that
   H^1(S^2;Z_2)=0, H^1(S^1xS^2;Z_2)=Z_2. CHALLENGE the homotopy-type
   reduction: is the doubled cell genuinely ~ S^2 (interval time) or could
   the radial collar / core cap (the #37 fork: r->0 cap => S^3, finite seal
   => S^2xS^1, p-twist => L(p,q)) change H^1 or w_2? Redo for the S^3, S^2xS^1,
   L(p,q) core-closure variants and report whether ANY admits a FORCED
   antiperiodic structure.
3. **THE HOLONOMY (Part 3, most important).** Attack the "round-trip loop is
   sigma^2=id, contractible => +1 forced." (i) Is there ANY non-contractible
   loop in the DEFAULT (canon, interval-time, hyperbolic) doubled cell whose
   holonomy could be -1? (ii) Does the sigma-ODD time row, treated as a
   CONNECTION (not just metric components), contribute a Z_2 holonomy the
   pure-coordinate argument misses? (iii) Could the core cap (r->0) or a
   p-fold twist (L(p,q)) introduce torsion in H^1 carrying a forced sign?
4. **TIME-CLOSURE (P5, the load-bearing fork).** Is "time is an interval /
   hyperbolic" really the canon default, or does the finite mirrored
   universe-cell (C-2026-06-10-2) plus the matter-cell mirror secretly CLOSE
   time? If time DOES close, re-grade: antiperiodic ADMITTED — then attack
   SELECTION (Part 4) hardest.
5. **q=1/3 (Part 5).** Challenge the "even/exact/H^2 => no spin tie." Is the
   #37 verifier's sigma-EVEN re-grading of omega_H1 correct, or does the
   actual same-minus junction make the radial factor sigma-ODD (wcc-D3),
   moving q to the odd sector and reopening a q-spin link? This is the same
   junction computation as attack #1 — settle it once.
6. **TARGETING CHECK.** The verdict is NOT-FORCED / NOT-SELECTED / EXISTS-and-
   ADMITTED-conditionally. Confirm the analysis OBSERVED the topology rather
   than steering to a desired (negative OR positive) answer. In particular
   check it did not UNDER-claim by defaulting to interval-time to kill the
   fermion: is the interval-time default genuinely the banked structure?

---
## VERDICT NOTE (appended 2026-06-14; blind verifier PENDING; corroborates #46)
The mirror fold does NOT force the spinor GLOBALLY: doubled cell ORIENTABLE,
spin structure EXISTS (w_2=0), but sigma=t->-t is an involution (sigma^2=id, a
fixed SURFACE not a twist) so the through-seal loop is contractible => holonomy
+1, all fields single-valued; for canon interval/hyperbolic time H^1(M;Z_2)=0,
the antiperiodic (fermionic) structure is NOT EVEN ADMITTED. q=1/3 is in H^2
(even, exact transgression), the WRONG slot for a Z_2 spin label. Corroborates
the LOCAL #46 negative. OPEN HINGES (flagged, not yet computed): the actual
same-minus junction across D=0 (orientation-preserving? omega_H1 even or odd?);
whether the finite-cell canon closes time into a circle. The fermion's origin is
NOT the fold; live sqrt(m)/spinor candidate = the Hopf-squaring route.

---

## BLIND ADVERSARIAL VERIFIER PASS — 2026-06-15
VERIFIER global_spin / 2026-06-15 / a7f3c9e21d6b08e4 (independent machinery,
not a re-run of global_spin_structure.py).

VERDICT: **STANDS-WITH-CAVEAT.** The registered negative (the global topology of
the time-reversal-doubled cell does NOT force or select a fermionic T^2=-1 spin
structure) survives independent reconstruction in sympy/numpy.

INDEPENDENTLY REPRODUCED: sigma^2=id exactly; reflection Jacobian det=-1 (single-
chart orientation flip only); w2(S^2)=0 (spin structure EXISTS in every candidate
shape); H^1(M;Z2)=0 for interval time, Z2 for circle time; core-closure forks
S^3->0, S^2xS^1->Z2, lens L(p,q)->Z2 iff p even (none changes the verdict);
q=1/3 is a real H^2 1-form coefficient (1/3 mod 1 != 1/2), wrong slot for a Z2
spin label, and exact (zero holonomy).

STRENGTHENING (cleaner than the doc's contractible-loop argument): whenever w2=0
the spin structures form a torsor over H^1(M;Z2) and the PERIODIC (bounding)
structure is ALWAYS a member; therefore an antiperiodic structure can NEVER be
forced by topology alone, in ANY shape — so NOT-FORCED is robust even to the
time-closure fork, not just to interval time.

CAVEAT (non-load-bearing): with w1=w2=0 BOTH Pin+ and Pin- exist, so a reflection
lift squaring to -1 (Kramers T^2=-1) IS topologically ADMISSIBLE. The doc's
sub-statement "the geometric time-reversal squares to +1" is therefore too strong;
correct reading = "admits both +-1 lifts; +1 is geometrically natural, -1 is not
SELECTED by any banked condition." NOT-FORCED and NOT-SELECTED both still stand;
the -1 lift is admitted-but-unselected, not unavailable. A genuine physical
T^2=-1 / Kramers / fermion-number SELECTOR from OUTSIDE the seal topology remains
the live route — consistent with the handoff.

OPEN HINGES (confirmed): (1) the same-minus junction across D=0 (orientability;
omega_H1 sigma-even vs sigma-odd) gates the orientability sub-claim and the q-spin
caveat; (2) Pin- admissibility (new) — the result rests on selection, not
unavailability. No data/wall-numbers used; no targeting detected.
