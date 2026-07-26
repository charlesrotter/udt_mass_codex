# Exact derivation

## 1. The soldering problem

The founded reciprocal operator acts on an abstract two-channel space:

```text
H_pair = diag(-1,+1).
```

A physical lift must supply an ordered clock and ruler inside a Lorentzian
tangent/coframe space, or explicitly replace that rank-two codomain by a
broader two-character representation. Frame covariance requires the lifted
endomorphism to transform by conjugation, not to retain one fixed component
matrix.

The commutant of the full connected Lorentz algebra in real `4 by 4`
endomorphisms is exactly

```text
span{I}.
```

Therefore the metric, `phi` at one point, and any number of scalar anchors do
not select a nontrivial reciprocal solder.

## 2. One nonnull direction: exact `1+3` alternative

For a nonnull vector `v`, define the metric-self-adjoint line projector

```text
P_v = v tensor v_flat / g(v,v).
```

The complete commutant of the stabilizer of that line is

```text
X = a P_v + b(I-P_v).
```

This holds both for a timelike line, whose complement has an `SO(3)` action,
and for a spacelike line, whose complement has an `SO+(1,2)` action. The only
stabilizer-invariant projector ranks are

```text
0, 1, 3, 4.
```

There is no invariant rank-two plane.

If one additionally declares the supplied line to carry one founded
character and its entire complement to carry the opposite character, the
nontrivial involutions are fixed:

```text
X_clock = I-2P_clock,
X_ruler = 2P_ruler-I.
```

For a timelike clock line, `X_clock` has eigenvalue `-1` on the clock and
`+1` on all three spatial directions. It is a clean clock-versus-all-space
`1+3` lift. For a spacelike ruler line, `X_ruler` has `+1` on that line and
`-1` on its Lorentzian three-dimensional complement; that complement contains
both temporal and spatial directions, so it is an algebraic character lift
rather than a clean clock-versus-space decomposition.

Both have nonzero physical metric tangent. Their traces are `+2` and `-2`,
respectively, so their complete coframe determinants are not one. This does
not violate the founded pair determinant: extending pair-volume preservation
to the whole coframe is a separate premise.

The `1+3` result is unique only after choosing the broader codomain. It does
not recover a distinguished ordered rank-two pair.

## 3. Null and zero directions

For a fixed null vector `k`, its connected little-group commutant is

```text
span{I,N},
N = k tensor k_flat,
N^2=0.
```

Writing `X=aI+bN`, the idempotent equation has only `X=0,I`, and the
involution equation has only `X=-I,+I`. There is no nontrivial semisimple
reciprocal lift. The normalized nonnull projector also divides by
`g(k,k)=0` and is unavailable.

At `dphi=0`, no line is present and the full metric-only obstruction returns.
Consequently a nonnull-`dphi` lift cannot continue regularly through a null,
zero, or causal-type-changing interface without additional data.

## 4. An ordered observer/separation pair leaves one physical modulus

Supply a unit timelike observer `u` and a unit spacelike separation direction
`n` with `g(u,n)=0`. Let

```text
P_u      = projector onto u,
P_n      = projector onto n,
P_screen = I-P_u-P_n.
```

The stabilizer of the ordered pair is the screen rotation group `SO(2)`. The
complete endomorphism commutant has dimension six. After its clock/ruler
block is fixed to `H_pair`, every lift is

```text
X_(lambda,omega)
  = -P_u + P_n + lambda P_screen + omega J_screen.
```

`J_screen` is metric-antisymmetric, so `omega` has zero pointwise metric
tangent and is local-Lorentz coframe presentation. `P_screen` is
metric-self-adjoint and has nonzero metric tangent. Thus exactly one physical
modulus remains:

```text
lambda = transverse-screen dilation weight.
```

Three notable values are:

```text
lambda=+1 : X_clock, clock versus all space;
lambda= 0 : pair-only spectator screen;
lambda=-1 : selected ruler versus clock and screen.
```

The complete trace is `2 lambda`. A separately imposed complete determinant
one or invariant screen area would set `lambda=0`, but neither is currently
derived from the pair determinant.

## 5. Every direction for one observer

For each unit spatial direction `n`, set the pointwise screen-rotation gauge
to zero and write

```text
X_lambda(n)
  = -P_u + P_n + lambda(P_space-P_n).
```

For two directions `n,m`, exact multiplication gives

```text
[X_lambda(n),X_lambda(m)]
  = (1-lambda)^2 [P_n,P_m].
```

The commutator of two spatial line projectors is a spatial rotation in their
plane. Six rational direction projectors span all symmetric `3 by 3` spatial
matrices; their commutators span all three spatial rotations.

Therefore:

- for every `lambda != 1`, the directional generators span six dimensions,
  their rotation commutators span three, and their closed fixed-observer Lie
  algebra has dimension nine;
- for `lambda=1`, every `X_lambda(n)` is the same `X_clock`; the directional
  span is one and all commutators vanish.

No other value changes the dimension. At `lambda=-1/2`, the sum over three
orthogonal axes becomes pure clock response, but the Lie algebra remains
nine-dimensional.

The three generated rotations are pointwise Lorentz-frame directions. This
is an exact angular assembly structure, not curvature, force, holonomy,
matter, or Hopf charge.

## 6. A plane is insufficient

A simple nondegenerate oriented Lorentzian bivector selects a two-plane and
its orthogonal screen, but not clock/ruler axes inside the plane. Boosts
within that plane preserve the bivector. The founded self-adjoint response
`diag(-1,+1)` does not commute with those boosts.

The plane's canonical Hodge/boost generator is metric-antisymmetric and has
zero metric tangent. It is a Lorentz-frame transformation, not the founded
physical reciprocal dilation under the calibrated diagonal readout. Treating
these as identical would repeat the prohibited identification of `phi` with
observer rapidity.

Two ordered independent covectors can produce `u,n` by Lorentzian
Gram-Schmidt when their Gram data are nondegenerate and their roles are
supplied. The same unoriented plane under an internal boost gives a different
founded response, so the plane alone still does not select axes.

## 7. Second jets and global data

A simple-spectrum self-adjoint tensor can mark four eigenlines, but even the
exact diagonal control has three Lorentzian rank-two choices: pair its
timelike eigenline with any of three spatial eigenlines. A priority rule is
still required. Eigenvalue crossings make the projectors nonunique or
discontinuous. Prior registered curvature families also include irreducible
full-algebra and flat-ambiguous cases.

A finite-cell normal is only one spacelike line. Conditional angular bundles
may identify a screen but do not back-select clock/ruler axes. Observer axes
at distinct events require an event-pairing path and transport; holonomy and
cut loci remain global obstructions.

## 8. Scalar anchors

Adjoining a Lorentz scalar does not reduce any stabilizer group. Therefore
`c_E`, `G_obs`, and provisional `hbar` have exactly zero directional selector
rank in this problem. `hbar` can later calibrate a derived action or period,
but only an additional quantization/period rule could make it act on the
angular sector.

## 9. Refined ontology fork

Two local codomains now remain sharply distinguished:

1. a single complete endomorphism, with the temporal-line `1+3` lift as a
   unique conditional candidate; or
2. an observer-and-direction-indexed family `X_lambda(u,n)`, closer to the
   pair-comparison wording of the founding postulates and carrying an exact
   noncommutative directional algebra.

The first needs a globally selected timelike line and fails at causal-type
change. The second needs event pairing, transport, a selected `lambda`, and a
consistency rule showing how all pair comparisons describe one geometry.
Current authority selects neither codomain.
