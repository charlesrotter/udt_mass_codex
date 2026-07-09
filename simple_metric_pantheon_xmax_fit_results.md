# Pantheon+ one-fit of \(x_{\max}\) + downstream consilience


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | static hyp J1; N=1580 full cov |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | LCDM Om=0.3 residual ref only |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **DEMO** |
| **Re-run commands** | see body / associated `*.py` if any |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body of this document | full ledger in sections | mixed — re-read body | Y |

### What is NOT claimed

- Physics canon (Charles only). Hygiene grade ≠ nature proof.
- Claims wider than **Slice scope** above.

### Do not build on (if any)

- Anything tagged CHOSE/explore in the body without re-stating premises.

---

**Date:** 2026-07-08 · **Mode: OBSERVE** (one pre-registered calibration)  
**Script:** `simple_metric_pantheon_xmax_fit.py`  
**JSON:** `simple_metric_pantheon_xmax_fit_out.json`  
**Data:** `/mnt/d/UDTDATA/SNe/Pantheon_SH0ES.dat`  
**Status:** **PROVISIONAL** — shape **fails** data systematically; absolute \(X\) is a scale pin only, not a pure prediction.

**Full cov (Charles paths 2026-07-08):** `Data/Pantheon+SH0ES.dat` + `Data/Pantheon+SH0ES_STAT+SYS.cov`  
**Script:** `simple_metric_pantheon_xmax_fit_fullcov.py` · **JSON:** `simple_metric_pantheon_xmax_fit_fullcov_out.json`  
**Verdict under full STAT+SYS:** same **shape FAIL** (stronger χ²); scale pin almost unchanged.

---

## 0. Pre-registered contract (frozen before run)

| Item | Choice | Tag |
|------|--------|-----|
| Model | \(d_L=X\,(1+z)^2\frac{(1+z)^2-1}{(1+z)^2+1}\) | THEORY under J1 + xmax postulate + n=2 |
| Free (shape score) | **1** additive offset only | \(M_B + 5\log_{10}X\) degenerate |
| Free (absolute \(X\)) | \(X\) with conventional \(M_B\) | \(M_B\) = **CONVENTION** (not derived) |
| Not free | Om, \(w\), free \(D_A\), 1101, shape knobs | — |
| Cut | `IS_CALIBRATOR==0`, `zHD>0.01` | same as prior repo SNe scripts |
| Errors | diagonal `m_b_corr_err_DIAG` | fast first look; full cov unpaid |
| Label | **Pantheon-calibrated \(x_{\max}\)** | not a pure prediction of \(X\) |
| Downstream | \(M_{\mathrm{tot}}=c^2 X/(2G)\) under J1; shell \(x/X\) at high \(z\) = check only | characterize |

**Observing or targeting?** Observing residual of the **held** form. Not retuning the law after residual.

---

## 1. Sample

- \(N=1580\) SNe after cut  
- \(z\in[0.0102,\,2.2614]\)

---

## 2. Shape result (primary)

### Full STAT+SYS covariance (authoritative for χ²)

| Model | RMS (mag) | \(\chi^2/\mathrm{dof}\) (full cov) | \(\chi^2\) |
|-------|-----------|-------------------------------------:|-----------:|
| **Hyperbolic n=2** (1 offset) | **0.307** | **2.17** | 3421 / 1579 |
| flat LCDM \(\Omega_m=0.3\) ref (1 offset) | 0.154 | **0.88** | 1390 / 1579 |

**Δχ² (hyp − LCDM) ≈ +2031** at same dof — not a marginal miss.

### Diagonal (earlier first look; still useful for RMS)

| Model | RMS (mag) | \(\chi^2/\mathrm{dof}\) (diag) |
|-------|-----------|--------------------------------|
| **Hyperbolic n=2** (1 offset) | **0.307** | **1.77** |
| flat LCDM \(\Omega_m=0.3\) ref (1 offset) | 0.154 | 0.44 |

**ΔRMS ≈ +0.15 mag** vs LCDM reference (hyperbolic worse). Full cov does **not** rescue the shape.

### Residual trend (hyp; res = \(m_{\mathrm{obs}} - m_{\mathrm{model}}\))

| \(z\) bin | \(n\) | mean res | |
|-----------|------:|---------:|--|
| 0.01–0.1 | 620 | **+0.24** | model too close (under-distance) at low \(z\) once mid-band set |
| 0.1–0.3 | 466 | −0.01 | near zero |
| 0.3–0.6 | 365 | **−0.22** | model over-distance |
| 0.6–1.0 | 104 | **−0.52** | worse |
| 1.0–2.5 | 25 | **−0.84** | severe |

**Shape reading (lay):** after one scale is set, the hyperbolic law puts **too much luminosity distance at high \(z\)** relative to Pantheon+ (SNe look systematically too bright vs the model). The mismatch grows with \(z\); it is not random scatter.

### Shape ratio (hyp vs LCDM, matched at \(z=0.05\))

| \(z\) | \(\Delta\mu\) (hyp − LCDM) |
|------:|---------------------------:|
| 0.10 | +0.04 mag |
| 0.30 | +0.16 |
| 0.50 | +0.25 |
| 1.00 | +0.44 |
| 2.00 | +0.71 |

Low-\(z\) series: hyp \(d_L/X = z + \tfrac32 z^2+\cdots\); LCDM \(\Omega_m=0.3\) is closer to \(z + 1.275\,z^2+\cdots\). The hyp law is **stiffer** (more distance growth).

**C5 numeric:** **FAIL** (scoped: this form + J1 + diagonal Pantheon+). Not a conviction of the metric alone — of **this kinematic cascade as a SNe distance law**.

---

## 3. Absolute \(X\) (scale pin only)

Shape score cannot separate \(X\) from \(M_B\). Absolute \(X\) needs a **conventional** SN Ia absolute magnitude (CHOSE, not theory):

| \(M_B\) (convention) | \(X=x_{\max}\) (Mpc) |
|---------------------:|---------------------:|
| −19.00 | 3196 |
| **−19.25** (primary report) | **~3596** (full cov offset) / 3586 (diag) |
| −19.50 | ~4035 |

RMS is **identical** for all three (pure degeneracy).  
**Language:** Pantheon-calibrated \(x_{\max}\approx 3.6\,\mathrm{Gpc}\) at \(M_B=-19.25\) — **not** a derived pure number.

---

## 4. Downstream consilience

### 4a. Mass lock (J1) — automatic, not independent

\[
M_{\mathrm{tot}}=\frac{c^2 X}{2G}
\quad\Rightarrow\quad
M_{\mathrm{tot}}\approx 3.75\times 10^{22}\,M_\odot
\quad(\log_{10}M/M_\odot\approx 22.57)
\]

at primary \(X=3586\,\mathrm{Mpc}\).

This is the **definition** of the J1 lock once \(X\) is fixed — it does **not** add a second observational win. It converts the SNe ruler into a total-mass label.

### 4b. Mean density in a ball of radius \(X\)

\[
\bar\rho = \frac{M_{\mathrm{tot}}}{\tfrac43\pi X^3} = \frac{3c^2}{8\pi G X^2}
\]

is an **identity** of \(M=c^2X/(2G)\) + ball volume — same number as a \((c/X)\)-scale critical density. **Not new consilience.**

### 4c. High-\(z\) shell (check only, not foundation)

At \(z=1100\): \(x/X\approx 0.999998\), \(A\sim 10^{-6}\) — kinematic near-bound, as expected.  
At \(z=2\): \(x/X=0.80\).  
**No independent support** for the SNe shape.

### 4d. What would count as real downstream consilience?

Something **not** fixed by the same \(X\): e.g. independent mass/radius of the filled cosmos, local weak-field recovery that does not re-use SNe, multi-observer atlas, dynamics. **None of those are paid by this fit.**

---

## 5. How the cascade stands after this tile

| # | Item | After this fit |
|---|------|----------------|
| C0–C1 | Hyperbolic form + low-\(z\) series | still form-true |
| C2 | Relational | structural (untouched) |
| C3–C4 | \(X=2GM/c^2\), closure identity | still theory under J1 |
| **C5 numeric** | SNe under n=2 hyp \(d_L\) | **FAIL** (systematic high-\(z\) over-distance) |
| Scale pin | one ruler | **done as calibration**, shape poor |
| Mechanism patch | forbidden | **not applied** |

**Standing rule (postulate doc):** if consilience stalls → revisit postulate or join, **do not invent mechanisms**.

**Solver-first note (not mechanism):** mismatch is **shape of the kinematic \(d_L(z)\)**, not a missing free param we should add. Options to ponder (not run without Charles):  
1. Is J1 (\(r\equiv x\)) the wrong join?  
2. Is the hyperbolic map the wrong composition law on areal \(r\)?  
3. Is static SSS the wrong regime for the SNe sky?  
4. Is n=2 + this \(D_A=x(\phi)\) the wrong operational chart for luminosity?  
All are **frame/join** questions — not “add dark fluid / fit \(w\)”.

---

## 6. Verifier note

- Contract pre-registered in script docstring + this §0.  
- No retune of shape after residual.  
- Diagonal understates χ²; full STAT+SYS paid: hyp **2.17**, LCDM-ref **0.88**, Δχ²≈**+2031**.  
- Residual trend unchanged under full cov.  
- Re-run: `python3 simple_metric_pantheon_xmax_fit_fullcov.py` (or diagonal script).

---

## 7. One-line

**Full cov confirms: one Pantheon fit of \(x_{\max}\) sets a scale (~3.6 Gpc at conventional \(M_B\)) but the hyperbolic n=2 shape fails hard (χ²/dof≈2.17 vs ~0.88 LCDM-ref, high-\(z\) residual); mass lock only renames that scale — consilience does not continue on SNe shape.**
