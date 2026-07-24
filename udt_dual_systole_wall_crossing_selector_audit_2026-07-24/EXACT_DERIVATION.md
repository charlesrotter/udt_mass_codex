# Exact wall-crossing derivation

## 1. Reciprocal control

On the shear-free toric control,

```text
H(phi)=diag(exp(-2phi),exp(+2phi)),
H(phi)^-1=diag(exp(+2phi),exp(-2phi)).
```

For the primitive character lines

```text
[e1]=[(1,0)],  [e2]=[(0,1)],
```

their squared dual norms are `exp(+2phi)` and `exp(-2phi)`.
Consequently,

```text
phi<0 : W_min={[e1]},
phi=0 : W_min={[e1],[e2]},
phi>0 : W_min={[e2]}.
```

This reproduces the parent continuous chamber theorem. The set persists at
the seal; uniqueness does not.

## 2. Reciprocity acts on the set, not one member

The reciprocal exchange is

```text
J=[[0,1],[1,0]],
J[e1]=[e2],
J[e2]=[e1].
```

Therefore

```text
J W_min(0)=W_min(0),
```

but neither member is fixed. Suppose a single-valued selector `s(H)` were
defined at the symmetric metric and equivariant under Reciprocity. Because
`J H(0) J^T=H(0)`, equivariance would require

```text
s(H(0))=J s(H(0)).
```

No member of `W_min(0)` satisfies this. Hence:

```text
no Reciprocity-equivariant single-valued shortest-line selector exists
at the symmetric seal.
```

The exchange-fixed primitive lines `[1,1]` and `[1,-1]` do not repair this:
at `H=I` their squared norm is two, while the minimum is one. They are not
members of `W_min(0)`.

This theorem is about the exact toric control and its integral lattice. It
does not assert that every complete UDT branch is toric or crosses this
seal.

## 3. Continuity and gluing are different questions

In one fixed lattice trivialization, a continuous map into the discrete
primitive-line set is locally constant. It cannot be `[e1]` on one side and
`[e2]` on the other while remaining a shortest single line at every point.

A global seam transition can change the comparison:

```text
identity gluing: I[e1]=[e1] != [e2],
swap gluing:     J[e1]=[e2].
```

Thus reciprocal-swap gluing can make the one-sided shortest lines represent
one global line across a mirrored chart transition. That is a genuine
conditional construction. It is not currently derived because exact C1
fixes scalar `phi` parity at the seal while leaving the transverse block,
other-field boundary data, and full angular lift open.

Identity, swap, sign-twisted swap, conjugate, cap, and monodromy cases remain
different global data. Algebraic availability of `J` is not selection of the
seam lift.

## 4. Coordinate tie-breaking fails

At the seal the lexicographic rule chooses `[e2]` from the represented set
`{[e2],[e1]}`. Under the basis swap, covariance requires the choice to map
to `[e1]`, while applying the same lexicographic rule to the unchanged
represented set again chooses `[e2]`.

Therefore a lexicographic or “first coordinate” rule is not `GL(2,Z)`
covariant. It is a chart convention, not UDT physics.

## 5. Common scale cannot break the tie

Under common positive rescaling, every dual-character norm receives the
same positive factor. Equal norms remain equal and their ordering is
unchanged. CSN preserves the chamber complex; it does not select a member.

This agrees with the direct CSN postulate: common scale is calibration,
while the determinant-one reciprocal sector is separately meaningful.

## 6. The three reciprocities remain distinct

- Reciprocal-c supplies the founding clock/ruler pair and its determinant-one
  generator. It does not equate the angular source or choose a character.
- Observer-frame Reciprocity requires covariant, no-preferred-observer
  description in the ordinary regime. The whole tied set is covariant;
  covariance alone does not force one member.
- `X_max` reciprocity is a working global-limit hypothesis with a
  conditional signed composition law. Its join to absolute metric `phi`,
  regular seals, and the angular character lattice remains open.

None supplies the missing angular seam lift.

## 7. Connection, cap, and boundary data

For a supplied character `w`, the projected connection

```text
b_w=w^T S
```

is covariant. It does not select `w`.

A parallel phase `d delta+b_w=0` requires locally `db_w=0`; a global
single-valued parallel phase additionally requires trivial compatible
holonomy and framing. Curvature or holonomy can obstruct a supplied phase,
but no current functional makes either choose between tied lines.

At a cap with collapsed primitive cycle `v`, a character can extend alone
only if `w(v)=0`. Otherwise a separately supplied amplitude must vanish or
patching data are required. This is compatibility, not physical selection.

All twelve completion families retain exactly these conditional
qualifications in `COMPLETION_WALL_CROSSING_ATLAS.tsv`.

## 8. Bootstrap and mass-emergence consequence

The primary bootstrap reading is after-solution admissibility. The stronger
local fork may eventually make stable-matter existence depend on global
geometry, but it supplies no current matter operator, density-to-geometry
map, wall-crossing functional, or boundary equation. Total proper density
is not yet operational and may not be inserted locally.

The positive geometric object surviving every current principle is therefore
the exchanged shortest **set**, not a selected physical `U(1)` line. This
does not derive a carrier. It shows that a future mass-emergence route should
first test whether the complete reciprocal pair is the relevant global
building block rather than assuming that UDT must choose one member.

