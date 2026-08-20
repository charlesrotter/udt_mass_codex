# G186 preregistration — nonradial completed-pair channel resolution

Date: 2026-08-20

## Whole question and bounded regime

In the declared primary static-spherical UDT metric, take one supplied regular local observer-pair
germ whose clock leg and ruler leg may both have angular components. Determine whether the full
metric pullback and the accepted completed-pair normalization uniquely allocate those components
among endpoint depth, ruler density, shift, and the local orthogonal screen without an additional
scalar, fitted coefficient, regime switch, or post-readout orchestra term.

This is a metric-led, exact, local classification. It is not a finite-path Jacobi calculation, an
SNe fit, a derivation of `R(Z)`, a physical query selector, or a nonspherical ambient history.

## Frozen local query slice

Use dimension-matched time `x0=c_E t` and the primary metric

```text
g = -exp(-2 phi) dx0^2 + exp(+2 phi) dr^2 + r^2 gamma_S2.
```

At one regular event with `r>0`, supply angular vectors `w0,w1` in the unit-sphere tangent plane and
the rank-two pair germ

```text
X0 = partial_x0 + w0,
X1 = v partial_r + w1.
```

The omission of a time component from `X1` and a radial component from `X0` defines the bounded
clock/ruler query slice. It is `CHOSE_BOUNDED_QUERY`, not a general pair theorem. Every `w0,w1`
direction and every regular real `v` are characterized; no angular alignment is assumed.

Define the coordinate-covariant angular invariants

```text
A = gamma(w0,w0),  B = gamma(w1,w1),  C = gamma(w0,w1),
nu^2 = exp(2 phi) r^2 A.
```

## Premise ledger

| Item | Status | Role |
|---|---|---|
| primary static-spherical metric | `pinned-by-THEORY` | bounded ambient metric |
| full pullback before readout | `pinned-by-THEORY`, G167/G179 | orchestra ordering |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | fixes physical ruler after pullback |
| supplied `X0,X1` germ | `CHOSE_BOUNDED_QUERY` | local nonradial test input |
| angular metric `gamma_S2` and areal factor `r^2` | `pinned-by-THEORY` | angular Gram |
| numerical witnesses | `free-and-explored` | exact algebra controls only |
| extra scalar, `mu`, fit, source, transfer, `X_max` | `OMITTED/INACTIVE` | forbidden |

No `pinned-by-HABIT` physical value is admitted.

## Preregistered calculations

1. Form `h_ij=g(Xi,Xj)` without deleting any angular Gram entry.
2. Derive the exact regularity conditions `h00<0`, `det(h)<0` in terms of `A,B,C,v`.
3. Apply the completed-pair formulas only after the pullback:
   `m^2=-det(h)`, `beta=h01/h00`, and `Phi=-1/2 log(-h00)`.
4. Classify separately the effects of clock-angular norm `A`, ruler-angular norm `B`, and their
   cross term `C`.
5. Construct the ambient orthogonal-screen projector directly from `g,J,h^-1`; verify symmetry,
   idempotence, rank two, annihilation of both pair tangents, and positive screen signature.
6. Prove covariance under arbitrary rotations of the angular tangent plane and under lawful
   auxiliary ruler reparameterization.
7. Derive the two-endpoint response inside one consistent reciprocal calibration class.
8. Test exact collinear, non-collinear, static-clock, radial, zero-angular, and near-null controls.
9. Keep the G119 finite sky Jacobi map distinct from this local screen projector.

## Mutations and falsifiers

The leading landing fails if any of the following occurs:

- the direct pullback disagrees with the invariant `A,B,C` expression;
- a regular witness needs information outside `h` to compute `m,beta,Phi`;
- `B` or `C` is silently appended to `Phi` after normalization;
- the local screen projector is not a rank-two positive projector orthogonal to the pair plane;
- an angular basis rotation changes any scalar result;
- the static-clock boundary does not recover `Phi=phi` while retaining live nonradial tape data;
- production and an implementation-independent exact replay disagree;
- a local screen is promoted to a finite Jacobi/flux response;
- or any fit, profile selection, `R(Z)`, `X_max`, source, action, matter, bootstrap, or signalling
  premise enters.

## Omitted sectors

Ambient nonspherical and mixed coframes, arbitrary radial/time components on both legs, null or
degenerate pair planes, coincidence, finite propagation, caustics, multiple images, screen
connection and holonomy, physical observer/query population, global completion, native light
transfer, `R(Z)`, SNe/BAO/CMB fitting, dynamics, action, source, matter, bootstrap, mass, and
signalling are outside G186.

## Mutually exclusive landings

1. `NONRADIAL_COMPLETED_PAIR_CHANNELS_RESOLVE_WITHOUT_EXTRA_SCALAR__CLOCK_ANGULAR_NORM_CONTROLS_DEPTH__FULL_ANGULAR_GRAM_CONTROLS_TAPE_SHIFT_AND_LOCAL_SCREEN`
2. `NONRADIAL_PAIR_REQUIRES_AN_ADDITIONAL_SCALAR_OR_POST_PULLBACK_RESPONSE`
3. `NONRADIAL_REGULARITY_SCREEN_OR_COVARIANCE_FAILURE`
4. `SOURCE_CONTRADICTION_BLOCKS_CLASSIFICATION`

## Certification and maximum conclusion

Required before banking a verdict: exact symbolic production derivation; independent standard-
library rational replay sharing no production functions; at least 20,000 regular witnesses;
named exact boundary controls; executable mutation and semantic guards; source-hash verification;
current 170-row premise audit; full repository regression; and a fresh adversarial review or an
explicit pending-review caveat.

At most G186 may classify the local completed-pair channels for the supplied bounded nonradial
germ family in the primary metric. It may explain why a static radial SNe scalar can remain
unchanged while angular pair information is still live elsewhere. It may not derive a physical
observer family, finite sky response, luminosity law, `R(Z)`, or global UDT history.
