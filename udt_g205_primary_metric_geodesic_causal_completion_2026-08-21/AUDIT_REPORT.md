# G205 audit report — primary-metric geodesic and causal completion

Date: 2026-08-21

## Landing

```text
FULL_GEODESIC_COMPLETENESS_AND_GLOBAL_HYPERBOLICITY_SURVIVE_ALL_REGISTERED_PARAMETERS
__NULL_TRAPPING_HAS_SUBCRITICAL_CRITICAL_AND_SUPERCRITICAL_STRATA
__NO_PARAMETER_XMAX_OR_PHYSICAL_HISTORY_SELECTION
```

Grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__ANALYTIC_GLOBAL_THEOREMS__INDEPENDENT_ALGEBRAIC_CORE`

## Result first

The G204 family passes the next global test. On the declared `R x R3` realization, every timelike,
null, and spacelike geodesic is complete. The center is a smooth Cartesian point. Every geodesic
that escapes toward the reciprocal outer end requires infinite affine parameter. Trapped and
turning geodesics remain in a smooth compact region and also extend indefinitely.

The optical spatial metric is complete, making every `t=constant` slice Cauchy. The supplied
history is therefore globally hyperbolic. This property is derived for the supplied family; global
hyperbolicity is not promoted to a founding UDT postulate.

## New internal structure

Completeness does not mean every parameter produces the same causal optics. A circular null orbit
exists when `p=r phi'=-1`. For each odd order there is an exact critical amplitude. Below it there
is no circular null orbit; at it there is one degenerate orbit; above it there is a stable inner and
an unstable outer orbit. Thus the same native family has distinct trapping regimes without adding
an external mechanism.

## Precision guards

- `f>0` at every finite radius, so there is no finite-radius Killing horizon.
- The outer end lies at infinite affine, spatial, and optical reach.
- The result is not standard asymptotic flatness, maximal inextendibility, event-horizon
  classification, or `X_max`.
- Completeness and trapping do not select `n`, `r0`, `a`, the family, or a physical history.

## Evidence

- preregistration committed and pushed at `932155c1`;
- direct full-metric Christoffel and Euler-Lagrange reconstruction;
- 112/112 symbolic assertions;
- independent algebraic-core Hamiltonian/exact-rational route: 10,000 distinct cases and 150,000
  assertions;
- 80-digit finite-radius boundary diagnostics controlled by analytic inequalities;
- 17 hostile mutation catches, including false-mechanization and independence-scope guards;
- seven frozen-source hashes checked separately in live repository context;
- self-contained no-write package replay does not read outside the package;
- fresh external review retained the mathematical landing and required only evidence-label and
  replay-boundary repairs;
- external repair-only follow-up returned `REPAIRS_VERIFIED__LANDING_RETAINED` with no remaining
  evidence overclaim in the sealed intake.

The general completeness and global-hyperbolicity results are written analytic proofs retained by
external mathematical review. They are not claimed as mechanized consequences of output flags.
The finite order census is regression evidence; the displayed general-`n` derivative proof owns
the universal odd-`n>=3` quantifier.

## Maximum conclusion

G205 proves conditional geodesic completeness, global hyperbolicity, and null-trapping strata for
the exact G204 supplied family. It does not prove physical-history ownership, uniqueness, maximal
extension, observational consilience, transfer, dynamics, source, matter, signalling, or `X_max`.
