# E2 BATTLE PLAN — the coupled particle-in-universe solve (pre-registration draft)

**Date:** 2026-07-03 (late). **Status: APPROVED AS WRITTEN — Charles, 2026-07-03: "Go, run it
exactly as written." This committed version is the contract; deviations require his ruling.**
Operational staging (not a plan change): E2a = BUILD + verify the coupled solver (reduction
checks, pure-universe limit recovery, instruments wired) with a bounded single-seed smoke test;
E2b = the pre-registered sweep, one bracket at a time, single process; then the blind verifier.
Stage E2 of
`microphysics_reentry_miniMAP.md`; consumes the blind-verified E0 tables and E1 condition set
(`microphysics_E1_composite_closure_results.md`). Charles's rulings carried: R-B = go with plan
first; R-C = migration is a margin note; guardrail 1 (family/Z = output) and guardrail 2
(both neighborhoods, no favorite) remain binding. Data-blind: no particle masses/data anywhere.

## The question (one sentence)

Does the coupled system — a native S² L2+L4 particle cell and the real N=0 fundamental ambient,
solved TOGETHER on their two domains with the derived condition set — have any actual solution,
and if so where (plateau vs wall), at what sizes, and does it survive the stability filter and
the σ cross-check?

## The unknowns and the conditions (from E1, counting SQUARE)

Solve for: cell fields (φ, ρ, f(r,θ)) on [0, r_p] + ambient (φ, ρ) on [r_p, r_sU] + the two
free boundaries r_p, r_sU. Conditions: core naturals (φ'=ρ'=f_r=0 at 0), seal set C1a/C1b/C1c +
C2 (⇔ E_ang(r_p)=U(ρ_p)), outer fold set (φ=0, ρ'=0, H_amb=0; q an output), poles f(r,0)=0,
f(r,π)=π, and the Δφ anchor at bracket level (per the cited E1 ledger #5: a* HELD at the
banked bracket value; Δφ floats at O(back-reaction) and is REPORTED, never imposed exactly on
the composite). [WORDING FIX post-approval, flagged to Charles: the original parenthetical
said "a* floats" — a paraphrase slip contradicting its own E1 citation; the E2a builder
implemented the cited E1 reading, which this fix restores. No physics change, same square
count; the alternate branch (a* freed + exact-Δφ row) is unwired and would need Charles's
ruling before use.]

## Knobs and coverage (all pre-committed)

- **Brackets:** all four E0 brackets (Z ∈ {1,8} × {A1 m=3, A3}) — family/Z dependence is an
  OUTPUT (guardrail 1). A closure in one bracket only = family-sensitive, said so.
- **Carrier couplings (ξ, κ) and winding N:** seeded from the E1 necessary-map admissible cells
  ONLY as coverage guides (they are necessary, not sufficient): N=1 moderate-ξ plateau cells,
  N=2 κ≈1 wall cells, plus 2 fully-admissible small-coupling cells per bracket as controls.
  ξN < 2 enforced (E1 core closure); κ > 0.
- **Neighborhood slices (guardrail 2, both always):** plateau-target seeds (r_p deep interior)
  AND wall-target seeds (r_p near the U=2 station r* ≈ 0.95 r_s) — r_p is a FREE unknown; the
  slices are seed placements, never constraints. Where the solver takes r_p is a result.
- **Seeds:** ≥3 distinct seeds per (bracket × window-cell × slice) — rigid-plus-bulge
  perturbations of controlled amplitude (the bulge theorem says any solution is non-perturbative
  in θ; far-from-rigid amplitudes included, banked N=1 undersampling lesson).

## Method (Category-A, soundness-checked)

Monolithic Newton/LM on the full coupled system (both domains + both free boundaries in ONE
residual vector — the E1 stiffness finding ‖Ψ‖~1e6–2e8 forbids domain-by-domain iteration),
building on `cell_solver_f2d.py` (2-D f, SH-exact angular, Cheb radial) + the T3 ambient
machinery; continuation in (ξ, κ) from the best-conditioned window cell. Grids BOUNDED per
anti-hang: cell Nr ≤ 16/24, ambient resolved at its seal wall (the E0 dense tables give the
scale), Newton/Krylov iters capped, ONE process, no background-poll, dense-LM as flooring tool,
recompute-on-saved-fields where possible. Budget: reduce and report throughput-limited rather
than hang; a bounded honest partial beats a dead agent.

## The verdict instruments (pre-committed BEFORE outcomes are seen)

1. **Existence:** a converged solution = residual floor ≤ 1e-8 (relative), grid-stable
   (Nr 12→16→24 or FD cross-check), seed-independent (re-found from ≥2 distinct seeds), both
   free boundaries interior and finite. Derrick + H-drift as artifact filters throughout
   (banked: H_cell ≡ 0 must hold on any true solution — a free consistency gate).
2. **Stability:** the two-tier filter — tier (a) constraint-reduced ENERGY Hessian (NOT the
   action Hessian — banked error), PD ⇒ stable; tier (b) indefinite ⇒ constraint-respecting
   perturb-and-coupled-re-solve (the banked decisive test).
3. **The σ cross-check (the armed pass/fail audit):** on any converged composite, read the
   matter density BOTH ways — geometry route (ε via m'_MS = 4πρ²ρ'·ε from the composite
   profile) vs matter-action route (the ambient's σ from L_m = −U; the cell's from the L2+L4
   stress) — agreement to grid tolerance across BOTH domains and at the seal. This can
   genuinely fail (nothing free on either side); failure = the result does not bank.
4. **Characterization (never filtering):** where r_p lands, q_p (ambient flux through the seal,
   an output), core depth φ_c vs the derived floor ρ_c ≥ N√(κ/(2(2−ξN))), bulge profile,
   cross-bracket ratios. Ratios only; NO masses (data-blind).

## Failure readings (pre-committed, solver-first)

- **No convergence anywhere:** indicts, in order — (1) seeds/continuation coverage (the bulge
  is non-perturbative; widen amplitudes first), (2) grid/conditioning (the 1e6–2e8 stiffness),
  (3) then and only then the frame: banked as the E2 scoped negative ("no static concentric
  embedded L2+L4 cell in the real ambient") with full premise set → the pre-named escape
  ladder: ω≠0 (Charles's φ-angular hunch — internal rotation, Nψ → Nψ+ωt) as a REFRAME decision
  with Charles, never a patch. A mechanism is never the reading.
- **Converges but σ cross-check fails:** the solve is wrong or a premise is — treated as a
  solver-completeness hunt (the audit exists precisely to catch this), not massaged.
- **Converges in one bracket only:** family-sensitive, reported as such (guardrail 1) — not
  canonical, not suppressed.
- **Converges on the wall slice only / plateau only:** the two-sided selectivity made real —
  reported symmetrically; no slice was preferred going in.

## Anti-drift tripwires

Observing-not-targeting: the deliverable is WHAT THE COUPLED SYSTEM DOES — including "nothing."
No acceptance criterion references shape/lump/expected answer (provenance + honesty only, per
the governing limit). Every converged object gets the full instrument set before any adjective.
Blind adversarial verifier on the whole E2 output before banking; results doc carries the
premise ledger forward from E1 unchanged (any new premise = flagged addition, tagged).

## Deliverable

`microphysics_E2_coupled_solve_results.md`: per-bracket × per-slice outcome table (converged /
no-converge with diagnosis / throughput-limited), instruments 1–4 per solution, the σ-audit
verdicts, characterization ratios, and the honest coverage statement (what was NOT swept).
