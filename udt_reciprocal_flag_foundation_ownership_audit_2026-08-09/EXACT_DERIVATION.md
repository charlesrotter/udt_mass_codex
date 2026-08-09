# Exact derivation — reciprocal flag, foundation ownership, and the missing comparison state

## 1. Landing

```text
FOUNDED_ABSTRACT_RECIPROCAL_CALIBRATION_SEED_DERIVED;
RECIPROCAL_ROOT_CONDITIONAL_UNIQUE_UNIVERSAL_ORDER_ZERO_READOUT;
COMPLETE_CAUSAL_FLAG_TRANSPORT_CALIBRATION_AND_PHYSICAL_ARROW_OPEN.
```

The reciprocal-root causal-flag formula is mathematically sound:

```text
delta_RF(A,F) = (1/2)b2(A,F)-b1(A,F)
              = (ell_r(A,F)-ell_t(A,F))/2.
```

It is not yet the missing physical UDT observer-pair rule. Its flag, complete exchange extension,
non-isometric comparison arrow, and physical calibration state are not all owned by the current
foundation.

The most useful result is a type correction: the founded reciprocal transformation acts first on
abstract clock/ruler **calibration channels**. It is not ordinary physical tangent-space transport.
The missing complete law must realize that calibration structure on an ordered observer-pair query;
searching arbitrary tangent-bundle connections does not derive it.

## 2. What the founding algebra actually owns

The founding pair is the dimension-matched pair

```text
q=(c_E dt,dr).
```

On an already supplied signed ordered depth, the exact representation is

```text
D(delta)=diag(exp(-delta),exp(+delta)).
```

It preserves the dual evaluation pairing

```text
K=[[0,1],[1,0]],
D(delta)^T K D(delta)=K,
```

and obeys exact composition and reversal. Moreover,

```text
K D(delta) K = D(-delta).
```

Thus exchange parity is derived on the two **abstract reciprocal labels**.

This is not a physical Lorentz exchange. With the physical two-plane signature

```text
eta=diag(-1,+1),
```

one has

```text
K^T eta K = -eta,
D(delta)^T eta D(delta) != eta  for delta != 0.
```

Therefore `K` is an anti-isometry for the physical causal metric and `D` is a reciprocal squeeze,
not a physical Lorentz isometry in the original clock/ruler basis. Diagonalizing `K` gives an
algebraic `O(1,1)` form for the dual pairing; it does not make `K` the physical interval. Earlier
language calling `D` an unqualified observer boost is regraded accordingly.

The foundation owns:

```text
abstract clock/ruler channel types
+ their dual pairing
+ the reciprocal character on supplied depth
+ abstract exchange parity.
```

It does not thereby own:

```text
a physical tangent clock line
+ a physical ruler direction
+ their complete flag update
+ a non-isometric cross-fibre arrow
+ a physical calibration-line trivialization.
```

## 3. Why the full-GL no-go is real but not final

In the full untyped general-linear group,

```text
D_t=diag(exp(-t),exp(+t),1,1)
```

is a commutator. Taking

```text
S_t=diag(exp(-t),1,1,1)
```

and a quarter-turn `J` in the first two coordinates gives exactly

```text
S_t J S_t^-1 J^-1 = D_t.
```

Every homomorphism from full `GL(4)` to the additive reals vanishes on commutators. Hence no
arrow-only real character on that oversized group can send `D_t` to `t`.

This proves a conditional no-go:

```text
FULL_UNTYPED_GL_ARROW_ONLY_CHARACTER = IMPOSSIBLE.
```

It does not disprove a cocycle with a moving comparison state. The physical object cannot be just
an arbitrary total matrix with full `GL(4)` isotropy.

## 4. The correctly typed conditional flag groupoid

For a Lorentz vector bundle `(E,g)`, let an object be a causal partial flag

```text
F=(L subset P subset E_p),
dim L=1, dim P=2, g|L<0.
```

The plane `P` is automatically Lorentzian. An arrow is a pair `(A,F)` with an invertible
cross-fibre map `A:E_p->E_q` such that both `F` and `AF` are causal. Source, target, composition,
inverse, and identity are

```text
s(A,F)=F,
t(A,F)=AF,
(B,AF)o(A,F)=(BA,F),
(A,F)^-1=(A^-1,AF),
1_F=(I,F).
```

This is the open restriction of the full flag action groupoid to causal objects. It is closed under
the displayed operations and is a Lie groupoid. It is conditional UDT structure because the
physical query has not yet been shown to supply `F` and its update.

For metric densities on the clock line and clock/ruler plane, define positive ratios

```text
rho1(A,F) = clock-line density expansion,
rho2(A,F) = clock-ruler-plane density expansion,
b1=log rho1,
b2=log rho2.
```

Intermediate densities cancel exactly:

```text
rho_k(BA,F)=rho_k(B,AF)rho_k(A,F),
b_k(BA,F)=b_k(B,AF)+b_k(A,F).
```

Writing the associated graded scales as

```text
ell_t=b1,
ell_r=b2-b1,
ell_s=b4-b2,
```

gives the exact cocycle

```text
delta_RF=(ell_r-ell_t)/2=(1/2)b2-b1.
```

It composes, reverses, is neutral on identities, and is invariant under independent orthonormal
endpoint coframe changes. On `D_t`, it returns exactly `t`.

For the registered lower-mixing witness,

```text
rho1^2=3/16,
rho2^2=3/4,
delta_RF=(1/4)log(64/3)=0.765067698672...
```

so the readout sees mixing that changes the transported clock norm or clock/ruler plane area.

## 5. Exact uniqueness boundary

The isotropy group of a standard `(1,1,2)` flag is the block parabolic with diagonal block sizes
`1,1,2`. Its Lie algebra has dimension 11; its commutator has rank 8. Therefore it has exactly
three independent smooth real characters, represented by

```text
alpha ell_t + beta ell_r + gamma ell_s.
```

This classification is not an assumed linear ansatz. It follows from the abelianization of the
isotropy parabolic.

For the complete transitive groupoid, however, every smooth cocycle also admits an arbitrary
endpoint coboundary:

```text
u(AF)-u(F).
```

Consequently the literal full smooth class is nonunique. Curvature-dependent endpoint terms also
survive when metric derivatives are admitted.

If the class is narrowed to universal diffeomorphism-natural order-zero formulae built only from
the two endpoint Lorentz spaces, the arrow, and the flag, no nonconstant endpoint scalar exists:
the Lorentz group is transitive on causal flags. The class then reduces to the three characters.

Pure reciprocal normalization gives

```text
-alpha+beta=1.
```

Extending abstract clock/ruler exchange to the three graded labels gives

```text
(ell_t,ell_r,ell_s)->(ell_r,ell_t,ell_s).
```

Oddness under that formal involution gives

```text
beta=-alpha,
gamma=0,
```

and therefore uniquely

```text
(alpha,beta,gamma)=(-1/2,+1/2,0).
```

The exact theorem is therefore:

> Given a supplied causal flag and arrow, and after adding the formal complete-channel exchange
> involution, `delta_RF` is the unique universal diffeomorphism-natural order-zero real character
> normalized on the pure reciprocal subgroup.

The exchange extension is not a physical causal swap and is not derived on the complete flag by the
current founding sources. The formula is not unique among all smooth cocycles or after refining the
flag object.

## 6. Foundation ownership of the physical flag

The repository's earlier object and semantics audits already derived the exact distinction:

```text
abstract ordered reciprocal comparison = FOUNDING_DERIVED_ABSTRACT;
physical depth/event/coframe realization = OPEN;
complete local coframe solder = CONDITIONAL_NOT_UNIQUE;
specified-path Levi-Civita transport = METRIC_CANONICAL_MATHEMATICS;
physical endpoint-only versus path-labelled semantics = OPEN.
```

An observer clock axis can supply a timelike line. A pair/path/measurement direction can supply a
ruler line. Their span supplies the causal plane. None is a preferred global congruence: the flag
may be pair-relative. But exact composition requires the target flag of one leg to be the source
flag of the next. Independently choosing a new best plane for each leg breaks the cocycle law.

The founding postulates do not currently provide that update functor. The seven-dimensional affine
complete-coframe response bundle exists over **supplied** ordered pair frames; its existence does
not select one physical pair frame or finite lift.

## 7. The comparison-arrow audit

The conditional flag formula reads a supplied non-isometric map `A`. The metric does not uniquely
own one:

1. Levi-Civita transport composes and is metric-natural, but preserves every metric density, so
   `b1=b2=b4=delta_RF=0`.
2. Matching endpoint orthonormal coframes composes but is either isometric or depends on a selected
   endpoint gauge.
3. The differential of the exponential map is curvature-sensitive but does not compose under path
   subdivision and becomes singular at conjugate points.
4. The complete Jacobi propagator composes on an eight-dimensional state; a four-dimensional
   reduction needs extra congruence, optical, Lagrangian, or Riccati data.
5. Cartan development composes affinely, but its linear part is isometric.
6. Strain and polar maps analyze an `A` already supplied; they do not generate it.
7. First-order local diffeomorphism-natural metric connection data reduce to Levi-Civita and zero
   reciprocal-root depth.
8. At higher metric-jet order, natural nonmetric connections form unselected families.

An exact counterfamily is

```text
nabla^(c)_X Y = nabla^g_X Y
  + c[(dR)(X) Ric^sharp(Y) + (dR)(Y) Ric^sharp(X)].
```

For

```text
g=-dt^2+(1+t^2)^2 dx^2+dy^2+dz^2
```

along `t:0->1`, the supplied clock/ruler flag has

```text
ell_t=6c,
ell_r=0,
delta_RF=-3c.
```

Every constant `c` gives a different natural, compositional non-isometric path rule on a short
causal interval. Thus metric naturality and composition do not select the physical arrow.

## 8. Calibration and `c_eff`

The flag character defines an exact multiplicative transport weight

```text
Lambda_RF=exp(-2 delta_RF)=rho1^2/rho2.
```

On the pure reciprocal branch this reduces to `exp(-2delta)`, as required by the established
reciprocal readout.

But `D_t` preserves the unscaled standard flag, so it is an isotropy arrow. An ordinary scalar on
flag objects has endpoint ratio one around isotropy, while `Lambda_RF(D_t)=exp(-2t)` is nontrivial.
Therefore `Lambda_RF` is not an endpoint scalar on the bare flag object space.

It is exactly a representation on an associated reciprocal calibration line/local system. To call
it the physical `c_eff(q)/c_eff(p)` ratio requires one of:

- enriching objects with the calibration scale so `D_t` changes the object;
- restricting to a zero-period subgroupoid; or
- selecting a global trivialization when one exists.

Current sources derive none of these universally. The pure reciprocal/reference identity remains
valid in its recorded scope; the mixed complete extension is `OPEN_CONSISTENT_EXTENSION`.

## 9. The smaller missing joint

The audit does not justify inventing a new connection. It narrows the missing object to a
pair-relative reciprocal **calibration-state realization functor** of the form

```text
(complete metric/coframe,
 ordered observers and event pairing,
 admissible path/branch data)
   ->
(physical pair-relative flag,
 compositional comparison arrow,
 reciprocal calibration-line action).
```

This display specifies the type of the missing law, not its formula and not a new postulate. It must
reduce to the founded `D(delta)` character, the stationary Killing-norm ratio where that branch
exists, ordinary `c_E` calibration locally, and the working `X_max` asymptotic gate globally. It
must also state how angular/mixing data enter and what happens at causal or cut-locus degeneracies.

The founding equations already provide the abstract calibration seed. The unsolved joint is its
metric-native **solder** to the complete pair query—not a missing scalar formula inside full
`GL(4)` and not an arbitrary tangent connection.

## 10. Scope

No action, source, carrier, matter, mass, boundary functional, `X_max` value, CMB spectrum,
signalling law, or dynamics is derived. The full status and downstream corrections are recorded in
`STATUS_LEDGER.tsv` and `DOWNSTREAM_REGRADE.tsv`.
