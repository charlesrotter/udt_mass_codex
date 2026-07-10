# DESIGN — the matter-filled background & the closure-amount scan (Thread A, done right)

> **⚠ α-COEFF CORRECTED (2026-07-10):** any `+α·ξ·e^{αφ}·ρ²·I_r` below is WRONG — the anchor-verified coefficient is **`−(α/2)·ξ·e^{αφ}·ρ²·I_r`** (`verify_alpha_coeff_ANCHORED.py`; reproduces base φ-EOM + base ρ-EOM + T_AB). **SIGN-CRITICAL:** for α<0 the direct source is POSITIVE (SUPPORTS `I_r`), not draining. Any pre-grok reasoning here that relied on the old `+α` sign is **CONDITIONS-CHANGED** (see LIVE.md on grok).


**Date:** 2026-07-08 · **Author:** Claude Opus 4.8 (1M) with Charles. **Status: DESIGN / pre-solve spec.**
Data-blind (no 1101 / 7.004 / C / μ_g / lepton values). Supersedes the vacuum-first reading of Thread A in
`derived_background_and_phi_coupling_DESIGN.md` §A — see §1 below for why.

---

## 1. Why this spec exists (the reframe from the cosine reconciliation)

The plan in `derived_background_and_phi_coupling_DESIGN.md` was: derive the ambient background φ(r) first (Thread A,
vacuum-ish), then add matter (Thread B). The cosine-reconciliation derive (2026-07-08, PROVISIONAL — blind-verify
pending, §5 Stage 0) forces a merge of A and B, for two independent reasons that point the same way:

- **Dimensional (iron-clad):** a maximum *distance* `x_max` cannot be built from `c` and `G` alone — those two
  constants cannot form a length; a mass/length scale is required. So any absolute scale in UDT must come from matter.
  *(Precision: this forces "no absolute SCALE without matter," NOT "no solution without matter" — vacuum solutions
  exist, they are just featureless/scale-free. It is the physics point below that upgrades "no scale" to "no edge.")*
- **Physics (scoped lead):** the full native two-player **vacuum** scalar equation `Z(ρ²φ′)′ = 4e^{−2φ}ρ′²` gives a
  φ that **saturates** — `e^{−φ/2}` levels off and never reaches 0, so **there is no finite `φ→∞` edge in vacuum**.
  Structural reason: the vacuum forcing `4e^{−2φ}` **vanishes as φ→+∞**, so nothing can drive φ to infinity. The banked
  "round-cell cosine" that *does* have a finite edge is a leading-order, cycle-averaged, ρ-frozen, **matter-sourced**
  reduction (`v''=−k²v`), self-labeled a leading-order instrument — NOT a solution of the native equation
  (`cosine_reconciliation_check.py`; `ladder_lemmaD_sealing_amplitude_results.md` truncation ledger).

**Together:** matter is the source of BOTH the scale AND the structure (the edge). Vacuum UDT is scale-free and
featureless; matter breaks the scale symmetry, and that single act supplies a scale and carves the edge. So the
"derived background" a particle embeds in is *already* a matter-coupled object — Thread A cannot be done vacuum-first.

**The sharp hook (why the edge, the matter amount, and α are ONE question).** The native direct matter source in the
dilation equation is `α·ξ·e^{αφ}·ρ²·I_r` (`udt_phi_blindness_relaxation_results.md`). Its φ-dependence is `e^{αφ}`:
- **α ≤ 0:** the source dies (or is absent) as φ→+∞, like the vacuum term ⇒ expected **no edge**.
- **α > 0:** the source **grows** as φ→+∞ ⇒ it can **sustain/drive** φ→∞ at finite r ⇒ **an edge can exist.**
So whether the universe has a finite `φ→∞` edge (= your `x_max`) may hinge on the **sign of α** and the **amount of
matter** `I_r`. This is the single coupled test this spec sets up. **Observe, do not target:** we do NOT assume α>0 or
that an edge exists — we scan and report what forms.

**Charles's hope (the payoff to watch for):** if a cell CLOSES (finite edge / seal satisfied) only for a **critical
amount** — or a bounded window — of matter, then the amount is not free: it is **pinned by closure**, and `x_max`
becomes *derived* (c, G, + a theory-forced critical mass) rather than requiring a free input. That would be the honest
recovery of "c and perhaps G determine it." Whether such a critical amount exists, and whether it is fixed by the
theory's constants, is exactly what the scan observes. **Whatever we find moves us forward** (Charles): a critical
amount, a window, or no-edge-either-way are all real characterizations of the solution space.

---

## 2. The frame stated whole (regime + what is held fixed)

- **Equations:** native two-player, **Branch-P interior**, with the direct matter source ON:
  ```
  Z(ρ²φ′)′ = 4 e^{−2φ} ρ′²  +  α·ξ·e^{αφ}·ρ²·I_r
  ρ″       = 2 φ′ρ′  −  (Z/4) ρ e^{2φ} φ′²  +  (e^{2φ}/4)( ξ ρ I_r  −  κ N² I_4th / ρ³ )
  I_r = ½∫ sinθ f_r² dθ ≥ 0 ,   I_4th = ½∫ (sin²f / sinθ) f_θ² dθ
  ```
  (`cell_solver_f2d.py:17-19` with the α-source restored per `udt_phi_blindness_relaxation_results.md`.)
- **Regime SCOPE (whole-before-slice — this solve is ONE tile):** static · spherically-symmetric round φ(r), ρ(r)
  (angular matter enters only through the θ-averaged moments `I_r`, `I_4th`) · Branch-P interior · matter ON.
  **NOT covered here (scoped out, revisit later):** off-round shear `h_AB`, Branch-G exterior matching / the seal
  junction, time-on (t→−t) sector. A "no edge" or "edge" result is SCOPED to this tile, never the frame's verdict.
- **Data-blind:** we look for edge-existence and a critical/bracketed matter amount as **structural facts and ratios**;
  no anchored numbers (1101/C/μ_g) enter.

---

## 3. Premise ledger (every choice tagged — chose / derived / assumed)

| # | Premise | tag |
|---|---------|-----|
| P1 | Matter is the source of scale AND edge (vacuum = no finite edge) | **DERIVED** (dimensional + the vacuum solve; Stage-0 verifies) |
| P2 | Direct source `α·ξ·e^{αφ}·ρ²·I_r` is the honest φ-matter coupling | **DERIVED** (action variation, blind-verified `udt_phi_blindness_relaxation_results.md`) |
| P3 | α scanned across BOTH signs (not pre-fixed) | **CHOSE-to-explore** (p16 verdict C; sanctioned by design §B.2) |
| P4 | "Amount of matter" knob (Stage 1: prescribed `I_r` amplitude; Stage 2: N, κ/ξ) | **CHOSE** — Design Decision D1, §7 |
| P5 | Stage 1 prescribes a parameterized `I_r(r)` profile shape to decouple the scan | **CHOSE-provisional / ledgered recon STAND-IN** (a characterization scan; self-consistent `I_r` in Stage 2 — do NOT read Stage-1 numbers as the answer; mitigations M1–M3 §5) |
| P5b | Scan range bracketed by the **theory's own** edge↔saturate↔collapse transitions (adaptive), NOT by ΛCDM/observed density | **DERIVED-bracket** (data-blind; ΛCDM is a DEFERRED comparison only, never a scan input — targeting trap) |
| P6 | Branch-P interior; round background (angular matter → moments) | **CHOSE** (the tile; the particle cell lives in Branch P) |
| P7 | Finite core `ρ(r_c)=ρ_c>0`, inner fold `φ′(r_c)=0` | **DERIVED** (smooth center diverges the 1/ρ² source; `cell_solver_round.py:14-15`) |
| P8 | Z (scalar kinetic weight) held fixed, test Z∈{1,8} | **CHOSE-fixed** (prior result claimed Z-independent — re-check, don't assume) |
| P9 | ξ=1, κ=1 units; ratios are the observables | **CHOSE-units** (κ/ξ sets absolute scale) |
| P10 | "Closure" = §6 detection criteria (finite edge OR seal + asymptotic condition) | **CHOSE-definition** — pin before scanning (§6) |

---

## 4. What is already known (so the scan is not re-run)
- Vacuum (I_r=0 or α=0): **φ saturates, no finite edge** (Stage-0 confirms). This is the null the scan is measured against.
- The α-source sign argument (§1 hook): α>0 grows with φ, α≤0 dies. The scan TESTS whether this structural expectation
  actually produces / fails to produce an edge in the full coupled solve — it is a hypothesis to check, not a result.

---

## 5. The solve — staged, bounded, cheap-first

**Stage 0 (gate — do FIRST): blind-verify the vacuum cosine-reconciliation derive.** A fresh zero-context adversarial
verifier re-runs `cosine_reconciliation_check.py`, checks the symbolic non-identity, the "cosine = averaged/matter-sourced
reduction" reading against the source docs, and the vacuum "no edge" numeric. Only if it survives do we build Stages 1–2
on it. (verifier-before-record; the reconciliation is currently PROVISIONAL.)

**Stage 1 (cheap, 1-D ODE — the edge-existence scan).** Prescribe a parameterized matter source `I_r(r)` (a bounded
localized profile; amplitude = the matter-amount knob `A_m`, tagged provisional P5). Solve the coupled **(φ, ρ)** ODEs
(BCs P7) as a 2-D scan over **(α, A_m)**, α across both signs. **OBSERVE**, at each point, which of the three §6 outcomes
occurs (finite edge / saturation / ρ-collapse). Deliverable = a map of the (α, A_m) plane: *where does a finite `φ→∞`
edge appear at all*, and *is there a critical A_m or a bounded window* (for the α that admit an edge)? Bounded: modest
grid, capped iterations, a SINGLE clean process, scipy `solve_ivp`/shooting (this is a 1-D ODE — fast). NEVER
background-poll. Test Z∈{1,8} for robustness (P8). Bracket the `A_m` range by the theory's own outcome transitions
(P5b, adaptive) — NOT by observed cosmology.

**Stage-1 honesty mitigations (binding — P5 is only a legitimate stand-in WITH these):**
- **M1 — recon-only reading.** Report Stage 1 as "an edge exists / roughly where / for which α-sign," NEVER as "the
  critical amount is X." The continuous map is a POINTER for Stage 2, not a verdict.
- **M2 — shape robustness.** Run the scan for 2–3 distinct `I_r(r)` profile shapes; an edge that appears for one shape
  but not others is a shape-artifact, flagged, not a result. Only shape-robust structure is carried to Stage 2.
- **M3 — native-N confirmation is mandatory.** No edge/critical-amount claim is banked until Stage 2 reproduces it
  with the self-consistent quantized winding matter. Continuous `A_m` can land between allowed integer N — a real
  possibility the scan cannot see (P4/§7 D1 downside 3).

**Stage 2 (escalate ONLY if Stage 1 shows an edge; slow, hard-bounded).** Replace the prescribed `I_r` with the
**self-consistent** winding field: full `(f, φ, ρ)` solve (`cell_solver_f2d.py`), `I_r` generated by `f(r,θ)`, at the
(α, matter-amount) region Stage 1 flagged. Confirm the edge / closure survives with *real* matter, and locate the
critical amount self-consistently. **ANTI-HANG (binding):** grid Nr≤16/24, cap Newton/Krylov iters, ONE clean process,
recompute on SAVED fields where possible; if a solve would exceed budget, REDUCE and report "throughput-limited" — a
bounded honest partial beats a hang. Do NOT launch Stage 2 as a background poll.

---

## 6. Detection criteria (pin before scanning — P10)
Integrating outward from the core, classify the outcome (all data-blind, shape-based):
- **FINITE EDGE (the x_max signature):** `v=e^{−φ/2}` decreases and **reaches 0 at a finite radius** `r_edge`
  (φ→+∞), smoothly (not via ρ→0). Record `r_edge` and the approach law (how v→0), as ratios/structure, not a number.
- **SATURATION (no edge):** φ levels off, `v` bounded away from 0 as r grows. (The vacuum outcome.)
- **ρ-COLLAPSE (a different singular edge):** `ρ→0` at finite r (the 1/ρ² blowup) — a collapse, NOT the redshift edge;
  record separately.
- **CLOSURE (Stage 2 / if a seal is used instead of the open edge):** the seal conditions `φ′=ρ′=f_r=0` at `r_s` +
  the transversality `H(r_s)=0` are met — the finite mirrored-cell version. (Note the two "edges" — the open `φ→∞`
  cosmological edge vs the finite mirror seal — may be distinct objects; §2 scope. Report which one, if any, the matter
  produces.)
**Characterize, do not filter:** we RECORD which outcome occurs across the plane; we do NOT discard runs that fail to
give an edge (a saturation region is a real result, not a failed run).

---

## 7. Design decisions for Charles (load-bearing, pin before Stage 1)
- **D1 — the matter-amount knob. LOCKED (Charles 2026-07-08): continuous-first as a ledgered recon STAND-IN.** Stage 1
  scans the prescribed `I_r` amplitude `A_m` continuously (fast 1-D map of *where* an edge lives); Stage 2 confirms with
  native quantized winding N. Legitimate ONLY with mitigations M1–M3 (§5). Downsides acknowledged: (1) prescribed shape
  is an imposition → M2; (2) `A_m` not independently dialable in the self-consistent solve → M3; (3) native charge is
  integer N, a continuous critical `A_m` can fall between allowed N (and that discreteness is itself the interesting
  structure) → M3. ΛCDM/observed density is NOT a scan bracket (targeting trap) — it is a DEFERRED comparison only (P5b).
- **D2 — α range.** Scan both signs symmetrically (e.g. α∈[−2, +2] including the α=−2 "physical-metric coupling" and
  α=0 φ-blind reference). Observe-not-target: no pre-fix.
- **D3 — round vs. bring shear in.** This spec is round (angular matter → moments). If the edge turns out to need the
  angular/shear sector, that's a scoped escalation, not this tile.

---

## 8. Deliverable
A blind-verified (verifier-before-record) characterization of the matter-filled Branch-P background:
1. **Does matter produce a finite `φ→∞` edge** in the full (un-averaged) two-player system, and for which **sign of α**?
2. **Is there a critical matter amount, or a bounded window, for closure** — or does an edge exist for all/no amounts?
3. If a critical amount exists, its **structural expression** (data-blind ratios) — and a first read on Charles's
   hope: **is it fixed by the theory's constants** (the analog of "c and G determine it"), or does it remain a free scale?
Every banked statement carries its regime stamp (§2 scope) and premise set (§3). Negative outcomes (no edge for any
amount, in this tile) are first-class results, scoped, and logged to NEGATIVES_REGISTRY with their premises.

## 9. Records to read first
`cosine_reconciliation_check.py` + the reconciliation result (this session, PROVISIONAL);
`udt_phi_blindness_relaxation_results.md` (the α-source, restoring channel); `cell_solver_f2d.py` (the solver);
`native_field_equations_constrained_two_player_results.md` (the two-player system — tagged "not yet canon");
`ladder_lemmaD_sealing_amplitude_results.md` (the cosine as a leading-order instrument — what it is/isn't).
