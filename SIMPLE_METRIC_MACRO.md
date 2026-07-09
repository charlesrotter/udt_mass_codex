# Simple-metric macro — foundation (live)

**Date:** 2026-07-08 · **Status: LIVE foundation** (Charles: stick to simple version; free \(D_A\) quarantined).  
**Frame:** `UDT_ELEGANT_FRAME.md`  
**CAS:** `simple_metric_FE_rederive.py`  
**Quarantine:** `grok/quarantine_free_DA/` (do not treat as live)

---

## 0. The metric (only)

\[
\boxed{
ds^2 = -e^{-2\phi(r)}\,c^2\,dt^2 + e^{+2\phi(r)}\,dr^2 + r^2\,d\Omega^2
}
\]

**This is the whole geometric arena for the macro restart.**

| Property | From |
|----------|------|
| Static, spherically symmetric, diagonal | FREE first slice (like Schwarzschild symmetry) |
| \(g_{tt}=-e^{-2\phi}c^2\), \(g_{rr}=e^{2\phi}\) | R1–R3: differences, composition → exponential, mutual reciprocity |
| Angular \(r^2 d\Omega^2\) | Areal radial coordinate: sphere area \(4\pi r^2\) |
| Dynamical field | **\(\phi(r)\) only** (plus \(L_m\) later) |
| Free \(D_A(r)\) | **Out of scope** (quarantined) |

**Redshift (static observers):** \(1+z = e^{\phi_{\mathrm{src}}-\phi_{\mathrm{obs}}}\).  
**\(\phi=0\):** this observer’s chart zero — not a preferred cosmic center.

---

## 1. What we derive (and what we do not)

| Derive from this metric | Do not import |
|-------------------------|----------------|
| Measure \(\sqrt{-g}\) | Free-\(D_A\) EL “then freeze” |
| R1-clean kinetic for \(\phi\) | Cell package, BB fluids |
| Angular scalars on \(r=\mathrm{const}\) spheres | Edge mechanisms |
| φ-only Euler–Lagrange for each honest bulk weight | G/P cosmology branding |

---

## 2. Geometric densities on this metric (CAS)

### Measure

\[
\sqrt{-g} = c\, r^2 \sin\theta
\quad\text{(independent of \(\phi\))}
\]

### R1 kinetic (shift-clean)

\[
\sqrt{-g}\, e^{2\phi}\, g^{rr}\, (\phi')^2 = \sqrt{-g}\,(\phi')^2
\]

Reduced radial density (angles stripped, overall const absorbed into \(Z\)):

\[
L_{\mathrm{kin}} = \frac{Z}{2}\, r^2\, (\phi')^2
\]

\(Z>0\): **FREE** overall constant (observational later).

### Angular mismatch on spheres of radius \(r\)

\[
R^{(2)} = \frac{2}{r^2}, \qquad
\mathcal{K} = -2 e^{-2\phi}\frac{1}{r^2}
\quad\bigl(D_A=r,\; D_A'=1\bigr)
\]

**Flat check:** \(\phi=0\): \(R^{(2)}+\mathcal{K}=0\).  
**Compensated:** \(R^{(2)}+e^{2\phi}\mathcal{K}=0\) for all \(\phi\).

Reduced angular densities (× \(r^2\) from \(\sqrt{h}\) factors in the usual reduction):

| Weight \(W\) on \(\mathcal{K}\) | Reduced bulk \(\phi\)-dependence |
|--------------------------------|----------------------------------|
| \(W=e^{2\phi}\) (shift exact) | angular cancels → no bulk \(\phi\) source from \(\mathcal{K}\) |
| \(W=1\) (uncompensated) | \(\propto e^{-2\phi}\) remains |

---

## 3. Action (φ-only on the simple metric)

\[
S = \int dt\,dr\,d\Omega\; c\, r^2\sin\theta
\left[
  \frac{Z}{2}(\phi')^2 + R^{(2)} + W(\phi)\,\mathcal{K} + L_m
\right]
\]

with \(W\in\{e^{2\phi},\,1\}\) tagged as a **fork**, not two universes.

Equivalent reduced radial Lagrangian for \(\phi\) (vacuum, drop pure \(r\)-total-derivatives where they do not affect EL):

### Compensated \(W=e^{2\phi}\)

\[
L = \frac{Z}{2}\, r^2\, (\phi')^2
\quad\Rightarrow\quad
\boxed{(r^2\phi')'=0}
\quad\Rightarrow\quad
\phi = \phi_\infty - \frac{q}{r}
\]

### Uncompensated \(W=1\)

\[
L = \frac{Z}{2}\, r^2\, (\phi')^2 - 2 e^{-2\phi}
\quad\text{(up to \(\phi\)-independent terms)}
\]

Euler–Lagrange:

\[
\boxed{Z\,(r^2\phi')' = 4\, e^{-2\phi}}
\]

**Provenance:** varied **only** \(\phi\) on the simple metric with this \(L\). Not “free \(D\) then set \(D=r\).”

---

## 4. Matter (minimal, same metric)

Prefer dilation weight (Charles): e.g. reduced

\[
L_m = -\rho(r)\, r^2\, e^{-2\phi}
\]

Then uncompensated geometric + dilated dust:

\[
Z(r^2\phi')' = 4 e^{-2\phi} + 2\rho\, r^2 e^{-2\phi}
\]

(Compensated geometric + same \(L_m\): \(Z(r^2\phi')' = 2\rho r^2 e^{-2\phi}\).)

\(\rho(r)\) prescribed = FREE probe until a continuum sector is derived.

---

## 5. FREE ledger (simple path only)

| Item | Tag |
|------|-----|
| Metric box above | THEORY (R1–R3 + areal chart) |
| Static spherical | FREE first slice |
| \(W\in\{e^{2\phi},1\}\) | FORK — principle later |
| \(Z\) | FREE until observation |
| \(L_m\) / \(\rho\) | OPEN |
| Free \(D_A\) | **QUARANTINED** |

---

## 6. Macro question (unchanged, elegant)

From this **φ-only** theory: does \(\phi(r)\) give relational redshift with reach and an asymptotic dilation barrier, without preferred center and without invented terms?

**Vacuum laws (simple metric) — harmonic triangle:** see `simple_metric_third_path_derive.md`  
- K-R1: \(\Delta\phi=0\)  
- K-UW: \(\Delta e^{-\phi}=0\) (\(c\)-horizon)  
- **K-A:** \(\Delta e^{-2\phi}=0\Leftrightarrow G_{\theta\theta}=0\) (Schwarzschild-like + \(c\)-horizon) — working lean for \(c\)-edge  
Quarantine free \(D_A\): `grok/quarantine_free_DA/`.

---

## 7. One-line

**Simple UDT macro metric: reciprocal dilation + areal \(r\); field = \(\phi(r)\); operators from that only; free \(D_A\) archived.**
