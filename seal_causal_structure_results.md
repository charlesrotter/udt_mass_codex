# RESULTS: the SEAL's causal structure — right-kind vs wrong-kind nonlocality (Check 3, BREAK A)

STATUS: OBSERVE results, PRE-REGISTERED (seal_causal_structure_PREREG.md), NOT yet blind-verified,
NOT canon. Derivation track, LOCAL branch session-2026-06-17 ONLY. NOT committed (verifier-before-record).
Driver: Claude (Opus 4.8 1M). Date: 2026-06-17.
Compute: sympy 1.14 (exact symbolic). Scripts (this run, not committed): the four /tmp/seal_causal*.py
blocks reproduced inline below; every algebraic identity re-derivable from the cited exact metric.

## DISCIPLINE / GUARD STATEMENT

Observed the geometry's causal cones from the EXACT W6 metric; imported/posited nothing. No approximation
as a stated result — the one expansion used (D -> 0 near-fold) is declared and its leading order is the
EXACT vanishing order (det proportional to D, linear), not a truncation of interest. VERDICT-HUNTING
GUARD honored: the result is reported as it fell out, and it is NOT the pilot-wave program's most
convenient outcome (it is the (c)-leaning "wrong-axis with a no-signaling caveat" finding, see G5).

## THE EXACT METRIC (cited, not posited)

W6 THE SYSTEM block (w6_arm1_lib.py:8-27, cited in VERIF_w_completed_barrier.py:26-29; W6_results.md):

    g4 = [[-f,   a,    b,    0          ],
          [ a,  1/f,   q,    0          ],
          [ b,   q,   r^2 W, 0          ],
          [ 0,   0,    0,    r^2 sin^2 th / W ]]

    W = (1+w)^2,   D = r^2 W - f q^2,   f = e^{-2phi} (the dilation; c_eff = f in bulk).
    a = g_Tr, b = g_Ttheta = the TIME ROW (zero on the static slice; the same-minus involution sigma
    flips (a,b) -> (-a,-b); the fold is sigma's FIXED surface, a=b=0).

The SEAL = the surface D -> 0 (W6: the q*-branch signal speeds diverge as 1/D there). f stays finite
in the bulk (~5 at hadronic depth) and -> inf only at the cell-core endpoint phi -> -inf (CANON);
the D=0 fold and the phi->-inf endpoint are the two distinct "c_eff opens" loci. This run analyzes the
D=0 MIRROR FOLD (the W6 object the MAP re-centered Check 3 on).

EXACT identity re-confirmed this run (matches W6_results.md:41-47):
    det g4 = -(r sin th)^2 / [f (1+w)^2] * [ f D (1+a^2) + (b - f q a)^2 ].
    ON D=0:  det g4 = -(r sin th)^2 (b - f q a)^2 / [f (1+w)^2]  — NONZERO for b != f q a.
(Verified: sympy det of g4 minus the W6 closed form simplifies to 0.)

---

## G1 — CAUSAL CONES (exact)

Inverse static-slice block (a=b=0), exact:
    g^TT  = -1/f                 (FINITE everywhere f is finite — depends on phi ONLY, not on D)
    g^rr  =  f r^2 W / D         (diverges as 1/D at the fold)
    g^thth =  1 / D              (diverges as 1/D at the fold)
    g^rth = -f q / D             (diverges as 1/D)

Coordinate signal (phase) speeds of the d'Alembertian g^{mu nu} k_mu k_nu = 0:
    radial   v_r^2  = -g^rr/g^TT  = f^2 r^2 W / D   -> +infinity as D->0   (the 1/D divergence)
    angular  v_th^2 = -g^thth/g^TT = f / D          -> +infinity as D->0   (the 1/D divergence)

RESULT G1: BOTH SPATIAL legs of the null cone open without bound (v^2 ~ 1/D) approaching the fold, while
the TIME leg g^TT = -1/f is untouched. So the coordinate light-cone FLATTENS OPEN ("instantaneous in
coordinates") at D=0. This is the q*-branch 1/D divergence (W6) entering as the cone opening: it lives
entirely in the INVERSE-metric spatial block (g^rr, g^thth, g^rth all ~ 1/D); the time component is
regular. The opening is a COORDINATE statement — G2 tests whether it is a physical channel.

VERDICT G1: the cone opens, in the COORDINATE sense only (proven; the proper sense is G2). SUCCEEDS vs
the pre-registered G1 (derive cones, locate the 1/D entry) — done exactly.

---

## G2 — SIGNALING vs NO-SIGNALING (THE CRUX, exact)

### Reaching the fold (from the bulk): FINITE
- Radial proper-length element: the spatial metric component h_rr = 1/f is FINITE and smooth at the fold
  (it carries NO D; depends on phi only). Proper RADIAL distance to the fold is finite.
- The W2 medium-wave (c_eff = f, finite in the bulk) propagates over a finite proper distance with finite
  action. ENERGY to bring a signal TO the fold: FINITE.
  => reaching the fold is unobstructed. (This is why the fold is "a locus of instantaneous connection" in
  the naive reading — the approach is real.)

### Crossing / using it as a channel: BLOCKED by a proper-volume + infinite-energy pinch
The decisive exact fact (S3 — coordinate divergence vs physical traversal):

    det(spatial 3-slice h_ij) = sin^2 th * r^2 * D / (f W)   ->  0   as D -> 0,
    for ANY constant-T slicing (time row on OR off — the spatial block is identical; the time row only
    fills the T row/column). [sympy-verified exact.]

The (r,theta) 2-block has det = D/f (vanishes LINEARLY in D) and FINITE trace = r^2 W + 1/f — so EXACTLY
ONE spatial eigenvalue -> 0 (a proper-length pinch) while the orthogonal direction stays finite. The
fold is a codimension-one PINCH of the spatial slice: a finite coordinate neighborhood of the fold has
proper spatial VOLUME -> 0.

Consequence for a signal (the energy block):
- The spatial inverse metric blows up as 1/D, so the gradient-energy density of any non-trivial transverse
  profile diverges: (1/2) h^thth (d_theta psi)^2 ~ (1/2)(1/D)(d_theta psi)^2 -> infinity.
- Equivalently, the angular null dispersion is om^2 = (f/D) k_theta^2. A FINITE-frequency (finite-energy)
  signal must have k_theta proportional to sqrt(D) -> 0: infinite proper wavelength, i.e. it carries NO
  localizable transverse information. To push a localized (finite-k_theta) signal through, om -> infinity
  (infinite energy / frequency).

RESULT G2: the coordinate cone-opening (v^2 ~ 1/D) is a PROPER-VOLUME PINCH + INFINITE-ENERGY block, not a
traversable physical channel. Reaching is finite; crossing-with-information costs divergent energy. By the
standard criterion (no finite-energy + controllable transit), this is **NO-SIGNALING**.

VERDICT G2: NO-SIGNALING (the coordinate divergence is a block, not a transit). This is the (a)-compatible
half of the answer. SUCCEEDS vs pre-registered G2 — the proper-time/energy computation was performed and
is decisive.

CRUX NUANCE (honest, not buried): "the cone opens but throughput costs infinite energy" is the SAME
structure as a horizon/coordinate-singularity block — it guarantees no SIGNALING, but it equally means the
fold does NOT hand you a usable connection. A no-signaling block that blocks ALL transverse information is
"no-signaling" the way a wall is no-signaling. Whether it can still carry CORRELATION (a fixed kinematic
identification across the crease) is the G3/G4 question, and that is where the right-kind reading weakens.

---

## G3 — WHAT IT CONNECTS (config-space crux, exact structure)

The fold is the FIXED SURFACE of the same-minus involution sigma: (a,b) -> (-a,-b) (W6_results.md:16).
A fixed surface of an involution joins each point to ITS OWN IMAGE under sigma. On the fixed set
sigma(p)=p. The two "sides" welded at the crease are a configuration and its MIRROR (time-row-flipped)
copy of the SAME cell.

RESULT G3: the fold is a **SELF-identification** (point <-> its own mirror image), NOT a bridge between
two pre-existing INDEPENDENT bulk points. There is no A -> seal -> B route with A and B distinct,
independent particles' positions: the only thing on the far side of the crease is the sigma-image of the
same cell (CANON: matter/universe cells are finite MIRRORED domains; the fold is ONE cell's mirror crease,
not a wormhole between two cells' interiors). The earlier topological-bridge route was already tested DEAD
(MAP LATER-12); this confirms the geometric reason — the fold's identification is reflexive.

This is the LOAD-BEARING finding against the Bell category: Bell correlation links TWO independent
particles (a configuration-space, 3N-dim object). A self-image gluing of one cell cannot, by its
construction, mediate a correlation between two INDEPENDENT particles' measurement outcomes.

VERDICT G3: SELF-CONNECTION (wrong axis for two-particle Bell correlation). SUCCEEDS vs pre-registered G3
(distinct-points vs self-image resolved — it is self-image).

---

## G4 — CONTROLLABILITY (exact-structure argument)

The identification across the fold is the FIXED kinematic structure of the involution sigma — a discrete
metric symmetry / geometric gluing, not a tunable operation. A local bulk operation can change field DATA
but cannot alter sigma's gluing rule. And imprinting a controllable, localized influence ACROSS the crease
requires transverse structure at the fold, which costs divergent energy (G2). So any influence carried is
a FIXED kinematic identification (correlation-type), never a controllable signaling operation.

RESULT/VERDICT G4: kinematic / no-signaling (correlation only, if anything). Consistent with G2. But note
the dependency: the "carries correlation" claim needs G3 to supply two distinct correlated endpoints, and
G3 found a self-image, not two endpoints.

---

## G5 — VERDICT (classify the seal's nonlocality)

Pre-registered options: (a) RIGHT-KIND (no-signaling, distinct points, carries correlation);
(b) WRONG-KIND / super-quantum (usable signaling channel); (c) WRONG-AXIS / NULL (self-connection only,
or transit blocked — carries nothing for two-particle Bell).

Component verdicts:
- G1: cone opens (coordinate sense, 1/D). 
- G2: NO-SIGNALING — the opening is a proper-volume pinch + infinite-energy block, not a usable channel.
  => DEFINITIVELY NOT (b). The seal is NOT a super-quantum signaling channel. The "too much" worry is
  geometrically refuted: c_eff -> inf at the fold does NOT give a usable fast-signal channel.
- G3: SELF-CONNECTION (point <-> its own mirror image), NOT a link between two independent bulk points.
- G4: kinematic only (no controllable influence).

OVERALL VERDICT: **(c) WRONG-AXIS / NULL**, with a clean sub-finding that the (b) super-quantum fear is
ruled out.

The seal passes the no-signaling test (G2 — good, it is not "too much"), but FAILS the config-space /
distinct-points test (G3): it is a self-image gluing of one cell, not a connection between two independent
particles. A two-particle Bell correlation needs the latter. Therefore "the seal IS the Bell-nonlocality
channel" is the WRONG CATEGORY at the geometric level: the seal cannot, by its involution-fixed-surface
construction, be the locus that correlates two independent distant particles. It also transmits no
localizable transverse information (G2 pinch), so it carries "nothing" usable across.

Against the FROZEN success/failure criteria: the (a) RIGHT-KIND criterion requires "connects distinct
points AND could carry configuration-space correlation." G3 shows it connects a point to its own image,
NOT distinct independent points. So criterion (a) FAILS; criterion (c) is MET.

=> Per the frozen contract: **conjecture B's seal-route for Bell nonlocality is REFUTED at the category
level (premise-scoped)**. The program would need a different home for two-particle nonlocality (the MAP
named candidates: the config-space measure, the closed-time sector). The one genuinely POSITIVE rescue is
recorded in the premise ledger #5 below (an inter-cell, not intra-cell, fold), but that is a DIFFERENT
geometric object than the one analyzed and is presently unbuilt.

---

## PREMISE LEDGER (chose / derived)

1. Seal = mirror fold, regular Lorentzian (time row on), q*-speeds ~ 1/D — DERIVED (W6; re-confirmed this
   run: det g4 closed form reproduced exactly). STRONG.
2. The analyzed seal is the D=0 fold, NOT the phi->-inf endpoint — DERIVED scoping (STATE LATER-4 / CANON
   distinguish them). CHOSE which locus to analyze: the D=0 fold (the W6 object the MAP centered Check 3
   on). The phi->-inf endpoint (c_eff=f->inf there) is a DISTINCT locus, NOT analyzed here; flagged as the
   one untested sibling object (see #6).
3. Wave operator whose characteristics were computed: the d'Alembertian of the EXACT W6 4-metric (its
   spatial-block determinant + inverse), which is the operator the W2 medium-wave and the W6 coupled
   operator both share for their PRINCIPAL part / causal cones. The verdict (cone opens via 1/D inverse-
   metric; spatial pinch det h ~ D) is a property of the METRIC's principal symbol, hence operator-robust
   for any second-order wave on this metric. DERIVED. (Sub-leading potential terms do not change the
   causal cones.) Sensitivity: LOW for G1/G2 (principal-symbol level).
4. No-signaling criterion = no finite-energy + finite-proper-distance + controllable transit. STANDARD;
   tagged. The G2 block is an infinite-ENERGY / zero-proper-VOLUME block (both reparam-invariant), the
   strongest form. CHOSE the criterion (standard).
5. "Self-image, not distinct points" (G3) — DERIVED from the involution-fixed-surface characterization
   (W6) + CANON finite-mirrored-cell. STRONG. This is the load-bearing premise of the (c) verdict.
6. POSITIVE-RESCUE caveat (not targeted, recorded for honesty): IF distinct cells share a common mirror
   crease (two cells' boundaries identified at one fold), the fold WOULD connect distinct cells — but that
   is an INTER-cell object, geometrically different from the intra-cell self-fold analyzed, and is
   presently unbuilt (the MAP's "all matter cells terminate at seals; inter-cell bridge via the angular
   sector" is conjecture, LATER-12 topological version DEAD). Tagged CHOSEN-not-to-pursue-here; a clean
   follow-up if Charles wants the inter-cell fold mapped.

## CONFIDENCE

- G1 (cone opens, coordinate, 1/D in the inverse-metric spatial block): HIGH (~0.9) — exact, principal-
  symbol-level, operator-robust.
- G2 (NO-SIGNALING; det h ~ D pinch + 1/D energy block): HIGH (~0.85) — exact spatial-determinant
  identity; the energy-block reading uses the standard finite-energy criterion (premise #4).
- G3 (self-image, not distinct points): MEDIUM-HIGH (~0.75) — rests on the involution-fixed-surface
  characterization (premise #5); the inter-cell rescue (#6) is the only way it flips, and it is unbuilt.
- G5 (verdict (c), with (b) ruled out): MEDIUM-HIGH (~0.75) — inherits G3's confidence; the (b)-exclusion
  is HIGH.

## LOAD-BEARING PREMISES FOR THE BLIND VERIFIER

- G2 crux: det(spatial 3-slice h_ij) = sin^2 th r^2 D/(fW) -> 0 (the (r,theta) 2-block det = D/f vanishes
  LINEARLY, trace finite => exactly one eigenvalue pinches), while h_rr = 1/f stays finite. Re-derive
  independently; confirm the coordinate cone-opening (g^rr, g^thth ~ 1/D) is a proper-volume / infinite-
  energy BLOCK, not a finite-energy transit. Attack: is there a slicing or a finite-energy mode that
  crosses with localizable transverse info? (Claimed NO.)
- G3 crux: is the fold a SELF-image gluing (one cell <-> its mirror) or a link between two DISTINCT
  independent bulk points? Verdict (c) depends on "self-image." Attack the inter-cell-fold rescue (#6):
  can two distinct cells share one crease such that the fold connects distinct cells? (If yes, (c) could
  move toward (a) — but the object would be the unbuilt inter-cell fold, not the analyzed intra-cell one.)

## NOT COMMITTED. Awaiting independent blind verifier (S5).

---

## BLIND VERIFIER BLOCK — agent (Opus 4.8 1M), 2026-06-17

Independent re-derivation (sympy 1.14, /tmp/verif_seal{,2,3,4}.py; NOT committed). No shared
machinery with the run's scripts. Per-task verdicts below.

### (A) NO-SIGNALING (G2) re-check — SURVIVES
All algebra reproduced EXACTLY (sympy difference = 0 in every case):
- det g4 closed form `-(r sinθ)^2/[fW]·[fD(1+a^2)+(b-fqa)^2]` — exact.
- det(spatial 3-slice h) = sin^2θ·r^2·D/(fW); (r,θ) 2-block det = D/f, trace = r^2W + 1/f
  (finite). Exactly ONE eigenvalue pinches as D→0 (proper-volume pinch), h_rr-direction stays
  finite — confirmed.
- Inverse block: g^rr = f r^2 W/D, g^thth = 1/D, g^rth = -fq/D; phase speeds v_r^2 = f^2 r^2 W/D,
  v_th^2 = f/D; angular null dispersion ω^2 = (f/D) k_θ^2. All exact, all ~1/D.
- The no-signaling logic is sound: a finite-ω (finite-energy) angular signal forces k_θ ∝ √D → 0
  (infinite proper wavelength, no localizable info); a localized signal costs ω→∞. This is a
  horizon-type / proper-volume + infinite-energy BLOCK, both reparam-invariant. No finite-energy,
  finite-proper-distance, controllable transit exists across the D=0 fold. (b) super-quantum is
  genuinely RULED OUT **at the D=0 fold**. I found no missed finite-energy/finite-proper-time route.

### (B) THE TWO-LOCUS GAP (make-or-break) — PARTIAL (the run tested the WRONG surface for conjecture B)
Confirmed the loci are DISTINCT, not the same surface:
- D=0 requires f q^2 = r^2 W (finite). phi→-inf gives f=e^{-2φ}→+∞, hence D = r^2W - f q^2 → **-∞**
  (q≠0) or → r^2W finite (q=0). Neither is D=0 generically. The run's caveat #2 is correct: D=0 and
  phi→-inf are genuinely different divergence conditions.
- **Which locus did conjecture B name?** The MAP (lines 12-14) and PREREG (lines 9, 14, ledger #2)
  BOTH define the Bell/seal locus as "c_eff = e^{-2φ} → ∞ at the cell boundary **phi → -inf**" — the
  CANON C-2026-06-10-2 core endpoint, NOT the W6 q*-branch D=0 fold. So the run analyzed a DIFFERENT
  surface (D=0, the W6 q*-speed divergence) than the one conjecture B actually named (phi→-inf).
  This is the single biggest scoping weakness: the verdict is delivered at a locus the conjecture
  did not name. The run is honest about this (caveat #2), but the headline "(b) RULED OUT" is, as
  stated, established at D=0 — not yet at phi→-inf.
- **phi→-inf endpoint causal structure (the untested surface), re-derived here** on the diagonal
  cell g_tt=-f, g_rr=1/f (a=b=q=w=0 reduction; STATE LATER-5's frame), representative monotone
  profile φ=A ln(r/R), A>0, φ→-∞ as r→0 of a FINITE cell:
  * c_eff = f = e^{-2φ} = (R/r)^{2A} → +∞ (cone opens — coordinate sense). CONFIRMED.
  * proper radial distance core→interface = R/(A+1): **FINITE** (reaching the endpoint is finite,
    like the fold).
  * coordinate light-travel time = R/(2A+1): finite.
  * proper time of a static clock ∝ e^{-φ}=(R/r)^A → ∞ at core (clock runs infinitely fast); local
    frequency ω_local = ω e^{φ} → 0 — modes FREEZE toward zero proper-frequency (matches STATE
    LATER-5: the intuition's sign is backwards; deep core freezes modes, does not blueshift them).
  * to keep any FINITE proper-frequency signal at the core, coordinate ω = ω_local e^{-φ} → ∞:
    **infinite energy** — SAME infinite-energy block as the D=0 fold.
  * crossing: the core is a TERMINUS, mirrored across φ→-φ (CANON: matter cell is the mirror of the
    CMB boundary). "Crossing" = reflection into the mirror image = self-connection, NOT passage to
    an independent bulk point.
  VERDICT at phi→-inf: ALSO no-signaling (infinite-energy block) + self/terminus (mirror reflection),
  NOT a usable signaling channel and NOT a link to a distinct bulk point. So the (c)/(b)-ruled-out
  verdict **does survive at the correct locus too** — but on the diagonal-cell premise (q=0,w=0),
  which is a CHOSE, not the full W6 stationary geometry the run used for D=0. The endpoint deserves
  the same exact full-metric treatment the fold got before "(b) ruled out" is banked there.

### (C) SELF-CONNECTION (G3) re-check — SURVIVES (premise-scoped)
The fold is the FIXED surface of the same-minus involution σ:(a,b)→(-a,-b); a fixed set joins each
point to its own σ-image (σ(p)=p on it). Geometrically this is a self-identification of ONE cell with
its time-row-flipped mirror, not a bridge between two independent bulk points — sound given the W6
involution characterization + CANON finite-mirrored-cell. The phi→-inf endpoint independently gives
the same conclusion (terminus mirrored across φ→-φ). The #6 inter-cell shared-crease rescue is genuine
as a logical possibility but UNBUILT and, on the current corpus, wishful: the topological inter-cell
bridge was tested DEAD (LATER-12), and no geometrically natural continuous inter-cell fold has been
constructed. It cannot currently move the verdict.

### (D) PREMISE AUDIT — PARTIAL
"(c) wrong-axis/null, (b) super-quantum ruled out, seal≠Bell-nonlocality at category level" SURVIVES,
but the refutation is SCOPED, not clean:
- At the D=0 fold (the surface actually computed): clean and exact. (b) ruled out HIGH; (c) MEDIUM-HIGH
  (rests on the involution self-image premise).
- At the phi→-inf endpoint (the surface conjecture B actually named): my independent re-derivation
  finds the SAME structure (no-signaling infinite-energy block + self/terminus), so the verdict does
  NOT flip — but it was established here on the diagonal-cell premise, not the full stationary W6
  metric, and the run did not test it at all. So "(b) ruled out" is presently PROVEN at D=0 and
  STRONGLY-INDICATED (not proven) at phi→-inf.
- Net: the conclusion does NOT change once the phi→-inf endpoint is analyzed — both loci give
  no-signaling + self-connection. The category-level refutation of "seal = Bell nonlocality" holds at
  both loci. What is NOT clean is that the run delivered its headline at D=0 while naming caveat #2,
  when the conjecture's named locus is phi→-inf; this is a presentation/scoping defect, not a sign
  error in the physics.

### OVERALL
- (A) SURVIVES · (B) PARTIAL · (C) SURVIVES (premise-scoped) · (D) PARTIAL.
- Confidence that the verdict [(c) wrong-axis/null; (b) super-quantum ruled out] is correct: **~0.82.**
  (b)-exclusion is the strongest leg (~0.9 at D=0, ~0.8 at phi→-inf on the diagonal premise);
  (c)/self-connection inherits the involution + finite-mirrored-cell premises (~0.75).
- BIGGEST WEAKNESS: the run computed the D=0 q*-branch fold, but conjecture B's named locus is the
  phi→-inf core endpoint (MAP/PREREG ledger #2). The verdict is delivered at a locus the conjecture
  did not name. My independent phi→-inf analysis shows the verdict survives there too (same
  no-signaling + self/terminus structure, sign of the redshift CONFIRMS freeze-not-blueshift per STATE
  LATER-5), so the conclusion is unchanged — but to bank "(b) ruled out" at the correct locus, the
  phi→-inf endpoint needs the same exact full-W6-metric treatment the fold received (it was checked
  here only on the q=0,w=0 diagonal cell).
- DOES THE CONCLUSION CHANGE at the correct locus? **No.** Both loci block signaling (infinite-energy /
  frozen-mode) and both are self/terminus identifications, not links to independent bulk points. The
  "seal = Bell nonlocality" category claim is refuted at BOTH loci on present premises.

