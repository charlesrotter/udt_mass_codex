# Exact derivation — ordered observer-query projection ownership

Date: 2026-08-10

Mode: metric-led source/type audit with exact CPU algebra

Final scoped status: `VERIFIED-WITH-CAVEATS`; fresh corrected external adversarial review returned
`FOUNDED_PROJECTION_ONLY_REALIZATION_CONDITIONAL`.

## 1. Result first

The two founding postulates ask one particular kind of question: compare the clock and ruler
calibration channels reciprocally. After a complete calibrated observer query has supplied a
regular pair relation, the previous
multi-channel audit gives the complete local state

```text
(kappa, phi, beta) plus path-labelled U_gamma,
```

where `kappa` is common clock/ruler scale, `phi` is their reciprocal imbalance, `beta` records the
pairing shift, and `U_gamma` transports the angular screen along a supplied path.

When the founding clock/ruler comparison is conditionally realized on the two logarithmic density
changes

```text
(Delta_kappa, Delta_phi),
```

its unique normalized continuous real character is

```text
delta_found = Delta_phi.                                    (1)
```

This is a limited uniqueness theorem. It does not say that the complete observer reads only one
number, that `kappa`, `beta`, or `U_gamma` are unreal, or that every possible measurement is a
function of `Delta_phi`. It says that the founded reciprocal question has one scalar answer in its
declared character class. The other channels require separately typed instruments and additional
query data.

The physical pair map, physical path, regime-dependent measurement policy, on-shell/global
conductor, action, source, and dynamics remain open.

## 2. Source signature

The direct founding source starts with the dimension-matched pair

```text
q = (c_E dt, dr)
```

and an already supplied ordered signed depth. Reciprocal-`c_E`, dual Reciprocity, and continuous
composition derive

```text
D(delta) = diag(exp(-delta), exp(+delta)),
D(delta_2)D(delta_1) = D(delta_1+delta_2),
D(-delta) = D(delta)^-1.
```

The exchange matrix

```text
K = [[0,1],[1,0]]
```

interchanges the abstract clock/ruler channel labels and obeys

```text
K D(delta) K = D(-delta).
```

Thus the source owns an exchange-odd additive reciprocal character on an already supplied ordered
comparison. It does not supply common-scale measurement, event-pairing shift, angular transport,
a physical path, or a regime switch. `c_E` supplies the observed clock/length calibration and is
not an architecture selector.

## 3. The complete pair metric and its two densities

On the regular calibrated pair-metric stratum

```text
h00 < 0, det(h) < 0,
```

the unique decomposition is

```text
h = -T^2(dy0 + beta dy1)^2 + L^2(dy1)^2,
T = exp(kappa-phi),
L = exp(kappa+phi).
```

For matched endpoints `p,q`, define the clock-line and clock/ruler-area logarithmic changes

```text
b1 = log[T(q)/T(p)]                = Delta_kappa-Delta_phi,
b2 = log[T(q)L(q)/(T(p)L(p))]      = 2 Delta_kappa.           (2)
```

Hence

```text
Delta_kappa = b2/2,
Delta_phi   = b2/2-b1.                                      (3)
```

Both telescope on matched pair states. Equation (3) is the reciprocal-root readout expressed in
the pair-metric densities. Common scale cancels from the reciprocal combination; this algebraic
cancellation does not make common scale gauge and does not revive strong local CSN.

## 4. Classification of the founded density characters

The matched density group is the additive group `R^2` with coordinates

```text
(Delta_kappa, Delta_phi).
```

Every continuous homomorphism from this group to `(R,+)` is linear:

```text
chi_(a,b)(Delta_kappa,Delta_phi)
    = a Delta_kappa + b Delta_phi.                            (4)
```

This is not an assumed linear ansatz; it is the standard continuous additive-character
classification of a finite-dimensional real vector group.

Clock/ruler channel exchange sends

```text
(b1, b2-b1) -> (b2-b1, b1),
```

and therefore

```text
(Delta_kappa,Delta_phi) -> (Delta_kappa,-Delta_phi).          (5)
```

The founded reciprocal scalar is exchange odd. Applying (5) to (4) gives

```text
a Delta_kappa - b Delta_phi
  = -a Delta_kappa - b Delta_phi,
```

for all density pairs, so `a=0`. Pure reciprocal normalization requires

```text
chi(0,delta)=delta,
```

so `b=1`. This proves (1).

The theorem is precisely:

> After a complete calibrated observer query has supplied a regular pair relation, realize the
> founding clock/ruler exchange on its two matched logarithmic density changes. Among continuous
> real characters of those densities, the character that is odd under that realized exchange and
> normalized on the pure reciprocal subgroup is uniquely `Delta_phi`.

The realization remains conditional on the supplied pair metric and matched state. The theorem
does not construct that pair relation.

## 5. Why the other instruments survive

### Common scale

`Delta_kappa` is a second exact real character of the pair-metric density group. It is exchange
even, so it is not the founded reciprocal answer. It remains genuine conditional geometric state
and may be read by a common-scale or area instrument.

### Shift

`beta` is part of the unique pair-metric state, but it is not a standalone additive character. A
measurement of it needs paired events and ruler evolution. More generally, for any supplied scalar
function `f(beta)`,

```text
c_f(p,q)=f(beta_q)-f(beta_p)
```

telescopes. This supplies an infinite family of mathematical endpoint coboundaries. The founding
source does not select `f`; these measurements are possible but unowned.

This counterfamily is why no uniqueness claim may be extended from the two-density character class
to all smooth cocycles on the enriched query state.

### Angular transport

For a supplied path,

```text
U_gamma : H_p -> H_q
```

is a screen isometry and composes by matrix multiplication. It is a different codomain, not a real
scalar. A continuous homomorphism from compact `SO(2)` to `(R,+)` is trivial: periodicity forces
every real character to vanish. Therefore angular transport cannot be faithfully folded into the
founded real scalar at order zero. Loop and relative-path holonomy remain separately readable.

### Complete screen weight

The complete R17 screen action is reconstructed from `Delta_phi`, `U_gamma`, tensor variance, and
supplied `lambda`. It is a representation of retained channels, not another independent
microphone.

## 6. Phi plus orchestra is retained

Selecting `Delta_phi` as the reciprocal scalar does not return to a pure diagonal block. Complete
clock/screen and ruler/screen mixing first changes the pullback pair metric; the terminal
decomposition then extracts its `phi`.

Two exact witnesses are:

```text
h1 = diag(-3/16,4),
det(h1) = -3/4,
exp(4 phi1) = 64/3;

h2 = [[-3/16,1/12],[1/12,37/9]],
det(h2) = -7/9,
exp(4 phi2) = 1792/81,
beta2 = -4/9.
```

Thus the angular/mixing orchestra can modulate the reciprocal terminal reading and other pair-state
coordinates simultaneously. The scalar projection occurs after the complete pair geometry is
formed.

## 7. The precise nonuniqueness boundary

The following statements are compatible and must not be conflated:

1. `Delta_phi` is unique inside the founded continuous two-density character class.
2. The complete supplied geometry contains other typed instruments.
3. Arbitrary endpoint coboundaries survive in a broader enriched-state groupoid.
4. The founding postulates do not own those extra measurement functions.
5. A future physical observer may read multiple channels, perhaps in a branch- or regime-dependent
   way, but no such policy has been derived.

The result therefore answers the bounded ownership question without deriving a universal complete
measurement law.

## 8. Calibration and downstream boundary

- `c_E`: observed terminal clock/ruler calibration; active.
- `G_obs`: observed but inactive here because no native mass readout is present.
- electron mass: unapplied future calibration candidate.
- `hbar`: excluded.
- strong local CSN: inactive; `kappa` is retained.

No coefficients, thresholds, regimes, or physical channel weights were fitted. Nothing here
selects a path, physical pair relation, on-shell branch, bootstrap conductor, action, source,
matter law, `X_max` value, CMB observable, signalling rule, or dynamics.

## 9. Bounded landing

```text
FOUNDED_PROJECTION_ONLY_REALIZATION_CONDITIONAL__AFTER_A_COMPLETE_CALIBRATED_QUERY_SUPPLIES_
THE_REGULAR_PAIR_RELATION_Delta_phi_IS_UNIQUE_WITHIN_THE_CONTINUOUS_REAL_TWO_DENSITY_
CHARACTER_CLASS__COMMON_SCALE_SHIFT_AND_
ANGULAR_TRANSPORT_REMAIN_SEPARATELY_TYPED_CONDITIONAL_INSTRUMENTS__ARBITRARY_ENRICHED_STATE_
ENDPOINT_COBBOUNDARIES_SURVIVE_BUT_ARE_NOT_FOUNDING_OWNED__PHI_PLUS_ORCHESTRA_RETAINED__
PHYSICAL_PAIR_MAP_PATH_MULTICHANNEL_MEASUREMENT_REGIME_POLICY_CONDUCTOR_ACTION_SOURCE_AND_
DYNAMICS_OPEN.
```
