# OBSERVE — Sourced φ on simple metric under true n=2


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric compensated dust |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | LCDM ref only |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **LEAD** |
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

**Date:** 2026-07-09 · **Mode: OBSERVE**  
**Script:** `simple_metric_sourced_profile_observe.py`  
**JSON:** `simple_metric_sourced_profile_observe_out.json`  
**Upstream:** #1 profile/source (`simple_metric_root_upstream_MAP.md`)  
**Status:** PROVISIONAL — probe matter, not fundamental continuum.

---

## 0. Held fixed

| Item | Choice |
|------|--------|
| Metric | simple, \(D_A=r\) |
| Optics | \(1+z=e^{\phi}\), \(d_L=r(1+z)^2\) |
| Operator | compensated \(W=e^{2\phi}\) + dilated dust \(L_m=-\rho r^2 e^{-2\phi}\) |
| EL | \((r^2\phi')'=(2/Z)\rho r^2 e^{-2\phi}\), \(Z=1\) units |
| \(\rho\) | FREE gauss/tophat amount×width — **probe** |
| Not | free \(D_A\), SNe-tuned cubic, claim dust = UDT matter |

Also: MS uniform ball as geometric reference (\(A=1-2m/r\)).  
Comparisons: hyp J1 n=2, locked cubic n=1/n=2, LCDM ref.

---

## 1. What emerged (compensated + dilated dust)

**Scan:** 96 profiles (gauss/tophat × 3 widths × 16 amounts).

| Quantity | Range / count |
|----------|----------------|
| \(\phi_{\max}\) | 0.01 → 4.8 |
| \(z_{\max}=e^{\phi_{\max}}-1\) | 0.01 → ~119 |
| Reach \(z\ge 2\) | **54 / 96** |

So the probe **can** produce large redshift. That is not the failure mode.

### SNe shape demo (full cov, 1 offset only; not a fit campaign)

Among probes that cover full Pantheon \(z\):

| | χ²/dof | RMS |
|--|-------:|----:|
| **Best dust probe** | **~10.1** | **0.67** |
| Worst in that set | ~16.0 | 0.95 |
| hyp J1 n=2 | 2.17 | 0.31 |
| cubic n=2 | 4.56 | 0.47 |
| cubic n=1 (old) | 0.94 | 0.16 |
| LCDM Ωₘ=0.3 | 0.88 | 0.15 |

**Reading:** free amount/width of this dust does **not** approach a sky-like \(d_L(z)\). Best residual still catastrophic vs data and vs hyp/cubic.

---

## 2. Structural finding (load-bearing)

Compensated dust is **regular at the origin**:

\[
\phi(r) = a r^2 + O(r^4), \qquad a=\frac{\rho(0)}{3Z}.
\]

Low \(z\):

\[
1+z=e^{\phi}\approx 1+a r^2 \quad\Rightarrow\quad r\sim\sqrt{z/a}.
\]

True optics:

\[
d_L=r(1+z)^2 \sim \sqrt{z}\quad\text{as }z\to 0.
\]

**That is the wrong low-\(z\) distance law.** Observations need \(d_L\sim z\) (linear Hubble).

| Leading \(\phi\) | Low-\(z\) \(r(z)\) | \(d_L=r(1+z)^2\) |
|------------------|-------------------|------------------|
| \(\phi\sim a r^2\) (regular, this probe) | \(r\sim\sqrt{z}\) | \(\sim\sqrt{z}\) **FAIL** |
| \(\phi\sim k r\) (locked cubic; irregular at 0) | \(r\sim z/k\) | \(\sim z\) **OK linear** |
| hyp \(x=X\tanh\phi\), \(r=x\), \(\phi\sim x/X\) | \(r\sim X z\) | \(\sim X z\) **OK linear** |

**Upstream implication:** under \(D_A=r\) and n=2, **regular-origin compensated kinetics conflict with linear low-\(z\) \(d_L\)** unless something else supplies a **linear** \(\phi\sim kr\) piece (which reopens origin regularity / operator fork / chart).

Uncompensated vacuum \((r^2\phi')'=(4/Z)e^{-2\phi}\) is **worse** at the origin (RHS finite ⇒ \(\phi'\sim 1/r\) blowup) — not a regular rescue.

---

## 3. MS uniform ball (geometric reference)

Compactness \(C=2M/R\) alone sets \(\phi_{\max}\) (scale-free interior).

| \(C\) | \(\phi_{\max}\) | \(z_{\max}\) (approx) |
|------:|----------------:|----------------------:|
| 0.10 | 0.05 | 0.05 |
| 0.50 | 0.35 | 0.41 |
| 0.80 | 0.80 | 1.23 |
| 0.95 | 1.48 | 3.37 |

High \(z\) only near trapping. Exterior is Schwarzschild (local hole), not a filled relational cosmos. **Not** a SNe background candidate as-is; confirms high redshift needs strong compactness or extended source.

---

## 4. J1 thin stress (parallel)

| Item | Status |
|------|--------|
| Geometric \(D_A=r\) at chart origin | forced |
| Hyp \(x=X\tanh\phi\) | compositional |
| **J1** \(r\equiv x\) | still **CHOSE** |
| This observe | used \(D_A=r\) only; did not assume hyp |

If hyp is kept without J1, need **derived** \(r(x)\) — not free \(D_A(r)\). Regular-origin issue is **independent** of J1: it hits any model with \(\phi\sim ar^2\) and \(d_L=r(1+z)^2\).

---

## 5. How this moves the upstream map

| Suspect | After this tile |
|---------|-----------------|
| #1 Profile/source | **Sharpened:** naive compensated dilated dust is the **wrong low-\(z\) class**; high-\(z\) reachable ≠ good shape |
| Optics / \(D_A=r\) | Unchanged |
| Old cubic linear term | Now read as **why** it got linear Hubble (at cost of irregular origin) — clue, not revival |
| Hyp low-\(z\) | Linear OK; high-\(z\) shape still fails (prior) |
| Next profile work | Need either (i) operator/BC that allows \(\phi\sim kr\) **honestly**, or (ii) different length in \(d_L\) only if geometry forces it (not shown), or (iii) non-probe matter sector from metric |

**Solver-first:** mismatch is **structural asymptotics** of this operator+regularity package, not “need more free ρ knobs.” Scanning ρ harder will not fix \(d_L\sim\sqrt{z}\).

---

## 6. Premise ledger

| Item | Tag |
|------|-----|
| Compensated + dilated dust EL | THEORY form from simple-metric ledger; dust **probe** |
| \(\rho\) gauss/tophat | FREE |
| \(Z=1\) | CHOSE units |
| MS \(A=1-2m/r\) | Geometric / GR-form reference on this metric |
| SNe χ² | DEMO residual only |

---

## 7. One-line

**On the simple metric with true n=2, compensated dilated dust can make large \(z\) but forces \(\phi\sim ar^2\) ⇒ \(d_L\sim\sqrt{z}\) at low \(z\) — structurally wrong; free ρ scans cannot fix that. Linear Hubble needs a linear \(\phi\sim kr\) sector (as the old cubic smuggled via irregular origin) or a different native join still to be derived.**
