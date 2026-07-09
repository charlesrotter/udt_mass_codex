# RESULT — Path B φ “ceiling” (E-hard-4 probe)

**Date:** 2026-07-08 · **Status: PROVISIONAL** (numeric + structural CAS; **not** a fully proved theorem).  
**Script:** `macro_pathB_phi_ceiling.py`  
**Companion MAP:** `macro_bulk_completion_limit_edge_MAP.md`  
**Parents:** HE1 · Path B vacuum characterize  

---

## 0. Question

Is there a **finite bound** on redshift depth for Path B vacuum dynamics — the numeric “φ∼2” attractor?

---

## 1. What is *not* true (important)

### No bound on absolute `φ`

Exact vacuum solutions:

```text
φ = const  (any real number),   D_A = a + b r
```

satisfy the Path B EL.  
Hence **`φ = 100` is allowed**. There is **no** universal field-space bound `φ ≤ φ_*`.

### `φ → φ+c` is **not** a symmetry of Path B

EH pieces carry `e^{±2φ}`.  
Setting `φ(0)=0` is a **physical normalization of the seed**, not pure gauge.  
Meaningful bounded quantities are along **trajectories**, e.g. `Δφ = φ_∞ − φ_core` for a specified data class.

---

## 2. What *is* supported (scoped conjecture)

### Data class D0 (flat-core redshifting seeds)

```text
D_A(r0)=D0>0,  D_A'(r0)=S0,  φ(r0)=0,  φ'(r0)=Q0≥0
```
integrate outward on Path B vacuum.

**Numeric (dense):**

| Survey | max Δφ | notes |
|--------|-------:|-------|
| Q0∈[0,5], D0=1, S0=0 | **2.044** | p50≈2.041, p99≈2.044 |
| Wider D0,S0,Q0 grid (120 OK) | **2.106** | p90≈2.05, p99≈2.09 |
| Counterexample hunt Δφ>2.2 (phi0=0) | **none found** | log grid D0×Q0×S0 |

**Conjecture C-ceil (D0 class, PROVISIONAL):**

> For Path B vacuum with data class D0 (`φ_core=0`, regular positive `D_A`, mild `S0`),  
> the outward solution satisfies  
> `Δφ = sup(φ−φ_core) ≤ Δ_*`  
> with `Δ_* ≈ 2.1` (numeric; exact `Δ_*` unknown).  
> Asymptotically `φ→φ_∞≤Δ_*`, `φ'→0`, `D_A'→v` (open S2-like exterior).

**Not proved:** no Lyapunov function found in this pass; no first integral that forces the bound.

---

## 3. Absolute `φ_∞` vs `Δφ`

Seeds with `φ_core ≠ 0`:

| φ_core | φ_end (Q0=0.5, D0=1, S0=0) | Δφ |
|-------:|----------------------------:|---:|
| −1.0 | ≈2.04 | ≈3.04 |
| −0.5 | ≈2.03 | ≈2.53 |
| 0.0 | ≈2.03 | ≈2.03 |
| +0.5 | ≈2.08 | ≈1.58 |
| +1.0 | ≈2.07 | ≈1.07 |
| +2.0 | ≈2.41 | ≈0.41 |

For **negative cores**, `Δφ` can exceed 2 while **`φ_end` still sits near ∼2**.  
So the attractor looks more like a **preferred absolute floor/ceiling region around φ∼2 for this kinetic+EH balance** when starting from below — not merely `Δφ≤2` from every core.

**Refined reading (still provisional):**

- From `φ_core ≤ 0` with D0-class kinematics, solutions often **approach φ_∞∼2 from below**.  
- From `φ_core > 2`, they need not fall back to 2 (seed φ0=2 → φ_end∼2.41).  
- Exact characterization of the basin of attraction of “φ_∞∼2” is **open**.

---

## 4. Structural facts that shape a future theorem

1. **S2 vacuum:** any constant φ + linear `D_A` is exact — redshifting needs **non-linear** `D_A` evolution.  
2. **On exact `D_A=vr`:** only `φ=const` (Coulomb hair off-shell) — same as HE1/Path B notes.  
3. **EH breaks φ-shift** — absolute φ levels can be dynamical targets.  
4. **HE1:** no finite-r `φ→+∞` in this bulk — consistent with a **finite** outer φ story.

---

## 5. Status of E-hard-4

| Claim | Grade |
|-------|--------|
| Absolute `φ` bounded for all solutions | **FALSE** |
| `Δφ` bounded for data class D0 (`φ_core=0`) | **CONJECTURE** — strong numeric support, no proof |
| Attracting φ_∞∼2 from below for a class of seeds | **LEAD** — supported by shift-seed table |
| Exact analytic `Δ_*` | **OPEN** |
| Replace c-analog edge | Only if Charles accepts finite-φ outer story |

---

## 6. Link to bulk completion

If C-ceil stands, **current Path B bulk’s honest outer story** is:

> open geometry + **finite redshift depth** from regular cores — not `φ→∞` at finite r (HE1).

Restoring E-hard-1 still requires **bulk completion** (`macro_bulk_completion_limit_edge_MAP.md`), not more IVP.

---

## 7. One-line summary

**No absolute φ bound (const-φ solutions free); for flat-core φ(0)=0 data, Δφ is numerically capped near ∼2.05–2.1 with no counterexample in large scans — a scoped ceiling conjecture, not a finished theorem.**
