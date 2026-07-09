# UDT field equations from the metric — clean core

**Date:** 2026-07-08 · **Mode:** foundation re-derive (metric → operators → action → EL).  
**CAS:** `macro_native_FE_rederive_clean.py` — **21/21 PASS** (this session).  
**Also aligns with:** `verify_native_fieldeq.py`, `verify_native_geo_action.py`, `native_geometric_action_results.md`.  
**Status: PROVISIONAL working core** — not new Charles canon. Aim: hold this and drop optional follow-on.

---

## Lay statement (the whole theory in one breath)

**GR:** geometry is the field; Einstein’s equation says how it responds to matter.  
**UDT:** **positional dilation** is the extra geometric content — clocks run at different rates in different places.  
The **metric form** is fixed by staying relativistic (dilation + reciprocity).  
The **field equations** come from a **single native geometric action** on that metric family — not from importing Einstein–Hilbert and hoping.

If this core is right, most of the recent macro scaffolding was optional noise.

---

## 1. Metric (only input: postulates)

| Postulate | Plain |
|-----------|--------|
| **R1** | Dilation depends only on **differences** in φ — no preferred zero of φ |
| **R2** | Dilations **compose** through intermediate places |
| **R3** | **Mutual:** each sees the other’s clock slow |

Named side premises (not hidden): regularity → exponential; R3 pairs clock factor with the **radial** length factor.

### Result

```text
ds² = − e^{−2φ} c² dt²  +  e^{2φ} dr²  +  D_A(r)² dΩ²
```

| | |
|--|--|
| **Redshift (static observers)** | `1 + z = e^{φ_source − φ_observer}` — simple, monotone in Δφ; **never an oscillating law** |
| **φ = 0** | Chart normalization for *this* observer — **not** a preferred cosmic center |
| **What R1–R3 do *not* fix** | Profile φ(r), free vs gauge-fixed D_A, dynamics, matter |

**Slice used below:** static, spherical, diagonal = **FREE first slice** (like Schwarzschild symmetry in GR).

---

## 2. Operators forced by the metric

### Measure (CAS)

```text
√(−g) = c D_A² sin θ     — independent of φ
```

Dilation factors cancel. Volume element on this family is φ-blind.

### R1 kinetic for φ (CAS)

Shift φ → φ+const must not invent a preferred zero. The density

```text
√(−g) · e^{2φ} g^{rr} (φ')²  =  √(−g) (φ')²
```

is **φ-free** (only φ'). Reduced radial kinetic:

```text
L_kin = (Z/2) D_A² (φ')²
```

**Z** = overall kinetic normalization (**FREE fork** — see §5).

### Angular geometry (CAS)

Split longitudinal (t,r) from transverse 2-geometry.

```text
R^{(2)} = 2 / D_A²                              (intrinsic)
𝒦     = −2 e^{−2φ} (D_A' / D_A)²               (extrinsic invariant K_AB K^{AB} − K²)
```

**Flat test (elegance):** flat space must cost nothing angularly.

| Case | Result |
|------|--------|
| φ=0, D_A=r | `R^{(2)} + 𝒦 = 0` |
| D_A=r, any φ | `R^{(2)} + e^{2φ} 𝒦 = 0` |

Off-round: uniqueness forces `𝒦 = K_AB K^{AB}−K²` (no free extra K²) — banked in geometric-action results.

### Why not 4D Einstein–Hilbert?

On this reciprocal family with **D_A = r**:

```text
√(−g) R  =  pure boundary term     (CAS: r²R = d/dr[…])
```

**Empty bulk for φ.** Importing “vacuum = Einstein” was the Principle-7 scar.  
Native bulk lives in **R1 kinetic + angular mismatch**, not bare 4D EH.

(With free D_A inside full EH the story can re-bulk — that is a packaging fork. The **simple native path** is the geometric action below.)

---

## 3. The native action (UDT’s EH analog)

```text
S = ∫ c √h [  (Z/2) (φ')²  +  R^{(2)}[h]  +  W(φ)·𝒦  +  L_m  ]
```

| Piece | Role |
|-------|------|
| `(Z/2)(φ')²` | R1-clean kinetic for dilation |
| `R^{(2)}` | intrinsic angular curvature |
| `W·𝒦` | extrinsic angular mismatch (the only depth-weighted bulk piece) |
| `L_m` | matter (with dilation — §6) |

**One action. Two honest free forks (W and Z). Everything else is solutions.**

---

## 4. Field equations (vacuum, round)

Among local pieces, **only 𝒦** transforms nontrivially under depth shift φ → φ+λ:  
`𝒦 → e^{−2λ} 𝒦`. So either compensate it or leave it:

### Weight W = e^{2φ} — shift exact (compensated)

Angular sector cancels for D_A=r; φ decouples from transverse:

```text
d/dr( Z D_A² φ' ) = 0
```

Frozen D_A=r:

```text
(r² φ')' = 0   ⇒   φ = φ_∞ − q/r     (Coulomb / scale-free)
```

### Weight W = 1 — shift broken by angular sector (uncompensated)

```text
d/dr( Z D_A² φ' ) = 4 e^{−2φ} (D_A')²
```

Frozen D_A=r:

```text
Z (r² φ')' = 4 e^{−2φ}
```

**Framing (binding for macro):** do **not** brand these as two cosmologies (“G vs P universes”).  
They are **one switch** on one geometric weight. Which is physical is a **principle question** (is depth-shift an exact bulk symmetry, or broken by angular/matter structure?). Matter-sourcing of φ needs a nonvanishing right-hand side or a non-φ-blind L_m — that is output of the setup, not a pre-chosen branch name.

---

## 5. FREE ledger (short, honest)

| Item | Tag |
|------|-----|
| R1–R3 + metric form | THEORY / canon |
| Static spherical diagonal | FREE first slice |
| D_A free vs D_A=r gauge | FREE / gauge |
| **W ∈ {e^{2φ}, 1}** | **Working set (2026-07-08 EOD):** **fallback C active** — \(W=e^{2φ}\) vacuum + matter sources φ (`macro_FE_LOCKED_C.md`). B parked after O1–O6 (`macro_FE_LOCKED_W_uncompensated.md`). |
| **Z (kinetic norm)** | **PINNED:** free overall constant until observation (no Route-B mixing for now) |
| Continuum L_m | OPEN — prefer dilated / native; φ-blind dust is incomplete |
| Edge / x_max | OPEN — ask only after W + packaging fixed |
| 4D EH as bulk engine on D_A=r | **Rejected** (empty) |

---

## 6. Matter (minimal)

Static energy feels dilation: metric factors on T_{tt} (e.g. weight ∼ e^{−2φ}).

- **Do not** treat φ-blind continuum dust as “the” macro theory.  
- Prefer **channel-corrected geometric matter** for microphysics when that sector is live.  
- Macro source of φ is **Q1** (open): uncompensated W, and/or dilated L_m, and/or free D_A dynamics — **solver completeness first**, not a new mechanism.

---

## 7. What this core already settles

| Claim | Status |
|-------|--------|
| Redshift from Δφ | Metric identity |
| No preferred cosmic center | φ=0 is local chart |
| Vacuum can be Coulomb (compensated W) | Yes |
| Angular sector can source φ (uncompensated W) | Yes |
| Soft numerical “closure scores” | **Unnecessary** once equations are primary |
| G/P as two universes | **Harmful framing** — drop for macro |
| Bare Einstein vacuum as UDT vacuum | **Wrong** on this family |

---

## 8. GR-like elegance checklist

| GR | UDT (this core) |
|----|------------------|
| Metric from equivalence / geometry | Metric from dilation + reciprocity |
| One action (EH) | One action (kinetic + angular mismatch + W·𝒦 + matter) |
| Vacuum structured | Vacuum: Coulomb or angular-sourced φ equation |
| Matter T_{μν} | Matter with **dilation weights** |
| No preferred frame | No preferred φ=0 location; relational redshift |

**Complexity belongs in solutions, not in a stack of stand-in mechanisms.**

---

## 9. Follow-on that becomes unnecessary (if this core is held)

- Soft S2 “everything matches” closure scores  
- φ-blind dust mass tournaments as theory  
- Treating G/P as two cosmologies  
- Importing Einstein vacuum as UDT vacuum  
- Building particles on an unstated macro background  
- Edge-shooting under packaging already proven empty (HE1-style dead ends)

**What remains necessary:**

1. **Which W?** — principle only (when is shift exact?).  
2. **Z / mixing** — if spectrum or bulk demands Route B.  
3. **Solutions** of these equations (with free D_A and honest L_m).  
4. **Native matter** when microphysics needs it.

---

## 10. One-line summary

**From the metric: reciprocal dilation + R1 kinetic + angular mismatch R^{(2)}+W·𝒦 (+ dilated matter). 4D EH is not the bulk engine. Redshift is e^{Δφ}. Hold this core; most recent macro complexity was optional noise around it.**

---

## Provenance

| Check | Script | Result |
|-------|--------|--------|
| Measure, kinetic, 𝒦, flat cancel, both ELs, Coulomb, EH boundary, redshift | `macro_native_FE_rederive_clean.py` | **21/21 PASS** (2026-07-08) |
| Founding EH-empty + Coulomb + Branch-P frozen | `verify_native_fieldeq.py` | banked |
| Geometric action / 𝒦 bulk / uniqueness | `verify_native_geo_action.py`, off-round uniqueness | banked |
| Full geometric-action writeup | `native_geometric_action_results.md` | banked |
