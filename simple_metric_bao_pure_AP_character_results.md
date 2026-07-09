## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (character) |
| **Focus** | BAO as pure two-leg appearance — **not** ΛCDM \(r_d\) / dark-energy packaging |
| **Geometry** | residual L kaleidoscope (center seat) |
| **Build-on grade** | **LEAD / character** — not a cosmology conviction |
| **Data** | DESI DR1 BAO Table 1 (arXiv:2404.03002) |
| **Machine** | `simple_metric_bao_pure_AP_out.json` |

# BAO without ΛCDM framing — pure \((\theta_*,\Delta z_*)\) vs residual L

## What we refuse

| ΛCDM package | Status here |
|--------------|-------------|
| Sound horizon \(r_d\sim 147\,\mathrm{Mpc}\) from early plasma | **Not used** as physics |
| Dark energy / \(w_0 w_a\) fits | **Out of scope** |
| “BAO proves Λ” | **Not the question** |
| Matching \(D_V/r_d\) tracks for cosmology contests | **Not the goal** |

## What we keep (closer to pure observation)

A preferred clustering scale shows up as **two legs** of the same ridge:

| Leg | Raw-ish content | Catalog proxy (rd cancels in ratio) |
|-----|-----------------|-------------------------------------|
| **Transverse** | peak angular separation \(\theta_*\) at mean \(z\) | \(D_M/r_d \propto 1/\theta_*\) |
| **Radial** | peak redshift thickness \(\Delta z_*\) | \(D_H/r_d \propto 1/\Delta z_*\) |

**Pure AP observable (one number per \(z\)):**
\[
F_{\mathrm{obs}}(z)\;=\;\frac{(D_M/r_d)}{(D_H/r_d)}\;=\;\frac{D_M}{D_H}\;\approx\;\frac{\Delta z_*}{\theta_*}
\]
(\(\theta_*\) in radians). **\(r_d\) cancels.** No early-universe ruler length required for this test.

**Caveat (honest):** DESI still *measures* clustering after converting \((z,\mathrm{RA,Dec})\) with a **fiducial** cosmology. \(F_{\mathrm{obs}}\) is the standard nearly model-robust AP combination, not a from-scratch pair catalog re-reduction. Character tile, not a blind re-analysis of raw catalogs.

---

## Residual L prediction (kaleidoscope)

Fixed **proper** stick length \(\ell\) at depth \(z\) (center seat, residual \(A=1-r/X\)):

\[
\theta=\frac{\ell}{d_A},\qquad
d_A=X\Bigl(1-\frac{1}{(1+z)^2}\Bigr),\qquad
\Delta z = H_0(1+z)^2\,\ell,\quad H_0=\frac{1}{2X}.
\]

Ratio (**stick length cancels**):
\[
\boxed{R_L(z)\;=\;\frac{\Delta z}{\theta}\;=\;z+\frac{z^2}{2}}.
\]

**Lay:** if the ridge is one physical stick seen across the sky and along the line of sight, residual L fixes how fat in \(\Delta z\) it must be for a given angle — at every \(z\), with **no free function**.

This is exactly the kaleidoscope AP tile: two instruments, one residual map.

---

## DESI DR1 two-leg data vs \(R_L\)

Anisotropic bins only (BGS/QSO are isotropic \(D_V/r_d\) — no two-leg split):

| Tracer | \(z_{\mathrm{eff}}\) | \(F_{\mathrm{obs}}=D_M/D_H\) | \(\sigma\) | \(R_L=z+z^2/2\) | \(F/R_L\) | pull \((F-R_L)/\sigma\) |
|--------|----------------------|------------------------------|------------|-----------------|-----------|-------------------------|
| LRG1 | 0.510 | 0.649 | 0.022 | 0.640 | **1.014** | **+0.4** |
| LRG2 | 0.706 | 0.839 | 0.030 | 0.955 | 0.879 | −3.9 |
| LRG3+ELG1 | 0.930 | 1.214 | 0.029 | 1.362 | 0.891 | −5.2 |
| ELG2 | 1.317 | 2.011 | 0.079 | 2.184 | 0.921 | −2.2 |
| Lyα | 2.330 | 4.661 | 0.144 | 5.044 | 0.924 | −2.7 |

**Summary**

| Diagnostic | Value |
|------------|--------|
| \(F_{\mathrm{obs}}/R_L\) mean | \(0.93\pm 0.05\) (scatter) |
| Lowest \(z\) (0.51) | **statistically on L** (\(\sim 1\%\), \(0.4\sigma\)) |
| \(z\gtrsim 0.7\) | \(F_{\mathrm{obs}}\) **systematically \(\sim 8\)–\(12\%\) below** \(R_L\) |
| \(\chi^2(R_L)\) 0 free params, \(N=5\) | \(\approx 54\) — **not a pass** |
| Same \(\chi^2\) flat ΛCDM \(F_{\mathrm{AP}}\) (Om=0.315, AP only) | \(\approx 10\) — better AP match |
| Nuisance \(F=k\,R_L\) | \(k\approx 0.92\), \(\chi^2\approx 11\) — overall rescaling helps; **shape still imperfect** |

---

## How to read this (lay)

1. **The two-component idea is right for the data language.**  
   BAO-as-observed is naturally “angle peak + redshift peak,” not “dark energy parameter.”

2. **Residual L makes a sharp, parameter-free claim about those two peaks.**  
   \(\Delta z/\theta = z + z^2/2\).

3. **At the nearest good two-leg bin (\(z\sim 0.5\)), that claim lands.**  
   Not a proof — one bin — but not a wild miss either.

4. **Across the DESI ladder, L’s AP ratio runs a bit high.**  
   Data want a **mildly smaller** \(\Delta z/\theta\) than pure L proper-stick geometry, more like the usual FLRW AP track.  
   So: kaleidoscope AP is **in the right family** (order unity, rising with \(z\)), **not** an automatic multi-\(z\) win.

5. **What this does *not* do**  
   - Does not derive why the stick exists (micro/cells still shelved).  
   - Does not use or need \(r_d\).  
   - Does not certify or kill residual L from SNe; this is **only** the two-leg ratio.  
   - Absolute \(\theta_*(z)\) or \(\Delta z_*(z)\) still needs one stick scale (or \(X/\ell\)); the **ratio** is the clean test.

---

## Absolute legs (secondary; needs scale)

If one *assumes* L and asks what \(X/\ell\) each leg wants, transverse and radial legs **disagree** and the disagreement grows with \(z\) — the same AP tension restated. Not an independent test.

Isotropic-only bins (BGS, QSO): only \(D_V/r_d\); **cannot** do pure two-leg AP without more assumptions.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Residual L, center seat, proper stick | WORKING geometry |
| \(F_{\mathrm{obs}}=(D_M/r_d)/(D_H/r_d)\) ≈ \(\Delta z/\theta\) | STANDARD BAO AP proxy; **rd cancels** |
| DESI Table 1 numbers | PUBLISHED (fiducial-converted clustering) |
| Same stick transverse & radial | FREE premise of isotropic proper feature |
| Observing or targeting? | OBSERVE character of two-leg ratio vs L |
| Sound-horizon mechanism | **Not invoked** |

---

## Link to kaleidoscope stack

| Prior tile | Relation |
|------------|----------|
| K2/K3 ruler + AP stretch | This **is** that tile aimed at published two-leg BAO |
| MINE “no angular BAO from pure L” | Still true: L does not *create* the stick |
| Charles “two components / drop LCDM framing” | Operationalized as \(F_{\mathrm{obs}}=\Delta z/\theta\) vs \(R_L\) |

---

## eBOSS / BOSS cross-check (survey scatter)

**Chronology:** eBOSS DR16 ≈ final SDSS-IV BAO (~2020–21). **DESI DR1 is later and tighter.** Both are valid; they do **not** always agree bin-by-bin — Charles’s point stands.

Same pure test \(F_{\mathrm{obs}}=D_M/D_H\) vs \(R_L=z+z^2/2\):

| Sample | \(z\) | \(F_{\mathrm{obs}}\) | \(R_L\) | \(F/R_L\) | pull |
|--------|------|----------------------|---------|-----------|------|
| BOSS Gal | 0.38 | 0.409 | 0.452 | 0.90 | −3.0 |
| BOSS Gal | 0.51 | 0.598 | 0.640 | 0.93 | −2.3 |
| **eBOSS LRG** | **0.70** | **0.924** | **0.945** | **0.98** | **−0.7** |
| eBOSS ELG | 0.85 | 0.963 | 1.202 | 0.80 | −3.0 |
| eBOSS QSO | 1.48 | 2.28 | 2.58 | 0.89 | −2.9 |
| eBOSS Lyα | 2.33 | 4.17 | 5.04 | 0.83 | −5.5 |

**Survey scatter at same depth (illustration):**

| \(z\sim\) | BOSS/eBOSS \(F\) | DESI \(F\) | \(R_L\) |
|-----------|------------------|------------|---------|
| 0.51 | 0.598 | **0.649** | 0.640 |
| 0.70 | **0.924** | 0.839 | 0.945 |
| 2.33 | 4.17 | 4.66 | 5.04 |

So: **match DESI at 0.51 ⇔ mild tension with BOSS at 0.51; match eBOSS LRG at 0.70 ⇔ tension with DESI at 0.70.**  
Data really are “all over” relative to a sharp zero-parameter curve — not only relative to each other.

**Best single contacts with residual L AP:** DESI LRG1 (\(z\sim 0.51\), \(\sim 0.4\sigma\)) and **eBOSS LRG (\(z\sim 0.70\), \(\sim 0.7\sigma\))**.

Machine: `simple_metric_bao_pure_AP_eboss_out.json`.

---

## If kaleidoscope accounts for the two-leg map

**Charles:** if kaleidoscope accounts for it, no other origin explanation is necessary.

**Scoped agreement (geometry, not mythology):**

| What | Need a separate origin story? |
|------|-------------------------------|
| **Why \(\Delta z/\theta\) has this \(z\)-shape** (two legs of one stick) | **No** — residual L predicts \(R_L=z+z^2/2\) as pure appearance. Sound horizon, dark energy, fluid oscillators are **not required** for that geometric relation. |
| **Why a preferred scale exists at all** (a ridge to measure) | Can stay a **bare fact of the catalog** until micro — not forced to import LCDM BAO plasma. |
| **Absolute Mpc calibration of the stick** | Still one scale (or \(X/\ell\)); not supplied by AP ratio alone. |

So: **kaleidoscope can be the account of the two-component BAO *as observed geometry*.**  
That is not the same as “every BAO number in every survey is a perfect L fit.” Surveys disagree; L hits some bins hard and sits high on others. The **claim that survives** is: the *mapping* is residual appearance of a stick, not LCDM packaging — and where data land near \(R_L\), **no extra mechanism is owed for that landing.**

---

## Next (if pursued)

1. Re-express peaks as explicit \((\theta_*,\Delta z_*)\) where fiducial can be unwound.  
2. Hold multi-survey scatter as first-class (don’t crown one campaign).  
3. **Not next:** fluid BAO / \(r_d\) fitting as required origin.

---

## One-line

**Pure two-leg BAO is \(\Delta z/\theta\); L predicts \(z+z^2/2\) with no \(r_d\); DESI \(z\sim 0.5\) and eBOSS LRG \(z\sim 0.7\) sit on that curve while surveys scatter and higher-\(z\) bins run low — kaleidoscope can own the two-leg *map* without an LCDM origin story.**
