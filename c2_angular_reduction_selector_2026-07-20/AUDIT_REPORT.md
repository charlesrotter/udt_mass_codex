# Conditional C2 Angular-Reduction Selector Audit

Date: 2026-07-20  
Base: `dc9aafa2d92db30594eafd28c50f99963472b61d`  
Preregistration commit: `ed2aa9c`  
Mode: CPU-only exact metric curvature, reduced variation, and full Bach-equation audit  
Status: **VERIFIED-WITH-CAVEATS** — exact derivation, an independently written coordinate-Ricci and
sectional-curvature implementation, base-source replay, and exercised fail-closed catches pass; no
fresh external-model review was authorized.

## Result first

The dimensionless metric equations select the round angular geometry in one important but explicitly
conditional branch.

For the static product representative

`g4 = epsilon_t d tau^2 + g3`

and the conditional reciprocal-toric spatial metric

`g3 = b^2[H(eta)^2 d eta^2 + cos^2(eta)sin^2(eta)d delta^2]`
`     + a^2[cos^2(eta)d xi1 + sin^2(eta)d xi2]^2`,

define `s=a/b`, `q=sin(eta)cos(eta)`, and `k=q'/q`. Exact curvature algebra gives

`C4^2 = 4/(3 H^4) [(k H'/H + 4(1-s^2))^2 + 3s^2(H'/H)^2]`.

This is a sum of squares. Its zero-Weyl branch requires

`H'=0`, `s=1`.

The unit smooth-cap slopes then give `H=1`.

More strongly, this is not merely a minimum chosen by hand. The full product Bach equation contains

`B_00 = -epsilon_t[Delta_3 R3/12 + |Ric3_TF|^2/4]`.

On a smooth compact capped `S3`, the Laplacian integrates to zero. Therefore `B_00=0` forces the
trace-free spatial Ricci tensor to vanish everywhere. In three dimensions that means constant
sectional curvature. Within the stated positive reciprocal-toric family, the only such branch is
again

`H=1`, `s=1`.

The exact verdict is:

`CONDITIONAL_ROUND_ANGULAR_SHAPE_SELECTION_IN_COMPACT_STATIC_PRODUCT_C2_SLICE`.

This does **not** yet select the physical scale `b`, derive the toric spatial realization, identify
the mathematical caps with the physical finite-cell boundary, or solve the time-live coframe.

## Lay interpretation

We allowed the candidate angular three-sphere to be stretched in two independent ways:

- its depth direction could have any smooth shape `H(eta)`;
- its circular fiber could be wider or narrower than its base.

The conditional `C^2` metric equation rejects both distortions when the geometry is a complete,
smooth, boundaryless capped cell in the static-product slice. It leaves the round geometry—not
because roundness was assumed, but because every distortion leaves a positive trace-free curvature
that violates one component of the full Bach equation.

This is genuine progress on the **dimensionless shape** problem. It does not pick the radius. Every
round solution can still be enlarged or shrunk together under CSN.

## Why full variation mattered

If `H=1` is frozen too early and only the squashing `s` is varied, the reduced action is

`J(s) = (128 pi^2/3) theta s(1-s^2)^2`.

It has positive stationary points

`s=1`, `s=1/sqrt(5)`.

The nonround point would look like a solution in an incomplete calculation. It is not. Varying the
depth equation before freezing `H` gives constant-branch roots

`s=1`, `s=1/sqrt(3)`.

The simultaneous reduced equations retain only `s=1`. Independently, the nonround frozen-depth
candidate has

`B_00=-128/75`

in the Euclidean convention, so it fails the full field equation directly.

This is a concrete example of the repository's “variation before restriction” warning: a plausible
nonround branch was manufactured solely by freezing a metric degree of freedom too early.

## Product identity and compact theorem

For a constant-lapse product, all nonzero four-dimensional Riemann components are spatial. The 3D
identity

`Riem3^2 = 4 Ric3^2 - R3^2`

then gives

`C4^2 = Riem3^2 - 2 Ric3^2 + R3^2/3`
`     = 2(Ric3^2-R3^2/3)`
`     = 2|Ric3_TF|^2`.

The result is unchanged by static Lorentzian continuation because only spatial curvature appears in
this slice.

For the Bach equation, the product Weyl component is

`C_0i0j = -(epsilon_t/2)(Ric3_ij-R3 g3_ij/3)`.

Contracted Bianchi then gives the displayed `B_00`. On a compact smooth `S3`, integration yields

`integral |Ric3_TF|^2 = 0`.

Positivity of the spatial norm makes the conclusion pointwise. A 3D Einstein metric has constant
sectional curvature, so all Weyl components vanish and the complete Bach tensor vanishes.

This proves the selection theorem for the declared compact product family without postulating that
the universe minimizes the action.

## A lower-derivative metric term really appears—but its identity matters

Expand the selected round branch in a genuine scale-free metric-shape direction:

`H(eta)=1+epsilon h(eta)`, `s=1`.

At quadratic order the same `C^2` invariant produces

`(4/3) q(k^2+3)(h')^2`.

For the smooth preregistered comparison mode

`h=sin^2(2 eta)`,

the integrated coefficient is exactly

`256 pi^2/5`

per unit dimensionless proper time.

This establishes:

`CONDITIONAL_TWO_DERIVATIVE_METRIC_SHAPE_TERM`.

It does not establish the historical carrier `L2`. The varied object here is the radial/orbit shape
of a conditional spacetime metric. There is no independent map into `S2`, no section or soldering,
and no material source. In this reduced mode there is also no derived nonzero balance between a
quadratic carrier term and a quartic carrier term.

The useful conceptual result is narrower: one scale-free curvature-square parent can indeed produce
lower-derivative stiffness when expanded around a selected curved metric. That makes the proposed
one-parent bridge mathematically real for metric shape, while leaving its matter interpretation
open.

## Physical scale remains absent

Under a common scaling, the proper-time interval contributes `b`, the spatial volume contributes
`b^3`, and `C^2` contributes `b^-4`. Their product is one. The dimensionless equations select `H`
and `s` but contain no equation for `b`.

Thus the two issues are now cleanly separated:

- dimensionless angular shape: selected conditionally in this branch;
- absolute radius/physical scale: still open.

Electron mass was not used. It remains available later as an `OBSERVED_CALIBRATION` after a physical
branch and its energy are defined.

## The physical finite cell is not yet the compact cap

The compact theorem uses a smooth boundaryless `S3`: the two coordinate endpoints are regular
circle-collapse orbits, not physical walls. Current UDT finite-cell canon supplies a mirrored static
`phi=0` seal but not the toric cap identification, a differentiable fourth-order boundary action, or
Bach boundary/corner data.

On a physical interval,

`integral Delta_3 R3`

is a boundary flux and need not vanish. A nonround solution could then balance interior
trace-free curvature against boundary data. Until the native boundary functional is derived, the
compact selection theorem cannot be silently promoted to the realized UDT cell.

Bootstrap and `Xmax` add no equation to this local dimensionless solve under their current wording.
A future global eigenproblem may select among full boundary-completed solutions, but no such
functional was inserted here.

## Provenance firewall and scope

The deterministic census froze 3,667 base-tree sources matching the preregistered vocabulary.
Thirty-five load-bearing sources were individually adjudicated. The July-1 firewall and current
owner clarifications control:

- `C^2`/Bach is `UNIQUE-CONDITIONAL` only inside the frozen metric-only/local/4D/unrestricted-
  variation class;
- the reciprocal toric spatial realization, `S3` caps, and free Hopf action remain conditional;
- round `S2` and `L2+L4` remain excluded inputs;
- complete action, source, boundary charge, physical scale, and carrier remain open.

The earlier Cartan audit's warning is preserved: curvature computed from a chosen metric does not by
itself make that metric the realized universe. This audit adds an equation-based selection theorem
inside one chosen conditional family; it does not derive that family's premises.

## Four banking gates

1. **Preregistered:** yes, commit `ed2aa9c`, before symbolic outcome calculation.
2. **Full space or bounded scope:** complete for arbitrary positive `H(eta)`, constant positive
   squashing, smooth compact Hopf caps, all reduced constant partial roots, and the decisive full
   Bach `00` equation in the product slice. Variable lapse/shift, function-valued squashing,
   physical boundary, alternative topology, and full time-live coframe remain explicit omissions.
3. **Independently verified:** yes in-package. A separate coordinate-Christoffel/Ricci calculation
   reproduced a nonround `H,s` sample, the false-root curvature and Bach residual, and the round
   zero. A separate sectional-curvature expansion reproduced `256 pi^2/5`. Thirty fail-closed
   corruption/overclaim catches pass. Fresh external-model review was not authorized.
4. **Every premise audited:** yes for the bounded verdict, including action class, product form,
   signature continuation, toric realization, caps, variation order, physical boundary, CSN scale,
   bootstrap, `Xmax`, carrier, and electron calibration.

Maximum banked grade: **VERIFIED-WITH-CAVEATS**.

## Next dimensionless equation

The immediate next test is to relax the most consequential bounded choice without yet introducing
matter:

`g4 = epsilon_t N(eta)^2 d tau^2 + g3[H(eta),s]`.

Vary `N` and `H` before restriction, keep every Bach component, and test whether the compact theorem
survives a nonconstant lapse. Then add the minimal time/fiber or reciprocal time/radial shift allowed
by the full `2+2` coframe census.

Only after the round/angular selection survives that time-live enlargement should the physical
finite-cell boundary functional and bootstrap eigenvalue be brought in. No GPU work is indicated.
