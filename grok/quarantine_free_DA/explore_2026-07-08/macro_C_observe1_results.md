# OBSERVE-C1 — Fallback C (compensated vacuum + dilated matter)

**Date:** 2026-07-08  
**Lock:** `macro_FE_LOCKED_C.md`  
**Script / data:** `macro_C_observe1.py`, `macro_C_observe1_data.json`  
**B:** parked after O1–O6.  
**Status:** PROVISIONAL first tile on C. OBSERVE, not sky-fit.

---

## Premise ledger

| Item | Tag |
|------|-----|
| \(W=e^{2\phi}\) vacuum | CHOSE (C) |
| Dilated \(L_m=-\rho D^2 e^{-2\phi}\) | CHOSE probe |
| Z=1 representative | FREE |
| Throat / expand / near-center seeds | FREE IVPs |
| Observing or targeting? | **Observing** |

---

## Equations (reminder)

**Vacuum:** \((Z D^2\phi')'=0\), \(D''=-(Z/4)D(\phi')^2\)  
**Dilated matter:** \((Z D^2\phi')'=2\rho D^2 e^{-2\phi}\), \(D''=-(Z/4)D(\phi')^2+\frac12\rho D e^{-2\phi}\)

CAS: Coulomb on frozen \(D=r\) ok; numeric \(G=D^2\phi'\) conserved in vacuum to \(\sim10^{-11}\).

---

## C vacuum — what is there

### Conserved flux

\(G = D^2 \phi'\) is **constant** along vacuum solutions (exact from FE).  
No angular RHS on φ — that is the C content.

### Throat family (\(D'=0\), \(D>0\))

At throat: \(D'' = -(Z/4) D (\phi')^2 \le 0\).

| Seed | Fate (outward) |
|------|----------------|
| \(u_*=0\) | Exact flat forever |
| \(u_* \neq 0\) (either sign) | **D decreases and pinches** at finite r; \|G\| fixed |

**Unlike B:** there is **no soft/hard split by sign of φ′**. Vacuum C is **even in φ′** (depends on \((\phi')^2\)). Both “directions” of slope at a bulge are hard in the sense of eventual pinch under pure throat IVP.

Inward short leg (\(r\to0.05\)) still mild (D barely drops) before a long outward pinch on the other side — not a two-mood φ-arrow like B.

### Expanding seed (not a throat)

Example: \(D'=0.3\), \(u=0.05\), \(D=1\): **reaches r=30**, D grows (~10), φ mild, G conserved.  

**Plain:** C vacuum can look “open and growing” if you don’t sit on a pure bulge with D′=0 and nonzero φ′.

### Near-center seed \(D\sim 0.2\), \(D'\sim1\), \(u=0\)

Vacuum: D grows linearly-ish (φ stays 0, G=0) — pure expanding spheres, no dilation drive.

---

## C + dilated matter — first look

### Matter on throat (ρ gaussian at bulge)

Even \(u_*=0\): matter **turns on G** (\(G\) rises from 0) and solutions still **pinch** outward; more ρ → earlier pinch.  
Does **not** turn the throat into a calm eternal exterior in this IVP class.

### Matter on expanding/near-center seed (\(u_0=0\), \(D'>0\))

| ρ₀ | Fate to r=30 |
|----|----------------|
| 0 | ok, φ=0, D grows |
| 0.5–20 | **ok**, D grows, **φ rises**, G grows then (in window) remains positive |

**Plain:** here matter does its C job — **sources φ** while spheres keep opening. No pinch in the scanned window. This is the first C sector that looks less like B’s cursed bulge and more like “stuff makes dilation, size can grow.”

### φ-blind control (throat, u=0, ρ=3)

D inflates, **φ stays 0** (no direct source) — control behaves as expected; not theory.

---

## B vs C (honest)

| | B (parked) | C (this tile) |
|--|------------|----------------|
| Vacuum φ from angular | yes | **no** |
| Vacuum throat ±φ′ | hard vs soft | **both pinch** (φ′-even) |
| Conserved G in vacuum | no | **yes** |
| Dilated matter on throat | worsens pinch | still pinches |
| Expanding + matter | (not focus) | **φ builds, D can grow** |

C did **not** magically become the night sky. It **did** remove B’s angular self-drive of φ and put the load on matter — as designed. Weird throat vacuum remains; **expanding + matter** is the more promising C corner so far.

---

## What this does *not* say

- Not Mozart / not SNe  
- Not that C is “right”  
- Not that throats are useless (BVP/matching untested)  
- Not Z fixed  

---

## Incremental next (when ready)

1. **C2:** map expanding / exterior family with compact support ρ (matter ball → vacuum exterior, match G=const outside).  
2. Coulomb exterior analytic + numeric match.  
3. Still no sky scoreboard until a clean exterior exists.

Recommend **C2** (matter ball → vacuum out) — the natural C cosmology sketch.

---

## Plain summary

We flipped the switch: **empty space no longer lets sphere-bending generate φ**; only matter does.  

Empty C still kills a pure “bulge with a slope” by pinching (both ways).  
But if spheres are **already opening** and you put dilated matter in, φ **turns on** and the run can stay open in our window — that is C doing something B’s vacuum throat never did cleanly.  

Not the universe yet. Clearer division of labor: **geometry holds the stage; matter plays the dilation.**
