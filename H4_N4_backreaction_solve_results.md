# H4 · N4 — Backreaction / mass solve: OUTCOME D (tool-limited), with a solid Phase-A reduction + source

> **★ RECLASSIFIED D-BUDGET → D-SOURCE-FRAME (2026-07-06, N4a `H4_N4a_source_background_audit_results.md`,
> blind-verified).** The source-background audit found the response operator here is the locally-flat / source-free
> approximation and DROPS the ambient self-screening term +8e^{−2φ_amb}δφ (the Branch-P source 4e^{−2φ} is
> φ-dependent). The bare-Euler BVP "clean next step" below would return a SPURIOUS clean monopole and MUST NOT be
> run as-was. The CF1/CF2 gap is therefore NOT merely response-solve budget — it includes a genuine FRAME
> uncertainty: whether a clean far-field monopole mass exists at all is set by the OPEN G/P switch criterion for
> the hopfion far field (clean δm=−δq in a Branch-G/shallow exterior; screened / log-periodic / no-clean-monopole
> in a deep Branch-P ambient). SOLID + INTACT: Phase-A ALGEBRA (only δh^(1) needed; flux=½⟨T,L⁻¹T⟩ — correct under
> its source-free premise, i.e. a Branch-G/shallow statement); the Phase-B source; the no-stress-only-shortcut
> departure; frame C(a) (no seal). The revised N4 must rebuild the operator on the true φ_amb(r) with screening and
> report the mass CONDITIONALLY. CF1 "leans δq≠0" and CF2 "open" stand as Branch-G/shallow statements.

**Status: BANKED, blind-verified (2026-07-06). Outcome D (tool-limited) — HONEST, not a dodge.** The symbolic
Phase-A reduction and the source characterization are SOLID and bankable; the load-bearing linear tensor
response-solve (which certifies the CF1/CF2 sign+magnitude) was not closed within bounded budget. **CF1 (does the
hopfion have a flux-mass, δq≠0?) LEANS YES (supported, not certified). CF2 (sign of δm) OPEN — both A (+mass) and
C (−mass, prime risk) live. CF3 (pinning) = D (below the H3 ~1% noise floor).** Executed the frozen
`H4_N4_backreaction_solve_preregistration.md`, DERIVE-then-EVALUATE, under frame C(a). Solver agent
a9073db162d6d6456; blind adversarial verifier af34ae7d0781fb7bd (all 6 targets PASS; could NOT break the crux
reduction and could NOT find a missed shortcut). Scripts: `h4_scripts/h4_n4_phaseA_{expansion,totalderiv,operator}.py`,
`h4_n4_phaseB_stress.py`. DATA-BLIND; Z_φ symbolic; no ξ-anchor; no GR minimal coupling.

## SOLID Phase A — the O(amp²) flux reduces to a LINEAR response (verified two independent ways)
Expanding √h𝒦 = −½e^{−2φ}(a'b'−s'²)/√(ab−s²) (N1) to second order about the round ambient (C(a): e^{−2φ₀} pulled
out as a constant over the localized core):
- **Only δh^(1) is needed (the crux).** The first-order flux density g₁ is an EXACT total r-derivative
  (g₁ = d/dr[−(α sin²θ+β)/(r|sinθ|)] + 4δφ|sinθ|), so ∫g₁ dr = 0 over compact support for ANY perturbation
  (verified: machine-zero). Because g₁ applied to the genuine second-order piece δh^(2) is ALSO a total derivative
  (g₁ is linear in its argument), **δh^(2) drops from the net flux entirely** — the O(amp²) flux is the bilinear
  (δh^(1))² term ALONE. ⇒ the whole solve reduces to the LINEAR transverse response δh^(1) = −L⁻¹T. (Verifier
  independently re-derived g₁ keeping the φ-perturbation the driver had frozen, and confirmed the δh^(2)→0 logic —
  no δh^(2)×background cross-term exists. This is the load-bearing reduction and it holds.)
- **Variational mass:** L is simultaneously the Hessian of the flux functional ∫√h𝒦 AND the linearized E^{AB}
  (E^{AB}=δS_geo/δh). Hence Lδh^(1)=−T ⇒ flux = ½⟨δh,Lδh⟩ = −½∫δh^(1)_{AB}T^{AB} d³x = **½⟨T, L⁻¹T⟩**, so
  **δm = −δq = (e^{−2φ₀}/4πZ_φ)⟨T, L⁻¹T⟩**. The sign of δm is the DEFINITENESS of L⁻¹ projected on the hopfion
  stress — NOT pre-determined. The irreducible core is the velocity-bilinear −½ det(∂_rδh)/√h₀, demonstrated
  **sign-indefinite** (aligned a'b'>0 → one sign, anti/pure-shear → the other). L is Euler-type
  (r²f''−2rf'+2f; indicial roots 1,2), analytically tractable; the DeWitt trace/shear sectors carry the competing
  signs.
- **★ Native "no stress-only shortcut" departure (load-bearing, anti-import).** phase1_geon read its O(A²) mass
  from a stress-only Hamiltonian/Misner–Sharp constraint (no metric solve). **That does NOT transfer to UDT:**
  φ-blindness (δS_m/δφ=0) removes the linear T→φ channel, so matter T enters the flux only at O(amp¹) (which
  integrates to zero); the net O(amp²) flux-mass is IRREDUCIBLY the geometric response δh^(1) = −L⁻¹T. Using
  G=8πT or an MS stress-only reading would be the GR smuggle. (Verifier searched for a native shortcut via the
  trace relation 𝒦=Z_φφ'²−h∂π+T — φ'² is O(amp⁴), 𝒦 is intrinsically quadratic in K∝∂_rh, so the constraint
  re-expresses but does not linearize 𝒦: **no native stress-only reading exists.**) ⇒ a real tensor response solve
  is genuinely REQUIRED — this is WHY N4 lands at D rather than closing on paper.

## SOLID Phase B — the source (resolved H3 field `prod_an256.npz`, N=256, L=6)
Native Faddeev–Skyrme static transverse stress T^{AB}(r,θ) from the fixed field (E=286.52, E2/E4=0.9995;
virial ∫tr(σ)=−E2+E4 to 14 digits). Shell-projected:
- **Genuine, nonzero, LOCALIZED, sign-varying** transverse stress; compact support (→0 by r≈5; <0.04% weight
  beyond r=5) ⇒ **read-surface-INDEPENDENT** (no box-control from the source side).
- Sector integrals 4π∫r²⟨·⟩dr: **transverse-trace ≈ −90.1, shear ≈ +139.1, T_rr ≈ +89.9** (trace+T_rr ≈ 0,
  virial-consistent). Both DeWitt sectors strongly + comparably excited with **OPPOSITE integrated signs** — the
  net flux is a difference of competing O(100) terms = exactly the phase1_geon-type prime-risk (negative-mass) structure.
- **δm_geo (geometric/MS mass) = the L2+L4 hopfion energy = +286.5 (positive).** This is a DIFFERENT object from
  the flux-mass (MAP-B: geometric mass is nonzero even at φ≡const, D2-E1) — it does NOT settle CF1/CF2. We did NOT
  assume δq = the energy (that is the untested plausibility lead).

## CF verdicts
- **CF1 (δq≠0?): LEANS YES — supported, not certified.** The source is a genuine nonzero sign-varying O(amp²)
  stress; δq=0 would require an accidental cancellation of a sign-indefinite quadratic form ⟨T,L⁻¹T⟩ — non-generic.
  Outcome B (massless/inert) is DISFAVORED. Certification needs the L⁻¹ contraction (not performed).
- **CF2 (sign of δm): OPEN.** δm ∝ ⟨T,L⁻¹T⟩ = whether the Green's-function-weighted shear(+) beats the trace(−).
  Genuinely undetermined without the solve; the sign was NOT steered (no import of GR's conformal-mode-negative
  signature — Principle 7). Both A (+mass) and C (−mass, the pre-registered prime risk, phase1_geon m/A²≈−0.905) live.
- **CF3 (pinning): D.** Subleading O((ℓ_hopf/r)²) gradient on an O(amp²) well — below the H3 ~1% precision floor.

## Frozen-outcome classification: D (tool-limited) — honest
Phase A complete + rigorous; source robustly computed; but δh^(1) = −L⁻¹T (the load-bearing response) was not
closed in bounded budget. Per the pre-reg + honesty gate, classify **D**, with CF1 leaning against B. **The
CF1/CF2 gap is response-solve BUDGET, NOT signal-below-noise** (source ~O(100) ≫ the 1% floor of 286); only CF3 is
genuinely below noise.

## The clean next step (a bounded, well-posed solve — NOT H5; certifies CF1/CF2)
Solve δh^(1) = −L⁻¹T per ℓ-sector (ℓ=0 and ℓ=2, by the source's axisymmetry) — a standard **Euler 2-point BVP**
(Green's function of r²f''−2rf'+2f, roots 1,2), then contract ½⟨T,L⁻¹T⟩ for δq's sign+magnitude. **Two owed
checks the solve MUST include** (verifier, inherited/owed — not new smuggles): (i) the true-φ_amb(r) correction to
the locally-flat operator = the N2-owed shear-decay exponent (round+φ≡0 is not a vacuum); (ii) **box-control:** if
δh^(1) GROWS rather than decays, the flux is box-controlled = a pre-registered D sub-outcome — must be checked, not
assumed. This is bounded (linear ODE Green's functions), one foreground process, anti-hang-safe; it CERTIFIES CF1
and RESOLVES CF2. It completes N4; it is not a new phase.

## Provenance / discipline
No GR minimal coupling (the no-shortcut argument IS the anti-import guard); no ξ-anchor asserted; Z_φ symbolic
(only e^{−2φ₀}=w0 pulled out, never numeric); frame C(a) honored (constant ambient, bulk read-surface, no private
seal); no particle labels/masses/data. H3 precision caveats separate + non-gating for CF1 (source ≫ 1% floor).
CF2 genuinely open (may return +mass, massless, or −mass — pre-registered, not retrofitted).
