## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (hard solution space) |
| **Frame** | residual spine; two rooms; angular Einstein \(A=H+G\) |
| **Slice** | (1) deformed wall under \(A=H(r)+G(\theta)\); (2) local-room residual eigenmodes |
| **Observing or targeting?** | OBSERVE — not BAO |
| **Build-on grade** | **LEAD** (robust discrete local spectrum; deformed wall) |
| **Re-run** | `simple_metric_continue_hard_out.json` / scripts below |

### Premise ledger

| Item | Tag |
|------|-----|
| \(G^r{}_\theta=0\Rightarrow A=H+G\) | DERIVED (prior hard explore) |
| L radial \(H=1-r/X\) | WORKING |
| Local quartic interiors | free-and-explored C1 family |
| Probe wave operator on fixed \(A(r)\) | first-cut |
| Dirichlet at surface / origin | CHOSE wall-quiet proxy |

---

# Interesting results: deformed wall + local residual cavity

## 1. Angular residual deforms the cosmos wall

Under Einstein mixed constraint, residual is \(A=H(r)+G(\theta)\).

With L-radial piece \(H=1-r/X\) and sky piece \(G(\theta)\):

\[
A=0 \quad\Rightarrow\quad \frac{r_{\mathrm{wall}}(\theta)}{X}=1+G(\theta).
\]

**Example:** \(G=0.1\,P_2(\cos\theta)\)  
\(r_{\mathrm{wall}}/X\) runs **0.95 → 1.10** (15% peak-to-peak), not a round sphere.

**News:** Angular residual is not only multipole ripples inside a round wall — it **reshapes residual death**.  
Native, no free “wall deformation parameter” beyond \(G(\theta)\).

(Positivity: \(|G|\) cannot be too large or \(A\) goes negative inside.)

---

## 2. Local residual interiors: **robust discrete spectrum**

Probe wave operator on quartic C1 star interiors (finite \(A(R)>0\)).

### Convergence (unlike filled L wall)

ℓ=1, α=1, R=1:

| N | \(\omega_1\) | \(\omega_2\) | \(\omega_3\) |
|--:|-------------:|-------------:|-------------:|
| 200 | 3.25977 | 5.75404 | 8.18885 |
| 400 | 3.25978 | 5.75422 | 8.18946 |
| 800 | 3.25978 | 5.75426 | 8.18962 |

Relative change N=400→800 \(\sim 10^{-5}\) — **converged**.

Filled L wall control still **densifies** as eps→0 (optical throat).

### Finite-cavity quantization

Overtones: \(\Delta\omega\cdot L_{\mathrm{opt}}\to\pi\) (gaps × optical length → π).

| α (compactness \(C=0.4\alpha\)) | \(L_{\mathrm{opt}}\) | \(\omega_1\) | \(\omega_1 L_{\mathrm{opt}}\) |
|--:|--:|--:|--:|
| 0.3 | 1.07 | 4.15 | 4.44 |
| 1.0 | 1.32 | 3.26 | 4.30 |
| 1.8 | 2.07 | 1.98 | 4.09 |

Not exactly \(\pi\) for the **fundamental** (geometry weights, angular barrier), but **overtone spacing is optical-cavity-like** (\(\Delta\omega\sim\pi/L_{\mathrm{opt}}\)).

**News:** Local residual stars support a **stable discrete residual ringing spectrum** set by interior optical size — native, no fluid, no cutoff fakery.

---

## 3. The split the metric insists on

| Room | SNe / mass-lock role | Wave role |
|------|----------------------|-----------|
| **Filled L** | Strong (one \(X\), near SNe) | Infinite optical wall — **no** robust finite drum |
| **Local residual interior** | Local gravity room | **Finite optical cavity** — robust \(\omega_n\) |

So “explore angular/time for BAO-like patterns on filled L” was always fighting the optical throat.  
**Discrete residual tones live in the local room** (or require a different derived wall law).

---

## One-line

**Angular residual deforms the outer wall via \(A=H+G\); local residual interiors host converged discrete ringing with \(\Delta\omega\sim\pi/L_{\mathrm{opt}}\); filled L remains a distance/mass room, not a finite residual drum.**
