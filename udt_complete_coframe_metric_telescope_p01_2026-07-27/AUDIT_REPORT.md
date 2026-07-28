# Complete-coframe metric telescope P01 — audit report

Date: 2026-07-27  
Status: `OBSERVED BOUNDED OFF-SHELL ATLAS; VERIFIED-WITH-EXPLICIT TRANSPORT SCOPE`

## Return

The complete triangular coframe is geometrically productive without imposing
an action or background equation.  Across the preregistered 5,120-member
family, it generically produces curvature, pair/screen mixing, causal changes
of the founded `dphi` readout, and nontrivial loop transport.

It does **not** generically collapse onto either a lightlike `phi` branch or a
repeated screen-tidal direction.  Those structures were not observed in this
generic full-dimensional sample and, if present in UDT, belong to a thinner
geometric stratum or require a still-open selector.  This is not a proof that
such strata do not exist.

## Exact bounded census

The same 1,024 scrambled-Sobol coefficient directions were evaluated on five
amplitude shells.  All eight complete-coframe amplitudes remained live.  Each
configuration was sampled on a 17 by 33 `(t,x)` grid.

| shell | local grids resolved | both timelike and spacelike `dphi` present | any registered repeated tidal point | transport resolved | nontrivial among resolved |
|---:|---:|---:|---:|---:|---:|
| 0.03 | 1,024 | 1,024 | 0 | 1,024 | 1,024 |
| 0.10 | 1,024 | 1,024 | 0 | 1,024 | 1,024 |
| 0.30 | 1,024 | 1,024 | 0 | 1,024 | 1,024 |
| 1.00 | 1,024 | 1,024 | 0 | 1,021 | 1,021 |
| 2.50 | 1,024 | 1,024 | 0 | 9 | 9 |

The local census covers 2,872,320 metric-grid evaluations.  Two shell-0.03
configurations contain one grid point each within the preregistered numerical
null tolerance; this is not a persistent lightlike branch.  No zero-gradient
point was registered.

For every one of the 1,024 coefficient directions, all three of these maxima
increase strictly through all five shells:

- scalar-curvature RMS;
- absolute Kretschmann maximum; and
- pair/screen Ricci-mixing maximum.

That is an `OBSERVED` radial organization of this bounded coefficient family,
not a physical amplitude law or probability measure.

## The orchestra pattern

The complete amplitude-norm correlation table is in `STRUCTURE_CENSUS.json`.
It is descriptive rather than causal, but it shows that no single amplitude
controls every readout:

- `phi` coefficient norm has the strongest association with the spread of its
  own causal norm, rising from Spearman 0.669 at shell 0.03 to 0.790 at shell
  2.50;
- at weak shells the longitudinal shift amplitudes `S11` and `S21` have the
  clearest individual associations with pair/screen Ricci mixing;
- at the strongest shell the angular anisotropy amplitude `alpha` has the
  clearest individual association with curvature and pair/screen mixing; and
- the associations change with shell, so the bounded map is ensemble- and
  regime-dependent rather than reducible to one universal instrument ranking.

Coefficient-norm correlation is not a functional derivative, field equation,
or selector.  It is only a coarse map of this registered orchestra.

## What did not emerge generically

The registered screen-tidal discriminant was nonzero at all 2,872,320 sampled
points.  Thus the earlier candidate of a uniquely repeated curvature direction
is not a generic algebraic identity of the complete coframe on this chart.

Likewise, every configuration crossed between timelike and spacelike `dphi`
regions on the sampled grid.  The complete coframe alone did not force a
globally lightlike `dphi` branch.

Because exact degeneracies occupy lower-dimensional sets, generic Sobol
sampling almost surely misses them.  The proper conclusion is therefore
`NOT GENERIC IN P01`, not `ABSENT FROM UDT`.

## Numerical certification and boundary

- Neutral and arbitrary constant-coframe controls are flat and have identity
  loop holonomy below `1e-10`.
- The exact determinant control holds; the worst registered relative error is
  `2.30e-10` at shell 2.50.
- An independent NumPy/finite-difference CPU implementation checked 32
  configurations at three points each without importing the GPU evaluator.
  Maximum scaled scalar-curvature disagreement is `2.12e-8` against the frozen
  `5e-5` tolerance.
- The registered 32/64/128 transport refinement reduces every shell-1.00
  error, with median second-order ratio `4.00675`.
- The primary batch-64 run used 20,687,226,368 bytes, exceeding the incorrect
  preregistered 6-GiB estimate.  A complete batch-16 replay used 5,183,212,032
  bytes.  All local features and transport-resolution identities reproduce
  exactly.  Resolved transport reproduces within `5.64e-12` scaled error.
- The original all-value replay verifier failed because it compared values
  already labeled unresolved.  That failure is preserved.  The corrected
  scope and passed verifier are separately recorded; no failed result was
  overwritten.

Transport is fully reliable through shell 0.30, reliable for 1,021/1,024 rows
at shell 1.00, and reliable for only 9/1,024 rows at shell 2.50.  Local metric
and curvature data remain batch-exact for all shell-2.50 rows.  No physical
singularity or transport structure is inferred from the 1,015 unresolved
strong-shell loops.

## Premise and scope audit

- Metric-led: **yes**, for the registered complete triangular coframe.
- Whole frame: all eight coframe amplitudes are live.
- Bounded slice: amplitudes depend only on `(t,x)` through eight frozen basis
  functions; general `(y,z)` dependence and the infinite-dimensional function
  space are not covered.
- Pair/screen split: chart-supplied and `CONDITIONAL`, not metric-selected.
- `phi`: the founded observer-pair logarithmic depth, not an extra scalar.
- Strong local CSN: inactive.
- Action, source, carrier, density, boundary law, bootstrap, and physical time
  evolution: absent and `OPEN`.
- Sobol frequency: numerical coverage only, not a physical measure.

## Four evidence gates

1. **Preregistered:** yes; numerical correction layers were committed before
   their production/replay outcomes, and both failed attempts are preserved.
2. **Full space or bounded scope justified:** bounded scope only; exact bounds
   and omitted dimensions are explicit.
3. **Independently verified load-bearing premise:** yes for coframe metric,
   determinant, `dphi` norm, scalar curvature, batch independence, and resolved
   transport.  Extreme-shell unresolved transport is excluded.
4. **Every premise audited:** yes for this package through
   `PREMISE_LEDGER.tsv` and the correction layers.

## Maximum conclusion

`OBSERVED`: in this exact bounded off-shell family, the complete coframe has a
radially ordered but genuinely mixed generic geometry.  Lightlike `phi` and a
repeated angular curvature direction are not generic identities.  P01 neither
selects a physical branch nor supplies dynamics.

The next metric-led map should deliberately cover the lower-dimensional rank
and causal strata that generic sampling cannot hit, while also releasing the
current `(t,x)` dependence to full four-coordinate local jets.  See
`NEXT_STEP.md`.

