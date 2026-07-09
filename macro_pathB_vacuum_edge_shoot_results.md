# RESULT — Path B vacuum: integrals scan + edge-oriented shooting

**Date:** 2026-07-08 · **Status: PROVISIONAL** (driver).  
**Script:** `macro_pathB_vacuum_integrals_edge.py`  
**Parents:** `macro_pathB_vacuum_characterize_results.md` · `macro_pathB_vacuum_continue_results.md`  
**No matter · no G/P · no SNe.**

---

## 0. Questions

1. Is there an obvious **first integral** along redshifting Path B vacuum trajectories?  
2. Can vacuum Path B reach a **high-z edge** (`φ` large) or an **outer turning** (`D'→0` after expansion) by shooting seeds?

---

## 1. Flux identity (CAS)

```text
EL_φ = 0  ⇔  d/dr(Z D_A² φ') = 4 D_A e^{−2φ} D_A''
```

φ-flux is tied to **`D_A''`**, not to an external density.  
Exact vacuum family remains: **`φ=const` and `D_A''=0`**.

No new closed-form redshifting integral found symbolically (Coulomb on free `D_A` still blocked by EL_D).

---

## 2. Numerical “constants” along a Q-kick run

Trajectory: flat core + `φ'(0.2)=0.5` → `r=10`, `Δφ≈+2.03`.

| Candidate | rel. span (roughly max−min over mid trajectory) |
|-----------|-----------------------------------------------|
| `φ` | O(1) — changes then floors |
| `D_A/r`, `D_A'` | O(1) — not constant early |
| `Z D_A² φ'` | O(10) — not conserved |
| `D_A² φ' e^{2φ}` | **smallest among tested** (~1.5 rel span) — **not** a clean integral |

**Verdict:** no sharp first integral jumped out of the scan; asymptotics remain “`φ→φ_∞`, `D_A'→v`” as characterization, not a named conserved charge.

---

## 3. Edge-oriented shooting (vacuum only)

### E1 — How large can `φ` get?

**375 seeds** (`D0`, `S0=D_A'`, `Q0=φ'` on a grid, integrate to `r≤15`):

| Stat | Value |
|------|------:|
| **max φ reached** | **≈ 2.042** |
| p50 | ≈ 2.014 |
| p90 | ≈ 2.039 |
| p99 | ≈ 2.042 |

**Hard ceiling near `φ∼2`** in this vacuum Path B IVP family — cannot push to CMB-scale depths or `φ→∞` by cranking initial `φ'`.

### E2 — `D_A'` turnovers

A few turnovers appear **only with initially negative `D_A'`** (contracting seeds): `D` decreases, `D'` crosses zero once, `φ` still **O(1)** (examples `φ∼0.8–0.9`).  

These are **bounce-like**, not “expand from core then close at outer edge.”

### E3 — Shoot `D_A'(r_out)=0` from flat core (`S0=0`, free `Q0`)

At `r_out=5`, `S(r_out)` is **≥ 0** and **increases** with `Q0` in the scan.  

**No root** `S(r_out)=0` for expanding flat-core redshifting seeds.

### E4 — `φ(r_out=5)` vs `Q0`

Max `φ(5)≈2.04` (same ceiling); min small when `Q0→0`.

---

## 4. Classification

| Target | Vacuum Path B IVP/shoot |
|--------|-------------------------|
| Open redshifting solutions | **Yes** (prior + here) |
| `φ→∞` or even `φ≫2` | **No** — ceiling ~2 |
| Outer `D'=0` after expansion from flat core | **No** in scan |
| Bounce from contracting seed | **Yes** (limited) |
| Replace need for matter for redshift | Vacuum already enough for mild Δφ |
| Replace need for matter for **edge / depth / scale** | **Still needed** (or new gravity terms) |

---

## 5. Implication for `x_max` / Charles limit picture

Under **only** Path B vacuum (EH + free `D_A` + R1 kinetic):

- You get a **finite redshift ceiling**, not an infinite-redshift edge.  
- You do **not** get a chart-finite `φ→∞` locus by IVP/shooting in this family.  
- So the **`c`-analog edge**, if real, requires **something beyond this vacuum sector** (native matter, different bulk terms, different BVP posing, or a different edge definition than `φ→∞`).

That is a **scoped vacuum no-go for edge-by-IVP**, not a no-go for UDT as a whole.

---

## 6. What “continue” should mean next

1. **Native matter on Path B** — first question: edge / mass selection / break φ∼2 ceiling — with a **derived or Charles-pinned** sector (not Gaussian μ by habit).  
2. **Or** return to **Path A + native matter** if areal gauge is preferred for coupling.  
3. **Or** MAP: which bulk term *could* allow `φ→∞` (if vacuum Path B forbids it structurally).  
4. **Do not** keep scanning vacuum seeds for higher φ — ceiling is robust in this grid.

---

## 7. One-line summary

**Path B vacuum: no clean new integral; φ is capped near ~2 across hundreds of seeds; no expanding-core outer D'=0 root — edge/`x_max` is not a vacuum-IVP phenomenon in this sector.**
