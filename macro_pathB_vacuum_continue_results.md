# CONTINUE — Path B vacuum asymptotics + what matter is *for*

**Date:** 2026-07-08 · **Status: PROVISIONAL** (CAS + prior numerics).  
**Parents:** `macro_pathB_vacuum_characterize_results.md` · Path A baseline.  
**No continuum μ grids · no SNe.**

---

## 1. Analytic structure (Path B vacuum)

### 1.1 Exact non-redshifting family (S2)

```text
φ = const,   D_A = v r + w,   (D_A'' = 0)
```

Both ELs vanish. Geometry may grow (`v≠0`); **redshift is identically zero**.

### 1.2 Freeze `D_A = v r` and solve for φ

Then:

```text
EL_φ  ⇒  (r² φ')' = 0  ⇒  φ = c₀ − q/r
```

But **EL_D** on that pair is

```text
∝ q² v (Z e^{2c₀} − 8 e^{2q/r}) e^{−2c₀} / r³
```

so **Coulomb hair is off-shell** for free `D_A` unless `q=0` (same lesson as before).  
**Areal Path A is not a free-`D_A` solution.**

### 1.3 Large-r series

Ansatz:

```text
φ = φ_∞ + A/r + B/r² + ⋯,   D_A = v r + w + C/r + ⋯
```

Leading coefficients can be solved for `(B,C)` in terms of `(A,v,w,φ_∞,Z)` (script/session algebra).  
**Physical point:** pure EH + free `D_A` **breaks φ-shift symmetry** (explicit `e^{±2φ}` in EL), so **`φ_∞` is not pure gauge** — unlike pure R1 kinetic in areal gauge.

### 1.4 Match to numerics (Q-kick family)

Observed attractor-like behavior:

- `φ → φ_∞` (finite), `φ' → 0`  
- `D_A' → v` (const), `D_A ∼ v r` growing  
- **No** finite-radius `φ→∞` edge  

So Path B vacuum naturally produces **open, finite-redshift** exteriors, not an `x_max` edge by itself.

---

## 2. What vacuum Path B already does / does not do

| Need | Vacuum Path B |
|------|----------------|
| Nontrivial redshift | **Yes** (from data / seeds with φ'≠0) |
| Open exterior | **Yes** |
| Regular Coulomb mass hair on free `D_A` | **No** |
| `φ→∞` edge / `x_max` | **No** (not in IVP vacuum) |
| Selected mass scale from `c,G` only | **No** — seeds set scales |

---

## 3. What **native matter** is now *for* (refocus)

Because vacuum can already redshift, matter is **not** “the thing that creates any Δφ.”  
Under the clean restart + Charles `x_max` frame, matter is for:

1. **Scale** — supply mass `M` so lengths ~ `GM/c²` can exist with only `c,G` as constants of nature.  
2. **Edge / closure** — select global solutions with a chart-finite high-z edge or critical whole (E1/E2), if those exist.  
3. **Regular center** — if the physical middle is not a vacuum seed.  
4. **Later: particles** — localized lumps on the background.

**Parked again:** Gaussian μ / α stand-ins used as if they were the field equations.

### Minimal next matter program (MAP only — not run here)

| Step | Content |
|------|---------|
| M0 | Choose Path A (areal) vs Path B (free `D_A`+EH) as the **gravity side** for matter coupling — do not mix silently |
| M1 | Matter must come from a **native sector** (geometric defect, or derived continuum limit) — empty ledger until derived/pinned |
| M2 | First question for matter: **does any native source create an edge or select M?** not “does Δφ become nonzero?” |
| M3 | Edge still prefers **BVP/matching** if the target is `φ→∞` at finite r |

---

## 4. Standing clean stack (after this continue)

```text
Phase 1  Metric form (R1–R3)                    SOLID
Phase 2  Free D_A ⇒ EH bulk nonempty             SOLID (CAS)
Path A   Areal vacuum: Coulomb φ                 SOLID (gauge-tagged)
Path B   Free D_A+EH vacuum: open redshifting    CHARACTERIZED (prov.)
Matter   OPEN — for scale/edge, not for “any z”
x_max    OPEN — not vacuum IVP
```

---

## 5. One-line

**Path B vacuum asymptotes to finite φ and growing D_A; Coulomb is not free-`D_A` on-shell; matter’s job is scale and edge, not inventing redshift from scratch.**
