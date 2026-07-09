# Side excursion — legacy cubic + Layer A + dimensional fix together?


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | legacy cubic; N=1580 full cov |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | LCDM ref only |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **DEMO** |
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

**Date:** 2026-07-09 · **Mode: OBSERVE (side)**  
**Question (Charles):** Take the legacy distance profile (good half-light fit), apply full light count **and** the dimensional PATH/AREAL-style fix — does the old fit come back?  
**Status:** Answered. **No** (except by algebra that undoes the light fix).

---

## Setup

Legacy profile: locked cubic \(\phi(r)\), invert \(1+z=e^{\phi(r)}\) → \(r(z)\).  
Data: Pantheon+ full STAT+SYS, same cut; **1 offset only**.

| Label | Rule | \(D_A\) | χ²/dof | RMS |
|-------|------|---------|-------:|----:|
| **LEGACY** | half light | \(r\) | **0.94** | 0.164 |
| Layer A only | full light | \(r\) | **4.56** | 0.471 |
| Algebraic undo | full light | \(r/(1+z)\) | **0.94** | 0.164 |
| Half + path as angle | half | \(\ell=\int e^{\phi}dr\) | 2.20 | 0.309 |
| Full + path as angle | full | \(\ell\) | 8.92 | 0.674 |
| Full + P_ell-like on cubic label | full | \(\int e^{-\phi}dr\) | 2.05 | 0.297 |
| Half + that reduced \(D_A\) | half | \(\int e^{-\phi}dr\) | 1.25 | 0.204 |

---

## Answer

**No — applying both honest fixes does not reconstruct the legacy fit.**

1. **Full light + same areal \(r(z)\)** (Layer A alone) **destroys** the fit (0.94 → 4.56).  
2. The **only** way to get the legacy \(d_L=r(1+z)\) back under full light is  
   \(D_A=r/(1+z)\), which makes  
   \((1+z)^2 D_A = r(1+z)\)  
   **by algebra** — that is the old formula again, not a new geometry.  
3. A **P_ell-style** reduction on the cubic label (\(\int e^{-\phi}dr\)) **helps a bit** vs bare full+\(r\) (4.56 → 2.05) but **does not** restore 0.94, and **does not** equal \(r/(1+z)\) (e.g. at \(z\sim1\), \(D_A/r\sim0.71\) vs \(1/(1+z)\sim0.50\)).

---

## Lay reading

The old win was **half light × that profile**.  
Correct light count changes the grading rule.  
The dimensional un-join (path vs sphere) is a **different** lever; on the cubic it does **not** cancel the extra stretch factor exactly.  
So you should **not** expect “full light + dimensional fix” to magically reprint the old scoreboard — and when something *does* reprint it, check it isn’t just \(D_A=r/(1+z)\) in disguise.

---

## One-line

**Legacy good fit is not reconstructed by full light + honest PATH/AREAL split on the cubic; only by definitions that return \(d_L=r(1+z)\) identically.**
