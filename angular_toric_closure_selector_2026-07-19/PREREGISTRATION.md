# Angular–Toric Closure Selector Audit — Preregistration

Date: 2026-07-19
Branch: `codex/angular-toric-closure-selector-2026-07-19`
Base: `cc7b08381281fa104661df5b6af9fb030cabac95`
Mode: CPU-only, metric-led, bounded analytic classification

## Whole question

The preceding frozen audit found an exact compatibility witness: in a supplied toric realization,
the determinant-normalized Hopf-orbit block is exactly
`diag(exp(-2 phi), exp(2 phi))`, and its angular–`phi` mixed connection has nonzero trace-free
shear. This audit asks the next, narrower question:

> Do registered Reciprocity, Common-Scale Neutrality, finite-cell structure, and bootstrap closure
> select the two periodic spatial angular slots, their global torus closure, the primitive `S3`
> endpoint caps, and the free diagonal/anti-diagonal circle action—or do admissible countermodels
> keep any of those choices open?

This is an observation/classification audit, not a search for a Hopfion. It must enumerate the
toric closure family and record what the registered principles eliminate without rewarding `S3` for
being familiar or useful.

## Bounded geometry

The candidate class is a cohomogeneity-one positive spatial three-geometry on its principal-orbit
region,

```text
h = U(phi)^2 dphi^2 + G_ij(phi) dxi^i dxi^j,
xi in R^2 / (2 pi Z^2),
```

with a possible integral change of torus basis. The exact reciprocal diagonal orbit block is tested
as a `WORKING_CANDIDATE` realization,

```text
G = Omega(phi)^2 diag(exp(-2 phi), exp(2 phi)),
```

not assumed to be a universal consequence of C0/C1. General primitive collapse cycles, non-round
radial/common-scale functions, finite cylinders with boundary, and off-diagonal cap/gluing data are
retained as countermodel classes. The angular period `2*pi` is a coordinate/lattice normalization,
not a derived physical length.

## Premise ledger

| Item | Status entering this audit | Treatment |
|---|---|---|
| Reciprocal exponential comparison pair | `DERIVED` under exact C0/C1 premise stamps | Frozen; no reassignment of the founding temporal/parallel slots is permitted. |
| Positive Common-Scale Neutrality | `POSTULATE` | May remove positive common scale only; it cannot cross a zero-scale cap or supply missing boundary data. |
| Four-dimensional conformal-Lorentzian readout | `INHERITED / CONDITIONAL` | Used only to preserve type distinctions; not promoted. |
| Two periodic spatial angular slots | `WORKING_CANDIDATE / OPEN` | Tested, never treated as foundation-derived. |
| Torus basis and primitive collapse cycles | `FREE-AND-EXPLORED` | Enumerate by the integral lattice and determinant class. |
| Full `phi` range and endpoint collapse | `FREE-AND-EXPLORED` | Include compact caps, finite boundary cylinders, and incomplete/noncompact alternatives. |
| Common scale `Omega` and radial coefficient `U` | `FREE-AND-EXPLORED` | Construct round and non-round smooth witnesses; no preferred function is targeted. |
| Circle generator `(m,n)` | `FREE-AND-EXPLORED` | Classify effective/free and exceptional-orbit actions. |
| Finite-cell mirror rule for `phi` | exact C1 static seal premise | Test only its actual parity/boundary content; do not invent angular swapping or cap data. |
| Bootstrap | `ON_SHELL_CLOSURE_OR_ADMISSIBILITY` | Test whether its registered wording ranks topology or completion; do not turn survival into a new equation. |
| Carrier, action, source, mass, time-live law | `OPEN` or `POSIT / CONDITIONAL` | Excluded from selection input and from maximum conclusion. |

No `pinned-by-HABIT` physical boundary, topology, preferred axis, circle action, or round metric is
allowed. Smoothness and integral-lattice algebra characterize candidate geometries; they do not
constitute UDT selection by themselves.

## Candidate families

1. `FINITE_TORUS_CYLINDER`: no collapse; principal torus orbits end on one or two finite boundaries.
2. `SAME_CYCLE_TWO_CAP`: the same primitive circle collapses at both ends.
3. `PRIMITIVE_DET_ONE`: distinct primitive cycles with absolute determinant one.
4. `PRIMITIVE_DET_P`: distinct primitive cycles with absolute determinant `p>1`.
5. `NONPRIMITIVE_ORBIFOLD`: a nonprimitive collapse or ineffective circle action.
6. `ROUND_S3_WITNESS`: the previously derived round completion.
7. `NONROUND_S3_WITNESSES`: smooth mirror-symmetric completions with the same normalized orbit block
   but a different CSN-invariant radial/orbit ratio.
8. `WEIGHTED_CIRCLE_ACTIONS`: primitive `(m,n)` actions, including free `|m|=|n|=1` and actions with
   exceptional stabilizers.

The audit may refine this bookkeeping after literal source census, but it may not discard a family
because it fails to resemble the desired carrier.

## Exact tests

A runnable independent algebra script must check at least:

1. every positive diagonal two-orbit block becomes `diag(F/G,G/F)` after determinant normalization;
2. `phi=(1/2) log(G/F)` realizes the reciprocal block wherever `F,G>0`;
3. primitive endpoint cycles `v_-`, `v_+` have lattice quotient controlled by
   `p=|det(v_-,v_+)|`, with explicit `p=0,1,3,5` mirror-compatible examples;
4. opposing coordinate-axis collapses give `p=1`, while mirror exchange alone does not;
5. round and explicit non-round, mirror-symmetric smooth `S3` completions have the same normalized
   reciprocal orbit block;
6. the non-round witness is not positively conformal to the round full three-metric because a
   scale-invariant radial/orbit ratio differs;
7. cap regularity and primitive periods hold for both witnesses;
8. a weighted action on `(z1,z2)` is free at both exceptional circles only if
   `|m|=|n|=1`; other nonzero weights have finite stabilizers;
9. the metric-dual connection for the free diagonal/anti-diagonal actions cancels common angular
   scale and reproduces the conditional unit classes;
10. finite `phi` intervals with positive orbit coefficients have no forced cap and remain valid
    local/bounded countermodels unless a separate boundary law excludes them.

The source verifier must separately confirm the exact C1 boundary scope, CSN positivity scope,
bootstrap status, and founding slot/type caveat from base-pinned source bytes.

## Adjudication rules

- `S3_SELECTED` is permitted only if registered UDT premises force the spatial torus slots, full
  range, primitive opposing eigen-circle collapses, determinant-one gluing, and cap regularity.
- If those facts force `S3` only after being separately supplied, record
  `S3_UNIQUE_CONDITIONAL_WITHIN_TORIC_CAP_PREMISES`.
- If mirror exchange permits more than one determinant class, mirror symmetry does not select the
  topology.
- A free smooth `S2` quotient may conditionally select weight magnitudes `|m|=|n|=1`; it does not
  establish that UDT requires such a quotient.
- Positive CSN may remove an interior common factor but may not be extended through a vanishing
  determinant representative without explicit completion data.
- Bootstrap cannot select by semantic appeal. A ranking, exclusion, or closure equation must be
  present in its registered wording.
- No local compatibility, regularity theorem, or convenient global topology may be relabeled as
  carrier emergence or action selection.

## Falsification and catch-proofs

The verifier must reject at least:

- treating the founding temporal/parallel pair as two periodic spatial circles;
- promoting the angular torus ansatz to C0/C1-derived;
- claiming mirror exchange forces determinant one;
- omitting a determinant-`p>1` or finite-boundary countermodel;
- treating smoothness as uniqueness of the round metric;
- treating positive CSN as valid through a zero-scale cap;
- calling a weighted action free when either weight has magnitude greater than one;
- promoting conditional quotient uniqueness to a UDT-selected carrier;
- importing the existing `L2+L4` action or static soliton as a selection criterion;
- assigning bootstrap a topology-ranking law absent from its source.

## Completeness map and exclusions

This is one bounded kinematic/global-geometry tile. It covers domain/topology/boundary alternatives
inside a toric three-geometry candidate. It does not solve the full four-metric, vary fields, derive
an action, determine a source, explore time-live branches, establish stability, or compute mass.
Off-toric spatial geometries remain outside this bounded class and prevent a universal metric-space
uniqueness claim.

## Maximum allowed conclusion

The audit may classify:

- whether `S3` is selected, merely unique-conditional inside explicitly supplied toric cap premises,
  or globally underdetermined;
- whether smooth free circle quotient conditions reduce `(m,n)` to diagonal/anti-diagonal choices;
- the smallest still-missing selector after all registered principles are applied.

It may not adopt a toric universe, carrier, boundary, action, source, mass law, time-live completion,
or canon statement.

## Evidence and stop gates

- Preserve base-pinned source inventory, complete candidate/status tables, exact scripts, raw
  stdout/stderr, fresh adversarial review, and a SHA-256 package manifest.
- Run CPU only.
- Replay frozen manifests, repository test baseline, current paths/links/frontier targets, and the
  original 54-path dirty-checkout metadata without reading dirty contents.
- Commit and push the isolated audit branch, then stop before startup integration, `grok`
  advancement, time-live work, action construction, GPU work, canonization, or reorganization.
