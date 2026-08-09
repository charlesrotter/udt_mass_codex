# M3c — Matched-rigor methodology map for the UDT-native BAO/LSS re-run

Date: 2026-08-08. Branch grok. MODE: RESEARCH / lit + methodology only (no compute, no
commit). Motivated by the M3b diagonal-jackknife-covariance caveat (BOSS_RESULTS.md §8):
per-shell Δχ² significances are plausibly INFLATED because bin–bin correlated broadband
residuals are not modelled. This map defines what "matched rigor" means for us and classifies
EVERY DESI/BOSS catalog + estimator + covariance step as **NEUTRAL** (safe to adopt),
**DEPENDENT** (forbidden by our ontology rule, F-IMPORT-LCDM), or **GRAY** (adopt only
with a stated neutral justification / native re-implementation).

Our hard rule (MAP §0): BAO enters as RAW OBSERVATIONS only. No acoustic story, no sound-horizon
r_d, no comoving/fiducial-cosmology distance conversion, no reconstruction, no ΛCDM templates,
no ΛCDM-simulation (mock) covariances. We work in OBSERVABLE angular space θ per thin z-shell
with UDT's own r(z).

--------------------------------------------------------------------------------------------
## A. Primary methodology sources (cited)

- **DESI DR1 LSS catalog construction** — Ross et al., "The Construction of Large-scale
  Structure Catalogs for DESI" — arXiv:2405.16593. (weights, randoms, veto, completeness)
- **DESI 2024 II — samples + two-point clustering** — arXiv:2411.12020.
- **DESI fiber-assignment / bitweights (PIP)** — "Production of Alternate Realizations of DESI
  Fiber Assignment…" arXiv:2404.03006; foundational method Bianchi & Percival 2017,
  MNRAS 10.1093/mnras/sty2377; eBOSS PIP+angular-upweight Mohammad et al. arXiv:2007.09005.
- **DESI fiber-assignment incompleteness mitigation (DR1)** — arXiv:2411.12020 companion
  (AMTL/FFA + PIP).
- **DESI imaging systematics** — "Mitigating Imaging Systematics for DESI 2024 ELGs…"
  arXiv:2411.12024 (SYSNet NN / linear-regression / random-forest template weights).
- **DESI covariance** — semi-analytic RascalC arXiv:2404.03007; EZmock/analytic validation
  arXiv:2411.12027.
- **BOSS DR12 catalogs** — Reid et al. 2016 arXiv:1509.06529 (weight combination Eq. 50);
  Ross et al. 2012 (imaging-systematics weights); Ross et al. 2017 arXiv:1607.03145 (obs.
  systematics); cosmology analysis Alam et al. 2017 arXiv:1607.03155.
- **FKP weights** — Feldman, Kaiser & Peacock 1994.
- **Estimator** — Landy & Szalay 1993. **Integral constraint** — Roche & Eales 1999
  (IC = Σ RR(θ)ω(θ) / Σ RR(θ), from randoms only).
- **Covariance corrections** — Hartlap et al. 2007 (inverse-covariance debias); Percival et al.
  2014/2022 (finite-sample parameter-covariance factor); Mohammad & Percival 2022
  arXiv:2109.07071 (corrected-jackknife/bootstrap weighting for the 2PCF).

--------------------------------------------------------------------------------------------
## B. Per-step classification table

### B.1 Catalog weights

| Step | What it does | Grade | Justification |
|---|---|---|---|
| WEIGHT_COMP / COMPLETENESS (DESI) | corrects observed density for fiber-assignment completeness (targets vs assigned) | **NEUTRAL** | pure survey operations / geometry; no cosmology. Already used in M3. |
| WEIGHT_ZFAIL (DESI) / WEIGHT_NOZ (BOSS) | up-weights neighbours for redshift-measurement failures | **NEUTRAL** | instrument/pipeline success rate; no cosmology. Used in M3. |
| WEIGHT_CP / close-pair (BOSS) | up-weights for fiber-collision missed close pairs | **GRAY→NEUTRAL** | the *nearest-neighbour* up-weight is neutral but only approximate at small θ; the rigorous replacement is PIP/bitweights (below). No cosmology either way. |
| PIP bitweights + angular up-weighting (DESI) | exact fiber-collision correction from N_real fiber-assignment realizations | **NEUTRAL** | pure survey geometry / assignment combinatorics; contains NO cosmological model. Recovers unbiased clustering in config + Fourier space. **A rigor upgrade we can adopt.** |
| WEIGHT_SYS / imaging-systematics (DESI SYSNet/regression; BOSS WEIGHT_SYSTOT) | removes spurious density–imaging (depth, seeing, dust, stellar density, airmass) correlations via template fitting | **GRAY** | templates are observational maps, NOT cosmology — neutral in principle. BUT ML weights can over-correct large-scale power (arXiv:2411.12024 flags this for QSO). KEEP the M3 with/without-SYS variant discipline; treat the spread as a systematic. |
| WEIGHT_FKP (both) = 1/(1+n̄(r)P₀) | variance-optimal down-weighting of dense regions; P₀≈10⁴ h⁻³Mpc³ | **GRAY / avoidable as-shipped** | it is only an S/N weight (unbiased estimator), BUT as shipped n̄(r) = NX uses a **fiducial-cosmology comoving volume** ⇒ contaminated column. Native fix: recompute an FKP-like weight from the **angular** number density per shell (no comoving volume, no P(k) conversion). P₀ is a scalar tuning constant, not a cosmology import. |
| Randoms construction | reproduce the angular+radial selection function (mask, completeness, n(z) sampled from data) | **NEUTRAL** | DESI/BOSS randoms sample the *observed* selection; no cosmology in the angular mask. (Radial n(z) is drawn from the data redshifts — native.) |
| Veto masks (bright stars, bad fields, focal-plane, imaging quality) | remove untrustworthy sky | **NEUTRAL** | survey/instrument quality cuts; no cosmology. Adopt fully. |
| NX / NZ / NBAR columns, COMOVING/DC | fiducial-cosmology comoving n(z), distances | **DEPENDENT — FORBIDDEN** | fiducial-ΛCDM comoving conversion. Already blacklisted in M3/M3b loaders. |

### B.2 Estimator + corrections

| Step | Grade | Justification |
|---|---|---|
| Landy–Szalay (DD−2DR+RR)/RR | **NEUTRAL** | pure pair-count statistic; no cosmology. Used in M3. |
| Angular θ per thin z-shell (vs 3D fiducial-distance ξ(s)) | **NEUTRAL (ours) — the 3D alt is DEPENDENT** | the angular projection avoids comoving conversion; the standard 3D ξ(s) requires z→distance under a fiducial cosmology = FORBIDDEN. |
| Integral-constraint correction, IC = Σ RR(θ)ω(θ)/Σ RR(θ) | **NEUTRAL** | estimated from the random catalog geometry alone (Roche & Eales 1999); removes the finite-area negative offset that biases broadband shape — directly relevant to our "is it a bump or broadband residual" question. **Adopt.** |
| Edge/boundary handling via LS + randoms | **NEUTRAL** | randoms encode the boundary; no cosmology. |
| BAO template fit / r_d calibration / D_V–r_d | **DEPENDENT — FORBIDDEN** | acoustic model + sound horizon. Never used; we keep the model-free bump search. |
| Reconstruction (displacement field) | **DEPENDENT — FORBIDDEN** | uses ΛCDM-gravity + fiducial cosmology to sharpen the peak. Blacklisted (_rec files). |

### B.3 Covariance (the load-bearing question)

| Method | Grade | Justification |
|---|---|---|
| Delete-one jackknife, **full bin–bin C_ij** | **NEUTRAL** | pure resampling of our own data/randoms; no cosmology. This is the fix for the M3/M3b caveat (we only used the diagonal). |
| Mohammad–Percival corrected-jackknife pair-weighting (arXiv:2109.07071) | **NEUTRAL** | a re-weighting of pairs in the resampling; recovers unbiased 2PCF covariance where naive JK fails. Adopt. |
| Bootstrap (resample regions) | **NEUTRAL** | resampling of own data; adopt as cross-check. |
| Hartlap 2007 factor (N−p−2)/(N−1) on C⁻¹ | **NEUTRAL** | debiases the inverse of a noisy sample covariance; adopt (mandatory once we invert a full C). |
| Percival 2014/2022 factor on parameter errors | **NEUTRAL** | finite-realization correction to fitted-parameter covariance; adopt. |
| RascalC semi-analytic / semi-empirical covariance (arXiv:2404.03007) | **NEUTRAL (semi-empirical mode) / GRAY (default template mode)** | its semi-empirical mode builds C from the **measured** 2PCF + randoms with a single shot-noise rescaling calibrated to jackknife — no cosmology, no mocks. It sidesteps the N_regions>N_bins singularity of raw JK. **Strong adopt.** Only its optional theory-P(k) input would be GRAY; use the data-ξ input. |
| Analytic Gaussian covariance | **NEUTRAL only if** built from our measured ξ / n̄; DEPENDENT if it ingests a fiducial P(k). |
| **Mock-based covariance (EZmock, QPM, Patchy, GLAM, Abacus)** | **DEPENDENT — FORBIDDEN** | all are ΛCDM-simulation (N-body/approx) realizations; DESI DR1 uses 1000 EZmocks + Abacus-2. These import the ΛCDM correlation structure directly into C. **Never adopt.** |

--------------------------------------------------------------------------------------------
## C. RECOMMENDED MATCHED-RIGOR SPEC (ranked by expected impact)

1. **Full bin–bin covariance, not diagonal (the #1 fix).** Replace the diagonal jackknife with
   a full C_ij. This directly addresses the caveat that broadband residuals correlate across θ
   bins and inflate per-shell Δχ². **Constraint (honest):** raw delete-one JK needs
   N_regions ≳ N_bins+2 (we had 24 regions vs 40 θ-bins ⇒ singular). Two neutral routes:
   (a) increase jackknife regions to ~100–200 (more sky patches), and/or reduce θ-bins for the
   fit window; (b) use **RascalC semi-empirical** covariance (below), which is not limited by
   region count. NEUTRAL: resampling / measured-ξ only. **Expected impact: largest — likely
   deflates the current Δχ² detections toward honesty.**

2. **RascalC semi-empirical covariance from our own measured ξ(θ).** Builds a smooth, full,
   invertible C from the data 2PCF + randoms + one jackknife-calibrated shot-noise rescale.
   NEUTRAL (data-ξ input, no mocks, no theory P(k)). Solves the region-count singularity and
   gives a stable inverse. Impact: high — makes a full C actually usable.

3. **Hartlap + Percival correction factors on the inverse covariance and parameter errors.**
   Mandatory once we invert any sample covariance. NEUTRAL. Impact: high — with few regions the
   naive C⁻¹ is badly biased; without this a full-C significance is itself untrustworthy.

4. **PIP bitweights + angular up-weighting for fiber collisions** (replace the M3 nearest-
   neighbour CP up-weight). NEUTRAL (pure survey geometry). Impact: moderate — cleans small-θ
   pair counts and the broadband shape the bump search sits on; DESI ships the bitweight files.

5. **Full randoms (undownsampled) + integral-constraint correction.** Use all DESI DR1 random
   files (we downsampled to 10×) and all BOSS random files (we used random0 only), and apply the
   Roche–Eales IC from RR. NEUTRAL. Impact: moderate — cuts RR/DR shot noise below the JK
   variance and removes the finite-area negative offset that can masquerade as broadband power.
   (Also adopt Mohammad–Percival corrected-JK weighting as a no-cost accuracy upgrade.)

--------------------------------------------------------------------------------------------
## D. FORBIDDEN LIST (F-IMPORT-LCDM — never adopt, restated for M3c)

Reconstruction (displacement fields); fiducial-cosmology z→distance / comoving conversion and
the whole 3D ξ(s) or P(k) path; sound-horizon r_d and any acoustic template / D_V–r_d fit;
ΛCDM-simulation (mock) covariances — EZmock, QPM, Patchy, GLAM, Abacus/AbacusSummit; FKP/n̄ as
shipped via the NX comoving-volume column; NX/NZ/NBAR/COMOVING/DC columns; any analytic
covariance seeded by a fiducial P(k).

--------------------------------------------------------------------------------------------
## E. Honest-ceiling statement

We can match DESI/BOSS **statistical rigor** — full bin–bin covariance, RascalC semi-empirical
C, Hartlap/Percival debiasing, integral constraint, PIP fiber-collision correction, full
randoms, proper binning — because every one of these is either pure resampling of our own data,
a survey-geometry operation, or a variance-optimization, none of which carries a cosmological
model. We **cannot** match their two biggest signal-to-noise sources: (i) **reconstruction**,
which sharpens the acoustic peak ~1.5–2× by undoing nonlinear bulk-flow smearing using a
ΛCDM-gravity displacement field, and (ii) **fiducial-distance 3D clustering**, which stacks the
full 3D signal coherently instead of diluting it across an angular projection in each thin
z-shell. Both are forbidden imports. **Therefore our detection ceiling is intrinsically lower
than the published BAO significances — this is expected from our ontology constraint, not a
failure of the method or of UDT.** The correct comparison target for us is the *pre-recon,
model-free, angular* signal, and against that baseline the matched-rigor upgrades above are the
honest maximum.

--------------------------------------------------------------------------------------------
## F. Additional-data shopping list (all pre-recon, LCDM-neutral; URLs)

- **DESI DR1 full LSS clustering catalogs + all randoms (18 files @ 2500 deg⁻²)** — we
  downsampled; get the full set:
  `https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/`
  (v1.2 also present). Use files with `clustering` in the name (LRG/ELG/QSO/BGS).
- **DESI DR1 bitweight (PIP) files** — in the same DR1 LSS tree (the "full"/target-level
  products alongside `LSScats`; bitweights per target for PIP). Datamodel:
  `https://desidatamodel.readthedocs.io/en/latest/DESI_ROOT/vac/RELEASE/lss/index.html`.
- **BOSS DR12 full randoms (random0 AND random1)** — we used only random0:
  `https://data.sdss.org/sas/dr12/boss/lss/` (DR12v5 combined, PRE-recon).
- **eBOSS DR16 pre-recon LSS catalogs** (mixed-dir hazard — pick NON-`_rec` files explicitly):
  `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/` (LRG/ELG/QSO). Cross-check grade.

--------------------------------------------------------------------------------------------
## G. Provenance / status

RESEARCH deliverable — literature + methodology only; nothing run, nothing committed.
Single-agent; grades are argued from the cited primary sources and should be spot-verified by a
blind verifier at the M3c prereg stage (per verifier-before-record). The covariance
recommendations are pre-registration inputs for a matched-rigor re-run, NOT results.
