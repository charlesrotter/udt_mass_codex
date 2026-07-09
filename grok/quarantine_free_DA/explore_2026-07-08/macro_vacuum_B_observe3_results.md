# OBSERVE-3 — Survival window (vacuum B throat family)

**Date:** 2026-07-08  
**Mode:** OBSERVE.  
**Script / data:** `macro_vacuum_B_observe3.py`, `macro_vacuum_B_observe3_data.json`  
**Prior:** O1 (polar blocked), O2 (throat = local max of D).  
**Status:** PROVISIONAL characterization tile.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Vacuum B, throat seed \(D'_*=0\), \(\phi_*=0\), \(r_*=1\) | as locked + FREE chart |
| **SURVIVE** = \(D > 0\) on whole path for \(r \in [0.05, 5]\) both sides | FREE window definition (method) |
| Scan \(Z, u_*=\phi'_*, D_*\) | FREE, not fit to data |
| Observing or targeting? | **Observing** |

---

## Definitions

| Label | Meaning |
|-------|---------|
| **SURVIVE** | Both out to \(r=5\) and in to \(r=0.05\) without \(D\to 0\) |
| **PINCH_OUT** | Hits \(D\sim 0\) on the outward side only |
| **PINCH_IN** | (not seen in this grid) |
| \(u_{\mathrm{crit}}^+(Z)\) | Largest \(+u_*\) with SURVIVE on that window (bisection) |

---

## Main findings

### 1. Failure mode is almost only outward pinch

In the grid: every non-SURVIVE point was **PINCH_OUT**. No PINCH_IN in the scanned box.

**Deep inward** (to \(r=10^{-4}\), mild \(u_*\), \(D_*=1\)): **all** tested cases reached \(r=10^{-4}\) with \(D_{\min}\) still \(\approx D_*\) (relative drop ≲ few percent).  

**Plain:** under throat seeds, the dangerous direction is **outward** (away from the bulge); inward is soft in this vacuum family.

### 2. \(u_{\mathrm{crit}}\) independent of \(D_*\)

For each fixed \(Z\), bisection gave **identical** \(u_{\mathrm{crit}}^+\) at \(D_* \in \{0.5, 1, 2\}\).

**Why (theory, not fit):** the system is homogeneous under \(D \to \lambda D\):

- FE-φ and FE-D both scale so \(\phi(r)\) is unchanged and \(D/D_*\) obeys a \(D_*\)-free equation.  
- Relative pinch is set by \((Z, u_*, \phi)\), not absolute sphere size.

### 3. Critical slope vs \(Z\) (window \([0.05, 5]\))

| \(Z\) | \(u_{\mathrm{crit}}^+\) | \(u_c\sqrt{Z}\) |
|------|-------------------------|-----------------|
| 0.5 | 0.2640 | 0.187 |
| 1 | 0.2196 | 0.220 |
| 2 | 0.1797 | 0.254 |
| 4 | 0.1446 | 0.289 |
| 8 | 0.1144 | 0.323 |

- Larger \(Z\) → **smaller** allowed \(|\phi'|\) at throat before outward pinch (matches \(D''_* \propto -Z u^2\)).  
- \(u_c\sqrt{Z}\) is **not** constant (slow rise with \(Z\)) — no claim of a simple closed scaling law yet.

### 4. Longer outward window shrinks the band

Same throat, window \([0.05, 10]\) instead of 5:

| \(Z\) | \(u_{\mathrm{crit}}^+\) (to 5) | (to 10) |
|------|-------------------------------|---------|
| 1 | 0.220 | 0.098 |
| 4 | 0.145 | 0.064 |
| 8 | 0.114 | 0.051 |

**Plain:** “survive forever outward” is stricter than “survive to a finite chart radius.” Finite-window survival is the honest report; asymptotic outer existence is a separate open question.

### 5. Sign asymmetry in \(u_*\)

On the grid (all \(Z\), all \(D_*\)):

| \(u_*\) | SURVIVE fraction |
|---------|------------------|
| \(+0.2\) | 6/15 |
| \(-0.2\) | **15/15** |
| \(+0.3,+0.5\) | 0/15 |
| \(0\) … \(0.1\) | 15/15 |

**Scoped:** with \(\phi_*=0\), **positive** \(\phi'\) (φ increasing outward) pinches more easily than **negative** \(\phi'\). Comes from \(e^{\pm 2\phi}\) factors — not a coding bug (flux mono still held in O2).

### 6. Compact matrix \(D_*=1\), window \([0.05,5]\)

```text
Z\u      0    0.05   0.10   0.15   0.20   0.30   0.50
0.5      S     S      S      S      S      Po     Po
1        S     S      S      S      S      Po     Po
2        S     S      S      S      Po     Po     Po
4        S     S      S      Po     Po     Po     Po
8        S     S      S      Po     Po     Po     Po
```

S = SURVIVE, Po = PINCH_OUT.

---

## What this does *not* say

- Not a cosmology fit or Z determination.  
- Not “edge of the universe” — only ODE survival on a chart interval.  
- Not that inward is always safe for all ICs (only throat family + tested range).  
- Not activation of fallback C — vacuum B still has an open **SURVIVE** set of positive measure in \((Z,u_*)\).  
- Not that sources are required.

---

## Running vacuum map (O1–O3)

| Tile | Result (scoped) |
|------|-----------------|
| O1 | Smooth polar origin blocked |
| O2 | Throat: \(D''_*\le 0\); nonflat → bulge; fluxes mono |
| O3 | Finite survival band in \(u_*(Z)\); fail = outward pinch; independent of \(D_*\); ±u asymmetric; deep inward mild |

---

## Incremental next (when ready)

1. **OBSERVE-4:** nondimensional reduction — write ODE for \(d=\ln D\), \(\phi\) only; exhibit \(D_*\)-independence cleanly; optional first integral hunt.  
2. Outer asymptotics: for SURVIVE seeds, does \(D\to const>0\), \(D\to 0\) slowly, or \(\phi\) floor? (longer runs / analytic)  
3. Still later: \(L_m\).

Recommend **4** (cheap analytic tidy) then outer asymptotics before sources.

---

## Plain summary

For throat seeds in vacuum B, there is a real **band of mild φ-slopes** that keep sphere size positive over a chosen radial window; steeper slopes **pinch off outward**. That critical slope depends on **Z** but **not** on how large the throat is. Going **inward** is gentle in the cases we tried. Negative φ-slope at the throat is more forgiving than positive in this chart. Still pure vacuum — no matter, no sky scores.
