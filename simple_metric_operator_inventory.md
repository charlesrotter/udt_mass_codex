# Inventory — bulk ingredients on the simple metric vs \(c\)-analogy

**Date:** 2026-07-08 · **Mode: MAP inventory** (no new term invented).  
**Test:** `simple_metric_c_analogy_MAP.md` (C1–C5)  
**Metric:** \(ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2\)

---

## Score key

| Mark | Meaning |
|------|---------|
| **SQ** | Self-quenching as \(\phi\to+\infty\) (source \(\to 0\)) — cannot drive \(c\)-like edge alone |
| **OK?** | Not obviously SQ; may participate in \(c\)-like structure |
| **EMPTY** | No bulk dynamics for \(\phi\) |
| **OUT** | Not derived from simple metric / quarantined / import |

---

## Ingredients

| # | Ingredient | On simple metric | As \(\phi\to+\infty\) | Mark | Note |
|---|------------|------------------|----------------------|------|------|
| 1 | 4D Einstein–Hilbert \(\sqrt{-g}R\) | Pure boundary (CAS, \(D_A=r\)) | — | **EMPTY** | Not φ engine |
| 2 | R1 kinetic \(\propto r^2(\phi')^2\) | Shift-clean | kinetic form OK; does not *source* φ alone | **OK?** | Needs a potential/source structure for EL |
| 3 | \(R^{(2)}=2/r^2\) | φ-independent | no φ drive | EMPTY for φ | Boundary-like in r |
| 4 | \(\mathcal{K}\propto -e^{-2\phi}/r^2\) uncompensated | Used in \(W=1\) | RHS \(\propto e^{-2\phi}\to 0\) | **SQ** | Current uncompensated exterior fails \(c\)-test |
| 5 | \(e^{2\phi}\mathcal{K}\) compensated | Cancels \(R^{(2)}\) | no bulk φ source | **EMPTY** for vacuum φ | Coulomb only from BCs / charge |
| 6 | Dilated dust \(L_m=-\rho r^2 e^{-2\phi}\) | Couples to φ | if ρ fixed chart density, weight \(e^{-2\phi}\to 0\) | **SQ** at large φ | Compact ball → finite \(Q\), finite \(\phi_\infty\) |
| 7 | φ-blind dust \(-\rho r^2\) | No direct φ weight | does not couple to φ in EL | weak / incomplete | Rejected as theory continuum |
| 8 | Free \(D_A\) dynamics | Quarantined | — | **OUT** | Not live |
| 9 | Cell winding / seal BCs | Import | — | **OUT** | Not macro derivation |
| 10 | Hand \(x_{\max}\) | Import | — | **OUT** | Forbidden mechanism |

---

## Structural conclusion

Every **active bulk source** we actually used on the simple metric for exterior φ dynamics is **self-quenching** in \(\phi\) (items 4, 6) or **empty** (1, 3, 5 vacuum).

So the failure of the \(c\)-analogy is **not an accident of numerics**. It is the **functional form** of the sources we put in:

\[
\text{source} \propto e^{-2\phi}\quad\Rightarrow\quad\text{deep dilation turns the source off.}
\]

A \(c\)-like law needs a different **derived** bulk content (or a different reading of reach) where approaching the edge makes the obstruction **stronger**, not weaker — the way approaching \(c\) makes \(\gamma\) **larger**.

---

## What re-derivation must hunt (still no invention)

From the metric and dilation principle only, find bulk content such that:

- either the EL **forces** \(\phi\to+\infty\) at finite \(r_*\) (or equivalent),  
- or the **invariant reach** has a bound with diverging dilation effect,  

**without** SQ exterior as the only engine.

Candidate **places to look** (corpus / GR mine — methods, not smuggled physics):

| Place | Why look | Risk |
|-------|----------|------|
| Full curvature / different split on **fixed** simple metric | EH empty does not exhaust all geometric scalars | must stay native, not GR paste |
| Boundary / horizon structure already in metric | \(c\)-like is often causal structure | don’t invent BC |
| Continuum from metric stress with different weight | dust weight may be wrong | must derive, not fit |
| Kinetic-only + constraint from reciprocity | thin | may be underdetermined |

**Not** first: free \(D_A\), BB, SNe.

---

## One-line

**Present simple-metric bulk sources die as \(\phi\) grows — opposite of a \(c\)-like edge; inventory done; next is re-derive non-self-quenching content from the metric under C1–C5 or show the \(c\)-analog lives in a different invariant.**
