# Exact derivation and selector logic

## 1. Founded input and complete pointwise class

The active foundation fixes the two-channel generator

```text
H = diag(-1,+1)
```

and its finite action `exp(phi H)`. In the registered positive-triangular
complete-coframe chart, the most general constant-generator extension has
four base-angular mixing coefficients and three lower-triangular angular
coefficients:

```text
X = [ -1   0    0    0 ]
    [  0  +1    0    0 ]
    [ c00 c01  k00   0 ]
    [ c10 c11  k10  k11].
```

For `eta=diag(-1,+1,+1,+1)`, the physical metric tangent is
`X^T eta + eta X`. Its coefficient map has exact rank seven. The determinant
one condition has rank one; unchanged transverse metric has rank three; no
base-angular mixing has rank four; the last two conditions together have rank
seven. Thus no one of the seven directions is a local-Lorentz presentation
artifact in this chart.

An independent rational implementation reproduces ranks

```text
physical tangent       7
determinant condition  1
transverse condition   3
mixing condition       4
joint spectator        7.
```

The commutator equations for an arbitrary real `4 x 4` matrix against all six
generators of `so(1,3)` have rank fifteen. The full Lorentz commutant is
therefore one-dimensional scalar identity. A fixed nontrivial reciprocal
generator cannot be invariant in every local Lorentz frame; it must transform
equivariantly with the frame.

## 2. Local directional candidates

### Killing structure

The frozen complete twisted-`S3` witness has a unique stationary Killing line,
and its twist can identify an unoriented ruler line on that witness. Symmetry-
enhanced branches have additional Killing directions, and the line-plus-twist
data still does not choose the angular generator or the remaining complete
extension. It is therefore a genuine branchwise geometric construction, not
a universal extension section.

### Non-null `dphi`

For non-null `v=grad(phi)`,

```text
P_v = v tensor v_flat / g(v,v)
```

is an exact idempotent line projector. It selects a `1+3` split only after the
realized profile is supplied and the whole complement is declared to carry an
opposite character. At null or zero `dphi`, the normalization is undefined or
directional symmetry is restored. No intrinsic continuation through causal
type change is registered.

### Ricci, Weyl, and Riemann spectral data

On the real, orthogonally diagonalizable Segre `{1,111}` stratum, a simple
Ricci spectrum marks one timelike and three spacelike unoriented eigenlines.
Pairing the timelike line with a founded spatial ruler then leaves exactly
three choices. “Simple spectrum” alone does not guarantee four real lines for
a Lorentz-self-adjoint endomorphism. The exact control

```text
A = [[ 0,1,0,0],[-1,0,0,0],[0,0,2,0],[0,0,0,3]]
```

is `eta`-self-adjoint but has characteristic polynomial
`(z^2+1)(z-2)(z-3)` and eigenvalues `+i,-i,2,3`. Complex, repeated, and
Einstein strata therefore prevent the earlier unrestricted phrasing. Weyl and
Riemann operators act naturally on the six-dimensional bivector space; even a
simple principal structure supplies a plane/bivector object rather than one
member of the seven-parameter extension class. Their zero controls have a
six-dimensional degenerate eigenspace. No active premise prioritizes one
principal member or identifies it with the founded pair.

### Reciprocal projector families

The registered projectors are covariant wherever their non-null directional
inputs exist. They either presuppose the soldered reciprocal plane they would
need to select or reduce only to a line/plane. Null, zero, and tie strata remain
obstructions rather than selected continuations.

## 3. Angular and lattice candidates

A supplied positive angular metric with simple spectrum determines two
unoriented axes. That statement depends on an already supplied base/screen
split. At the round point the axes tie, and monodromy can exchange them.

On a supplied integral torus lattice, the dual-systole invariant is globally
set-covariant. Exact enumeration gives two shortest unoriented primitive lines
for the square form and three for the hexagonal wall vertex:

```text
square:    [(0,1),(1,0)]
hexagonal: [(0,1),(1,0),(1,1)].
```

Thus it is an exact set-valued invariant but not a single-valued section at
the reciprocal tie. Sign, phase, torus lattice, and physical role remain
additional inputs.

## 4. Holonomy is the closest conditional selector

For the additional diagonal subfamily

```text
X_lambda = diag(-1,+1,lambda,lambda),
```

ordinary path-independent descent requires every holonomy generator to
commute with `X_lambda`. Exact commutators give

```text
screen SO(2) rotation:                 every lambda
spatial rotations mixing ruler/screen: lambda=+1
boosts mixing clock/screen:             lambda=-1
base clock/ruler boost:                 no lambda
full so(1,3):                           no lambda.
```

If a separately supplied reciprocal swap is required to reverse the complete
generator, `F X_lambda F^-1=-X_lambda` gives `lambda=0`. But this swap obeys
`F^T eta F != eta`, so it is a twisted external transition, not ordinary
Lorentz holonomy.

Solving the same constraints on the full seven-parameter generator, in the
variable order `(c00,c01,c10,c11,k00,k10,k11)`, gives

```text
SO(3):             (0,0,0,0,+1,0,+1)
SO+(1,2):          (0,0,0,0,-1,0,-1)
reciprocal odd F:  (-a,+a,-b,+b,0,0,0).
```

Thus the first two supplied centralizer conditions uniquely force pointwise
full-chart diagonal generator members. They do not yet define global sections,
because the extension bundle and descent law remain open. The twisted
condition leaves two mixing freedoms in the full class. Its `lambda=0`
uniqueness is only a diagonal-subfamily statement.

These are three different conditional global reductions:

- `+1` for a parallel timelike line with spatial `SO(3)` holonomy;
- `-1` for a parallel spacelike ruler line with complementary `SO+(1,2)`
  holonomy; and
- `0` for an odd sign-twisted reciprocal object only in the diagonal
  subfamily; the full class retains two mixing directions.

They do not combine into one result. They arise on different supplied branch
or ontology conditions. The registered nonconstant twisted witness has full
sampled Lorentz holonomy, while the one exact regular parallel `lambda=+1`
product witness has constant `phi`, `Q=1`, no twist, and no distinguished
ruler. Cross-branch assembly is forbidden.

## 5. Seal and completion data

At a scalar seal `phi=0`,

```text
exp(0 X)=I
```

for every extension generator `X`. The seal value therefore has zero
extension-selector rank. A normal, isotropy lift, cap, quotient, or gluing map
can constrain a supplied extension, but the finite-cell atlas contains
multiple completion types and unbounded remainders. It does not select one
completion or bulk continuation.

## 6. Complete candidate census

All `12 x 16 = 192` preregistered candidate/gate cells are recorded in
`SELECTOR_GATE_MATRIX.tsv`. The outcome census is:

```text
AVAILABLE_CONDITIONAL                  6
SET_VALUED_ONLY                        4
PARTIAL_CONSTRAINT                     2
SELECTED_DERIVED                       0.
```

The independent implementation reconstructed the extension ranks, full
Lorentz commutant, holonomy values, projector singularity, Ricci pairing
count, lattice ties, and seal identity without reading production result
files. Its twelve semantic outcome features are generated from separately
listed frozen-source tokens in `INDEPENDENT_SOURCE_FACTS.tsv`, then classified
by a generic feature-to-outcome rule. It also independently emits all 192
status cells without importing the production module or reading the production
matrix; the two TSVs are byte-identical. Those statuses are independently
transcribed adjudications, so their exact agreement satisfies the registered
implementation-agreement gate but is not a proof that the candidate universe
is semantically complete.

## 7. Exact scope of the boundary

The twelve preregistered metric-natural candidate families do not evidence an
active UDT-authoritative, local-Lorentz-equivariant complete-extension
section. This is not a universal no-go. Source `S05/D14` explicitly leaves
arbitrary higher-jet and global-functional constructions unclassified, and no
closure census was performed for combined tensors or derivatives. Within the
bounded set, each candidate supplies at most a conditional substructure,
while holonomy supplies different answers only after a global reduction has
been supplied.

The physical observer/event/path variation domain remains a separate open
gate. No response, action, source, or matter conclusion follows from this
classification.
