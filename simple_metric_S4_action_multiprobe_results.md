## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE / OBSERVE |
| **Slice scope** | simple metric; Einstein-route ceiling; action EL contrast; distance ladder readout |
| **Observing or targeting?** | OBSERVE consistency — not targeting multi-probe win |
| **Comparator scaffolds** | none for selection |
| **Verifier status** | SELF-SCRIPT / CAS session |
| **Build-on grade** | **LEAD** — multi-probe ladder OK; Einstein \(p_r=0\) path **WITHDRAWN** (S4 reconcile scar); stresses corrected there |
| **Re-run commands** | `python3 simple_metric_S3_native_dust_ceiling.py` · CAS in session |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Einstein/MS on simple metric | GR-form mine | Y for S3 |
| \(p_r=0\Rightarrow A=1-r/X\) | DERIVED under that form | Y |
| R1 kinetic + \(L_m=-\rho r^2 e^{-2\phi}\) | THEORY probe action | Y for mismatch |
| Full light ladder | DERIVED | Y |
| BAO products | SCAFFOLD later | N as fit |

### What is NOT claimed

- Action and Einstein routes already agree.
- BAO fit.

### Do not build on

- Ignoring the action EL mismatch.

---

# S4 — Action honesty + multi-probe ladder (same geometry)

**Prior:** S3 Einstein-route selection of \(A=1-r/X\).

---

## 1. Continuum stresses (uncovered) — **CORRECTED in S4 reconcile**

For \(A=1-r/X\) on the simple metric (\(c=G=1\)), **full curvature**:

\[
\rho=\frac{1}{4\pi X r},\qquad p_r=-\rho,\qquad p_\perp=-\frac12\rho
\]

| Stress | Meaning |
|--------|---------|
| \(p_r=-\rho\) | **simple-metric identity** (not free dust) — old \(p_r=0\) was a \(G^r_r\) scar |
| \(p_\perp=-\rho/2\) | **tangential tension** (geometry speaks) for this profile |

**Elegance:** the metric does not give isotropic dust; it gives a definite anisotropic continuum with **\(p_r=-\rho\)**. Own it. Details: `simple_metric_S4_reconcile_critical_results.md`.

---

## 2. Action EL vs Einstein route (important hygiene)

**Probe action** (SIMPLE_METRIC_MACRO): R1 kinetic + \(L_m=-\rho r^2 e^{-2\phi}\).

Compensated EL:
\[
Z(r^2\phi')'=2\rho r^2 e^{-2\phi}
\]

On the ceiling solution \(\phi=-\frac12\ln(1-r/X)\), \(\rho=1/(4\pi X r)\):

\[
\frac{(r^2\phi')'}{2\rho r^2 e^{-2\phi}}
=\pi X^2\frac{2X-r}{(X-r)^3}
\neq 1
\]

**CAS residual ≠ 0.** Uncompensated bulk term also fails to match.

### Meaning (solver-first, no mechanism panic)

| Route | Status |
|-------|--------|
| **Einstein / MS + \(p_r=0\)** | Selects \(A=1-r/X\) cleanly |
| **R1 kinetic + dilated dust \(L_m\)** | **Does not** have that profile as EL solution for the same \(\rho\) |

So S3 is **real geometry** on the Einstein/MS reading of the simple metric, **not** yet “the EL of the R1+dust action.”

**UDT posture:**  
Do **not** invent a new force to fix the residual.  
Do **ask** which continuum is native:

1. Prefer Einstein-defined \(T_{\mu\nu}=G_{\mu\nu}/8\pi\) on this metric (geometry speaks source) — then \(p_r=0\) is a **slice** of that \(T\), and EL for \(\phi\) may need the action that reproduces Einstein, not a thin R1+dust probe; or  
2. Prefer R1+dust action — then **solve its EL** (S2-style) and see what ceilings appear **without** forcing \(p_r=0\) by hand.

Both are uncover paths. **Gluing them without residual check was the soft spot** — now tagged.

---

## 3. Multi-probe ladder (same law, readout only)

Under ceiling + full light:

\[
\frac{D_A}{X}=1-\frac{1}{(1+z)^2},\qquad
\frac{D_M}{X}=\frac{z(z+2)}{1+z},\qquad
\frac{d_L}{X}=z(z+2)
\]

| \(z\) | \(D_A/X\) | \(D_M/X\) | \(d_L/X\) |
|------:|----------:|----------:|----------:|
| 0.1 | 0.174 | 0.191 | 0.210 |
| 0.5 | 0.556 | 0.833 | 1.250 |
| 1.0 | 0.750 | 1.500 | 3.000 |
| 2.0 | 0.889 | 2.667 | 8.000 |

Low-\(z\): \(D_A\sim 2Xz\), \(d_L\sim 2Xz\) (scale absorbed in calibration).

**BAO transverse (character, not fit):**  
Surveys often publish \(D_M/r_d\). Under this law \(D_M(z)=X\,z(z+2)/(1+z)\).  
One scale \(X\) (and a ruler \(r_d\) if used) — **no new shape knobs**.  
**Next concrete multi-probe tile:** compare this **fixed** \(D_M(z)/X\) shape to published \(D_M\) ratios (care: survey fiducials) — characterize residual, don’t retune \(A(r)\).

---

## 4. Program state after S4

| Piece | Status |
|-------|--------|
| Full light | DERIVED, fixed |
| Sphere ceiling \(X\) | Charles CHOSE meaning |
| Einstein \(p_r=0\Rightarrow A=1-r/X\) | **DERIVED** under GR-form on simple metric |
| Action R1+dust EL | **Does not** currently reproduce that solution |
| SNe residual ~0.91 | Demo character under full light |
| Multi-probe | Ladder formulas ready; data compare **owed** |

---

## 5. Next (elegant order)

1. **Reconcile routes:** either Einstein-primary continuum on simple metric, or solve R1+dust EL solution space (no hand \(p_r=0\)) and compare characters.  
2. **BAO transverse character** with fixed \(D_M(z)\).  
3. Own \(p_\perp=-\rho/2\) as geometric fact.

---

## One-line

**\(p_r=0\) on the simple metric uniquely gives the sphere-ceiling law and \(p_\perp=-\rho/2\); that is Einstein-route geometry — the thin R1+dust action EL does not yet match, so the next uncover is action vs Einstein continuum consistency, not a new SNe mechanism.**
