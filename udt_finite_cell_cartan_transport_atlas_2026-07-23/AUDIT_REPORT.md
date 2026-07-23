# Finite-cell Cartan transport atlas

Date: 2026-07-23

Preregistration commit: `2a0a199`

Mode: metric-led, CPU-only exact algebra

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The boost/rotation `3+3` structure has now been followed through every
registered finite-cell completion family and every causal type of `dphi`.
The local answer is exact:

| `dphi` domain | surviving object | connection behavior |
|---|---|---|
| timelike and nonzero | observer boost `3` + rotation `3` Cartan split | Levi-Civita transport preserves it iff the boost/extrinsic connection block vanishes; otherwise it mixes |
| spacelike and nonzero | real `3+3` `SO+(1,2)` symmetric pair | preserves iff the complementary connection block vanishes; otherwise it mixes |
| null and nonzero | rank-two nilpotent two-form filtration | normalized semisimple `3+3` split degenerates |
| zero | no intrinsic line or split | continuation depends on the approach direction |
| type-changing | piecewise nonnull structures | any change must cross a null or zero degeneration |

The timelike split therefore persists on every connected smooth region
where `dphi` stays timelike and nonzero. It does **not** require the
Levi-Civita connection to preserve the two sectors separately. If the
off-stabilizer connection is nonzero, the sectors mix in a precisely
controlled way.

For one generic tangent-direction witness, each off-diagonal mixing block
has rank two and the total mixing map has rank four. The direction aligned
with that tangent's boost/extrinsic vector remains unmixed. This is the
standard algebraic rank of the cross-product-type action; it is not a
new physical propagation law.

## Exact connection block result

In an orthonormal frame adapted to timelike `dphi`, the general local
Lorentz connection contains three rotation components `r_i` and three
boost/extrinsic components `b_i`. Its induced two-form connection has
the exact block pattern

```text
A_Lambda2 = [ rotation block    boost/extrinsic block ]
             [ boost/extrinsic  rotation block         ].
```

The `r_i` act within the boost and rotation sectors. The `b_i` exchange
them. Consequently,

```text
nabla_T Pi = 0  iff  the off-stabilizer b_i(T) all vanish.
```

This is a frame-normal form for the full connection, not a block-diagonal
metric ansatz. Shift, angular, and anholonomic information is retained in
the six connection coefficients.

On every smooth fixed-rank nonnull region, the Kato correction

```text
K = (nabla Pi) Pi - (nabla Pi) (1-Pi)
```

is metric-skew and satisfies

```text
[K,Pi] = nabla Pi.
```

The corrected connection `nabla-K` preserves the moving subbundles.
This proves exact geometric transport of the reduction. It does not make
Kato transport a force, field equation, or physical time evolution.

## Causal change

The exact family

```text
alpha(lambda) = dt + lambda dx,
s = g^-1(alpha,alpha) = lambda^2 - 1
```

shows the complete local transition. For `|lambda|<1`, the split is the
timelike boost/rotation Cartan split. For `|lambda|>1`, a real `3+3`
survives, but its stabilizer is `SO+(1,2)` and it is not an observer
boost/rotation split. At `|lambda|=1`, the normalized projector diverges.

The unnormalized null line map is rank one and nilpotent. Its induced
two-form map is rank two and nilpotent. Thus the null limit retains a
filtration/screen structure, not two complementary rank-three
eigenspaces.

At `dphi=0`, the timelike approach `epsilon dt` and spacelike approach
`epsilon dx` yield different limiting projectors. There is no
frame-independent continuation without extra line data.

The scalar value `phi=0` is a separate issue. The control `phi=t` at
`t=0` has `dphi=dt`; the split is regular there. A seal defined by a value
of `phi` therefore does not by itself cause degeneration.

## Complete finite-cell cross

The source universe contains exactly twelve registered completion
families, FC01--FC12. The audit crosses each with five causal classes,
giving 60 unique rows in `COMPLETION_CAUSAL_CROSS.tsv`.

This is a completion-family atlas, not twelve solved universes:

```text
complete on-shell (g,phi) finite-cell solutions supplied: 0.
```

Accordingly, the exact local rules above are available in every family,
but the actual causal history and mixing profile remain conditional on an
unsupplied complete metric/`phi` field.

The strongest family-level consequences are:

- boundary-to-boundary cells can support a nonvanishing submersion but do
  not force one;
- a static real scalar on a compact boundaryless completion has a
  critical point, so the split must degenerate somewhere;
- a time-dependent component can evade that static theorem, but no
  current UDT equation forces such a profile;
- cap, mirror, quotient, nonorientable, stratified, and singular families
  each add the extension qualifications recorded in
  `FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv`;
- a true metric/manifold singularity admits claims only on its regular
  complement.

No family is selected.

## Common-scale neutrality

The normalized `dphi` line projector and its induced `3+3` reduction are
unchanged by positive common rescaling, so the split itself descends
through CSN.

Levi-Civita preservation of the split does not. A nonconstant conformal
rescaling can change `nabla Pi` even when the starting representative is
flat with constant `dphi`. Thus the pre-scale conformal class fixes the
reduction but not its Levi-Civita mixing profile.

This is a concrete selector seam: a physical metric representative, or a
pre-scale conformally natural connection, is required before the mixing
profile can become physical.

## What is and is not derived

Derived:

- the local causal stratification;
- the exact connection blocks and preservation conditions;
- the rank of a generic one-direction timelike mixing witness;
- Kato transport on smooth fixed-rank nonnull regions;
- null and zero degeneration controls;
- the exact 12-by-5 completion/causal cross.

Open or conditional:

- every complete on-shell finite-cell `(g,phi)` branch;
- whether `dphi` is timelike, spacelike, null, zero, or type-changing on
  the selected universe;
- selection of a physical scale representative;
- through-interface laws;
- action, source, boundary functional, carrier, Hopf section, matter, or
  physical evolution.

The audit therefore characterizes where the structure persists, mixes,
and degenerates without converting a local metric invariant into a
complete UDT solution.
