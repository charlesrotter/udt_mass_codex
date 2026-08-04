# Exact derivation — metric-natural reciprocal/screen selectors

## 1. The object being tested

A realized reciprocal/screen split is a smooth decomposition

```text
TM = N + Q
```

with `N` a nondegenerate Lorentzian rank-two plane (one clock direction and one ruler direction)
and `Q=N_perp` its positive rank-two screen. Equivalently, it is a metric-self-adjoint projector
`P_N` satisfying

```text
P_N^2=P_N, rank(P_N)=2.
```

A metric-natural selector must be equivariant. In particular, every isometry fixing a point must
commute with the selected projector at that point. This is stronger and more precise than asking
whether a convenient coframe displays a `2+2` block.

## 2. Full-isotropy obstruction

For the defining Lorentz representation, solve

```text
[P,K_i]=0, [P,J_i]=0
```

for all three boosts and all three rotations. The exact coefficient matrix has rank 15 in the 16
entries of `P`. Its one-dimensional nullspace is scalar identity:

```text
Comm(so(1,3)) = {s I}.
```

The scalar idempotent equation is `s^2=s`, so the only invariant projectors have ranks zero and
four. There is no rank-two metric-natural plane on a full-isotropy control. This recovers and
sharpens the prior pointwise partial no-go for the exact object needed by the globalization audit.

## 3. Registered round-branch obstruction

The round ultrastatic `R x S3` control already supplies a distinguished time line. Its spatial
isotropy is `SO(3)`. Solving only the three spatial commutator equations gives rank 14 and a
two-dimensional commutant:

```text
P = diag(a,b,b,b).
```

For an idempotent, `a,b` are each zero or one. The possible ranks are

```text
0, 1, 3, 4,
```

never two. Geometrically, `SO(3)` selects the time line and the whole spatial three-plane, but no
spatial ruler line. Therefore it selects no Lorentzian clock/ruler plane.

This is not restricted to a zero-jet formula. Any unique natural local or global construction on
that exact round metric must respect its isometry stabilizer at every point and meets the same
obstruction. A boundary, marked point, chosen Hopf field, or additional physical structure could
break the symmetry, but then it is part of the input rather than a consequence of the round metric.

The conclusion is correspondingly bounded: no unique metric-natural smooth rank-two split exists
on a retained domain that includes this round control. A future native law could change the domain
by excluding or further decorating that branch; this audit does not forbid that.

## 4. One founded or metric-derived line is not yet a plane

A regular timelike `dphi` supplies one line conditionally on a physical local `phi` assignment.
The residual stabilizer is spatial `SO(3)`, so the preceding calculation still supplies no ruler.
A regular spacelike `dphi` has the dual `SO+(1,2)` stabilizer on its complement. Its commutant also
has dimension two and invariant projector ranks `0,1,3,4`. It supplies one ruler line but no clock
line.

The null-vector little group has a two-dimensional nonsemisimple commutant, but its only
idempotents have ranks zero and four. The null orthogonal complement is degenerate, so the usual
orthogonal-projector construction is unavailable. At `dphi=0`, no primary gradient line exists.
Thus first-jet `phi` data alone do not provide the required smooth rank-two split.

Second-jet selection has causal prerequisites. For timelike `dphi`, the spatially restricted
Hessian can supply a ruler only where it has a unique simple spacelike line. For spacelike `dphi`,
the restricted complement is Lorentzian and must supply a unique simple **timelike** line; complex,
null, nondiagonalizable/Jordan, and tied spectra remain. Null `dphi`, zero `dphi`, and causal-type
change require separate degenerate/rank-changing continuation. No such continuation follows
automatically, and physical local/global `phi` assignment remains open.

## 5. Exact curvature-selected positive construction

Let the metric-self-adjoint Ricci operator have the exact control spectrum

```text
A = diag(2,3,5,5)
```

in an orthonormal causal frame. Its simple time and ruler spectral projectors are polynomials in
`A`:

```text
P_2 = product over mu in {3,5} of (A-mu I)/(2-mu),
P_3 = product over mu in {2,5} of (A-mu I)/(3-mu),
P_N = P_2+P_3 = diag(1,1,0,0).
```

Exactly,

```text
P_N^2=P_N, rank(P_N)=2, P_N^T eta=eta P_N.
```

Because it is a polynomial in the tensorial operator, it is equivariant. The production and
independent implementations verify this under the rational Lorentz boost with
`cosh=5/3, sinh=4/3`.

This proves capability on the simple-spectrum stratum. It is not merely formal: the frozen
squashed-`S3` control has ultrastatic time plus a metric-selected unoriented simple Ricci/Hopf line
away from the round locus. In the reordered homogeneous frame its Ricci endomorphism has spectrum

```text
Ric#_Q02 = diag(0,1/2,3/2,3/2),
A = 2 I + 2 Ric#_Q02.
```

Thus the synthetic exact projector is an affine rescaling of the registered Q02 Ricci operator and
has identical eigenspaces. That branch is complete as a homogeneous metric but remains off shell,
and its selected plane is not parallel under the registered full spatial holonomy.

## 6. Exact collision obstruction

Consider two simple-spectrum approaches:

```text
A_e1(epsilon)=diag(2,5-epsilon,5,5),
A_e2(epsilon)=diag(2,5,5-epsilon,5).
```

Both tend to the same round operator `diag(2,5,5,5)`. For every positive `epsilon`, the natural
clock/ruler projectors are respectively

```text
diag(1,1,0,0), diag(1,0,1,0).
```

Their difference has rank two. Hence the unique simple-eigenline construction has no
approach-independent continuous member at the round collision. At the collision, the natural
object is the full `SO(3)` orbit of unoriented spatial lines, a two-dimensional set, not one plane.
The second path is the first path conjugated by the round-branch spatial isometry exchanging the two
candidate squashing axes, so this is the same registered symmetry collision rather than two
unrelated algebraic examples.

This does not make the set meaningless. It separates a natural set-valued answer from a realized
smooth section.

## 7. Intrinsic-form positive and defect loci

The frozen intrinsic two-form audit is replayed without altering it. Among 18 candidates it has:

```text
9 ZERO,
6 MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI,
2 PROJECTOR_BLOCKED,
1 METRIC_DEGENERATE.
```

On each of the six nonzero candidates,

```text
W != 0: ker(W)=span(T,N), dimension 2.
```

This is a second exact branch-local positive selector. It fails as a global fixed-rank split on the
registered zero graph: the kernel becomes four-dimensional there, the projective line extends only
through the generic equator, and it is path-obstructed on three great circles. The later defect
audit supplies a global lift only on the graph complement, not across the removed graph.

## 8. Query bundle is not a spacetime section

The total ordered pair-frame query bundle `pi:F_(1,1)(TM)->M` has a tautological reciprocal plane in
`pi*TM`: at `(x,u,n)` it is `span(u,n)`. Different points of the same fiber over `x` carry different
planes. Existence of this object needs no section.

A realized field on spacetime would be an equivariant choice of one fiber point or one plane over
every `x`. Many smooth plane sections exist on `R x S3`, but the query-bundle projection selects
none of them. On the round control, a unique metric-natural choice would select an
`SO(3)`-invariant spatial line, which the exact rank calculation forbids. Projection therefore does
not derive a natural realized field.

## 9. Remaining candidate families

- A unique real simple decomposable curvature-bivector eigenspace could select a plane, but
  conformally flat, tied, complex, or nonsimple strata obstruct universality; no such complete
  frozen witness is registered.
- Two independent curvature-scalar gradients can span a plane on a nondegenerate rank-two locus;
  constant, collinear, null, and rank-changing loci remain.
- Unique intrinsic Killing clock/ruler lines or a unique invariant holonomy subspace can select a
  branch-local plane. No symmetry, enhanced symmetry, irreducible holonomy, and the round `1+3`
  holonomy are retained controls. Parallelism is stronger than metric naturality.
- A unique metric-natural whole-solution or nonlocal construction on the exact round control still
  must respect its global isometry stabilizer, so the round obstruction reaches that branch. The
  positive capability of nonlocal operations on other, less symmetric branches remains
  unclassified because no registered operation supplies one.
- Boundary/topology and rank-changing constructions remain open because no registered operation
  supplies them. They could decorate or change the domain; they are not silently covered by the
  undecorated-round theorem.
- An action or dynamical stability rule might later select a response plane, but using it here would
  reverse the current dependency order and change the metric-only question.

## 10. The bounded theorem

```text
UNIVERSAL UNIQUE SMOOTH METRIC-NATURAL RANK2 SPLIT
  = OBSTRUCTED on the retained domain containing the round complete control;

BRANCH-LOCAL METRIC-NATURAL SPLITS
  = EXIST on simple-curvature and intrinsic-form nonzero strata;

GLOBAL CONTINUATION
  = OBSTRUCTED OR OPEN at symmetry collisions, zero graphs, causal/rank changes, and untyped joins;

QUERY-BUNDLE RECIPROCAL PLANE
  = DERIVED CONTAINER, not a spacetime section.
```

No physical branch, field, action, source, carrier, boundary, or dynamics is selected.
