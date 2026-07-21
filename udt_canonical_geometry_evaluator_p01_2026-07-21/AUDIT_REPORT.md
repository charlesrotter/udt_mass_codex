# P01 canonical geometry evaluator — audit report

Date: 2026-07-21

Base: `7476fe32643e0e987982a4ba979aa5a4970e5858`

Status: `VERIFIED-WITH-CAVEATS`

Maximum conclusion: `GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED`

## Result

P01 is complete. The package supplies one deterministic, law-neutral evaluator for local
four-dimensional Lorentzian metric and coframe zero-, first-, and second-jet geometry. It also
supplies a conditional ten-slot `2+2` interface that retains the full base block, transverse-screen
shape, and all four mixed shifts. No action, field equation, solution-space search, boundary
completion, topology, carrier, matter source, or physical evolution was evaluated.

The evaluator is a measuring instrument for the later atlas. It prevents later algebraic and ODE
work from silently freezing the off-diagonal, angular, shift, twist, shear, or time-dependent
channels registered by the complete-metric map.

## Evaluated interface

The primary coordinate input is a finite, nondegenerate Lorentzian metric value and its symmetric
first and second derivatives in four coordinates. The primary frame input is a nonsingular coframe
and its first and symmetric second jets. The conditional split input consists of:

- three Lorentzian base-block components;
- three positive transverse-screen components, including the off-diagonal shape component; and
- four base/screen shifts.

All 10 values, 40 first-derivative channels, and 100 symmetric second-derivative channels were
exercised. The split was supplied to the software; UDT has not derived or globally selected it.

## Geometry returned

The evaluator returns metric, inverse, determinant, inertia/signature, Levi-Civita connection and
its first derivative, Riemann, Ricci, scalar curvature, metric compatibility, algebraic curvature
identities, spin connection and derivative, the first Cartan torsion identity, and second Cartan
curvature agreement. It also returns forward/reverse split reconstruction, block inverse and
determinant checks, and Common-Scale Neutrality weights and variable-scale connection bookkeeping.

The conventions are stated in `FORMULAE_AND_INDEX_CONVENTIONS.md`; these are geometric identities,
not field equations.

## Main and independent results

The deterministic main suite reports 36 passing checks. Its maximum raw residual is
`5.684341886080802e-14`, below the preregistered `2e-10` float64 tolerance. Its result/transcript
SHA-256 is:

`a2bfefe3f22c4ca18e33301baad64e45e660dc631ea0a9627e13c670b6735734`.

The independent verifier reports 15 passing checks and 33 exercised corruption catches. It uses
direct SymPy coordinate differentiation on Cartesian-flat, polar-flat, and line-product unit-sphere
fixtures; a separately written generic off-diagonal tensor contraction; exact symbolic split
determinant, inverse, and two-jet differentiation; known Cartan witnesses; and an independent
variable-conformal connection. Its maximum independent residual is
`2.220446049250313e-16`. Its result/transcript SHA-256 is:

`073213581a4ac2021ab4b6d63c64a56df29f7621d3fde8d927d6d2fe982294e0`.

## Frame, coordinate, and CSN stress tests

The main suite checks full constant linear coordinate transformations of metric value, both jet
orders, connection, curvature, and coframe round trip. It checks a coordinate-dependent local
Lorentz two-jet through metric-jet invariance, the inhomogeneous spin-connection law, and Cartan
curvature covariance. The final external reviewer added a noncommuting Lorentz-jet witness with all
reported residuals at or below `5.56e-17`.

Common-Scale Neutrality is represented only as positive local rescaling. The coframe, metric,
inverse, determinant, and volume weights are respectively `1`, `2`, `-2`, `8`, and `4`, with the
variable-scale Levi-Civita connection transformation checked independently. No physical scale
representative was selected.

## External review correction

The initial external review is preserved. Its only blocking finding came from inspecting base commit
`7476fe3`, where the separately committed P01 preregistration was necessarily absent. Its useful
coverage recommendations were incorporated. A corrected fresh read-only review from preregistration
commit `c2264f9` replayed both suites byte-identically, ran an additional noncommuting frame test,
found no blocking defect or material caveat, and returned `PASS`. See
`EXTERNAL_REVIEW_ADJUDICATION.md`.

## What remains open

P01 does not determine which local jets UDT permits. In particular, it does not:

- select a reciprocal plane or prove the supplied `2+2` split is integrable or global;
- identify signed local `phi` with any metric component;
- choose a physical CSN representative or scale;
- select a connection, action, source, carrier, boundary, or topology;
- classify degenerate, signature-changing, or global strata; or
- explore static, algebraic, ODE, time-live, PDE, or finite-cell solution space.

Those questions remain under the separate P02-and-later gates of the parent map. P02 was not
launched.

## Four banking gates

1. **Preregistered:** yes; commit `c2264f9570fe544d0b059fd6081d3f5e976f9657` precedes result banking.
2. **Full space or bounded scope justified:** yes for the P01 local evaluator interface and fixed
   regression scope; no solution space was claimed explored.
3. **Independently verified on the load-bearing premise:** yes; independent symbolic/direct
   implementations, 33 catches, and a corrected fresh external review all passed.
4. **Every premise audited:** yes for the 16-row P01 status ledger and 15-row source/coverage ledgers;
   the split, `phi` join, dynamics, scale, boundary, and global questions remain explicitly open.

Verdict: `VERIFIED-WITH-CAVEATS / GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED`.
