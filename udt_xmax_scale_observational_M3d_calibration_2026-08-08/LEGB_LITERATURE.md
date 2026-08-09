# M3d LEG B — literature cross-check (published angular theta_BAO(z) vs OUR thread)

Prereg `PREREGISTRATION.md` §2 (962bd0c6, FROZEN). LEG-B agent, 2026-08-08, branch grok.
Terminology ruling in force: ours = "the observed clustering feature"; "acoustic"/"BAO" only
when attributing the mainstream's account. Published values enter as ATTRIBUTED MEASUREMENTS
(cross-check grade); no cosmology is imported into any UDT fit. NOT committed (per dispatch).

## 1. The compiled published angular-only theta_BAO(z) series

All values are the papers' own quoted measurements (degrees). "Corr." = the fiducial-projection
/ shell-width correction the authors document (the M1-graded 0.28–1.44% class); it is ALREADY
APPLIED in their quoted values and is small vs all errors here — we do not undo it (removing it
would shift values by <=1.4%, far below every combined error in §3).

### 1a. SDSS thin-shell 2PACF series (spectroscopic; Sanchez-style template = power-law + Gaussian bump)
| z | theta_BAO (deg) | err | survey/tracer | source |
|---|---|---|---|---|
| 0.11 | 19.8 | 3.26 | SDSS blue galaxies | de Carvalho et al. 2021 (A&A 649, A20; arXiv:2103.14121) |
| 0.235 | 9.06 | 0.23 | SDSS DR7 LRG | Alcaniz et al. 2017 (arXiv:1611.08458) |
| 0.365 | 6.33 | 0.22 | SDSS DR7 LRG | Alcaniz et al. 2017 |
| 0.45/0.47/0.49 | 4.77/5.02/4.99 | 0.17/0.25/0.21 | SDSS DR10 LRG | Carvalho et al. 2016 (PRD 93, 023530; arXiv:1507.08972) |
| 0.51/0.53/0.55 | 4.81/4.29/4.25 | 0.17/0.30/0.25 | SDSS DR10 LRG | Carvalho et al. 2016 |
| 0.57/0.59/0.61 | 4.59/4.39/3.85 | 0.36/0.33/0.31 | SDSS DR11 LRG | Carvalho et al. 2020 (Astropart. Phys. 119; arXiv:1709.00271) |
| 0.63/0.65 | 3.90/3.55 | 0.43/0.16 | SDSS DR11 LRG | Carvalho et al. 2020 |
| 2.225 | 1.77 | 0.31 | SDSS DR12 quasars | de Carvalho et al. 2018 (arXiv:1709.00113) |

(Compilation rows as tabulated in Nunes, Yadav, Jesus & Bernui 2020, MNRAS 497; arXiv:2002.09293, Table 1.)

### 1b. Menote & Marra 2022 (MNRAS 513, 1600; arXiv:2112.10000) — BOSS DR12 + eBOSS DR16 LRG thin shells
14 points, 0.32<z<0.66, ~3% each; projection+parametrization+RSD bias corrected (theta = theta0/(1+B);
documented systematics delta_par = delta_rsd = 1% each — their Table 1):
z=0.35:5.80±0.106, 0.37:6.07±0.136, 0.39:5.89±0.109, 0.41:5.30±0.157, 0.43:4.87±0.093,
0.45:4.52±0.150, 0.47:4.69±0.131, 0.49:4.69±0.080, 0.51:4.65±0.112, 0.53:4.03±0.089,
0.55:3.56±0.078, 0.57:4.36±0.103, 0.61:3.78±0.079, 0.63:3.90±0.080.
NOTE the group-to-group scatter at the top of the range: MM22 z=0.63 gives 3.90±0.08 while the
Carvalho series z=0.65 gives 3.55±0.16 — a ~2σ methodology spread we carry as an anchor systematic.

### 1c. DES tomographic angular BAO (photometric; angular-only observables, alpha x fiducial template)
| z_eff | quoted | theta-equivalent (deg) | source |
|---|---|---|---|
| 0.81 | D_A/r_d = 10.75±0.43 | 2.945±0.118 | DES Y1, Abbott et al. 2019 (MNRAS 483; arXiv:1712.06209) |
| 0.835 | D_M/r_d = 18.92±0.51 | 3.028±0.082 | DES Y3, Abbott et al. 2022 (PRD 105; arXiv:2107.04646) |
| 0.85 | D_M/r_d = 19.51±0.41 | 2.937±0.062 | DES Y6, Abbott et al. 2024 (arXiv:2402.10696) |
theta = (180/pi)/(D_M/r_d) — unit conversion only; the alpha-template fiducial dependence is theirs,
attributed (their documented fiducial-projection correction class = our M1 0.28–1.44% recon).

### 1d. New (2025) SDSS quasar angular-only points and DESI BGS angular
| z_eff | theta_BAO (deg) | err | source |
|---|---|---|---|
| 1.725 | 1.911 | 0.062 | SDSS quasars, arXiv:2510.15650 (projection negligible at dz=0.01, their App. A) |
| 1.775 | 1.727 | 0.081 | same |
| 0.21 / 0.25 | 11.78 / 11.81 | 1.12 / 1.20 | DESI DR1 BGS angular 2PACF, arXiv:2510.02144 |
No published angular-only QSO measurement exists between z=0.66 and z=1.725; eBOSS DR16 QSO's
official D_M(1.48)/r_d = 30.21±0.79 (Alam et al. 2021 consensus; fiducial-3D class) -> 1.897±0.050 deg,
used only in the cross-check ladder below, flagged DEPENDENT.

### 1e. Fiducial-3D reference ladder (DEPENDENT class — shape cross-check only, never primary)
DESI DR1 (arXiv:2404.03002): LRG z=0.706: D_M/r_d=16.85±0.32 -> 3.400±0.065 deg;
LRG+ELG z=0.93: 21.71±0.28 -> 2.639±0.034 deg. eBOSS QSO z=1.48 -> 1.897±0.050 deg (above).

## 2. OUR thread (verified from the banked jsons)

Centers verified from `udt_xmax_scale_observational_M3_runs_2026-08-07/bao_results_{sys,nosys}.json`
(40-bin diag): LRG 0.725→2.365/2.367, 0.925→2.337/2.329, 1.025→2.438/2.439; QSO 1.025→1.392/1.394,
1.175→2.052/2.055 (sys/nosys) — the dispatch's listed values check out.
PRIMARY comparison values = the M3c full-C Delta-chi2=1 profile centers+errors (Percival-corrected),
the 3 PRIMARY shells from `m3c_refit_results.json`, the 2 others computed HERE with the identical
frozen `rerun_m3c.theta_center_err` machinery (no pipeline change):
| shell | z | sys: theta±err | nosys: theta±err |
|---|---|---|---|
| LRG_0.70_0.75 | 0.725 | 2.437±0.223 | 2.437±0.223 |
| LRG_0.90_0.95 | 0.925 | 2.221±3.284 | 2.221±3.218 | (essentially UNCONSTRAINED at 12-bin full-C) |
| LRG_1.00_1.05 | 1.025 | 2.348±0.155 | 2.348±0.199 |
| QSO_0.95_1.10 | 1.025 | 1.450±0.126 | 1.424±0.137 |
| QSO_1.10_1.25 | 1.175 | 2.221±0.226 | 2.263±0.226 | (full-C center sits higher than the 40-bin 2.05) |

## 3. THE COMPARISON (frozen metric: per-shell pulls + global chi2)

Published curve interpolated to our z in log-log (geometric interp between adjacent angular-only
anchors — data-driven, no cosmology). Anchors: z=0.725 leg uses {MM22 z=0.63 | Carvalho z=0.65}
-> DES Y6 z=0.85 (both variants averaged, half-spread carried as systematic); z=0.925/1.025/1.175
use DES Y6 z=0.85 -> quasars z=1.725. Interp error = endpoint stat + anchor spread + SHAPE
systematic (= full |angular-interp − fiducial-3D-interp| difference, §1e), all in quadrature:
pub(0.725)=3.350±0.101, pub(0.925)=2.790±0.148, pub(1.025)=2.621±0.165, pub(1.175)=2.413±0.184 deg.

Pulls = (ours − pub)/sqrt(err_ours² + err_pub²), full-C values primary:
| shell | z | sys pull | nosys pull | M3 40-bin-center pull (ref) |
|---|---|---|---|---|
| LRG | 0.725 | **−3.73** | −3.73 | −4.02 |
| LRG | 0.925 | −0.17 | −0.18 | −0.14 (unconstrained) |
| LRG | 1.025 | −1.21 | −1.06 | −0.81 |
| QSO | 1.025 | **−5.64** | −5.58 | −5.92 |
| QSO | 1.175 | −0.66 | −0.52 | −1.24 |
GLOBAL chi2 = **47.6/5 (sys, p=4e-9)**; 46.4/5 (nosys, p=7e-9).
LRG-only: 15.4/3 (p=0.0015). Excluding QSO_1.025: 15.8/4 (p=0.003).

### The plain answer
The published theta_BAO(z) curve does NOT pass through our thread as a whole (p~1e-9,
every pull negative). Structure of the failure:
- **z≈1 LRG: CONSISTENT.** Our 2.35±0.16 vs published 2.62±0.17 -> −1.2σ. At the thread's
  strongest shell the published angular-BAO scale and our measured feature roughly coincide.
- **z=0.725 LRG: 3.7σ LOW.** Published 3.35°, ours 2.44°. Our center is ~27% below the curve.
- **QSO z≈1.02: NOWHERE on the published curve.** 1.45±0.13 vs 2.62±0.17 -> −5.6σ. It is
  smaller than EVERY published measurement at z<1.775 (the whole compiled series); on the
  extrapolated published power law, theta=1.45° corresponds to z≈2.7. No published angular
  measurement at any comparable z resembles it — consistent with either a real tracer-scale
  split the thin-shell literature has never probed at z~1 with quasars (no angular-only QSO
  point exists in 0.66<z<1.725), or a pipeline artifact specific to our low-S/N QSO shells.
- **QSO z=1.175: consistent** (−0.7σ) at the full-C center 2.22° (the 40-bin 2.05° is −1.2σ).

### The drift comparison
Published curve across our LRG range falls monotonically: 3.35° -> 2.62° over z=0.725->1.025
(**−22%**, the geometric-dilution drift every published series shows). Our LRG thread is FLAT:
2.437 -> 2.348 (full-C, **−3.6%**; the 40-bin centers even rise +3.1%). The banked anti-drift is
therefore a real disagreement with the published curve's SHAPE, driven almost entirely by the
z=0.725 point sitting low; at z≈1 the two curves cross. Equivalently: our z=0.725 and z=1.025
LRG centers are mutually consistent (~2.4°) where the published curve demands 3.35° vs 2.62°.

## 4. Honest method caveats (travel with §3)
1. Like-for-like is GOOD at the estimator level: the SDSS series fit power-law+Gaussian-bump
   templates to thin-shell 2PACFs; ours is a free Gaussian bump over a free cubic broadband —
   same object class (a localized bump over smooth broadband). It is NOT like-for-like on:
   (a) shell width — theirs dz=0.01–0.02, ours 0.05 (LRG) / 0.15 (QSO). arXiv:2511.18430 shows
   wide bins bias the recovered angle LOW (projection), safe at sigma_z<~0.04: our LRG tophat
   0.05 (sigma_z≈0.014) is safe; our QSO 0.15 (sigma_z≈0.043) sits AT the bias edge — a low-bias
   contribution to the QSO 1.45° cannot be excluded (though the neighboring QSO shell, same
   width, lands ON the curve, so uniform projection bias cannot produce the whole split).
   (b) Their quoted values carry small documented projection corrections (0.28–1.44% / 1%+1%
   MM22); ours carry none — negligible at our error level, direction noted.
   (c) DES points are alpha×fiducial-template tomographic fits (attributed, not undone).
2. The interpolated "published curve" over 0.66<z<1.725 rests on sparse anchors (DES + the 2025
   quasar points); the shape systematic (§3) covers the angular-vs-fiducial-3D spread (up to 7%)
   but a genuinely non-power-law shape between anchors is uncovered. The z=0.725 anchor spread
   (MM22 3.90 vs Carvalho 3.55 at z~0.64) is carried; even at the extreme Carvalho-only anchor
   the 0.725 pull stays ≈ −3.4σ.
3. Ours-side errors are the M3c full-C machinery (Hartlap/Percival, 12-bin JK covariance) with
   its own traveled caveats (Hartlap-on-JK; LRG–QSO independence). LRG_0.90_0.95 is
   unconstrained at 12-bin full-C (±3.3°) — its consistency is vacuous, disclosed.
4. Frozen-metric fidelity: prereg §2 fixed pulls + global chi2 BEFORE compilation; the
   interpolation scheme (log-log, data-only) was the analyst's one free choice, made before
   computing any pull, with the fiducial-3D ladder used only to bound interpolation shape error.

## 5. Prereg §5 reading (leg-B component only; leg-A mocks adjudicate separately)
Neither clean outcome: the published curve neither threads our whole data (CAL-MUNDANE leg-B
half FAILS: p~1e-9) nor misses it everywhere (the z≈1 LRG agreement is real). Component verdict
= **CAL-MIXED (leg B)**: strongest-shell scale MATCHES the published angular BAO scale; the
z=0.725 low center, the flat/anti-drift shape, and above all the 1.45° QSO point are all
EXTERNAL-TENSION features with no counterpart in the published series. Whether they are
instrument-manufactured is exactly leg A's question. HOLD for consolidation + Charles.
