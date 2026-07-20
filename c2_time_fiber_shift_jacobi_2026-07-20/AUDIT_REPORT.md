# Conditional C2 Time/Fiber-Shift Jacobi Audit

Date: 2026-07-20  
Base: `61f6bc01e5732b3bc59120d506bd6b2716646369`  
Preregistration commit: `dc78c51`  
Mode: CPU-only exact 4D Weyl/Bach linearization and complete smooth-kernel classification  
Status: **VERIFIED-WITH-CAVEATS** — exact direct curvature and Bach derivation, independent finite-
metric Euclidean sample, independent operator/energy reconstruction, base-source replay, and 31
exercised fail-closed catches pass; no fresh external-model review was authorized.

## Result first

The smallest stationary connection between time and the conditional angular fiber has no regular
non-gauge Jacobi mode on the smooth compact round `C^2` background.

Writing the opened coframe component as

`e3 = b[cos^2(eta)d xi1 + sin^2(eta)d xi2 + epsilon w(eta)d tau]`,

the exact Euclidean quadratic Weyl density, with `q=sin(eta)cos(eta)`, is

`q[(w''-2cot(2eta)w')^2+16(w')^2]`.

The stationary Lorentzian density has the opposite overall sign and therefore the same linearized
field equation. The direct full 4D Bach calculation gives exactly the same equation as reduced
variation.

On the smooth compact capped domain, the complete regular kernel is

`w=constant`.

That constant is not a new physical rotation: the finite metric is exactly the round product after

`xi1 -> xi1 + w tau`, `xi2 -> xi2 + w tau`.

The exact verdict is:

`NO_REGULAR_NON_GAUGE_TIME_FIBER_SHIFT_JACOBI_MODE_IN_CONDITIONAL_ROUND_COMPACT_C2_SLICE`.

This is a linearized statement. It does not exclude nonlinear disconnected shift branches,
boundary-supported modes, singular completions, other connection components, or genuine time
dependence.

## Full equation rather than reduced stationarity

The calculation assembled the complete coordinate metric before expansion, including the
`epsilon^2 w^2 d tau^2` term required by the coframe. It then independently formed the 4D Riemann,
Ricci, scalar, Weyl, and Bach tensors.

The shift Euler-Lagrange equation is

`S w'''' + 4C w''' - (16S+4C^2/S)w'' + 8C(C^2/S^2-1)w' = 0`,

where `S=sin(2eta)` and `C=cos(2eta)`.

The direct Bach projection is

`B_tau_xi1+B_tau_xi2 = -Jacobi/[4 sin(2eta)]`.

Thus the result is not the familiar false shortcut of varying a restricted action and never testing
the corresponding full field equation.

## Complete smooth kernel

With `x=cos(2eta)`, the equation becomes

`d_x^2[(1-x^2)^2 w_xx] - 4 d_x[(1-x^2)w_x] = 0`.

Multiply by a smooth `w(x)` and integrate from `-1` to `1`. The boundary terms vanish because their
coefficients contain `1-x^2` or `(1-x^2)^2`. What remains is

`integral[(1-x^2)^2 w_xx^2 + 4(1-x^2)w_x^2] dx = 0`.

Both terms are nonnegative. Therefore `w_x=0`, and `w` is constant. This classifies the entire smooth
compact Jacobi kernel; it does not merely test selected modes.

The local fourth-order equation also contains endpoint pole/log and endpoint-log integration-
constant strata. They are recorded rather than erased. They fail the registered smooth capped
domain, but a future physical-boundary or singular completion could assign them a different status.

## Independent checks

The independent verifier rebuilt the finite off-diagonal Euclidean metric for

`w=cos(2eta)`

and obtained the exact `epsilon^2` Weyl coefficient

`C4^2=48` at `eta=pi/6`,

matching the derived square formula. It independently reconstructed the compact-coordinate
Euler-Lagrange operator, found the exact degree-six polynomial energy matrix to have rank six with
only the constant null vector, and obtained the sample Jacobi residual `32 sqrt(3)` and Bach
projection `-16`.

## Lay interpretation

We allowed the angular geometry to lean into time by an amount that could vary from one depth to
another.

If every depth leans by the same amount, nothing physical has changed—we have simply described the
same universe with angular coordinates rotating at a constant rate.

If different depths lean by different amounts, the conditional conformal-curvature equation assigns
a positive Euclidean cost made of two exact squares. On a complete smooth capped cell, its field
equation has no regular zero direction except the constant coordinate copy.

This does **not** say UDT has no rotation, acceleration, or time evolution. We tested one infinitesimal
stationary connection around one conditional compact background. The nonlinear metric, the physical
wall, and genuine time dependence were not solved.

## Why this calls for a zoom-out

Two adjacent extensions now have the same pattern:

1. a nonconstant diagonal lapse is rejected unless it is a common CSN rescaling;
2. a nonconstant time/fiber shift is rejected at Jacobi order unless it is a coordinate copy.

That is evidence of **rigidity of the smooth compact conformally-flat conditional `C^2` corner**. It
is not evidence that unrestricted UDT is rigid.

The proofs are powered specifically by three choices: the conditional pre-scale `C^2` action, smooth
compact no-boundary caps, and perturbation about the round conformally-flat branch. Repeating the same
calculation one component at a time would risk mistaking the corner's rigidity for the theory's
answer.

The next decision should therefore compare, as a whole:

- the complete nonlinear stationary `N,H,s,W` family and possible disconnected branches;
- the physical finite-cell boundary, which invalidates both compact integration proofs;
- the still-open action/variation-domain bridge that made `C^2` conditional in the first place.

No new mechanism is needed. The missing structure, if present, must be in one of those omitted parts
of the metric problem.

## Scale and matter ruling

The Jacobi equation is dimensionless and common-scale neutral. It selects neither overall radius nor
clock calibration. `c`, `G`, `Xmax`, total mass/density, and electron mass do not enter.

No carrier, section, soldering, matter action, source, or particle stability conclusion follows.

## Four evidence gates

1. **Preregistered:** yes, commit `dc78c51` before algebra.
2. **Full space or bounded scope justified:** complete smooth kernel for one explicitly bounded
   stationary Jacobi field; nonlinear, boundary, other-connection, topology, and time-live layers
   remain open.
3. **Independently verified:** yes in-package by a finite-metric curvature reconstruction and a
   separate operator/energy calculation; no fresh external-model review.
4. **Every premise audited:** yes for the slice; conditional `C^2`, round background, toric coframe,
   smooth caps, noncompact time, and Jacobi order are explicit.

The correct banked grade is **VERIFIED-WITH-CAVEATS**, not a nonlinear no-go or complete UDT result.
