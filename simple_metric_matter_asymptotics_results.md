# Simple metric + dilated matter (matter couples to φ)


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | see body — retrofit default LEAD |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | see body |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | see body / associated `*.py` if any |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body of this document | full ledger in sections | mixed — re-read body | Y |

### What is NOT claimed

- Physics canon (Charles only). Hygiene grade ≠ nature proof.
- Claims wider than **Slice scope** above.

### Do not build on (if any)

- Anything tagged CHOSE/explore in the body without re-stating premises.

---

**Date:** 2026-07-08 · **Mode: OBSERVE**  
**Foundation:** `SIMPLE_METRIC_MACRO.md`  
**Script / data:** `simple_metric_matter_asymptotics.py`, `simple_metric_matter_asymptotics_data.json`  
**Frame:** `UDT_ELEGANT_FRAME.md`  
**Status:** PROVISIONAL. Compact \(\rho\) is a FREE probe profile — not unique continuum theory.

---

## Setup (simple metric only)

\[
ds^2 = -e^{-2\phi}c^2 dt^2 + e^{2\phi} dr^2 + r^2 d\Omega^2
\]

**Dilated continuum** (couples to \(\phi\)):

\[
L_m = -\rho(r)\, r^2\, e^{-2\phi}
\]

| \(W\) | Field equation |
|-------|----------------|
| \(e^{2\phi}\) | \(Z(r^2\phi')' = 2\rho r^2 e^{-2\phi}\) |
| \(1\) | \(Z(r^2\phi')' = 4e^{-2\phi} + 2\rho r^2 e^{-2\phi}\) |

\(\rho\): compact ball of radius \(R_m\) (FREE shape). Exterior \(\rho=0\).

---

## What matter does (observed)

### \(W=e^{2\phi}\) (compensated geometry + dilated dust)

Inside the ball, matter **sources** \(Q:=r^2\phi'\):

| \(\rho_0\) (sample \(R_m=2\)) | \(Q(R_m)\) | \(\phi(R_m)\) | \(\phi_\infty\approx\phi_{R_m}+Q/R_m\) |
|------------------------------|------------|---------------|----------------------------------------|
| 0 | 0 | 0 | 0 |
| 0.5 | 1.14 | 0.45 | ~1.01 |
| 1 | 1.63 | 0.74 | ~1.54 |
| 5 | 2.29 | 1.72 | ~2.86 |
| 10 | 2.25 | 2.20 | ~3.31 |

Exterior vacuum: **\(Q\) conserved** (drift \(\sim 10^{-8}\)–\(10^{-6}\)).

\[
\phi(r)=\phi_{R_m}+Q\Bigl(\frac{1}{R_m}-\frac{1}{r}\Bigr)
\quad\Rightarrow\quad
\phi\to\phi_\infty=\phi_{R_m}+\frac{Q}{R_m}
\]

| Probe | Result |
|-------|--------|
| Matter ↔ φ coupling | **YES** — more \(\rho\) generally deeper \(\phi\), larger exterior charge \(Q\) |
| Redshift out | **YES** |
| \(z_{\max}\) | \(e^{\phi_\infty}-1\) **finite** (set by ball) |
| Hard barrier | **NO** — \(\ell\) grows ~linearly with \(r_{\max}\) (open exterior) |

**Plain:** Dilated matter **turns on** the Coulomb exterior (vacuum had \(Q=0\) if you start flat). Far away, depth **levels** to a finite \(\phi_\infty\) fixed by how much matter loaded \(Q\). Not an infinite wall.

### \(W=1\) (uncompensated + dilated dust)

Geometric source already active with \(\rho=0\); matter **adds** to \(Q\) and deepens \(\phi\).

Exterior still **open**: \(\phi\) rises toward a higher plateau-ish value; \(\ell\) grows with window. **No hard barrier** in the scanned set.

---

## Scoreboard update (simple metric)

| Content | Redshift out | Hard barrier | Role of dilated matter |
|---------|--------------|--------------|-------------------------|
| Vacuum \(W=e^{2\phi}\) | only if \(q\neq 0\) | no | — |
| Vacuum \(W=1\) | yes | no | — |
| **Matter ball + \(W=e^{2\phi}\)** | **yes** (from \(\rho\)) | **no** | sets exterior \(Q\) and \(\phi_\infty\) |
| **Matter ball + \(W=1\)** | yes | no | deepens / loads on top of geometric source |

---

## What this does *not* say

- Not a unique \(\rho\) law (profile FREE).  
- Not SNe / closure / BB.  
- Not free \(D_A\).  
- Not “matter fails forever” — only **this** compact dilated dust on the simple metric does not create a hard far-reach barrier; it creates a **finite** exterior depth scale.

---

## Next options (still simple metric)

1. **Ponder:** Is finite \(\phi_\infty\) from matter the intended “depth of the sky,” with edge elsewhere (optics / horizon definition), vs hard \(\ell<\infty\)?  
2. **Different \(\rho\) support** (not compact) — only if principle-motivated, not to force a barrier.  
3. **Relational / observer** reading of Coulomb exterior (shell theorem track already in corpus).  

No invented edge operator.

---

## Plain summary

On the simple metric, **dilated matter does couple to \(\phi\)**: a ball of stuff loads a conserved exterior charge and you look out into a **Coulomb-like** dilation that **redshifts then caps** at a finite max depth set by the matter. Proper distance still runs to infinity. So matter **sources the sky’s depth**; it does **not**, in these runs, build an impassable dilation wall by itself.
