# Native flux/luminosity-law ownership audit — preregistration

Date: 2026-08-15

## Whole question

Given a supplied regular complete UDT metric history, a supplied typed source-to-observer null/screen
query, and the rebuilt complete pair evaluator, determine the strongest flux-transfer law that follows
without importing Maxwell dynamics, photon-number conservation, Planck's relation, GR optical
reciprocity as a physical premise, an intrinsic source model, or the historical SNe luminosity law.

The audit asks separately:

1. what endpoint clock/frequency conversion is owned;
2. what forward/reverse screen-area conversion is owned;
3. what carrier amount, energy, or intensity transport is owned;
4. whether these uniquely determine received bolometric flux from supplied emitted luminosity; and
5. what additional premise is smallest if the metric does not close the last step.

This is metric-led. It characterizes the available law space. It does not target
`d_L=(1+z)^2 d_A` or any alternative exponent.

## Exact bounded regime

- Smooth time-oriented four-dimensional Lorentzian metric supplied through the complete coframe.
- One supplied regular source/observer query and one regular null branch.
- Two-dimensional screen Jacobi maps with nonzero determinants; caustics and cut-locus branch sums
  are recorded as excluded strata, not discarded as failures.
- Time dependence, angular anisotropy, screen shear/rotation, and complete mixing remain allowed in
  the geometry. No static, spherical, radial, or diagonal restriction is imposed by the theorem.
- Absorption, scattering, intrinsic source variability, detector bandpass, and matter conversion are
  not silently set to zero. They are typed as unowned transfer/source data unless a current native
  source derives them.

## Preregistered factorization

Write `Z=1+z`, `d_A^2=|det D_f|`, and `d_G^2=|det D_r|`, where `D_f` and `D_r`
are the forward and reverse endpoint-normalized screen maps on the same relation. For differential
source luminosity `L_Omega=dL_s/dOmega_s`, define only as bookkeeping

```text
F_o = L_Omega * A_surv * E_o/E_s * d_tau_s/d_tau_o / d_G^2.
```

`A_surv`, `E_o/E_s`, and `d_tau_s/d_tau_o` are not assigned values in advance. The audit must
derive, condition, or leave open each factor.

## Candidate landings

1. `FULL_NATIVE_FLUX_LAW_DERIVED`: all factors and their composition/reversal laws follow from
   active UDT premises and the supplied metric/query, with no unowned carrier or source premise.
2. `GEOMETRIC_RECIPROCITY_DERIVED__RADIATIVE_TRANSFER_OPEN`: endpoint clock conversion and complete
   forward/reverse screen dilution are derived conditionally, but carrier survival or energy
   conversion remains unowned.
3. `CONDITIONAL_CONSERVED_CURRENT_CLOSES_FLUX_LAW`: a precisely stated additional conserved-current
   or wave-action premise closes a unique conditional law; the premise is not relabelled derived.
4. `HISTORICAL_DL_LAW_INCOMPATIBLE_WITH_DERIVED_GEOMETRY`: the complete geometric factors contradict
   the registered historical relation on the declared regular stratum.
5. `TYPE_OR_EXISTENCE_FAILURE`: the proposed flux observable cannot be coherently typed even after
   the source state and detector readout are supplied.

More than one scoped statement may hold, but the final headline must identify the earliest open
arrow and must not imply an intrinsic supernova luminosity law.

## Certification and falsification contract

- Derive the forward/reverse Jacobi identity from a symmetric optical tidal operator using a
  conserved matrix Wronskian; do not infer it from G80 numerics alone.
- Reproduce the finite-dimensional scaling algebra symbolically and by a separately written exact
  implementation.
- Construct at least two covariant radiative transport laws on the same supplied geometry/query if
  claiming nonuniqueness. They must agree on all geometric inputs and differ only in an explicitly
  unowned transfer factor.
- Search the current native authority corpus for an owned current/action/normalization before
  declaring the transfer factor open. Historical sources are provenance only and cannot overrule
  `LIVE.md` or `CURRENT_SCIENTIFIC_PREMISES.tsv`.
- Catch-proof guards against: dropping one redshift factor, equating `d_A` and reverse area distance,
  importing photon-number conservation, treating `E proportional to frequency` as metric algebra,
  freezing angular/mixing channels, and calling an isotropic source metric-derived.
- Maximum conclusion: a regular-branch propagation ownership theorem. No SNe fit, physical history,
  `X_max`, BAO/CMB, action, matter, bootstrap, or intrinsic source luminosity follows.

## Four evidence gates required before banking

1. Preregistered before the native-source census and new algebra: required.
2. Full space or bounded scope justified: regular single-branch theorem only; singular/global strata
   must remain explicit.
3. Independent verification of the load-bearing factorization: required.
4. Every physical premise audited: required.
