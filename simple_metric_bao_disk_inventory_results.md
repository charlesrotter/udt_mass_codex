## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE / inventory |
| **Path** | `Data/BAO/` (Charles download collection) |
| **Focus** | What on disk can feed pure two-leg / kaleidoscope AP |
| **Build-on grade** | LEAD inventory |

# BAO data on disk — what we can use

## Layout (~9 GB)

| Folder | Contents | Use for pure AP? |
|--------|----------|------------------|
| **`SDSS_eBOSS_BAO/`** | Consensus \(D_M/r_d\), \(D_H/r_d\), cov, growth | **Yes — best clean table on disk** |
| **`DESI_BAO_Data/`** | Galaxy/Lyα summary CSVs, cov, growth, vizier sample | **Partial / quality-flagged** |
| **`BAO extraction/`** | DESI Lyα **RP×RT** correlation functions, cov, distortion; multi-tracer xi/Pk scraps | **Rawer** but still fiducial comoving; BAO isolation hard |

---

## 1. eBOSS consensus (use this)

File: `Data/BAO/SDSS_eBOSS_BAO/eboss_dr16_bao_consensus.csv`

Pure AP \(F_{\mathrm{obs}}=(D_M/r_d)/(D_H/r_d)\) vs residual L \(R_L=z+z^2/2\):

| \(z\) | Tracer | \(F_{\mathrm{obs}}\) | \(R_L\) | \(F/R_L\) | pull |
|------|--------|----------------------|---------|-----------|------|
| **0.380** | LRG | 0.452 | 0.452 | **1.000** | **−0.01** |
| **0.510** | LRG | 0.631 | 0.640 | **0.985** | **−0.30** |
| 0.698 | ELG | 0.858 | 0.942 | 0.911 | −1.3 |
| 0.845 | QSO | 0.913 | 1.202 | 0.76 | −2.9 |
| 1.48 | QSO | 2.28 | 2.58 | 0.89 | −1.8 |
| 2.33 | Lyα | 4.18 | 5.06 | 0.83 | −3.8 |

**Lay:** With **your on-disk eBOSS numbers**, the two lowest LRG bins sit **on** the kaleidoscope curve. That is stronger contact than the mixed literature scrape used earlier. Higher‑\(z\) / messier tracers still run low.

---

## 2. Local DESI CSVs — quality flag

Files under `DESI_BAO_Data/` look **prepared for an older UDT fit narrative** (README: βr², “no DE”, χ² success criteria). They are **not** a faithful dump of DESI DR1 anisotropic Table 1:

| Issue | Detail |
|-------|--------|
| \(D_H\) at \(z=0.51\) | Local **20.0**; official paper **20.98** |
| Bins | Only 3 galaxy rows + Lyα; missing LRG2/3, ELG2, QSO anisotropic split as in paper |
| \(z=0.706\) row | Labeled ELG with \(D_M=18.33\) — does **not** match official LRG2 \(D_M=16.85\), \(D_H=20.08\) |
| Vizier `table0` | Object redshift catalog sample — **not** BAO peaks |

**Do not treat local DESI CSVs as anisotropic BAO authority.** Prefer arXiv:2404.03002 Table 1 (or re-download official products). Local Lyα \(D_M/D_H\approx 4.22\) is in the right ballpark vs paper ~4.66.

---

## 3. “Rawer” extracts — what they are

### Lyα (and QSO×Lyα) correlation functions  
`BAO extraction/extracted_cf_*_exp_cor.csv`

- Columns: `DA` (ξ), `RP`, `RT`, `Z`, `NB`, cov diagonal  
- Header: **fiducial \(\Omega_m=0.315\)**, coordinates in \(h^{-1}\mathrm{Mpc}\)  
- Mean \(z\sim 2.34\)  
- Monopole-ish BAO bump near \(r\sim 100\,h^{-1}\mathrm{Mpc}\) (as expected)  
- **Not** pure \((\theta,\Delta z)\): already converted with a fiducial cosmology  
- Peak isolation in RP vs RT strips is **noisy** (broadband + weak BAO); needs template / wedge analysis, not a one-line max  

**Use:** future careful two-leg peak work in fiducial chart (still one step above \(D_M/D_H\), one step below raw angle).  
**Not yet:** drop-in replacement that “resolves high \(z\)” without further reduction.

### Multi-tracer ξ / P(k)  
CSV/dat under extraction — **appear truncated / incomplete** (few lines); not usable as full multipoles without the original complete files.

### Distortion matrices / huge cov  
Present; useful only with a full BAO fitter, not for a quick pure-AP number.

---

## 4. What this means for the high‑\(z\) question

| Data tier on disk | Verdict |
|-------------------|---------|
| eBOSS LRG \(z\sim 0.4\)–\(0.5\) | **Kaleidoscope AP lands** |
| eBOSS higher \(z\) | Still low vs \(R_L\) (same pattern) |
| Local DESI tables | **Don’t trust** for this test |
| Lyα RP×RT CF | **Closer to raw**, still fiducial-Mpc; not yet reduced to clean \((\theta_*,\Delta z_*)\) |

So: **yes, the collection is usable**, and the **best pure-AP contact so far is your on-disk eBOSS LRG bins**.  
**No**, we did not yet get a pure angular/redshift peak catalog that could adjudicate high-\(z\) packaging — the CF files are the right *direction* but need a proper BAO-peak reduction.

---

## Recommended use of this folder

1. **Now:** pure AP from `eboss_dr16_bao_consensus.csv` (authoritative on disk).  
2. **DESI:** use published Table 1, not the simplified local galaxy CSV.  
3. **Later (if pursuing rawer):** BAO template / wedge fit on `extracted_cf_lya_x_lya_exp_cor.csv` (+ cov) to extract \(s_\parallel\), \(s_\perp\) peak ratio at \(z\sim 2.3\).  
4. Ignore vizier object table for BAO geometry.

Machine: `simple_metric_bao_disk_inventory_out.json`

---

## One-line

**On-disk eBOSS consensus is the gold for pure AP (LRG bins sit on \(R_L\)); local DESI summaries are suspect; Lyα RP×RT CFs are the rawest useful layer but still fiducial-comoving and need a real peak pipeline.**
