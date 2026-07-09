# RESULT — Clean-core macro: DERIVE free-`D_A` EOM + first OBSERVE (center structure)

**Date:** 2026-07-08 · **Status: PROVISIONAL (first observe; driver CAS + numeric; blind verifier not yet run).**  
**Contract (pre-registered):** `macro_clean_core_first_observe_CONTRACT.md`  
**Script:** `macro_clean_core_derive_observe.py`  
**Posture / MAP:** `macro_Q1_source_posture.md` · `macro_universe_clean_core_MAP.md`  
**Mode:** DERIVE + OBSERVE (characterize). **Not** a SNe fit, cosine hunt, or “macro works” headline.

---

## 0. What was asked

Finish remaining planning pins (Q4/Q5), then **derive** the clean-core free-`D_A` equations under Q1 posture (a) and **observe** whether a **regular geometric center** + **nontrivial redshift** exists in that slice.

---

## 1. Premise ledger (this run)

| Item | Tag |
|------|-----|
| Q1 posture (a) primary; (c) edge ref; (b) parked | POSTURE (Charles-accepted) |
| Uncompensated `𝒦` (P-type) for matter/on P explore; G as control | POSTURE |
| Round free `D_A` (`h = D_A²Ω`), not frozen to `r` | FREE ansatz |
| Q4: `L_m = −ρ(r)` prescribed Gaussian / φ-blind | **FREE temporary stand-in** (not native macro matter claim) |
| Q5: no mirror seal; mid-domain box / analytic center | FREE |
| Target center class: `D_A(0)=0`, power-law, `φ` finite | THEORY-motivated regularity target |
| `Z_φ = 1` | FREE convention |
| Static spherical | FREE slice |
| 1101 / SNe / cosine as targets | **OUT** |

---

## 2. DERIVE (CAS) — free-`D_A` Euler–Lagrange

Reduced radial action (angles integrated, overall constants dropped as in contract):

```
L_G = (Z/2) D_A² φ'² − 2 (D_A')²                         # compensated 𝒦
L_P = (Z/2) D_A² φ'² − 2 e^{−2φ} (D_A')²                 # uncompensated 𝒦
L_Pρ = L_P − D_A² ρ(r)                                     # + φ-blind density
```

### 2.1 Branch G vacuum — recovers banked vacuum macro

| Claim | CAS |
|-------|-----|
| `d/dr(Z D_A² φ') = 0` ⇒ `Z D_A² φ' = q` | TRUE |
| `D_A'' = −q²/(4 Z D_A³)` | TRUE |
| Matches `sne_native_background_n2.py` vacuum | TRUE |

### 2.2 Branch P vacuum — free `D_A`

| Claim | CAS |
|-------|-----|
| `d/dr(Z D_A² φ') = 4 e^{−2φ} (D_A')²` | TRUE |
| Frozen `D_A = r` ⇒ `Z(r²φ')' = 4 e^{−2φ}` (founding Branch-P eq) | TRUE |
| Coupled `D_A` equation (see script EL_DA) | TRUE (sympy EL) |

### 2.3 Branch P + φ-blind `ρ` — load-bearing for Q1(a)

| Claim | CAS |
|-------|-----|
| **EL_φ identical to vacuum P** (`ρ` does not enter) | **TRUE** |
| `ρ` enters only EL_`D_A` (extra `+2 D_A ρ` in the DA residual form) | TRUE |

**Interpretation (observe-ready):** under the native claim `δS_m/δφ = 0`, a continuum density stand-in **cannot** source or regularize `φ` except by changing `D_A(r)`. The `φ` equation still only sees geometry through `(D_A')²`.

---

## 3. DERIVE — center structure (analytic)

### 3.1 P-type, `D_A(0) = 0`, power-law

Integrate EL_φ with finite flux at the origin (`C = 0`):

```
Z D_A² φ'(r) = ∫_0^r 4 e^{−2φ} (D_A')² ds
```

Ansatz `D_A = a r^α` (`α > 1/2`), `e^{−2φ} ∼ const` at leading order:

```
φ'(r) ∼ 1/r     for every such α
```

In particular standard regularity `D_A ∼ r` (`α = 1`):

```
φ'(r) ∼ 4/(Z r)     (leading, φ≈0)
φ(r)  ∼ (4/Z) ln r  → −∞ as r → 0
```

**Log dilation singularity at the geometric center.** Structural, not a grid artifact.

Leading-order numeric check (`eps * φ'(eps) = 4` for `Z=1`): confirmed for `eps ∈ {1e-1 … 1e-5}`.

### 3.2 G-type (control)

```
Z D_A² φ' = q
D_A ∼ r, q ≠ 0  ⇒  φ' ∼ q/r²  ⇒  φ ∼ −q/r   (stronger singularity)
q = 0           ⇒  φ = const   (no redshift)
```

Same vacuum tension as the n=2 optics / vacuum-macro banked story: **no regular centered redshifting vacuum**.

### 3.3 Why φ-blind matter does not open C3 in this slice

Because `ρ` is absent from EL_φ, any profile of φ-blind density leaves the integral identity for `φ'` unchanged in form. Changing `D_A` cannot remove the `φ' ∼ 1/r` law for power-law vanishing `D_A(0)=0` (same scaling argument).

---

## 4. OBSERVE — numeric (bounded)

### 4.1 G control (IVP)

| Case | Result |
|------|--------|
| `q=0`, `E=1` | `Δφ = 0`, `D` grows — no redshift |
| `q=0.5`, `E=0` start `D=10^{-3}` | large `Δφ`, huge `φ'` at start — off-center/singular start |
| `q=1` similarly | same class |

### 4.2 P mid-domain trajectories (not centers)

Starting at `r0=0.5` with finite data (not a regularity claim), P IVP **succeeds**:

| `ρ0` | `Δφ` (to r=4) | finite |
|------|----------------|--------|
| 0 | +1.72 | yes |
| 1 | +1.71 | yes |
| 10 | +1.87 | yes |

EOM residual on vacuum mid-domain path: median `|π' − 4 e^{−2φ}(D')²| ∼ 8×10^{−5}` (integrator OK).

**So:** P free-`D_A` dynamics are real away from the origin; the obstruction is **center regularity**, not “no ODE.”

### 4.3 Near-center full IVP

Integrating *from* `eps` with `D∼r` seed is stiff (expected: `φ'∼1/eps`). Analytic center law used as the load-bearing diagnostic; mid-domain IVP used for residual check.

---

## 5. Pre-registered classes (outcome)

| Class | Meaning | Outcome |
|-------|---------|---------|
| **C0** | G vacuum tension | **CONFIRMED** (analytic + IVP) |
| **C1** | vacuum P free-`D_A` center | **SINGULAR** (`φ'∼1/r`) |
| **C2** | P + φ-blind `ρ` cures center? | **NO** (`ρ` ∉ EL_φ) |
| **C3** | regular geometric center + nontrivial `Δφ` | **NOT FOUND / structurally blocked in this slice** |

---

## 6. Scoped claim (whole-before-slice)

**In the static, spherically symmetric, round free-`D_A` clean-core slice, with uncompensated `𝒦` and φ-blind continuum density stand-in:**

1. Free-`D_A` G and P Euler–Lagrange equations are derived and CAS-checked (G matches the prior vacuum macro).  
2. **Option (a) as implemented with strictly φ-blind bulk density does not produce a regular geometric center with finite `φ`.**  
3. The blockage is **structural** in EL_φ + `D_A(0)=0`, not a failed SNe fit and not a frozen-`h=r` artifact alone (free `D_A` was used).  
4. Mid-domain P solutions exist and carry nontrivial `Δφ` — the theory is not dynamically empty; the **centered regular cosmology** class is the empty one in this coupling.

This is **not** a verdict that “UDT has no macro.” It is a verdict that **this first legal slice of Q1(a) does not admit the regularity class we asked for.**

---

## 7. What this does *not* kill

| Escape (not yet explored here) | Why it might matter |
|--------------------------------|---------------------|
| **Non-round / co-varying full `h_AB`** | `𝒦` structure richer than `(D_A')²` |
| **`D_A(0) > 0` minimum** (no point center) | cell-like finite core / throat; different regularity |
| **Direct φ–matter channel** (`δS_m/δφ ≠ 0`, Thread-B α) | would put matter in EL_φ; reopens P6 |
| **Ensemble (b)** | effective source from many exteriors — parked |
| **Different matter kinetic** (still φ-blind but with `h`-derivatives in `L_m`) | could change EL_`D_A` strongly; still won’t enter EL_φ if truly φ-blind |
| **Time-live / less symmetry** | out of this slice |

Solver-first order if one still wants centered regular redshift: (1) left out of solver = direct coupling or non-round `h` or different center class; (2) numeric was not the C1/C2 limit; (3) DOF free-`D_A` was on; (4) this is one symmetry+coupling corner.

---

## 8. Honest re-grade of the “matter will cure the vacuum center” hope

`external.md` §7A hoped a finite core density would cure the vacuum center. **Under strict φ-blindness, that hope fails for a pointlike geometric center:** density never appears in the `φ` equation. Curing requires either a **different center geometry**, a **channel into EL_φ**, or a **different `𝒦`/transverse structure**.

That is progress: it prevents another rabbit hole of scanning `ρ0` for a regular center that the equations forbid.

---

## 9. Recommended next (for Charles — not auto-launched)

Pick one **explicit** fork (solver-first, not mechanism-shopping):

1. **MAP the center class** — allow `D_A(min) > 0` / mirror core as macro (finite-cell universe canon adjacent) and observe closure there; or  
2. **Re-audit φ-blindness** for macro matter (when is `δS_m/δφ = 0` forced vs CHOSE levers?); or  
3. **Free non-round `h_AB`** (harder) with the same φ-blind discipline; or  
4. Stay in mid-domain characterization (what P free-`D_A` solutions look like as pure math) without demanding `D_A(0)=0`.

---

## 10. Files

| Path | Role |
|------|------|
| `macro_clean_core_first_observe_CONTRACT.md` | pre-registration |
| `macro_clean_core_derive_observe.py` | CAS + numeric |
| this file | results |
| `macro_Q1_source_posture.md` / `macro_universe_clean_core_MAP.md` | planning parents |

**Verifier:** not run (PROVISIONAL). Owed before any banked “theorem” wording: independent sympy re-derive of free-`D_A` P EL_φ + center scaling, and re-check that `ρ` is absent from EL_φ.

---

## 11. One-line summary

**Derived free-`D_A` G/P equations (CAS OK); observed that Q1(a) with φ-blind density cannot regularize a point center — `φ'∼1/r` is structural; mid-domain P solutions exist.**
