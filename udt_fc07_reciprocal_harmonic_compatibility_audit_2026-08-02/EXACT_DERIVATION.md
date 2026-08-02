# Exact derivation — FC07 reciprocal/harmonic compatibility

Date: 2026-08-02  
Preregistration: `090f8ee`  
Source freeze: `47d5610`

## 1. Bounded coframe and parent theorem

The audited family is

```text
theta0 = p(s) dt,                         p=c_E exp(-phi),
theta1 = a(s) ds,                         a=L exp(+phi),
thetaA = u_A(s)dt+b_A(s)ds+P_Aa(s)dy^a,
D      = det(P)=sqrt(det(h))>0.
```

It is stationary and torus-invariant, with arbitrary smooth finite descending data in the chosen
bounded lower-triangular field generalization and supplied global descent. The J07/J11 cocycle is
not constructed. On each of the four FC07 mapping tori with `b1=1`, the parent theorem gives

```text
I     = integral_cell a(s)/D(s) ds,
alpha = [a/(I D)] ds = theta1/(I D),
P_alpha = P_theta1.
```

Here and below, “descending” means that the field descends to the quotient; it does not mean that a
single-valued scalar is strictly monotone around a closed base.

## 2. Hodge algebra and the only simple proportionality cut

For an invariant base form `beta=f(s)ds`,

```text
delta beta = -[1/(aD)] d/ds [D f/a].
```

Therefore

```text
delta alpha  = 0,
delta theta1 = -D'/(aD).
```

The pointwise scalar between the two forms is

```text
r(s) = alpha/theta1 = 1/[I D(s)].
```

Consequently:

```text
alpha = k theta1 for one cell-wide constant k
    iff D'=0,

k = 1/ell,
ell = integral_cell theta1 = integral_cell a ds.
```

Thus constant proportionality and raw-ruler harmonicity are the same local area condition. No
registered active premise requires `D'=0`.

Pointwise equality is stronger:

```text
alpha=theta1
    iff I D=1 everywhere
    iff D is constant and ell=1 in the chosen unit.
```

It equates a primitive dimensionless cohomology period with a physical proper length. The `ell=1`
step is a unit/scale choice, not a consequence of projective ownership.

## 3. Three objects on one direction are not one object

The closed base carries three distinct quantities:

```text
dphi:     exact local reciprocal-depth change,  integral_loop dphi=0;
theta1:   physical ruler form,                   integral_loop theta1=ell>0;
alpha:    primitive harmonic H1 representative, integral_loop alpha=1.
```

They occupy the same base covector line wherever `dphi` is nonzero, but their global information is
different. Composition of observer comparisons governs `Delta phi`; the metric determines `ell`;
the integral cohomology lattice normalizes `alpha`. None of those operations equates the three.

This immediately rules out a nontrivial constant solder on a closed base:

```text
dphi = k alpha, k constant
=> 0 = integral dphi = k integral alpha = k
=> k=0
=> dphi=0.
```

A variable coefficient is always definable:

```text
dphi = F alpha,
F = I D phi'/a,
integral_cell F alpha=0.
```

This is an identity for any admitted `phi`, not an equation selecting `F` or `phi`. Any future
nontrivial exact-to-harmonic bridge on a closed cell must carry local sign/shape information with
zero harmonic mean; a nonzero constant conversion cannot do the job.

## 4. Exact counterfamilies

### Free physical ruler scale

For every `q>0`,

```text
L -> qL,
a -> qa,
theta1 -> q theta1,
I -> qI,
alpha -> alpha,
r -> r/q.
```

The topology, monodromy, harmonic class, projective ownership, founded reciprocal character, and
supplied descent remain intact. This is an exact one-parameter counterfamily to any claim that the
current premises fix the scalar normalization.

### Smooth positive variable angular area

On a `2 pi` base choose

```text
a=L,
D=1+(3/5)cos(s)>0.
```

Then

```text
I=5 pi L/2,
r(0)=1/(4 pi L),
r(pi)=1/(pi L).
```

The coefficient varies by a factor of four while the reciprocal/harmonic projectors remain equal.
Unimodular mapping-torus descent constrains the endpoint determinant, not the interior area profile;
a smooth periodic area modulation can be inserted without changing the monodromy class.

### Variable founded depth with constant angular area

Choose

```text
exp(phi)=1+cos(s)/3>0,
D=1.
```

Then

```text
I=2 pi L,
r=1/(2 pi L),
F=-6 pi sin(s)/(3+cos(s))^2,
integral F alpha=0.
```

The ruler is harmonic despite nonconstant `phi`. It is angular area—not local `phi`—that controls
raw-ruler harmonicity in this bounded family.

## 5. Reciprocity, composition, seal, and descent

### Observer Reciprocity

Observer-frame Reciprocity requires a future law to transform naturally. It does not require a
configuration to be fixed by every observer change and it does not choose a scalar invariant level.
Projector equality is tensorial. The scalar family `r=1/(I D)` can transform as part of the complete
observer data without one member being selected. The complete observer action on the Hodge slice,
seal, and global completion remains open.

### Internal dual Reciprocity

The founded pair identity

```text
diag(exp(-phi),exp(phi))^T K diag(exp(-phi),exp(phi))=K
```

fixes the reciprocal representation. It survives every free-`L` and variable-screen witness above.
It supplies no inverse length or invariant level equating `alpha` and `theta1`.

### Composition

The exact reciprocal comparison cocycle makes depth differences additive. It explains the zero
closed-loop period of `dphi`; it does not set the positive metric loop length `ell` or the primitive
cohomology period. Treating those three additive quantities as one is a type error.

### Finite-cell seal

The current mirror-closure clause is working/conditional, and the complete seal action on the
coframe, screen, time direction, and Hodge slice is not selected. The physical seal therefore
cannot presently be used to assign a universal parity or normalization to `alpha` and `theta1`.

A minimal mathematical reflection control with even `a,D` sends both base covectors to their
negatives and leaves their ratio and projector even. It retains arbitrary `L` and even area
profiles. This proves only that reflection parity by itself need not fix the level; it is not a
physical UDT seal lift.

### Mapping-torus and mixing descent

For all four monodromies,

```text
det M=1,
det(M^T-I) != 0.
```

Unimodularity preserves the descended screen determinant, and `b1=1` preserves the unique base
harmonic line. Neither condition fixes `L`, `I`, or `D(s)`. The bounded mixing functions cancel from
the ownership formula, but their global descent is supplied. The still-open J07/J11 construction
cannot be counted as a selector.

## 6. Positive invariant readouts that do survive

The audit does derive more than a negative. In a unit-coordinate-area fiber convention,

```text
integral_fiber (*alpha) = 1/I,
||alpha||^2_L2 = 1/I.
```

Furthermore lower-triangular mixing drops out of the complete wedge:

```text
theta0 wedge alpha wedge theta2 wedge theta3
    = (c_E L/I) dt wedge ds wedge dy1 wedge dy2.
```

The local `phi` factors and screen determinant cancel. These are constant transport/capacity
readouts of the complete cell. Their value still changes across the admitted metric family; no
registered premise supplies a required level. They are not same-solution return equations.

## 7. Scale and the density opening

The dimensional matrix for `c_E` and `G_obs` has rank two, and no monomial of those two quantities
has inverse-length dimensions. This leaves the exact free-`L` counterfamily intact. It does not mean
that the physical UDT metric is scale-free; it means the bounded completion's physical loop scale
has not been closed by the registered relations.

If total proper density is independently supplied, then

```text
sqrt(G_obs rho_tot)/c_E
```

does have inverse-length dimensions. This is a genuine reason density could participate in the
missing bridge. Dimensional availability is not a native equation: nothing here derives

```text
1/(I D), 1/ell, or another metric response = sqrt(G_obs rho_tot)/c_E.
```

Consequently no density value or window is scanned.

## 8. Bounded ruling

Across the preregistered 16-candidate family and the frozen current premises:

```text
projective reciprocal/harmonic ownership                         DERIVED_CONDITIONAL_BOUNDED
primitive harmonic normalization                               DERIVED_TOPOLOGICAL_ONLY
raw ruler harmonic iff angular area constant                    DERIVED
constant alpha/theta1 coefficient iff angular area constant     DERIVED_IFF_NOT_REQUIRED
nonzero constant dphi/alpha solder on closed base               REFUTED_IN_BOUNDED_CLASS
variable dphi/alpha representation with zero harmonic mean      IDENTITY_COEFFICIENT_OPEN
constant harmonic flux/capacity readouts                        DERIVED_LEVEL_NOT_SELECTED
observer Reciprocity                                            NATURALITY_GATE_ONLY
physical seal normalization                                     OPEN_COMPLETE_SEAL_LIFT
global mixing normalization                                     OPEN_J07_J11
additional geometry-cutting relation from registered premises   NOT_DERIVED_SCOPED
density/curvature admissibility window                          NOT_AUTHORIZED_NOT_COMPUTABLE
```

This does not rule out a future native law. It localizes the missing operation: a physical,
observer-natural same-solution relation must connect local exact reciprocal depth to the global
harmonic/metric channel without confusing topological normalization with physical length.
