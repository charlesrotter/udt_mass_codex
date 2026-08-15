# Exact derivation — native flux/luminosity-law ownership

Date: 2026-08-15

## 1. Types and notation

Supply one regular complete metric history, one ordered source/observer query, and one regular null
branch. Let `u_s,u_o` be the endpoint observer velocities and let `k` be the affinely transported
null tangent used by the query. Define

```text
omega_s = -g(k,u_s),
omega_o = -g(k,u_o),
Z       = omega_s/omega_o = exp(phi_pair) > 0.
```

The last equality is the registered conditional SNe readout. The complete pair evaluator determines
`phi_pair` after all `B,Q,S,Y,Z_pair` channels have entered its induced two-metric. This section does
not identify the null query with a material signal.

Let `D_f:S_o -> S_s` be the forward two-screen Jacobi map normalized at the observer and let
`D_r:S_s -> S_o` be the source-normalized reverse map on the same geometric branch. Define

```text
d_A^2 = |det D_f|,
d_G^2 = |det D_r|.
```

`d_A` is the observer-angle to source-area distance. `d_G` is the source-angle to receiver-area
distance. They are different geometric types.

## 2. General forward/reverse screen reciprocity

In a parallel screen basis the Jacobi equation has the form

```text
D'' = T D,
```

where the optical tidal matrix `T` is symmetric by the algebraic symmetries of the Levi-Civita
curvature. For two solutions `D_f,D_s`, define the matrix Wronskian

```text
W = D_s^T D_f' - D_s'^T D_f.
```

Then

```text
W' = D_s^T T D_f - (T D_s)^T D_f = 0.
```

Evaluating at the two endpoints with zero-position/unit-derivative boundary conditions gives the
transpose relation between the unscaled endpoint maps. Reversing the whole affine tangent and
renormalizing it to unit source frequency introduces the factor `Z`. Up to orthogonal endpoint
screen-basis overlaps and an orientation sign,

```text
D_r = Z O_o D_f^T O_s.
```

Since `|det O_o|=|det O_s|=1` on the positive screen,

```text
|det D_r| = Z^2 |det D_f|,
d_G       = Z d_A.                                      (1)
```

Equation (1) is a conditional geometry theorem on the regular query stratum. It retains arbitrary
time dependence, anisotropic screen curvature, shear, rotation, and complete metric mixing inside
`D_f`. It is not a source or luminosity law. G80/G81 are bounded numerical witnesses of this
Wronskian structure, not its only basis.

## 3. The endpoint clock factor

For two corresponding phase labels or wavefront markers,

```text
omega = d phase / d tau.
```

Therefore the registered frequency ratio gives

```text
d tau_o / d tau_s = omega_s/omega_o = Z,
d tau_s / d tau_o = 1/Z.                                (2)
```

This is a clock/frequency statement. It does not say how much physical energy one marker carries.

## 4. Exact flux factorization

Avoid source isotropy by using the differential emitted luminosity

```text
L_Omega = dE_s/(d tau_s d Omega_s).
```

Let

```text
eta     = surviving carried amount / emitted carried amount,
epsilon = observer energy per carried unit / source energy per carried unit.
```

These are positive transfer readouts. They are deliberately not assigned by geometry. A source
solid angle maps to receiver area by

```text
dA_o = d_G^2 dOmega_s.
```

Consequently the received bolometric flux is exactly

```text
F_o
 = L_Omega eta epsilon (d tau_s/d tau_o) / d_G^2
 = L_Omega eta epsilon / (Z^3 d_A^2).                    (3)
```

Thus the supplied metric/query owns three powers of `Z` conditionally: two from reverse screen
area and one from endpoint clock rate. It does not by itself own `eta epsilon`.

If source isotropy is separately supplied, `L_s=4 pi L_Omega`, and luminosity distance is defined by

```text
F_o = L_s/(4 pi d_L^2).
```

Equation (3) gives

```text
d_L^2 = Z^3 d_A^2/(eta epsilon).                         (4)
```

This definition does not derive isotropy or intrinsic source luminosity.

## 5. Exact nonuniqueness under composition and reversal

On a matched observer network, endpoint frequency ratios multiply:

```text
Z_AC = Z_AB Z_BC,
Z_BA = 1/Z_AB.
```

For every real pair `(p,q)`, the positive continuous transfer laws

```text
epsilon_p(Z) = Z^(-p),
eta_q(Z)     = Z^(-q)
```

also compose and reverse exactly. Substitution into (4) gives the family

```text
d_L = Z^[(3+p+q)/2] d_A.                                (5)
```

Every member sees the same complete pair metric, `phi_pair`, redshift, forward screen map, reverse
screen map, and middle-state composition. Therefore endpoint composition, Reciprocity, and complete
angular/mixing geometry do not select `p+q`.

This is a constructive nonuniqueness theorem, not merely an absence-of-search statement.

More generally, composition and reversal alone permit any positive multiplicative character
`chi:R_>0 -> R_>0`. Writing `f(x)=log chi(exp(x))` turns this into the additive Cauchy equation.
Continuity, measurability, or local boundedness forces `f(x)=-p x`, so the power laws above are the
complete regular character family. Without such regularity, pathological additive characters also
survive. The displayed regular family is already sufficient to disprove kinematic uniqueness.

The same nonselection exists locally. On two finite cross-sections of a regular ray pencil, let
`A` be its positive screen area and let `n` be a positive carried density. Every real `a` defines
the covariant local transport family

```text
d(log n) = -a d(log A).
```

The carried amount changes as

```text
n_2 A_2/(n_1 A_1) = (A_2/A_1)^(1-a),
```

and these ratios compose for every `a`. The special value `a=1` is exactly conservation of carried
amount. The metric supplies `A` and its expansion; it does not turn `a=1` into an identity. That is
an evolution/current statement.

## 6. Conditional closures

The historical relation follows from the explicit pair of extra statements

```text
eta = 1,          conserved carried count or wave action,
epsilon = 1/Z,   carried energy is endpoint null-momentum/frequency energy.
```

Then

```text
F_o = L_Omega/(Z^4 d_A^2),
d_L = Z^2 d_A.                                           (6)
```

A massless-particle realization can obtain `epsilon=1/Z` by supplying a physical null momentum and
defining measured energy as `-p.u`. A geometric-optics wave realization can obtain both statements
from a selected wave action and its amplitude/current equation. Current UDT authority owns neither
material realization universally. The conditional toric identity `F=dS`, `dF=0` supplies no
inhomogeneous field equation, radiative current, stress tensor, source coupling, or normalization.

Other transfer characters are equally compositional until such a law is supplied. For example,
`eta=1, epsilon=1` gives `d_L=Z^(3/2)d_A`; `eta epsilon=Z` gives `d_L=Z d_A`. These are mathematical
countermodels to uniqueness, not proposed physical laws.

## 7. Historical regrade

- The current registered `d_L=Z^2 d_A` relation is **compatible** with the complete metric geometry.
  It is not contradicted by the rebuilt kernel.
- Its geometry portion is stronger than previously recorded: equations (1)--(4) isolate exactly
  what the complete metric/query owns.
- The July claim that the full relation was forced by a metric-selected minimal Maxwell sector is
  superseded by current G13/G16/G21 ownership. The action, current, carrier, source, measure, and
  normalization remain open.
- Calling the historical one-power implementation an arithmetic error is valid only inside the
  additional transparent null-momentum closure. It is not a metric-only theorem.

## 8. Landing

```text
VERIFIED_WITH_CAVEATS__GEOMETRIC_RECIPROCITY_AND_THREE_Z_POWERS_DERIVED_CONDITIONALLY
__RADIATIVE_TRANSFER_PRODUCT_ETA_EPSILON_NOT_SELECTED
__HISTORICAL_DL_EQUALS_Z2_DA_COMPATIBLE_CONDITIONAL_CLOSURE
```

This result is scoped to one regular branch of a supplied complete history/query. Caustics,
multiple-image aggregation, absorption/scattering, source anisotropy, detector bandpass, intrinsic
luminosity, physical history selection, and global completion remain outside the theorem.
