# PHASE 1 — Metric only (clean restart)

**Date:** 2026-07-08 · **Mode: MAP / cold read. No field equations. No solutions. No continuum stand-ins.**  
**Parent:** `macro_clean_restart_from_metric_MAP.md`  
**Authority:** CANON **C-2026-06-18-1** + `relativistic_metric_rederivation_results.md` (provenance).  
**Status:** Orientation for restart — not new canon.

---

## 0. Purpose

State **only** what the metric postulates fix, and what they leave open — so Phase 2 (field equations) cannot smuggle solution-space choices back into the geometry.

---

## 1. Owner inputs (the only premises for the metric form)

Charles’s relativistic requirements (canonized):

| ID | Content |
|----|---------|
| **R1** | Positional dilation depends only on **differences** in φ (no privileged zero of φ as a geometric fact; φ → φ+const is pure gauge for the structure) |
| **R2** | Dilations **compose** across intermediate positions |
| **R3** | **Mutual reciprocity**: each position sees the other’s clock run slow; neither preferred |

**Named side premises (not hidden):**

| ID | Content | Tag |
|----|---------|-----|
| **P-reg** | Dilation factor continuous/positive (regularity) so Cauchy equation ⇒ exponential | Physically mandatory regularity, not a free coupling |
| **P-slot** | Under R3, the direction conjugate to time is the **φ-gradient (radial)** direction, not a transverse one | **CHOSE analog** (canon caveat): obvious, not forced by abstract relativity alone |

No matter, no action, no field equation, no asymptotic flatness enter the metric-form derivation.

---

## 2. What is forced (metric structure)

### 2.1 Clock factor

Clock-rate function `f(φ) = √(−g_tt / c²)`.  
Dilation between positions: `D(φ_A,φ_B) = f(φ_B)/f(φ_A)`.

- R1 ⇒ `D = g(φ_B − φ_A)`  
- R2 ⇒ `g(x)g(y)=g(x+y)`  
- P-reg ⇒ `g(x)=e^{k x}`  
- Convention: define φ so that `g_tt = −e^{−2φ} c²` (sign/normalization of φ; no physics content)

### 2.2 Radial reciprocity (B = 1/A)

R3 + P-slot ⇒ clock factor and radial length factor are mutual inverses:

```text
√(−g_tt/c²) · √g_rr = 1
⇒  g_tt g_rr = −c²
⇒  g_rr = e^{+2φ}
```

**Source-free / kinematic** — true before matter and before field equations (canon).

### 2.3 Line element (structure)

In a chart where φ = φ(r) is static and the φ-gradient is along `r`, the **radial–time block** is:

```text
ds² ⊃ −e^{−2φ} c² dt² + e^{2φ} dr² + (transverse part)
```

### 2.4 Immediate kinematic consequences (still no FE)

| Consequence | Formula / statement | Needs FE? |
|-------------|---------------------|-----------|
| Redshift, static observers | `1+z = e^{φ_source − φ_observer}` | No |
| Zero of φ | Gauge (R1); each observer may set φ=0 at themselves | No |
| Lorentzian signature | Holds for all real φ | No |
| Local SR | Local frames intact | No |
| Meaning of `φ→∞` | Infinite redshift between that locus and φ=0 | No — **existence** of such a locus is not metric-forced |

**Optics (null geodesics + photon number):** luminosity-distance factor `n=2` on this metric family was derived in the n=2 arc (`d_L = (1+z)² D_A`). That is **kinematic once photons are standard null + conserved**; it is not a field equation for φ. Keep it on the kinematics shelf for later checks; do not use it to fix φ(r).

---

## 3. What is **not** forced by the metric postulates

Canon is explicit (C-2026-06-18-1 “Forces”):

| Free / open | Tag |
|-------------|-----|
| **Transverse / angular block** `h_AB` (or `D_A(r)² dΩ²` vs frozen `r² dΩ²`) | FREE geometric sector |
| Off-diagonal / shift (rotation, shear) | FREE unless set to zero by ansatz |
| Time dependence of φ | FREE (static is a choice) |
| Chart and topology | FREE |
| Profile `φ(r)` | Requires dynamics (Phase 2+) |
| Matter content | Not a metric input |
| Edge / `x_max` as a locus | Solution question, not metric identity |
| Constants beyond structure | `c` appears in `g_tt`; `G` does not enter the metric form |

**Four independent solution-space choices often smuggled as if metric-forced:**

1. Static  
2. Spherical symmetry  
3. Diagonal  
4. Areal-radius gauge (`D_A = r` or coordinate = areal radius)

Each must be **tagged FREE** when used.

---

## 4. Two readings of R1 (do not conflate)

| Reading | Meaning | Used for metric form? |
|---------|---------|------------------------|
| **Weak** | No privileged zero of φ (shift gauge) | **Yes** — this is what the exponential derivation uses |
| **Strong** | No privileged point in space (full spatial homogeneity of the universe) | **No** — not forced by the metric construction; would over-constrain profiles |

Phase 2+ must not slide from weak to strong without a new postulate.

---

## 5. Preferred writing for Phase 2

Use the **most open** metric family consistent with §2, without freezing transverse size:

```text
ds² = −e^{−2φ} c² dt² + e^{2φ} dr² + h_AB dx^A dx^B
```

Spherical reduction (FREE ansatz when used):

```text
h_AB dx^A dx^B = D_A(r)² dΩ²
```

with **`D_A` a free function**, not set equal to `r` unless gauge-fixed and tagged.

**Measure fact (for Phase 2 CAS):** on this reciprocal family,  
`√(−g) = c √h` is **φ-free** (dilation factors cancel). That is kinematic identity, not a field equation.

---

## 6. Explicitly out of Phase 1

- Einstein equation, Einstein–Hilbert bulk content  
- Any bulk action for φ  
- Matter Lagrangians, α, μ, winding  
- G/P, cell seals, continuum IVPs  
- Claims about existence of `x_max` or critical matter  

---

## 7. One-line Phase 1 summary

**Metric postulates fix exponential dilation + radial reciprocity and the redshift law; they leave transverse geometry, time dependence, and the profile of φ completely open — those need field equations or further postulates, not smuggled chart choices.**
