# OBSERVE-2 — Vacuum B throat family (no polar origin)

**Date:** 2026-07-08  
**Mode:** OBSERVE (not target). Incremental after OBSERVE-1.  
**Equations:** `macro_FE_LOCKED_W_uncompensated.md` (W=1, free D, L_m=0)  
**Script / data:** `macro_vacuum_B_observe2.py`, `macro_vacuum_B_observe2_data.json`  
**Prior tile:** `macro_vacuum_B_observe1_results.md` (polar smooth origin blocked)  
**Status:** PROVISIONAL characterization — one solution-space tile.

---

## Premise ledger

| Item | Tag |
|------|-----|
| W = 1, vacuum | CHOSE / scoped |
| Seed: \(D_*>0\), \(D'_*=0\) at \(r_*\) (throat) | FREE family (natural if no polar pinch) |
| Two-sided IVP in/out of \(r_*\) | method |
| \(Z \in \{1,4,8\}\), \(u_*=\phi'_* \in \{0,\pm0.05,0.1,0.2,-0.1\}\) | FREE scan, not fit |
| \(\phi_*=0\), \(D_*=1\), \(r_*=1\) (plus D_* variation) | chart / scale choice FREE |
| Observing or targeting? | **Observing** |

---

## Analytic (throat)

At a throat \(D'=0\), FE-D gives immediately:

\[
D''(r_*) = -\frac{Z}{4}\, D_*\, e^{2\phi_*}\, (\phi'_*)^2
\]

| Case | Meaning |
|------|---------|
| \(\phi'_* \neq 0\), \(Z,D>0\) | \(D''_* < 0\) → **local maximum** of sphere size |
| \(\phi'_* = 0\) | \(D''_*=0\); with \(\phi\) flat → exact constant solution |

**Plain:** if dilation is still changing at the widest sphere, the geometry **cannot stay at that width** — size falls off on both sides of the throat.

CAS: `implies_D2 = [-D0*Z*u0**2*exp(2*p0)/4]`.

---

## Numerics (two-sided IVP)

**Method:** DOP853; out to \(r=5\), in to \(r=0.05\); stop if \(D\to0\) or \(|\phi|>20\).  
**Residual spot-check** (outward from throat, Z=1, u=0.1): flux residuals ~1e−6 abs / ~1e−3–1e−2 rel.

### Pattern (all non-flat seeds in the box)

1. **D is a local max at the throat** — both sides drop away from \(D_*\) (or stay flat only if \(u_*=0\)).
2. **Outward (\(r > r_*\)):** \(D\) decreases; for larger \(|u_*|\) and larger \(Z\), can hit **\(D \to 0\)** in finite \(r\) (e.g. u=0.2 with Z=4 or 8).
3. **Inward (\(r < r_*\)):** \(D\) also decreases away from throat; in this box, inward to \(r=0.05\) usually **survives** without hitting zero (mild \(D\) loss).
4. **φ with \(u_*>0\):** φ increases with \(r\) (higher φ outward); inward, φ lower than at throat.
5. **φ with \(u_*<0\):** opposite tilt — still \(D''_*<0\) (depends on \(u^2\)).
6. **Flat seed \(u_*=0\):** exact constant \(D,\phi\) both ways — recovers trivial vacuum.
7. **Flux mono F↓, G↑:** held on successful runs.

### Z trend (qualitative)

Larger Z → **stronger** \(D''_* \propto -Z u^2\) → faster pinch of \(D\) away from throat for fixed \(u_*\).  
(Opposite “feel” from OBSERVE-1 expand family, where large Z softened φ for fixed D′ seed — different IC class.)

### D_* variation (Z=1, u=0.1, D_* ∈ {0.5,1,2})

Same qualitative throat-max behavior; all reached r bounds in this mild box.

---

## How this sits next to OBSERVE-1

| Tile | Finding |
|------|---------|
| O1 | Smooth **polar origin** inconsistent with vacuum B |
| O2 | **Throat** (finite D, D′=0) is allowed; non-flat → **bulge** in D, φ tilts; may pinch D→0 outward |

Together (scoped): vacuum B likes **finite minimum coordinate domains with a maximum sphere size**, not a smooth ball-with-point-center — unless further structure (sources, different W, singular φ) is added later.

**Not claimed:** that this *is* the universe, BAO, or an edge. Only what the vacuum ODE family contains.

---

## What this does *not* say

- Does not activate fallback C (B still has a nonempty smooth family: throats + trivial).  
- Does not require sources yet (Charles gate: sources later).  
- Does not fix Z or match data.  
- Does not prove global existence for all ICs (strong u / Z hit D=0).

---

## Incremental next (when ready)

1. **OBSERVE-3:** phase portrait / nondimensional reduce (how many true free parameters after scaling)  
2. **OBSERVE-3b:** longer inward runs — does D always hit 0 at finite r_in for any u≠0?  
3. Map “survival window” in (Z, u_*, D_*) for both sides open  
4. Still later: L_m  

Recommend **3b + survival window** before sources — keeps vacuum map complete enough to know what matter would change.

---

## Plain summary

Starting where the sphere is widest and not yet changing size: if φ is still sloping, the equations force that width to be a **peak** — spheres get smaller both inward and outward. Mild slopes give smooth profiles over a finite range; steep slopes or large Z can pinch the sphere size to zero on the outside. Flat φ at the throat is just the constant vacuum. No polar point-center was used. Still vacuum only.
