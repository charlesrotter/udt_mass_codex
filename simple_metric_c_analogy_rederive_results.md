# Re-ground bulk operators under the \(c\)-analogy (simple metric)


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

**Date:** 2026-07-08 · **Mode: MAP + OBSERVE (analytic).**  
**Metric:** simple only (`SIMPLE_METRIC_MACRO.md`).  
**Test:** `simple_metric_c_analogy_MAP.md` (C1–C5).  
**Inventory:** `simple_metric_operator_inventory.md`.  
**Status:** PROVISIONAL diagnosis + candidate-profile check. **No new bulk term invented.** Free \(D_A\) stays quarantined.

---

## 1. What we already know

Present φ-only EL on the simple metric (geometric \(W\cdot\mathcal{K}\) ± dilated dust) give:

- \(\phi\to\phi_\infty<\infty\), open \(r\), finite \(z_{\max}\)

That is **not** \(c\)-like. Root form of the active sources:

\[
\text{source} \propto e^{-2\phi}
\quad\text{(self-quenching as dilation deepens)}
\]

Opposite of \(\gamma\to\infty\) as \(v\to c\).

---

## 2. \(c\)-like **profiles** exist as pure geometry (functions)

On the simple metric, set (example family)

\[
\phi(r) = -a\ln\bigl(1-r/R\bigr), \qquad 0\le r < R,\quad a>0.
\]

Then \(\phi\to+\infty\) as \(r\to R^-\) (**finite chart radius**).

| \(a\) | Proper \(\ell=\int_0^R e^{\phi}\,dr\) | Null \(\int e^{2\phi}dr\) |
|-------|--------------------------------------|---------------------------|
| \(a<1\) | finite | finite if \(a<\tfrac12\) |
| \(a\ge 1\) | **diverges** (unattainable in proper distance) | diverges |

So **\(a\ge 1\)** is a clean **\(c\)-like** geometric signature:  
**finite coordinate edge, infinite dilation, unreachable in proper distance** — matching Charles’s “φ→∞ at finite coordinate radius.”

**Metric permits it.** The question is only: **do any derived field equations admit such solutions?**

---

## 3. Current EL **reject** that profile (CAS)

For \(\phi=-a\ln(1-r/R)\):

| Operator | Residual |
|----------|----------|
| \(W=e^{2\phi}\): \((r^2\phi')'=0\) | **nonzero** (not Coulomb) |
| \(W=1\): \(Z(r^2\phi')'-4e^{-2\phi}=0\) | **nonzero** (series at \(r=0\): leading \(-4+\cdots\)) |

So the present bulk equations **do not** generate the \(c\)-like edge profiles the metric allows.  
This is a **hard fail of the operators under the \(c\)-test**, not a soft numeric miss.

---

## 4. Structural tension: R1 shift vs \(c\)-edge

**R1 (metric / dilation):** only **differences** of \(\phi\) enter dilation factors — no preferred zero of \(\phi\).

Applied to a **bulk action** as exact shift symmetry \(\phi\to\phi+\mathrm{const}\):

| Allowed local bulk pieces | Forbidden if R1 is exact on the action |
|---------------------------|------------------------------------------|
| densities depending on \(\phi'\) only (e.g. \(r^2(\phi')^2\)) | potentials \(V(\phi)\) |
| shift-invariant combos (e.g. \(e^{2\phi}\mathcal{K}\), φ-independent) | bare \(e^{-2\phi}\) bulk without compensation |

**Kinetic-only + exact shift** ⇒ \((r^2\phi')'=0\) ⇒ **Coulomb** ⇒ **fails \(c\)-analogy**.

**Uncompensated \(\mathcal{K}\)** breaks shift but with **weight \(-2\)** ⇒ **self-quenching** ⇒ **fails \(c\)-analogy**.

**Dilated dust** \(\propto e^{-2\phi}\) ⇒ same **SQ** ⇒ **fails \(c\)-analogy**.

### Honest fork (principle, not mechanism shopping)

| Fork | Meaning |
|------|---------|
| **F1** | R1 is **exact** for bulk action ⇒ vacuum dynamics are Coulomb-like ⇒ **\(c\)-edge is not bulk-EL exterior** on this cut; edge must live elsewhere (relational/optical/invariant), or the \(c\)-test is mis-aimed |
| **F2** | R1 binds the **metric form** only; bulk may break shift **if derived** (angular/matter) — then the **weight** of the break must **not** be SQ if \(c\)-edge is required (current \(\mathcal{K}\) weight **is** SQ) |
| **F3** | \(c\)-edge is **metric-kinematic**: whenever \(\phi\to+\infty\) at finite \(r_*\), unattainability follows from \(d\ell=e^{\phi}dr\); the missing piece is an EL that **forces** that profile — still must be derived |

**No fork is “add \(x_{\max}\) by hand.”**

---

## 5. What re-derivation is allowed to look for

On the **simple metric only**, from geometry/dilation:

1. **All local scalars** built from the metric and \(\partial\phi\), classified by shift weight (inventory started).  
2. **Which weights** are forced by reciprocity / angular flatness / R1 (not free shopping).  
3. **Whether any forced non-SQ combination** exists.  
   - Current forced angular mismatch \(\mathcal{K}\) has weight \(-2\) → SQ when uncompensated.  
   - Compensated form has weight \(0\) but is φ-independent on \(D_A=r\).  
4. **Boundary / variational** terms: EH is pure boundary — might encode conditions without bulk SQ source (careful: don’t smuggle GR).  
5. **Continuum** from \(T_{\mu\nu}\) with weights **derived from the metric**, re-checked for SQ.

**Refuse:** free \(D_A\) return, BB, hand wall, fitting \(R\) or \(a\).

---

## 6. Immediate conclusions (banked)

| Claim | Status |
|-------|--------|
| Simple metric allows \(c\)-like \(\phi\to+\infty\) at finite \(r\) | **YES** (profile family exists) |
| Present geometric ± dilated-dust EL admit those profiles | **NO** (CAS residual) |
| Failure mode of present EL | **Structural SQ** \(e^{-2\phi}\) |
| R1-exact bulk vacuum | Coulomb; **cannot** be \(c\)-edge engine |
| Free \(D_A\) needed? | **Not shown** — not reopened |
| Hand \(x_{\max}\)? | **Forbidden** |

---

## 7. Next step (when continuing)

**Principle fork F1 vs F2 with Charles (lay):**  

- If bulk must obey exact φ-shift, the \(c\)-analog **cannot** be “bulk source drives \(\phi\to\infty\)”; redefine where the analog lives.  
- If bulk may break shift, the break we used (\(\mathcal{K}\)) has the **wrong weight** for a \(c\)-edge; hunt a **derived** non-SQ structure on the simple metric only.

Optional analytic tile before ponder: complete classification of **shift weights** of all curvature components of the simple metric (table), still no new action.

---

## Plain summary

A \(c\)-like edge would look like dilation running away at a finite chart distance so you never arrive — the metric allows that shape. Our field equations **don’t produce it**; they **turn the source off** as things get deeper. That’s a real operator problem under your analogy. Exact “no preferred zero of φ” in the bulk pushes us toward Coulomb (also not \(c\)-like). So the next work is a **principle choice** about shift and a **re-derivation** of bulk content — not more of the same EL, and not inventing a wall.
