# FD1 Phase I — blind geometry return

Date: 2026-08-09
Status: `OBSERVED`, data-blind metric-slice atlas; independently verified within the stated scope
Controller: `PREREGISTRATION.md` at commit `ea05331b`

## Scope

This is the frozen Phase-I calculation required before opening any new CMB peak-width or trough
values. It samples only the RA1/RA2 equatorial stationary scalar `Box_g` probe, the SNe-conditioned
P1 exponent interval, the preregistered mixing completion, `m=-1,0,+1`, and the Dirichlet/Neumann
wall anchors. It is not a full-sphere calculation, source law, mode-population law, native UDT
dynamics, carrier derivation, or CMB explanation.

No CMB peak or trough datum is present in the derivation script or either certified atlas.

## Exact formulation

The production calculation uses the RA2 Liouville coordinate

`dx/dr = r/sqrt(A D)`, `v=sqrt(r) R`, `D=A r^2+h^2`,

and assembles the unscaled weak pencil

`K v = omega^2 M v + omega C v`.

The kinetic form is assembled as `integral (v_x-r_x v/(2r))^2 dx`; this avoids an unstable
coefficient whitening at the finite-cell wall. The finite limit-circle tail is included analytically.
The final wall condition is applied at the finite metric wall, not at a coordinate cutoff.

Mode labels are the ordered radial Sturm branches. Resolved node counts and cross-`hbar` overlaps are
diagnostics; neither is allowed to relabel an overtone merely to improve a comparison.

## Numerical return

Commands:

```text
python3 derive_phase1.py --grid 240 --output phase1_atlas_g240.json
python3 derive_phase1.py --grid 180 --output phase1_atlas_g180.json
```

Environment: Python 3.10.12; NumPy 2.2.6; SciPy 1.15.3; SymPy 1.13.1; CPU only.

Both full runs contain exactly 462 rows: `3 n values x 7 q strata x 2 wall anchors x 11 hbar
values`. The `hbar=0` rows are explicitly classified as continuum limit points and do not claim a
finite ladder.

Grid 240 internal gates: 11/11 pass.

- exact `q=0` splitting maximum absolute error: `8.366529691272717e-12`;
- maximum raw backward residual: `6.057905256433022e-10`;
- non-real eigenvalue count: `0`;
- maximum tail asymptotic contamination ratio at the join: `1.000000000000004e-06`;
- rows: `462`;
- wall-clock runtime: `287.10978746414185 s`.

Grid 180 internal gates: 11/11 pass.

- exact `q=0` splitting maximum absolute error: `2.0635715358707785e-12`;
- maximum raw backward residual: `7.459519408443124e-10`;
- non-real eigenvalue count: `0`;
- rows: `462`;
- wall-clock runtime: `117.76095843315125 s`.

Across every saved frequency, the maximum `g180`/`g240` relative drift is
`0.01881627004784847`; the median is `0.0005375674729779512`. The worst point is the deliberately
retained extreme `inv_n=0.9658, q/qcrit=-2, wall=N, hbar=1, m=0` point. Phase II must recheck every
actual classification boundary or witness at a finer grid; this whole-atlas comparison does not
pre-certify an observational transition.

## Preserved failed attempt

The first complete `g240` attempt is preserved as `phase1_atlas_failed_tail_g240.json` with its raw
transcript. It completed all rows but failed its tail-control key because the asymptotic tail was
started from a fixed fraction of the mixing crossover. Near `q/qcrit=0.95`, that is not an error
control: the crossover exponent itself becomes small.

The correction changed no metric, physical stratum, mode, wall datum, or conclusion rule. It moved
the join until the explicit ratio `A r^2/h^2` is at most `1e-6`, and then retained the analytic tail.
The failed artifact remains part of the provenance record.

## Blind geometric observation

The atlas does not support the simplistic inference “small `+m/-m` splitting means the whole
multiplet stays on the `m=0` comb.” The even-in-`m` centrifugal displacement is separately present.
Both effects become small toward the positive near-critical `q` strata and small `hbar`, while the
negative-`q` strata can remain strongly displaced even at the smallest nonzero sampled `hbar`.

This is only an `OBSERVED` structure in the bounded scalar-probe slice. It does not yet say whether
any open region fits the empirical peak basins. That question remains sealed for Phase II.

## Verification preregistration

`verify_phase1.py` is frozen before execution. It must:

1. reject malformed, partial, observationally disclosed, or internally failed atlases;
2. require full `g180`/`g240` frequency drift below 2.5%;
3. rebuild six endpoint/interior witnesses at grid 300 without importing the production script;
4. derive the metric coordinate with `solve_ivp` rather than production cumulative quadrature;
5. solve selected modes as nonlinear symmetric eigenvalue roots rather than a companion pencil;
6. require independent frequency drift below 3% and raw residual below `1e-8`;
7. require 10x and 100x cutoff changes below 0.5% on a near-critical and a negative-`q` extreme;
8. exercise catch-proofs for duplicate rows, observational disclosure, a missing multiplet member,
   a broken exact `q=0` split, and the preserved failed atlas.

No tolerance may be relaxed after viewing that verifier's output. A failed key leaves Phase I open.

## Independent verification return

The frozen verifier was executed after commit `90d6db56`; all 8/8 keys passed without modification:

- all successful atlas schemas passed and the preserved failed-tail atlas was rejected;
- maximum full-atlas `g180`/`g240` frequency drift: `0.01881627004784847`;
- 54 independently reconstructed endpoint/interior mode points;
- maximum independent frequency drift: `0.013888619300468363`;
- maximum independent raw backward residual: `5.134201512268387e-09`;
- 24 independent 10x/100x cutoff points;
- maximum cutoff drift: `2.990016002568652e-07`;
- all corruption catch-proofs passed: duplicate identity, observational disclosure, missing multiplet
  member, broken exact `q=0` split, and internally failed atlas.

The independent path did not import the production script. It used `solve_ivp` rather than cumulative
quadrature for the metric coordinate and solved scalar nonlinear symmetric eigenvalue roots rather
than diagonalizing the production companion pencil.

```text
f0b59ca9bb5ffe46fef194c092307851ad0c941abc17c973694d31b60e624429  phase1_verification.json
1fbe4722586c031b301c92c58803715ad275f3b95d2150f1602bb4fe541e019f  phase1_verification_output.txt
```

## Hashes before independent verification

```text
a7412a6e382df91cb6552c8a81b56c1cd57f6eec484a1e67036edc64e19ee5b5  phase1_atlas_g180.json
534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d  phase1_atlas_g240.json
a1fdc589f8d77790dbd838c29112f0e32e03681155f4d52a9bbb41b18c52e2de  phase1_atlas_failed_tail_g240.json
f0249178721016d990f3cd6a6b89b2b14e91d0f003a90f62c47f92faa717060c  derive_phase1.py
01f3c8e33647bf4e4b6794de33ce791bdec65f5b61491db37ff64fffb23fa7d3  verify_phase1.py
```

Maximum allowed conclusion before Phase II: a numerically certified, data-blind geometry atlas for
the stated slice, with an independently checked multiplet calculation. No empirical compatibility,
background explanation, source inference, or UDT prediction is authorized here.
