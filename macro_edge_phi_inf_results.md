# RESULT — Finite-core continuum probe for `φ→∞` edge at finite chart radius

**Date:** 2026-07-08 · **Status: PROVISIONAL** (driver observe; no blind verifier).  
**Contract:** `macro_edge_phi_inf_CONTRACT.md`  
**Script:** `macro_edge_phi_inf_probe.py`  
**Frame:** `macro_xmax_limit_FRAME.md` · edge MAP E2.  
**No G/P · no SNe/1101 targets.**

---

## 0. Question

Under the `x_max` limit frame — *does a clean-core continuum solution starting from a finite core develop*  
**`φ → +∞` at some finite coordinate radius `r_*`?**

---

## 1. Setup (reminders)

- Action-consistent continuum:  
  `L = (Z/2)D_A²(φ')² − 2 e^{−2φ}(D_A')² − D_A² μ(r) e^{αφ}`  
  with `μ = μ0 e^{−(r/r_c)²}`, `Z=1`.  
- Finite core IC: `D_A=D_c`, `D'=0`, `φ=0`, `π=0`.  
- Grid: `α ∈ {−1,−0.5,0,+0.5}`, `D_c,r_c ∈ {0.5,1,2}`, `μ0 ∈ {0…10}` → **252** primary runs; `r_max=50`, event at `φ=8`.  
- Control: prior **σ-jet** family (6 runs).  
- All levers FREE continuum stand-ins except geometric structure of L.

---

## 2. Outcomes (pre-registered)

| ID | Result |
|----|--------|
| **X0** | **CONFIRMED for this family** — no run develops large φ |
| **X1** φ_cut candidates (`φ≥8` at finite r) | **0 / 252** cores |
| **X2** true φ→∞ blowup | **Not seen** |
| **X3** D→0 collapse (primary grid) | **0** (this scan; prior α=−2 corners were unstable, not in this grid) |
| **X4** r_*/M clustering | N/A (no edge) |
| **X5** who shows edge | **Neither** cores nor jets |

### φ behavior (structural)

- Trivial `μ0=0`: `φ≡0`, `D≡D_c`.  
- All nontrivial cores that reach the box: **`φ_max` saturates ≈ 1.3–2.4** (highest ~**2.40**).  
- Raising cut to 12/20 and `r_max=80` on the highest-φ cases: **same ceiling** (`φ_max` unchanged ~2.3–2.4) — not “slow approach to ∞.”  
- Jets: **`φ_max ≈ 2.07–2.21`**, same ceiling family.  
- `D_A` typically **grows** (often a lot); area does not pinch off as an edge.

**Plain language:** in this continuum stand-in, redshift **levels off** near `1+z = e^φ ∼ 5–11`. It does **not** run to an infinite-redshift edge at finite chart radius under free outward integration from a regular core.

---

## 3. What this does *not* kill

| Still alive | Why |
|-------------|-----|
| **`x_max` / `c`-analog idea** | We tested **one** matter L + **one** IC class + **IVP outward**, not all of UDT |
| **E2 limit edge** | May require **BVP/matching** (impose edge, solve for parameters), not “hope IVP blows up” |
| **E1 closure** | Never imposed a second boundary; critical amount not asked |
| **`x_max ∼ GM/c²`** | Needs an edge or asymptotic mass definition first |
| Finite-core as middle | Still the best continuum middle we have |

---

## 4. What this *does* pressure

1. **Naive hope:** “Just integrate continuum matter from a core and `φ→∞` will appear.”  
   → **False** for this large FREE grid.

2. **Identification:** “Any saturating Δφ~2 is the cosmic edge.”  
   → **False** — it is a **ceiling of this dynamical family**, far below a true `φ→∞` edge, and it does not sit at a special finite `r_*` where the solution ends.

3. **IVP-only program** for E2  
   → Insufficient. A limit edge is usually a **boundary-value / matching** object (interior solution joined to a limit, or parameters tuned so an edge exists).

---

## 5. Interpretation (scoped advice)

Three distinct outer programs, sharpened by this null:

| Path | Meaning after this null |
|------|-------------------------|
| **A. BVP edge** | Define outer condition (e.g. `φ→∞` as `r→r_*`, or marginal `2M/D_A→1`, or `D_A'→0` + large φ) and **solve for** `(μ0, r_*, …)` — existence scan, not IVP tourism |
| **B. Different continuum / coupling** | This `L_m` may lack the channel that drives `φ` without bound; native angular matter or different weight might (must not invent for SNe) |
| **C. Soften the edge definition** | Maybe the physical “cannot exceed” is **not** `φ→∞` but a **finite max φ** set by the solution (saturates) — still a limit, but **not** infinite redshift. That would be a **different** postulate than Charles’s φ→∞ edge line and needs a Charles ruling |

**Driver lean (not a pin):** Prefer **A** next if we keep Charles’s wording (`φ→∞` at finite chart radius). The null says IVP from the core with this L does not free-fall into that edge; it does not say the edge is impossible as a selected global solution.

---

## 6. Mass-proxy side note (not load-bearing)

Crude `M ∼ ∫ 4π D_A² μ e^{αφ} dr` varies over many orders as `D_A` runs away. With no edge, `r/M` is not an `x_max` diagnostic — only shows how bad scale-free growth + stand-in density can be. **Do not bank.**

---

## 7. Whole-before-slice

- Static, spherical, round free `D_A`, this L, uncompensated `𝒦` term treatment, finite core, FREE μ Gaussian, geometric units.  
- One tile: **no φ→∞ edge under free outward IVP in this tile.**

---

## 8. Recommended next (when you say go)

1. **MAP a BVP edge condition** in one sentence (choose among: true `φ→∞` at `r_*`; marginal mass condition; finite-φ ceiling as alternate postulate).  
2. If true `φ→∞`: set up **existence/shooting** — free parameters `(μ0, r_c, …)` vs outer condition; report whether any solution hits it.  
3. Optional analytic: for this L, show why `φ` approaches a finite limit along open trajectories (if true) — would explain the ~2 ceiling.  
4. Do **not** add mechanisms to force `φ→∞` for SNe.

---

## 9. One-line summary

**Across 252 finite-core continuum runs (+ jet controls), φ saturates near ~2–2.4 and never hits a finite-radius `φ→∞` edge under outward IVP — the `x_max` limit idea now needs a BVP/matching (or a revised edge definition), not more free outward scans of this L.**
