# G77 exact derivation and numerical return

Date: 2026-08-11

## Independent equation route

G77 reconstructs the supplied G75 Cartesian metric directly. With spatial position `X`,
`s=X.X`, `A=1+a s`, `q=q(s)`, and `w=q(-Y,X,0)`, its nonzero blocks are

```text
g_00 = -A,
g_0i = g_i0 = w_i,
g_ij = delta_ij - a X_i X_j/A.
```

The production right-hand side does not import the G76 Hamiltonian or trajectory solver. It codes
the metric and all first coordinate derivatives, then solves the contracted geodesic equation

```text
g_mn du^n/dlambda = -[partial_a g_mb - (1/2) partial_m g_ab] u^a u^b.
```

At 24 preregistered algebraic control states spanning zero and strong variable-profile rows, this
contracted route agrees with a separately assembled full Christoffel tensor to
`3.552713678800501e-15`, against the frozen `2e-12` gate.

## Complete direct census

The checkpointed CPU `float64` RK4 replay evaluates:

- all `591` frozen G75 profiles;
- all `2,562` frozen level-4 directions per profile;
- all `5,120` oriented faces per profile;
- `2,048` direct-Christoffel steps per ray.

That is `1,514,142` complete trajectory rays and `3,025,920` oriented face maps. Every ray reaches
the registered first crossing. There are zero nonfinite rays, active leftovers, negative signed
faces, negative independent projected tangent maps, or faces below the `1e-2` diagnostic.

Relative to the frozen G76 Hamiltonian endpoints:

```text
590 STRONG_DIRECT_AGREEMENT       (maximum chord <= 2e-5)
  1 REGISTERED_DIRECT_AGREEMENT   (2e-5 < maximum chord <= 5e-5)
  0 CROSS_METHOD_NUMERICALLY_UNRESOLVED
```

The sole registered-tier row is `G75_AM_S03_E100`, with maximum chord
`2.0269360962840678e-05`. The full-family maximum null backward error is
`2.85631585050794e-09`, below the frozen `2e-7` gate. The maximum direct/G76 degree difference is
`3.3306690738754696e-16`.

## Four-row refinement return

G76 historically and correctly retained four rows as `NUMERICALLY_UNRESOLVED` because its frozen
Hamiltonian `512`/`1024` endpoint-chord gate was exceeded. G77 does not rewrite those historical
rows. It supplies a new direct-Christoffel `1,024`/`2,048`/`4,096` ladder:

| profile | direct 1024/2048 chord | direct 2048/4096 chord | ratio | G77 status |
|---|---:|---:|---:|---|
| `G75_A0_S03_E100` | `1.5637421621304865e-05` | `3.892176797771222e-06` | `4.017654498700914` | `DIRECT_TIME_REFINEMENT_RESOLVED` |
| `G75_AM_S03_E100` | `2.0271432044357318e-05` | `5.059526747903485e-06` | `4.006586594834623` | `DIRECT_TIME_REFINEMENT_RESOLVED` |
| `G75_AM_S24_E100` | `1.3674821355848283e-05` | `3.3501067380330906e-06` | `4.08190616752618` | `DIRECT_TIME_REFINEMENT_RESOLVED` |
| `G75_AP_S03_E100` | `1.2540672800794869e-05` | `3.2131952437718344e-06` | `3.9028667259179377` | `DIRECT_TIME_REFINEMENT_RESOLVED` |

All four have zero crossing-mask mismatch, pass the frozen `5e-5` high-resolution chord gate, and
show approximately fourfold reduction from one step doubling to the next. This is numerical
resolution under G77, not a retroactive modification of G76.

## Independent verification

`verify_artifacts_independent.py` reconstructs all `591` rows directly from the raw endpoint and
mask arrays. It independently recomputes every G76 chord, spherical degree, signed face ratio,
projected tangent orientation, and four-row refinement chord. It reproduces the exact `590/1`
census and all zero-defect counts.

`verify_panel_scipy_independent.py` does not import production equations. It uses SciPy DOP853,
full Christoffel symbols, and central finite differences of the metric. Across all eight exact G75
strata and all four former G76 exceptions, `11 x 5` rays pass. Its maximum direct-endpoint chord is
`4.7046525883627355e-06`; maximum null error is `1.5370622830079839e-10`.

Eight hostile in-memory mutations are all rejected.

## Scope

This verifies numerical-method agreement for the complete frozen G75 family under one supplied
stationary G74/G76 observer query. It remains a sampled finite-mesh result. It does not establish
continuum injectivity or select a physical profile, source, endpoint, scale, `R`, `X_max`, CMB
population, polarization law, bootstrap state, action, matter source, or observable spectrum.
