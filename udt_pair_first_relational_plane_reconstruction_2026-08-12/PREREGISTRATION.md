# Preregistration — pair-first relational-plane reconstruction

Date: 2026-08-12

## Whole question

Does a supplied regular calibrated ordered observer-pair realization carry its own clock--ruler
two-plane, so that the complete UDT metric evaluates and modulates that plane without requiring
ambient curvature to select one universal reciprocal/angular split?

The audit must separately decide what is owned by:

1. the founding abstract clock/ruler channel pair;
2. a supplied ordered query and regular realization `F:Sigma^2 -> (M^4,g)`;
3. the complete metric once `F` is supplied; and
4. the founding postulates alone, before `F` is supplied.

## Bounded regime

- smooth Lorentzian four-metric `g`;
- one supplied smooth rank-two timelike immersion `F`;
- A-calibrated pair coordinates only when terminal `(kappa,phi,beta)` is read;
- an optional local complete-coframe chart
  `E=[[B,0],[Q S,Q]]` with regular `B`, positive-screen `Q`, and arbitrary real `S`;
- for the reduced `S+W` chart formula only, an invertible base projection of `dF`;
- local differential geometry only; no claim of global integrability from a merely pointwise plane
  field.

No physical history, observer query, realization, path, branch, action, source, carrier, bootstrap
law, `X_max`, SNe model, CMB model, signalling law, or dynamics is selected.

## Metric-led or template-led

Metric-led after the query realization is supplied. The audit derives the pullback and the
tangent/normal decomposition from `g` and `F`. It does not filter for a desired plane and does not
ask curvature to reproduce the previously registered ambient split.

## Premise ledger in prose

- `c_E`: `OBSERVED`; calibrates the clock/ruler coordinates and terminal ratio.
- Abstract ordered clock/ruler channel plane and dual pairing: `POSIT` in the founding source.
- Reciprocal exponential character on supplied depth: `DERIVED`.
- Complete Lorentz metric `g`: `SUPPLIED/CONDITIONAL` history for this audit.
- Ordered query and immersion `F`: `SUPPLIED/CONDITIONAL`; physical ownership remains `OPEN`.
- Complete triangular coframe chart: `CONDITIONAL` representation on its regular local stratum.
- Pair-induced tangent plane `dF(TSigma)` and normal screen: candidate `DERIVED CONDITIONAL` objects.
- Action, source, matter, bootstrap, `X_max`, SNe, CMB: inactive.

## Required exact derivations

1. Prove that a regular timelike immersion gives a canonical pair-relative splitting
   `TM|F(Sigma)=E_pair direct-sum H_pair`, with `E_pair=dF(TSigma)` and
   `H_pair=E_pair^perp` positive definite.
2. For `dF=[Y;Z]` in the complete-coframe chart, derive directly

   `h = Y^T B^T eta_2 B Y + (S Y+Z)^T Q^T Q (S Y+Z)`.

3. On the invertible-`Y` stratum, derive the reduced combination

   `Y^-T h Y^-1 = B^T eta_2 B + C^T q C`, with
   `C=S+Z Y^-1` and `q=Q^T Q`.

4. Characterize the full pointwise image of `C^T q C`, including all signature changes, rather
   than retaining only Lorentzian outcomes.
5. In calibrated coordinates, derive how the Gram correction changes `h00`, `h01`, `h11`,
   `(kappa,phi,beta)`, and `c_eff^(pair)/c_E`.
6. Prove screen-frame covariance, pair-coordinate covariance, and the pure-base limit.
7. Retain the exact flat counterfamily showing that the abstract ordered observer pair and `c_E`
   do not select the realized immersion.

## Preregistered landings

### A — `PAIR_FIRST_CONDITIONAL_RESOLUTION`

Return this if `F` canonically supplies the pair plane and screen, the full metric pullback contains
the angular/mixing modulation exactly, and no ambient curvature selector is required after `F` is
supplied. The landing must still state that the founding algebra does not by itself construct `F`.

### B — `AMBIENT_SELECTOR_STILL_REQUIRED`

Return this if a supplied regular `F` fails to define the needed plane/screen or the complete metric
cannot evaluate the pair geometry without a second ambient selector.

### C — `FOUNDING_CHANNEL_TYPE_FAILURE`

Return this if the founding `q=(c_E dt,dr)` and dual pairing do not even define an abstract ordered
two-channel comparison space.

### D — `NUMERICALLY_OR_ALGEBRAICALLY_UNRESOLVED`

Return this if production and independent derivations disagree or any required identity remains
unverified.

## Falsification and certification contract

The primary landing is falsified by any of:

- rank loss of `dF` on a row called regular;
- non-Lorentzian `E_pair` on a row used for terminal readout;
- failure of `H_pair=E_pair^perp` to be positive rank two;
- disagreement between direct pullback and block formula;
- failure of screen-frame or pair-coordinate covariance;
- failure to recover the base metric at `C=0`;
- a claim that `F`, its event pairing, or its physical branch was derived from the two founding
  algebraic postulates;
- filtering non-Lorentzian Gram corrections rather than recording them.

Certification requires exact symbolic checks plus an independently expressed component replay.
A fresh adversarial review must try to show that the result merely renames a preferred flag, hides
an extra realization premise, or overclaims global integrability.

## Maximum allowed conclusion

At most:

> A supplied regular calibrated pair immersion owns a pair-relative tangent plane and orthogonal
> screen. The complete metric evaluates that realized plane, and in a regular complete-coframe chart
> all screen/mixing/embedding modulation enters its first fundamental form through one positive
> semidefinite Gram term. Therefore no universal ambient curvature-selected split is required for
> conditional pair evaluation. The founding source owns the abstract clock/ruler channel type and
> reciprocal character, but it does not by itself own the embedding, event pairing, global pair
> family, or physical realization.

No stronger physical or global conclusion is permitted.
