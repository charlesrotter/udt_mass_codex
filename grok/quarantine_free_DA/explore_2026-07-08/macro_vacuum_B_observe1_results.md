# OBSERVE-1 — Vacuum option B (W=1), free D, no sources

**Date:** 2026-07-08  
**Mode:** OBSERVE (not target). Slow / incremental.  
**Equations:** `macro_FE_LOCKED_W_uncompensated.md`  
**Script / data:** `macro_vacuum_B_observe1.py`, `macro_vacuum_B_observe1_data.json`  
**Status:** PROVISIONAL characterization — not a go/no-go on the metric; one tile of solution-space.

---

## Premise ledger

| Item | Tag |
|------|-----|
| W = 1 (option B) | CHOSE (Charles) |
| Z free; used {1, 4, 8} as representatives | FREE (not fit to data) |
| L_m = 0 | CHOSE (vacuum first) |
| Static spherical diagonal | FREE first slice |
| IVP from r₀ > 0, D₀ > 0 | FREE (avoids polar chart issue; see §2) |
| Observing or targeting? | **Observing** — no SNe/BAO/CMB targets |

---

## What we asked

What does the **vacuum** system do?

\[
\frac{\mathrm{d}}{\mathrm{d}r}(Z D^2 \phi') = 4 e^{-2\phi}(D')^2, \qquad
\frac{\mathrm{d}}{\mathrm{d}r}(e^{-2\phi} D') = -\frac{Z}{4} D (\phi')^2
\]

No sources. No sky. Report structure.

---

## §1 Exact / structural facts (analytic)

### 1.1 Trivial vacuum

\(\phi = \mathrm{const}\), \(D = \mathrm{const}\) solves both equations.  
**Numerics:** held to machine path (status ok, flat fluxes).

### 1.2 Flux monotonicity (Z > 0, D > 0)

| Flux | Definition | Property |
|------|------------|----------|
| \(F = e^{-2\phi} D'\) | “weighted expansion rate” | **nonincreasing**; strictly ↓ where \(\phi' \neq 0\) |
| \(G = D^2 \phi'\) | “weighted φ-gradient” | **nondecreasing**; strictly ↑ where \(D' \neq 0\) |

CAS/logic from FE signs; confirmed on all successful IVPs in the survey.

**Plain:** once φ starts changing, it tends to keep “charging” G; once spheres expand or contract, F only gets more negative or less positive — expansion is eroded by any φ gradient.

### 1.3 Z is a real parameter

Cannot remove Z by rescaling φ alone (\(e^{-2\phi}\) blocks it). Representative scan {1, 4, 8}: larger Z → milder φ growth for similar ICs (kinetic stiffer).

---

## §2 Regular polar origin — obstruction (scoped)

**Question:** Can we have a smooth geometric origin \(D(0)=0\), \(D'(0)=d_1 \neq 0\), even smooth \(\phi\)?

**CAS (sympy series of FE-φ):**

\[
(\mathrm{LHS} - \mathrm{RHS})\big|_{r=0} = -4\, d_1^2\, e^{-2\phi_0}
\]

- LHS of FE-φ is \(O(r^2)\) for even smooth φ and \(D \sim d_1 r + \cdots\)  
- RHS is \(4 e^{-2\phi_0} d_1^2 + O(r^2)\)  
- **Inconsistent unless \(d_1 = 0\)**  
- With \(d_1 = 0\) and \(D \sim r^k\) (higher), leading balance still fails for smooth φ (e.g. \(D \sim r^3\) leaves \(O(r^4)\) residual)

**Scope (honest):** this is an obstruction to a **smooth regular polar origin** under **vacuum B**, not a proof that “B is dead.” Alternatives still open:

- No polar origin (D never zero) — chart covers a shell / finite cell without a point center  
- Singular φ at origin (not pursued this step)  
- Sources later (not this step)  
- Fallback C if B’s intended regimes all block (not declared yet)

**Near-polar IVPs** (start at small D₀ with v₀=1, r₀=D₀): integrate forward fine — they do **not** construct a smooth solution *through* r = 0; they only show the ODE is runnable away from the origin.

---

## §3 Numerical survey (bounded IVP)

**Method:** DOP853, rtol 1e−9, from r₀ = 0.5, D₀ = 1, φ₀ = 0 (chart), mild (φ′, D′); r up to 4.  
**Residual spot-check** (mild_expand, Z=1): flux derivatives match RHS at ~1e−3 relative (np.gradient noise); mono F/G clean.

### Patterns observed

| Class | Behavior (scoped to IC box) |
|-------|-----------------------------|
| **Trivial** | Stays flat |
| **Mild expand** (D′>0, small φ′) | D grows; **φ rises**; F↓, G↑; runs to r_max for Z∈{1,4,8} |
| **Near flat** | Same direction, small amplitude |
| **φ′ < 0 initially** | G nondecreasing: can climb through zero; φ may dip then rise (Z=1) or stay down if G stays negative longer (higher Z in this box) |
| **Mild contract** (D′<0) | D decreases to 0 in finite r; φ rises hard; F → large negative — **terminates** at D→0 |

**Not observed in this box (and not claimed absent globally):**

- φ → −∞ outer “edge”  
- oscillatory φ (redshift law remains e^{Δφ}; profiles here were monotone or single-dip)  
- need for sources to have *any* smooth solution — free-D vacuum solutions **exist** off the polar origin

### Z trend (qualitative, same ICs)

Larger Z → smaller φ excursion on expand family (Z=1: φ up to ~0.85; Z=8: ~0.18 on mild_expand). Consistent with heavier kinetic weight.

---

## §4 What this does *not* say

- Does **not** say vacuum B fails cosmology (no data comparison).  
- Does **not** say sources are required (Charles: add later; intuition not used as evidence).  
- Does **not** activate fallback C — polar obstruction is real but **regime-scoped**; free-D shell-type solutions exist.  
- Does **not** fix Z.

---

## §5 Incremental next options (when ready — not auto-launched)

Ordered slow → richer:

1. **OBSERVE-2:** reverse IVP / two-sided from a throat (D′=0, D>0) — natural “no polar origin” family  
2. **OBSERVE-3:** classify phase portrait in (F, G) or (φ′, D′/D)  
3. **OBSERVE-4:** frozen D=r specialization only as contrast (known hard at origin)  
4. Only later: continuum L_m  

Recommend **1** next if we continue vacuum B.

---

## §6 One-paragraph plain summary

Under the locked vacuum equations with angular weight uncompensated, **constant** φ and D is a solution, and **smooth expanding** solutions with finite sphere size also exist: φ tends to increase as the spheres change size, with clear flux rules. A **smooth point-center** (spheres pinching to zero radius like ordinary polar coordinates) **does not** work for smooth φ — the equations disagree at leading order. Collapsing spheres hit zero size with φ blowing up. We have **not** put matter in yet; nothing here forces sources — it only maps vacuum behavior. Z still free; larger Z softens φ response in the samples we ran.

---

## Verifier note

Driver CAS + IVP mono checks + one residual spot-check. **Not** a blind adversarial agent pass — appropriate for OBSERVE-1 tile; bank any stronger claim only after verifier-before-record.
