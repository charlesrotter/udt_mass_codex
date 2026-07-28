# Exact derivation — finite-cell reciprocal quotient reduction

## 1. The early physical gate remains open

The founded result supplies the reciprocal clock/ruler action, but no active premise states that the
complete coframe must be an exact quotient representation. Everything below that uses the word
“quotient” is therefore a conditional branchwise construction. The calculation can still decide
whether the complete metric already contains the needed geometry if that semantics is adopted.

The corrected frozen universe contains sixteen branch/stratum representatives and twelve completion
classes. Only the `FC04_TWO_CAP_P1`/`S3` class currently contains complete all-gate intrinsic-pair
metric witnesses. Other rows remain controls, local configurations, degenerations, or structural
completion classes.

## 2. The complete twisted-S3 metric supplies a global screen

On B01–B06 and B16, the complete metric intrinsically identifies an unoriented timelike clock line
`u` and, through its nonzero twist, an unoriented spacelike ruler line `n`. Their signs do not affect
the projectors

```text
P_u = -u tensor u_flat,
P_n =  n tensor n_flat.
```

The orthogonal screen projector and screen metric are

```text
H = I-P_u-P_n,
q = g+u_flat tensor u_flat-n_flat tensor n_flat.
```

Exact algebra gives

```text
H^2=H, rank(H)=2, H(u)=H(n)=0,
q|image(H) positive definite.
```

Because the two lines are global and the formula is sign-independent, `image(H)` is a smooth global
rank-two subbundle on each registered all-gate twisted-`S3` configuration. This is metric-intrinsic
given the configuration; it is not merely the supplied Maurer–Cartan basis.

The twist-off, depth-off, static-clock-only, round, squashed, local WR-L, and reduced-product
controls fail earlier gates as recorded in `BRANCH_OUTCOMES.tsv`. They cannot be combined with the
twisted branch by taking the best property from each.

## 3. The finite metric lift is basis-free on this branch

Let `phi` be the founded depth and let `lambda` denote the branch's unselected isotropic screen
weight. The complete generator can be written without choosing screen axes:

```text
X_lambda = -P_u+P_n+lambda H.
```

Its finite action is

```text
F_lambda(phi)
 = exp(-phi)P_u+exp(+phi)P_n+exp(lambda phi)H.
```

It induces the founded pair action exactly, preserves `image(H)`, composes, and reverses. Its first
metric response has zero pair/screen mixing and an isotropic screen block `2 lambda I`.

The parent audit found a one-parameter family of fixed-response generators `K=lambda I+wJ`.
Here it integrates to

```text
exp(phi K)=exp(lambda phi)R(w phi),
```

and the rotation cancels from `F^T g F`. Therefore every `w` gives exactly the same finite metric,
not merely the same first derivative. The screen rotation is genuine coframe representative freedom
on this branch. The anisotropic and mixed controls retain their exact second-jet differences, so
this conclusion is not generalized beyond the stated stratum.

Orientation-preserving screen transitions commute with `F_lambda`; orientation reversal also
preserves the finite metric. Consequently the **metric** lift descends across screen-frame changes
without choosing a screen flag.

This does not select `lambda`, the profile, topology, branch, or physical quotient semantics.

## 4. A screen flag is not selected—and is not needed for the metric lift

The supplied global Maurer–Cartan coframe displays two global screen axes, but that is a
configuration trivialization. At pointwise metric order, the intrinsic pair and isotropic screen
retain full `SO(2)` symmetry. Exact algebra shows that no nonzero real vector or line is invariant
under that full connected action.

Derivatives of the realized metric may define local screen directions on nondegenerate patches.
No registered theorem extends any such local direction through every zero, tie, and loop as a
metric-selected global flag. This audit does not claim a universal no-go for all higher-jet or
global constructions. It derives the stronger practical point that no flag is required to define
the finite metric lift above.

## 5. The metric does supply a canonical screen rotation connection

Full ambient parallel transport and intrinsic screen transport must be separated. Once `H` and the
Levi-Civita connection are supplied, the metric canonically defines a connection on the screen
bundle:

```text
D_X s = H(nabla_X s),  s in image(H).
```

For an orthonormal screen frame, its connection matrix is the screen block of the Lorentz
connection. Exact block algebra proves:

```text
H D = D H = D,
D q = 0,
D_connection in so(2) locally.
```

Under a screen rotation by angle `alpha`, the local scalar connection coefficient obeys the usual
frame-covariant law

```text
A -> A+d alpha
```

with the sign set by frame convention. Thus the metric supplies a genuine screen-rotation law along
every supplied path. It is a connection, not a chosen axis or an endpoint-only comparison. Calling
it the physical observer-comparison law remains open.

## 6. Ambient Levi-Civita transport does not preserve the reduction

The projected connection closes because of its explicit projection. The ambient Levi-Civita
connection generically has nonzero pair/screen blocks. In the intrinsic adapted frame,

```text
nabla_(u+n)(u+n) = -p1(u+n)-2p2 E2-2p3 E3,
nabla_(u-n)(u-n) = +p1(u-n)-2p2 E2-2p3 E3.
```

The ruler-aligned null lines are pregeodesic only where `p2=p3=0`. On the contact `S3`, imposing
that condition globally forces `p1=0` and hence `dphi=0`. A nontrivial stationary depth therefore
forces ambient pair/screen mixing somewhere.

The independent covariant-derivative control also gives

```text
(nabla_E0 X_lambda)^0_1=-3/25
```

for every sampled real `lambda`. No screen weight repairs the frozen nonconstant profile.

## 7. Holonomy leaves only path-labelled descent

The registered complete twisted configurations have sampled curvature span and Lie closure equal to
all six dimensions of `so(1,3)`. Exact centralizer algebra gives rank fifteen in `End(R4)`, so the
centralizer is only the scalar identity. `X_lambda` is never scalar because its clock and ruler
eigenvalues differ.

Therefore ambient loop holonomy cannot preserve the reciprocal grading. A source generator may be
transported by conjugation along each path and composes exactly, but different paths can return
different endpoint representatives. The screen connection likewise has path-dependent rotation
holonomy. The exact status is `PATH_LABELLED_ONLY`. Neither result selects a global flag.

This does not erase the global screen subbundle: `H(p)` is defined intrinsically at each point. It
means ambient parallel transport does not map it to itself without an endpoint projection/reset.

## 8. The reduced-holonomy survivor is not full reciprocal closure

At `lambda=+1`, constant `phi`, and zero twist, the product

```text
R x round S3
```

has spatial `SO(3)` holonomy and a parallel clock-versus-all-space grading. But `Q=1`, the twist
ruler vanishes, and spatial isotropy removes the distinguished ruler/screen split. It is a valid
reduced-holonomy control, not a nontrivial complete founded-pair branch.

The regular `lambda=-1` and generic-lambda contact branches have no strong parallel survivor. No
active premise requires strong parallelism or selects the product control.

## 9. Completion census

`FC04_TWO_CAP_P1` has concrete complete `S3` representatives and therefore receives the branchwise
results above. The other eleven registered completion classes do not contain a current concrete
all-gate metric with exact quotient transition data. Their boundary, cap, quotient, reflection,
orientation, rank-change, and monodromy labels identify requirements; they do not compute a screen
flag or transport law.

## 10. Bounded conclusion

The developed complete branch supplies more than an open placeholder:

- an intrinsic global screen subbundle;
- a basis-free finite reciprocal **metric** lift;
- exact descent through the one-parameter screen-rotation representative fiber; and
- a canonical metric-projected `O(2)`/`SO(2)` screen connection along supplied paths.

It does not supply:

- a metric-selected global screen flag;
- ambient parallel preservation of the reciprocal split;
- path-independent endpoint descent;
- an active physical quotient/observer/path rule; or
- on-shell branch, profile, `lambda`, completion, variation, action, source, carrier, boundary,
  bootstrap, density, `X_max`, mass, or dynamics selection.
