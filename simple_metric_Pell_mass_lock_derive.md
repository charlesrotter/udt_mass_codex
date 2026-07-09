# ⚠ RETIRED (2026-07-09) — P_ell join

**Status: RETIRED.** External audit V2: imposition (SNe-shopped; rod story after χ²; no non-SNe derivation).  
Inferior to canon L (χ²/dof ~1.02 vs ~0.910). Never canonized.  
Also **Principle-7**: MS / \(r_{\max}=2GM/c^2\) is GR-form / definitional under MS packaging — not a native UDT prediction.  
Audit: `simple_metric_WR_L_external_triple_blind_audit_results.md`.  
**Do not build on this file as live foundation.**

---

# P_ell join — motivation + mass lock without J1

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | DERIVE |
| **Slice scope** | P_ell CHOSE + MS GR-form |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | see body |
| **Build-on grade** | **CONDITIONAL** |
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


**Date:** 2026-07-09 · **Mode: DERIVE / MAP**  
**Prior:** `simple_metric_path_areal_split_results.md` (P_ell sky demo)  
**Status:** PROVISIONAL. P_ell = **motivated named join**, not Charles-canon theorem.

---

## 0. Held

- Full light: \(d_L=(1+z)^2 D_A\)  
- PATH: \(x=X\tanh\phi\), \(1+z=e^{\phi}\), \(A=e^{-2\phi}=(X-x)/(X+x)\)  
- Simple metric areal chart \(r\): \(D_A=r\), \(d\ell=e^{\phi}dr\)  
- **Not** J1 (\(r=x\))

---

## 1. Motivation for P_ell (why path = proper length?)

### What static observers measure

A static observer’s **radial measuring rod** between nearby areal spheres is

\[
d\ell = e^{\phi}\,dr
\]

(that is the metric’s proper radial element). Composition of displacements, if it is about **what rulers measure**, is a law on **proper** increments, not on the areal label \(r\).

### Composition already needs a 1D chart

The xmax group law is a **1D** composition \(x_1\oplus x_2\) with rapidity \(\phi=\mathrm{arctanh}(x/X)\).  
That chart is PATH by nature.

### Named join P_ell

\[
\boxed{x \equiv \ell = \int_0^r e^{\phi(s)}\,ds
\qquad\Leftrightarrow\qquad
dr = e^{-\phi}\,dx
\qquad\Leftrightarrow\qquad
D_A=r(x)=\int_0^x e^{-\phi(u)}\,du}
\]

with \(\phi=\mathrm{arctanh}(u/X)\) on the path.

| Tag | |
|-----|--|
| Metric \(d\ell=e^{\phi}dr\) | THEORY |
| Composition as law on ruler displacements | MOTIVATED (relational static rods) |
| \(x=\ell\) exactly | **CHOSE / motivated join** — not forced by uniqueness theorem yet |
| Alternatives | radar; affine; \(x=r\) (J1); other operational lengths |

**Lay:** Path distance is what rods add up; sphere size is a different geometric job; recover sphere size by integrating the metric once path and \(\phi\) are known.

---

## 2. Closed geometry under P_ell

\[
e^{-\phi}=\sqrt{\frac{X-x}{X+x}},
\qquad
\frac{r}{X}=\int_0^{x/X}\sqrt{\frac{1-u}{1+u}}\,du.
\]

Exact integral to the bound:

\[
\boxed{
\frac{r_{\max}}{X}
= \int_0^1\sqrt{\frac{1-u}{1+u}}\,du
= \frac{\pi}{2}-1
\approx 0.570796
}
\]

(CAS/quad identity). So

\[
r_{\max} = X\Bigl(\frac{\pi}{2}-1\Bigr),
\qquad
X = \frac{r_{\max}}{\pi/2-1}.
\]

Areal radius **saturates** at finite \(r_{\max}<X\) while PATH proper length approaches \(X\).

---

## 3. Mass lock without J1

Misner–Sharp on the simple metric (geometric):

\[
m(r)=\frac{c^2 r}{2G}\bigl(1-A\bigr),
\qquad
A=e^{-2\phi}=\frac{X-x}{X+x}.
\]

Thus \(1-A=2x/(X+x)\) and

\[
\boxed{
m(x)=\frac{c^2}{G}\frac{r(x)\,x}{X+x}
}
\]

### Total mass at the bound

As \(x\to X^-\), \(A\to 0\), \(r\to r_{\max}\):

\[
\boxed{
M_{\mathrm{tot}}
= \frac{c^2 r_{\max}}{2G}
= \frac{c^2 X}{2G}\Bigl(\frac{\pi}{2}-1\Bigr)
}
\]

| Quantity | Under **J1** (\(r=x\)) | Under **P_ell** |
|----------|------------------------|-----------------|
| Horizon-like scale | \(X=2GM/c^2\) | \(r_{\max}=2GM/c^2\) |
| Composition bound \(X\) | \(=2GM/c^2\) | \(X=r_{\max}/(\pi/2-1)\approx 1.752\times(2GM/c^2)\) |
| Compactness \(2Gm/(c^2 r)\) | \(2x/(X+x)\) | **same** \(2x/(X+x)\) (depends on \(x,A\), not on which is \(r\)) |

**Lay:** Total mass locks to the **areal** saturation radius (Schwarzschild-like \(r_{\max}\)), not to the composition bound \(X\). Composition bound is larger by the pure number \(1/(\pi/2-1)\).

### Consistency check

Compactness \(\to 1\) as \(x\to X\) still holds (filled critical bound), same as the J1 identity in the \(x\) chart.

---

## 4. What improved / what remains

| Item | Status |
|------|--------|
| Sky demo under full light | P_ell χ²/dof≈1.02 vs J1≈2.17 (prior tile) |
| Dimensional story | PATH rods vs AREAL spheres — clearer |
| Mass lock | Re-derived; \(r_{\max}=2GM/c^2\), \(X=r_{\max}/(\pi/2-1)\) |
| Is \(x=\ell\) forced? | **Still open** — motivated, not unique proof |
| High-\(z\) residual vs LCDM | Still present (~0.14 mag RMS gap class) |
| Half light | Still wrong; not reopened |

---

## 5. Next (if continuing)

1. **Alternatives to P_ell** with same discipline (radar one-way/round-trip; null affine) — one tile each, job ledger, full light, no fudge.  
2. **Uniqueness:** does composition of static rod displacements **force** \(x=\ell\)?  
3. Residual high-\(z\): characterize, don’t retune \(X\) as shape.

---

## 6. One-line

**Under P_ell (path = proper length), areal radius saturates at \(r_{\max}=X(\pi/2-1)=2GM/c^2\), while composition bound \(X\) is larger by \(1/(\pi/2-1)\); mass locks to \(r_{\max}\), not to \(X=r\) as in J1 — a clean no-J1 cascade step, with \(x=\ell\) still motivated rather than proven unique.**
