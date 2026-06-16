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
- [v] ψ (azimuth) — OPENED (#60, full3d_catalog_results.md): Fourier-ψ spectral
      basis machine-exact; the ROUND #56 soliton recovered in the full-3-D (ψ-live)
      basis (M_MS=0.281, gate PASS). Criterion-4 ψ-DOMAIN now covered for the round
      solution. (OFF-ROUND ψ-shaped solve = solver-limited, see F / 8.)
- [E] t (time) — STATIC solved; time-periodicity SELECTOR examined #57 (seal = interval,
      not a circle; ω₁ depth-flat ⇒ no classical selector). Fully-dynamic evolution [ ].

## C. MATTER (winding field n, charge m, depth p)
- [V] Θ(r) radial profile — #56.
- [v] Θ(r,θ) angular shape, matter FREE — 2-D spectral #59 (charge-1, axisym; corrected EL).
- [v] winding m=1 — ground state, round (spherical).
- [R] winding m=2,3 — found grid-stable (#52d/#57d); 3-D EL now carries winding m
      (matter_el_3d_gen.py, correct), seeds built (#60) but shapes/masses NOT mapped
      — OFF-ROUND solve solver-limited (#60). Still [R].
- [ ] winding m≥4 — seed built (#60) but solver-limited; UNMAPPED.
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
- [E] NON-axisymmetric (ψ-dependent; platonic/higher-winding types) — MACHINERY BUILT
      + ROUND-GATE PASS in 3-D (#60: pole-stable analytic 3-D Einstein, correct 3-D
      matter EL machine-zero on round + symbolic div(T) ν=r exact, Fourier-ψ). SEARCH
      itself SOLVER-LIMITED (off-round coupled-solve convergence gap — the axisym
      CONTROL that #59 relaxes does NOT relax cleanly here). Catalog binary OPEN, NOT
      banked. Residual: full off-diagonal METRIC + full S³ matter map (F,G,H).

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
- PARTLY OPENED (#60): full-3-D SPECTRAL (Cheb_r × GL_θ × Fourier_ψ) cures the #57/#58
      coordinate-spike for the GEOMETRY/EL (pole-stable analytic 3-D Einstein flat=0 /
      Schwarzschild exp / 2-D-match 1e-14; correct 3-D matter EL machine-zero on round +
      symbolic div(T) ν=r exact) AND recovers the round soliton in the 3-D basis (gate
      PASS, M_MS=0.281). REMAINING WALL: the OFF-ROUND coupled SOLVE convergence — the
      matrix-free Jacobi-PCG LM does not drive off-round angular configs (incl the
      axisym control #59 relaxes) to a clean floor in feasible cost. The non-axisym /
      higher-winding catalog SEARCH is gated on a faster off-round 3-D solver (dense-LM
      on a moderate grid / Newton-Krylov w/ elliptic preconditioner / block SCF).
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
soliton, no imports. NO classical discrete catalog YET found in the genuinely-searched
CHARGE-1 STATIC AXISYMMETRIC matter-deforming tile (#59). The full-3-D spectral build
(#60) now has the CORRECT, POLE-STABLE 3-D MACHINERY (analytic Einstein, correct off-round
matter EL, Fourier-ψ) and RECONFIRMS the round soliton in the 3-D ψ-live basis (gate PASS,
M_MS=0.281) — but the NON-AXISYMMETRIC + HIGHER-WINDING catalog SEARCH is SOLVER-LIMITED
(off-round coupled-solve convergence gap; the axisym control #59 relaxes does not relax
cleanly here), so that catalog home is still OPEN (NOT banked, not a negative). The gap is
now isolated to OFF-ROUND 3-D SOLVE TRACTABILITY (the next build), not the physics content.
Time-dynamic, rotation/twist, full-off-diagonal-metric, full-S³-matter, and quantum
sectors remain open.

## STANDING-QUESTION ANSWERS — push #60 (full-3-D spectral)
1. COVERS: criteria 1-5 for the diagonal-Weyl/single-Θ 3-D class incl. ψ (criterion-4
   OPENED, round gate). DROPS (explicit): spatial off-diagonal metric g_rθ/g_rψ/g_θψ;
   full S³ matter map (F,G,H) [single-Θ is restricted non-axisym]; twist (crit-7);
   off-round CONVERGENCE for crit-6/8/9.
2. Could a dropped criterion host structure? YES — the non-axisym catalog (crit-8) and
   winding shapes (crit-6) are exactly what could not be searched ⇒ flagged blind-spot,
   NOT a closure. The off-diagonal metric + full S³ map are the most likely missing DOF.
3. REGIME: validated machinery + round gate basis-robust at (p=0.4, kap8=0.05, 14L). The
   off-round search has NO established regime (did not converge).
4. Category-A? YES — every technique conditioning, proven (flat/Schwarzschild/round/2-D-
   match/machine-zero EL/div-identity). NO category-B. The honest limit is SOLVER speed.
5. Tooling next: a faster off-round 3-D solver (dense-LM on a moderate grid / Newton-
   Krylov with an elliptic preconditioner / metric-matter block SCF) to drive off-round
   to a clean floor (Phi~1e-9 with the axisym control round-recovered), THEN re-run the
   non-axisym + winding search.
6. ONE tile: the 3-D non-axisym/winding CATALOG verdict is still BLANK; what is newly
   filled is the 3-D ROUND recovery + the correct 3-D physics machinery.
