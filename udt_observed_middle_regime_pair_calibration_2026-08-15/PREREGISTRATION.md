# Preregistration — observed middle-regime observer-pair calibration

Date: 2026-08-15

Program label: `G99`

Mode: one-time adoption of already banked observational evidence; no new fit and no holdout read

## Whole question

Can the already verified Pantheon+ P1 result be frozen as a minimal `OBSERVED/CONDITIONAL`
middle-regime calibration for the UDT observer-pair relation, without promoting it to a complete
metric history or using BAO, CMB, endpoint, or `X_max` behavior to choose it?

This is not a blind observational calculation. The P1 numbers were already observed and verified
in G65. The preregistered act is their forward scientific use: one fixed calibration is adopted
once, its type is narrowed, and all later test lanes are declared before any transfer into them.

## Exact calibration object

The object directly constrained by the SNe likelihood is an effective luminosity-distance relation
on the registered SNe query, not a ten-component coframe history:

```text
Z = 1+z,
phi_pair = log Z,
dL_cal(z) = n X_eff Z^2 [1-Z^(-2/n)].
```

The conditional historical factorization is

```text
r_cal(phi_pair) = n X_eff [1-exp(-2 phi_pair/n)],
d_A = r_cal,
d_L = exp(2 phi_pair) d_A.
```

The last two equalities are retained as an effective registered SNe transfer/readout premise. SNe
alone does not separately observe `r_cal`, the screen-area map, `eta`, or `epsilon`. Under the G94
notation, this factorization is compatible with the provisional product `eta*epsilon=1/Z`; it does
not derive that product or a radiative carrier law.

The accompanying supplied-pair cone readout

```text
c_eff^(pair)/c_E = Z^(-2)
```

is derived conditionally from `phi_pair`; it is not fitted here and is not a material signal speed.

## Frozen evidence and parameters

No optimizer will be run. The program must extract exactly these already banked fields:

- primary shape from `A:zCMB:P1` in G65;
- conditional absolute scale from `B:zCMB:P1`, carrying `M_B=-19.253 +/- 0.027`;
- observed domain and row count from the frozen M3 dry run;
- prior mode-C and redshift-column shifts only as disclosed sensitivity diagnostics, never as
  additional fitting freedom.

The central calibration is therefore the pair `(n,X_eff)`, with `R_w=n X_eff` reported only at the
joint best point. The shape-only SNe result does not determine `X_eff`; the absolute scale remains
conditional on the external luminosity anchor and the registered transfer convention.

## Scope and holdouts

- Calibration domain: the selected `zCMB` SNe interval already registered by M3, not an
  extrapolation to zero, the CMB, or an asymptotic endpoint.
- BAO: strict forward holdout. No R2--R5 curve, covariance, feature, angle, or historical M3 BAO
  result may be read or used.
- CMB: strict forward holdout. No profile, sky response, spectrum, source covariance, or endpoint
  may be used.
- Endpoint/`X_max`: strict forward holdout. No asymptote, wall, seam, terminal distance, or
  completion class may be inferred or used to alter this calibration.
- The protected curvature atlas, stopped native-on-shell draft, pair-response payload, and G88
  payload remain outside the source universe.
- No bootstrap, action, source, carrier, matter, or mass premise is activated.

## Ownership boundary

This program may adopt an observed terminal relational history over the SNe interval. It may not
claim that observations selected:

- a complete `E=[[B,0],[Q S,Q]]` history;
- a physical pair realization `J=[Y;Z]`;
- a unique split of the terminal response among `B,Q,S,Y,Z`;
- a time-live continuation outside the SNe interval;
- a CMB or BAO response;
- an `X_max` value or realization.

The complete orchestra remains upstream. A later complete metric/query proposal must reproduce the
frozen terminal calibration without using a holdout to retune it.

## Certification contract

1. Verify every byte in `SOURCE_MANIFEST_PREREG.tsv` before extracting values.
2. Read the calibration fields from the two independently banked G65 result artifacts; do not
   optimize against the Pantheon+ table.
3. Emit one machine-readable calibration contract containing the exact parameters, intervals,
   domain, formulas, premise stamps, and holdout list.
4. Independently reconstruct all central parameters from the source JSON and evaluate the fixed
   relation at the preregistered nodes `z=(0.02307,0.1,0.5,1.0,2.0,2.2613)`.
5. Verify analytically or symbolically that `dL_cal(0)=0`, `r_cal'(0)=2 X_eff`, the curve is positive
   and strictly increasing for `z>0`, and the two displayed factorizations agree.
6. Catch proofs must reject: calling the calibration a complete metric history; dropping the
   luminosity-anchor condition; calling `R_w` marginally measured; treating the SNe domain as an
   `X_max` interval; appending an orchestra correction; reading a holdout; or calling the transfer
   or signal-speed interpretation derived.
7. Run repository tests and the current premise verifier after the package passes locally.

## Registered returns

- `OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN`: all extraction, formula, independence, scope,
  and premise gates pass.
- `SOURCE_OR_TYPE_FAILURE`: a registered source does not reproduce or the object cannot be frozen
  without promoting a conditional relation.
- `HOLDOUT_CONTAMINATION`: any BAO, CMB, endpoint, or `X_max` result enters construction or choice.

## Maximum conclusion

At most, G99 may freeze one observed, conditional middle-regime observer-pair luminosity relation
and its terminal reciprocal coordinate for later independent testing. It cannot derive the
complete history, physical transfer law, regime score, loud-end behavior, `X_max`, cosmology,
action, source, matter, mass, or bootstrap closure.
