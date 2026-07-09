# RESULT — Macro continuation: larger box, action-matter, finite core

**Date:** 2026-07-08 · **Status: PROVISIONAL** (driver observe; no blind verifier).  
**Contract:** `macro_alpha_continuation_CONTRACT.md`  
**Script:** `macro_alpha_continuation.py`  
**Framing:** `macro_no_GP_framing.md` (no G/P).  
**Prior:** `macro_alpha_jet_outward_results.md` · `macro_phi_blindness_reaudit.md`.

---

## 0. What we continued

1. Push the successful **prescribed-σ jet** to larger boxes (r_max = 8, 30, 80).  
2. Replace ad hoc `σ` with **action-consistent** continuum matter  
   `L ⊃ −D_A² μ(r) e^{αφ}` (one L → both EL_φ and EL_`D_A`).  
3. Probe **finite-core** center class `D_A(0)=D_c>0`, `D_A'(0)=0` (no point pinch).

No SNe / cosine / 1101.

---

## 1. Premise ledger

| Item | Tag |
|------|-----|
| Uncompensated `𝒦` reduced radial L | CHOSE probe |
| Jet: `σ0=−4/α` Gaussian (prior stand-in) | FREE |
| Action matter: `μ=μ0 exp(−(r/r_c)²)`, weight `e^{αφ}` | FREE continuum stand-in, action-consistent |
| α ∈ {−2,−1,−0.5,0} on cores | FREE |
| Finite core `(D_c, D'=0, φ'=0, π=0)` | FREE center class |
| Z=1 | FREE convention |

---

## 2. PART A — Jet, larger box

### Outcomes

| r_max | OK finite | `D_A` turnover | Δφ range (sample grid) |
|------:|:---------:|:--------------:|:-----------------------|
| 8 | 5/5 | **0** | ~1.96–2.10 |
| 30 | 5/5 | **0** | ~2.07–2.18 |
| 80 | 5/5 | **0** | ~2.14–2.24 |

**L1:** jet solutions **survive** to r=80.  
**L2:** **no** `D_A` turnover in-box — areal radius keeps growing.  
**L5:** no edge signal; fields stay finite.

### Sample profile (`α=−1`, `r_c=1`, jet)

| r | D_A | D_A' | φ | 1+z=e^φ |
|--:|----:|-----:|--:|--------:|
| 1 | 7.9 | 10.3 | 1.76 | 5.8 |
| 5 | 54 | 12.3 | 1.97 | 7.2 |
| 20 | 250 | 13.6 | 2.09 | 8.1 |
| 80 | 1108 | 14.7 | 2.18 | 8.9 |

**Observe:** φ **rises fast then slows** (Δφ almost saturates near ~2.2 on this stand-in); D_A grows roughly with **slowly rising** D_A'. Looks like an **open, ever-expanding areal radius** with a **bounded redshift increment**, not a closed cell and not a φ→∞ edge inside the box.

**Scoped, not a depth law:** saturation near Δφ~2 is tied to this FREE `σ` family + box; do not bank as 1101 or cosmology.

---

## 3. PART B — Action-consistent bulk `μ` at a **point** center

### Analytic (load-bearing)

```
π' = 4 e^{−2φ}(D_A')² − α D_A² μ e^{αφ}
```

At `D_A=0`, `D_A'=1`: matter term **vanishes** ⇒ `π'(0)=4` ⇒ same **`φ'∼1/r` singularity** as φ-blind / α-only-through-D².

**L3: FAIL for regular point center.**  
The prior jet’s finite-at-origin `σ` is **not** reproduced by bulk `μ` with standard `D_A²` measure. Those are different stand-ins.

### Numeric

All action point-center seeds with `D(ε)=ε` **die immediately** (`|φ'(ε)|∼4/ε`, collapse) — matches analytic.

---

## 4. PART C — Finite core + action `μ` (the productive class)

Start: `D_A=D_c>0`, `D_A'=0`, `φ=0`, `π=0` at the origin (even core).

### Outcomes (r_max=30)

| Class | Behavior |
|-------|----------|
| `μ0=0` | Trivial: `D_A≡D_c`, **Δφ=0** (vacuum core, no dynamics) |
| `α=−2`, `μ0>0` | **Mostly unstable**: D collapses toward 0, φ runs away (failed before r=30) |
| `α∈{−1,−0.5,0}`, `μ0>0` | **Many clean successes**: reach r=30, finite, **Δφ ∼ 1.7–2.2**, D_A grows |
| `D_A` turnover | **0** among successful cores |
| **L4** | **YES** for a large open set of `(α, D_c, μ0, r_c)` with α ≥ −1 in this scan |

### Important structural read

Even **`α=0`** (no direct weight in EL_φ) gives **nontrivial Δφ** on finite cores once `μ0>0`:

- Matter in EL_`D_A` drives `D_A` off the constant core (`D_A'` becomes nonzero).  
- Geometric piece `4 e^{−2φ}(D_A')²` then sources φ.  
- That is **indirect geometric sourcing** working in the **finite-core** center class — without prescribed finite-at-origin `σ`.

So:

| Center class | What works |
|--------------|------------|
| Point `D_A(0)=0` | Needs a source that **does not vanish** as D_A→0 (prior `σ` stand-in); bulk `D_A²μ` **fails** |
| Finite core `D_c>0` | **Action-consistent bulk μ works**, including α=0 indirect channel |

α=−2 is a **bad corner** for this L_m (collapse) — characterize, don’t prefer it just because it was an old import-tagged value.

---

## 5. Classification (contract IDs)

| ID | Verdict |
|----|---------|
| L1 | **PASS** — jet survives r=80 |
| L2 | **No turnover** on jet or successful cores in boxes used |
| L3 | **Point center + action μ blocked** (analytic + numeric) |
| L4 | **Finite core + action μ works** (wide island α∈{−1,−0.5,0}, μ0>0) |
| L5 | **No natural edge** yet (no φ→∞, no D turnover) |

---

## 6. What changed in the “stuck?” picture

1. **Jet stand-in** remains a viable regular **point-center** path but looks **open** with **saturating Δφ~2**, not a closed universe.  
2. **Honest bulk continuum matter** does **not** save the point center.  
3. **Finite-core** is the natural home for action-consistent continuum matter — and there **indirect sourcing alone can produce redshift**.  
4. Still **no closure/edge** in these FREE scans — next physics is edge/BC/matter sector, not more α=0 panic.

---

## 7. Whole-before-slice

Static · spherical · round free `D_A` · uncompensated `𝒦` · FREE μ/α/σ · finite boxes.  
Not the full native angular matter sector; not dynamical μ; not verified blind.

---

## 8. Natural next

1. **Finite-core + action μ** as the primary continuum macro probe (retire point-center σ as mainline).  
2. Seek **edge/closure** conditions (what BC or μ profile makes D_A'→0 or φ→∞ at finite r?) — MAP first if needed.  
3. Optional: larger r_max on mild cores (`α=−1`, small μ0) — any late turnover?  
4. Reconnect to native cell `L_m` only when embedding particles, not as default macro.  
5. Blind verify analytic L3 + a few core residuals.

---

## 9. One-line summary

**Jets stay open to r=80 with Δφ saturating ~2; action bulk matter cannot regularize a point center but finite cores work (including α=0 indirect) with growing D_A and Δφ~2 — still no edge/closure in-box.**
