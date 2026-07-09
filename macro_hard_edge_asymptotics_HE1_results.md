# WP-HE1 RESULT — Asymptotics of hard edge `φ→+∞` at finite chart radius

**Date:** 2026-07-08 · **Status: PROVISIONAL** (driver CAS / asymptotic balance; independent verifier owed before bank).  
**MAP:** `macro_native_edge_HARD_MAP.md`  
**Script:** `macro_hard_edge_asymptotics_HE1.py`  
**Scope:** Path A areal + Path B free-`D_A`; vacuum + dilated bounded source. No shooting. No SNe.

---

## 0. Question

Under the **current** bulk (Path A / Path B as used in the clean restart), is an outer hard edge

```text
φ → +∞  as  r → r_*^−  with  r_* < ∞
```

compatible with the Euler–Lagrange equations?

This is the primary E-hard-1 (c-analog / `x_max`) candidate.

---

## 1. Path A (areal `D_A ≡ r`, EH empty, R1 kinetic)

### Vacuum

```text
d/dr(Z r² φ') = 0  ⇒  φ = c₀ − q/r
```

| Limit | Behavior |
|-------|----------|
| `r→∞` | `φ→c₀` **finite** |
| `r→0` | `φ→±∞` if `q≠0` — **center** singularity, not outer edge |

### Outer blowup ansatz

`φ = −α log(r_*−r)` or `φ = β/(r_*−r)^μ` (`α,β,μ>0`)  
⇒ `(2r φ' + r² φ'') ∼ (r_*)² / s^{μ+2} ≠ 0`.

Vacuum EL cannot hold.

### Dilated dust

```text
d/dr(Z r² φ') = 2 ρ r² e^{−2φ}
```

As `φ→+∞`, `e^{−2φ}→0`. For **bounded** `ρ`, RHS→0 while LHS stays singular for blowup ansätze.

**Dilated matter makes outer `φ→∞` harder, not easier** (source self-thins exactly where you need a balance).

### Path A verdict

**Outer `φ→+∞` at finite `r_*` is incompatible with Path A bulk + bounded dilated density.**

---

## 2. Path B (free `D_A`, EH + R1 kinetic)

### Smooth finite `D_A` at the would-be edge

As `φ→+∞`, the EH piece `∝ e^{−2φ} D_A''` drops out of EL_φ  
⇒ `d/dr(D_A² φ') ≈ 0` ⇒ `φ' ∼ C/D_A²` finite if `D_A` finite nonzero  
⇒ **`φ→∞` needs infinite radial range**, not finite `r_*`.

### Singular `D_A→0` with `φ→∞`

Kinetic balance can suggest candidates (e.g. log / power blowups with `D_A ∼ s^ν`).

But **EL_D** contains

```text
∼ Z D_A e^{+2φ} (φ')²
```

When `φ→+∞` and `φ'≠0`, **`e^{2φ}(φ')²` is catastrophically large**.  
For any power-law `D_A ∼ s^ν` with `ν` finite and `Z>0`, this term **cannot be canceled** by the remaining power-law pieces.

**Escapes (all theory-changing):**

| Escape | Meaning |
|--------|---------|
| `Z=0` | Drop R1 kinetic (abandons Path A/B bulk) |
| `D_A≡0` | Degenerate metric |
| Drop/replace EH+kinetic form | New bulk |
| No free-`D_A` variation | Back to areal freeze (Path A) — still no outer φ→∞ |

### Dilated dust on Path B

Sources `∝ e^{−2φ}→0` at the edge — **cannot** cancel `e^{2φ}(φ')²` in EL_D.

### Path B verdict

**Outer `φ→+∞` at finite chart radius with nondegenerate free `D_A` is blocked by EL_D under current Path B bulk.**

---

## 3. Summary table

| Setting | Outer `φ→∞` at finite `r_*` |
|---------|------------------------------|
| Path A vacuum Coulomb | **NO** (only center) |
| Path A + dilated bounded ρ | **NO** |
| Path B, smooth finite `D_A` | **NO** (needs infinite r) |
| Path B, `D_A→0` + `φ→∞` | **NO** (EL_D / `e^{2φ}(φ')²`) |
| Path B + dilated dust | **NO** (thins; doesn’t fix EL_D) |

---

## 4. HE1 result (scoped)

> **Under the clean-restart Path A and Path B bulks used in this arc, a hard outer edge `φ→+∞` at finite coordinate radius is not available.**  
> Numerics that never saw such an edge are consistent with this asymptotic obstruction, not merely unlucky seeds.

**Not claimed:** UDT cannot have any edge in any bulk.  
**Claimed:** **This** bulk + **this** edge definition do not fit.

---

## 5. Implications for theory flesh-out (ordered)

| Priority | Move | Why |
|----------|------|-----|
| **1** | **Re-open bulk completion** | Hard edge may need terms not in EH+kinetic free-`D_A` (or different variational treatment of EH) |
| **2** | **E-hard-3 marginal M–R** | Scale `∼GM/c²` without requiring `φ→∞` |
| **3** | **E-hard-2 finite-cell BC** | Derived outer data on `(φ,D_A)` finite; not φ→∞ |
| **4** | **E-hard-4 φ-ceiling theorem** | Elevate Path B’s φ∼2 attractor to a proven bound; reframe “edge” as asymptotic ceiling |
| **5** | Do **not** WP-HE2 shooting for `φ→∞` | HE1 says empty — shooting would only reconfirm |

**Dilation of matter toward the edge remains correct** and is **hostile** to sourcing a `φ→∞` wall with bounded density — consistent with self-thinning.

**`x_max` as finite-chart `φ→∞`:** still a good **ambition**, but it **demands bulk that HE1 does not contain**. Either change the bulk or change the edge definition.

---

## 6. Recommended next (single)

**Pick one with Charles:**

**A.** FE completion MAP: what native term could cancel `e^{2φ}(φ')²` or change the variational problem so a limit edge exists.  

**B.** Prove/characterize **φ ceiling** on Path B (E-hard-4) as the honest outer story of current bulk.  

**C.** Derive **marginal mass condition** (E-hard-3) on Path A Coulomb / Path B for scale without φ→∞.

Driver lean: **B short (ceiling theorem attempt) + A in parallel as written MAP** — don’t shoot φ→∞.

---

## 7. One-line summary

**HE1: outer `φ→∞` at finite radius is incompatible with Path A vacuum/dilated dust and is blocked on Path B by EL_D’s `e^{2φ}(φ')²`; hard c-analog edge needs new bulk or a different native edge definition — not more IVP.**
