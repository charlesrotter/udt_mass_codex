# G290 exact screen-holonomy descent preregistration

Date: 2026-08-28
Mode: metric-led, outcome-blind exact derivation
Outcome status: `FROZEN_BEFORE_EXACT_DERIVATION`

## Whole question

On a supplied regular complete-pair network or null congruence, with the screen projection and
path-labelled screen carry already supplied by the bounded G225/G226/G274 architecture, determine
exactly what the representative metric's projected Levi-Civita connection owns.

The derivation must distinguish five jobs:

1. open-path screen-frame covariance;
2. closed-loop gauge-invariant holonomy data;
3. infinitesimal curvature recovery;
4. separation of G289's conformal metric twins; and
5. time-live transgression on a supplied loop worldtube.

It must stop before persistence, dynamics, loop population, or physical-history selection.

## Frozen construction

Let `W` be a supplied smooth relation base with a supplied immersion/carry into a smooth Lorentzian
metric history `(M,g)`. Let `S -> W` be the supplied rank-two positive screen bundle and `P_S` its
metric screen projection. Define the conditional projected connection

```text
D_X s = P_S(nabla^g_{F_* X} s).
```

On an oriented orthonormal screen frame `(e1,e2)`, use the fixed convention

```text
a(X) = g(e1, D_X e2),
Hol_gamma = exp(i integral_gamma a).
```

No connection is to be inferred from a bare one-event null line. If the supplied screen projection
or carry is insufficient for this definition, the theorem must land at that narrower boundary.

## Preregistered exact tests

1. **Oriented gauge descent.** Under a smooth `SO(2)` frame rotation by `theta`, derive the exact
   transformation of `a`; prove endpoint covariance for open carry and invariance for closed-loop
   holonomy.
2. **Unoriented gauge descent.** Under an orientation-reversing `O(2)` frame change, determine the
   exact inversion/conjugacy law. Retain only orientation-free data actually invariant under it.
3. **Curvature limit.** Derive `F_S=da` locally and the signed small-loop curvature limit, with the
   loop orientation and branch/phase-alias restriction explicit.
4. **Conformal twins.** Recompute directly from the Levi-Civita connection of
   `g_alpha=exp(2 alpha (x^2+y^2+z^2)) eta` on the registered static-clock, `z`-pair, oriented
   `x-y` screen and circle `gamma_rho`. Test the frozen whiteboard formulas

   ```text
   a = 2 alpha (y dx - x dy)
   F_S = -4 alpha dx wedge dy
   Hol_gamma_rho = exp(-i 4 pi alpha rho^2).
   ```

   Flat `alpha=0` must give unit holonomy. Nonzero `alpha` must be separable by a sufficiently small
   loop family without changing null-cone topology.
5. **Time-live transgression.** For a supplied oriented loop worldtube `C` with
   `boundary(C)=gamma_t2-gamma_t1`, derive the exact holonomy-ratio/curvature-flux relation. Verify it
   independently on `alpha(t)=alpha0+b t`.
6. **Nonselection.** Exhibit that every smooth regular `alpha(t)` satisfies the descent and
   transgression identities. No residual may be called a propagation or selection law.

## Hostile mutations that must be caught

- call open-path screen transport gauge invariant rather than endpoint covariant;
- call one oriented phase invariant under full `O(2)` gauge rather than retaining inverse/conjugacy
  data;
- flip the connection, curvature, or transgression sign without changing the frozen convention;
- call one phase-aliased loop a unique curvature measurement;
- call a bare null line a full-base screen connection;
- call transgression a conservation law or a history selector;
- import a fixed round target, action, source, boundary, observation, mass, scale, Planck cutoff,
  physical history, or `X_max`.

## Certification contract

- one explicit tensor derivation with all supplied structures typed;
- one production symbolic/exact implementation;
- one implementation-distinct standard-library replay that imports neither production code nor its
  result;
- hostile catches for every mathematical and promotion mutation above;
- current 274-row premise verifier and complete repository tests;
- fresh external adversarial review only after local banking and separate authorization.

## Candidate landings

1. `EXACT_COMPLETE_PAIR_SCREEN_HOLONOMY_DESCENT_AND_TIMELIVE_TRANSGRESSION_DERIVED_CONDITIONALLY`
2. `ONLY_ORIENTED_SCREEN_STRATUM_DESCENDS__FULL_O2_DATA_REQUIRES_REGRADING`
3. `CONFORMAL_TWIN_HOLONOMY_WITNESS_FAILS_EXACT_RECOMPUTATION`
4. `SUPPLIED_COMPLETE_PAIR_STRUCTURE_IS_INSUFFICIENT_FOR_A_SCREEN_CONNECTION`
5. `EXACT_DERIVATION_REFUTES_THE_WHITEBOARD_LEAD`

## Maximum conclusion

At most G290 may derive a gauge-covariant metric evaluator whose closed-loop data distinguish some
supplied histories and whose time-live change obeys transgression on a supplied worldtube. It may
not derive topological conservation, dynamics, an admissible-history law, physical loop/path
population, carrier matter, observation, scale, or `X_max`.
