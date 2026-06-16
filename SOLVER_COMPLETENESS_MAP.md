# SOLVER COMPLETENESS MAP — the UDT-native solver coverage ledger

Living document (started 2026-06-16). The metacognitive "solver-architect" view
(Charles 2026-06-16): the real project is a COMPLETE, numerically-tractable,
UDT-NATIVE solver that drops NO potentially-emergent sector/effect/operator and is
honest about its regime of validity. Every result is ONE TILE here, with a regime
stamp, next to the still-blank sectors. Update at every push. Append-style; correct
statuses as coverage changes.

LEGEND: [V]=solved native + blind-verified · [v]=solved/validated (lighter) ·
[R]=solved but REDUCED (scoped) · [E]=examined separately · [ ]=untested ·
[!]=known blind-spot/open.

## A. METRIC DEGREES OF FREEDOM (the 10 components)
- [V] g_tt, g_rr diagonal warps, B=1/A FREE (independent) — radial #56 (blind-verified);
      2-D axisym spectral #59.
- [v] g_θθ, g_ψψ angular metric — carried in 2-D spectral #59 (axisym).
- [E] time-row / shear off-diagonals g_tr, g_tθ, g_rθ — #57 found them LINEARLY
      DECOUPLED on the round background; NOT solved nonlinearly with structure. [!] partial.
- [ ] rotation / twist off-diagonals g_tψ, g_rψ, g_θψ (angular momentum) — UNTESTED. [!]

## B. COORDINATES / DIMENSIONS (t, r, θ, ψ)
- [V] r (radial) — #56.
- [v] θ (polar) — 2-D spectral #59.
- [!] ψ (azimuth) — UNTESTED; the non-axisymmetric blind spot. (full-3-D build IN PROGRESS)
- [E] t (time) — STATIC solved; time-periodicity SELECTOR examined #57 (seal = interval,
      not a circle; ω₁ depth-flat ⇒ no classical selector). Fully-dynamic evolution [ ].

## C. MATTER (winding field n, charge m, depth p)
- [V] Θ(r) radial profile — #56.
- [v] Θ(r,θ) angular shape, matter FREE — 2-D spectral #59 (charge-1, axisym; corrected EL).
- [v] winding m=1 — ground state, round (spherical).
- [R] winding m=2,3 — found grid-stable (#52d/#57d) but shapes/masses NOT mapped. (3-D build)
- [ ] winding m≥4 — UNTESTED.
- [V] depth p (dilation) — continuous family, super-exponential M(p), NO native selector
      (#54/#56; the lepton-relevant same-charge axis).

## D. ACTION TERMS
- [V] L2 (two-derivative) — settled, audited clean.
- [V] L4 (Skyrme stabilizer) — settled; radial EL correct (#56). [!] the 2-D off-round L4
      EL had a BUG (axisym_matter_el.py, found by verifier 7cf94053) — corrected
      (axisym_matter_el_CORRECT.py); the 3-D EL must be generated correct (div-identity test).
- [V] seal / boundary (same-minus = time-reversal) — radial/2-D.
- [V] κ8 back-reaction coupling — FREE dial; over-collapse existence ceiling κ8*(p),
      NON-critical (Path 2, #52); criticality conjecture NOT supported in this regime.

## E. DYNAMICAL REGIME
- [V] static (∂_t=0).
- [ ] stationary rotating/twist (g_tψ etc.) — UNTESTED. [!]
- [E] time-periodic — examined #57 (no classical selector; closed-time hinge underived).
- [ ] fully dynamic (NR-grade evolution) — NOT attempted. [!]

## F. SYMMETRY SECTOR
- [V] spherical (charge-1 ground state).
- [v] axisymmetric (r,θ) — 2-D spectral #59.
- [!] NON-axisymmetric (ψ-dependent; platonic higher-winding types) — UNTESTED; the most
      likely home of a Skyrme-type distinct-shape catalog. (full-3-D build IN PROGRESS)

## G. SCALE REGIME
- [V] shallow ↔ deep φ — radial to p≈6 (#56); bulk swept to p≈-40 pre-L4 (#39).
- [V] weak ↔ strong κ8 — to the over-collapse ceiling (#52).

## H. QUANTUM (ħ) SECTOR
- [E] fermion statistics / the coin — #51/#53: classically FREE, NOT derived (postulated,
      like the SM); SHELVED per the observation-led reframe.
- [!] Euclidean time-circle discreteness (standard QSM origin of discreteness) — flagged,
      UNTESTED; distinct from the shelved SM-fermion line.

## TRACTABILITY MAP (what the numerics reach)
- TRACTABLE NOW: 1-D radial coupled Einstein+L2+L4 (#56); 2-D axisym SPECTRAL coupled solve
      (Cheb_r × Legendre_θ), exponential convergence, matter free (#59). Continuation (depth).
- WALLED (being opened): full-3-D nonlinear — FINITE-DIFFERENCE failed (#57/#58 coordinate-
      spike ill-conditioning); SPECTRAL 3-D (Cheb_r × spherical-harmonics) is the cure, IN
      PROGRESS (this build).
- NOT YET BUILT: fully-dynamic (time-evolution) NR-grade solver; the quantum-sector machinery.
- TOOLING CORPUS being mined (category-A, NR): spectral elliptic methods, self-consistent-
      field (KEH/Hachisu), gravitating-Skyrmion/boson-star solvers, pseudo-arclength continuation.

## THE TEN COMPLETENESS CRITERIA (the mathematically-complete governing set;
## refined 2026-06-16 from Charles's "sectors/effects/operators" — his words map as
## operators→2; sectors→4,6,7; effects→8,9). A variational field theory's FULL solution
## space is exhausted iff all ten are covered. Each push declares its status on each.
## LAYER 1 — what you're solving:
##  1. FIELDS (every varying DOF: 10 g_μν + matter + φ).
##  2. ACTION TERMS (every term: L2,L4,gravity,seal/boundary) — the "operators".
##  3. FULL EQUATIONS (every variation of every field — NEVER a subset; the #55 scar).
##  4. DOMAIN & COORDINATES (r,θ,ψ,t live unless a STATED symmetry; the 2-D-in-4-D scar).
##  5. BOUNDARY & REGULARITY (seal, center/axis, finite cell — they SELECT solutions).
## LAYER 2 — which world:
##  6. TOPOLOGICAL SECTOR (winding/charge m — each a disconnected world).
##  7. DYNAMICAL CHARACTER (sit=static / spin=stationary / ring=time-periodic / evolve=dynamic;
##     elliptic vs eigenvalue vs hyperbolic; the time-selector lives in "ring").
## LAYER 3 — what emerges:
##  8. BRANCH / BIFURCATION STRUCTURE (are there OTHER disconnected solutions? = the CATALOG).
##  9. STABILITY SPECTRUM (which solutions persist; a "particle" = a STABLE solution).
## 10. REGIME OF VALIDITY (scale/coupling range; where the math changes character).

## STANDING COMPLETENESS QUESTIONS (run every push)
1. For EACH of the ten criteria: what does this push cover, and what does it DROP (explicitly)?
2. Could any DROPPED criterion host emergent structure? If yes ⇒ flagged blind-spot, not a closure.
3. State the REGIME OF VALIDITY (criterion 10) of the result.
4. Is every technique category-A (conditioning) — not category-B (physics simplification)?
5. What tooling/tractability step covers the dropped criteria next?
6. (anti-inflation) This is ONE tile — how much of the ten-criteria space is still blank?

## CURRENT HEADLINE (honest, regime-stamped)
UDT NATIVELY PRODUCES MASS (#56, the milestone): a self-consistent full-(radial)-Einstein
soliton, no imports. NO classical discrete catalog YET found — but only the CHARGE-1,
STATIC, AXISYMMETRIC, matter-deforming tile has been genuinely searched (#59). The most
likely catalog home — NON-AXISYMMETRIC + HIGHER-WINDING + rotation/twist — is still BLANK,
and is what the full-3-D spectral build targets. Time-dynamic and quantum sectors remain open.
