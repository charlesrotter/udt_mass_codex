# Exact derivation — same-solution founded depth and curvature

## 1. Typed objects

The founded reciprocal object is

```text
H = diag(-1,+1,0,0),
D(phi) = exp(phi H),
D(phi_2)D(phi_1) = D(phi_1+phi_2).
```

This pair algebra is `DERIVED`. The local complete-coframe realization tested here is the registered
positive-triangular architecture

```text
E(phi,D,S) = [[D(phi), 0],
              [D S,    D]],
theta = E bar_theta.
```

The architecture is supplied; it is not a selected physical section. The reference coframe
`bar_theta` is therefore kept visible throughout.

## 2. Exact factorization redefinition

Define

```text
L_chi = diag(D(chi),I_2).
```

Then the simultaneous redefinition

```text
phi'       = phi + chi,
S'         = S D(chi),
bar_theta' = L_chi^-1 bar_theta
```

obeys the exact identity

```text
E(phi+chi,D,S D(chi)) L_chi^-1 = E(phi,D,S).
```

Thus `theta` and the metric are unchanged. This is an exact redundancy of the displayed
factorization when the reference presentation is not fixed. It is not being asserted as a derived
physical gauge principle. Its narrower consequence is decisive: the complete coframe alone cannot
identify which part of this factorization is `phi` without a separately owned reference/section
rule.

## 3. Complete product jets

For `theta=E bar_theta`, the first and second partials are

```text
theta_,mu = E_,mu bar_theta + E bar_theta_,mu,

theta_,munu = E_,munu bar_theta
            + E_,mu bar_theta_,nu
            + E_,nu bar_theta_,mu
            + E bar_theta_,munu.
```

At the identity, the founded contribution is

```text
E_,mu   = p_mu H,
E_,munu = q_munu H + p_mu p_nu H^2.
```

All product-rule cross terms are retained. With all eight registered factorized chart directions
and an arbitrary 16-component reference-coframe jet, the per-coordinate first-jet map is

```text
24 inputs -> 16 complete-coframe outputs,
rank = 16,
nullity = 8.
```

Across four coordinate directions this is rank 64 and nullity 32. One explicit kernel vector is

```text
delta p_mu = 1,
delta(extension jets) = 0,
delta bar_theta_,mu = -H,
```

which leaves `theta_,mu` unchanged. With first jets fixed, the same coefficient map acts in every
symmetric second-derivative slot. Across ten slots it has rank 160 and nullity 80, including the
explicit founded-Hessian kernel `delta q_munu=1`, `delta bar_theta_,munu=-H`.

Constructively, for any desired complete-coframe jets `X_mu,T_munu` and any supplied factorized
parameter jets,

```text
B_mu   = X_mu - A_mu,
B_munu = T_munu - E_munu - A_mu B_nu - A_nu B_mu
```

chooses reference jets yielding the same complete-coframe jet. This is non-identifiability, not a
selection theorem.

## 4. Curvature coefficient map

At a regular point, the second-derivative part of the Riemann tensor is

```text
R_abcd = 1/2 (g_ad,bc + g_bc,ad - g_ac,bd - g_bd,ac)
         + b_abcd(g,g_first),
```

where `b` is the connection-quadratic first-jet offset. Therefore at fixed zero jet and fixed first
jets,

```text
R = A(generator Hessians) + b(fixed first jets).
```

The matrix `A` does not depend on `dphi`. First-jet amplitude and causal type can move the affine
origin but cannot change the Hessian image rank on this regular tile.

The algebraic Riemann target is represented by 21 symmetric bivector-pair entries with one exact
algebraic Bianchi relation, hence dimension 20.

## 5. Frozen-reference family ranks

Every allowed generator receives all ten symmetric Hessian slots. Exact rational ranks are:

| Family | Generators | Rank | Codimension in algebraic Riemann space |
|---|---:|---:|---:|
| F01 full factorized | 8 | 20 | 0 |
| F02 determinant-one screen | 7 | 20 | 0 |
| F03 founded + four mixing | 5 | 19 | 1 |
| F04 founded + three screen | 4 | 19 | 1 |
| F05 founded spectator | 1 | 8 | 12 |
| F06 locked founded/angular field | 1 | 10 | 10 |
| F07 locked founded/shift field | 1 | 10 | 10 |
| F08 released complete coframe/reference | 10 metric tangents | 20 | 0 |
| F09 independent scalar control | no metric action | not typed | not typed |

For F01, F02 and F08, exact 20-by-20 invertible minors and their rational inverses are preserved in
`RIGHT_INVERSE_WITNESSES.json`. They prove surjection onto the full algebraic Riemann target.

The two codimension-one restrictions have simple representatives:

```text
F03: R_2323 = 0,
F04: R_0123 = 0,
```

with the universal Bianchi relation still imposed. These restrictions are local to the registered
families; they are not UDT field equations.

The one-parameter locked families are a useful nontrivial result. Locking angular shear or a
base-screen shift to the founded field raises the image from the spectator rank 8 to rank 10. This
shows an actual reciprocal/angular or reciprocal/mixing interaction at the curvature level, but it
does not make either lock unique or complete.

## 6. Causal strata and same-solution existence

The exact representatives retained are

```text
zero       p=(0,0,0,0),
timelike   p=(1,0,0,0),
spacelike  p=(0,1,0,0),
null       p=(1,1,0,0).
```

For every typed family, the rank is identical in all four strata. This does not say that the full
curvature tensor is independent of `p`; the first-jet offset generally changes. It says the
attainable curvature affine space has the same direction space.

Consequently:

- in F01 and F02, any fixed founded first jet and any algebraic Riemann tensor admit at least one
  local factorized two-jet carrying both in the same supplied realization;
- in F03-F07, the same statement holds only for the exact lower-dimensional image listed above;
- in F08, arbitrary factorization-depth jets can coexist with any complete-coframe two-jet, but this
  is precisely the released-reference non-identifiability;
- F09 has no curvature map because none was supplied or invented.

## 7. What the join does and does not establish

This closes the parent atlas's narrow algebraic caveat: the depth and curvature axes need not belong
to different local solutions. The registered factorized architectures contain explicit
same-solution witnesses.

It does **not** close the ownership caveat. The founded pair algebra still does not provide a
frame-independent rule assigning `phi(x)` and its jets to a complete metric. Nor does local
surjection select one extension family, one curvature, a response/evolution law, action, source,
boundary, global completion, bootstrap return, or matter branch.

The exact bounded outcome is therefore:

```text
DERIVED_FACTORIZATION_NONIDENTIFIABILITY
CONDITIONAL_FULL_LOCAL_PHI_CURVATURE_COMPATIBILITY_IN_F01_F02
DERIVED_RESTRICTED_FAMILY_CODIMENSIONS
NO_METRIC_NATIVE_PHI_ASSIGNMENT_OR_CURVATURE_SELECTION
```
