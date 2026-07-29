# GR-ANALOG RECONNAISSANCE REPORT (TG1–TG4)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before the survey).
Companion data file: `GR_ANALOG_MAP.tsv` (26 rows, columns per contract; every row carries a
mandatory DISANALOGY and an attribution status). This is a METHOD survey: machinery and
failure surfaces only; no GR answer is recommended for adoption anywhere in this document
(F-G1), and no analog is claimed to BE a P4 problem (F-G2 — shape-analogy only, disanalogy
always stated).

**THE LANE CLAUSE (travels verbatim, non-droppable):** these triggers police the SMUGGLE OF
PHYSICS, never the BORROWING OF METHOD. CATEGORY-A (conditioning / numerical technique / *how*
we solve) is ALWAYS GREEN and only needs a soundness/convergence check — including USING GR AS A
REFERENCE/LIMIT. A technique changes HOW we solve the UDT equations, not the physics; only two
duties — apply it to the UDT equations (don't silently swap in GR's), and soundness-check it.
CATEGORY-B (a change to the PHYSICS — a mechanism, coupling, equation-form, source, or a
structure-holding BC) is gated. A "forbid"-only half over-blocks.

**Standing caveat (travels with every row so marked):** Route A Stage 2 is still under
verification. Every statement leaning on Stage-2 specifics — above all the pointwise Noether
vacuity claim and the ℛ_PW parametrization — is tagged **PROVISIONAL-pending-Stage-2-bank**
and must be re-read after the Stage-2 verifier banks or amends. **Refinement landed (Stage-2
verifier, 2026-07-29; applied to this document as amendment A2):** the UNQUALIFIED vacuity is
superseded. The refined claim is: R7(b) Noether identities are GENERICALLY pointwise-vacuous
(trivial per-member stabilizer on generic strata), BUT on resonance strata (k_mod=0; also C=0
with λ∓k_mod ∈ {±1}) a continuous class-tangent gauge direction survives and imposes exact
pointwise Noether identities — e.g. on k_mod=0: −2k10·r_tf + m00c10 + m01c11 − m10c00 −
m11c01 = 0. The surviving content is stratum-local and discrete-character-graded — NOT a
restored GR-like Noether-II tower (no arbitrary-function parameter is implied) — so the
Wald-charge, Utiyama, and constraint-classification failure surfaces below hold GENERICALLY,
with the stratum-local exception recorded in place where it bites. Still PROVISIONAL until
the Stage-2 bank.

---

## TG1 — the correspondence map, narrated by vein

Vein census: the §1 floor (6 items) is fully covered; the charter item (vein 6 of the prereg)
is expanded into four distinct veins, and two veins are ADDED (Fefferman–Graham as a named
CONTRAST; the geon/topology vein made explicit). Total: **11 veins, 26 map rows.** No floor
vein dropped.

### Vein 1 — Lovelock + natural tensors / variational bicomplex ↔ the inverse problem

Lovelock (1971, VERIFIED: JMP 12, 498–501) is the corpus's flagship instance of exactly the
Route A problem SHAPE: "classify ALL objects of a stated type satisfying typed constraints,
and determine whether the space is empty, a point, or a family." In 4D, symmetric
divergence-free 2-tensor concomitants of (g, ∂g, ∂²g) = a·G + b·g — a POINT (up to two
constants). The machinery: invariant theory of concomitants, the normal-coordinate/replacement
jet-reduction, dimension-dependent identities, and the divergence-free condition as an
overdetermined system on coefficients. What transforms: the problem shape and the
classification style — and the finite-group half of the invariant-theory machinery has
ALREADY crossed the bridge natively (Stage 2's character modules over the 11-generator
invariant ring are the K₄ version of the same classification move; PROVISIONAL). What does
not: all three inputs that source Lovelock's uniqueness pressure (full invariance,
divergence-free identity, second-jet bound) are absent or altered on the UDT domain (TG2/TG4).
The global companion (Anderson–Duchamp 1980, VERIFIED) contributes the cleanest structural
match of the whole survey: the local-variational vs globally-variational split with a
cohomological obstruction is EXACTLY the gate-3 vs gate-6 split, already typed in the specs.

### Vein 2 — inverse problem of the calculus of variations ↔ L6/L7

Helmholtz conditions (self-adjointness of the formal linearization; global version Takens
1979, VERIFIED; bicomplex school) are gate 3's literal content — with the one forced UDT
modification that the corpus never makes: the pairing is a VARIABLE. The corpus states
variationality as an absolute because it silently fixes the duality (fibred structure +
volume form); L7 says the pairing is part of the missing object, and Route B T4 proves the
volume choice is load-bearing (blindness loci). So the corpus absolute becomes a UDT relative
statement — self-adjoint UNDER P1/P2/P3 as declared. Douglas (1941, VERIFIED: Trans. AMS 50,
71–128) answers the multiplier question completely only for n=2 ODE systems, by a
case-analysis on the Jacobi endomorphism that is irreducibly finite-dimensional; the general-n
and PDE/field cases are open IN THE CORPUS ITSELF. On the typed domain, "the multiplier
problem" would mean: which element of the enumerated pairing structures (P1's constrained
volume functional / P2's declared dual class / P3's stratum trace maps) renders a given ℛ_PW
member self-adjoint — a question with Douglas's shape but none of Douglas's tools, since the
UDT multiplier is not a free g_ij but a TAGGED supplied structure drawn from a typed menu.
Vainberg/Tonti (VERIFIED) contribute the structural lemma (potentialness is pairing-dependent)
and simultaneously the named import shape: Tonti's integrating-operator trick INVENTS kernels
to force variationality — on UDT an invented kernel is unregistered structure, the MAP's L6
HABIT flag in corpus clothing.

### Vein 3 — boundary/corner variational completeness ↔ R6 / gate 5

GHY (York; Gibbons–Hawking 1977; VERIFIED) and Hayward corners (VERIFIED — content confirmed
via secondary sources; the exact 1993 journal citation not individually checked, caveat
carried in the map row) supply
the machinery for "which boundary data make variation differentiable on a FINITE region":
integrate by parts, enumerate the unpaired boundary jets per candidate order, then either
(corpus) append a counterterm and fix a polarization, or (UDT gate 5) demand the candidate's
own R_wall/R_corner components pair every slot. The jet-slot BOOKKEEPING transforms cleanly
and Route C TC5 is its concrete UDT instance — the typed mismatch (a 2nd-order EH-type
candidate needs 1-jet wall data; a 4th-order C2/Bach-type needs 2-jet wall data plus
3rd-normal-derivative momenta) is precisely the corpus phenomenon that higher-derivative
gravities need deeper boundary data than GHY provides. Two corpus moves do NOT transform:
appending a counterterm (a structure-holding BC — Category-B/gated; on UDT differentiability
must live inside the candidate), and the habit-fixed Dirichlet polarization (on UDT the
varied-vs-held boundary fork BR-B is open and ledgered). Covariant phase space (Lee–Wald
1990; Crnković–Witten 1987; both VERIFIED) survives only on the gate-3 LOCALLY-EXACT branch —
a nonvariational ℛ member has no θ — and its constraints↔symmetries theorem has no seat
without continuous gauge (PROVISIONAL). The corner-symmetry program mostly evaporates: its
content is diffeo-generated, and the UDT wall carries a trivial continuous stabilizer plus
discrete K₄.

### Vein 4 — Noether charges + periods ↔ R9 / gates 4, 6 [PROVISIONAL throughout]

Wald–Iyer (1994, VERIFIED: PRD 50, 846) is anchored, at every step, on a continuous
symmetry parameter ξ: J[ξ] exists by Noether's second theorem, Q by on-shell descent. On the
UDT registered chart there is GENERICALLY no ξ — the continuous stabilizer is trivial on
generic strata and K₄ carries no parameter; per the Stage-2 verifier's refinement the
pointwise Noether identity set is GENERICALLY EMPTY, but on resonance strata (k_mod=0; also
C=0 with λ∓k_mod ∈ {±1}) a continuous class-tangent gauge direction survives and imposes
exact pointwise identities (PROVISIONAL-pending-Stage-2-bank, flagged per the contract). If
that stands, the charge-construction machinery has no seat on generic strata; the surviving
stratum-local, discrete-character-graded identities are not the arbitrary-function ξ the
machine consumes, so no GR-like charge tower is restored — whether they seat anything
charge-like is an open question, not assumed either way. What survives is (a) the WS
current-conservation leg (statements on solutions, not identities — Stage 3's business), and
(b) the bookkeeping discipline. Barnich–Brandt asymptotic charges (VERIFIED-existence) fail
one step earlier: their home (spatial infinity with fall-off classes) does not exist on
finite mirrored cells; only the cohomological TYPING (charge = pairing of a class with a
cycle) transforms, onto the internal cycle census (completion classes, K₄ orbifold strata,
J07 cocycle loops). Chern–Simons level quantization (DJT; Witten 1989; VERIFIED) splits
cleanly along the lane: the MATHEMATICS (holonomy of a cocycle over nontrivial cycles is
classified; quantization = integrality) is exactly gate 6's "vanish or explicitly quantized
with the quantum reported"; the MECHANISM (single-valuedness of e^{iS}) imports a quantum
premise UDT has not derived (postulate-A boundary) and is RED as a rationale. Note the native
work already ahead of the corpus here: the K₄-torsion period vacuity was computed natively
(gate-6 scope note); the live content is the J07 twisted-cocycle holonomy — whose
classification machinery (twisted H¹) is GREEN but MODEL-KNOWLEDGE (flagged, see TG3 item 4).

### Vein 5 — Utiyama-type invariance theorems ↔ F-RA1

Utiyama (1956, VERIFIED: Phys. Rev. 101, 1597) forces a compensating connection by
localizing a continuous parameter: the ∂ε term must cancel. On UDT the ∂ε term never arises —
no arbitrary-function parameter exists to localize (trivial continuous stabilizer; discrete
K₄) — so the forcing step forces NOTHING. The invariance-classification half transforms after
one substitution: invariant → relative-invariant with K₄ characters, i.e. classify
equivariant-response FAMILIES rather than invariant Lagrangians — which is what Stage 2's TB2
did natively (PROVISIONAL). Where the corpus leans on connection-type field content UDT
lacks, the lean is total: there is no UDT slot for a compensating field, and F-RA1's "no
invariant member exists" replaces the corpus's "the invariant Lagrangian is …" as the
theorem-form.

### Veins 6–9 — the charter veins where they touch P4

**Israel junction conditions (VERIFIED: NCimB 44, 1)** — the jet-continuity TYPING across a
codim-1 stratum (what is continuous, what may jump) transforms onto the wall jet census; the
direction of inference does not: Israel derives junction conditions FROM known field
equations, while UDT's wall typing constrains the UNKNOWN response. And the UDT wall is a
MIRROR (φ→−φ identification), not a two-sided interface — jump data are parity-locked, and
the mirror-vs-shift clash with its anchor-absorption resolution (Stage-1 V8) has no corpus
counterpart. **DtN/Calderón (VERIFIED: Calderón 1980; Sylvester–Uhlmann 1987)** — the typing
"a finite region's interior response is completely encoded in a boundary operator pairing
complementary data-halves" maps onto the P3 stratified pairing and the gate-5 question of
which wall jets are free vs determined; the uniqueness machinery (CGO solutions) leans on a
KNOWN linear elliptic law and does not transfer — UDT's unknown is the law itself, one level
up. **Birkhoff rigidity (VERIFIED: Jebsen 1921 / Birkhoff 1923)** — the question shape
"does the field-equation system force extra rigidity on symmetric solutions" is a WS
classification tool for Stage 3+; the conclusion consumes Einstein's vacuum equations and
sits on the banked SCAR site (vacuum = GR), so nothing transfers before ℛ is found.
**Constraint classification (VERIFIED: Fischer–Marsden 1973; Moncrief 1976)** — the
adjoint-kernel/integrability machinery transforms as gate-1 step 3; the corpus's founding
step ("constraints exist automatically, by Bianchi") FAILS on UDT if the Stage-2 vacuity
stands: with no continuous gauge there may be NO forced constraint/evolution split — the
Stage-3 handoff already flags exactly this (overdetermination must be resolved by explicit
integrability, not assumed identities).

### Veins 10–11 — added / explicit

**Fefferman–Graham (VERIFIED; ADDED as a named CONTRAST)** — the expansion-at-conformal-
infinity machinery has NO seat (finite mirrored cells, no infinity); its analog question
("which boundary data parametrize the interior") must be reposed as a mirror/two-point
boundary problem, DtN-flavored. This row exists to stop silent application of any
asymptotic machinery (it also guards the Barnich–Brandt row). **Geon/self-trapping
(VERIFIED: Wheeler 1955)** — thin but honest: the corpus lesson (localized mass-energy
requires FIELD SUPPORT, not a topological label) is consonant with R15's honesty condition;
the analyses consume Einstein equations plus asymptotic mass definitions UDT replaces with
R5's same-solution finite-cell relation.

---

## TG2 — failure-surface analysis: the precise proof-step that breaks, per major vein

1. **Lovelock vein — the replacement/normal-coordinate step.** Lovelock-type proofs begin by
   using full Diff-naturality to pass to normal coordinates at a point: first-jet metric data
   are gauged to zero and second-jet dependence is reduced to curvature. That step needs a
   continuous gauge group acting transitively on the relevant jet data. On the UDT domain the
   chart is REGISTERED (positive triangular), the continuous stabilizer is trivial on generic
   strata (transport only, no pointwise constraint generically; on resonance strata a
   class-tangent direction survives — PROVISIONAL), and the residual gauge is the discrete K₄:
   first-order chart data CANNOT be gauged away, and no curvature-reduction of the jet
   dependence is forced. Second break, same vein: the divergence-free hypothesis is an INPUT
   Lovelock takes from the Bianchi identity; UDT's counterpart (forced off-shell identities)
   is GENERICALLY empty per the Stage-2 refinement — exact identities survive only
   stratum-locally, on resonance strata (k_mod=0; C=0 with λ∓k_mod ∈ {±1}) (PROVISIONAL) — so
   the single strongest constraint in the corpus proof has no GENERIC UDT analog, and with it
   goes the uniqueness pressure off those strata. Third: the second-derivative
   bound is an assumption in the corpus and a graded SLOT in the UDT object (§2.2).

2. **Inverse-variational vein — the fixed-duality step.** Every corpus statement of the
   Helmholtz conditions silently commits the dual pairing (fibred duality + volume form)
   before writing "self-adjoint." On the typed domain that commitment is exactly the open
   L7 datum (P1/P2/P3 enumerated, none adopted; volume choices provably load-bearing per
   Route B T4). The proof does not break — it becomes RELATIVE: each Helmholtz verdict is
   conditioned on a declared pairing. Douglas's classification breaks earlier and harder: the
   case split runs on the eigenstructure of a finite-dimensional endomorphism that exists
   only for SODE systems; no analog exists for a jet-graded component family with moduli
   directions, boundary strata, and a character rule (the corpus itself stops at n=2 ODE +
   scattered PDE results).

3. **Boundary/corner vein — the append-a-counterterm step and the polarization step.** The
   corpus proof of differentiability APPENDS structure (K√h; Hayward angles) and FIXES a
   polarization (Dirichlet) — two supplied choices made by habit. On UDT the first is
   Category-B (a structure-holding boundary term is a physics change unless it emerges as a
   component of the candidate response), and the second is the open BR-B fork. The surviving
   core — enumerate unpaired wall/corner jets per declared order and demand pairing — is
   pure bookkeeping and transforms whole (gate 5 steps 1–2, with TC5 as the typed instance).
   The additional UDT structure with no corpus counterpart: mirror parity + sector split
   (wall data parity-locked) and the anchored-φ rule (wall components may use absolute φ only
   through supplied-structure slots — the V8 clash resolution).

4. **Noether/charge vein — the Noether-second-theorem step.** J[ξ] exists in the corpus
   because a local symmetry with an arbitrary-function parameter exists; every downstream
   object (θ contraction, dQ descent, first law, asymptotic charge) inherits that seat. On
   UDT the seat is GENERICALLY empty (trivial continuous stabilizer on generic strata;
   parameter-free K₄); on resonance strata (k_mod=0; C=0 with λ∓k_mod ∈ {±1}) a continuous
   class-tangent direction survives and imposes exact pointwise identities — e.g. on k_mod=0:
   −2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01 = 0 — PROVISIONAL. So the charge tower
   fails at its first line on generic strata; the stratum-local identity is
   discrete-character-graded, not an arbitrary-function parameter, so no Noether-II tower is
   restored there either — but the categorical "no seat at all" is retired. What survives is
   pairing-with-cycles (period/holonomy control), where UDT's native work is already ahead on
   the torsion part.

5. **Utiyama vein — the ∂ε-cancellation step.** The forcing theorem's engine is the
   appearance of a ∂ε term when a continuous parameter is localized. No continuous parameter
   ⟹ no ∂ε term ⟹ no forced compensating field. The classification half survives after
   invariant → character-relative substitution (executed natively in TB2 — PROVISIONAL).

6. **Junction/DtN/constraint veins — the known-law step.** All three corpus machines consume
   a KNOWN field equation (Einstein's) at their first move: Israel differentiates it
   distributionally; Calderón inverts a known elliptic operator's boundary data;
   constraint classification splits it along its gauge identities. UDT's law is the unknown.
   In each case the surviving transform is the TYPING (which data live on which stratum;
   which boundary data are complementary; compute the compatibility complex explicitly), and
   the breaking step is any use of the conclusion-side formulas.

---

## TG3 — the Stage-3 shortlist (machines for the WS/GC gates on ℛ_PW)

Prioritized by GATE-RELEVANCE and TRANSFORMABILITY ONLY (F-G4 — no expected-physics ranking).
Each entry: machine → gate → what must transform FIRST → the soundness check owed. All are
Category-A techniques under the lane clause; each carries the duty to be applied to the UDT
equations, never to have GR's swapped in.

1. **Variational-bicomplex Helmholtz/source-form machinery (Takens/Anderson school) → gate 3.**
   Transform first: rewrite the self-adjointness condition RELATIVE to a declared pairing
   (P1/P2/P3) on the typed domain — including moduli directions and the K₄ quotient — so the
   test is computable per candidate declaration D1–D3. Soundness owed: the transformed
   condition must (a) reduce to the classical Helmholtz conditions in the fibred-manifold
   special case, and (b) correctly stamp known test forms (e.g. the exact ω = ½d(k10²)
   LOCALLY-EXACT). Attribution: VERIFIED.

2. **GHY/Hayward-style jet-slot bookkeeping (enumeration only, never the counterterms) →
   gate 5.** Transform first: derive the wall/corner jet-slot census on the MIRRORED cell —
   parity + sector split + anchored-φ-through-supplied-slots — as a function of the
   candidate's declared order N (replacing the example-typed TC5 depths with derived ones,
   as the Stage-3 handoff already requires). Soundness owed: the transformed bookkeeping must
   reproduce the TC5 typed instance (2nd-order → 1-jet wall; 4th-order → 2-jet wall +
   3rd-normal-derivative momenta) as its special case. Attribution: VERIFIED.

3. **Adjoint-kernel / explicit-integrability analysis (Fischer–Marsden/Moncrief-style) →
   gate 1.** Transform first: compute the compatibility complex of the candidate system
   {R_i = 0} NATIVELY, with NO assumed Bianchi-type identities — the gate-4 identity input is
   the derived R7(b) vacuity [PROVISIONAL-pending-Stage-2-bank: if the Stage-2 verifier
   amends the vacuity, this machine's starting point changes]. Soundness owed: the computed
   identity count must be cross-checked against gate 4's derived identity set on the same
   candidate, and the method verified on a worked example with known compatibility structure.
   Attribution: VERIFIED (Fischer–Marsden 1973; Moncrief 1976).

4. **Twisted-cocycle holonomy classification (the mathematical core shared by CS-level
   integrality and monodromy theory) → gate 6.** Transform first: state the holonomy
   classification problem for the banked two-sided law L(γ₂∘γ₁) = Q(γ₂)L(γ₁) + L(γ₂)ρ(γ₁)
   with DEPTH-DEPENDENT coefficients (a groupoid over φ, not a fixed group — the corpus H¹
   must be re-derived there), over the cycle census (completion classes, non-torsion cycles,
   J07/J11 loops). Soundness owed: the native K₄-torsion vacuity result must fall out as the
   special case. **FLAG (F-G3): the twisted-H¹ machinery row is MODEL-KNOWLEDGE — a source
   check is owed before this item is used load-bearing.** The quantization MECHANISM
   (e^{iS} single-valuedness) is RED and excluded; only the classification math is
   shortlisted.

5. **DtN/Calderón boundary-response typing → gate 5 + R3.** Transform first: pose the
   wall-data-independence question (which wall jets are free, which determined) for the P3
   stratified pairing under mirror parity — typing only; no uniqueness theorem transfers
   (unknown, nonlinear law). Soundness owed: exhibit the parity-halving of boundary data on
   a toy elliptic example before trusting the census on ℛ_PW members. Attribution: VERIFIED.

Not shortlisted, with reason: Wald-charge machinery (no seat without continuous gauge —
PROVISIONAL, revisit after Stage-2 bank); corner-symmetry program (content evaporates on
discrete residual); Corvino-type gluing (needs a candidate operator's symbol first);
Douglas's case split (irreducibly ODE); all asymptotic machinery (no infinity — FG contrast
row).

---

## TG4 — the departure-point register (PONDER observations, not leads)

The exact argument-steps where GR-side uniqueness/classification FAILS on the UDT domain —
each a candidate birthplace of native structure GR does not have. Recorded for pondering
with Charles; nothing here is a drill target.

- **D1 (Lovelock seat).** The normal-coordinate jet-reduction and the div-free input both
  fail (registered chart + discrete K₄; generically vacuous identity set — stratum-local
  exceptions, see TG2 #1 [PROVISIONAL]). Where GR's
  classification collapses to a POINT (Einstein tensor), UDT's collapses only to a MODULE
  FAMILY (ℛ_PW: dims 10/13/16 per grade × module ranks 1/5/4/4). The residual freedom GR
  does not have is structured (character modules, syzygies, fixed strata) — that structure
  itself is native and unclassified by any corpus theorem.
- **D2 (Noether-II seat) [PROVISIONAL-pending-Stage-2-bank].** With no continuous gauge on
  generic strata, no constraint/evolution split is forced there: the candidate system
  {R_i = 0} can be fully DETERMINED — GENERICALLY. On resonance strata (k_mod=0; also C=0
  with λ∓k_mod ∈ {±1}) the surviving exact Noether identities reintroduce a constraint seat
  (stratum-local and discrete-character-graded, not a Bianchi-type tower) — PROVISIONAL. The
  generic regime remains one the GR corpus never occupies (its systems are always
  underdetermined by diffeo gauge), and the stratum-graded alternation between determined
  and constrained regimes is itself corpus-less. Whatever integrability structure gate 1
  finds will be UDT-native, not Bianchi-inherited.
- **D3 (Utiyama seat) [PROVISIONAL-pending-Stage-2-bank].** The corpus's compensating-field
  forcing step never fires; the
  local-invariance pressure lands entirely on CHARACTER MATCHING. The seat where GR-side
  gauge bosons are born is occupied, on UDT, by the K₄ character rule — a discrete,
  parameter-free forcing with no corpus analog.
- **D4 (GHY seat).** "Append a counterterm to rescue Dirichlet data" is unavailable
  (Category-B) and the polarization is an open fork: differentiability on the mirrored cell
  must be achieved INSIDE the candidate (R_wall/R_corner slot pairing) under parity + the
  anchored-φ rule. A candidate that achieves it carries native boundary structure with no
  GHY counterpart.
- **D5 (asymptotic seat).** FG expansions, BBC charges, ADM-type mass — the entire
  at-infinity toolbox has no seat. Mass/charge concepts must be reborn as R5's
  same-solution finite-cell relation and gate-6 period reports — a genuinely different
  birthplace for "mass" than anywhere in the corpus.
- **D6 (multiplier seat).** The corpus fixes the pairing implicitly and nowhere treats it
  as a variable; on UDT variationality is pairing-RELATIVE (L7 open; T4 blindness loci).
  The dependence of the gate-3 verdict on the declared pairing is itself a native structure
  axis no corpus theorem addresses.
- **D7 (junction seat).** Israel's inference direction inverts: wall typing constrains the
  unknown law rather than following from a known one, and the mirror wall (parity-locked,
  anchor-absorbing) is a boundary species the two-sided corpus formalism does not contain.

---

## Attribution tally and falsifier record

- **Rows: 26, a true row partition (amendment A3): VERIFIED: 17 + VERIFIED-existence: 3 +
  MODEL-KNOWLEDGE: 6 = 26.** The 3 VERIFIED-existence rows (work's existence/title confirmed;
  exact journal citation not individually checked): the arXiv:0910.2933 inverse-problem row,
  the corner-proposal row, the Barnich–Brandt row. The 6 MODEL-KNOWLEDGE rows: classical
  invariant theory; Aldersley/jet-group naturality; twisted-H¹ machinery [flagged — TG3
  item 4]; invariant-Lagrangian theorem-family; Corvino gluing; tetrad-GR. (The Hayward row
  counts VERIFIED, carrying its exact-citation caveat in the row.)
  **Sub-row attributions (statements INSIDE rows — listed separately, not counted in the row
  partition):** (i) the arXiv:0910.2933 SCOPE statement is MODEL-KNOWLEDGE inside its
  VERIFIED-existence row; (ii) the Z₂-brane cousin note is MODEL-KNOWLEDGE inside the
  VERIFIED Israel row (not load-bearing). All web checks run 2026-07-29 via WebSearch.
- **F-G1:** no adoption recommended anywhere; every conclusion-side formula is RED-stamped
  in the map.
- **F-G2:** every row's disanalogy column is filled; no "is" claims.
- **F-G3:** one shortlist item (TG3 #4) leans partly on a MODEL-KNOWLEDGE row and carries
  the required flag in place; no other MODEL-KNOWLEDGE row underpins the shortlist.
- **F-G4:** shortlist ordering is by gate-relevance (gates 3, 5, 1, 6, 5/R3) and
  transformability; no expected-physics criterion used.
- **Ceiling respected:** the strongest statement made anywhere is of the pre-committed form
  "corpus result X was proved by machinery Y, which transforms up to step Z where it breaks
  on structure W." Nothing about what UDT's equations ARE; no candidate favored; no gate
  pre-judged.

---

## STAMP RESOLUTION (driver, 2026-07-29 — Stage 2 BANKED)

Route A Stage 2 is banked at grok 2c0e7cc (VERIFIED-WITH-AMENDMENT, two closure rounds). Every
`[PROVISIONAL-pending-Stage-2-bank]` stamp in this document is hereby RESOLVED to the banked
statement, which matches the refined form carried above with ONE further deepening from the
second closure round: the resonance rank-drop locus λ∓k_mod ∈ {±1} carries, beyond the four
named C = 0 strata (identities auto-satisfied), higher-codimension **C ≠ 0 sub-varieties whose
identities ARE further genuine cuts** (derived example: the shear-slot identity
−c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0}); k_mod = 0 remains the only
CODIMENSION-1 cut (Gröbner-exhaustive), and the full deeper stratification is
TYPED-NOT-EXHAUSTED. Consequences for this map: the generic-stratum qualifications above stand
unchanged; D2's "stratum-graded alternation between determined and constrained regimes" is
STRENGTHENED (the alternation has depth — a graded tower of stratum cuts, still corpus-less);
the gate-1/Fischer–Marsden shortlist item and the Wald-exclusion reasoning survive unchanged.
Standing condition inherited from the bank: any Stage-3 candidate CONTACTING the resonance
locus requires the queued deeper-census tile before adjudication.
