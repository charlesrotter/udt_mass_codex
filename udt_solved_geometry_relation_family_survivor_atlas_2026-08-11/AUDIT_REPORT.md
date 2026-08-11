# Solved-geometry relation-family survivor atlas

Date: 2026-08-11  
Primary landing: **`MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES`**  
Epistemic grade: **`OBSERVED`**, bounded and independently numerically verified

## What was learned

The first solved rather than purely algebraic comparison does **not** select one observer-relation
architecture. Across the complete preregistered witness set:

- all `14/14` endpoint pair constructions remained Lorentzian and regular;
- all `28/28` timelike/spacelike geodesic-deviation propagators remained regular at the registered
  affine endpoint;
- all `28/28` declared loops carried nonidentity Levi-Civita holonomy;
- all `18/18` R17 loop evaluations carried nonzero induced normal-connection angle;
- no sample was discarded, no numerical tolerance failed, and no near-conjugate stratum occurred.

The strongest structural result is therefore coexistence. On the same R17 metric family, the exact
endpoint scalar relation and nontrivial path transport both survive. They are not forced to be rival
definitions of one number. The geometry supports an endpoint “clock-depth” channel and a distinct
route-memory/angular channel at the same time.

This resolves one source of circling: a winner-take-all search between endpoint descent and path
holonomy posed the wrong question. The solved witnesses show that the metric can carry both.

## Perturbation atlas

The stationary R17 family was tested at every cross product

```text
lambda = -1, 0, +1
epsilon = -0.12, 0, +0.12.
```

The complete time-live local coframe was tested at

```text
epsilon = -0.15, -0.075, 0, +0.075, +0.15.
```

Both signs and the zero witnesses were retained. All endpoint, propagator, and path classes persisted
through those bounded changes. The values moved continuously; no branch disappeared, merged, became
singular, or became numerically unresolved in the sampled neighborhood.

This is geometric persistence, not physical or dynamical stability. Quantitative holonomy magnitude
is not ranked as “better,” because no native law has supplied such a criterion.

## Independent verification

The production implementation used adaptive `DOP853` and complex-step metric differentiation. A
separate implementation reconstructed both coframes, used centered finite differences, and integrated
with fixed-step RK4. It reproduced all `56/56` geodesic/path classifications.

Maximum independent discrepancies were:

| Quantity | Maximum discrepancy |
|---|---:|
| geodesic endpoint | `1.08e-11` |
| Levi-Civita holonomy matrix | `6.64e-10` |
| R17 normal angle | `2.11e-13` |

The independent metric/geodesic defects remained below the preregistered certification thresholds.
All `23/23` internal catch-proofs pass, including missing/duplicate-sample rejection, source-scope
guards, endpoint-presentation covariance, holonomy conjugacy, and overclaim guards.

## Honest interpretation

What survives is richer than one scalar tape. The bounded geometry contains at least:

1. an endpoint reciprocal-depth readout;
2. timelike and spacelike propagation geometry;
3. route-dependent full-coframe holonomy;
4. on R17, an additional angular normal-bundle holonomy.

That is a concrete solved version of the “orchestra” picture. It does **not** yet tell us which
combination an actual ordered observer query reads. It also does not show that the time-live local
witness satisfies a native UDT evolution law; no such law was imported or invented.

## Four evidence gates

1. **Preregistered:** yes; symbolic and numerical contracts were committed and pushed before solve.
2. **Full space or bounded scope justified:** bounded scope only, explicitly enumerated `14` samples.
3. **Independent load-bearing verification:** yes; distinct derivative and integrator families,
   `56/56` comparisons passed.
4. **Every premise audited:** yes for this bounded package; the missing physical relation owner,
   native evolution, global completion of the time-live family, and physical boundary remain `OPEN`.

Because gate 2 is bounded rather than exhaustive, the result is an independently verified bounded
observation, not a universal selection or no-go theorem.

## Next justified step

Do not make the grid merely larger yet. The useful next move is to construct a **coupled-channel
readout atlas** on these saved solved paths: retain endpoint depth, route holonomy, causal class, and
angular normal transport as separate coordinates, then test whether the founding ordered-observer
query supplies any metric-native relation among them. That test must not choose coefficients or fit a
desired regime. If no relation is metric-owned, the missing joint is sharply localized to the
observer-query/closure rule rather than to the existence or numerical regularity of the instruments.
