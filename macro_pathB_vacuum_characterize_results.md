# RESULT — Path B vacuum characterization (free `D_A` + EH + R1 kinetic)

**Date:** 2026-07-08 · **Status: PROVISIONAL** (driver CAS + numeric; no blind verifier).  
**Lean executed:** characterize Path B vacuum **before** native matter.  
**Parents:** `macro_phase3_pathA_areal_results.md` · `macro_phase3_pathB_freeDA_EH_results.md`  
**Script:** `macro_pathB_vacuum_characterize.py`  
**No matter stand-ins · no G/P · no SNe.**

---

## 0. System

Vacuum only, static spherical FREE ansatz:

```text
L = D_A² R[φ, D_A] + (Z/2) D_A² (φ')²
```

(EH bulk kept because `D_A` is varied; R1 kinetic included.)

---

## 1. CAS structure

### 1.1 EL identity

```text
EL_φ + d/dr(Z D_A² φ') − 4 D_A e^{−2φ} D_A'' = 0
```

So φ’s flux is sourced by **`D_A''`** (through EH), not by an external matter density.

### 1.2 Special solutions

| Sol | Content | EL_φ | EL_D |
|-----|---------|------|------|
| **S0** | `φ=const`, `D_A=const` | OK | OK |
| **S2** | `φ=const`, `D_A=a+br` (`D_A''=0`) | OK | OK |
| **S1 Path A** | `D_A=r`, `φ=c₀−q/r` | **OK** | **NOT OK** unless `q=0` |

**Load-bearing:**

```text
EL_D[S1] ∝ q² (Z e^{2c₀} − 8 e^{2q/r}) e^{−2c₀} / r³
```

**Path A Coulomb vacuum is a solution of Path A (areal freeze, do not vary `D_A`).**  
It is **not** generally a solution of Path B (free `D_A` + EH).  
Only the **non-redshifting** case `q=0` sits in both.

That resolves a potential confusion: free transverse geometry is not a harmless upgrade of Path A Coulomb — it **kills** Coulomb as an on-shell free-`D_A` solution.

---

## 2. Numeric observe (bounded IVP)

First-order form for `(D_A, D_A', φ, φ')` from the linear solve of `(D_A'', φ'')` in the two ELs.  
`Z=1`. Characterize, do not target cosmology.

### 2.1 Catalog

| Seed class | Behavior |
|------------|----------|
| Flat core `D=D_c`, `D'=0`, `φ=0`, `φ'=0` | **Exact rest** — no redshift, no expansion |
| Linear `D=a+br`, `φ=0`, `φ'=0` | **Stays** in S2 — geometry can grow, **φ stays 0** |
| Pure `D'` kick, `φ'=0` | `D` grows, **φ stays 0** |
| Pure `φ'` kick on flat core | **Nontrivial Δφ** + `D` growth — main interesting family |
| Path A Coulomb seed integrated with free-`D_A` RHS | Runs but **off Path B shell** for `q≠0` (expected); large drift in `D` |

### 2.2 Redshifting vacuum trajectories (Q-kick family)

Example: start `r=0.2`, `D=1`, `D'=0`, `φ=0`, `φ'=0.5`:

| r | D | D' | φ | φ' |
|--:|--:|---:|--:|--:|
| 0.2 | 1.00 | 0 | 0 | 0.50 |
| 1.0 | 1.43 | 0.72 | 1.04 | 1.70 |
| 2.0 | 5.84 | 7.23 | 1.90 | 0.18 |
| 4.0 | 21.5 | 8.00 | 2.00 | 0.014 |
| 8.0 | 53.5 | 8.07 | **2.02** | ~0 |

**Pattern (observe):**

- φ **rises then saturates** near **~2** (for this seed scale).  
- φ' → 0 at large r.  
- D' → roughly constant ⇒ **D grows ~ linearly** at large r (open).  
- No D-collapse in the scan.  
- Median on-shell residuals on this run: `|EL_φ|∼2×10^{-3}`, `|EL_D|∼2×10^{-5}` (max large near stiff points — integrator OK enough for characterization, not machine-precision).

Across mild Q-kicks: **Δφ ∼ 0.09–2.03** on the box; larger initial φ' → Δφ approaches a **ceiling near 2**, not a run to `φ→∞`.

### 2.3 What vacuum Path B does *not* show (this scan)

- `φ→∞` at finite chart radius  
- Closed `D` (turnover to a finite outer edge)  
- A preferred mass scale (vacuum, scale-free structure + seed scales)

---

## 3. Classification (plain)

| Class | Path B vacuum |
|-------|----------------|
| Trivial non-redshifting | Yes — large (const/linear `D`, `φ=0`) |
| Open redshifting | **Yes** — excited by initial φ' (or off-shell Path A seeds) |
| Path A Coulomb as free-`D_A` solution | **No** (`q≠0`) |
| Regular center + global edge | **Not found** in vacuum |
| Need for matter to get vacuum-like Coulomb in free `D_A`? | Coulomb isn’t free-`D_A` on-shell; matter / other terms still open |

---

## 4. Relation to Path A and to the old continuum cruft

| Statement | Status |
|-----------|--------|
| Path A Coulomb is the clean **areal-gauge** vacuum | Stands |
| Free `D_A` + EH vacuum is a **different theory sector** | Stands — not a smooth extension of Coulomb |
| Continuum μ was “needed to fix vacuum” | **Not the first issue** — free-`D_A` vacuum already has open redshifting solutions; μ was a separate (parked) story |
| Saturating Δφ~2 | Appears again **in pure vacuum Path B** — so it is not an artifact of Gaussian matter alone |

---

## 5. Whole-before-slice

Scoped to: static spherical, vacuum, EH+R1 kinetic, `Z=1`, IVP seeds, finite boxes.  
Not a global BVP survey; not uniqueness; not stability.

---

## 6. What next (after this lean item)

1. **Optional analytic:** closed form for the Q-kick family (why φ→const, D'→const).  
2. **Native matter** — only with a derived/pinned sector; ask whether it creates an **edge** or selects scale (`x_max ∼ GM/c²`), not whether redshift can exist (it already can in vacuum Path B).  
3. **BVP edge** still the right tool if Charles wants `φ→∞` at finite r — vacuum IVP does not produce it.  
4. Keep Path A as the areal-gauge reference; do not mix Coulomb into free-`D_A` claims.

---

## 7. One-line summary

**Path B vacuum: Path A Coulomb is off-shell unless `D_A` is frozen; free-`D_A`+EH vacuum still admits open redshifting solutions (φ saturates ~2, D grows) from φ' seeds — no finite-radius `φ→∞` edge in vacuum IVP.**
