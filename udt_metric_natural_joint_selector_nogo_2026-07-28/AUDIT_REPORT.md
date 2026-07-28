# Metric-natural joint-selector possibility/no-go audit

Date: 2026-07-28

Primary preregistered outcome: `NO_GO_PREMISES_INSUFFICIENT_STOP`

Exact secondary result:
`FRAME_ONLY_AND_POINTWISE_METRIC_ONLY_NO_GO; REDUCED_COCYCLE_PLUS_ANGULAR_GROUPOID_TYPE_REQUIRED`

Verification: `VERIFIED-WITH-CAVEATS` — a non-importing standard-library implementation rehashed
all 13 fixed source blobs, independently reconstructed every load-bearing rank and counterexample,
and passed all 32 catch-proofs. Both implementations ran in the same session.

## Result first

The audit found a real structural theorem and an equally important limit.

### What is ruled out

A nontrivial additive scalar depth cannot be extracted as a continuous character of the entire
connected Lorentz frame-comparison group. Its Lie algebra is perfect:

```text
[so(1,3),so(1,3)] = so(1,3).
```

Therefore every continuous homomorphism from the connected full frame-comparison group to the
additive real numbers has zero derivative and is trivial. The exact rank calculation gives six
independent bracket directions and zero real-character dimension.

This does **not** mean that observer comparisons are impossible or that there is a preferred
observer. A covariant law can act on every observer query. It means that arbitrary non-collinear
full-frame comparison cannot be compressed into one nontrivial additive real number. Indeed,

```text
[K_1,K_2] proportional_to J_12 != 0,
```

so composing boosts in different directions necessarily produces angular information. The angular
sector is not optional bookkeeping.

At the pointwise metric-only level, full Lorentz isotropy gives a second exact obstruction. There
is no nonzero fixed vector or covector, and the endomorphism commutant is only scalar identity. A
non-scalar founded generator with clock/ruler eigenvalues `-1,+1` therefore requires a reduction of
the frame structure; it cannot be selected pointwise from the unrestricted Lorentz metric alone.

### What survives

The no-go does not touch two viable depth routes:

1. a base-dependent cocycle `delta(p,q)=f(q)-f(p)` when the metric or whole solution actually
   derives the physical potential `f`; and
2. a real character on a reduced reciprocal subgroup or typed path groupoid.

The stationary Killing-norm result is the concrete positive example of the first route:

```text
delta_K(p,q)=log[Q(p)/Q(q)].
```

The supplied-depth path groupoid is the concrete conditional example of the second.

The reduced full-frame algebra is now exact:

| Supplied or metric-derived reduction | Equivariant generator | Exact status |
|---|---|---|
| none; full `SO+(1,3)` | scalar identity only | incompatible with founded `-1,+1` pair |
| timelike observer line; `SO(3)` stabilizer | `diag(-1,a,a,a)` | founded spatial `+1` forces `a=+1`, unique conditional |
| spacelike ruler line; `SO+(1,2)` stabilizer | `diag(a,+1,a,a)` | founded clock `-1` forces `a=-1`, unique conditional |
| ordered clock/ruler pair; `SO(2)` screen | `diag(-1,+1,lambda,lambda)` | every real `lambda`, not selected |
| supplied path, depth, and frames | transported conjugacy/groupoid family | exact given inputs, not a selector |

Thus observer-line reduction really does provide a conditional `lambda=+1` extension, and the dual
ruler-line reduction provides conditional `lambda=-1`. They are different reduced geometries and
cannot be promoted to one universal answer. An ordered reciprocal pair alone retains the real
screen modulus.

## The conceptual advance

Founded `phi` remains exact. What changes is its proper job description.

`phi` is an additive abelian reciprocal channel. It cannot also be the complete encoding of generic
non-collinear observer-frame comparison. The full object must retain angular/nonabelian transport,
for example as the already-derived conditional type

```text
(D(delta_gamma), U_gamma).
```

This explains why repeated attempts to squeeze the scalar, the complete coframe, and angular
transport into one number or one invariant generator kept leaving residual choices. The residual
angular information is mathematically required, not a failed scalar derivation.

It also separates two questions that had been partially conflated:

- **comparison kinematics:** the reciprocal real cocycle plus angular/full-frame transport;
- **metric realization:** how the physical metric's transverse and mixing sectors respond to
  `phi`, including `lambda`.

Frame reciprocity and composition alone cannot select the second. Whether UDT requires the
comparison object itself to contain a four-dimensional `X_lambda`, or whether the reducible
cocycle-plus-transport object is already kinematically complete, remains an ownership question.

## Why the universal no-go stops short

The preregistered full no-go cannot honestly be claimed. The exact obstructions cover:

- frame-only scalar characters;
- pointwise metric-only non-scalar generators;
- homogeneous invariant endpoint cocycles;
- generic metric interval as an additive signed depth; and
- global endpoint descent under full holonomy.

They do not classify every possible base-dependent, higher-jet, nonlocal, set-valued, or
whole-solution natural construction. A natural scalar potential, when genuinely derived, produces
an endpoint cocycle; the stationary norm is already one bounded witness. Set-valued reductions can
also survive symmetry/tie strata. Calling all future UDT laws impossible would therefore exceed the
proof.

The primary outcome is consequently `NO_GO_PREMISES_INSUFFICIENT_STOP`, not the stronger universal
no-go label. The partial theorem is exact and useful; the universal theorem is not established.

## Global result

Pointwise reduction is not global descent. For

```text
X_lambda=diag(-1,+1,lambda,lambda),
```

the Lorentz-holonomy centralizer dimensions are:

```text
generic lambda: 1
lambda=+1:      3
lambda=-1:      3
lambda=0:       1.
```

Full six-dimensional Lorentz holonomy centralizes none of them. A path-labelled groupoid remains
exact, while endpoint collapse requires separately derived reduced holonomy, a section, or
transition/descent data. Null, zero, and symmetry-restoration strata remain explicit continuation
gates.

## What is unchanged

- founded `phi` identity and inverse pair action: `DERIVED`;
- stationary Killing-norm depth: `DERIVED_BOUNDED`;
- reducible scalar-plus-coframe comparison: `AVAILABLE_CONDITIONAL_EXACT`;
- physical observer/path semantics and general depth: `OPEN`;
- metric transverse/mixing realization and `lambda`: `OPEN`;
- global completion/descent/interfaces: `OPEN`;
- strong local CSN: inactive and challenged/not derived;
- `c_E` and `G_obs`: observed anchors;
- co-presence and bootstrap: working interpretations;
- action, source, carrier, boundary, density, `Xmax`, mass, dynamics, and predictions: unchanged.

## Four evidence gates

1. **Preregistered:** yes, commit `2a9f709`; the 13-source packet was frozen and pushed at
   `d6d69d1` before the new derivation.
2. **Full or bounded:** complete for input categories I0-I4, the defining Lorentz representation,
   full and reduced stabilizer algebra, full-frame continuous real characters, exact endpoint
   cocycles, the named holonomy strata, and seven explicit escape routes. It does not classify all
   higher-jet/nonlocal whole-solution operations.
3. **Independently verified:** yes by a standard-library rational implementation; caveat: same
   session rather than a fresh adversarial context.
4. **Premises audited:** yes; observer query versus preferred frame, supplied versus derived
   reductions, stationarity, path, depth, `lambda`, holonomy, strata, anchors, CSN, co-presence,
   bootstrap, and excluded downstream physics are explicit.

## Maximum conclusion

`DERIVED` in the stated scope: the full connected Lorentz comparison group has no nontrivial
continuous additive real character; non-collinear comparison forces angular information; and the
unrestricted pointwise metric cannot select a founded non-scalar reciprocal generator.

`CONDITIONAL`: reduced observer/ruler structures give the exact generator families above.

`OPEN`: base-dependent/higher-jet/nonlocal whole-solution selection, physical comparison semantics,
metric realization, and global descent.

No action, matter, density, boundary, `Xmax`, dynamics, observation model, or canon is derived.
