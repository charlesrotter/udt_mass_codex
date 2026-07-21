# Complete-seal fixed-set and orientation selector audit — preregistration

Date: 2026-07-21

## Frozen question

Does the established UDT finite-cell seal have enough geometric meaning to select one of the four
registered complete angular lifts? In particular, is it a pointwise fixed codimension-one spatial
mirror, an orientation-preserving codimension-two involution, a codimension-three time-axis
involution, or only an invariant scalar-depth locus with an unresolved angular identification?

This audit tests the first missing join from the metric-native two-pair selector package. It may not
prefer a reflection lift because that lift supports the conditional two-pair/Hopf correspondence.

## Base and scope

- base: `a0e928890ed2966d3f2defcd493ee4c14b9fde5f`;
- computation: bounded CPU-only exact linear algebra and fixed-set geometry;
- covered data: the conditional Lorentzian base seal, its derived local clock/radial causal
  eigendirections, all four registered angular lift classes, determinant/orientation, fixed and
  anti-fixed multiplicities, metric orthogonal normal/tangent decomposition, and the exact current
  finite-cell wording;
- covered interpretations: pointwise fixed hypersurface, invariant-but-not-pointwise-fixed
  hypersurface, angular quotient/identification, and smooth doubled-manifold chart transition;
- covered metric coupling: zero-cross canonical representatives and registered exact nonzero-cross
  witnesses.

Not covered: choosing an action, boundary functional, cap, period, topology, carrier, bulk transport,
holonomy reduction, matter source, mass, scale, GPU work, or canonization.

## Premise ledger

| Item | Stamp | Role |
|---|---|---|
| Static seal scalar datum `phi=0` with odd reciprocal parity | `pinned-by-THEORY` | Established finite-cell boundary datum |
| Conditional Lorentzian mixed base and seal-local clock/radial soldering | `CONDITIONAL_DERIVED` | Supplies fixed timelike and reversed radial lines |
| Complete angular seal lift | `OPEN` | Object under selection audit |
| Seal is a pointwise fixed codimension-one hypersurface | `TO_BE_SOURCE-AUDITED` | If established, tangent/normal theorem may select a lift |
| Seal merely preserves the `phi=0` locus setwise | `free-and-explored` | Allows angular action without pointwise fixation |
| Four-dimensional orientation | `free-and-explored` | Must not be confused with orientation of the gluing transition |
| Time orientation | `free-and-explored` | Test against the derived fixed timelike base line |
| Hopf/toric/carrier geometry | `EXCLUDED_AS_SELECTOR_INPUT` | May be compared only after adjudication |

## Preregistered lift census

With the normalized base seal having one `+1` and one `-1` direction, test exactly:

1. angular `+I`;
2. angular `-I`;
3. angular axis reflection `diag(+1,-1)`;
4. local angular Hopf exchange `J`, which is locally conjugate to a reflection.

For each record:

- full determinant and orientation action;
- full fixed/anti-fixed multiplicities;
- spatial fixed/anti-fixed multiplicities after the fixed timelike line is removed;
- local fixed-set codimension if realized by a smooth involutive isometry;
- whether it is compatible with a pointwise fixed boundary hypersurface;
- whether it admits the seal-local complementary reciprocal pair from the parent audit; and
- what additional global/angular identification it requires.

## Exact geometry contract

For a smooth involutive isometry `R` at a fixed point:

1. `T_p Fix(R)=ker(R-I)`;
2. its metric normal space is the `-1` eigenspace;
3. local fixed-set codimension equals `dim ker(R+I)`;
4. the derivative determinant is `(-1)^(anti-fixed dimension)`; and
5. a pointwise fixed codimension-one spatial mirror that preserves time has multiplicity `3/1` in
   four-dimensional spacetime.

These reference facts classify a supplied geometric interpretation. They do not prove that the UDT
word “seal” has that interpretation.

## Preregistered falsifiers

A lift is not selected if:

- selection uses the word “mirror” without proving pointwise fixation of all tangential directions;
- four-dimensional determinant sign is treated as physical orientation preservation without
  separating the involution from an oriented-double chart transition;
- time orientation alone leaves multiple lifts;
- nonzero cross terms change coordinates but not the fixed/anti-fixed multiplicity;
- a reflection lift requires an angular quotient or fixed-set codimension not supplied by current
  finite-cell authority;
- the Hopf match, carrier stability, or desired second pair supplies the reason for choosing it; or
- the result silently identifies an invariant hypersurface with a pointwise fixed hypersurface.

## Certification contract

Acceptance requires:

1. exact eigenvalue, determinant, rank, signature, and conjugacy calculations for all four lifts;
2. a source-level distinction between pointwise fixed, setwise invariant, and quotient language;
3. nonzero-cross witnesses proving multiplicity and causal meaning are basis-independent;
4. explicit comparison of the involution orientation with oriented gluing/doubling semantics;
5. an independent standard-library rational reconstruction and exercised overclaim catches;
6. no use of Hopf/carrier merit in selection; and
7. repository, frozen-manifest, tests, navigation, and dirty-checkout gates.

## Maximum allowed conclusion

`UDT_COMPLETE_SEAL_FIXED_SET_SELECTOR_STATUS_CHARACTERIZED`.

Possible returns:

- `PLUS_IDENTITY_SELECTED_CONDITIONAL_ON_POINTWISE_CODIMENSION_ONE_SEAL`;
- `REFLECTION_CLASS_SELECTED_CONDITIONAL_ON_A_SEPARATELY_DERIVED_ORIENTATION_LAW`;
- `COMPLETE_LIFT_REMAINS_OPEN_BECAUSE_SEAL_POINTWISE_ACTION_IS_UNDERDETERMINED`; or
- a narrower exact combination of these.

No bulk two-pair law, topology, action, matter, or canon conclusion may follow.
