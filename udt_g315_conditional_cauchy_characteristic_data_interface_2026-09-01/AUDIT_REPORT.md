# G315 audit report

Date: 2026-09-01

## Internal bounded landing

```text
ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE
__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS
```

Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`.

## What was established

- Lawful spacelike data are `(gamma_ij,K_ij)` satisfying one Hamiltonian and three momentum
  constraints; arbitrary seed data are not automatically lawful.
- The active equation propagates the complete metric data. Lapse and shift are gauge, not selected
  physical inputs.
- The generic local remainder is four phase-space functions: two metric configuration modes and
  their initial rates. This is not a global moduli theorem.
- Bianchi makes the constraint propagation homogeneous within each connected constant-`Lambda`
  sector, conditional on the standard smooth local hyperbolic theorem already caveated in G303.
- On a regular affine twist-free null sheet, `Ric(ell,ell)=0` and Raychaudhuri contains shear but no
  direct `Lambda` term. The normalized mixed-null projection is `Ric(ell,k)=-Lambda`.
- A complete local characteristic claim requires compatible intersecting-null and corner data; one
  null sheet was not promoted to a universe.
- The pair evaluator remains downstream and adds no independent Cauchy evolution residual.

## Executable evidence

- production: 72 exact assertions and a 15-row interface atlas;
- independent: 89 exact assertions, including general non-orthonormal two-screen matrices;
- hostile mutations: 17/17 rejected;
- four exact spacelike controls and six general-screen controls;
- production and independent implementations import neither each other nor each other's results.

## Scope and remaining work

This is a regular local interface classification, not global existence, boundary evolution,
caustic control, a formalism-independent minimal characteristic-data theorem, or physical
actualization. Topology, data population, `Lambda` magnitude, scale, sources, matter/mass,
observations, physical `X_max`, and complete UDT extension remain open. Metric, kernel, angular
cancellation, and observational interfaces are unchanged.

## External adversarial review

The fresh zero-context `gpt-5.4` reviewer authenticated all 35 sealed payloads, ran the four
registered commands, reproduced five generated artifacts byte-for-byte, and independently
rederived the constraints, evolution signs, local degree count, null projections, PDE scope, and
downstream-kernel boundary. It found no scientific defect and returned:

```text
G315_ACCEPTED__CONDITIONAL_DATA_INTERFACE_UPHELD
```

Its sole provenance caveat is scope-exact: because repository access was prohibited, it could
authenticate the sealed preregistration record but could not independently reconstruct Git
ancestry. This does not alter the scientific landing.
