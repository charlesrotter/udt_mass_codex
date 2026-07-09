# RESULT — Outward integrate from α&lt;0 regular center jet (clean-core macro)

**Date:** 2026-07-08 · **Status: PROVISIONAL (driver observe; blind verifier not run).**  
**Contract:** `macro_alpha_jet_outward_CONTRACT.md`  
**Script:** `macro_alpha_jet_outward.py`  
**Framing:** `macro_no_GP_framing.md` — **no Branch G/P labels.**  
**Parents:** `macro_phi_blindness_reaudit.md` · first-observe (α=0 control).

---

## 0. Question

After reopening direct matter–φ weight α (not forced φ-blind) and dropping G/P macro labels:  

> Can we start at a **regular geometric center** and integrate a free-`D_A`, geometry-coupled φ system **outward** with finite fields and nontrivial redshift?

Characterize only. No SNe, cosine, or 1101.

---

## 1. Premise ledger (this run)

| Item | Tag |
|------|-----|
| Metric form; free round `D_A` | as prior clean-core |
| Uncompensated `𝒦` in reduced radial L (geometry couples to φ) | **CHOSE for this probe** (not a “branch”) |
| Direct weight α ∈ {−2, −1, −0.5} | **FREE** (Thread B; not derived) |
| `σ(r)=σ0 e^{−(r/r_c)²}`, `σ0=−4/α` | **FREE stand-in** + leading jet pin |
| `ρ_eff=0` primary in EL_`D_A` | **FREE** (geometry EL without extra bulk ρ) |
| `Z=1` | FREE convention |
| Center series / `p_2` formula | from re-audit CAS |
| `c_3 ∈ {0, ±0.05}`, `r_c ∈ {0.5,1,2}` | FREE scan |
| Box `r∈[10^{-3},8]` | FREE anti-hang box |
| SNe / cosine / 1101 | **OUT** |

---

## 2. Equations used

```
π = Z D_A² φ'
π' = 4 e^{−2φ} (D_A')² + α e^{αφ} σ(r)
D_A'' = 2 φ' D_A' − e^{2φ}(Z/4) D_A (φ')²     # ρ_eff=0 primary
```

IC at `ε=10^{-3}` from regular jet (`D_A∼r`, `φ∼p_2 r^2`, `φ'(ε)=O(ε)`).

---

## 3. Outcomes (pre-registered classes)

| ID | Result |
|----|--------|
| **J0** α=0 control | Still singular at center (`φ'∼4/(Z r)`) — unchanged |
| **J1** regular start α&lt;0 | **YES** — all constructed ICs have `φ'(ε) ∼ 10^{-4}–10^{-3}` (not `∼1/ε`) |
| **J2** reach `r_max=8` finite | **YES — 27/27 primary runs** (plus 2 exploratory `ρ_eff=σ`) |
| **J3** `D_A` shape | **Monotone growth** in-box; `D_end ∼ 80–100` (primary); **no local turnover** in box |
| **J4** `Δφ` | **Nontrivial on every OK run:** about **+1.88 to +2.13** (primary); mild dependence on `(α,r_c,c_3)` |
| **J5** natural edge in-box | **Not seen** (no blowup of fields; no `D` turnover; integration hits box end cleanly) |
| **J6** stiff fail | **0** primary fails |

EOM residual on `π'` (primary): median typically **∼10^{-6}`**, max ∼ few×10^{-2} (gradient noise / ends) — integrator consistent.

---

## 4. Representative trajectories (primary, `ρ_eff=0`)

| α | r_c | c_3 | D_end | Δφ | \|φ'\|max |
|---|-----|-----|-------|-----|-----------|
| −1 | 1 | 0 | 91.5 | +2.018 | 9.4 |
| −2 | 1 | 0 | 87.8 | +2.099 | 19.8 |
| −0.5 | 1 | 0 | 92.3 | +1.958 | 5.9 |
| −1 | 2 | 0 | 86.7 | +1.972 | 5.9 |

**Pattern (observe, not target):** over this FREE grid, **Δφ clusters near ∼2** on a fixed coordinate box to r=8. That is a **scoped numerical observation** (box + stand-in `σ` + `σ0=−4/α` pin), **not** a derived universal depth and **not** 1101.

---

## 5. Cross-check `ρ_eff=σ` (exploratory only)

Tagging `ρ_eff=σ` in EL_`D_A` is **not derived** (σ was introduced as a φ-equation stand-in). Runs still “succeed” but `D` explodes (`∼10^4–10^5`) and residuals degrade — **do not bank** as physical. Primary conclusions use **`ρ_eff=0`**.

---

## 6. What this means (scoped)

**Unstuck relative to α=0 first observe:**

1. Regular **point center** + **finite φ** at the origin is achievable once α&lt;0 and the leading direct source cancels the geometric piece.  
2. The ODE system **extends** through a finite box with **nontrivial redshift** and growing areal radius.  
3. No G/P menu was used — only uncompensated `𝒦` + free `D_A` + FREE α + FREE `σ`.

**Still not a finished macro cosmology:**

1. `σ(r)` is a **stand-in**, not native `L_m`.  
2. α unfixed (FREE).  
3. No edge / closure / turnover of `D_A` in the box — looks **open/growing**, not a closed cell.  
4. Δφ∼2 on this box is **not** a depth prediction.  
5. No n=2 SNe comparison (correctly out of scope).  
6. Blind verifier not run → **PROVISIONAL**.

---

## 7. Whole-before-slice

This is **one probe**: static, spherical, round free `D_A`, uncompensated `𝒦`, Gaussian direct source with jet pin `σ0=−4/α`, `ρ_eff=0`, finite box.  
It does **not** claim “the universe solution.” It claims: **the α=0 center wall is not the end of the clean-core path; α&lt;0 jets integrate.**

---

## 8. Natural next (for Charles)

1. **Native `L_m`** that produces both geometry stress and a direct α-weight (retire prescribed `σ`).  
2. Larger box / continuation — any late turnover or edge?  
3. **Closure scan** on a better matter sector (amount as prediction, not SNe fit).  
4. Blind CAS re-check of jet + residual on saved trajectories.  
5. Optional: compensated **vacuum reference** only as limit comparison (still no G/P name).

---

## 9. One-line summary

**α&lt;0 regular-center jets integrate cleanly to r=8 with Δφ∼2 and growing D_A (27/27); α=0 center wall bypassed in this stand-in probe — macro path open, cosmology not finished.**
