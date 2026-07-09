# PHASE 3 — Path A chosen: areal gauge bulk (clean restart)

**Date:** 2026-07-08 · **Status: PROVISIONAL restart bulk (CAS; founding EH-empty already blind-verified historically).**  
**Decision:** driver choice after Charles “whatever you think best.”  
**Parents:** `macro_phase1_metric_only.md` · `macro_phase2_fe_from_metric_results.md` · `macro_clean_restart_from_metric_MAP.md`  
**Script:** `macro_phase3_pathA_areal.py`

---

## 0. Why Path A (not free-`D_A` first)

| Criterion | Path A (areal `D_A≡r`) | Path B (free `D_A` first) |
|-----------|------------------------|---------------------------|
| EH status | **Empty bulk — proven** | Nonempty if `D_A` varied (Phase 2) — extra fork |
| Matches founding native FE CAS | Yes | Partial / new |
| Isolates “what replaces GR bulk?” | Clean | Mixed with EH content |
| Risk of smuggled freeze | **Real** — must stay tagged FREE gauge/ansatz | Lower freeze risk |
| Speed to a clean vacuum statement | High | Lower |

**Choice:** **Path A first** — write the cleanest forced vacuum bulk under the areal chart, with freeze **loudly tagged**.  
**Not abandoned:** free `D_A` + EH (Phase 2) is the **mandatory generalization** after this floor is solid — not optional forever.

**Rationale in one line:** fix one coordinate gauge so EH emptiness is a theorem, derive the R1 vacuum, freeze nothing else (no matter stand-ins, no edge IVP, no G/P).

---

## 1. Premises (Path A)

| Item | Tag |
|------|-----|
| Metric longitudinal block from R1–R3 | THEORY (canon C-2026-06-18-1) |
| Static, spherical, diagonal | **FREE ansatz** |
| **`D_A ≡ r` (areal gauge)** | **FREE gauge / chart choice** — not metric-forced |
| Bare EH as gravitational curvature integrand | Standard GR mine; **bulk vanishes** here |
| R1-weighted kinetic for φ as vacuum bulk | **DERIVED structure** given R1 + reciprocal measure (founding); `Z` free |
| Matter | **Absent** (vacuum Path A) |
| Edge / `x_max` / continuum μ / α | **OUT** |

---

## 2. Metric (Path A)

```text
ds² = −e^{−2φ(r)} c² dt² + e^{2φ(r)} dr² + r² dΩ²
```

```text
√(−g) = c r² sinθ   (φ-free)
```

---

## 3. CAS results (this run)

| Check | Result |
|-------|--------|
| EH: `r² R = d(…)/dr` | **TRUE** (empty bulk) |
| R1 kinetic density `√(−g) e^{2φ} g^{rr} (φ')²` | `∝ r² (φ')²` — **no explicit φ** |
| Vacuum EL from `L = (Z/2) r² (φ')²` | `d/dr(Z r² φ') = 0` |
| Solution | `φ = φ_∞ − q/r` (Coulomb) |
| Unweighted kinetic `g^{rr}(φ')²` | **Explicit φ** — not R1-clean; **not adopted** |

**Vacuum metric factor:**

```text
g_tt = −c² exp(−2φ_∞ + 2q/r)
```

Not Schwarzschild as an exact rational function; agrees with weak-field mass identification `M = −q` at leading order (founding nonlinear-escape note — keep as known, not re-litigated here).

---

## 4. Path A vacuum field content (what we *do* claim)

Under Path A premises:

1. **Curvature EH does not supply bulk φ dynamics.**  
2. **Shift-invariant kinetic does:**  
   ```text
   (r² φ')' = 0     (Z absorbed into normalization of q)
   ```  
3. **General regular-at-infinity vacuum solution (static spherical):**  
   ```text
   φ(r) = φ_∞ − q/r
   ```  
4. **`q = 0` ⇒ no redshift; `q ≠ 0` ⇒ singular at r=0** (Coulomb center).  
   → A **regular center + redshift** is **not** a Path A vacuum property. That gap is real and **not** to be filled by AI continuum gadgets in this document — it is the pointer to matter and/or free-`D_A`/EH generalization and/or different global structure.

---

## 5. FREE ledger after Path A

| # | Item | Status |
|---|------|--------|
| A1 | Areal gauge `D_A=r` | **FREE** (Path A pin for this floor) |
| A2 | Static spherical diagonal | **FREE ansatz** |
| A3 | `Z` | **FREE** norm (set 1 wlog for vacuum EL form) |
| A4 | `q`, `φ_∞` | Integration constants / gauge |
| A5 | Matter | **OPEN** — next physics after vacuum floor |
| A6 | Free `D_A` + EH bulk | **OPEN** — Path B generalization (Phase 2 CAS ready) |
| A7 | Geometric extras with areal freeze (transverse terms beyond kinetic) | **OPEN** if something beyond vacuum kinetic is forced — not introduced here |
| A8 | Edge / `x_max` | **OPEN** solution question — not in vacuum Coulomb |

---

## 6. What we deliberately did **not** do

- Continuum `μ`, α, finite cores, σ-jets  
- G/P labeling  
- SNe / 1101  
- Claiming vacuum cosmology is viable  
- Claiming `x_max` from vacuum  

---

## 7. How this corrects the cruft stack

| Old habit | Path A status |
|-----------|----------------|
| Free `D_A` + only kinetic+𝒦 without EH | **Invalid as “forced”** — either freeze areal (here) or include EH (Path B) |
| Continuum stand-ins to “fix vacuum” | Parked; vacuum gap stated honestly |
| IVP edge hunt | Not run; wrong stage |

---

## 8. Recommended next (ordered)

1. **Charles checkpoint:** accept Path A vacuum floor as the clean restart baseline?  
2. **Matter (minimal native):** only after a native matter sector is derived or pinned — not Gaussian μ.  
3. **Path B:** free `D_A` with **EH included** in the variation (Phase 2), vacuum EL — does regular redshifting structure appear without stand-in matter?  
4. **Edge / `x_max`:** only after (2) or (3) produces a candidate global class; prefer BVP/matching over hope-IVP.

**Driver default if continuing without further lean:** do **Path B vacuum (free `D_A` + EH + R1 kinetic only)** next — one CAS+EL writeup, still no continuum μ — because Path A already closed the empty-EH vacuum story and the next integrity issue is free transverse geometry.

---

## 9. One-line summary

**Path A: in areal gauge EH is empty and R1 kinetic forces Coulomb vacuum `φ=φ_∞−q/r` — clean floor; regular redshifting cosmologies are not vacuum Path A; free `D_A`+EH and native matter remain open, not filled with stand-ins.**
