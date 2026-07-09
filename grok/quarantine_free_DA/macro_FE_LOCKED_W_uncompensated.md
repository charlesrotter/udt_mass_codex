# Locked field equations — start with W uncompensated (option B)

**Date:** 2026-07-08  
**Charles pins (this session):**

| Pin | Choice | Tag |
|-----|--------|-----|
| **W** | **B — angular can break shift** → \(W = 1\) (uncompensated \(\mathcal{K}\)) | **CHOSE (Charles)** |
| **Fallback** | If B hits a hard blocker → try **C** (vacuum compensated; matter breaks shift) | Contingency, not active |
| **Z** | Free overall constant until observation | **FREE (observational later)** |
| **Matter** | Vacuum geometry first (\(L_m = 0\)); dilated continuum later | **Scoped** |
| **Varied** | \(\phi(r)\), free \(D_A(r)\); static spherical diagonal | **FREE first slice** |

**Status:** PROVISIONAL locked working equations — not Charles-canon until he signs.  
**CAS:** EL identities checked this session (sympy euler + manual). Builds on `macro_native_FE_from_metric_CLEAN.md`.

**Do not brand as “Branch P cosmology.”** This is the uncompensated-weight case of the native geometric action, with free transverse size.

---

## 1. Metric (unchanged)

\[
\mathrm{d}s^2 = -e^{-2\phi}\,c^2\,\mathrm{d}t^2 + e^{2\phi}\,\mathrm{d}r^2 + D(r)^2\,\mathrm{d}\Omega^2
\]

(\(D \equiv D_A\).) Redshift: \(1+z = e^{\Delta\phi}\). \(\phi=0\) = observer chart, not cosmic center.

---

## 2. Action (locked for B, vacuum)

\[
S = \int c\sqrt{h}\,\Bigl[\tfrac{Z}{2}\,(\phi')^2 + R^{(2)}[h] + \mathcal{K}\Bigr]\,\mathrm{d}t\,\mathrm{d}r\,\mathrm{d}^2x
\]

with

\[
R^{(2)} = \frac{2}{D^2},\qquad
\mathcal{K} = -2\,e^{-2\phi}\Bigl(\frac{D'}{D}\Bigr)^2,\qquad
W = 1.
\]

- \(Z > 0\): free overall constant (fix later from data).  
- No Route-B mixing term.  
- No continuum \(L_m\) yet.

**Reduced radial density** (angles stripped; constant factors dropped from EL):

\[
L = \frac{Z}{2}\,D^2\,(\phi')^2 + 2 - 2\,e^{-2\phi}\,(D')^2.
\]

---

## 3. Field equations (vacuum, round, free \(D\))

### φ-equation (dilation)

\[
\boxed{\displaystyle
\frac{\mathrm{d}}{\mathrm{d}r}\bigl(Z\,D^2\,\phi'\bigr)
= 4\,e^{-2\phi}\,(D')^2
}
\tag{FE-φ}
\]

**Plain:** gradients of φ are sourced by how fast the sphere size changes, weighted by depth \(e^{-2\phi}\).

### D-equation (areal / transverse size)

\[
\boxed{\displaystyle
\frac{\mathrm{d}}{\mathrm{d}r}\bigl(e^{-2\phi}\,D'\bigr)
= -\frac{Z}{4}\,D\,(\phi')^2
}
\tag{FE-D}
\]

Equivalent forms (same equation):

\[
\frac{\mathrm{d}}{\mathrm{d}r}\bigl(-4\,e^{-2\phi}\,D'\bigr) = Z\,D\,(\phi')^2,
\]

\[
D'' - 2\,\phi'\,D' = -\frac{Z}{4}\,D\,e^{2\phi}\,(\phi')^2.
\]

**Plain:** the sphere’s radial profile is driven by the φ-gradient energy density.

### System character

- Coupled second-order system for \((\phi, D)\).  
- **Not** sourceless: even in vacuum, angular geometry and φ talk to each other.  
- \(Z\) only sets relative strength of kinetic vs angular pieces (overall scale of solutions may absorb \(Z\) in part — characterize before fitting).

---

## 4. Useful reductions (not the primary system)

### Frozen \(D = r\) (gauge / specialization)

\[
Z\,(r^2\phi')' = 4\,e^{-2\phi}.
\]

Known finite-domain / no-asymptotic-vacuum behavior under this freeze is **scoped to frozen \(D\)** — not automatic for free-\(D\) (FE-φ)+(FE-D). Macro default: **keep \(D\) free**.

### Compensated contrast (not active — option A / C-vacuum)

If \(W = e^{2\phi}\): \(\frac{\mathrm{d}}{\mathrm{d}r}(Z D^2\phi') = 0\).  
Held only as **fallback C** vacuum sector if B blocks.

---

## 5. Fallback C (if B blocks) — not active yet

| Sector | W | Notes |
|--------|---|--------|
| Vacuum | \(W = e^{2\phi}\) | Shift exact; φ sourceless unless boundaries |
| Matter | Break shift | Dilated \(L_m\) and/or uncompensated only where matter sits |

**Trigger to switch:** genuine blocker in B (inconsistency of FE, no regular solutions in the intended regime after solver-complete exploration) — **not** a mismatch to SNe/BAO alone (solver-first).

---

## 6. What is still open (not in the boxes)

| Item | Status |
|------|--------|
| Value of \(Z\) | FREE — observational later |
| Continuum \(L_m\) | Not in FE yet |
| Boundary conditions / domain | Solution-space |
| Time dependence, anisotropy | Later generation |
| BAO / CMB | Downstream emergence checks, not inputs |

---

## 7. Observing stance (when we solve)

- **Metric-led:** what solutions \((\phi,D)\) exist under (FE-φ)+(FE-D)?  
- Not targeting BAO/CMB shapes; if structure-like features appear, report them.  
- \(Z\): scan as a parameter or nondimensionalize; do not fit sky until form is stable.  
- If regular free-\(D\) solutions refuse the intended regime → document blocker → consider C.

---

## 8. One-line summary

**Start here:** uncompensated native action, free \(D\), free \(Z\), vacuum —  
\(\partial_r(Z D^2\phi') = 4 e^{-2\phi}(D')^2\) and \(\partial_r(e^{-2\phi} D') = -\frac{Z}{4} D (\phi')^2\).  
Fallback C only if B is blocked.
