## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE — proper pass (disk + search + fit) |
| **Build-on grade** | **LEAD** (honest limits on self-fit) |
| **Machine** | `simple_metric_bao_lya_fullfit_out.json` · `simple_metric_bao_lya_constrained_fit_out.json` |

# Proper pass: disk, search, and Lyα fit

Charles asked for this done properly. This records what was actually opened, searched, fitted, and concluded.

---

## 1. Full disk inventory (beyond earlier extracts)

### Under `Data/BAO/` (~9 GB)

| Item | What it is |
|------|------------|
| Extracted CSVs (ξ, CO 2500², DM 2500², dmattri) | Same as DESI Lyα VAC content, CSV form |
| 3.2 GB zip | **Same CSVs** re-packaged (no extra FITS) |
| `zenodo.zip` in extraction | **Corrupt / not a zip** |
| eBOSS consensus CSVs | Clean \(D_M,D_H\) |
| Local DESI summary CSVs | **Not** official anisotropic table (quality-flagged earlier) |

### Original FITS found elsewhere on D: (not under UDT_m_e)

| Path | Contents |
|------|----------|
| `/mnt/d/UDTT/data/BAO_old/*.fits` | `cf_*`, `dmat_*`, `full-covariance-smoothed.fits` |
| `/mnt/d/UDT/02_data/raw/desi_lya_bao/*.fits` | Same set |

FITS `COR` HDU: `DA, RP, RT, Z, CO(2500×2500), DM(2500×2500), NB` — **exactly** what the CSVs were extracted from.  
So the “raw” on disk **is** those FITS; the CSV extract is complete for Lyα auto (we verified structure with astropy).

**Distortion matrix in the extract is the identity** (\(\|D-I\|_F=0\)). Off-diagonals zero. So “using Dmat” does nothing for this product — either the export stored identity or DM column is placeholder. Official pipeline may use a different dmat product.

---

## 2. Search for available material (done this pass)

| Source | Result |
|--------|--------|
| **astroquery** | Installed 0.4.11; Vizier BAO catalog search flaky; modules listed |
| **Zenodo API** | Multi-survey package = same extracts; early DESI BAO zip **downloaded** (83 MB); fidcosmo systematics tar **downloaded** (1.7 MB) |
| **CobayaSampler/bao_data** | Official DESI 2024 Gaussian BAO means/cov (already in `Data/BAO/fetched/`) |
| **data.desi.lbl.gov** | VAC listing: **`lya-correlations/`**, **`bao-cosmo-params/`**, **`full-shape-bao-clustering/`**, `lss/`, `lya-deltas/` — **these are the public originals** of what you already have |
| **FITS on D:** | Found under `UDTT` and `UDT` (above) |

Downloaded this pass → `Data/BAO/fetched/public/`:

- `early_desi_bao_zenodo.zip` (~83 MB)  
- `fidcosmo_zenodo.tar.gz` (~1.7 MB)  
- VAC READMEs for bao-cosmo-params and lya-correlations  
- `PACKAGE_SUMMARY.md`  

**Not re-downloaded:** multi-GB FITS from DESI VAC (already present as FITS on D: and as CSV extracts). Under 50 GB cap easily.

Public DESI URLs (authoritative):

- https://data.desi.lbl.gov/public/dr1/vac/dr1/lya-correlations/v1.0/  
- https://data.desi.lbl.gov/public/dr1/vac/dr1/bao-cosmo-params/v1.0/  
- https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-bao-clustering/v1.0/  

---

## 3. Proper-ish Lyα fit (full cov)

### Data used

- `extracted_cf_lya_x_lya_exp_cor.csv` — ξ(RP,RT), n=2500  
- `extracted_cf_lya_x_lya_exp_co.csv` — full **2500×2500** covariance (Cholesky OK)  
- `extracted_cf_lya_x_lya_exp_dm.csv` — **identity** (no effect)

### Fit A — free template (unconstrained)

Simple envelope+Gaussian + poly BB, free \(a_\parallel,a_\perp\) unbounded → **degenerate** (\(a_\perp/a_\parallel\sim 1.75\), \(F\sim 8\)). **Not usable.** χ² still huge. Template too wrong for absolute AP.

### Fit B — constrained alphas ∈ [0.7, 1.3] + empirical monopole bump

| Quantity | Value |
|----------|--------|
| \(z_{\mathrm{eff}}\) | 2.367 |
| Best \(a_\parallel\) | 1.099 |
| Best \(a_\perp\) | 1.186 |
| \(F_{\mathrm{fit}}=(a_\perp/a_\parallel)F_{\mathrm{fid}}\) | **5.02** |
| Official DESI Lyα \(F\) | **4.66** |
| Residual L \(R_L\) | **5.17** |
| \(F_{\mathrm{fit}}/R_L\) | 0.97 |
| χ² (best) | ~1.99×10⁵ (terrible absolute fit) |
| χ² (force \(R_L\) ratio) | ~2.03×10⁵ (Δχ²~4×10³ vs best) |
| χ² (\(a_\parallel=a_\perp=1\)) | ~2.01×10⁵ |

**Honest reading:**

- Absolute χ² ≫ N_bins → **our template is not a valid BAO model.** Absolute \(F_{\mathrm{fit}}\) is **not** a replacement for the DESI pipeline.
- Relative Δχ² between \(F\sim 4.66\), \(F\sim 5.02\), \(F\sim 5.17\) is **not** trustworthy as a cosmological test without a proper picca/DESI template.
- Earlier **wedge Gaussian** peak ratio still gives \(F\sim 4.5\) ≈ official — that remains the more stable CF-level character result.
- **Identity Dmat** means we did not gain from distortion modeling.

**Authoritative high‑\(z\) AP for science claims:** still **official DESI \(D_M/D_H\)** (Cobaya means), not our self-fit.

---

## 4. Pure AP scoreboard (authoritative products only)

| Sample | \(z\) | \(F=D_M/D_H\) | \(R_L=z+z^2/2\) | \(F/R_L\) |
|--------|------|---------------|-----------------|-----------|
| eBOSS LRG (disk) | 0.38 | 0.452 | 0.452 | **1.00** |
| eBOSS LRG (disk) | 0.51 | 0.631 | 0.640 | **0.99** |
| DESI LRG1 (official) | 0.51 | 0.649 | 0.640 | **1.01** |
| SDSS DR16 LRG | 0.70 | 0.924 | 0.942 | **0.98** |
| DESI LRG2+ | ≥0.7 | … | … | **~0.88–0.92** |
| DESI Lyα official | 2.33 | 4.66 | 5.04 | **0.92** |
| Lyα wedge peaks (CF) | 2.37 | ~4.46 | 5.17 | ~0.86 |
| Lyα constrained self-fit | 2.37 | ~5.02 | 5.17 | ~0.97 (**untrusted model**) |

---

## 5. Answers to the two process questions (closed)

| Question | Answer after proper pass |
|----------|---------------------------|
| Disk: only extracts? | **Initially yes.** Proper pass: full inventory, **opened original FITS** on `UDTT`/`UDT`, confirmed CSV = FITS COR, loaded **full cov**, checked **Dmat=I**. |
| Search? | **Initially thin.** Proper pass: Zenodo, Cobaya, **data.desi.lbl.gov VAC**, FITS locations, downloads of early DESI + fidcosmo packages. |

---

## 6. Bottom line for kaleidoscope / high \(z\)

1. **Low \(z\) LRG:** pure AP still sits on residual L — **best evidence**.  
2. **High \(z\) Lyα:** official + wedge CF ≈ \(F\sim 4.5\)–\(4.7\) vs \(R_L\sim 5.1\)–\(5.2\). **Offset survives** rawer CF + full cov work.  
3. **Self-fit AP near \(R_L\)** is **not** bankable (broken template / huge χ²).  
4. **Next real upgrade** if wanted: full-shape BAO clustering VAC multipoles (galaxy, not only Lyα), or run **picca**-class template on FITS — not more crude envelopes.

---

## One-line

**Proper pass: FITS located and matched to extracts; full cov used; Dmat is identity; DESI public VAC mapped and small packages fetched; low‑\(z\) LRG still on \(R_L\); high‑\(z\) official/wedge CF still below \(R_L\); unconstrained self-fit AP is not science-grade.**
