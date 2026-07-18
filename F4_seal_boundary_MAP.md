# F4 — UDT's Finite-Cell / SEAL / Boundary Structure (MAP)

**Mode:** MAP (no compute, no fit, DATA-BLIND, METRIC-LED, OBSERVE-not-target).
A make-visible/planning doc for Charles's steer. NOT canon. NO solves run.
**Created:** 2026-06-21, as the F4 item of the FOUNDATIONAL-ASSUMPTIONS AUDIT.
**Author:** Claude Opus 4.8 (1M).

---

## 0. WHY F4 IS NOW THE FRONTIER (the load-bearing caveat, in lay terms)

This session's central headline — "the classical metric box-controls (no intrinsic
discreteness) ⇒ we must quantize" — was established by treating the cell's outer
boundary as an **arbitrary box**: scan the box radius R, watch the lowest level fall
like ω ~ 1/R, and call it a "box-control artifact." That is a legitimate diagnostic
**for a generic box**. But UDT's canon (C-2026-06-10-2) says the cell is **physical**
(no spatial infinity) and the boundary is a **specific structure** — a mirror-fold
"seal," read as a time-reversal involution. **That actual physical seal BC was never
imposed in any box-control / discreteness solve.** (Confirmed below: all four solves
used a plain Dirichlet wall whose radius was scanned.)

Two ways the physical seal could CHANGE the box-control verdict:
1. A **physical** finite cell makes box-modes physical: ω_n ~ n/R_cell becomes a
   GENUINE discrete spectrum, not an artifact to be scaled away.
2. A **non-trivial seal BC** (a time-reversal involution junction, not a simple
   Dirichlet wall) could give a **non-harmonic** spectrum (not 1:2:3…).

So F4 sits directly UNDER the "must-quantize" verdict and must be mapped before
quantization (F6). **Honest counter-weight, recorded up front (§5):** even a physical
box gives a TRIVIAL harmonic ladder (1:2:3…), which is not the observed mass pattern,
and the cell size is not natively pinned at particle scale (F7). So F4 likely does NOT
fully rescue a classical spectrum — but the non-trivial seal BC is genuinely UNTESTED,
so it **cannot be ruled out** without the map + a test.

---

## 1. F4 STATED WHOLE — the finite-cell / seal / boundary structure

UDT's canon (C-2026-06-10-2, the finite-cell canon) claims the following composite
structure. Each sub-piece is given its own DERIVED-vs-POSITED grade (from F0).

**The claim, whole:** There is no spatial infinity. The universe is a finite cell
([0, r_CMB], φ: 0 → ln(1101) at the CMB boundary). Matter cells are finite inside-out
cells (φ: 0 at the interface → −∞ at the core endpoint), mirrored across φ → −φ. The
outer boundary of a matter cell is not a hard edge but a **SEAL**: a mirror-fold where
the cell is glued onto its own mirror image. The seal is read as a **time-reversal
involution** (t → −t). The matter cell is the **double** of a radial collar I×S²
across this seal. The inner core endpoint (r=0, φ→−∞) is curvature-singular and
removed.

### Sub-piece grades (DERIVED vs POSITED), with F0 provenance

| # | Sub-piece | Grade | F0 tag / provenance |
|---|-----------|-------|---------------------|
| (a) | **No spatial infinity / finite domain** ([0, r_CMB]) | **POSITED** | F0 **A1**: a premise-SWAP asserted as "the real UDT universe," NOT derived. "The single deepest frame posit; licenses finite-cell discreteness + the outer Dirichlet + the box-control reinterpretation." [ASSUMED]. Canonized (C-2026-06-10-2) but canonized-as-posited. |
| (b) | **Mirrored cells** (φ → −φ; matter cell = mirror of CMB boundary) | **DERIVED (the mirror/Z2 quotient)** | F0 D1: "The mirror/Z2 quotient is DERIVED." Provenance: w6/w7 same-minus involution σ:(a,b)→(−a,−b), σ²=id (`w7_results.md:48-49`). |
| (c) | **The FOLD (seal ≠ edge)** | **DERIVED + blind-verified** | F0 D1: "the seal FOLD (seal ≠ edge) is DERIVED + blind-verified (exact det g4 ∝ (b−fqa)² identity)." Provenance: `w6_results.md:41-59` (verdict line `:9` "MIRROR FOLD, not an edge"; blind verifier independent cofactor expansion `:44-46`). |
| (d) | **TIME-REVERSAL reading of the fold** (σ = t→−t) | **ROW-CONDITIONAL** (derived only on one slot-choice; a competing involution exists) | F0 D1: "'= time-reversal (t→−t)' is derived only CONDITIONAL on restricting the off-diagonal arm to the W6 same-minus stationary row (a slot-choice, with a competing involution on record)." Provenance: `w7_results.md:52-54`; competing P×T at `fermion_forcing_verifier_results.md:91-92`. **← the premise for Charles's eye, §6.** |
| (e) | **Cell-doubling** (cell = double of collar I×S²) | **CHOSEN** (a topology choice; a competitor exists) | F0 **D2**: "Matter cell = the DOUBLE of a collar I×S²; the H¹=0/H²=ℝ 'one-type × continuous-mass' rigidity rests on this topology choice (an S²×S¹ second-seal doubling would give an integer Chern family instead — parked-unbuilt). [CHOSEN]." Provenance: `h1_types_results.md:28-29`. |
| (f) | **Inner-core removal** (r=0, φ→−∞ excised) | **POSITED** (separate inner BC) | F0 **D3**: "Inner core endpoint (r=0, φ→−∞) is curvature-singular and REMOVED — a separate posited inner boundary (F4 stresses only the outer seal). [ASSUMED]." |
| (g) | **What BC the seal imposes on the fields** | **PARTIALLY DERIVED (a parity dichotomy); the actual junction condition UNCOMPUTED** | Derived dichotomy: σ-EVEN → Neumann, σ-ODD → Dirichlet at the crease (`w7_results.md:57-58`, `wcc_results.md:51-52`). BUT the explicit Israel/same-minus junction condition (the second-fundamental-form matching) was **never computed**: `fermion_forcing_results.md:273-275` "the next computation, not this one." **← this is the core gap, §3-4.** |

**Read of the table:** the FOLD itself (c) is the one theorem-grade pillar. The
mirror quotient (b) is derived. But the CONTAINER that makes box-modes physical —
(a) no spatial infinity, (e) the doubling, (f) the inner cut — is POSITED/CHOSEN, and
the TIME-REVERSAL label (d) is row-conditional with a competitor. The seal's actual
field BC (g) is a derived parity-dichotomy in the abstract, but the concrete junction
condition that would set the spectrum was never written down.

---

## 2. PREMISE LEDGER (chose / derived) — every sub-piece, provenance attached

| Sub-piece | Chose or Derived? | Note |
|-----------|-------------------|------|
| (a) no spatial infinity, domain [0,r_CMB] | **CHOSE** (canonized-but-posited) | F0 A1 — deepest frame posit; in TENSION with N6 (asymptotic flatness pins the vacuum branch). |
| (b) mirrored cells / Z2 quotient | **DERIVED** | w6/w7 same-minus σ. |
| (c) the fold (det g4 ∝ (b−fqa)²; seal ≠ edge) | **DERIVED + blind-verified** | w6. The single strongest result in F4. |
| (d) σ = TIME REVERSAL (t→−t) | **DERIVED *conditional on a CHOSE*** | Derived ON the W6 same-minus stationary row (a*=αf_T, b*=(f_θ/f_r)a*); the row is a slot-choice. Competing involution P×T on record. |
| (e) cell = double of collar I×S² | **CHOSE** | D2; competitor S²×S¹ (integer-Chern family) parked-unbuilt. |
| (f) inner-core removal (r=0) | **CHOSE** (posited inner BC) | D3. |
| (g) seal field BC (parity dichotomy Neumann/Dirichlet) | **DERIVED-in-the-abstract; junction condition UNCOMPUTED** | The actual Israel matching never done; the one junction that WAS computed (`h1_types_results.md:108-110`, σ-EVEN/Neumann/ρ-flat) "glues the datum SYMMETRICALLY with NO normal-derivative constraint that would discretize the value." |

---

## 3. WHAT THE BOX-CONTROL SOLVES ACTUALLY USED — the GAP, made explicit

**KEY FINDING (recon-confirmed): in NONE of the four box-control / discreteness solves
was the physical seal involution imposed. Every solve used a generic Dirichlet /
regular-node wall whose RADIUS was scanned. The ω ~ 1/R scaling is precisely the
fingerprint of that generic Dirichlet box — by construction it could not have revealed
discreteness sourced by the mirror-fold junction, because that junction's coupling was
absent from the imposed BC.**

Exact BCs used (quotes, file:line):

- **archive/pre_2026-07-01/STEP2_timelive_matter_results.md** — Dirichlet wall + R-scan.
  `:96` "ω² m u = −(k u')' + V u, **Dirichlet both ends**"; charge BC
  `:195` "Charge-1 hedgehog Θ(0)=π, **Θ(seal)=0**"; verdict from box-radius scan
  `:117-121` "w_pos_low·R² ~20-31 (roughly constant ⇒ 1/R² BOX MODE)";
  `:123` "the level moves… when the **seal is relocated**" (seal = relocatable wall).

- **P5e_proper_results.md** — Dirichlet charge BC + R-scan; off-diagonal time row H
  PINNED=0 as a gauge mode (a gauge pin, NOT a mirror junction).
  `:162` "Θ(0)=π, **Θ(seal)=0**"; `:160` (Pe-H) H "pinned=0 in the static limit as a
  gauge mode"; `:134-139` "ω DECREASES as the box grows (0.429 → 0.295 as R 10 → 12,
  ~1/R)… intercept fit ω² = a/R² + b… b = −0.134 (≤0)" (box scan over R∈[8,12]).

- **archive/pre_2026-07-01/static_soliton_rerun_derived_operator_results.md** — explicit Dirichlet/regular wall.
  `:170` "P7 | **Seal BC A=B=1, φ=0**; core regularity (zero-gradient) | CHOSE… **A
  continuous BC, not a quantizer.**"; verifier even flags the BC-dependence as untested
  `:225-226` "**Does the seal BC (A=B=1, φ=0)**… pre-select the deficit/hair? Try a
  larger box / different seal."

- **offround_classical_discreteness_results.md** — Dirichlet amplitude pins + R-scan.
  `:36` fluctuation amplitudes "pinned at both ends (regular at core, **sealed at
  wall**)"; verdict `:64-66` "w·R = 77.7→76.8 (constant to 1.2%) across a 2.8x wall
  relocation → BOX-CONTROLLED"; `:64` "||M|| R-INDEPENDENT; ||K|| ~ 1/R²."

Solver-code confirmation (committed .py): `radial_Bfree_soliton.py:154` "Dirichlet
ends Th(core)=m*pi, Th(seal)=0"; `coupled_tl_timelive.py:138-140` "u=0 at both ends";
`p5e_offround_qep.py:154-163` regular fluctuation amplitudes pinned=0 at seal/core.

**The derived-but-UNUSED mirror BC exists in the repo:** `w7_a_mirror_bc.py` (dated
2026-06-13) implements the same-minus fold σ:(g_Tr,g_Tθ)→(−g_Tr,−g_Tθ). **None of the
four solvers import or use it.** (The one "Mirror" hit in solver code, `p5d_timelive.py:124`,
means "replicates," not a physical mirror BC.)

### THE GAP, stated cleanly

| | Box-control solves USED | The PHYSICAL seal WOULD impose |
|---|---|---|
| Outer boundary | Generic Dirichlet wall, value-pinned (Θ(seal)=0, φ=0, A=B=1) | A mirror-fold **junction**: gluing the cell to its own mirror across the D=0 crease |
| Treatment | Wall radius R is **scanned** (and the scan IS the verdict) | A **fixed physical** cell radius (whatever the canon sets it at) |
| Field condition | One Dirichlet condition (value=0) on every field | **Parity dichotomy**: σ-EVEN → Neumann, σ-ODD → Dirichlet/anti-periodic across the fold |
| Time row | Static, or H pinned=0 as gauge | σ = t→−t acts on the **f_T-driven (time-on) sector** — the seal's content is carried ONLY by the time-on arm (`w7_results.md:64`) |
| Result | ω ~ 1/R → "box artifact, continuum" | UNKNOWN — never solved with this BC |

The crux: the box-control solves pinned the SAME Dirichlet value on every field and
scanned R. The physical seal would (i) hold R **fixed** (a physical cell, not a knob),
and (ii) split the fields by σ-parity, giving DIFFERENT conditions to even vs odd
sectors — and the live (quantizing) content sits in the time-on/odd sector, which the
static box-control solves either froze or gauge-pinned away.

---

## 4. THE DECISIVE QUESTION + how to test it (the heart of F4)

**Decisive question:** Would imposing the ACTUAL seal BC — the time-reversal /
mirror-fold junction at the physical cell radius (NOT a generic Dirichlet box) — change
the time-live spectrum from box-control/continuum to a PHYSICAL (possibly non-harmonic)
discrete spectrum?

Split into ANALYTIC sub-questions (derive the BC) and the SOLVE (impose + re-run).

### 4A. ANALYTIC sub-questions (derive the seal junction condition — do FIRST, no solve)

- **A-i. Write the explicit junction condition across the fold.** The parity
  dichotomy (σ-EVEN→Neumann, σ-ODD→Dirichlet/anti-periodic) is derived, but the
  concrete **Israel / same-minus matching of the second fundamental form of the σ-ODD
  sector at the seal** was never computed (`fermion_forcing_results.md:273-275`). This
  is the GR-corpus junction-condition machinery (Principle 4: the GR corpus is a mine)
  transformed under the same-minus quotient. Deliverable: the coupled matching
  conditions that the cell's fields and the mirror cell's fields satisfy at ρ = b−fqa
  = 0, per σ-parity sector. **This is analytic; no solve.**

- **A-ii. Which fields are σ-even vs σ-odd?** From `fermion_forcing_verifier_results.md:88-90`:
  the arm (g_tr, g_tθ) is ODD, φ (in g_tt) is EVEN. Map each field/fluctuation amplitude
  in the time-live solver onto its σ-parity, hence onto Neumann vs Dirichlet/anti-periodic.

- **A-iii. Resolve the involution choice (gating — see §6).** The junction condition
  depends on WHICH involution is the seal: the W6 same-minus t→−t, or the competing
  P×T (`fermion_forcing_verifier_results.md:91-92`), which "would regrade" the
  parities. Different parities → different Neumann/Dirichlet assignment → potentially
  different spectrum. **Do not solve until this is set by Charles.**

### 4B. THE SOLVE (impose the derived BC + re-run the time-live solver)

- Take the existing time-live solver (the STEP2 / P5e machinery) and **replace** the
  generic Dirichlet outer wall with the derived seal junction condition (4A) at a
  **fixed** physical cell radius. Turn the time-on / σ-odd sector ON (un-freeze the
  f_T-driven amplitude that the static box-control solves froze or gauge-pinned).
- Read the resulting spectrum: harmonic ladder (1:2:3…) or non-harmonic? Does the
  lowest level stay FINITE (not → 0) as the physical structure is held, vs the old
  ω → 0 of the scanned box?

### Gates (pre-registered, before any solve)

1. **Control gate (reproduce the old result):** with a GENERIC Dirichlet wall +
   R-scan, the new solver must reproduce the banked ω ~ 1/R box-control. If it does
   not, the harness is wrong, not the physics. (This isolates the seal BC as the one
   new thing.)
2. **Seal-BC gate (the new thing):** impose the derived junction condition at fixed R.
   Compare spectrum to the control. A genuine change requires the spectrum to differ
   from the scanned-box continuum in a way that SURVIVES the controls below.
3. **Involution-robustness gate:** run BOTH candidate involutions (t→−t and P×T) and
   report both; do not silently pick the one that discretizes (OBSERVE-not-target).
4. **Box-vs-physical gate:** confirm any discreteness is a property of the FIXED
   physical cell (not re-introduced by an arbitrary radius). If ω_n still scales away
   under a legitimate physical-size variation, it is still box-control.
5. **ANTI-HANG (binding op rule):** bounded grid (Nr ≤ 16/24), capped iters, single
   clean process, NEVER background-poll. A bounded honest partial beats a hang.
6. **Verifier-before-record:** blind adversarial verifier on whatever emerges, +
   premise set attached, before any bank.

**Interrogation tag:** this push is **METRIC-LED** ("what does the derived seal
junction condition DO to the spectrum?"), NOT template-led. We are OBSERVING what the
physical seal imposes, not targeting discreteness. If the analytic derivation (4A)
shows the seal imposes a plain symmetric value-glue with no normal-derivative
constraint (as the ONE computed junction so far did, `h1_types_results.md:108-110`),
then the answer may be "no change" BEFORE any solve — that is a legitimate, cheap,
analytic close.

---

## 5. THE HONEST COUNTER-WEIGHT (recorded — why F4 may NOT rescue a classical spectrum)

Even if the seal BC is non-trivial, two standing facts say F4 likely does NOT fully
rescue a classical discrete spectrum:

1. **Harmonic-ladder triviality.** A physical finite cell with a clean wall gives
   ω_n ~ n/R_cell — a TRIVIAL harmonic ladder (1:2:3…). The observed lepton/hadron
   pattern is nothing like 1:2:3. So "box-modes are physical" buys a discrete spectrum
   of the WRONG shape. Only a genuinely NON-HARMONIC seal junction (the σ-parity
   dichotomy producing different Neumann/Dirichlet sectors with a non-trivial matching)
   could give a non-trivial pattern — and that is exactly the untested object (§4).

2. **Cell size not natively pinned (F7).** Even a perfect discrete ladder needs a
   length to set the scale, and F7 is a known OPEN gap (~10⁴⁰ autonomy; F0 §F7): the
   cell radius is NOT natively pinned at particle scale. A spectrum ω_n ~ n/R_cell with
   R_cell unpinned predicts nothing absolute.

3. **The one junction actually computed was flat.** `h1_types_results.md:108-110`
   (`topo_d3_junction.py`): the computed seal junction is σ-EVEN / Neumann / ρ-flat —
   "it glues the datum SYMMETRICALLY with NO normal-derivative constraint that would
   discretize the value." And the doubled-cell cohomology gives "one type × continuous
   mass" (D = [discrete 4π] × [continuous (ln f)_seal], `dD/dE ≠ 0`, "No lattice, no
   jump", `h1_types_results.md:80-103`). The ALREADY-DONE seal analysis points toward
   "continuous," not "discrete."

**Net:** F4 likely does NOT overturn "must-quantize." But the σ-ODD / time-on junction
(the one sector that carries the seal's quantizing content, `w7_results.md:64`) was
NEVER imposed on a spectrum solve, and the explicit junction condition was never
computed — so the verdict cannot be banked as theorem-grade without doing 4A (and, if
4A is non-trivial, 4B). The honest status is: **well-supported, NOT closed.**

---

## 6. THE 2-3 PREMISES FOR CHARLES'S EYE (where a wrong choice is expensive)

1. **WHICH INVOLUTION IS THE SEAL?** (the most expensive, F0-flagged.)
   The whole quantizing content of the seal depends on this. The adopted reading is the
   **W6 same-minus t→−t** (σ:(a,b)→(−a,−b), on the stationary row a*=αf_T,
   b*=(f_θ/f_r)a*, `w7_results.md:52-54`). But a **competing involution P×T** is on
   record (`fermion_forcing_verifier_results.md:91-92`): "A different involution (P×T)
   would regrade, but that is a DIFFERENT seal than the w6/#42 same-minus time
   reversal." P×T regrades which fields are σ-even vs σ-odd → different Neumann/Dirichlet
   assignment → potentially a different spectrum. Choosing t→−t to make the spectrum
   discrete would be exactly the "fix a value to make it solvable" tripwire. **Charles
   must set (or hold open) which involution is the physical seal BEFORE 4B.**

2. **IS THE TIME-REVERSAL LABEL EVEN LOAD-BEARING, OR ONLY THE FOLD?** The FOLD
   (seal ≠ edge) is theorem-grade (c). The t→−t LABEL is row-conditional (d). It is
   possible the spectrum is set by the FOLD's parity dichotomy regardless of the
   t→−t/P×T naming — or it is possible the naming is what selects the σ-odd sector that
   carries the content. Charles's read on whether we are testing "the fold" or "the
   t→−t reading of the fold" frames the whole test.

3. **THE DEEPER CONTAINER IS POSITED, NOT DERIVED.** "No spatial infinity" (a, F0 A1)
   is the single deepest frame posit and is in TENSION with N6 (asymptotic flatness
   pins the vacuum branch). The cell-doubling (e, D2) is a CHOSEN topology with a live
   competitor (S²×S¹ → integer-Chern family, parked-unbuilt). The inner-core removal
   (f, D3) is a separate posited inner BC. A wrong choice here is expensive because the
   ENTIRE "physical box ⇒ physical modes" rescue rests on the container being physical
   — and three of its pieces are posited/chosen, not derived. If Charles wants the
   S²×S¹ doubling instead, the spectrum gets an integer Chern family (a genuinely
   different, possibly non-harmonic, structure) — that is a fork worth naming before
   committing to the I×S² double.

---

## ORIENTATION

- The FOLD (det g4 ∝ (b−fqa)²) is the one theorem-grade pillar of F4 (`w6_results.md`).
- The seal BC was NEVER imposed in any box-control solve (recon-confirmed §3); the
  derived-but-unused mirror BC is `w7_a_mirror_bc.py`.
- The decisive analytic sub-question (4A-i) — the explicit Israel/same-minus junction
  condition for the σ-odd sector — was named as "the next computation, not this one"
  (`fermion_forcing_results.md:273-275`) and is STILL unexecuted. It is cheap (analytic)
  and gates the solve.
- Honest expectation: F4 likely does NOT fully rescue a classical spectrum (harmonic
  triviality + F7 + the one flat computed junction), but the σ-odd/time-on junction is
  untested, so the box-control verdict is well-supported, NOT theorem-grade.

**Primary files:** `w6_results.md` (fold/determinant), `w7_results.md` (t→−t + parity
BC), `wcc_results.md:40-58` (seal closure BCs), `fermion_forcing_results.md` +
`fermion_forcing_verifier_results.md` (junction/P×T competing involution),
`h1_types_results.md` (doubling + one-number rigidity), `F0_SYSTEMATIC_AUDIT_results.md:132-143`
(F4/D1/D2/D3 grades), CANON.md C-2026-06-10-2 (the finite-cell canon).
