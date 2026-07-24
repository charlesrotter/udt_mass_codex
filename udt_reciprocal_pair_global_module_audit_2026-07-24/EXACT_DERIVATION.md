# Exact reciprocal-pair global-module derivation

## 1. Typed starting object

On a genuinely toric angular region, let `Lambda*` be the rank-two integral
character local system and let `Q=H^-1` be its positive determinant-one dual
metric. A primitive character is an integer covector modulo sign.

At a generic shortest-character wall, the parent theorem gives two
co-shortest primitive lines:

```text
W_min(Q) = {[w1],[w2]}.
```

The theorem also gives

```text
abs det(w1,w2)=1.
```

This determinant is the first decisive fact.

## 2. The pair spans the complete module

Because the determinant has magnitude one, `(w1,w2)` is an integral basis:

```text
Z w1 + Z w2 = Lambda*.
```

Thus the rank-two object obtained by “keeping both characters” is not a
proper submodule. It is exactly the complete torus character module already
present wherever the integral torus exists.

The production control uses

```text
Q = [[13/12, 5/12],
     [ 5/12,13/12]].
```

It has determinant one. Enumeration of primitive vectors gives precisely
`[e1]` and `[e2]` at the minimum `13/12`. Their determinant is one and their
Smith index is one.

This is positive and limiting at once:

- positive: no member must be discarded at the tie;
- limiting: retaining both does not yet produce a new carrier bundle.

## 3. The co-shortest pair is wall-local

On the reciprocal diagonal,

```text
Q_minus = diag(1/2,2),  W_min={[e1]},
Q_zero  = I,            W_min={[e1],[e2]},
Q_plus  = diag(2,1/2),  W_min={[e2]}.
```

The full lattice `Lambda*` persists throughout the toric region, but the
metric-derived two-element shortest set exists only at the wall.

At a three-way vertex the shortest set is, in a suitable basis,

```text
{[e1],[e2],[e1-e2]}.
```

Every two-element subset is unimodular. There are three possible pair
choices, so the metric does not select one pair at the vertex.

Consequently a global **metric-derived co-shortest pair reduction** requires
both:

1. a branch lying everywhere in a two-way wall stratum; and
2. transition/monodromy maps preserving that unordered pair.

A supplied continuation outside the wall is mathematically possible, but it
is no longer derived by shortestness.

## 4. Exact structure group of an unordered pair

Fix the standard unoriented pair `{[e1],[e2]}`. Its stabilizer in
`GL(2,Z)` consists exactly of the signed permutation matrices:

```text
one entry +/-1 in each row and column, all other entries zero.
```

There are eight. This is the complete order-eight integral hyperoctahedral
group in two dimensions.

Unipotent shear, hyperbolic, and determinant-minus-one shear controls do not
preserve the pair:

```text
[[1,1],[0,1]],
[[2,1],[1,1]],
[[1,1],[0,-1]].
```

They still act invertibly on the full module. Therefore:

```text
full Lambda* descends under arbitrary GL(2,Z) cocycles;
an unordered pair splitting descends only under the signed-permutation
subgroup, plus the everywhere-wall condition when shortestness is claimed.
```

## 5. Pair-associated covariants

Let `W` be the matrix with columns `w1,w2`.

Once an unordered pair reduction is supplied, the following are
sign/order-covariant:

```text
G_pair = W^T Q W,
K_pair = w1 tensor w1 + w2 tensor w2.
```

For a signed permutation `R`, their representatives transform by

```text
G_pair -> R^T G_pair R.
```

The determinant, trace, and absolute mutual angle are intrinsic to the
reduction. At a generic wall the Gram diagonals are equal; at the symmetric
seal the Gram matrix is the identity.

For the torus connection doublet `S`,

```text
b = W^T S,
f = W^T dS.
```

Under an ambient lattice change `M` and a pair reordering/sign matrix `R`,

```text
W' = M^-T W R,
S' = M S,
b' = R^T b,
f' = R^T f.
```

These are genuine associated-bundle doublets. They do not choose a phase
section, pair member, or physical field.

## 6. The pair does not select an exchange lift

Four signed-permutation matrices exchange the two unoriented lines:

```text
 J = [[0, 1],[ 1,0]],    J^2= I,
-J = [[0,-1],[-1,0]],  (-J)^2=I,
 R = [[0, 1],[-1,0]],    R^2=-I,
-R = [[0,-1],[ 1,0]],  (-R)^2=-I.
```

The first two are involutions. The latter two are order-four lifts. All act
as the same transposition on the **unoriented line pair**, but they have
different fixed sets.

For `J`,

```text
Lambda_+ = Z(1,1),
Lambda_- = Z(1,-1).
```

For `-J`, the fixed and anti-fixed lines are exchanged. The two involutions
are conjugate by the sign basis change `diag(1,-1)`.

The order-four lifts have no nonzero fixed lattice and therefore no fixed
circle subgroup. Hence the unordered pair alone cannot supply a fixed
circle: it does not distinguish an involutive swap from an order-four swap.
Exact C1 fixes scalar `phi` parity, not this angular lift.

## 7. Exact integral parity residue

Even after an involutive exchange is supplied, its real eigenlines do not
split the integral lattice directly:

```text
det [[1,1],
     [1,-1]] = -2.
```

Therefore

```text
[Lambda* : Lambda_+ + Lambda_-] = 2.
```

The diagonal and anti-diagonal sublattices are each primitive, but together
they contain only characters whose two coordinate parities agree. This
`Z2` index is an exact associated invariant. No physical interpretation is
assigned to it.

## 8. Conditional fixed circle and quotient character

If a global involutive angular exchange `J` is separately supplied, its
fixed primitive sublattice exponentiates to the diagonal circle. The
anti-fixed character

```text
w_-=(1,-1)
```

annihilates that circle and therefore represents the relative quotient
character, up to sign. For `-J`, diagonal and anti-diagonal roles exchange.

This is a conditional construction from the global lift. The local tied pair
does not select the lift.

## 9. Conditional reciprocal spinor and Hopf chain

In the aligned reciprocal toric chart, normalize the two positive reciprocal
weights:

```text
a1 = exp(-phi)/sqrt(exp(-2phi)+exp(2phi)),
a2 = exp(+phi)/sqrt(exp(-2phi)+exp(2phi)).
```

Then exactly

```text
a1^2+a2^2=1,
a2/a1=exp(2phi),
phi -> -phi swaps a1 and a2.
```

If two periodic phases are supplied,

```text
z1=a1 exp(i xi1),
z2=a2 exp(i xi2),
```

is a unit `S3` spinor coordinate. Quotienting by a supplied diagonal fixed
circle gives the standard unit `S2` formula. This reproduces the already
conditional relation `tan(eta)=exp(2phi)`.

The interpretation is not automatic. It requires:

- the aligned reciprocal angular chart;
- interpreting coframe weights as normalized amplitudes;
- two periodic phases;
- full reciprocal range;
- a global toric completion; and
- a selected involutive exchange lift.

For the supplied `FC04` independent primitive caps, the fixed circles of
`J` and `-J` have weights `(1,1)` and `(1,-1)`. Both are free on the
conditional `S3`. Their normalized classes have

```text
c1=+1 or -1,
abs(c1)=1.
```

The sign changes with lift/orientation convention. The maximum invariant
without those choices is the already known conditional absolute unit class.

The sharpened point is that no preferred shortest member is required for
this conditional Hopf bundle. What is required is a global involutive
exchange and the `FC04` completion—neither presently selected.

## 10. Completion rulings

All twelve registered completions are retained in
`COMPLETION_MODULE_ATLAS.tsv`.

- Boundary branches retain the full interior module but need framing.
- Caps replace the principal rank-two orbit lattice by isotropy quotients;
  the rank-two regular fiber does not extend through a cap unchanged.
- `FC04` conditionally supports the `S3`/unit-class chain.
- Lens and orbifold families retain quotient/stabilizer dependencies.
- Periodic bundles always retain the full `GL(2,Z)` local system; a
  metric-derived pair additionally needs an everywhere-wall branch and
  signed-permutation monodromy.
- Mirror classes distinguish identity, sign, involutive swap, and
  order-four lifts.
- Nonorientable gluing twists signs and characteristic orientation.
- Rank loss terminates or quotients the module.
- A nonintegrable plane distribution supplies no integral character module.
- The reciprocal diagonal remains a local wall-crossing control whose
  endpoint completion is open.

No completion is selected.

## 11. Authority boundary

Derived:

- the full character local system where toric;
- the wall pair's unimodularity and full span;
- the order-eight pair stabilizer;
- pair-associated Gram/tensor/connection data;
- the four exchange-lift distinction;
- the index-two eigenlattice residue.

Conditional:

- a global pair reduction on an everywhere two-way-wall branch with
  signed-permutation monodromy;
- a fixed circle from a global involutive exchange;
- the reciprocal spinor coordinate;
- the `FC04` `S3` quotient with `abs(c1)=1`.

Open:

- the angular exchange lift;
- torus periods and completion;
- carrier section and transport;
- action, source, boundary completion, density feedback, mass, scale, and
  time-live persistence.

No canonization follows.
