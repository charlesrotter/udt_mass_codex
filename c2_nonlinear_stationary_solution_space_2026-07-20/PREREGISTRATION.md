# Conditional C2 Nonlinear Stationary Solution-Space Exploration — Preregistration

Date: 2026-07-20

Base: `786d00a05a4475fcd8495645d39ee2897f5185b3`

Branch: `codex/c2-nonlinear-stationary-solution-space-2026-07-20`

Mode: bounded CPU spectral/Galerkin candidate census with exact tensor construction and independent
residual checks

## Whole question

Inside the already frozen `UNIQUE-CONDITIONAL` pre-scale metric-only `C^2` branch and the separately
conditional reciprocal-toric smooth-cap geometry, what stationary solutions are visible when lapse,
radial/depth shape, angular squashing, and the time/fiber shift are varied together nonlinearly?

Do the parity-free, seal-even, and seal-odd metric sectors contain only the known round
coordinate/CSN orbit in the registered bounded search, or do nonround, shifted, asymmetric, or
disconnected candidate branches appear?

This is **observing**, not targeting rotation, a particle, mass, a spectrum, agreement with GR, or a
preferred seal completion.

## Whole frame and bounded tile

The unrestricted UDT question would vary all ten spacetime-metric components with genuine time
dependence, every local angular/topological sector, the physical finite-cell boundary and corner
fields, any native matter field, and the complete bootstrap conditions under a complete action.
That problem is not available because the complete action, physical boundary law, and carrier/source
remain open.

This tile uses the same conditional cohomogeneity-one coframe as the prior angular and shift audits,
now without freezing nonlinear backreaction:

```text
e0 = N(eta) d tau
e1 = H(eta) d eta
e2 = sin(eta) cos(eta) (d xi1-d xi2)
e3 = S(eta) [cos(eta)^2 d xi1 + sin(eta)^2 d xi2 + W(eta) d tau]
g  = -e0^2 + e1^2 + e2^2 + e3^2.
```

The interval is `0 <= eta <= pi/2`; both angular periods are `2 pi`. The ansatz retains the full
nonlinear metric dependence of `N,H,S,W`, including the `W^2 d tau^2` backreaction. It is only one
stationary, torus-invariant, conditional-topology tile.

## Premise, gauge, and numerical ledger

| Object | Classification |
|---|---|
| Metric is the theory | `pinned-by-THEORY` |
| Reciprocal exponential character | `DERIVED-CONDITIONAL` under the frozen sign/unit and slot premises |
| Positive CSN equivalence before physical scale | `FOUNDING` |
| Metric-only local four-dimensional `C^2` bulk | `UNIQUE-CONDITIONAL` under the frozen action-class premises; not complete UDT action |
| Reciprocal-toric coframe, angular periods, and two smooth primitive caps | `CONDITIONAL CANDIDATE PREMISES`; not derived physical UDT topology |
| Stationarity, torus invariance, and cohomogeneity one | `pinned-by-HABIT / BOUNDED SLICE`; genuine time dependence and nontoric fields omitted |
| Lorentzian sign | `pinned-by-THEORY` for the stated stationary physical comparison; positive-definite continuation is a numerical cross-check only |
| `N(eta),H(eta),S(eta),W(eta)` | `free-and-explored` in each declared spectral space |
| `e2=sin eta cos eta(dxi1-dxi2)` | coordinate plus local-CSN gauge choice on the open interval; it does not select physical scale |
| `H(0)=H(pi/2)=1` | `pinned-by` smooth primitive-cap regularity in that gauge; not a physical-wall condition |
| Smoothness of all functions as functions of `x=cos(2 eta)` | `pinned-by` the conditional smooth-cap domain |
| Constant lapse normalization | removed as a time-coordinate gauge by `N(eta=pi/4)=1` |
| Constant `W` | retained analytically as an exact coordinate orbit, then removed from numerical roots by `W(pi/4)=0` |
| Overall common scale | quotient/calibration under CSN; no numerical scale selected |
| Midpoint/seal parity | three separate sectors: unrestricted, metric-even with `W` even, metric-even with `W` odd |
| Physical finite-cell wall, boundary functional, and polarization | `OPEN / NOT SUPPLIED`; smooth caps are not identified with them |
| Carrier, section, soldering, source, `X_max`, `c_E`, `G_obs`, mass | excluded; none enters the dimensionless equations |
| Spectral order, quadrature, tolerances, seed amplitudes | category-A numerical controls, preregistered below |

No solution is rejected for being oscillatory, asymmetric, non-particle-like, high-action, or unlike
the expected answer. Roots and solver failures are characterized by raw residual, signature,
regularity representation, action, parity, and convergence only.

## Frozen candidate and sector census

1. The exact round orbit `N=H=S=1`, `W=0`, including its constant-lapse and constant-shift coordinate
   copies before gauge quotient.
2. General cap-smooth functions with no midpoint parity enforced.
3. Seal-even `N,H,S,W` functions.
4. Seal-even `N,H,S` with seal-odd `W`.
5. Nonround diagonal branches with `W=0` if they emerge; `W` is never frozen in the coupled solve.
6. Shifted branches with full `N,H,S` backreaction.
7. Midpoint-asymmetric branches in the unrestricted sector.
8. Roots found from the round seed, every single-sector seed family, and deterministic mixed seeds.
9. Root-search failures, singular Jacobians, runaway coefficient sequences, and signature loss as
   reported solver strata rather than silently discarded data.
10. Endpoint-singular local Bach branches, physical-wall interval branches, nontoric topology,
    genuine time dependence, other shifts, and other actions as explicit unsampled strata.

Coframe lifts that induce the same metric are recorded as metrically indistinguishable. A
metric-only `C^2` solve cannot rank `+I` versus `-I` coframe signs when their metric pullbacks agree.

## Numerical and algebraic contract

1. Construct the full four-metric and its inverse from the coframe at every quadrature node.
2. Construct Christoffel, Riemann, Ricci, scalar, Weyl, `C_abcd C^abcd`, and `sqrt(-g)` from metric
   derivatives; do not import reduced GR equations or a hand-written shift mechanism.
3. Verify the round branch has vanishing Weyl density and action to floating-point backward error.
4. Verify a registered nonround test profile against an independent coordinate finite-difference or
   symbolic tensor evaluation at fixed points before using the action.
5. Obtain stationarity equations by differentiating the full reduced `C^2` action with respect to
   every retained spectral coefficient simultaneously.
6. Use Gauss-Legendre quadrature with at least 48 nodes; solve spectral orders `p=2` and `p=4`, and
   attempt `p=6` only if the bounded CPU budget remains practical.
7. Use deterministic seed families: zero; signed single-sector amplitudes `0.05` and `0.20`; and at
   least eight fixed-seed mixed directions at the same two norms. Do not retune seed families after
   viewing outcomes.
8. Bound each nonlinear root attempt to 30 Newton/trust-region iterations or 60 seconds, and the
   complete pilot to 20 minutes CPU wall time. Report throughput-limited coverage rather than
   weakening the residual gate.
9. A numerical root requires raw stationarity infinity norm `<=1e-9` on its solve quadrature and
   `<=1e-7` after doubled quadrature and projection into two additional polynomial degrees.
10. A branch match across orders requires gauge-fixed coefficient/function agreement `<=1e-5` and
    residual convergence. Distinctness is descriptive: function-distance `>1e-4` after the declared
    coordinate/CSN quotient.
11. Any nonround candidate is a `REDUCED_STATIONARY_CANDIDATE` until a direct full Bach residual is
    independently checked. Failure or absence of that check forbids calling it a solution of the
    unrestricted field equations.
12. Exercise fail-closed catches for a frozen backreaction field, omitted `W^2` term, Euclidean sign
    substituted for Lorentzian, missing higher-mode validation, merit filtering, a constant-shift
    copy counted as rotation, coframe-gauge copies counted as metric selection, and a reduced root
    promoted to complete UDT physics.

## Frozen outcome branches

1. `ONLY_ROUND_COORDINATE_CSN_ORBIT_OBSERVED_IN_BOUNDED_SEARCH` — every certified reduced root in the
   registered seeds/orders is the round metric modulo declared gauges.
2. `ADDITIONAL_REGULAR_REDUCED_BRANCHES_OBSERVED` — at least one distinct cap-smooth reduced
   stationary root passes solve and higher-mode residual gates.
3. `PARITY_OR_ASYMMETRY_BRANCH_DEPENDENCE_OBSERVED` — certified root classes differ among the three
   registered sectors.
4. `SOLVER_OR_TRUNCATION_INCONCLUSIVE` — conditioning, throughput, resolution, or independent tensor
   disagreement prevents the registered certification.

Outcomes 1–3 remain observations inside this bounded conditional slice. Outcome 1 cannot exclude a
disconnected branch outside the seed/order census, endpoint-singular branch, physical-wall branch,
nontoric geometry, time-live solution, other action, or complete UDT solution.

## Certification and stop line

Pre-register, commit, implement the tensor/action engine, preserve every raw root attempt and
environment record, independently reconstruct the load-bearing residual, exercise mutation catches,
and replay repository gates. With no fresh different-model review authorization, maximum evidence
grade is `VERIFIED-WITH-CAVEATS`.

Do not select a seal completion, physical boundary condition, topology, action, carrier, scale, or
mass. Do not edit startup controls or `CANON.md`, use the GPU, launch genuine time evolution, perform
repository reorganization, or turn an unobserved branch into a no-go theorem.
