# P4 period gate — exact derivation record (TP-1..TP-6)

Date: 2026-07-30. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
run). Script: `derive_period_gate.py` — **28/28 checks, exit 0 = 22 SUBSTANTIVE
zero-residual exact-SymPy checks + 6 GUARDS** (guards = citation/typing/table rows,
labeled `[guard]` in-script and in the JSON), deterministic (no floats, no
randomness, no numeric solvers, no GPU; stdout byte-identical across reruns —
verified ×3), single CPU process, ~1 min wall (**FULL DECLARED SCOPE — no
scope-ladder reduction taken**: all four postures, all four candidate families, the
enumerated pairing branches carried symbolically). Outputs:
`period_gate_results.json`, `DERIVATION_STDOUT.txt`, `PERIOD_LEDGER.tsv` (20 rows),
`DECISION_SURFACE_UPDATE.md`. Every check named in `monospace` below is one of
the 28. **Status: VERIFIED-WITH-AMENDMENT — blind adversarial pass returned
PASS-WITH-REQUIRED-AMENDMENTS (two bookkeeping amendments, no substantive claim
touched; `VERIFIER_REPORT.md` + `VERIFIER_INDEPENDENT_CHECK.py`, 14 groups, exit 0;
same-session-spawned verifier, caveat travels), amendments applied
(`CORRECTION_LAYER.md`, `AUDIT_REPORT.md`); post-amendment rerun 28/28, exit 0,
byte-identical; nothing adopted** (the §4 ceiling of the contract honored).

**Honesty note (one solver-path defect found during the run, cured):** SymPy's
`solveset(exp(I*t)-1, t, Reals)` returns the INCOMPLETE set {0} (missing the 2πZ
lattice); the C3c contrast certificate was recoded as direct exact evaluation
(e^{2πi} = 1 with 2π ≠ 0; e^{πi} = −1). The check's claim is unchanged; the
certificate route was replaced. No check condition was weakened (three checks were
HARDENED pre-bank: a vacuous disjunct in C3c, a weak disjunction in C5a, a soft
`ask` in C2c — all replaced with exact solveset/nonnegativity conditions). Note
[AM-2]: the three pre-bank hardenings are not git-diffable — no earlier draft was
ever committed (only the final script exists) — and the verifier audited the FINAL
forms and certified them as the strong versions claimed (no soft `ask`, no vacuous
disjunct anywhere in the final script).

**FULL STAMPS (F-P3, travel with every claim):**
- **arena:** the registered stationary one-parameter presentation (fields
  (φ, f, bh), jets ≤ 2), registered positive triangular chart, cell x ∈ [−ℓ, ℓ];
  the W-1D seam arena's jump laws enter as SUPPLIED seam data (arena-transfer
  premise stamped in C2b); the toric R×S³ arena enters only through its banked cap
  cycle census (S0c).
- **census branches:** constants-census (BASE, INTEGRATED rows) and fields-census
  (BR-M, gradient-seat lock class) both carried; **none adopted.**
- **pairing branches:** P1-4D (a_F = 2λ), P1-triad (a_F = 1+2λ), P2 (a_F = 0)
  carried with a_F SYMBOLIC; a_F ≠ 0 conditions stated where used; **none adopted.**
- **completion branch (L4, both ways):** the completion-class axis enters as
  {ACYCLIC completions (crease-/open-terminated chains): no non-torsion cycle} vs
  {CYCLIC completions (periodic identification): one Z cycle} — which FC family
  realizes which is completion DATA (the banked NEEDS-COMPLETION-DATA stamp
  travels); the vary-within-one vs vary-over-class fork: the discrete 𝔠 label
  contributes no continuous cycles (typed).
- **posture:** quotient / two-sided (partner and glue+B) / open-end — the banked
  seam menu, interrogated, **none adopted** (F-P4).
- **families:** (i) constants-census massive locus {I_p = 0, E0 > 0}; (ii)
  fields-census lock-emergence massive class (P1-4D landing); (iii) massless strata
  (P2-side, triad-locked, pointwise survivors); (iv) wall germ data — **all four
  enumerated, none dropped.**
- **parity:** ε_φ = −1 DEFINITIONAL (CANON layer 3) — used in C6a's crease jets.
- **quadratic class:** the fiberwise-quadratic p-unmixed LE class (banked Slice-2b
  definition); every atlas-riding claim carries this stamp.

---

## TP-1 — the cycle census (`C1d`, per posture × completion branch)

R9's live content (wall-gate certification, re-derived here in census form):

| cycle class | torsion? | R9 status | provenance |
|---|---|---|---|
| K₄-orbifold classes | order 2 | VACUOUS for closed real forms (nP = 0 ⇒ P = 0) | banked proof CITED; arithmetic re-instantiated `S0b` |
| toric cap / closer classes | order \|det\| — **banked enumeration: all 104 two-cap pairs have \|det\| = 1 ⇒ π₁ trivial** | VACUOUS (no live 1-cycle from the 3D/4D arena at all; the \|det\| = n > 1 lens class would still be torsion Z_n ⇒ vacuous) | `S0c` on the banked `TORIC_CAP_ENUMERATION.tsv`; exotic non-Hopf-preserving families = the banked open boundary, typed |
| quotient-posture completion cycle γ_T (the D∞ translation) | **non-torsion** | LIVE — but every period IDENTICALLY VANISHES (below) | `C1a–C1c` |
| two-sided CYCLIC completion cycle (Z translation) | non-torsion | **LIVE — carries the real period conditions of TP-2** | `C2*`; L4 cyclic branch |
| two-sided ACYCLIC chains (crease-/open-terminated) | no cycle | VACUOUS | typing `C1d` |
| J11 chart-transition loops | groupoid loops | **LIVE — twisted-cocycle holonomy** (conditional on a multi-chart completion possessing a loop: completion data) | banked Route B T3/E08; `C3*` |
| open-end posture, cycles through the endpoint | none exist | VACUOUS | typing |

**The quotient-posture theorem (new, exact — `C1a`,`C1b`,`C1c`):** the mirrored
cell's orbifold fundamental group is the infinite dihedral group D∞ = ⟨r₋, r₊⟩
(affine reps computed: r±² = id, γ_T = r₊r₋ = translation by 4ℓ, non-torsion), and
**r₋ γ_T r₋⁻¹ = γ_T⁻¹ exactly** (conjugacy reversal, zero residual). A period map
of a closed one-form is a homomorphism h: D∞ → (R, +); the torsion generators force
h(r±) = 0 (2h = 0 over R), and generation forces h ≡ 0 — **Hom(D∞, R) = 0: EVERY
period of EVERY closed one-form vanishes identically on the quotient posture.**
Corroborated by explicit integration: the γ_T period of the equivariant
mirror-double extension of an arbitrary degree-5 cell profile is 0 with all six
coefficients free (`C1c`). So on the quotient posture R9's exact subcase is
**IDENTICALLY SATISFIED — it imposes nothing on any candidate family there.**

## TP-2 — the derived period conditions (live cycles × families)

### The cyclic-completion momentum period (`C2a`,`C2b`)

On the banked quadratic-class atlas (w = Ax² + w1x + w0, A = a_F²E0/(2g_p),
π_p = g_p w′/a_F), the per-cell increment of the momentum is exactly

    Δπ_p(cell i) = a_F · E0_i · L_i        (g_p cancels — heterogeneous members allowed)

so the period of dπ_p around the completion cycle, with seam jumps J_s supplied by
the germ data, is (N = 1, 2, 3 explicit; general N = finite telescoping,
Category-A):

    ∮ dπ_p = a_F Σ_i E0_i L_i + Σ_s J_s = 0.

On **flux-sealed / partner seams** (the banked glue pin 𝔅_Q = 0 ⟺ flux seal,
CITED) the seam sources vanish and the condition is exactly

    **Σ_i E0_i L_i = 0**   (a_F ≠ 0; the LIVE R9 condition on cyclic completions).

### Its mass-branch reading (`C2e`)

Δπ_p(cell i) = **M-WALL_i = a_F·M-GEN_i** exactly (banked identities recomputed):
the cyclic period condition READS **Σ M-WALL_i = 0 ⟺ Σ M-GEN_i = 0** (common
a_F ≠ 0; M-DENS-proper ≡ M-GEN by the banked calibration) — the labeled total
chain mass vanishes. Branch labels carried; no branch promoted.

### The field periods (single-valuedness of f, h)

∮df = Σ_i (G_i⁻¹c)_f J_i = 0 and likewise for h, with c COMMON across the chain
(momentum continuity [π_f] = 0, π_f = c_f per cell) and J_i = ∫ dx/w_i > 0
(banked positivity). Instances computed: N = 1 (`C2d`), the lock-class affine
instance (`C6c`), the massless strata (`C6d`).

### The whole-completion integrated tie (`C2f`)

W_F·L̃ = E0 on-shell (zero residual) ⇒ the completion-level INTEGRATED λ-row is

    a_F′ · Σ_i E0_i · I_p,i = 0

— **the banked per-cell tie 2E0·I_p = 0 is the SINGLE-CELL instance; a multi-cell
whole admits massive members with per-cell I_p ≠ 0 balanced across cells.** (Map
fact; INTEGRATED/BASE branch, λ a single whole-level constant, a_F′ ≠ 0 branches.)

### The J11 loop holonomy (`C3a–C3d`; the nonvariational form of gate 6)

The banked E08 cocycle and the two-sided twisted law
L(γ₂∘γ₁) = Q(γ₂)L(γ₁) + L(γ₂)ρ(γ₁) are recomputed (associativity zero residual,
diagonal-K subfamily). Around a loop the holonomy is **REAL-LINEAR/AFFINE in the
segment data** with real invertible coefficient matrices: the trivial-holonomy
locus is a codim-1 real hyperplane, the obstruction value ranges over all of R (a
real matrix space for the L-block law) — **"trivial or classified" = one real
(matrix) value; there is no discrete structure.** This also discharges the
nonvariational-closure form: the holonomy of the closure data is CLASSIFIED by a
real continuum invariant. (F-S7 twisted-H¹ flag inherited on any full
classification claim; the computations here are the banked laws only.)

## TP-3 (Q-A) — posture selection: **NO SELECTION** (`C4a`,`C4b`)

No period condition is violated-in-one-posture/satisfiable-in-another on matched
configurations in the eliminating sense: quotient — identically satisfied (any
configuration); cyclic two-sided — real conditions, satisfiable (the constant
stratum satisfies all of them exactly, witnessed); open/acyclic — vacuous. **No
posture is emptied and none is forced.** R9's per-posture STRENGTH differs
(identically-satisfied / one real condition per cycle / vacuous) — a typing
DISTINCTION, recorded as such, not a selection. The comfortable outcome (T2) did
not land.

## TP-4 (Q-B) — quantization: **NO — with the exact reason per condition** (`C5a`,`C5b`)

**No integer/discrete structure is forced on E0, ℓ, the germs, or the moduli.**
Per condition:

- Σ E0_i L_i = 0 — a real hyperplane (solved; continuum).
- No condition constrains ℓ alone: ℓ enters only through E0·L products; at E0 ≠ 0
  the N = 1 condition has NO positive-L solution (solveset = ∅) — it forces
  E0 = 0, never a discrete length.
- The moduli (k_mod, k10, C) are ABSENT from every derived condition (computed).
- J11 holonomy — real hyperplane / real matrix value (C3).
- Torsion classes — identically satisfied (nothing to quantize).

**The structural reason (the located absence, `C3c`):** every banked holonomy
target is REAL — K₄ characters ±1, anchored weights e^{a_F p0} ∈ R₊, E08/T3
twists e^{φK}, e^{φH} — and e^t = 1 over R has the UNIQUE solution t = 0 (point
kernel, no lattice). The 2πZ lattice exists only for an imaginary/circle-valued
exponent (e^{2πi} = 1 exactly, certified as the contrast) — **and no
circle-valued or imaginary holonomy target exists anywhere in the banked census**
(fields real; f is the real connection moment, not an angle — so the atan
quadrature multivaluedness never engages). The "explicitly quantized" disjunct of
R9 CANNOT ENGAGE on the banked cycle content. F-P2 discharged in both directions:
no quantization mechanism imported, and the absence is DERIVED, not assumed. The
only integers anywhere in the cycle content are the torsion ORDERS (K₄ order 2;
cap |det|) — domain data whose period conditions are vacuous; they cut no family
parameter.

## TP-5 (Q-C) — the sector-compatibility map (`C6a–C6g`; typing facts ONLY — F-P7)

| pair | verdict | exact content |
|---|---|---|
| crease \| crease (mirrored cell) | **PERMITTED** | banked mirrored-cell canon; R9 identically satisfied (TP-1) |
| crease \| two-sided glue (mixed-posture chain) | **PERMITTED-CONDITIONAL** | crease-end conditions on the quadratic class DERIVED from the banked mirror-jet kill (ε_φ = −1): **w(−ℓ) = 1 AND 2A·w(−ℓ) = w′(−ℓ)²**; massive witness w = x²/2 + 1/2 exact (`C6a`); **family (i) {I_p = 0, E0 > 0} is REALIZABLE with a crease at one end** (`C6b`, below) |
| two-sided cyclic, all-definite members | **FORBIDDEN for massive members** | Σ E0_i L_i = 0 + E0_i ≥ 0 (exact SOS) ⇒ every E0_i = 0 (`C2c`): an all-definite chain on a cyclic completion is ENTIRELY MASSLESS; the massive escape REQUIRES an indefinite member somewhere (full mixed-witness existence: CONDITIONAL — the remaining field-period balance is a derived real condition, not certified nonempty here) |
| two-sided cyclic, 1 cell | **FORBIDDEN for nonconstant members** | single-valuedness forces w1 = 0, E0 = 0, then c = 0 (definite class): CONSTANTS ONLY (`C2d`); the massive locus {I_p=0, E0>0} is EMPTY there |
| open-end terminator + any chain | **PERMITTED** | no cycle; germs freed; the q-datum stays a wall-response output (banked) |
| cross-census / cross-pairing cells in one whole | **CONDITIONAL** | at any seam locus at the seal value p0 = 0, W_F = e^{a_F·0} = 1 for EVERY enumerated branch (a_F symbolic, `C6f`) — cross-pairing joins are weight-consistent there (the banked TW3 weight-drop, seam-locus instance); off-seal seams need the (c_E/Q_w)^{a_F} factor matched; the J07 transition-data obligation is inherited (F-S7 travels) |

**The crease-compatible massive witness (`C6b`, the computation of the push):** on
the crease-pinned one-parameter branch (ℓ = 1) w1 = 2A − √(2A), w0 = 1 + A − √(2A):
disc(w) = −2A < 0 for ALL A > 0 (nodeless, regular); I_p(A = 1/2)·a_F = **π − 4 < 0
exactly** (Dalzell integral: 22/7 − π equals a nonnegative-integrand integral —
recomputed; and this value is exactly the banked Slice-2b `ADOPTED_Ip_signchange`
c = 1 endpoint, an unplanned consistency contact); I_p(A = 9/2)·a_F ≥
(2/3)·log(5/2) > 0 by exact piecewise bounds (vertex w(−2/3) = 1/2, root
factorization w − 1 = (3/2)(3x+1)(x+1), monotone tail w ≥ 5 on [1/3, 1] — all
zero-residual); continuity of A ↦ I_p (Category-A) gives a root A* ∈ (1/2, 9/2)
with E0 = 2A*g_p/a_F² > 0. **The constants-census massive family (i) is realizable
with a quotient crease at one end and a two-sided seam at the other** —
the owner's "different candidates as different sectors of one whole" is hereby
CHARACTERIZED as a computed typing fact (a massive cell can sit in a
mixed-posture whole); it is NOT adopted and resolves no fork (F-P7).

## TP-6 — candidate-family statuses (every family; none dropped)

| family | quotient posture | two-sided CYCLIC completion | open / acyclic chains |
|---|---|---|---|
| (i) constants-census massive {I_p=0, E0>0} | **UNTOUCHED** (all periods identically vanish); crease-compatibility conditions derived + massive witness exists (`C6a/C6b`) | **CUT on all-definite chains (forced massless); EMPTY at N = 1; CONDITIONAL with indefinite partners** — and the tie relaxes to Σ E0_i I_p,i = 0 (per-cell I_p = 0 is the single-cell instance) | **UNTOUCHED** (no cycle) |
| (ii) fields-census lock-emergence massive (P1-4D landing) | already excluded upstream by the banked parity collapse (CITED, not re-adjudicated) | **CUT (forced massless: ∮df = f1·L = 0 ⇒ slopes = 0 ⇒ E0 = 0)** (`C6c`) | **UNTOUCHED** (its banked conditionalities travel unchanged) |
| (iii) massless strata (P2-side, triad-locked, pointwise survivors) | SATISFY identically | SATISFY identically (constants); nonconstant affine members reduce to constants | UNTOUCHED |
| (iv) wall germ data | crease germ forced trivial upstream (banked) | banked glue germs pinned upstream; the flux-seal pin 𝔅_Q = 0 is EXACTLY the no-seam-source form of the period law (consistency); active germs enter as supplied jumps J_s | **FREED/UNTOUCHED** (no cycle reaches a free endpoint) |

## Outcome and falsifier record (derivation-side)

**Outcome class: MIXTURE — OQ3 (the sector-compatibility map computed, with one
FORBIDDEN row and exact conditional rows) + OQ4 on Q-B (the periods impose no
integer structure — with the derived structural reason) + Q-A NO-SELECTION (typing
distinction only). The TP-2 derived REAL period conditions (Σ E0_iL_i = 0 ⟺ the
labeled total chain mass vanishes; the field periods; the whole-completion tie)
are first-class content.**

- **F-P1 (multi-directional steering):** the landed outcome contains the
  owner-pleasing sector leg (a massive cell CAN sit in a mixed-posture whole) and
  the quantization silence. Both directions attacked in-text: the sector leg is a
  CONDITIONAL typing fact with its witness's nonconstructive step named (IVT root,
  Category-A) and its ℓ = 1 normalization tagged CHOSE; the silence is not
  bare — the exact reason (real holonomy targets, point kernels) is derived and
  the one place integers DO live (torsion orders) is named and shown to cut
  nothing. The verifier should attack `C6b` (the sector-witness leg) and `C5a/C3c`
  (the silence leg) hardest.
- **F-P2 (invented quantization): not fired** — no integer condition exists to
  audit; the located-absence certificate uses e^{2πi} = 1 only as a CONTRAST
  (explicitly outside the banked census).
- **F-P3 (stamps):** every claim carries posture / census / pairing / completion
  branch / cycle / family / jet-layer / arena stamps (see the standing block and
  per-check details).
- **F-P4 (assumption smuggle): not fired** — no posture/census/pairing/G18/
  completion class adopted; all conditions carried per-branch symbolically.
- **F-P5 (bank contradiction): none found** — the banked per-cell tie, mass-branch
  identities, flux-seal equivalence, cap enumeration, cocycle laws, and the
  Slice-2b I_p(c=1) = π − 4 endpoint are all reproduced zero-residual or cited;
  the whole-completion tie REFINES (does not contradict) the per-cell tie: the
  banked form is the single-cell instance.
- **F-P6 (symbolic failure): none in the banked run** — 28/28, exit 0,
  byte-identical ×3; one SymPy solver-path defect (incomplete `solveset` on
  `exp(I*t)−1`) found and routed around, recorded in the honesty note.
- **F-P7 (sector-frame discipline):** the sectors reading appears ONLY as the
  computed rows of the Q-C table; no fork is resolved by it; the owner's statement
  is recorded as DIRECTION in the contract.

**Limits that travel:** (i) all atlas-riding conditions are QUADRATIC-CLASS scoped
(beyond it, the TP-2 content is the momentum-period FORM ∮dπ_p = Σ jumps and the
single-valuedness conditions, member-general but not closed-form); (ii) jet ≤ 2,
stationary presentation, enumerated pairing branches, READY bin; (iii) the seam
jump laws are the W-1D arena's, entering the W-REG chain computation as SUPPLIED
data (arena-transfer premise, stamped); (iv) J11 rows are conditional on a
completion whose chart graph HAS a loop (completion data; F-S7 flag on any full
twisted-H¹ classification); (v) the mixed-sign cyclic witness is certified only at
the w-sector level — the full-member field-period balance Σ(G_i⁻¹c)J_i = 0 is
derived but its nonemptiness is NOT certified (typed open); (vi) `C6b` rides two
named Category-A steps (IVT root existence; log-monotonicity bounds) exactly as
the banked A2/sign-change precedent; (vii) the D∞ theorem is for CLOSED REAL
one-forms (the R9 exact subcase); twisted/equivariant coefficients would need
their own computation (typed); (viii) exotic non-Hopf-preserving higher-isometry
families remain the banked open boundary.
