# N5d Stage-1 Pilot — Results (TOOL-LIMITED / Outcome D; NO A/B banked)

**Date:** 2026-07-06 · **Driver:** Claude Opus 4.8 (1M) · run foreground, bounded, from build `84287b6`.
**Scope (ONE tile):** static, Branch P, block-diagonal, **frozen H3-hopfion source + live ℓ=2 shear + exact φ**,
whole cosmic cell, BOTH seal BCs (S-Dir, S-JC2). Command:
`timeout 550 python3 n5d_pilot.py --Nr 16 --Nth 8 --lmax 2 --maxit 30 --budget 100`. Artifacts:
`n5d_pilot_SDir.json`, `n5d_pilot_SJC2.json`, `n5d_pilot_report.txt`, `n5d_pilot_run.log`, `n5d_pilot.py`.

## Verdict: TOOL-LIMITED (Outcome D). NO Outcome A or B banked.

The pilot INFRASTRUCTURE works (real H3-hopfion source loaded — Q=0.9917, virial-balanced; bounded; fast: ~1s/BC;
exact e^{−2φ}; contamination-clean), but the coupled solve **did NOT converge** under either seal BC, so pin-vs-
continuum CANNOT be read from this run.

| quantity | S-Dir | S-JC2 | reading |
|---|---|---|---|
| converged (tol 1e-12) | **False** | **False** | maxit=30 hit at EVERY continuation step; Φ floored ~1e-4 (not ~1e-12) |
| closed_cell_exists | False | False | **NOT a physics "no"** — reflects non-convergence (H_seal ≈ −5.6e-3 / −6.4e-3, not ≈0) |
| jac_cond | **4.2e15** | **9.2e16** | near-singular, at the float64 limit ⇒ linear solves rank-deficient/unreliable |
| a2_peak (shear response) | 5.1e-3 | 1.9e-5 | at/near solver noise despite source amp→1 (sh2 up to 12.5) |
| q_raw / M_readout | 2.5e-8 / −2.5e-8 | −4.1e-8 / +4.1e-8 | induced mass ≈ 0 to noise (sign_convention=−1) |
| reduced-source turning points | 1 | 3 | mechanism-(i) sign-changes DO appear, but differ by BC — within non-converged noise, not a signal |
| Derrick residual | 1.8e-2 | 9.1e-3 | not satisfied (consistent with non-convergence) |
| throughput_limited | False | False | NOT time-limited (fast); this is a CONDITIONING/convergence limit, not throughput |

## Why this is tool-limited, not a verdict (solver-first)

Per MISMATCH → SOLVER, not mechanism / not metric: the run's failure is a SOLVER conditioning issue, not a physics
statement. The Jacobian condition number ~1e16 sits at float64's precision floor, the LM floors at Φ~1e-4 without
converging, and the shear + induced-q are at solver noise. **A near-singular Jacobian is exactly ambiguous between (a)
a numerical/gauge artifact and (b) a genuine soft/flat shear direction — and a flat direction, if physical, would
itself be evidence toward CONTINUUM (no pin).** At cond~1e16 we cannot distinguish signal from noise, so the
pin-vs-continuum question lives precisely at the unresolved near-singular direction. That is the honest finding.

The build agent had flagged that at the exact round seed (a2=0) cond~6e16; the nonzero seed (a2=1e-3) improved the
Nr=8 smoke (cond~1e5) but at the full Nr=16 continuation the coupled system returns to cond~1e15–1e16 — so the
ill-conditioning is NOT merely the a2=0 seed; the ℓ=2 shear block is marginally coupled at finite amplitude too.

## NEXT (Charles-gated; NOT done here — this is solver diagnosis, NOT a mechanism hunt)

The disciplined next step is to DIAGNOSE + fix the conditioning BEFORE any pin-vs-continuum reading:
- identify the near-zero mode (SVD of the Jacobian) — is it a GAUGE freedom (fix it), a scaling/normalization issue
  (rescale the shear block / the a2-vs-φ,ρ blocks), or a genuine physical soft mode (which would be the continuum
  signal, to be confirmed at higher precision)?
- try block/variable rescaling or a preconditioner (the certified `lbare_inverse` is available as a Category-A
  shear-block preconditioner — the plan wired `lbare_precondition`, unused in this pilot);
- consider float64→higher-precision or a better-conditioned shear parametrization;
- only once the solve CONVERGES (Φ→tol, cond manageable) can Outcome A/B be read for the ℓ=2 tile.

## Scope / banking discipline
- **NO Outcome A or B banked** (Charles's rule). This is Outcome **D (tool-limited)** for the ℓ=2 frozen-source tile.
- BC-fork: both non-converged ⇒ their apparent disagreement is not a physics signal; the S-Dir/S-JC2 fork verdict is
  **undetermined** (cannot be adjudicated from a non-converged run).
- Even a future CONVERGED continuum here would be B for THIS TILE only; a pin would be an A-CANDIDATE needing
  higher-ℓ + co-relaxed source + BC-fork survival.
- **Premise ledger (this run):** ξ FREE (probed), κ FREE-units, **Z_φ=8 (CHOSE — Route-A carrying the Route-B
  number)**, source = FROZEN H3-hopfion ℓ=2 sh2(r) (ledgered scoped simplification), source registration CHOSE
  (sampled at seed L0, clamped outside support), shear seal BC CHOSE-provisional (both run), ℓ=2-only SCOPED. All
  conditioning params (Nr=16, Nth=8, maxit=30, seed a2=1e-3, continuation [0.1..1.0], budget) = Category-A.
- PROVISIONAL: this is a tool-limited pilot outcome, not a verifier-banked result.
