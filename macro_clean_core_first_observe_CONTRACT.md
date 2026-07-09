# CONTRACT — clean-core macro first observe (Q4/Q5 pins + gates)

**Date:** 2026-07-08 · **Status: PRE-REGISTERED before compute** (this file).  
**Posture:** `macro_Q1_source_posture.md` (Charles-accepted: Q1=(a) primary).  
**MAP:** `macro_universe_clean_core_MAP.md`.  
**Mode:** finish planning pins → DERIVE EL → OBSERVE (characterize, do not target SNe/cosine).

---

## 0. Goal of this first observe

**Existence / structure only:** on the clean core with Q1 posture (a),

> does a static, spherically symmetric solution exist with a **regular center** and **nontrivial redshift** (`φ` not constant)?

Not: fit Pantheon, reproduce cosine, pick critical matter amount for SNe.

---

## 1. Final planning pins (minimal, tagged)

| ID | Choice | Tag | Why |
|----|--------|-----|-----|
| Q1 | (a) indirect geometric; (c) vacuum edge ref; (b) parked | POSTURE (Charles) | already accepted |
| Q2 | uncompensated `𝒦` when matter-on; G as vacuum control | POSTURE | matter→φ only on P-type route |
| Q3 | `h_AB = D_A(r)² Ω_AB` (**free** `D_A`, not frozen to `r`) | FREE ansatz (round) | free radius function; full non-round later |
| **Q4** | **Minimal φ-blind continuum stand-in:** `L_m = −ρ(r)` with **prescribed** non-negative density profile (family below). Not winding. Not claimed as true macro matter. | **FREE temporary stand-in** | cheapest probe of channel (a); native `L_m` still open |
| **Q5** | Outer: integrate to finite `r_max` or until breakdown; **no** mirror seal / H=0 cell BC. Report edge behavior. | FREE box | avoid cell contamination |
| Q6 | Target regularity: `D_A(0)=0`, `D_A'(0)=1`, `φ` finite, `φ'` finite (standard spherical center). Also record alternatives if that class is empty. | THEORY-motivated target | frame-relation observer at center |
| Q7 | Depth 1101 / SNe / cosine | **OUT** as inputs | characterize only |
| Z_φ | `= 1` | FREE convention | scale-degenerate |
| Symmetry | static, spherical | FREE ansatz | scoped slice |

### Q4 density family (prescribed, FREE)

```
ρ(r) = ρ0 * exp(−(r/r_c)²)     # Gaussian core, or
ρ(r) = ρ0 * Θ(r_c − r)         # top-hat (optional cross-check)
```

Scan `ρ0 ≥ 0`, `r_c > 0` as FREE labels. `ρ0 = 0` = vacuum control.  
**Honesty:** prescribed `ρ` is not a dynamical native sector; it only tests whether a φ-blind bulk density can regularize / source via geometry. If the φ equation never sees `ρ` (true when `δS_m/δφ=0`), that fact is itself a result.

---

## 2. Derive package (must pass before banking numerics)

From action (angles integrated, `c=1`, drop overall `4π`):

```
S = ∫ dr [ (Z/2) D_A² φ'² + 2 + D_A² 𝒦_branch + D_A² L_m ]
```

with round free `D_A`:
```
𝒦_uncompensated = −2 e^{−2φ} (D_A'/D_A)²     # P-type
𝒦_compensated   = −2 (D_A'/D_A)²               # G-type (e^{2φ}𝒦)
L_m = −ρ(r)                                     # Q4 stand-in
```

**CAS-verify:**

1. Recover vacuum G EOM: `Z D_A² φ' = q`, `D_A'' = −q²/(4 Z D_A³)` (matches `sne_native_background_n2.py`).  
2. Derive vacuum P EOM for free `D_A`.  
3. Derive P + `L_m=−ρ` EOM; confirm whether `ρ` enters the **φ** equation.  
4. Series / limiting analysis at a regular center `D_A∼r`.

---

## 3. Observe package (bounded)

| Control | Cap |
|---------|-----|
| Grid / IVP | `solve_ivp` or collocation; r from `ε` to `r_max≤20` (scale-free units) |
| Scans | small discrete set of `(ρ0, r_c)`, plus `ρ0=0` |
| Time | single process; fail soft if stiff |
| Diagnostics | max `|φ'|`, whether `φ` finite at center, `D_A` shape, residual of EOM |

**Report classes (pre-named, no look-elsewhere on SNe):**

- **C0** vacuum G: reproduce known singular-center / off-center redshift tension  
- **C1** vacuum P free-`D_A`: center structure  
- **C2** P + φ-blind `ρ`: does matter change the φ-center structure?  
- **C3** any configuration with regular center + nontrivial Δφ in the box?

---

## 4. Acceptance (characterize, do not filter)

- A solution is **recorded** if the integrator is consistent (EOM residual small where defined).  
- **Empty C3** is a first-class result (solver/structure finding), not a failure to “make cosmology.”  
- No merit gate on cosine, SNe RMS, or critical ρ0.

---

## 5. Outputs (parallel docs only)

| File | Role |
|------|------|
| `macro_clean_core_derive_observe.py` | CAS + numeric |
| `macro_clean_core_first_observe_results.md` | premises + what emerged |
| this CONTRACT | pre-registration |

No edit of `LIVE.md` / `external.md` / older MAPs unless Charles asks.
