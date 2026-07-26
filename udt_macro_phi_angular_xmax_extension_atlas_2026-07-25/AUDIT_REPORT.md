# Macro phi–angular–Xmax extension atlas

Date: 2026-07-25

Grade: `VERIFIED_WITH_CAVEATS_BOUNDED_ALGEBRA_AND_SOURCE_LED_GLOBAL_ATLAS`

## Result

The complete coframe supports two distinct angular-modulation channels, and
they must not be conflated.

For the fixed founded clock-horizontal frame, exact inversion of the complete
spatial triangular coframe gives

```text
B=h^-1(dphi,dphi)=c1^2+c2^2+c3^2.
```

When `dphi` is aligned with the founded depth coordinate, all three angular
and all four lower base-angular extension directions leave the local result
exactly

```text
B=(p/w)^2.
```

Angular structure can nevertheless change the transverse metric and the
complete cell diameter. This is a global observer-pair distance modulation,
not a change to the local founded clock law.

When `dphi` has angular components, the angular inverse metric and the two
depth-angular shifts enter `B`. Two exact fixed-level witnesses give nonzero
differences `1/25` and `-3/80`. Hence angular structure can also modulate the
local conversion from `phi` to distance and can prevent `B` from being a
function of `phi` alone. The two clock-to-angular directions remain absent
from the fixed founded clock-horizontal spatial metric, although they change
the four-dimensional metric.

The 84-row branch atlas crosses all seven extension directions with all twelve
registered finite-cell completion classes. It contains:

| status | rows |
|---|---:|
| conditional regular FC12 interior; endpoint open | 2 |
| regular interior only; cap descent open | 28 |
| regular complement only; singular descent blocked | 7 |
| open boundary data | 7 |
| open monodromy descent | 7 |
| open mirror-lift descent | 7 |
| open nonorientable descent | 7 |
| stratum-local only | 7 |
| insufficient complete metric data | 7 |
| FC12 enlargement beyond supplied branch | 5 |

No row is newly selected or globally closed. All 84 rows explicitly retain
`Xmax` as unselected.

## Interpretation

The user's proposed macro picture survives in a precise, premise-scoped form:

`DERIVED_EXACT_BOUNDED`: the complete metric tells how angular and mixing
sectors enter the observer-rest norm of `dphi`.

`DERIVED_POSSIBILITY`: non-aligned angular structure can make the physical
distance associated with one clock depth directional or path-dependent.

`DERIVED_CONDITIONAL_WITNESS`: aligned angular structure can change the global
finite-cell diameter without changing the local radial depth law.

`OPEN`: no current UDT premise selects the angular extension, alignment,
global completion, observer comparison, or scalar feedback/profile law.

Thus this audit does not derive angular feedback into the founded `phi`
subgroup. It derives how a separately realized angular extension can modulate
the metric embedding and the global observer-pair separation.

## Consequence for Xmax

The previous local reach formula remains valid only on a transnormal branch:

```text
X_phi = integral dphi/sqrt(B(phi)).
```

This audit shows why `X_phi` cannot yet be identified with global `Xmax`:

- angular geometry can change the global diameter while leaving `X_phi`
  unchanged; or
- angular dependence can make `B` vary on a `phi` level, eliminating one
  scalar `X_phi` in favor of path/direction-dependent distances.

The smallest missing object is therefore more specific than “an angular
effect”: it is a globally descending complete-coframe branch plus its native
observer-pair comparison/connection, with enough endpoint data to calculate
the diameter or supremum. No action or density law is supplied here.

## Evidence gates

1. **Preregistered:** yes, commit `a618524`, with an append-only triangular-
   convention correction at `f64826b`, both before new atlas outcomes.
2. **Full or bounded:** complete for the `12 x 7` basis-direction cross-product
   and exact local triangular-coframe algebra; not exhaustive for nonlinear
   direction combinations, arbitrary topology, global profiles, or time-live
   solutions.
3. **Independent:** pinned SymPy 1.14 exact algebra is replayed by a separately
   implemented standard-library rational/Gauss–Jordan calculation at six
   nontrivial exact samples. Twelve fail-closed corruptions are exercised.
   The global atlas is source-led rather than independently reconstructed from
   first-principles topology, hence the caveat grade.
4. **Premises audited:** founded pair, clock-horizontal frame, coframe chart,
   alignment, angular/mixing freedom, completion/gluing, action, source,
   carrier, density, scale, and `Xmax` scopes are explicit.

Maximum conclusion:

`BOUNDED_PHI_ANGULAR_LOCAL_AND_GLOBAL_DISTANCE_MODULATION_MAP`.

No numerical `Xmax`, angular selection, cosmological prediction, action,
source, carrier, bootstrap closure, GPU work, canonization, or repository
reorganization follows.

## Repository gates

- 70 tests passed and one expected xfail;
- all six frozen packages passed, retaining 127 manifest entries and 133
  tracked paths;
- all 1,114 current artifact paths and 101 frontier targets resolve;
- the package manifest covers 23 non-self-referential files;
- the original dirty checkout retained its 55-path metadata identity and its
  contents were not read; and
- no GPU process was launched.
