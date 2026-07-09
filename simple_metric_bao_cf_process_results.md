## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Work** | (b) process handed BAO files + fetch official DESI means |
| **Paths** | `Data/BAO/BAO extraction/` · `Data/BAO/fetched/` (CobayaSampler/bao_data) |
| **Build-on grade** | **LEAD** |

# Processing local CF + official products vs residual L AP

## What was done

1. **Processed** DESI DR1 Lyα auto correlation on disk (`extracted_cf_lya_x_lya_exp_cor.csv`): 50×50 \((R_\parallel,R_\perp)\) in \(h^{-1}\mathrm{Mpc}\), fiducial \(\Omega_m=0.315\).
2. **BAO isolation:** poly broadband + **Gaussian bump** fits on μ-wedges; monopole bump at \(r_0\sim 103\,h^{-1}\mathrm{Mpc}\).
3. **Fetched** official DESI 2024 Gaussian BAO means/cov from [CobayaSampler/bao_data](https://github.com/CobayaSampler/bao_data) → `Data/BAO/fetched/` (~200 KB, well under budget).
4. **Re-ran pure AP** \(F=D_M/D_H\) vs \(R_L=z+z^2/2\) on authoritative numbers + on-disk eBOSS.

astroquery is installed; for this tile the **bao_data GitHub products** were the cleanest small public release (same content as DESI likelihood inputs). No multi-GB download required.

---

## A. Official DESI 2024 pure AP (from fetched means)

| Sample | \(z\) | \(F_{\mathrm{obs}}=D_M/D_H\) | \(R_L=z+z^2/2\) | \(F/R_L\) | pull |
|--------|------|------------------------------|-----------------|-----------|------|
| LRG1 | 0.510 | 0.649 | 0.640 | **1.014** | **+0.4** |
| LRG2 | 0.706 | 0.839 | 0.955 | 0.879 | −3.9 |
| LRG3+ELG | 0.930 | 1.214 | 1.362 | 0.891 | −5.2 |
| ELG2 | 1.317 | 2.011 | 2.184 | 0.921 | −2.2 |
| Lyα | 2.330 | 4.661 | 5.044 | 0.924 | −2.7 |

Same pattern as before: **low‑\(z\) LRG lands; higher \(z\) systematically ~8–12% low vs \(R_L\).**

---

## B. On-disk eBOSS (unchanged gold contact)

| \(z\) | \(F/R_L\) | pull |
|------|-----------|------|
| **0.38 LRG** | **1.000** | **−0.01** |
| **0.51 LRG** | **0.985** | **−0.30** |
| ≥0.70 | 0.76–0.91 | low |

---

## C. Lyα CF processing (your files) — the key test of “rawer”

| Method | Result |
|--------|--------|
| Monopole residual peak | \(r\sim 100.5\,h^{-1}\mathrm{Mpc}\) (BAO-scale present) |
| Gaussian bump, radial wedge \(\mu>0.5\) | \(r_{0,\parallel}\approx 103.0\pm 2.7\) |
| Gaussian bump, transverse \(\mu<0.5\) | \(r_{0,\perp}\approx 98.6\pm 5.7\) |
| Peak ratio \(r_\perp/r_\parallel\) | \(\approx 0.957\) |
| \(F_{\mathrm{CF}}\approx (r_\perp/r_\parallel)\,F_{\mathrm{fid}}\) | \(\approx\mathbf{4.46}\) |
| Official DESI Lyα \(F\) | \(\approx\mathbf{4.66}\) |
| Residual L \(R_L(z\sim 2.37)\) | \(\approx\mathbf{5.17}\) |

**Lay reading:**

- Starting from **your RP×RT correlation function** (one step closer to the measurement than a cosmology paper table) and pulling two-leg BAO peaks **recovers \(F\) consistent with the official DESI Lyα product** (~4% low, within crude-method error).
- It does **not** move \(F\) up to residual L’s \(R_L\sim 5.2\).

So for high‑\(z\) Lyα: **the tension with \(R_L\) is not mainly “DESI packaged \(D_M/D_H\) wrong vs the CF.”** The CF itself, in the fiducial chart, already encodes an AP ratio near the published value.

**Caveats (honest):**

- Coordinates are still **fiducial comoving Mpc**, not raw \((\Delta\theta,\Delta z)\).
- Gaussian+poly is a **crude** BAO isolator vs the collaboration’s metal/continuum/distortion pipeline.
- Radial high-μ Lyα is noisy; treat CF-derived \(F\) as **exploratory confirmation**, not a new official measurement.

**First (failed) wedge max without a bump model** put the radial peak at ~137 Mpc (artifact). **Bump fit** repaired that → ~103 Mpc. Method matters; conclusion after repair is stable: **CF ≈ official, not ≈ \(R_L\).**

---

## D. Does “rawer data resolve high \(z\)?”

| Hypothesis | After this work |
|------------|-----------------|
| High‑\(z\) residual is only FLRW **table packaging** | **Weakened** for Lyα: CF → same \(F\) family as official |
| High‑\(z\) residual is **L paint / static chart** domain | **Still live** |
| Low‑\(z\) kaleidoscope contact is real | **Strengthened** (eBOSS LRG + DESI LRG1) |
| Need fluid BAO origin for two-leg map | **Still no** — geometry account of the *map* stands; high \(z\) is a **shape** stress |

---

## Files written / used

| Path | Role |
|------|------|
| `Data/BAO/fetched/desi_2024_gaussian_bao_*` | Official DESI means/cov |
| `Data/BAO/BAO extraction/extracted_cf_lya_x_lya_exp_cor.csv` | Processed CF |
| `simple_metric_bao_lya_cf_peaks_out.json` | First pass peaks |
| `simple_metric_bao_process_out.json` | Combined machine out |
| This doc | Results |

---

## One-line

**Processed your Lyα RP×RT CF: BAO two-leg peaks give \(F\sim 4.5\), matching official DESI Lyα (~4.7), not residual L (~5.2) — rawer CF does not erase the high‑\(z\) AP offset; low‑\(z\) LRG contact remains the strong kaleidoscope hit.**
