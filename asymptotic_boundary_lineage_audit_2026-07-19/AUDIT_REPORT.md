# Asymptotic-boundary lineage audit

Date: 2026-07-19

Base: `85a0363b2bef9a1cfb0149dc1aaf20bcd44e1bd8`

Compute: CPU-only exact algebra and repository-evidence audit; no GPU

## Result first

The repository did not contain one boundary under several names. It contained several physically
different objects.

The recorded CMB/finite-cell outer fold and the WR-L wall are **derived distinct within their stated
models**:

| quantity | CMB outer fold | WR-L wall |
|---|---:|---:|
| `phi` | `0` | tends to `+infinity` |
| `A=e^-2phi` | `1` | tends to `0` |
| clock factor | `1` | tends to `0` |
| reciprocal radial ruler | `1` | tends to `+infinity` |
| recorded character | mirror/quotient boundary with non-null normal | regular null causal horizon |

Thus the CMB fold is not the clock-dilation asymptote. The WR-L wall is the actual recorded metric
asymptote: finite proper room, infinite optical reach, vanishing static clock rate, divergent local
radial ruler factor, and finite wall curvature.

The WR-L wall is nevertheless **not derived to be the hard end of spacetime**. Its ingoing metric is
regular and admits crossing curves. It can consistently delimit a static observational or causal
domain without being a terminal manifold boundary. Whether UDT's global bootstrap chooses that
domain—and thereby identifies its supplied `X` with the unknown global `X_max`—remains `OPEN`.

No post-July native derivation was found for mass dilation at either surface. The familiar wall
readout `c_E^2 X/(2G_obs)` is Misner-Sharp/GR reference structure, not native UDT mass. The metric
does supply an exact raw lapse flux `-2*pi*X`, but a raw metric flux is not a mass until a complete
action fixes the generator, normalization, reference, orientation, and boundary term.

## What is genuinely promising

The owner hypothesis is coherent in a sharpened form:

1. ordinary-regime `c_E` and `G_obs` are accepted observational anchors;
2. a complete UDT solution must derive a normalized native total-mass functional;
3. a boundary/bootstrap equation must select the global branch and `X_max`; and
4. at least one of those native structures must break the common rescaling
   `M_tot -> lambda M_tot`, `X_max -> lambda X_max`.

If those independent equations exist, they can select dimensionless universe data and `c_E,G_obs`
can calibrate it into an absolute total mass and length. If the mass law only says
`M_tot proportional to X_max`, then `c_E,G_obs` determine only the mass-per-length conversion and
the absolute pair remains free.

This is not a negative result. It identifies the exact missing content: **not another dimensional
formula, but a native scale-selection eigenvalue or homothety-breaking closure supplied by matter,
the boundary, or their bootstrap**.

## Exact metric audit

For the recorded WR-L representative

```text
A(r) = 1-r/X,
phi(r) = -log(A)/2,
0 < r < X,
```

the independent calculation gives:

- proper radial reach: `2X`;
- proper static volume: `64*pi*X^3/15`;
- optical/tortoise reach: infinite;
- Ricci scalar at the wall: `6/X^2`;
- Kretschmann scalar at the wall: `8/X^4`;
- raw wall lapse flux: `-2*pi*X`;
- ingoing radial-block determinant at the wall: `-1`.

The finite invariants and regular ingoing block distinguish a horizon from a curvature singularity.
The `r=0` seat is instead curvature-singular if this macro profile is extrapolated globally, so the
static patch is not yet a complete universe solution.

The power-family selector rerun also reproduces the conditional WR-L exponent: finite proper reach
requires `alpha<2`, infinite optical reach requires `alpha>=1`, and the recorded finite second-
derivative condition in `1<=alpha<2` leaves `alpha=1`. This selects the profile within the stated
axioms; it does not select the value of `X` or a global domain.

## Surface rulings

- `CMB_FOLD`: conditional mirror fold with ordinary lapse; not the WR-L wall.
- `WRL_WALL`: exact regular null horizon of the supplied static profile; strongest recorded
  candidate for an observational/causal `X_max`, but not yet global or terminal.
- `WRL_SEAT`: `phi=0` normalization point but a curvature singularity under global extrapolation;
  not the CMB fold merely because `phi` matches.
- historical hyperbolic `x=X tanh(phi)` endpoint: compatible endpoint asymptotics, but its `X` was
  supplied and its physical-distance interpretation has been withdrawn.
- H3 numerical boundary: computational box only.
- `GLOBAL_XMAX`: frame-shared unknown output; no derived metric surface or numerical value yet.
- complete differentiable boundary: action, allowed variations, primitive, and normalized charge
  remain open.

The full pairwise record is in `SURFACE_IDENTITY_MATRIX.tsv`; individual limits are in
`QUANTITY_LIMIT_LEDGER.tsv`.

## Mass and scale closure

The noncircular unknown/equation count is in `GLOBAL_CLOSURE_EQUATION_LEDGER.tsv`. In compact form:

```text
known:    c_E, G_obs
unknown:  selected dimensionless state, common scale, X_max, slice/volume,
          native M_tot, boundary ontology/charge
needed:   native mass functional + global boundary/bootstrap equation
          + an absolute scale selector (possibly contained in either one)
```

The often-written relation

```text
X_max = alpha G_obs M_tot / c_E^2
```

contains one equation for `X_max`, `M_tot`, and the presently underived dimensionless coefficient
`alpha`. It becomes useful after `alpha` and `M_tot` have native definitions; it cannot create them.

The exact flux `-2*pi*X` is a concrete geometric lead because it is finite and linear in the same
scale. It could become part of a boundary generator in a complete action. Calling it mass now would
silently import the missing normalization and is therefore rejected by an exercised catch-proof.

## Provenance ruling

The census froze 1,061 candidate sources: 67 load-bearing, 99 context-only, 88 duplicate snapshots,
350 negative controls, and 457 excluded with reason. All 67 load-bearing sources were individually
adjudicated. Pre-July-1 material was used only to expose failures, conflicts, or historical lineage;
it supplied no affirmative UDT physics.

The seven available bounded historical algebra packages were rerun successfully. The independent
implementation then reproduced 24 exact limit/algebra checks. A separate verifier recomputed the
WR-L curvature from Christoffels and Riemann contraction and exercised 12 fail-closed mutations.

The preregistered fresh-context model review was not transmitted: the external-service disclosure
gate correctly required separate user authorization. `EXTERNAL_REVIEW_PROMPT.md` records the frozen
challenge and `EXTERNAL_REVIEW_TRANSCRIPT.txt` records the blocked launch. No workaround was used.
Consequently this package is banked as `VERIFIED-WITH-CAVEATS`, not `SETTLED`.

## Four evidence gates

1. **Preregistered:** yes, commit `1c5354c` before source adjudication or derivation.
2. **Full space or bounded scope justified:** yes for the recorded static WR-L/fold lineage; no claim
   about all time-live or matter-bearing solutions.
3. **Independently verified on the load-bearing premise:** yes by a separate direct tensor/limit
   implementation; fresh-context model review remains unexecuted pending disclosure authorization.
4. **Every premise audited:** yes for this bounded audit, with action, source, carrier, global
   domain, angular/time-live sectors, and native mass explicitly unprovided.

## Maximum conclusion and next scientific seam

Bank this as `VERIFIED-WITH-CAVEATS`:

> The recorded CMB fold and WR-L wall are distinct. The WR-L wall is a finite-proper/infinite-optical
> regular causal horizon and is a plausible candidate for an observational `X_max`, but neither its
> global selection nor a native mass relation is derived. Known `c_E` and `G_obs` can determine
> absolute total mass and `X_max` only after native matter/boundary/bootstrap structure supplies an
> independent scale selector.

The bounded next question is whether the exact WR-L boundary flux and complete matter-bearing
finite-cell geometry furnish a native normalized generator plus a scale-breaking bootstrap
condition. That is a new audit/derivation and is not launched here.

No canonization, complete action, mass theorem, numerical `X_max`, GPU result, or boundary ontology
is claimed.
