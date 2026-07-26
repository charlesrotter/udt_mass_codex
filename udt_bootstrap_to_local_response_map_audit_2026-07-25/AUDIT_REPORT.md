# Bootstrap-to-local response map audit

## Verdict

No complete bootstrap-to-local response map is derived by the current UDT
premises. The broadened bootstrap hypothesis does, however, identify the
correct general mathematical architecture: a potentially vector-valued global
closure built from native energy, density, curvature, boundary/global data,
and other metric-native observables.

The owner's tuning hypothesis needs two arrows. Let `X` be the complete
finite-cell configuration, `O` independent global data, `A(X,O)=0` the locally
admissible matter-and-geometry branches for those data, and `R[X]` the global
observables recomputed from a realized configuration. The coupled closure is

```text
A(X,O)=0,
O-R[X]=0.
```

Its exact differential contains both `D_X A + D_O A D R_X` and the full
extended constraint response. This is a
`DERIVED_CONDITIONAL_RESPONSE_SKELETON`, not a selected physical law. The
present foundation supplies neither complete arrow, the observable census,
the closure target, the coupled Jacobian, the native dual pairing, branch
regularity, nor the complete local/boundary variation domain.

The owner's second clarification sharpens this into a two-way working
hypothesis: global matter, energy, density, and curvature condition which local
matter-and-geometry branches can exist, while the realized local and macro
configuration recomputes those global quantities. Closure is where the two
directions agree. That is a coherent fixed-point *architecture*, but neither
arrow is yet complete. In the owner's intended sense this is mutual tuning or
optimization of the whole system. It does not require a scalar objective.
Scalar extremization is a narrower possible implementation and would require a
native objective or ordering, which has not been supplied.

The smallest genuinely missing object is therefore:

> a metric-native differentiable coupled global-local closure section on the
> full extended finite-cell configuration space, together with the native dual
> pairing and branch regularity that turn its derivative into a physical local
> response.

No candidate among the nine preregistered placements passes all eight gates.

## What the clarification changed

The bootstrap was initially at risk of being read too narrowly as a density
window. The owner clarification was frozen before accepting the result and
expands the admissible channels to total energy, total proper density,
spacetime curvature data, boundary/global data, observer-pair diameter or
`X_max`, holonomy/topology/angular data, and other native parameters.

This correction matters. The exact trace-free result below is a limitation of
the density projection, not a no-go theorem for a multi-observable bootstrap.
Energy, curvature, boundary, or continuous holonomy components could have
trace-free angular derivatives. Their possibility is not their derivation or
selection.

One concrete mathematical control confirms the curvature possibility without
selecting it: the bulk variation of `integral sqrt(h) R` against a trace-free
angular perturbation `H=diag(1,-1,0)` in a Ricci eigenframe is `-r1+r2`,
generically nonzero, together with a required boundary flux. This is a
candidate metric functional, not a derived UDT closure component. No analogous
energy test is possible until a native total-energy functional is defined.

## Exact results

For same-solution native total mass and proper volume,

```text
rho = M/V,
delta rho = (delta M-rho delta V)/V.
```

The proper-volume variation is trace-only in the local bulk:

```text
delta V_bulk = 1/2 integral sqrt(h) h^ij delta h_ij.
```

Both independent trace-free angular controls used in the audit—diagonal
anisotropy and off-diagonal shear—give `delta V_bulk=0`. Hence a scalar density
channel gives

```text
alpha_rho[delta h_TF]
  = eta F'(rho) delta M[delta h_TF]/V.
```

Density can therefore drive that angular channel only through a native
trace-free mass response. A non-density closure component can contribute
instead; the executable three-observable control gives

```text
alpha_angular
  = lambda_E D E_total|TF + lambda_K D K|TF
```

when the density-volume row vanishes.

A density *window* is an on-shell admissibility condition, not an Euler
equation. Interior points have no conormal response. Replacing it with an exact
level set would be a stronger, unsupplied premise and would still fix only a
conormal line, not its normalization.

A realized root or fixed point does not recover the off-shell law. The audit
constructs distinct integrable response maps with the same unique root, and
distinct fixed-point operators with the same unique fixed point but different
linearizations. Calling a configuration self-consistent is not enough to
select how it responds away from closure.

The chicken-and-egg hypothesis therefore sharpens rather than closes `R04`,
`R06`, and `R07`: it identifies the two arrows a successful bootstrap must
join, but does not define either map, its domain, or its derivative. It does
instantiate the owner's broad “tuning” meaning of optimization, but it does not
by itself supply a scalar extremization law.

Finite-cell response cannot silently freeze the seal. Even the product control
`V=A L` gives `delta V=A delta L+L delta A`; fixing the boundary deletes a
shape channel. A complete closure section must cover boundary, corner, gluing,
and global-modulus variations.

## Candidate adjudication

- `R01`, the owner-stated density-window interpretation, is entailed only as
  an on-shell filter.
- `R02-R03` provide conditional density-response formulae after adding an
  equality or varied constraint, native mass, normalization, and boundary
  data that are not currently supplied.
- `R04`, a vector complete closure section, is the correct general type after
  the owner clarification, but remains type-incomplete.
- `R05-R08` are possible representations or functional families and are not
  selected by the metric and registered premises.
- `R09` obtains a response by assuming the still-open action and reverses the
  registered action-downstream-of-closure direction.

The full gate matrix is in `CANDIDATE_RESPONSE_MAP_MATRIX.tsv`.

## Ontology and anchors

The calibrated-physical-metric and conformal-class readings remain distinct.
The former defines proper volume once a physical slice and boundary exist but
does not derive native mass or closure. The latter needs a representative or a
compensating native mass law because spatial volume scales as `Omega^3`.
Strong local Common-Scale Neutrality is challenged rather than derived, so it
cannot be used to splice the two branches.

Observed `c_E` and `G_obs` calibrate dimensions but do not select the closure
functional. They alone form neither a length nor a mass density. This does not
weaken their role as observational anchors; it limits the conclusion they can
support in this response-map audit.

## Verification and scope

- Exact production algebra: 38/38 checks, SymPy 1.14.0.
- Independent stdlib/Fraction verifier: 31/31 checks; 23 are direct algebraic
  reconstructions and eight are production/manifest/ledger integrity checks.
  It does not import the production implementation.
- Fail-closed audit verifier: 26/26 mutations rejected.
- A fresh zero-context adversarial review is recorded separately.
- Repository preservation gates, six frozen manifests, navigation, tests, and
  dirty-checkout metadata are recorded in `REPOSITORY_GATES.json`.

This audit maps one structural tile. It derives no action, matter carrier,
native energy or mass functional, topology, boundary completion, density
value, solution branch, dynamics, or physical parameter selection.

## Next bounded question

The next justified task is a preregistered, ontology-neutral census of native
global observables and their complete variations: determine which energy,
mass/density, curvature, boundary/global, diameter, and continuous holonomy
objects are actually defined by the complete metric and founded premises, and
whether those premises supply any closure relation among them. Do not choose a
target, weighting, or coupling to obtain a preferred result. Stop before dual
pairing, action reconstruction, density solving, or GPU work unless the
closure section itself is derived.
