VERIFIED_AS_BOUNDED

**DERIVED**
- Saved-state reconstruction is type-correct on the sealed intake: `D_AB(x) = E_A^mu(x) g_mu_nu(x) J_B^nu(x)` from the interpolated saved state, with no new solve. My independent replay from `FINITE_PATH_SAMPLES.npz` reproduces the atlas `D` values to `1.9259e-34` relative with `PCHIP`, and the official `x=1` G68 endpoints to `3.7444e-16`.
- The source-covariance theorem is exact for invertible `D`:
```text
C_obs = D C_src D^T,
C_src = D^-1 C_obs D^-T,
D C_src D^T = C_obs,
v^T C_src v = (D^-T v)^T C_obs (D^-T v) > 0
```
  so positive definiteness is preserved when `C_obs` is positive definite.
- Singular-map qualification is also exact:
```text
rank(D C_src D^T) <= rank(D)
```
  so if `rank(D) < 2`, a generic positive-definite `2 x 2` `C_obs` cannot be represented. In this intake that caveat is inactive because every recorded map is invertible.
- Type adjudication: this theorem addresses only the declared local `2 x 2` screen-covariance transfer. It does not by itself address full TT/TE/EE/BB spectra, source populations, or a physical CMB prediction law.

**OBSERVED**
- `REVIEW_MANIFEST.tsv` verified cleanly before source use: every listed hash matched.
- Census verified: `21` profiles, `15` endpoints, `315` cells, `15` sensitivity cells, `945` covariance reconstructions, with no omitted or duplicated profile-endpoint cells.
- Interpolation check is legitimate but limited: `PCHIP` versus `CubicSpline` gives `1.0141e-10` maximum relative `D` disagreement across all `315` cells. That is an interpolation-family robustness check on the same frozen paths, not independent path integration. The package distinguishes this honestly in [PRECALCULATION_CLARIFICATION.md](/tmp/udt_g69_review_IOWOt6/udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11/PRECALCULATION_CLARIFICATION.md).
- F01 sanity gates pass exactly: max F01 anisotropy `0.0`, max F01 polar rotation `0.0`.
- Rank claim survives recomputation from the atlas and from fresh replay. Column-normalized `sigma_min/sigma_max` spans `4.6381e-4` to `1.4965e-2`; normalized condition numbers span `66.8237` to `2156.0777`; all `15/15` cells are `FULL_RANK_OBSERVED`.
- The rank result is not threshold-fragile under the registered challenge points. Without column normalization, the worst ratio is still `3.0718e-5 > 1e-6`. Using the `epsilon=1/20` or `epsilon=1/5` endpoint/lapse columns separately, the worst normalized ratio is still `7.6892e-5 > 1e-6`. So midpoint/averaging and normalization do not create the rank observation.
- The azimuthal-carry channel is load-bearing. If it is removed, the readout becomes `2 x 3`, so rank is at most `2` by dimension; no one- or two-channel scalar reduction can identify all three controls.
- Covariance replay also survives independent recomputation: max backward relative error `2.8305e-16`, minimum constructed source eigenvalue `1.56159`, minimum map singular value `0.0496135`.

**CHOSE_CONTROL**
- Registered controls are explicit and honored: endpoint grid `x in {0.30,...,1.00}`, control tile `(x,a,epsilon)`, readout `y = (log(det(D)/s_F01^2), log(sigma_max/sigma_min), psi)`, column normalization, and rank thresholds `1e-6` / `1e-8`.
- Numerical adjudication of those controls: accepted. The full-rank result is comfortably above the preregistered threshold, so this is not a knife-edge classification artifact.
- Exact correction: none.
- One wording guard should remain strict: “independent verification” here means independent reconstruction/algebra on shared saved paths, not independent geodesic or Jacobi integration.

**CONDITIONAL**
- A few future coefficients may be fitted only if the exact compensation freedom is first broken by typed ownership. At least one of these must be supplied independently: a restricted source/state covariance family, an independently owned endpoint/profile rule, or additional independent observables that are not absorbed by the same unrestricted source freedom.
- The hold-out rule is necessary: at least one independent observable/channel/regime must remain unused during fitting.
- Without such ownership restrictions, fitting even a small geometric coefficient set to a local covariance is non-identifying, because `C_src = D^-1 C_obs D^-T` absorbs the map exactly.
- The P1 SNe anchor remains inactive and conditional only, consistent with [OBSERVATIONAL_ANCHOR_POLICY.md](/tmp/udt_g69_review_IOWOt6/udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11/OBSERVATIONAL_ANCHOR_POLICY.md).

**OPEN**
- Still open by type and scope: physical CMB profile, physical endpoint or last-scattering surface, source/state covariance, TT/TE/EE/BB spectra, polarization transport law, source population, action, bootstrap, and signalling claims.
- Scope adjudication: the package does not silently prove global CMB non-identifiability. It proves a bounded local geometric separation result plus an exact non-identifiability result for unrestricted source covariance at the declared `2 x 2` screen-covariance level, consistent with [EXACT_DERIVATION.md](/tmp/udt_g69_review_IOWOt6/udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11/EXACT_DERIVATION.md) and [OBSERVABLE_CHANNEL_REQUIREMENTS.tsv](/tmp/udt_g69_review_IOWOt6/udt_cmb_complete_observation_query_map_2026-08-11/OBSERVABLE_CHANNEL_REQUIREMENTS.tsv).
- Lay adjudication: inside this frozen test map, the geometry really does change in three distinguishable directions. But if the original source pattern is left completely free, that source can be re-chosen to cancel any invertible geometric map at the local covariance level. So the geometry contains information, but the sky covariance alone does not yet own enough information to pick the real profile or endpoint.