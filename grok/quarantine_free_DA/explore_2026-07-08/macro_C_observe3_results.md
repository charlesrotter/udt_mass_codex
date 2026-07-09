# OBSERVE-C3 — Seed scan (C ball → exterior)

**Date:** 2026-07-08  
**Lock:** `macro_FE_LOCKED_C.md`  
**Fixed ball:** \(Z=1\), \(\rho_0=5\), \(R_m=2\) (C2 reference)  
**Script / data:** `macro_C_observe3.py`, `macro_C_observe3_data.json`  
**Status:** PROVISIONAL. OBSERVE, not sky-fit.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Ball fixed | FREE reference from C2 |
| Vary \(D_0,v_0,u_0\) at \(r_0=0.05\) | FREE seeds |
| Exterior classes | GROW / FALL / TURN / PLATEAU / PINCH / NO_EXT |
| Observing or targeting? | **Observing** |

---

## Structural fact (vacuum exterior)

\[
D'' = -\frac{Z}{4}\frac{G^2}{D^3} \le 0 \quad (G = D^2\phi'\ \text{const})
\]

So in any vacuum exterior with \(G \neq 0\):

- **\(D'\) is strictly decreasing**  
- **True long-term plateau** (\(D'=0\), \(D''=0\)) requires **\(G=0\)** (no exterior charge)  
- If \(v(R_m)>0\): either stays positive a long time (**GROW** in finite window) or eventually crosses 0 (**TURN** → then **FALL** → possible pinch)  
- If \(v(R_m)<0\): **FALL** immediately  

This is not a numeric accident — it is the C vacuum ODE.

---

## Seed scan results

### (A) Polar-like \(D_0=r_0=0.05\), vary \(v_0\), \(u_0=0\)

| \(v_0\) | Class (to r~60–100) |
|---------|---------------------|
| ≤ 0 | NO_EXT / PINCH (dies before or at matter edge) |
| 0.1 – 2.5 | **GROW** throughout window; \(v(R_m)>0\) tracks \(v_0\) |

C2 baseline \(v_0=1\) sits deep in **GROW**.  
No PLATEAU. No TURN in this thin-core family up to \(r=100\).

### (B) \(v_0=1\), vary \(D_0\)

| \(D_0\) | Class |
|---------|--------|
| 0.02 – 0.5 | GROW |
| 1.0 | **TURN** then pinch (exterior \(v\) crosses 0) |

Fatter core at same \(v_0\) → larger \(G(R_m)\), smaller \(v(R_m)\) → easier for vacuum \(D''<0\) to kill expansion.

### (C) Vary \(u_0\) at C2 seed

Mild: all **GROW**; \(G(R_m)\) almost unchanged. Central φ-slope is **not** the main exterior driver once the ball has loaded \(G\).

### (D) Fat / slow-open cores

Many **NO_EXT** (collapse inside the ball) if \(v_0\) too small.  
Some **FALL** just after \(R_m\) with \(v(R_m)<0\).

### (E) Large \(u_0\)

Still **GROW** for open polar seeds — does not flip exterior class.

### (F) \(D_0=1\), \(v_0\) scan to \(r=100\) — the interesting window

| \(v_0\) | Class | Notes |
|---------|--------|--------|
| 0 – 0.2 | NO_EXT | die inside |
| 0.4 – 0.6 | FALL | \(v(R_m)<0\) |
| 0.8 – 1.2 | **TURN** | \(v(R_m)>0\) then crosses 0; later pinch |
| ≥ 1.4 | GROW | expansion survives window |

**Plain:** for a fat enough core there is a **finite band** of opening rates that produce an exterior **turnaround** (max of \(D\) outside the ball), and a higher band that keeps growing in the chart window.

---

## Answer to C2’s question

> Can exterior \(D\) level off, or is growth baked in?

| Claim | Status |
|-------|--------|
| Growth baked into C2 seed only | **Mostly yes** for thin polar + large \(v_0\) |
| Plateau of \(D\) with \(G\neq0\) | **Forbidden** by vacuum ODE (strict) |
| Exterior **turn** (max \(D\)) | **Yes**, in a seed band (fat core + intermediate \(v_0\)) |
| After turn | FALL → typically pinch (finite chart life of that exterior) |

So the honest exterior zoo under C is:

```text
G = 0          →  can be boring flat/expanding without dilation
G ≠ 0, v_Rm≫0  →  GROW (long) 
G ≠ 0, v_Rm≳0  →  TURN then FALL (and often pinch)
G ≠ 0, v_Rm<0  →  FALL
v too small in ball → die before exterior
```

No Mozart static shell with nonzero exterior charge under this free-\(D\) C vacuum law.

---

## What this does *not* say

- Not that growing \(D\) is wrong physics (could be chart)  
- Not that TURN exteriors are particles  
- Not a fit for Z or ρ  
- Not that pressure / dynamics / other \(L_m\) couldn’t change \(D''\) law  

---

## Incremental next (when ready)

1. **C4:** analytic vacuum exterior quadrature — time-to-turn as function of \((G, D_m, v_m)\).  
2. **C5:** outer BC / finite domain (mirror, cutoff) — different question than infinite IVP.  
3. Ponder with Charles: is free-\(D\) C exterior *supposed* to grow, or is a different continuum needed for static areal radius?

Recommend **C4** (cheap, exact structure) or **pause/ponder** — solution space of infinite IVP is now fairly mapped.

---

## Plain summary

Outside the matter ball, C’s vacuum rule is harsh and simple: **if there’s any dilation charge \(G\), the sphere’s expansion rate can only go down.**  
So you either open fast enough that size keeps growing for a long way, or expansion dies, size turns over, and that branch often pinches.  
A true frozen size with nonzero charge is not on the menu of these equations.  
The C2 “always grow” picture was largely the polar open seed; other seeds show **turn** and **fall** too — still not a calm static cosmos, but a clearer map of what C allows.
