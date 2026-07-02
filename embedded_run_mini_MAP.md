# Mini-MAP — the EMBEDDED cell run (H_cell = H_amb), before any compute

**Date:** 2026-07-02. **Mode:** MAP (no compute). **For claude.ai review BEFORE the run** (per its spec:
"send the spec back when the mini-MAP is drafted"). **Author:** Claude Code. Foundation:
`embedded_cell_closure_H_amb_results.md` (H_cell=H_amb DERIVED+blind-verified), the N=1,2,3 CLOSED-cell
negatives (`cell_solver_f2d_first_build_results.md`, `cell_solver_f2d_N2_results.md`, blind-verified),
`discreteness_preregistration.md` (Class-A EMBEDDED sub-class, AMENDMENT 2026-07-01b).

## 0. Why embedded, why now (the motivating finding, restated)
The closed (H=0) round-static Class-A cell has NO finite cell at N=1,2,3 — and the blind-verified reason
is specific: **the matter is convex/stable (V7); the cell dies because the GEOMETRY has no finite
stationary point** — nothing anchors the seal, so dilution (ρ→∞ and/or φ→deep-negative) is always
downhill. Embedding is the failure-mode-specific cure (claude.ai): the junction matching **pins the seal
data to an ambient solution**, which structurally closes that escape direction — a mechanism-level reason
to expect a different outcome, not merely a new place to look.

## 1. THE COUNTING (done honestly, BEFORE running — the thing that made the closed cell readable)
Interior cell on r∈[r_c, r_s], core = regular/mirror inner boundary (φ'_c=ρ'_c=0, f pole BCs). Shooting
the interior EOMs outward from the core is a **2-parameter family** (φ_c, ρ_c) [φ'_c=ρ'_c=0 pin the other
two constants]; at r_s it yields (φ, ρ, π_φ, π_ρ) with H conserved = H(core) = −L̄(φ_c,ρ_c).

The ambient (universe-interior) solution at the seal location R_amb supplies KNOWN targets
(φ_amb, ρ_amb, π_φ,amb, π_ρ,amb, H_amb) — see §4 for where these come from.

**Matching conditions at the seal (source-free Class-A embedded):**
- field continuity: φ_cell(r_s)=φ_amb, ρ_cell(r_s)=ρ_amb  — 2 (essential)
- momentum continuity (JC1/JC2): π_φ,cell=π_φ,amb, π_ρ,cell=π_ρ,amb — 2 (natural)
- corner condition C2: H_cell(r_s)=H_amb — **REDUNDANCY QUESTION (must settle before running):** since
  H=q'π−L̄ is built from (φ,ρ,π_φ,π_ρ), IF all four field/momentum matches hold then H matches
  automatically ⇒ C2 is IMPLIED, not independent. (Contrast the CLOSED cell, where there is no field
  match — the mirror φ'=ρ'=0 replaces it — so there C2=H=0 is the independent 3rd condition. C2's status
  FLIPS between closed and embedded. This must be stated as a premise, because it decides the count.)

**Count (taking C2 as implied ⇒ 4 independent matching conditions):**
| scenario | unknowns | conditions | determinacy | reading |
|---|---|---|---|---|
| **R_amb FREE** (scan ambient) | φ_c, ρ_c, r_s, R_amb = **4** | 4 | **SQUARE** | isolated cells generic — for each admissible ambient a cell |
| **R_amb FIXED** (one ambient density) | φ_c, ρ_c, r_s = **3** | 4 | **OVER-determined by 1** | cells exist only at ISOLATED ambient densities → the **Misner–Sharp band** |

**⇒ The honest pre-registered expectation:** unlike the closed cell (exactly square → runaway), the
embedded cell at fixed ambient density is **over-determined by one** → **cells are admitted only at
isolated ambient densities.** Scanning the ambient (R_amb / H_amb) as a diagnostic axis should then show
cells appearing at discrete/banded ambient values — that IS the discreteness mechanism (isolation source
§4d), and it is the mass-vs-cosmology structure if it appears. **If C2 turns out NOT redundant** (e.g. a
seal source, or the momentum match is weaker than full derivative continuity), the count shifts by 1 —
so the redundancy question is settled FIRST (a CAS/analytic check, not a solve), and the table re-read.

## 2. Premise ledger (chose / derived — tagged BEFORE running)
| # | premise | tag |
|---|---|---|
| P1 | ambient = universe-cell INTERIOR solution (Branch-P/matter), not vacuum-G | THEORY (finite-cell canon, F5) — but its VALUE is OWED, see §4 |
| P2 | seal source-free (Class-A embedded); φ,ρ,momenta continuous | CHOSE (source-free first; a seal source = Class-B proper, shifts the count) |
| P3 | core = regular/mirror inner boundary (φ'_c=ρ'_c=0) | CHOSE (as in the closed build; a finite singular core is the alternative) |
| P4 | C2 (H-corner) is redundant given field+momentum continuity | **CHOSE-pending-CAS** — settle analytically before the run (decides the count) |
| P5 | round, static, constrained-metric form; minimal L2+L4; N per run; Z fixed | CHOSE (Risk-1 standing; same as closed build) |
| P6 | H_amb / ambient data are DERIVED from the universe solution, NOT free knobs | THEORY — but see §4 (the universe solution is owed) |

## 3. H_amb is DERIVED, not a knob (claude.ai item 2)
The physical ambient data come from the F5 universe-cell solution at the particle's location R_amb — a
DERIVED value, not a fitting parameter. **Scanning H_amb (equivalently R_amb / ambient density) is a
DIAGNOSTIC AXIS** that maps where cells exist as a function of ambient density (the Misner–Sharp band,
directly). The axis is **labeled diagnostic**; the derived physical value(s) are **marked on it** once the
universe solution (§4) is in hand. No cell is claimed at a hand-picked H_amb; the claim is the STRUCTURE
of where-cells-exist along the axis, with the derived value(s) annotated. If cells appear at isolated
ambient densities, that plot is the first mass-spectrum-vs-cosmology figure of the program.

## 4. ⚠️ LOAD-BEARING OPEN PREMISE — where does the ambient solution come from?
The embedded run needs (φ_amb, ρ_amb, π_amb, H_amb). These come from a **universe-cell solution**. But:
**if the universe cell is ALSO a closed round-static cell, our N=1,2,3 result says it too runs away** —
so we may not HAVE a finite ambient solution to match to. Candidate resolutions (for claude.ai — this is
exactly the kind of thing to settle before running):
- (i) the universe cell is the ONE self-closing object (claude.ai's Machian reading / F5 / "critical
  universe" canon): it self-closes by a mechanism the small cells lack — e.g. it sits at the CRITICAL
  matter amount, or is a Branch-G (continuum-exterior, scale-free) object, or its size IS the thing set
  by its own H. If so, the universe solution is special and must be characterized on its own terms.
- (ii) as a STAGING step, run the embedded match against a **MODEL ambient** = a chosen constant
  (φ_amb, ρ_amb, H_amb) treated purely as the §3 diagnostic axis, with the DERIVED value deferred until
  (i) is solved. This lets us test the MECHANISM (does an ambient anchor close the escape direction and
  admit isolated cells?) before the harder universe-solution question — but it must be labeled a model
  ambient, not the derived one.
**Recommendation:** stage it — (ii) first to test the mechanism + counting, then (i) for the physical
value. But claude.ai should confirm, since (i) may reframe the whole picture (if the universe cell is
Branch-G / critical, the "ambient" is not just a Branch-P interior value).

## 5. Boundary conditions + diagnostics change (claude.ai item 3)
The outer seal is NO LONGER a mirror (φ'=ρ'=0). It is the **matched interface** (§1). Consequences:
- The transversality/closure condition is **H_cell(r_s)=H_amb**, not H=0 (and see the P4 redundancy).
- The **Derrick identity** must be RESTATED for the matched boundary: the closed-cell free-boundary
  Derrick (S_a=S_b, boundary term killed by the mirror) picks up an ambient boundary term — the correct
  per-solution identity for a matched cell is owed (analytic, before the run) and becomes the adapted
  artifact filter.
- **H-drift** stays a discretization-soundness diagnostic (H conserved in the interior; check it lands on
  H_amb at the seal).
- **Two-tier stability filter** as now built (tier-a ENERGY Hessian, tier-b constraint-respecting
  re-solve) — unchanged, applied to any matched closure.

## 6. What the run does / what counts as a cell (pre-registered)
For fixed N, Z, ξ=κ=1, and the §4 ambient (model first): scan the ambient axis; at each ambient value,
solve the interior BVP + match (the §1 conditions); a **cell** = a converged interior solution meeting all
matching conditions with small adapted-Derrick and H-drift, that passes the two-tier filter. Discreteness
= cells admitted only at ISOLATED ambient values (the §1 over-determined-by-1 expectation), seed-,
grid-, and Z-checked, UNLABELED. A continuum of ambient values all admitting cells, OR runaway
everywhere, are the honest alternative outcomes — reported as-is.

## 7. Owed BEFORE the run (gate)
1. Settle **P4** (C2 redundancy) analytically — fixes the count.
2. Restate the **matched-boundary Derrick identity** analytically (the adapted artifact filter).
3. Decide the **§4 ambient** (model-ambient staging vs universe-solution-first) — claude.ai's call.
Then implement + run (model ambient first), verify, and only then pursue the derived universe value.
**Send-back point: this MAP is for claude.ai to check the counting, the P4/redundancy call, and the §4
ambient question before anything executes.**
