# G88 AM radial SNe / asymptote compatibility atlas — preregistration

Date: 2026-08-12

Status at banking: `PREREGISTERED__NO_NEW_LIKELIHOOD_EVALUATED`

Question type: `MIXED__METRIC_LED_EVALUATION_WITH_OBSERVATIONAL_RANKING`

Controlling rule: this is one bounded solution-space tile, not a physical profile selector.

## Whole question

Within the complete frozen G75 `AM` control family, what observer-pair redshift and angular-distance
curves are returned by one already verified stationary, outward, equatorial radial null/Jacobi
query over the complete frozen Pantheon+ redshift sample, and how do those curves compare with the
registered low-redshift SNe compatibility anchor after profiling only one common magnitude/scale
offset?

Every one of the `197` AM rows is evaluated. No row is chosen because it resembles the data, no
shape coefficient is adjusted, and no failed or badly scoring row is discarded from the atlas.

The same AM lapse continuation has a stationary divergence candidate at `x=2`. This audit records
whether each query reaches the largest required SNe source surface below that candidate and keeps
the exact asymptotic property attached to the family. It does **not** identify the candidate with
physical `X_max`.

## Exact bounded regime

- Frozen profile universe: exactly the `197` rows with `lapse_name=AM` in G75
  `PROFILE_ATLAS.tsv`, including the zero-mixing control and all `196` nonzero rows.
- Metric evaluator: the full nonlinear four-dimensional G68 null, parallel-screen, and Jacobi
  system with the G75 polynomial `q(s)` substituted exactly. No angular/mixing term is zeroed.
- Ordered query: coordinate-stationary endpoint observers; receiver `x_r=0.25`; outward radial
  equatorial ray; receiver-measured unit frequency; source sphere determined separately for each
  observed redshift.
- Lapse: `A(x)=1-x^2/4` (`FREE_AND_EXPLORED` AM continuation).
- Redshift: `1+z=sqrt(A_r/A_s)`, hence
  `x_s(z)=2*sqrt(1-A_r/(1+z)^2)` with `A_r=63/64`.
- Data: frozen `Pantheon+SH0ES.dat`; primary `zCMB`; `zCMB>0.023`;
  `IS_CALIBRATOR=0`; frozen full statistical+systematic covariance. This gives `1367` rows and
  `z_max=2.2613`, so the largest required source coordinate is
  `x_s,max=1.9052028080619356 < 2`.
- Distance readout: `d_A/R=sqrt(abs(det D))` from the complete Jacobi screen, and the conditional
  registered readout `d_L/R=(1+z)^2 d_A/R`.
- Likelihood: compare `m_b_corr` with
  `5*log10(d_L/R)+B`; profile the one additive constant `B` analytically using the full covariance.
  No `R`, absolute magnitude, profile coefficient, endpoint, or redshift relation is separately
  fitted.
- Registered observational benchmark: frozen `A:zCMB:P1`,
  `chi2=1260.8480887040496` for `1367` data and `1365` degrees of freedom. The benchmark is a
  comparison anchor, not a derivation or acceptance cutoff.

## Why this is not the whole empirical question

Pantheon supplies sky coordinates and the AM controls are axisymmetric. The existing G76/G77
whole-sky machinery classifies endpoint maps but does not yet supply the complete source-screen
Jacobi area at every redshift. Therefore this audit is deliberately the already owned full-Jacobi
**radial-query** tile. It cannot certify or reject a profile's full-sky SNe behavior.

The pure next empirical layer, if justified by this atlas, is a separately preregistered whole-sky
source-screen/Jacobi reconstruction over the same family. A one-ray score will not be used to erase
profiles from that later full-sky atlas.

## Numerical contract

Production integrations use `DOP853`, `rtol=1e-10`, `atol=1e-12`, `max_step=1/400`, and affine cap
`20`. The maximum-redshift surface is terminal. Dense output is sampled at every catalog redshift;
the first outward crossing is used. The route is characterized, rather than filtered, if it turns,
encounters a sampled caustic, remains below the surface at the affine cap, becomes nonfinite, or
fails a residual gate.

Certification residuals are evaluated on at least 101 affine samples per path. The preregistered
bound is `1e-7` separately for nullness, screen orthonormality, screen-ray orthogonality, conserved
`p_t`, and conserved `p_psi`. A profile can receive a likelihood only when every catalog source
surface has an owned first crossing and finite nonzero `d_A`; all other profiles remain fully
recorded with a non-likelihood status.

The outcome-independent method-replay subset is:

```text
G75_F01_AM
G75_AM_S01_E100
G75_AM_S12_E100
G75_AM_S02_E100
G75_AM_S13_E100
G75_AM_S03_E100
```

It spans the zero control and the five nonzero G75 behavior classes. Those six curves are replayed
with `Radau`, `rtol=2e-10`, `atol=2e-12`, `max_step=1/400`. The production/replay distance-modulus
agreement gate is maximum absolute difference `<=2e-5 mag` at the 1367 frozen redshifts. The
likelihood is also recomputed from saved distance curves by a separate implementation.

## Outcome-independent classifications

Path/query status is one of:

- `FULL_QUERY_REGULAR_NO_SAMPLED_CAUSTIC`
- `FULL_QUERY_AFTER_SAMPLED_CAUSTIC`
- `TURNING_OR_MULTICROSS_QUERY`
- `AFFINE_CAP_BEFORE_MAX_SOURCE`
- `NUMERIC_OR_SIGNATURE_FAILURE`
- `RESIDUAL_UNCERTIFIED`

For rows with a certified likelihood, report exact `chi2`, `chi2/ndof` with `ndof=1366`, profiled
`B`, and `delta_chi2_vs_registered_P1`. Observational summaries are descriptive:

- `P1_OR_BETTER_IN_THIS_QUERY` iff `chi2 <= 1260.8480887040496`;
- `WORSE_THAN_P1_IN_THIS_QUERY` otherwise.

These labels do not include look-elsewhere correction and are not physical viability verdicts.
The full distribution, rank, family/behavior-class summaries, and all ties are retained. The best
row is only a `LEAD`, even if it beats P1.

## Falsification and certification ceiling

The bounded family/query is falsified as a complete SNe-route candidate if no AM row supplies all
1367 finite source-screen distances. It is observationally noncompetitive on this radial tile if
no certified row reaches the registered P1 benchmark. Neither return falsifies UDT, the complete
AM whole-sky family, another observer query, or a time-live completion.

Maximum positive conclusion:

`OBSERVED_EMPIRICAL_COMPATIBILITY_LEAD_WITHIN_THE_FROZEN_197_AM_STATIONARY_RADIAL_QUERY`

No result from this audit may select a physical profile, identify `x=2` with physical `X_max`,
derive a bootstrap function, assign a physical `R`, claim a full SNe fit, or infer action, source,
matter, CMB, BAO, or local signal physics.
