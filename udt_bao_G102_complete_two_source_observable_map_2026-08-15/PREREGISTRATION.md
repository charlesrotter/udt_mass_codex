# G102 preregistration — complete observer-plus-two-source BAO observable map

Date: 2026-08-15

Status:

```text
PREREGISTERED
__NO_BAO_CURVE_OR_DESCRIPTOR_READ
__EVALUATOR_DERIVATION_ONLY
```

## Whole question

For one calibrated observer and two supplied complete observer--source pair realizations, what exact
metric-native map produces the redshift and angular-separation arguments consumed by the already
frozen BOSS observer-coordinate estimator?

This is a metric-led evaluator question. It does not ask the geometry to manufacture a preferred
angle, ruler, oscillation, source distribution, or desired BAO curve.

## Bounded arena

For each source label `a in {1,2}`, supply the complete regular pair data

```text
E = [[B,0],[Q S,Q]],
J_a = [Y_a;Z_a],
V_a = E J_a = [v_a0,v_a1],
h_a = V_a^T eta_4 V_a.
```

Require

```text
(h_a)00 < 0,
det(h_a) < 0.
```

The two pair relations must share one calibrated observer clock after normalization. This is a
query-typing condition, not a preferred global congruence.

The candidate endpoint map to be derived is

```text
T_a = sqrt(-(h_a)00),
u_a = v_a0/T_a,
r_a = v_a1 - ((h_a)01/(h_a)00) v_a0,
L_a = sqrt((h_a)11-(h_a)01^2/(h_a)00),
n_a = r_a/L_a,
phi_a = (1/4) log[(-det h_a)/(h_a)00^2],
Zobs_a = exp(phi_a),
cos(theta_12) = g(n_1,n_2),
```

conditional on `u_1=u_2` in the common observer calibration.

The normalized `n_a` is derived as the positive direction inside the supplied pair plane. Its
identification with the catalogued source direction additionally requires the ordered query to
declare the second channel as the observer-to-source ruler and to fix its outward sign. The metric
does not infer that measurement convention from a bare pair plane.

The exact pair counts and Landy--Szalay estimator will then be typed as a deterministic functional
of the evaluated `(Zobs_a,n_a)` catalog, the frozen observational weights, mask/random catalog, and
angular bins.

## Premise ledger in words

- Complete `E,J_a` histories: `FREE_AND_EXPLORED` as symbolic regular inputs; no history is selected.
- Common observer clock: `PINNED_BY_QUERY_SEMANTICS`; without it the two directions do not inhabit one
  observer sky.
- `Zobs=exp(phi_pair)`: `OBSERVED_CONDITIONAL_G99` in the frozen middle regime.
- Direction normalization: candidate `DERIVED_FROM_COMPLETE_PAIR_VECTORS`; identification and
  outward orientation as the observed source direction: `PINNED_BY_ORDERED_QUERY_SEMANTICS`.
- BOSS directions, redshifts, weights, masks, bins, and randoms: `OBSERVED` frozen measurement data.
- Landy--Szalay: `BORROWED_CATEGORY_A_ESTIMATOR`, already primary-method cross-checked.
- Source one- and two-point measures, selection/transfer, branch weights: `OPEN`.
- G99 `r_cal(z)`: frozen conditional radial chord; it may index a later supplied history but is not
  inserted into the angular estimator.
- `X_max`, a standard ruler, acoustic scale, Lambda-CDM distance, flux law, source mechanism, and
  complete history: excluded.

## Outcome-blindness disclosure

The mandatory startup surface states the qualitative R4/R5 conclusions and therefore prevents
literal zero-knowledge blindness. This derivation will not read any saved curve, curve descriptor,
feature angle, DCT coefficient, covariance, singular vector, or R2--R5 result array. No observed
pattern value may enter code or algebra.

## Preregistered checks

1. `C-TYPE`: `u_a` is unit timelike and `n_a` is unit spacelike orthogonal to `u_a`.
2. `C-COMMON`: a joint sky angle is legal only when the normalized observer clocks agree.
3. `C-ORIENT`: the observed source direction is not claimed without ordered outward query orientation.
4. `C-GAUGE`: `n_a` and `theta_12` are invariant under positive clock rescaling and positive ruler
   rescaling plus clock shift of each pair column.
5. `C-FRAME`: common Lorentz/coframe changes leave `phi_a` and `theta_12` invariant.
6. `C-PAIR`: one observer--source scalar cannot produce the two-source angular statistic.
7. `C-EST`: normalized `DD`, `DR`, `RR`, and Landy--Szalay are reconstructed from a synthetic catalog
   without reading observational outcomes.
8. `C-BRANCH`: the continuous formulation must be a pushforward of one- and two-point source measures
   and must remain meaningful for multiple branches; an injective Jacobian formula may appear only as
   a reduction.
9. `C-IDENT`: if the source pair measure/selection is unrestricted, no unique predicted angular curve
   may be claimed from the evaluator alone.
10. `C-NOIMPORT`: no ruler, `X_max`, acoustic origin, Lambda-CDM distance, G99 refit, or observed feature
   enters the derivation.

## Certification ceiling

Maximum permitted landing:

```text
COMPLETE_TWO_SOURCE_OBSERVABLE_EVALUATOR_DERIVED
__DIRECTION_IDENTIFICATION_QUERY_OWNED
__PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN
```

or a narrower failure identifying the exact type/algebra obstruction.

This phase cannot compare to BAO outcomes, fit anything, select a metric history, infer `X_max`, or
claim a BAO prediction.
