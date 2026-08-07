# Working postulate — finite max distance \(x_{\max}\)

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | MAP |
| **Slice scope** | working postulate doc |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | see body |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | see body / N/A |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body | full ledger | mixed | Y |

### What is NOT claimed

- Physics canon. Hygiene grade ≠ nature proof.
- Scope wider than slice above.

### Do not build on (if any)

- CHOSE/explore items without restating premises.

---


**Date:** 2026-07-08 · **Charles:** accepts the postulate, especially if consilience continues.  
**Status:** **WORKING POSTULATE** (not yet Charles-canon theorem).  
**Derive form:** `simple_metric_hyperbolic_derive.md` · CAS `derive_xmax_boost.py`

---

## Postulate (P3)

**There exists a finite invariant maximum distance \(x_{\max}\)** for positional composition — the twin of a finite maximum speed \(c\) in SR.

- Limit of a **distance**, not a place  
- Always the far end of reach; approached asymptotically as \(\phi\to\infty\), not occupied as a town on the map  
- Value not fixed by the postulate alone (like \(c\)’s value is not fixed by “\(c\) is finite”)

---

## Already derived from metric + postulate (form)

\[
x = x_{\max}\tanh\phi,
\quad
1+z = \sqrt{\frac{x_{\max}+x}{x_{\max}-x}},
\quad
A = e^{-2\phi} = \frac{x_{\max}-x}{x_{\max}+x}
\]

Simple metric supplies \(A=e^{-2\phi}\), \(1+z=e^{\phi}\), reciprocal \(g_{rr}=1/A\).

---

## Consilience cascade (checklist — continue here)

Each item is a **win if it falls out** without new knobs. Failures must be recorded, not patched.

| # | Cascade item | Status |
|---|--------------|--------|
| C0 | Hyperbolic reach + redshift–distance + \(A\to 0\) at \(x\to x_{\max}\) | **DONE** (form) |
| C1 | Small-\(x\): \(1+z \approx 1 + x/x_{\max}\) (linear distance–redshift) | **DONE** (series of C0) |
| C2 | Relational: every observer’s \(\phi=0\), same *kind* of bound ahead (not one preferred place) | **PASS structural** — `simple_metric_cascade_C2_C5_J1.md` |
| C3 | Lock \(x_{\max} = k\, G M_{\mathrm{tot}}/c^2\) with pure \(k\) from geometry/closure | **DONE conditional** — \(k=2\) under J1 (`simple_metric_mass_xmax_cascade.md`) |
| C4 | Closure \(A\to0\), compactness→1 at bound | **DONE as identity** of hyperbolic \(A\) + MS under J1; filled \(m(x)\) |
| C5 | n=2 optics \(d_L=(1+z)^2 D_A\) consistent with this \(x(\phi)\) chart | **Form DONE**; **numeric FAIL** on Pantheon+ (`simple_metric_pantheon_xmax_fit_results.md`) |
| C6 | Weak field / local mass limits recover Newtonian / Schw-like where required | **OWED** check |
| C7 | No need for dark-matter pudding or BB edge fluids for the kinematic sky | **PROGRAM** (elegant frame) |
| C8 | Absolute meters from \(c,G\) only | **NOT expected** — lock \(M\)–\(x_{\max}\); ratios primary |

**Standing rule:** if consilience **stalls**, revisit the postulate or the join to areal \(r\) / dynamics — do not invent mechanisms to save it.

---

## Relation to other vacuum laws

| Law | Role under accepted postulate |
|-----|-------------------------------|
| Hyperbolic \(x(\phi)\) | **Kinematic core** of macro reach |
| K-A / Schw | Local mass horizons — different story (places); may sit *inside* the same metric |
| K-R1 Coulomb | Shift-pure; not the distance-bound law |
| SQ geometric exterior | Demoted for macro edge |

---

## One-line

**\(x_{\max}\) accepted as working postulate; hyperbolic cascade is live; consilience (mass lock, relational, optics) is the next proof of the pudding.**
