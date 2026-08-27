# G279 exact bounded rederivation

Date: 2026-08-27

This derivation is deliberately separated into native/mixed-status geometry and downstream
observational interfaces. It does not use P1, G116, G189, a fitted kernel profile, a preferred
resolution, `X_max`, a Lambda-CDM distance law, or any protected package.

## 1. Founded reciprocal character on supplied depth

For the positive diagonal comparison representation

```text
P(delta) = diag(u(delta), v(delta))
K        = [[0,1],[1,0]],
```

Dual Reciprocity gives

```text
P^T K P = K  =>  u v = 1.
```

With the separately posited additive composition and reversal laws, plus the registered regularity
and nontriviality assumptions, the normalized character is

```text
D(delta) = diag(exp(-delta), exp(+delta)).
```

Status: `DERIVED_ON_SUPPLIED_ORDERED_DEPTH`. The event/observer/history-to-depth assignment is not
derived by this step.

## 2. Declared primary metric readout

The declared quadratic Lorentzian coframe readout and declared areal angular sector give

```text
ds^2 = -exp(-2 phi) c_E^2 dt^2 + exp(+2 phi) dr^2 + r^2 dOmega^2.
```

Status: `DERIVED_AFTER_DECLARED_READOUT`. This fixes the reciprocal metric form, not the values of a
global history `phi`.

## 3. Complete pair pullback before readout

On a supplied regular complete coframe and supplied pair germ,

```text
E = [[B, 0], [Q S, Q]]
J = [[Y], [Z]]
h = J^T E^T eta_4 E J
  = Y^T B^T eta_2 B Y + (S Y + Z)^T Q^T Q (S Y + Z).
```

Thus base, screen, angular, and mixing information enters the pair metric `h` before any terminal
scalar is read. This is the native ordering. It does not imply that every spatial/angular change
must alter `h_00`; angular response is a metric sibling channel, not a scalar correction appended
after redshift.

Status: `DERIVED_CONDITIONAL` on the supplied metric/coframe, query, and regular pair germ.

## 4. Completed-pair Dual Reciprocity

For

```text
h = -T^2 (d tau + beta d sigma)^2 + L_sigma^2 d sigma^2,
```

the exact identities are

```text
T^2 = -h_00
beta = h_01 / h_00
L_sigma^2 = h_11 - h_01^2 / h_00
T^2 L_sigma^2 = -det(h).
```

The working completed-pair premise W1 chooses

```text
m = T L_sigma = sqrt(-det(h)),
```

so the normalized pair determinant is `-1` and

```text
Phi = -log(T/T_star).
```

Status: the decomposition is `DERIVED_CONDITIONAL`; W1 is a
`WORKING_FOUNDATIONAL_CLARIFICATION`, not a bare-metric theorem or canon.

## 5. Endpoint-relative depth and direct redshift

For a supplied completed source-observer comparison,

```text
delta_AB = -log(d tau_B / d tau_A).
```

On the supplied redshift query this gives

```text
log(1+z) = Phi_source - Phi_observer.
```

In the founded radial block with the observer reference fixed,

```text
h = diag(-exp(-2 delta), exp(+2 delta)),
Phi = delta,
chi = tanh(delta).
```

The direct redshift edge needs no angular correction, luminosity law, distance profile, P1, or
`X_max`. It remains conditional on the source-observer query and is not a complete theory of light
or flux.

## 6. Exact observational import boundary

G236 then introduces a declared transparent-transfer interface:

```text
d_A = R
d_L = (1+z)^2 R.
```

Only after that import does

```text
y = m - 10 log10(1+z) = 5 log10(R) + offset
```

become the observational relative-area reconstruction used by the SNe code. The piecewise-linear
`K = 8,12,16,24` hat families are a `DECLARED_NUMERICAL_REPRESENTATION` of this downstream state,
not alternative reciprocal kernels.

G278 adds the published Cepheid ladder and same-operational-distance bridge to attach

```text
ell/Mpc = 10^(a/5),
```

then compares the frozen state to the published DES `MU` release without retuning. These are
`OBSERVED` and `CONDITIONAL` observational interfaces. They do not alter any equation in Sections
1--5.

## 7. Projective and angular dependency result

The G271--G275 projective/W5 chain and the metric-null-screen angular/Jacobi chain remain meaningful
native/mixed-status sibling developments. Static source and AST tracing show that neither is
executed by the G236 or G278 SNe programs. Therefore G278 cannot certify, fit, or corrupt either
one. It tests only the direct-redshift plus imported-transfer observational route.

The G278 historical `PREMISE_LEDGER.tsv` marks `completed_pair_projective_state` as used. That is too
broad for executable provenance. G279 preserves the historical file and records the repair here:
W5 is conceptually adjacent but not a numerical dependency of G278.

## 8. Subtraction theorem for the bounded chain

The registered graph subtractions establish:

- remove transparent transfer: Sections 1--5 survive; the SNe area curve, scale, and holdout do not;
- remove the G236 hat representation: the native chain and imported formula survive; the frozen
  numerical state and G278 outputs do not;
- remove the Cepheid/optical attachment: the relative state survives; the absolute scale and DES
  holdout do not;
- remove W5 or the angular sibling: G278 is unchanged;
- remove W1: the general completed scalar and its downstream endpoint/redshift semantics fail,
  while the supplied metric and pair pullback remain;
- remove the founded reciprocal character: the full downstream reciprocal chain fails.

This proves a source-bounded dependency separation. It is not a proof that W1 or W5 is necessary in
Nature, that the imported transfer law is native, or that the G236 finite representation is the
unique physical area history.
