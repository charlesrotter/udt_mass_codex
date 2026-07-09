# PATH B (companion) — free `D_A` vacuum with EH + R1 kinetic

**Date:** 2026-07-08 · **Status: PROVISIONAL CAS sketch** (no blind verifier; no matter).  
**Parent decision:** Path A is the clean baseline (`macro_phase3_pathA_areal_results.md`).  
**This file:** honesty pass on free transverse radius with **EH included**.  
**Script:** `macro_phase3_pathB_freeDA_EH.py`

---

## 0. Action (vacuum only)

Static spherical FREE ansatz. Reduced radial density (constants stripped):

```text
L = D_A² R[φ, D_A] + (Z/2) D_A² (φ')²
```

No continuum matter. No 𝒦 add-ons. No G/P.

---

## 1. EL system (CAS)

```text
EL_φ = −Z D_A² φ'' − 2 Z D_A D_A' φ' + 4 D_A e^{−2φ} D_A''
EL_D = e^{−2φ} (
         Z D_A e^{2φ} (φ')² − 8 D_A (φ')² + 4 D_A φ''
         + 8 D_A' φ' − 4 D_A''
       )
```

(Equivalent forms in script.)

### Slices

| Slice | Content |
|-------|---------|
| **`D_A = r` (gauge)** | `EL_φ = 0` ⇔ `d/dr(Z r² φ') = 0` — **same vacuum φ equation as Path A**. `EL_D` becomes an **extra** constraint (not imposed when `D_A` is frozen). |
| **`φ = const`** | `EL_φ ∝ D_A D_A''`, `EL_D ∝ −D_A''` ⇒ **`D_A'' = 0`** ⇒ `D_A = a + b r` (linear) |
| **`D_A = a r`, `φ = const`** | EL_D holds (flat transverse scaling) |

---

## 2. Read (lay)

- Freeing `D_A` **without** EH was an incomplete story.  
- Freeing `D_A` **with** EH couples φ and `D_A` through second derivatives — a real 2-field vacuum system.  
- Restricting back to areal gauge recovers Path A’s φ equation; the price of the freeze is that **`EL_D` is not enforced**.  
- Constant-φ free-`D_A` vacuum wants **linear** `D_A` (no interesting redshifting cosmology by itself).

**No claim** yet of a regular centered redshifting solution of the full Path B system — that is a later OBSERVE with bounded methods, still without continuum μ cruft.

---

## 3. Standing stack after Path A + Path B sketch

| Floor | Status |
|-------|--------|
| Metric form | Solid (Phase 1) |
| Path A vacuum (areal, EH empty, R1 kinetic) | **Clean Coulomb vacuum** |
| Path B vacuum EL (free `D_A`, EH+kinetic) | **Written**; solutions not fully mapped |
| Matter | Still empty on purpose |
| Edge / `x_max` | Still open |

---

## 4. One-line

**Path B: free `D_A` + EH + kinetic is a coupled vacuum system; on areal gauge it reduces to Path A for φ, while pure constant-φ wants linear `D_A` — next real work is solving/characterizing this system or adding native matter, not stand-in μ grids.**
