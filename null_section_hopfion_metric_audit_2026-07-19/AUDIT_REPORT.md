# Null-Section / Hopfion Metric Audit — Report

Date: 2026-07-19
Base: `715fa57767ecc2ec370599ad18cd9f87911798d8`
Preregistration commit: `3588962`
Mode: CPU-only, metric-led, no research-artifact mutation

## Result

`EXACT_RECIPROCAL_HOPF_ORBIT_BLOCK_COMPATIBILITY_WITNESS__CONDITIONAL_UNIT_HOPF_CONNECTION_AFTER_TORIC_S3_COMPLETION__ANGULAR_SLOTS_GLOBAL_CLOSURE_BOUNDARY_CONFIGURATION_SPACE_AND_ACTION_OPEN__DIRECT_CELESTIAL_CARRIER_IDENTITY_BLOCKED_WITHOUT_SOLDERING`

The angular-sector suggestion exposed a substantially sharper bridge than the bare observation that
both the light cone and the existing carrier involve an `S2`.

There is an exact algebraic relation between reciprocal exponential dilation and the angular
two-torus orbits of the standard Hopf fibration of `S3`. In Hopf coordinates for a round unit
three-sphere,

\[
z_1=\cos\eta\,e^{i\xi_1},\qquad
z_2=\sin\eta\,e^{i\xi_2},
\]

\[
ds_{S^3}^2=d\eta^2+\cos^2\eta\,d\xi_1^2+\sin^2\eta\,d\xi_2^2.
\]

Define reciprocal depth by

\[
\tan\eta=e^{2\phi}.
\]

Then exactly

\[
\boxed{
ds_{S^3}^2=
\operatorname{sech}^2(2\phi)d\phi^2
+\frac{1}{2\cosh(2\phi)}
\left(e^{-2\phi}d\xi_1^2+e^{2\phi}d\xi_2^2\right).
}
\]

Thus the determinant-normalized angular orbit block is precisely

\[
\boxed{\operatorname{diag}(e^{-2\phi},e^{2\phi}).}
\]

This is the same reciprocal metric-coefficient pair supplied by the C0/C1 exponential comparison,
now appearing in an explicitly Hopf-capable angular geometry. The match was not found anywhere else
in the prior topology audit or the current load-bearing source set.

## Lay interpretation

The previous audit found a sphere of possible causal directions at every event but no rule choosing
a direction field. The present audit found a more structured possibility.

Imagine a three-dimensional closed geometry built from two circular directions. As positional depth
changes, one circle shrinks exactly as the other expands. After removing their common size, their
relative sizes obey UDT's reciprocal exponentials. At one end the first circle closes; at the other
end the second closes. With the simplest primitive gluing, the completed space is `S3`, and its
natural quotient by simultaneous rotation of both circles is `S2`. That is the Hopf fibration.

The existing Hopfion's target sphere could therefore be the quotient of a reciprocal angular metric
structure rather than an unrelated internal sphere. This is a stronger and more UDT-specific lead
than merely matching the celestial `S2`.

It remains a conditional completion. Current C0/C1 does not put its reciprocal pair into two
periodic spatial angular slots, choose their common scale, choose the circle action, or close the
endpoints into `S3`.

## The common-scale-independent Hopf connection

Let the candidate angular block be

\[
q_{\rm ang}=\Omega(\phi)^2
\left(e^{-2\phi}d\xi_1^2+e^{2\phi}d\xi_2^2\right).
\]

If two periodic spatial circle directions and the diagonal generator

\[
V=\partial_{\xi_1}+\partial_{\xi_2}
\]

are separately supplied, its normalized metric-dual connection is

\[
\mathcal A=
\frac{e^{-2\phi}d\xi_1+e^{2\phi}d\xi_2}{2\cosh(2\phi)}.
\]

The common scale `Omega` cancels exactly. With `phi` running once from minus infinity to plus
infinity, both angles having period `2*pi`, and the two primitive circle factors collapsing at
opposite ends,

\[
\int \mathcal A\wedge d\mathcal A=-4\pi^2,
\qquad
Q_H=-\frac{1}{4\pi^2}\int \mathcal A\wedge d\mathcal A=1.
\]

This is the normalized principal-connection convention. Doubling the connection to match the
unit-`S2` area-form convention gives

\[
\int (2\mathcal A)\wedge d(2\mathcal A)=-16\pi^2,
\qquad
Q_H=-\frac{1}{16\pi^2}\int (2\mathcal A)\wedge d(2\mathcal A)=1.
\]

The two normalizations therefore agree on the unit class and must not be mixed when comparing to the
existing numerical convention.

The quotient map can be written directly in reciprocal depth and relative angle
`delta=xi1-xi2`:

\[
\boxed{
\mathbf n(\phi,\delta)=
\left(
\operatorname{sech}(2\phi)\cos\delta,
\operatorname{sech}(2\phi)\sin\delta,
-\tanh(2\phi)
\right),
}
\]

and the exact script verifies `n dot n=1`.

This quotient is one canonical `Q=+/-1` witness (or seed-level map) supplied by the conditional
toric completion. It is not the full carrier configuration space `Map(S3,S2)`, an arbitrary
deformation of `n`, or the actually relaxed no-null field. Deriving those carrier degrees of
freedom from metric quotient data would require additional dynamics and remains open.

This is load-bearing: once the angular slots, diagonal circle action, periods, and endpoint closure
are granted, the connection and unit class do not depend on the common angular scale. It is exactly
the kind of division Common-Scale Neutrality invites.

There is a discrete orientation/chirality ambiguity. The diagonal and anti-diagonal circle
combinations give the two registered signs `Q=+1` and `Q=-1`. Current Reciprocity/CSN does not
choose that sign.

## Why the exact match is not yet selection

Every positive diagonal two-block has a reciprocal determinant-one normal form:

\[
\frac{\operatorname{diag}(a^2,b^2)}{\sqrt{\det}}
=\operatorname{diag}(a/b,b/a).
\]

Therefore the local exponential match is a compatibility theorem, not a uniqueness theorem. Hopf
content enters only after additional global facts are supplied:

1. the two reciprocal directions are spatial and periodic;
2. they form a declared `U(1) x U(1)` angular orbit;
3. a diagonal or anti-diagonal circle action is selected;
4. `phi` spans the required range with appropriate monotonicity;
5. one primitive circle collapses smoothly at each end;
6. the common scale and radial metric make those endpoints regular;
7. the physical finite-cell boundary or global closure admits that construction.

C0/C1 supplies none of those items universally. It explicitly leaves slot identification, the
transverse spatial block, off-diagonal terms, topology, and other-field boundary data open.

There is also a type gate stronger than ordinary underdetermination. The founding construction is
stated using the dimension-matched temporal/parallel conversion pair `(c dt, dr)`. The audit has
found the same determinant-one representation inside a positive spatial angular block; it has not
shown that the founding temporal/parallel pair may be reassigned or duplicated there. Compactifying
the physical time direction as one of the Hopf circles would change the problem and can introduce
closed timelike curves, so it is not an admissible shortcut. A viable bridge needs either a derived
transverse spatial representation of the reciprocal action or angular metric equations that produce
the same block independently while remaining compatible with the clock/parallel readout.

The round completion uses

\[
\Omega_H^2=\frac{1}{2\cosh(2\phi)},\qquad
g_{\phi\phi}=\operatorname{sech}^2(2\phi),
\]

but smooth compact closure does not uniquely select these round functions. Nor does the local block
select global `S3`: different primitive collapse cycles have determinant `p` and admit lens-space
alternatives. Those are countermodels to global uniqueness, not affirmative UDT physics.

The relation is globally subtler than an ordinary CSN gauge choice. `Omega_H` tends to zero at both
circle-collapse orbits and `phi` tends to plus or minus infinity. Common-Scale Neutrality identifies
representatives only for positive `Omega`. Therefore the normalized reciprocal orbit block and the
round metric's orbit block are positively conformally related on the open principal-orbit region,
not at the two caps. The full three-metric additionally requires the independently supplied radial
coefficient `g_phiphi=sech^2(2phi)`. Adding the smooth caps is conformal-completion/boundary data.
The round metric is regular in `eta`,
while the determinant-one representative and `phi` coordinate are singular there. This is compatible
with an asymptotic-depth interpretation but is not derived from CSN itself.

## Reciprocity mirror and the finite-cell clue

Within the exact Hopf-coordinate match,

\[
\phi\mapsto-\phi
\]

exchanges the two circle scale factors. At `phi=0` they are equal; in the round witness this is the
Clifford torus separating the two circle-collapse regions.

That resembles the finite-cell mirror rule more closely than the earlier celestial-fiber analogy:
the C1 seal has odd `phi` with `phi=0`, while Reciprocity exchanges the dual factors. A two-sided
closure could join reciprocal halves across the equal-scale torus and cap them by opposite circle
collapses.

This remains `WORKING_CANDIDATE`, not a boundary derivation. C1 does not state that the mirror swaps
two angular circles, that `phi` reaches both infinite endpoints, or that either cap is physical.

## What the actual angular–phi coupling does

The user correctly identified the angular/transverse sector as the likely selector locus. The audit
separates three cases.

### 1. Pure round angular scale

For

\[
h_{AB}=R(\phi)^2\gamma_{AB},
\]

the mixed connection is

\[
\Gamma^A{}_{\phi B}=\frac{R'}R\delta^A{}_B.
\]

Its trace-free part vanishes, so an isotropic `phi`-dependent angular radius cannot select an angular
direction. A rotating dyad on this round block is frame gauge.

### 2. Reciprocal angular anisotropy

If the reciprocal pair is actually realized in two spatial angular directions,

\[
h_{AB}=\Omega^2\operatorname{diag}(e^{-2\phi},e^{2\phi}),
\]

then the scale-free mixed connection has trace-free part

\[
\left(\Gamma^A{}_{\phi B}\right)_{\rm TF}
=\operatorname{diag}(-1,1)
\]

when `phi` itself is used as the coordinate. This is genuine shear in the supplied angular
realization. It can distinguish the two circle axes and is exactly where a selector could live. The
unresolved question is whether UDT derives those spatial angular slots rather than merely allowing
them.

### 3. Angular dependence of the scalar in the old diagonal radial slice

For the chosen metric slice

\[
ds^2=-A\,dt^2+A^{-1}dr^2+q_{AB}dy^A dy^B,
\qquad A=e^{-2\phi(r,y)},
\]

the radial-looking covector

\[
\ell=dt+A^{-1}dr
\]

is null. When `A` depends on angle,

\[
\ell\wedge d\ell
=dt\wedge d(A^{-1})\wedge dr
\]

has nonzero angular-gradient components. This confirms real geometric coupling between angular
variation and the reciprocal block.

It is not yet the static Hopf charge. Its pullback to a constant-`t` spatial slice vanishes, and the
radial-looking null line has angular acceleration

\[
a^A=\frac{q^{AB}\partial_B A}{A^2},
\]

so it is not a null geodesic congruence when the angular gradient is nonzero. The banked scalar
multipole probe likewise reports that regular static angular modes become wall-loud in its chosen
working-L/round-areal slice. That supports the importance of the boundary but is not a full
transverse-metric result.

## Why the direct celestial-carrier identity fails

The existing numerical carrier is an internal unit triplet. Its ordinary derivatives and global
target rotations are visible directly in `fs_hopfion.py` and `noNull_energy.py`. A tangent or null
direction is instead a section of a position-dependent sphere bundle and changes components under
local frame rotations.

The exact countermodel is decisive:

- start with one physically constant axis;
- describe it in a quaternion frame that winds once over `S3`;
- its components become the standard unit Hopf map;
- the component Hopf number changes from zero to one although the physical axis did not change.

Similarly, a local rotation by `theta(x)` gives the constant axis ordinary derivative density

\[
|\partial_x\mathbf n|^2=(\partial_x\theta)^2.
\]

The pure-gauge frame connection cancels it covariantly, but the existing `L2+L4` functional has no
such local frame connection. Therefore the existing carrier cannot simply be renamed a celestial or
tangent section. It needs a soldering/frame plus a covariantized or intrinsic bundle action, neither
currently selected.

The Hopf charge in the Faddeev field links preimages of target values. Those preimage curves are not
automatically the integral curves of a tangent/null congruence; the two objects even live in
different geometric bundles until soldering is supplied.

## Effect of the co-present framing

Co-presence materially improved the question. It encourages treating the complete fibration or
section as one whole spacetime solution rather than as a particle assembled step by step. It also
makes global closure, endpoint regularity, and topology propagation impossible to ignore.

It does not select the construction. Whole-solution membership supplies no foliation, angular
slots, circle action, boundary completion, field equation, or protection against caustics,
singularities, boundary escape, or topology change. Light-cone causality remains a separate local
constraint.

The celestial-null `S2` remains a valid conditional fiber, but the angular Hopf-torus route is now
the more specific UDT candidate because it uses the reciprocal exponential structure itself.

## Action and time-live consequences

No existing action is derived by this audit. The conditional angular completion supplies a metric
connection and curvature, so a future dimensional-reduction or bundle-geometry derivation could ask
whether `L2`, `L4`, or a related functional descends from the parent metric. That route must not
assume the answer or import the existing Faddeev–Skyrme functional.

A time-live solve remains valuable, but it would currently evolve a carrier/action choice made
before this angular slot and closure question is settled. The scientific ordering is therefore:

1. audit whether C0/C1 plus finite-cell/bootstrap conditions select the two spatial angular slots,
   their diagonal circle action, and primitive endpoint closure;
2. if that survives, derive rather than assume the reduced carrier/connection action;
3. compare its time-live stability against the existing independently posited `S2` control branch.

## Mechanical adjudication

| Route | Ruling | Reason |
|---|---|---|
| Bare celestial `S2` identification | `BLOCKED_WITHOUT_SOLDERING` | Fiber topology does not supply a frame-invariant carrier field or its ordinary-derivative action. |
| Round angular scale coupled to `phi` | `NO_DIRECTION_SELECTOR` | The mixed connection is proportional to the identity. |
| Angular-dependent scalar in old radial metric | `GEOMETRIC_COUPLING_NOT_HOPF_SELECTION` | Frobenius coupling appears, but the spatial Hopf form vanishes and the obvious line is nongeodesic. |
| Reciprocal pair in two spatial angular slots | `CONDITIONAL_TRACEFREE_SHEAR` | It carries scale-free anisotropic transport once those slots are supplied. |
| Hopf-coordinate `S3` completion | `EXACT_ALGEBRAIC_COMPATIBILITY` | The normalized orbit block is exactly reciprocal. |
| Diagonal `U(1)` connection and `Q=1` | `CONDITIONAL_CSN_INVARIANT_HOPF_CLASS` | Exact after periods, circle action, full `phi` range, and primitive `S3` closure are supplied. |
| Unique native carrier/action | `OPEN` | Slot, closure, boundary, representative, action, and dynamics are not selected. |

The detailed twenty-two-row result is `STATUS_LEDGER.tsv`.

## What is not claimed

- No physical time direction was compactified or reinterpreted as an angular circle.
- No current clock/parallel metric readout was replaced.
- No global `S3` universe, lens space, or Clifford-torus seal was adopted.
- No carrier, action, source, mass, boundary charge, or time-live law was derived.
- No existing particle field was recomputed.
- No GPU work, canonization, repository reorganization, startup update, or `grok` integration was
  performed.

## Four evidence gates

1. Preregistered: yes, commit `3588962`, including the angular-sector/`phi` arm before further source
   inspection.
2. Scope: exact local/global compatibility and countermodel audit; not a full metric solution-space
   enumeration.
3. Verification: deterministic exact-algebra replay plus exercised fail-closed corruptions; fresh
   adversarial semantic review recorded separately.
4. Premises: frozen in `PREREGISTRATION.md`, `SOURCE_INVENTORY.tsv`, and `STATUS_LEDGER.tsv`.
