# CONTRACT — Does a finite-core continuum solution develop a `φ→∞` edge at finite chart radius?

**Date:** 2026-07-08 · Pre-registered before compute.  
**Frame:** `macro_xmax_limit_FRAME.md` · `macro_edge_closure_MAP.md` (E2 + E1 hybrid lean).  
**No G/P labels** (`macro_no_GP_framing.md`). No SNe / 1101 / cosine targets.

---

## 1. Edge definition (this probe)

**Primary (E-def A) — chart-finite dilation edge:**

> There exists finite coordinate radius `r_* < ∞` such that `φ(r) → +∞` as `r → r_*^−`.

**Secondary diagnostics (report, do not require all):**

| ID | Meaning |
|----|---------|
| E-def B | Integrator stops with `φ` large (`φ > φ_cut`, e.g. 5–20) while `r` still moderate — **candidate** edge, not proof of true asymptote |
| E-def C | `D_A` stays positive/finite as `φ` runs large (edge ≠ collapse of area to 0) |
| E-def D | Proper radial element `dl = e^φ dr` suggests large accumulated proper distance as `φ` grows (horizon-like unreachable) — qualitative only |
| E-def E | Crude mass proxy `M_proxy = ∫ 4π D_A² μ_eff e^{…} dr` (stand-in) and compare `r_*` or `D_A(r_*)` to `G M / c²` in geometric units `G=c=1` → `M` |

**Units:** `G = c = 1` for the probe (lengths = masses). Tag: FREE convention for numerics.

---

## 2. Equations (clean-core continuum, action-consistent)

Reduced radial L (angles stripped; uncompensated `𝒦` treatment CHOSE for this probe):

```
L = (Z/2) D_A² (φ')² − 2 e^{−2φ} (D_A')² − D_A² μ(r) e^{α φ}
```

Euler–Lagrange (as in continuation):

```
π = Z D_A² φ'
π' = 4 e^{−2φ} (D_A')² − α D_A² μ e^{α φ}
D_A'' = 2 φ' D_A' − e^{2φ}(Z/4) D_A (φ')² + e^{2φ}(1/2) D_A μ e^{α φ}
```

```
μ(r) = μ0 exp(−(r/r_c)²)     # FREE continuum stand-in
```

| Lever | Values | Tag |
|-------|--------|-----|
| Z | 1 | FREE convention |
| α | {−1, −0.5, 0, +0.5} | FREE (include 0 and mild +) |
| μ0 | scan | FREE |
| r_c | {0.5, 1, 2} | FREE |
| D_c | {0.5, 1, 2} | FREE finite core |
| Start | D=D_c, D'=0, φ=0, π=0 | finite-core regularity |
| Box | r_max up to 50; stop if φ>φ_cut or non-finite | FREE |

**Also run:** prior **σ-jet** point-center family as control (known open, Δφ saturates) — expect **no** E-def A.

---

## 3. Pre-named outcomes

| ID | Meaning |
|----|---------|
| X0 | No run reaches large φ (all saturate or die mild) |
| X1 | Some runs hit φ_cut at finite r with D_A>0 (**candidate** edge) |
| X2 | True-looking blowup: φ grows without bound as r approaches finite r_* (step-size collapse + φ↗) |
| X3 | Failure is D→0 collapse, not φ→∞ edge |
| X4 | Mass-proxy vs scale: any rough `r_*/M` clustering near O(1)–O(10) (characterize only) |
| X5 | Only σ-jet / only action-core / both / neither show candidates |

---

## 4. Honesty limits

- Hitting `φ_cut` is **not** a theorem of `φ→∞`. Label **candidate**.  
- `μ(r)` is FREE stand-in, not final native matter.  
- Uncompensated `𝒦` is CHOSE for probe, not a branch badge.  
- No claim of unique `x_max` from `c,G` alone without M.

## Outputs

`macro_edge_phi_inf_probe.py` · `macro_edge_phi_inf_results.md`
