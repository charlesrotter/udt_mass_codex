# WP1 RESULT — Path B + dust probe: Euler–Lagrange (no solve)

**Date:** 2026-07-08 · **Status: PROVISIONAL CAS** (equations only).  
**MAP:** `macro_native_matter_edge_MAP.md` (Charles go on MAP-first recommendation).  
**Script:** `macro_pathB_dust_EL.py`  
**Gravity:** Path B — free `D_A` + EH + R1 kinetic.  
**Matter:** FREE temporary static dust probe, **α=0** (no explicit φ in L_m).

---

## 1. Premises

| Item | Tag |
|------|-----|
| Path B vacuum gravity | CHOSE program pin |
| Static spherical | FREE ansatz |
| `L_m = −ρ(r) D_A²` reduced | **FREE temporary probe** — not UDT-fundamental |
| α=0 (no `e^{αφ}` in L_m) | Default this WP |
| Cell seals / Gaussian habit as theory | OUT |
| Solve / edge shoot | **Not in WP1** |

---

## 2. Equations

### Gravity (unchanged vacuum Path B)

```text
L_g = D_A² R[φ,D_A] + (Z/2) D_A² (φ')²
```

### Dust probe

```text
L_m = −ρ(r) D_A²
L   = L_g + L_m
```

### EL (CAS)

**EL_φ — identical to vacuum Path B:**

```text
−Z D_A² φ'' − 2 Z D_A D_A' φ' + 4 D_A e^{−2φ} D_A'' = 0
```

equivalently

```text
d/dr(Z D_A² φ') = 4 D_A e^{−2φ} D_A''
```

**Matter does not appear in EL_φ** under this L_m (φ-blind reduced density).

**EL_D — vacuum Path B + dust:**

```text
EL_D[vac] − 2 ρ D_A = 0
```

(with the same vacuum differential expression as in Path B characterize; matter shifts the `D_A` equation by `−2ρ D_A` in the reduced convention of the script).

### Conservation note (static dust)

Pressureless static dust: hydrostatic equation is trivial (`p=0`).  
**Continuity does not fix ρ(r)** for static flow.  

So in the probe, either:

- **ρ(r) FREE profile** (scan amount/shape — labeled FREE), or  
- **ρ on-shell** from Einstein/`EL` algebraic constraint if one equation is used to define ρ.

Tag whichever is used in WP2.

---

## 3. Structural implication (why this probe can still matter)

Dust does **not** directly source φ. It only **reshapes `D_A`**, and φ feels that through **`D_A''` in EL_φ** (EH channel).

So WP2 is really testing:

> Can a φ-blind density, by bending free `D_A`, break the vacuum **φ∼2 ceiling** or create **E-turn / E-φ∞**?

If **no** across a wide FREE ρ scan: scoped null on **this dust probe**, not on all matter.

---

## 4. α≠0 contrast (not default)

```text
L_m = −ρ D_A² e^{α φ}  ⇒  EL_φ gets  −α ρ D_A² e^{α φ}
```

Only for a **separate tagged fork**. Default WP2 stays **α=0**.

---

## 5. Next (WP2)

Bounded observe on Path B + ρ:

1. System: EL_φ, EL_D with ρ prescribed FREE family **or** ρ from constraint.  
2. Diagnostics: max φ, E-turn, candidate E-φ∞, mass proxy.  
3. Vacuum seeds as control (ρ=0 ⇒ recover ceiling ∼2).  
4. No SNe.

---

## 6. One-line

**WP1: α=0 dust on Path B only enters EL_D (−2ρ D_A); EL_φ stays pure geometry/EH — matter affects φ only by bending D_A.**
