# P01 canonical geometry evaluator — preregistration

Date: 2026-07-21

Base: `7476fe32643e0e987982a4ba979aa5a4970e5858`

Authority: Charles explicitly authorized `P01` after accepting the complete-metric map.

## Frozen question

Can a single law-neutral local evaluator represent an abstract four-dimensional Lorentzian coframe
and all ten slots of the conditional `2+2` metric bookkeeping—with arbitrary first and second
derivatives in all four coordinates—and correctly reconstruct inverse, determinant, signature,
Levi-Civita connection, curvature, Cartan identities, and Common-Scale Neutrality weights?

This evaluates local zero-, first-, and second-jet geometry. It does not explore or classify the jet
space (`P02`), solve an equation, select an action, impose a boundary, establish topology, or run a
time evolution.

## Frame and premise ledger

- `pinned-by-THEORY`: four-dimensional conditional conformal-Lorentzian metric readout; Common-Scale
  Neutrality; founding reciprocal clock/ruler structure as provenance only.
- `CONDITIONAL_BRANCH`: a supplied Lorentzian reciprocal/base two-plane and positive transverse
  screen used solely for the general `2+2` software interface.
- `free-and-explored`: all ten slot values, every first derivative, every symmetric second derivative,
  coframe values/jets, frame/coordinate gauges, and conformal factor/jets in the evaluator domain.
- `pinned-by-HABIT / BLOCKED`: staticity, diagonality, zero shift, zero twist, zero shear, round screen,
  areal gauge, spherical/axial symmetry, and any preferred `phi`-slot identification.
- `COMPARISON_READOUT_ONLY`: named flat and curved geometries used only as regression fixtures.

No action, EOM, source, carrier, mass, physical scale, finite-cell completion, GR field equation, or
empirical target enters.

## Canonical representations

1. **Primary whole-frame input:** coframe value, first jet, and symmetric second jet. The metric is
   reconstructed as `g = e^T eta e`; local Lorentz transformations are representation changes.
2. **Primary coordinate-jet input:** symmetric nondegenerate metric value plus first and symmetric
   second coordinate derivatives at one point.
3. **Conditional `2+2` input:** base block `h_ij`, positive screen `q_AB`, and four shifts `A^A_i`,
   totaling ten independent slots. The interface uses
   `ds^2 = h_ij dx^i dx^j + q_AB(dy^A + A^A_i dx^i)(dy^B + A^B_j dx^j)`.
   This is complete component bookkeeping conditional on a supplied split, not a derived UDT split.

## Required evaluator outputs

- metric, inverse, determinant, inertia/signature, and inverse/determinant residuals;
- Christoffel connection and its first derivative;
- Riemann, Ricci, scalar curvature, and curvature symmetry/Bianchi residuals;
- coframe-derived metric jets, spin connection, its derivative, Cartan torsion, and agreement between
  the second Cartan curvature and coordinate Riemann curvature;
- forward/reverse `2+2` reconstruction and determinant-factorization residuals;
- CSN/conformal weights for coframe, metric, inverse, determinant, and volume, plus the exact
  Levi-Civita connection transformation using the gradient of `ln Omega`;
- machine-readable provenance, status, shapes, checks, and raw residual maxima.

## Independent regressions

The main evaluator will use explicit array/tensor formulas. An independent SymPy implementation
will differentiate named coordinate metrics directly and compare point jets and invariant outputs for:

1. Cartesian flat spacetime;
2. flat spacetime in a nontrivial polar/cylindrical chart, requiring nonzero connection but zero
   curvature; and
3. a purely geometric line product with a unit two-sphere, requiring nonzero known curvature.

These fixtures are mathematical readouts only and may not select fields or dynamics.

## Certification and catch contract

Acceptance requires, at float64 tolerance `2e-10` unless an exact SymPy equality is available:

1. exact shape/symmetry validation and Lorentzian inertia;
2. all ten slots change the reconstructed metric somewhere;
3. every slot's first and second jets in each of four coordinates propagate to the corresponding
   metric jets—40 first-jet and 100 symmetric-second-jet channels;
4. `2+2` reverse reconstruction, block inverse, and determinant factorization;
5. metric compatibility, torsion-free first Cartan equation, Riemann antisymmetry/pair symmetry,
   first Bianchi identity, Ricci symmetry, and second Cartan agreement;
6. local Lorentz coframe invariance and invertible coordinate reconstruction;
7. exact constant-CSN weights and variable-CSN connection transformation;
8. agreement with the independent SymPy regressions; and
9. exercised fail-closed mutations for omitted slot, omitted coordinate derivative, asymmetric jets,
   wrong inverse, wrong connection sign, wrong curvature sign/index order, broken first/second Cartan
   identity, broken CSN weight, failed gauge reconstruction, and conditional split promotion.

Stop on any missing channel, identity failure, independent-regression mismatch, or reconstruction
failure. No tolerance may be loosened after seeing an outcome.

## Compute bound

CPU only. Exact symbolic regressions and small fixed-size array tests only; expected runtime under two
minutes and memory under 2 GiB. No parameter sweep, ODE, PDE, GPU process, or long solve.

## Maximum conclusion

`GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED`

Even a fully passing evaluator does not derive a reciprocal plane, choose `phi`, select dynamics,
characterize solution space, establish global geometry, or produce UDT matter.
