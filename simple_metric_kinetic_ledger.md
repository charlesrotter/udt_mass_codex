# Principle ledger — R1-weighted vs unweighted kinetic (simple metric)

**Date:** 2026-07-08 · **Mode: MAP / OBSERVE**  
**Metric:** \(ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2\) only.  
**Goal:** make the kinetic fork visible under the \(c\)-analogy (no free \(D_A\), no hand \(X\)).  
**CAS:** session sympy + numeric horizon map.  
**Status:** PROVISIONAL ledger — not Charles canon.

---

## 0. Why this ledger exists

Two vacua already appear in founding native FE (`f766478`):

| Name | Kinetic density (schematic) | Vacuum solution |
|------|----------------------------|-----------------|
| **R1-weighted** | \(\sqrt{-g}\,e^{2\phi}g^{rr}(\phi')^2=\sqrt{-g}(\phi')^2\) | \(\phi=\phi_\infty-q/r\) |
| **Unweighted** | \(\sqrt{-g}\,g^{rr}(\phi')^2=\sqrt{-g}\,e^{-2\phi}(\phi')^2\) | \(e^{-\phi}=C_0+C_1/r\) |

They are **different theories** for \(\phi\), not a coordinate choice.  
Recent live work used **R1-weighted** (+ SQ angular/matter).  
Near-miss explore showed **unweighted** can be **\(c\)-like**.

---

## 1. Actions and Euler–Lagrange (simple metric, φ only)

Reduced radial Lagrangians (overall constants absorbed in \(Z\)):

### K-R1 (shift-clean / project-preferred)

\[
L_{\mathrm{R1}} = \frac{Z}{2}\, r^2\, (\phi')^2
\]

\[
\boxed{(r^2\phi')' = 0}
\quad\Rightarrow\quad
\phi = \phi_\infty - \frac{q}{r}
\]

### K-UW (unweighted / self-consistent with bare \(g^{rr}\))

\[
L_{\mathrm{UW}} = \frac{Z}{2}\, r^2\, e^{-2\phi}\, (\phi')^2
\]

EL equivalent to:

\[
\boxed{\Box_g\phi + e^{-2\phi}(\phi')^2 = 0}
\quad\Rightarrow\quad
e^{-\phi} = C_0 + \frac{C_1}{r}
\]

CAS: residual of UW EL on that solution is **0**.  
CAS: R1 residual \((r^2\phi')'\) on UW solution is **\(C_1^2/(C_0 r+C_1)^2\neq 0\)** in general — **not** the same solution.

---

## 2. What each preserves (principle)

| Principle / property | **K-R1** | **K-UW** |
|----------------------|----------|----------|
| Simple metric form | Yes | Yes |
| R1 as **metric** (dilation from differences → exp factors) | Yes | Yes |
| Bulk kinetic **shift-invariant** (\(\phi\to\phi+\mathrm{const}\)) | **Yes** (only \(\phi'\)) | **No** (explicit \(e^{-2\phi}\)) |
| Probe variation = self-consistent variation | **Yes** (founding argument) | **No** (extra term) |
| Weak field \(\sim 1/r\) | Yes (\(q/r\)) | Yes (\(C_1/(C_0 r)\) at large \(r\)) |
| Matches Schwarzschild \(g_{tt}\) at linear order | Yes (\(M\sim -q\)) | Different expansion of \(A=(C_0+C_1/r)^2\) |

**Core tension:** K-R1 is cleaner under **exact bulk shift**. K-UW is cleaner under **“vary φ inside the metric without R1 weight on kinetic.”**  
You cannot have both as written.

---

## 3. \(c\)-analogy scoreboard

### K-R1 vacuum

| Criterion | Result |
|-----------|--------|
| \(\phi\to+\infty\) at finite chart \(r\) | **No** (smooth for \(r>0\); \(\phi\to\phi_\infty\) as \(r\to\infty\)) |
| \(z\to\infty\) outward | **No** (finite \(z_{\max}\)) |
| Unattainable edge (\(\ell\) diverges at finite \(r_*\)) | **No** |
| Open infinity | **Yes** |

**Verdict:** fails bulk \(c\)-edge; keeps bulk shift purity.

### K-UW vacuum (horizon branch)

Set \(C_0>0\), \(C_1=-C_0 r_*\) with \(r_*>0\):

\[
e^{-\phi} = C_0\Bigl(1-\frac{r_*}{r}\Bigr), \qquad r > r_*.
\]

Then as \(r\to r_*^+\):

| Criterion | Result |
|-----------|--------|
| \(\phi\to+\infty\) | **Yes** |
| \(A=e^{-2\phi}\to 0\) (\(g_{tt}\to 0\)) | **Yes** |
| \(1+z\to\infty\) approaching edge | **Yes** |
| \(\ell=\int e^{\phi}dr\) as lower limit \(\to r_*^+\) | **Diverges** (numeric \(\sim|\ln\varepsilon|\)) |
| Large \(r\) | \(A\to C_0^2\), \(\phi\to-\ln C_0\) finite (open exterior away from edge) |

**Verdict:** **passes bulk \(c\)-like geometry** for the **inner** edge at \(r_*\); outer end is ordinary finite depth.

**Reading:** edge is a **horizon-like surface at finite areal radius**, approached from outside (or inside, other sign choices) — SR-like unattainability via infinite proper distance / infinite redshift, not a Coulomb plateau at infinity.

---

## 4. Horizon domain map (K-UW)

| Parameters | Domain where \(e^{-\phi}>0\) | Horizon |
|------------|----------------------------|---------|
| \(C_0>0\), \(C_1>-C_0 r\) always if \(C_1\ge 0\) | all \(r>0\) | **none** (no zero) |
| \(C_0>0\), \(C_1=-C_0 r_*<0\) | \(r>r_*\) | \(r=r_*\), approach from above |
| \(C_0>0\), \(C_1=-C_0 r_*<0\) | \(0<r<r_*\) if inequality flips | same zero; other side of chart |
| \(C_0=0\), \(C_1>0\) | all \(r>0\) | \(\phi=-\ln(C_1/r)\to+\infty\) as \(r\to 0^+\) only |

**Weak-field exterior** (\(r\gg r_*\)): looks Coulomb-like with \(q\sim r_*\).  
**Near \(r_*\):** strongly non-Coulomb; \(c\)-like edge.

**Relational caution:** \(r_*\) is a special radius in this chart. Elevating it to “the cosmos edge for everyone” still needs the **frame-relation** story (observer-centered charts) — same as any SSS solution. The **local** \(c\)-structure is real; preferred-center ontology is not automatic.

---

## 5. Comparison to xmax boost (inspiration only)

| | K-UW solution | xmax boost profile |
|--|---------------|-------------------|
| \(\phi\) | \(-\ln(C_0+C_1/r)\) | \(\mathrm{arctanh}(x/X)\) |
| \(A=e^{-2\phi}\) | \((C_0+C_1/r)^2\) | \((X-x)/(X+x)\) |
| Same ODE solution? | **No** | Different |
| \(A\to 0\) at finite chart locus? | **Yes** (if \(r_*\)) | **Yes** (if \(x\to X\)) |
| \(X\) / \(r_*\) free? | Yes (integration constants) | Yes (postulate / ruler) |

**Shared spirit:** finite chart edge, \(\phi\to\infty\), \(A\to 0\).  
**Not interchangeable formulas.**

---

## 6. How this sits with F1 / F2

| Fork | Natural kinetic | \(c\)-edge from vacuum kinetic alone |
|------|-----------------|--------------------------------------|
| **F1** (bulk shift exact) | **K-R1 only** | **No** |
| **F2** (bulk may break shift) | K-UW **allowed as a candidate** (breaks shift in kinetic) | **Yes** (horizon branch) |

So the near-miss “unweighted vacuum” is essentially **F2 applied to the kinetic term itself**, not only to \(\mathcal{K}\).

SQ geometric \(\mathcal{K}\) is a *different* F2 try that **fails** \(c\).  
K-UW is an F2 try that **passes** \(c\)-geometry but **fails** bulk-shift purity.

---

## 7. Premise ledger (honest)

| Item | Tag |
|------|-----|
| Simple metric | LIVE |
| K-R1 | THEORY-leaning (R1 on action + founding native FE) |
| K-UW | Founding dual vacuum; **downgraded** for R1 purity; **re-elevated** as \(c\)-near-miss |
| Choosing one kinetic | **OPEN principle** — not solved by numerics |
| Hand \(x_{\max}\) / free \(D_A\) | Still out |

---

## 8. What we are **not** doing

- Declaring K-UW canon  
- Declaring K-R1 wrong  
- Importing free \(D_A\)  
- Setting \(r_*\) from data  

---

## 9. Next options (both honest)

1. **Develop K-UW as working hypothesis** under F2: full solution-space map (signs, matching to matter, relational charts) + list every R1 objection in one place.  
2. **Keep K-R1** and accept bulk \(c\)-edge is not from vacuum kinetic (F1 kinematic path).  
3. **Seek a third derivation** that recovers horizon \(A\to0\) **and** a shift story (unknown; not forced yet).

---

## Plain summary

There are **two simple vacuum engines** already in the project’s founding math:

1. **Clean shift** → Coulomb → depth levels off, no wall.  
2. **Unweighted kinetic** → can put an **infinite-redshift horizon at a finite radius** you never reach in proper distance — much more like \(c\).

They disagree on principle (shift symmetry of the action).  
They are not the same as the xmax boost formula, but the unweighted one **does** the horizon job.  
Choosing between them is the real fork for a \(c\)-like macro — not free sphere size.
