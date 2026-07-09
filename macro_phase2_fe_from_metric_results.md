# PHASE 2 — Field equations from the metric (clean restart)

**Date:** 2026-07-08 · **Status: PROVISIONAL restart record** (CAS driver; independent blind verifier not re-run on free-`D_A` EH claim).  
**Parent:** `macro_clean_restart_from_metric_MAP.md` · Phase 1: `macro_phase1_metric_only.md`  
**Script:** `macro_phase2_fe_from_metric.py`  
**Rule:** no continuum μ/α, no G/P names, no edge solves, no particle package.

---

## 0. Goal of this phase

From the **metric family only**, re-establish what bulk structure is **forced** vs **open**, with free transverse radius `D_A(r)`.

---

## 1. Metric family under study (from Phase 1)

**FREE ansatz for this CAS (tagged):** static, spherical, diagonal.

```text
ds² = −e^{−2φ(r)} c² dt² + e^{2φ(r)} dr² + D_A(r)² dΩ²
```

Longitudinal block = metric postulates (R1–R3 + sides).  
`D_A(r)` = **not** set to `r` (transverse sector open per Phase 1 / CANON).

---

## 2. FORCED or re-verified (CAS)

### 2.1 Measure is φ-free

```text
√(−g) = c |D_A|² |sin θ|   (with D_A>0, sinθ>0: c D_A² sinθ)
```

Independent of φ — reciprocal cancellation. (Sympy prints `sqrt(D_A⁴)` / `Abs(sin)`; same on the physical domain.)

### 2.2 Ricci scalar (free `D_A`)

```text
R = 2 e^{−2φ}/D_A² · (
      −2 D_A² (φ')² + D_A² φ'' + 4 D_A D_A' φ'
      − 2 D_A D_A'' + e^{2φ} − (D_A')²
    )
```

**Check:** `D_A → r` recovers the founding formula for R — **TRUE**.

### 2.3 Einstein–Hilbert: frozen areal radius vs free `D_A`  ⚠

| Setting | `∫ D_A² R` (radial density) | Bulk content? |
|---------|----------------------------|---------------|
| **`D_A = r` fixed** (areal gauge) | `r² R = d(…)/dr` exact | **Empty bulk** for φ (founding identity; EL_φ ≡ 0) — **TRUE** |
| **`D_A(r)` free** (varied) | EL_φ and EL_`D_A` **not** identically 0 | **Nonempty bulk** |

CAS:

```text
EL_φ[D_A² R] = 4 D_A e^{−2φ} D_A''     (not ≡ 0)
EL_D[D_A² R] = 4 e^{−2φ}(−2 D_A (φ')² + D_A φ'' + 2 D_A' φ' − D_A'')   (not ≡ 0)
```

**Restart implication (load-bearing):**

> The slogan “EH is pure boundary on the UDT reciprocal family” is **true in areal gauge with `D_A` not varied** (the founding setting).  
> It is **not** automatically true when **`D_A` is an independent dynamical field**.

So Phase 2 must **not** copy “EH empty ⇒ bulk must be pure φ-kinetic” into the free-`D_A` variational problem without re-deriving. Two clean options (both legal if tagged):

| Path | Meaning |
|------|---------|
| **Areal gauge** | Fix `D_A = r` (or gauge-fix areal radius); EH bulk empty; dynamics from other terms |
| **Free `D_A`** | EH can contribute bulk EL; full story includes that content **or** an explicit reason to omit EH |

**Neither path is chosen here** — only exposed. Prior macro continuum probes used free `D_A` **without** EH bulk; that was a **CHOSE truncation**, not forced by “EH empty.”

### 2.4 R1-weighted kinetic density

```text
√(−g) · e^{2φ} g^{rr} (φ')² = √(−g) (φ')²
```

φ-free density (only φ') — probe and self-consistent variation coincide for this weight.

**Vacuum from kinetic only** (reduced `L = (Z/2) D_A² (φ')²`):

```text
EL_φ:  d/dr(Z D_A² φ') = 0  ⇒  Z D_A² φ' = q
EL_D:  −Z D_A (φ')² = 0
```

On shell with free `D_A`: EL_D ⇒ **`q = 0` or singular `D_A`**.  
So **pure kinetic + free dynamical `D_A` does not give a redshifting regular vacuum.**  
Either freeze/gauge `D_A`, or add geometric (or other) terms that support free `D_A`.

### 2.5 Geometric tensors (definitions only — not dynamics)

For round free `D_A`, extrinsic combination:

```text
𝒦 := K_AB K^{AB} − K² = −2 e^{−2φ} (D_A'/D_A)²
D_A² 𝒦 = −2 e^{−2φ} (D_A')²
D_A² e^{2φ} 𝒦 = −2 (D_A')²     # compensated density
```

These are **identities** given the metric split. They do **not** by themselves say whether `𝒦` or `e^{2φ}𝒦` appears in the action.

---

## 3. Illustrative Lagrangians (NOT the theory — catalog only)

Shown so EL structure is visible; **not** adopted as Phase 2 output theory.

| Label | Reduced L | Role |
|-------|-----------|------|
| (A) | `(Z/2)D_A²(φ')² − 2(D_A')²` | kinetic + compensated-`𝒦` density |
| (B) | `(Z/2)D_A²(φ')² − 2 e^{−2φ}(D_A')²` | kinetic + raw-`𝒦` density |

(A) recovers the known vacuum free-`D_A` system used in n=2 vacuum work:  
`Z D_A² φ' = q`, `D_A'' = −q²/(4 Z D_A³)`.  
(B) recovers the geometry-coupled φ EL used in later continuum probes.

**Tag both: CHOSE geometric completion candidates — not forced in this phase.**

---

## 4. FREE ledger after Phase 2 (empty of smuggled pins)

| # | Item | Status after Phase 2 |
|---|------|----------------------|
| F1 | Static / spherical / diagonal | **FREE ansatz** (used in CAS) |
| F2 | `D_A` free vs areal gauge `D_A=r` | **OPEN fork** — changes EH status |
| F3 | Include EH bulk when `D_A` free? | **OPEN** — CAS shows bulk ≠ 0 if included and varied |
| F4 | φ kinetic weight `Z` | **FREE** normalization |
| F5 | Kinetic φ term present? | **Strongly motivated by R1**; still a construction step, not metric-only |
| F6 | Geometric completion: none / (A) / (B) / EH / mix | **OPEN** — not derived uniquely here |
| F7 | Matter sector | **OPEN — empty** (no stand-in) |
| F8 | Direct φ–matter weight α | **OPEN — not introduced** |
| F9 | Edge / `x_max` | **OUT of Phase 2** |
| F10 | Constants `c` (in metric), `G` (not in metric form) | `c` in `g_tt`; `G` appears only when gravity coupling/matter scale enters |

---

## 5. What Phase 2 does **not** claim

- A unique native action for the universe  
- That (A) or (B) is correct  
- That vacuum cosmology works  
- That `x_max` exists  
- That prior continuum IVP null is a theorem about UDT (only about that stack)

---

## 6. Honest bridge to prior “AI cruft”

| Prior habit | Clean status |
|-------------|--------------|
| “EH empty ⇒ only kinetic + 𝒦” | Only safe under **areal freeze** of `D_A`; free `D_A` reopens EH |
| Free `D_A` + (A) or (B) without EH | **CHOSE** truncation |
| Continuum μ, α, cores, σ-jet | Still **parked** |
| G/P | Still **not used** |

---

## 7. Natural Phase 3 (gated — not run)

Only after Charles leans on the fork **F2/F3/F6**:

1. **Path areal:** set `D_A=r` (gauge), EH empty, re-derive bulk from R1 kinetic + whatever transverse terms are forced with that gauge.  
2. **Path free `D_A`:** either include EH variation or justify omission; then complete geometric sector.  
3. Matter only when a native sector is derived or explicitly pinned.  
4. Then solutions / edge.

**Do not** resume μ-grids until F2–F6 are pinned or cleanly explored as labeled forks.

---

## 8. One-line summary

**Metric restart: measure φ-free and R1 kinetic clean; EH is empty for frozen areal `D_A=r` but has bulk content if `D_A` is free and varied — so free-`D_A` dynamics are not forced to be “kinetic + 𝒦 only,” and the FREE ledger for geometric completion is open again.**
