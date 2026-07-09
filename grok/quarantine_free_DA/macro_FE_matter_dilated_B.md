# Field equations — option B + minimal dilated dust

**Date:** 2026-07-08  
**Builds on:** `macro_FE_LOCKED_W_uncompensated.md`  
**CAS:** session sympy (EL match).  
**Status:** PROVISIONAL working equations for OBSERVE (not canon).

---

## Premises

| Item | Tag |
|------|-----|
| W = 1 (option B) | CHOSE |
| Z free | FREE |
| Continuum sector | **Minimal dilated dust** (probe, not unique native matter) |
| ρ(r) | **Prescribed** profile (FREE shape) — not dynamical fluid |
| Compare | vacuum / dilated / φ-blind (control) |

**Dilated form (Charles dilation + prior macro probe):**

\[
L_m = -\rho(r)\, D^2\, e^{-2\phi}
\]

in the same reduced radial density as the geometric \(L\).

**Plain:** matter energy carries an extra depth weight \(e^{-2\phi}\) (weaker where φ is large).

**φ-blind control (not theory):** \(L_m = -\rho(r)\, D^2\).

---

## Reduced density

\[
L = \frac{Z}{2} D^2 (\phi')^2 + 2 - 2 e^{-2\phi}(D')^2 + L_m
\]

---

## Field equations — dilated

\[
\boxed{
\frac{\mathrm{d}}{\mathrm{d}r}\bigl(Z D^2 \phi'\bigr)
= 4 e^{-2\phi}(D')^2 + 2\rho\, D^2 e^{-2\phi}
}
\tag{FE-φ-m}
\]

\[
\boxed{
\frac{\mathrm{d}}{\mathrm{d}r}\bigl(e^{-2\phi} D'\bigr)
= -\frac{Z}{4} D (\phi')^2 + \frac{1}{2}\rho\, D\, e^{-2\phi}
}
\tag{FE-D-m}
\]

**Plain:**

- Matter **directly sources φ** (extra positive term on RHS of FE-φ when ρ>0).  
- Matter **pushes on expansion flux F** (can counteract the vacuum drain of F from φ-gradients).

### φ-blind control

\[
\frac{\mathrm{d}}{\mathrm{d}r}(Z D^2\phi') = 4 e^{-2\phi}(D')^2
\quad\text{(no direct ρ→φ)}
\]

\[
\frac{\mathrm{d}}{\mathrm{d}r}(e^{-2\phi} D')
= -\frac{Z}{4} D (\phi')^2 + \frac{1}{2}\rho\, D
\]

---

## Observe stance

**Question:** does dilated ρ **change** the vacuum hard/soft throat story (pinch vs plateau)?  
Not: fit the sky. Not: invent a profile to force a desired shape.
