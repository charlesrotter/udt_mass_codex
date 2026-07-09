## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric; compensated R1+dust EL; uncompensated vacuum probe; free φ / free ρ |
| **Observing or targeting?** | **OBSERVE** A-primary space — not gluing to Einstein map |
| **Comparator scaffolds** | none |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S7_Aprimary_space.py` |
| **Build-on grade** | **LEAD** (A-primary census) |
| **Re-run commands** | `python3 simple_metric_S7_Aprimary_space.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| R1 compensated kinetic + \(L_m=-\rho r^2 e^{-2\phi}\) | THEORY probe action | Y |
| EL \(Z(r^2\phi')'=2\rho r^2 e^{-2\phi}\) | DERIVED from that action | Y |
| Free φ / free ρ probes | **free-and-explored** | Y as census |
| Einstein \(\rho_E\) on same φ | GR-form contrast only | Y as contrast |
| Uncompensated vacuum EL | THEORY fork \(W=1\) | Y scoped |

### What is NOT claimed

- R1 is the final UDT macro action.
- A-primary solutions are “wrong” because they ≠ Einstein.
- Numeric uncompensated runs are high-precision (stiff near 0).

### Do not build on

- Forcing EL solutions onto \(A=1-r/X\).
- Adding terms so \(\rho_{EL}=\rho_E\).

---

# S7 — A-primary solution space (R1 EL)

**Prior:** S6 mapped **E-primary** continuum (\(\rho\) or \(A=1-cr^p\)).  
**This tile:** map the **other** route — what the thin R1+dust EL actually does.

---

## Lay summary

Two ways to read “matter on the simple metric”:

| Route | Question |
|-------|----------|
| **E-primary (S5–S6)** | Given a density/lapse, what stresses and walls does **geometry** assign? |
| **A-primary (this)** | Given the **φ action**, what densities and shapes does the **equation for φ** require or produce? |

We did **not** try to make them match. We asked what the A-primary space **contains**.

**Uncovered:**

1. Empty compensated R1 ⇒ **Coulomb** \(\phi\) (as in SIMPLE_METRIC_MACRO) — not Schwarzschild.  
2. Every free \(\phi\) **defines** a density \(\rho_{EL}\) that would source it; that density is **almost never** the Einstein density of the same shape.  
3. With free prescribed \(\rho\) and a quiet center (\(\phi=\phi'=0\)), the EL **does** drive \(\phi\) up and \(A=e^{-2\phi}\) down — but in the runs here it **did not** hit a hard \(A=0\) wall the way MS critical balls do. Different character, not a failure.  
4. Routes remain **two maps**, not one theory with a missing knob.

---

## 1. Compensated EL (definition)

\[
Z\,(r^2\phi')' = 2\rho\, r^2 e^{-2\phi}
\qquad\Leftrightarrow\qquad
\rho_{EL}=\frac{Z\,(r^2\phi')'}{2 r^2 e^{-2\phi}}
\]

Simple-metric chart: \(A=e^{-2\phi}\) (definition of the metric ansatz).

---

## 2. Free \(\phi\) catalog → \(\rho_{EL}\) vs \(\rho_E\)

| \(\phi\) family | \(\rho_{EL}\) | Einstein \(\rho_E\) | Joint? |
|-----------------|---------------|--------------------|--------|
| const | 0 | generally ≠0 unless \(\phi=0\) | only flat |
| Coulomb \(a-q/r\) | **0** (vacuum R1) | ≠0 generally | **no** (Schw ≠ Coulomb) |
| linear \(a+br\) | \(\propto e^{2br}/r\) | different | no |
| quad \(a+br^2\) | \(\propto e^{2br^2}\) | different | no |
| log | power-law-ish | different | no |
| E-ceiling \(\phi=-\frac12\ln(1-r/X)\) | \(\frac{X(2X-r)}{4r(X-r)^3}\) | \(\frac{1}{4\pi X r}\) | **no** (known residual) |
| Schw \(\phi=-\frac12\ln(1-k/r)\) | **negative** expression | **0** | no (R1 wants source; E vacuum) |

**Character:** A-primary vacuum and E-primary vacuum are **different points** in field space.  
The old ceiling shape is **not** an EL solution for its Einstein density.

---

## 3. Numeric: prescribe free \(\rho\), integrate EL

BC (regular-center probe): \(\phi=\phi'=0\) near origin. \(Z=1\). Domain \(r\lesssim 3\).

| Prescribed \(\rho\) | \(A_{\min}\) | Hit \(A=0\)? | \(\rho_E/\rho\) mid (order) |
|--------------------|-------------:|:-------------|--------------------------------|
| const 0.05 | ~0.76 | no | \(\ll 1\) |
| const 0.2 | ~0.41 | no | \(\ll 1\) |
| \(\propto 1/r\) | ~0.76 | no | \(\ll 1\) |
| \(\propto r\) | ~0.67 | no | \(\ll 1\) |
| gauss | ~0.82 | no | ~0.7 |

**Observe (not verdict against the action):**  
with this BC and these free \(\rho\), φ-driven \(A=e^{-2\phi}\) **softens** but does not reproduce the E-primary “integrate mass until compactness 1” wall in-domain.  
Also mid-point **Einstein density from the resulting \(A\)** is **not** the prescribed \(\rho\) — expected: EL does not enforce \(G=8\pi T\).

---

## 4. Uncompensated vacuum fork (scoped)

\[
Z(r^2\phi')' = 4 e^{-2\phi}
\]

Coulomb is **not** a solution (LHS=0, RHS≠0).  
Numeric probes with small center slope show \(A\) driven down (self-coupled) — **different branch** from compensated vacuum. Tag as open character, not macro pick.

---

## 5. Two maps side by side (S6 + S7)

| Feature | E-primary (S6) | A-primary (S7) |
|---------|----------------|----------------|
| Primary equation | MS / Einstein \(G\sim T\) | R1 EL for \(\phi\) |
| Vacuum | flat or Schw | Coulomb (compensated) |
| Wall \(A=0\) | critical \(M=X/2\) when mass enough | not seen in these regular-BC free-\(\rho\) runs |
| Free continuum | continuous \(p\)/\(\alpha\) map | free \(\phi\)⇒\(\rho_{EL}\); free \(\rho\)⇒ numerically integrated \(\phi\) |
| Glue | — | **not** by residual erasure |

**Still pure math exploration of two operator packages on one metric.**  
Which package is native UDT macro remains **open** (Charles / deeper action) — not closed by residual hunting.

---

## 6. Refused

| Move | |
|------|--|
| Add coupling so \(\rho_{EL}=\rho_E\) on ceiling | mechanism |
| Declare R1 dead because ≠ Einstein | merit judgment / wrong route war |
| Declare Einstein dead because R1 is “the action” | same |
| Pick free-\(\rho\) EL run with smallest \(A_{\min}\) as cosmology | shopping |

---

## One-line

**A-primary R1 space is real and different: vacuum Coulomb, free φ⇒ρ_EL catalog, free-ρ EL softens A without E-primary critical walls in these runs, and ρ_E≠ρ_EL generically — two maps, no glue, no winner.**
