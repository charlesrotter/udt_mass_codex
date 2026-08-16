# Exact derivation — complete sky/depth reference projection

Date: 2026-08-15

## 1. Bounded landing

```text
COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY
__PURE_RADIAL_MODULATION_REMOVED
__DEPTH_DEPENDENT_ANGULAR_RESPONSE_SURVIVES
__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED
__PHYSICAL_HISTORY_AND_OUTCOMES_OPEN
```

G106 derives the mathematical bridge from G105's local complete-pair Jacobian to a complete
sky/depth density and then through the idealized BOSS DR12 random-reference construction. It does
not select the physical complete metric history or compare a curve with data.

The decisive refinement is:

> Changing only the number of observed objects with depth is removed by the registered angular
> shell normalization and by random redshifts drawn from the observed redshift marginal. A physical
> artifact survives only when the conditional angular response is nontrivial; its amplitude or
> shape may vary with depth according to one common history.

## 2. Complete sky/depth map

Let `(Sigma,gamma)` be a supplied three-dimensional source-label space. For one supplied complete
history and typed observer relation, the banked evaluator gives

```text
E=[[B,0],[Q S,Q]],
J=[Y;Zeta],
V=EJ,
h=V^T eta_4 V,
Psi(a)=(zeta(a),n(a)),
zeta=DeltaPhi.
```

Every complete channel enters through `V` and its source-label differential before `zeta,n` are
read. On the observer target

```text
X=I_zeta x S_O^2,
G_X=d zeta^2+q_S2,
mu_X=d zeta dOmega.
```

The pullback metric on `Sigma` is

```text
M_AB=(D_A zeta)(D_B zeta)+q_S2(D_A n,D_B n).          (1)
```

On a regular branch,

```text
J_Psi=sqrt(det M/det gamma).                           (2)
```

Under a source-coordinate change with derivative `C`, both determinants acquire `det(C)^2`, so
their ratio is unchanged. The exact rational witness gives the same ratio

```text
323062/260925
```

before and after a nontrivial basis change with `det C=2`.

For a finite-to-one branch family and proper source density `rho`, the observed one-point density
relative to `mu_X` is

```text
p(zeta,n)=sum_(a in Psi^-1(zeta,n)) rho(a)/J_Psi(a).   (3)
```

Equation (3) is conditional on the supplied history, relation family, branch weights, and source
density. It is not yet a UDT cosmology.

## 3. The BOSS-style reference as a projection

Fix one registered sample and Galactic cap. Let `s(n)` be the normalized official angular
footprint/completeness density,

```text
integral_S2 s(n)dOmega=1.
```

For a normalized observed one-point density `p`, define its depth marginal and the ideal reference
operator

```text
p_zeta(zeta)=integral_S2 p(zeta,n)dOmega,
(R_s p)(zeta,n)=p_zeta(zeta)s(n).                      (4)
```

Equation (4) types the documented construction in which angular randoms sample the accepted
footprint/completeness and random `Z` values are drawn from observed galaxy redshifts. It is an
ideal expectation operator; finite random noise and detailed weighting remain separate.

The operator is positive, mass preserving, and idempotent:

```text
R_s^2=R_s.                                             (5)
```

Its exact range and kernel are

```text
range(R_s)={f(zeta)s(n)},
kernel(R_s)={r: integral_S2 r(zeta,n)dOmega=0 for every zeta}.  (6)
```

Thus every density has the unique direct-sum decomposition

```text
p=p_zeta s+r,
R_s p=p_zeta s,
integral_S2 r dOmega=0.                               (7)
```

This is a projection, not an orthogonality claim. No inner product has been selected.

Where `p_zeta s>0`, write

```text
p=p_zeta s(1+m),
integral_S2 s(n)m(zeta,n)dOmega=0.                    (8)
```

The physical-versus-instrumental ownership of `m` remains open. G106 only derives which type is
visible to the measurement.

## 4. Exact shell/window projection

For a redshift/depth window `W` and nonnegative registered data weight `w(zeta)`, normalize the
angular data density:

```text
p_W(n)
 = [integral_W w(zeta)p(zeta,n)d zeta]
   /[integral_W w(zeta)p_zeta(zeta)d zeta].            (9)
```

The ideal factorized random reference gives

```text
q_W(n)=s(n).                                           (10)
```

Using (8),

```text
p_W=s(1+m_W),
m_W(n)
 = [integral_W w p_zeta m(zeta,n)d zeta]
   /[integral_W w p_zeta d zeta].                     (11)
```

Consequences:

1. If `m=0`, any change in the radial marginal `p_zeta` is removed exactly. Distance-dependent
   total abundance alone cannot create the normalized angular pair curve.
2. If `m=a(zeta)u(n)` with `integral s u=0`, then

   ```text
   m_W=bar(a)_W u.                                     (12)
   ```

   One depth-dependent amplitude produces different window amplitudes without per-window fitting.
3. If several angular modes are active,

   ```text
   m=sum_l a_l(zeta)u_l(n),
   m_W=sum_l bar(a_l)_W u_l(n).                        (13)
   ```

   Their relative loudness can change both amplitude and shape across windows. The functions
   `a_l` must all come from the same complete history.

For an angular bin kernel `I_k`, the factorized-source Landy--Szalay expectation becomes

```text
w_(W,k)
 = [integral I_k s(n1)s(n2)m_W(n1)m_W(n2)dOmega1dOmega2]
   /[integral I_k s(n1)s(n2)dOmega1dOmega2].           (14)
```

For (13), equation (14) is the quadratic form

```text
w_(W,k)=sum_(l,m) bar(a_l)_W bar(a_m)_W C_(k,lm).      (15)
```

This is the precise mathematical version of regime-dependent instrument loudness. It is also a
cross-dataset constraint: every survey window must be an average of the same history, after its own
documented selection and weighting. Independent window retuning is forbidden.

## 5. Exact full-sky loud--quiet--loud witness

This witness proves existence in the regular sky/depth map class; it does not select a physical
history. Let `t in [0,1]`, `mu=cos(theta)`, and let the reference sky be uniform. Define

```text
a(t)=(2t-1)^2/4,
P2(mu)=(3mu^2-1)/2,
mu_source=mu_observer + a(t)(mu_observer^3-mu_observer)/2.  (16)
```

The map fixes both poles. Its angular Jacobian is

```text
d mu_source/d mu_observer=1+a(t)P2(mu).                (17)
```

Since `0<=a<=1/4`, the density ratio lies between `7/8` and `5/4`; hence the map is positive and
regular everywhere. Because `integral_-1^1 P2(mu)dmu=0`, every depth slice is normalized.

For the three equal windows `[0,1/3]`, `[1/3,2/3]`, and `[2/3,1]`, the exact mean amplitudes are

```text
13/108, 1/108, 13/108.                                (18)
```

For two directions with cosine separation `c`, rotational averaging gives

```text
<P2(n1.z)P2(n2.z)>_rotation=P2(c)/5=(3c^2-1)/10.      (19)
```

Therefore the outer-window pair amplitude is exactly `169` times the middle-window amplitude. One
smooth function creates the loud--quiet--loud change; no window has its own parameter.

The witness does not prove that UDT selects `P2`, this amplitude, these windows, or this history.
G105 proved that the complete `B,Q,S,Y,Zeta` arena can contribute to a local nonconstant Jacobian.
G106 proves the global map/reference consequences. Their realization by one selected complete
metric history remains open.

## 6. What survives and what does not

- **Removed:** pure radial abundance, common normalization, and any component already encoded in
  the registered angular footprint/completeness reference.
- **Survives conditionally:** angular modulation at fixed depth, depth-dependent angular amplitude,
  changing angular mode mixtures, and branch-summed one-point structure not represented by `s`.
- **Separate owner:** finite random shot noise, incorrect completeness, weight mismatch, or
  redshift--angle coupling in the survey construction.
- **Not addressed by `R_s`:** a genuine nonfactorizing two-source term `H`; it remains open and is
  not required for the G105/G106 one-point artifact route.

## 7. Certification ceiling

Production SymPy algebra, an independent Fraction-only implementation, and twelve hostile mutations
all pass. Executable outcome-read ledgers are empty. The result defines a falsifiable architecture,
not a BAO result: a physical complete history, source law, actual finite reference projection,
global branches, coefficients, and every comparison with BOSS or CMB remain open.
