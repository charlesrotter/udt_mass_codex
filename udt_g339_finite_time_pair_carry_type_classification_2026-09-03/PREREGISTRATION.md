# G339 preregistration — finite-time pair-carry type classification

Date: 2026-09-03
Status: preregistered before production code or result artifacts

## Frozen metric and bounded regime

Use only the exact G338 spacetime

```text
g=-dT^2+a_X(T)^2 dX^2+a_perp(T)^2(dy^2+dz^2),
a_X/a_X0=u^(-1/3), a_perp/a_perp0=u^(2/3), u=T/T0>0.
```

Keep the supplied normal congruence `n=partial_T`, every initially unit spatial direction with
longitudinal squared fraction `rho in [0,1]`, and every finite initial rapidity `z`. No carry is
declared physical.

## Candidate carry family

For the diagnostic interpolation parameter `lambda in [0,1]`, define coordinate components

```text
J_lambda^i(T)=J_0^i [a_i(T0)/a_i(T)]^lambda.
```

Then `lambda=0` is the G338 commuting/Lie connecting field and `lambda=1` is Levi-Civita parallel
carry along `n`. The candidate squared-length ratio is

```text
G_lambda(u,rho)
 =rho*u^(-2(1-lambda)/3)+(1-rho)*u^(4(1-lambda)/3).
```

With `c=cosh(z)`, `s=sinh(z)`, and the boost coefficients held fixed in the carried normal-spatial
pair, test whether the full G338 formulas remain valid after `G -> G_lambda`:

```text
h00=-c^2+G_lambda*s^2
h01=(G_lambda-1)*s*c
h11=-s^2+G_lambda*c^2
det(h)=-G_lambda
Delta=c^2-G_lambda*s^2.
```

Apply W1 only after the complete pullback is formed.

## Required exact classifications

1. Derive the transport identity

   ```text
   (1/2)n[g(V,V)]
    =(1/2)(L_n g)(V,V)+g([n,V],V),
   ```

   and identify the geometric deformation endomorphism
   `H=(1/2)gamma^(-1)L_n gamma`.
2. Show that commuting carry has `[n,J_0]=0`, parallel carry has
   `[n,J_1]=-H J_1`, and a norm-preserving rotating carry has
   `[n,V]=Omega V-HV` with `Omega` spatially skew.
3. Cover analytically every `u>0`, `rho in [0,1]`, `lambda in [0,1]`, and finite `z` on the
   derived `Delta>0` clock-timelike stratum.
4. At `lambda=1`, determine whether the full raw pair and terminal readouts stay quiet for all
   time. At `lambda<1`, determine the unique initially first-order-silent direction and its exact
   finite-time behavior.
5. For nonzero boost and `0<=lambda<1`, classify endpoint and mixed-direction clock-timelike
   intervals. The preregistered endpoint candidates are

   ```text
   rho=1: u>tanh(|z|)^[3/(1-lambda)]
   rho=0: u<coth(|z|)^[3/(2(1-lambda))].
   ```

6. Show that Fermi-Walker carry along geodesic `n` equals parallel carry. For each principal
   direction `e_i`, test the explicit constant-rapidity accelerated pair

   ```text
   U=c*n+s*e_i, S=s*n+c*e_i,
   acceleration=H_i*s*S, nabla_U S=H_i*s*U,
   ```

   and its pair Gram matrix.
7. Determine whether a scalar of the raw `2x2` component matrix alone survives arbitrary smooth
   invertible pair-frame congruence, and whether the typed pair-plus-carry state recovers
   `L_n g` after subtracting transport.
8. Keep the fixed-normal metric invariants separate from carry: the candidate eigenvalues are
   `(-1,2,2)/(3T)`, with dimensionless ratios independent of the pair carry.

## Candidate landings

- **A:** `RAW_COMPLETED_PAIR_RESPONSE_IS_INVARIANT_UNDER_ALL_NATURAL_CARRIES`.
- **B:** `FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY__NO_PHYSICAL_CARRY_SELECTED`.
- **C:** `ALL_G338_FINITE_TIME_RESPONSE_IS_A_PURE_FRAME_ARTIFACT_WITH_NO_RECOVERABLE_METRIC_DEFORMATION`.
- **D:** `THE_METRIC_UNIQUELY_SELECTS_COMMUTING_LIE_CARRY_AS_THE_PHYSICAL_PAIR_POPULATION`.

No candidate is privileged before execution.

## Certification and falsification contract

Production must independently reconstruct the connection, carry family, pullback, W1 outputs,
silent stratum, regular intervals, Fermi/accelerated controls, and carry-corrected deformation.
Finite rational cases are controls; analytic identities own continuous coverage. An
implementation-distinct verifier may use direct floating matrices and finite differences but may
not import production code or read its result.

Hostile checks must catch at least: dropped carry term; Lie carry mislabeled parallel; parallel
carry mislabeled connecting separation; Fermi distinguished from parallel on geodesic `n`;
orthonormal quietness promoted to zero geometry; acceleration treated as metric-selected; a wrong
`lambda` endpoint; terminal scalar called carry invariant; a selected observer population; and a
scale or `X_max` promotion.

Maximum grade before fresh external review is
`INDEPENDENTLY_VERIFIED_DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW`.
