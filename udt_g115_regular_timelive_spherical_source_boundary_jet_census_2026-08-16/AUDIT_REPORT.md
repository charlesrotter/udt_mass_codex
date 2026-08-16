# G115 audit report — regular time-live spherical source-boundary jets

Date: 2026-08-16

Base: `9e48ff70bf7ff8c4b588fe461226286f8afff34a`

Preregistration: `5c3f19ba`

Mode: exact symbolic CPU derivation plus independent numerical integration; no observation exposure,
fit, history solve, GPU, action, source dynamics, bootstrap, matter, mass, `X_max`, or selection

Status: `BLIND_VERIFIED_WITH_CAVEATS__REPAIRS_IMPLEMENTED`

## Result first

For the complete smooth central time-live spherical metric two-jet

```text
g = -N^2 dT^2 + L^2(dR+beta dT)^2 + R^2 dOmega^2,
N=1+nR^2+O(R^4), L=1+ell R^2+O(R^4), beta=bR+O(R^3),
```

one central outgoing radial observer exponential gives, with a live celestial drift `w_A`,

```text
phi_pair_fixed
  = 1/2 (ell-n+b^2-dot(b)/2+|w|^2) R^2 + O(R^3),

phi_areal
  = (ell+b^2/2) R^2 + O(R^3),

log(omega_source/omega_observer)
  = (b-q)R + (b^2/2-n+dot(b)/2-dot(q))R^2 + O(R^3).
```

Here `qR` is the supplied smooth spherical source velocity relative to the Eulerian radial frame.
Thus smooth-center parity delays terminal and areal reciprocal potentials to quadratic order, while
the complete observer–source frequency comparison can contain a linear term. These are related
channels of one supplied metric/query construction, not interchangeable definitions.

The individual coefficients `n`, `ell`, `b`, and `q` depend on the residual areal-time slicing
`T'=T+a(T)R^2+O(R^4)`. The displayed terminal, areal, optical, and frequency combinations are
invariant under its exact coefficient transformation. Physical meaning belongs to those
combinations, not to a nonzero `b` or `dot b` by itself.

The angular/mixed sector was not appended after the readout. The same pullback has

```text
C_0A = R^2 w_A,
h_AB = R^2 gamma_AB,
```

and `|w|^2/2` enters the fixed-label `phi_pair` coefficient when the label is tied to an active
instrument/transport protocol. A passive time-dependent sky relabeling is removable gauge.
Orthogonally quotienting angular directions removes the term, exposing a precisely typed reduction
choice rather than a universal scalar rule.

## Affine and phase result

Direct Christoffel reconstruction gives

```text
A_opt = 2 ell + 2 n + dot(b),
K^R   = 1 - A_opt R^2/2 + O(R^3),
R(lambda) = lambda - A_opt lambda^3/6 + O(lambda^4).
```

Spherical symmetry derives

```text
D_sky = R(lambda) I_2,
```

with zero central shear on this bounded class. The full `(J,D_KJ)` phase carrier remains symplectic
through the retained order and survives the separate exact position-caustic control.

## Source-boundary result

The source types do not collapse:

- a point event imposes `J_s=0` and generically has zero nontrivial resolved angular variation;
- a resolved screen supplies endpoint positions but no phase graph;
- a worldtube plus flow, orientation, and chosen null-normal branch can induce a phase graph after
  the ray satisfies the same zero-order phase-point boundary;
- a general regular Lagrangian boundary graph is `B_H={(x,Hx)}`, `H=H^T`.

For the spherical observer graph `Lambda(q_o)={(x,q_o x)}`,

```text
d = dim(Lambda(q_o) intersect B_H) = nullity(H-q_o I_2).
```

Therefore `d=2,1,0` according as `H=q_o I`, `det(H-q_o I)=0` with unequal matrices, or nonzero
determinant for tangent planes already placed at one admissible phase point. Rank one remains
available for anisotropic supplied source boundaries outside the exact spherical subclass.

For QW specifically, a ray with `widehat K_s!=k_s` is inadmissible at zero order; it is not a
rank-zero tangent match. Once `widehat K_s=k_s`, spherical symmetry makes the tangent match
automatically rank two.

Three source-normalized spherical observer planes have a common two-dimensional variation iff their
three scalar slopes agree. The local jet does not guarantee three rays to one source, choose a
source boundary, or select that equality.

## What this corrects

Time dependence alone does not repair the old exact P1 linear central slope by turning the regular
terminal `phi_pair` into a linear spatial profile. Instead, the complete query locates a distinct
lawful linear channel in the source-clock frequency comparison. Whether the founding reciprocal
calibration identifies observed redshift with that channel or with a derived combination remains
open and is the next type-level gate.

This result also narrows “the orchestra” without deleting it. In the central spherical chord,
screen area, phase momentum, celestial drift, radial shift, and source motion all survive. Central
shear and rank-one spherical matching are absent by symmetry, not by a frozen numerical choice.

## Numerical evidence

Production exact algebra passes 20/20 checks, including all five residual-slicing invariants. A
separate implementation uses numerical metric
derivatives, RK4 affine geodesics, an independently integrated null graph, coefficient recovery, and
direct subspace ranks. It reports:

```text
maximum coefficient relative error = 1.7205983982684353e-4
maximum null-pullback residual      = 2.220446049250313e-16
caustic symplectic defect           = 0.0
intersection ranks                  = 0,2,2,1,0 with rotation rank 1 preserved
```

All six hostile mutations are caught: deleting `dot b`, deleting celestial drift, conflating
frequency with terminal depth, deleting source motion, collapsing rank one to rank two, and deleting
the phase state at a position caustic.

`verify_package.py` reruns all three scripts, reproduces every JSON byte-for-byte, and verifies the
seven source hashes at the preregistration commit.

## Four evidence gates

1. **Preregistered:** yes, with design-stage pilot disclosure; commit `5c3f19ba` precedes the
   confirmatory implementation and outcome files.
2. **Full or bounded:** complete for the declared smooth central spherical two-jet and typed source
   boundary algebra; explicitly incomplete globally, radially, nonspherically, and dynamically.
3. **Independently verified:** the main terminal/frequency distinction, affine coefficient, null
   pullback, and rank examples have an independent executable check. The blind verifier independently
   reconstructed the remaining algebra and returned `VERIFIED_WITH_CAVEATS`. No direct Riemann
   reconstruction or independent Jacobi/QW executable was added, so full-method independence is not
   claimed.
4. **Premises audited:** yes in `TYPE_AND_PREMISE_LEDGER.tsv`, including the residual gauge,
   active/passive sky distinction, and QW zero-order gate. The repository-wide verifier passes all
   102 rows; the repository suite passes 90 tests with one documented xfail.

## Maximum conclusion

```text
REGULAR_CENTRAL_TIMELIVE_SPHERICAL_PAIR_AND_PHASE_JETS_DERIVED_CONDITIONALLY_MODULO_RESIDUAL_TIME_GAUGE
__TERMINAL_AND_AREAL_RECIPROCAL_POTENTIALS_BEGIN_QUADRATICALLY
__SUPPLIED_SOURCE_CONGRUENCE_PERMITS_A_DISTINCT_LINEAR_FREQUENCY_CHANNEL
__ACTIVE_INSTRUMENT_SKY_DRIFT_ENTERS_THE_COMPLETE_FIXED_LABEL_PAIR_PULLBACK_BEFORE_READOUT
__POINT_SCREEN_WORLDTUBE_AND_PHASE_BOUNDARY_QUERIES_REMAIN_INEQUIVALENT
__SOURCE_BOUNDARY_INTERSECTION_RANKS_ZERO_ONE_TWO_CLASSIFIED_AFTER_ZERO_ORDER_PHASE_MATCH
__CENTRAL_SPHERICAL_COMMON_BEAMS_REQUIRE_EQUAL_SOURCE_NORMALIZED_SLOPES
__PHYSICAL_HISTORY_REDSHIFT_JUNCTION_SOURCE_TRANSFER_GLOBAL_BRANCH_AND_SELECTION_REMAIN_OPEN
```

No SNe, DES, Pantheon+, P1 outcome, BAO, CMB, `X_max`, bootstrap, action, source dynamics, matter,
mass, or signalling conclusion follows.
