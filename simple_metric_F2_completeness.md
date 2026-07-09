# F2 completeness pass — local bulk densities on the simple metric

**Date:** 2026-07-08 · **Fork F2 thread** (dual explore with F1).  
**Question:** Within a stated class, is there a **derived** non-self-quenching bulk density?  
**Status:** PROVISIONAL completeness **within the class** below — not all of mathematics.

---

## Stated class (honest bounds)

Local bulk Lagrangian densities for \(\phi(r)\) on the simple metric that are:

1. Built from \(\phi\), \(\phi'\), and explicit \(r\) (static spherical),  
2. At most **first** derivatives of \(\phi\) in the action (second order EL),  
3. Definite **shift weight** \(k\): multiplies by \(e^{2k\lambda}\) under \(\phi\to\phi+\lambda\),  
4. Motivated by **metric geometry** already in the project (kinetic R1, angular Gauss/\(\mathcal{K}\), EH),  
5. **No** free \(D_A\), **no** free \(V(\phi)\) shopping.

Form:

\[
L = a(r)\,(\phi')^2 + \sum_k b_k(r)\, e^{2k\phi} + \sum_k c_k(r)\, e^{2k\phi}(\phi')^2.
\]

---

## Geometric determination of \(k\)

| Geometric object | Weight \(k\) | On simple metric |
|------------------|--------------|------------------|
| R1 kinetic after \(e^{2\phi}g^{rr}\) | 0 | \(a(r)\propto r^2\) |
| \(R^{(2)}\) | 0 | \(\propto 1/r^2\) |
| \(\mathcal{K}\) (extrinsic, normal \(\propto e^{-\phi}\partial_r\)) | **−1** on \(K\), **−2** on \(\mathcal{K}\) | \(\propto e^{-2\phi}/r^2\) |
| \(e^{2\phi}\mathcal{K}\) (compensate) | 0 | \(\propto 1/r^2\), **φ-free** |
| \(\sqrt{-g}R\) | empty bulk | pure boundary |
| Longitudinal \(R_L\sim e^{-2\phi}(\phi''-\cdots)\) | −2 before weighting | Route B multiplies \(e^{2\phi}\) → weight 0 + mixing |

**No angular/extrinsic construction produces weight \(k=+1\)** (would be non-SQ growth as \(\phi\to+\infty\)).  
The normal \(n^r=e^{-\phi}\) **forces** extrinsic objects to carry **negative** φ weight.

---

## Exhaustion in this class

| \(k\) | Geometric status | Exterior as \(\phi\to+\infty\) | \(c\)-bulk edge |
|-------|------------------|--------------------------------|-----------------|
| 0 kinetic | Forced by R1 form | Coulomb if alone | **No** |
| 0 compensated angular | Forced if shift restored on \(\mathcal{K}\) | no bulk source | **No** |
| −1 / −2 uncompensated \(\mathcal{K}\), dilated dust | Forced shape of \(\mathcal{K}\) / metric \(T_{tt}\) weight | **Self-quenching** | **No** |
| +1 | **Not derived** from angular normal | would be non-SQ | **Not available without invention** |

**Completeness claim (scoped):**  
Within {R1 kinetic, angular \(R^{(2)}+\mathcal{K}\) with or without compensation, EH empty, dilated \(e^{-2\phi}\) dust}, **every option either empties vacuum φ dynamics to Coulomb or self-quenches**.  
**None** yields a derived bulk \(c\)-edge.

**Outside class (not opened):** higher derivatives, free \(D_A\), non-local terms, arbitrary \(e^{+2\phi}\) potentials — would need **new derivation**, not a menu pick.

---

## Route B (optional, not a fix claim)

Longitudinal completion → weight-0 mixing \(\sim\phi'/r\) on simple metric.  
Changes first integrals; **not** shown to solve \(\phi=-a\ln(1-r/R)\).  
Remains a **sub-fork of F2** if re-derived carefully later — **not** activated as the answer here.

---

## F2 bottom line

**Trying F2 with the project’s actual geometric bulk content still fails the \(c\)-test.**  
Failure is completeness-within-class, not a missed numeric solution.  
A bulk \(c\)-edge would require structure **outside** this class — which is either a real future derivation or a return to F1’s kinematic reading.

---

## One-line F2

**Known geometric bulk on the simple metric is Coulomb or self-quenching; no derived non-SQ angular density; bulk \(c\)-edge not found.**
