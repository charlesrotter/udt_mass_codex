# Pre-density substrate-response atlas

## Verdict

The complete metric supplies more than two unrelated local hints.

Where the finite-cell angular sector is genuinely toric, the exact coframe

```text
theta_ang = D(dxi + S dx)
```

already defines a joint geometric object:

```text
(integral T2 fiber, normalized fiber metric H, T2 connection S).
```

That object does **not** directly identify the chart spin-two eigenaxis with a
phase. The proposed direct identification fails under torus translations and
the eigenaxis is not intrinsic under unrestricted `GL(2)` changes without a
second reference structure.

The stronger metric-led route is different. The torus lattice and `H` define
the canonical set

```text
W_min(H) =
  argmin { w^T H^(-1) w :
           w in Z^2 primitive, w identified with -w }.
```

Every member is an integral torus character. Where this set contains one line,
the geometry makes a canonical rank-one character and connection candidate
available:

```text
b_star = w_star^T S.
```

This is a real geometric reduction, not an imported carrier. But it is not yet
a physical selection theorem and it does not supply a phase section, latitude,
action, source, boundary completion, or stable matter.

The package ruling is therefore:

```text
BRANCHWISE_CANONICAL_METRIC_LATTICE_U1_REDUCTION_AVAILABLE
PHYSICAL_SELECTION_AND_PHASE_SECTION_OPEN
```

The broader evidence grade is `VERIFIED-WITH-CAVEATS`: the algebra and bounded
atlas are independently verified, while the continuous torus-moduli space and
all possible global completions are not exhausted.

## 1. Metric-native local structure

For

```text
D = [[exp(-phi), shear],
     [0,        exp(+phi)]],
```

the normalized angular metric is

```text
H = D^T D
  = [[exp(-2 phi),              shear exp(-phi)],
     [shear exp(-phi), shear^2 + exp(+2 phi)]] ,

det H = 1.
```

The familiar traceless pair is

```text
X = H11-H22,
Y = 2 H12.
```

Under an `SO(2)` angular basis rotation by `theta`,

```text
X' = cos(2 theta) X + sin(2 theta) Y,
Y' =-sin(2 theta) X + cos(2 theta) Y.
```

The symbolic residuals are exactly zero. At `phi=0`, `shear=0`, both vanish,
so the matrix eigenaxis is undefined.

This object is useful but limited. The spin-two law assumes an `SO(2)`
reference. Under a general angular `GL(2)` chart change, `H` transforms by
congruence; ordinary matrix eigenvectors do not define an invariant line
without another reference metric. That is why the eigenaxis cannot honestly
be promoted to a target phase.

## 2. The shift block is genuine transport data

Writing `w=(1,-1)` only as a control character,

```text
delta = w^T xi,
b     = w^T S dx,
```

and applying the base-dependent torus translation

```text
xi' = xi + lambda(x),
S'  = S - d lambda,
```

gives

```text
delta' = delta + w^T lambda,
b'     = b - d(w^T lambda),
d delta' + b' = d delta + b,
db' = db.
```

Thus `S` is a `T2` connection. A supplied character projects it to a `U1`
connection. Curvature, holonomy, and parallel-section obstructions are real;
they do not select the character or a phase value.

## 3. Why the direct eigenaxis-phase join fails

Under a relative torus translation the angular metric and its chart eigenaxis
do not change, while a phase character changes with weight one. Therefore

```text
delta = 2 alpha
```

cannot be equivariant for arbitrary relative translation. The independent
witness used `lambda_rel=pi/3` and obtained a unit complex-phase change.

Common CSN weight does not repair the mismatch. Many inequivalent objects are
simultaneously scale neutral.

## 4. The metric-lattice route

An integral torus fiber supplies structure that a bare local two-plane does
not: the primitive cycle and character lattices. The inverse fiber metric
measures a primitive character:

```text
norm_H(w)^2 = w^T H^(-1) w.
```

The shortest primitive set is:

- independent of torus translation;
- common-scale neutral;
- covariant under `GL(2,Z)`;
- integral by construction; and
- set-valued on equality walls rather than falsely tie-broken.

For `xi'=M xi`,

```text
H' = M^(-T) H M^(-1),
w' = M^(-T) w,
```

so

```text
w'^T H'^(-1) w' = w^T H^(-1) w.
```

All six frozen `GL(2,Z)` representatives passed this covariance test.

This construction bypasses the chart eigenaxis. It uses only the already
present metric and finite-cell lattice.

## 5. Bounded selector atlas

The preregistered Cartesian product

```text
phi   = {-1,-1/2,0,1/2,1},
shear = {-1,-1/2,0,1/2,1}
```

retained all 25 points.

- 22 points had one shortest primitive dual-character line.
- 3 points lay on a tie wall.
- The independent fixed-box lattice enumeration agreed at every point, with
  maximum norm residual `3.553e-15`.
- The finite-search exterior bounds certify that no omitted primitive vector
  can be shorter at a sampled point.

These counts are `OBSERVED` on the frozen grid. They are not a measure or
census of the continuous moduli space.

### Exact reciprocal diagonal result

On the shear-free family,

```text
H^(-1) = diag(exp(2 phi), exp(-2 phi)).
```

Therefore:

- `phi<0`: the shortest primitive dual character is `(1,0)` modulo sign;
- `phi=0`: `(1,0)` and `(0,1)` tie;
- `phi>0`: the shortest primitive dual character is `(0,1)` modulo sign.

This reciprocal swap is exact. It is one of the clearest structures yet found
directly in the angular metric. It does not by itself say which side is matter,
cosmology, or any physical regime.

With shear present the shortest integral character can be a combination. The
frozen grid includes `(1,-1)`, `(1,1)`, `(2,-1)`, and `(2,1)` subcases. No one
combination was privileged.

## 6. Global completion atlas

All twelve inherited finite-cell classes were retained.

- On ordinary toric regions the full `(H,S)` object exists locally.
- A unique shortest dual character supplies a local character line and
  projected connection.
- At systolic tie walls the selector is set-valued.
- At caps, a phase character alone extends only if it is trivial on the
  collapsed cycle, or if another field amplitude vanishes there. The latter
  is how a full Hopf map can remain regular; it is not supplied here.
- Periodic torus bundles additionally require monodromy-compatible transport.
- Mirror and nonorientable branches can preserve or conjugate the character
  line.
- Rank-changing strata can destroy the construction.
- The nonintegrable-distribution class has no supplied global torus character
  lattice.

No completion was selected, and FC04/S3 was not privileged.

## 7. Conditional carrier response

Only after the metric-native atlas was frozen, the supplied round-`S2`
`L2+L4` diagnostic was tested.

Under a spatial conformal representative `h -> q^2 h`,

```text
E(q) = q E2 + q^(-1) E4
```

for constant `q`. This retains the relative two-/four-derivative ruler; it is
not physical scale selection.

For nonconstant `q=exp(a x)`, the manufactured scalar anchor gives

```text
-div(q grad u) = -q [Laplacian(u) + a partial_x u].
```

The production residual was `8.882e-16`; the independent five-point residual
was `1.393e-12`.

For trace-free anisotropy `K`,

```text
delta[sqrt(h) h^ij A_ij] =
  -K^ij A_ij,

delta[sqrt(h) h^ik h^jl F_ij F_kl] =
  -2 K^ik F_ij F_kj.
```

The independent finite-difference maximum residual was `5.297e-12`.

If a character and phase section are separately supplied, `d delta+b_w`
provides the exact connection channel seen by the conditional carrier.

These are response identities, not a matter solve.

## 8. What this changes

The bootstrap hypothesis now has a sharper geometric target. It does not have
to invent a micro coupling from nothing:

1. the global cell can control torus shape `H`;
2. `H` and the integral lattice carry a canonical set of primitive phase
   directions;
3. the shift block transports those directions;
4. a conditional matter sector is sensitive to common scale, anisotropy, and
   the projected connection.

What is missing is ownership:

- Does UDT make the shortest-character invariant physically operative?
- How are tie walls crossed or resolved?
- Does bootstrap select a completion, representative, sign/orientation, and
  phase section together?
- What maps total proper density or other global invariants into `(H,S)`?

Until those are answered, no density window or matter closure can be claimed.

## 9. Verification

- Preregistration commits: `2fe47fd`, `223d460`.
- Sources: `20/20` hashes reproduced.
- Registered completion coverage: `12/12`.
- Production symbolic/numeric run: pass.
- Independent standard-library implementation: pass.
- Independent selector residual: `3.553e-15`.
- Independent conformal residual: `1.393e-12`.
- Independent anisotropy residual: `5.297e-12`.
- Catch-proofs: `16/16`.
- Matter solves: zero.
- GPU work: zero.

No external model arm was used. The independent implementation and exercised
mutations certify the load-bearing algebra within the registered scope; an
external scientific review remains welcome.

