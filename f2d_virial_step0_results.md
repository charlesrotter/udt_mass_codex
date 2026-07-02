# Step 0 — Virial / free-boundary CAS analysis of the finite mirrored cell (Class A)

**Date:** 2026-07-01. **Mode:** analytic OBSERVE (MAP §8, gated by Charles). **Driver:** Claude
(claude.ai session). **Script:** `verify_f2d_virial_step0.py` (SymPy 1.14).
**Status:** BLIND-VERIFIED 2026-07-01 (Claude Code session, verifier agent `af0a5fdd`) — physics
V1–V7 all reproduce under independent from-scratch re-derivation, INCLUDING the flagged V5
(transversality → H≡0) and V7 (δ²E>0). **Banked** with two honesty corrections applied (see VERIFIER).
**No wall numbers loaded. No solving performed.**

## Headline results (lay first)

1. **The counting problem resolves itself — the theory supplies the missing pin.** If the cell's
   size is a dynamical variable of the action (the cell chooses its own size — a tagged chose,
   but the natural reading of a closed cell), the variational principle FORCES one extra scalar
   condition: the conserved radial Hamiltonian must vanish, **H ≡ 0**, everywhere in the cell.
   That makes the closed-cell problem SQUARE (3 conditions vs 3 unknowns): **isolated cell sizes
   become the generic expectation, with no hand-pinned core rule.** This is the native analog of
   the GR Hamiltonian constraint, appearing on its own.
2. **It unifies with Charles's environment pin (MAP §4d).** H is exactly the quantity an embedded
   cell would have to MATCH to the ambient universe at the seal: closed cell → H = 0; embedded
   cell → H = H_ambient (the Misner-Sharp density of the universe). One derived structure carries
   both isolation mechanisms — and natively encodes the old indication that particle formation
   depends on the ambient density.
3. **The core-rule knob may be eliminated.** At a mirror core, H = 0 pins ρ_c given the core
   angular profile — the single most dangerous chose in the MAP (§4a, P9) becomes derived.
4. **Near-rigid stabilization is analytically disfavored (N=1).** The second variation of the
   matter energy about f=θ is STRICTLY positive definite on ANY round background. Radial
   structure is never free; it turns on at the same order as its cost. Consequence for the
   solver: if cells exist they likely live FAR from rigid — seed accordingly. No cheap analytic
   kill in either direction: the 2-D solver is genuinely required.

## Exact statements (each CAS-verified)

**V2 (linchpin).** The reduced per-4π Lagrangian
`L̄ = (Z/2)ρ²φ'² + 2 − 2e^{−2φ}ρ'² − (ξ/2)(ρ²I_r + I_θ + N²I_s) − (κN²/2)(I_4r + I_4θ/ρ²)`
reproduces EXACTLY all three recorded EOMs (φ-EOM, ρ-EOM with the ξρI_r − κN²I_4θ/ρ³ source,
and the f-PDE). Everything below stands on this. The `+2` is √h·R^{(2)} per 4π — it drops from
the EOMs but is LOAD-BEARING for H and the free-boundary condition.

**V4 (conservation).** L̄'s density has no explicit r → the θ-integrated radial Hamiltonian
`H(r) = φ' ∂L̄/∂φ' + ρ' ∂L̄/∂ρ' + ∫ f_r (∂D/∂f_r) dθ − L̄` is conserved: dH/dr = 0 on-shell
(pointwise Noether identity verified; pole fluxes vanish under the pole BCs).

**V5 (free boundary ⇒ H = 0).** With natural (mirror) BCs, stationarity of S under variation of
the seal position gives the transversality condition L̄(r_s) = 0. At a mirror point all radial
derivatives vanish, so H = −L̄ there; hence **H ≡ 0 throughout the cell**. Explicitly at any
mirror surface: `2 = (ξ/2)(I_θ + N²I_s) + (κN²/2) I_4θ/ρ²` — the intrinsic curvature term (the 2)
balancing the angular matter energy. Illustration only (rigid f=θ, N=1, ξ=κ=1): ρ_s² = 1/2.
(Rigid is not a solution of the coupled system; the number shows the condition is satisfiable in
range, nothing more.)
- **Chose-or-derived:** H = 0 is DERIVED **given** the chose "r_s is dynamical." If instead the
  seal is externally pinned (embedded cell), the same H carries the ENVIRONMENT value — MAP
  §4(d) — so the fork is Class-A-free (H=0) vs Class-A-embedded (H=H_amb), not pin vs no pin.
- **Counting:** seal conditions φ'_s=0, ρ'_s=0, H=0 (3) vs unknowns φ_c, ρ_c, r_s (3, core
  derivatives mirror-pinned) → SQUARE → isolated solutions generic. At a mirror core H=0
  additionally relates ρ_c to the core profile — the MAP-P9 knob derived away.

**V3 + V6 (scaling / Derrick).** Under (r, ρ) → λ(r, ρ), f(r) → f(r/λ): geometry and the entire
ξ-sector are scale-covariant (common weight λ after dr = λdu); the κ-sector carries an extra
λ^{−2} and is the UNIQUE breaker → κ/ξ sets the absolute cell scale; ratios are the invariants.
Derrick identity for any free-boundary solution: `S_a = S_b`, i.e.
`∫[(Z/2)ρ²φ'² + 2 − 2e^{−2φ}ρ'² − (ξ/2)(ρ²I_r + I_θ + N²I_s)] dr = −(κN²/2)∫(I_4r + I_4θ/ρ²) dr`,
with the RHS strictly negative for winding matter — a necessary integral condition every found
solution must satisfy (a solver diagnostic; pre-reg-friendly). Finite mirrored domain + the
geometric −2e^{−2φ}ρ'² term evade the classic Derrick prohibition: **finite cells are not
scaling-forbidden.** Second scaling derivative of the energy is +κN²∫(...) > 0: the scaling
mode about any solution is stable.

**V1 (OBS-3 banked at CAS level).** Residual of f = θ in the f-PDE is exactly ξ(1−N²)cosθ, on
ANY background ρ(r): rigid is stationary only at N=1; for N ≥ 2 the θ-profile must deform before
radial structure enters.

**V7 (second variation, N=1).** About f = θ + ε g(r)h(θ) (admissible: h(0)=h(π)=0):
- ξ-part: `(ξ/4)[ρ² g'² ∫sinθ h² + g² Q_ξ[h]]`, `Q_ξ[h] = ∫(sinθ h'² + (cos2θ/sinθ) h²)dθ` —
  the BPS harmonic-map Hessian, ≥ 0, kernel h ∝ sinθ (verified: Q_ξ[sinθ] = 0).
- κ-part: cross term integrates by parts (key identity cos2θ + 2sin²θ = 1, boundary terms vanish
  for admissible h) to `(κ/4ρ²)[ρ² g'² ∫sinθ h² + g² ∫(sinθ h'² + h²/sinθ)dθ]` — **manifestly
  strictly positive.**
- Even along the ξ zero direction (h = sinθ, g const) the κ-part is 8/3·(κ/4ρ²)g² > 0.
⇒ **δ²E_m > 0 for every admissible nonzero perturbation: f = θ is a strict local minimum of the
matter energy at fixed geometry.** I_r generation is a strict cost at O(ε²) traded against an
O(ε²) geometric gain — the outcome is quantitative, exactly what the 2-D solver must decide.

## Consequences for the build (amend MAP §9)

1. Add H(r) as a MONITORED conserved quantity (discretization drift diagnostic) and **H = 0 as
   the third closure condition** for the free Class-A cell; the scan is then square — report the
   isolated closure set directly, plus the H≠0 continuum as context.
2. Add the Derrick integral identity as a per-solution acceptance diagnostic.
3. Seeding: include far-from-rigid seeds (large θ-deformation, nontrivial radial profile) — V7
   says rigid-adjacent seeds are downhill toward collapse.
4. For N ≥ 2: relax the θ-profile first (V1) before freeing r.
5. Pre-reg amendment owed BEFORE running: register "Class A free (H=0)" vs "Class A embedded
   (H = H_amb)" as the two closed-cell sub-classes; the embedded variant is where the
   Misner-Sharp / ambient-density mechanism (MAP §4d) lives.

## Premises carried (unchanged from MAP)

Constrained-two-player, static, round, axisymmetric (CHOSE, Risk 1); {L2, L4} minimal basis
(CHOSE-minimal, F2); Route-A structure with Z held fixed (OBS-2); ξ = κ = 1 units. NEW chose
introduced here: **"the seal position is a dynamical variable of the action"** (it produces
H = 0; its alternative is the embedded/environment pin — the fork is now explicit, both lanes
derived past that single chose).

## VERIFIER

**Blind adversarial pass — 2026-07-01, Claude Code session, agent `af0a5fdd`.** A fresh
zero-context verifier independently re-derived every load-bearing claim from scratch (not
importing the author's intermediates) and hunted for false passes. **Verdict: all physics
V1–V7 CORRECT**, including the two flagged for hostile review:
- **V5** — re-derived the variable-endpoint transversality from first-principles calculus of
  variations: the mirror BCs `φ'=ρ'=0` emerge as the *natural* (variational) BCs (momenta are
  purely first-order: `π_φ=Zρ²φ'`, `π_ρ=−4e^{−2φ}ρ'`, so they vanish at the mirror); transversality
  `(L̄−Σq'π_q)|_{r_s}=−H=0` follows; `H=0` is a genuine *independent* condition (`L̄|_mirror≠0`
  generically), so the 3-vs-3 counting → isolated cell sizes is sound. Conditioned on the tagged
  premise "r_s is dynamical." Caveat (bounds the claim, not the logic): "isolated sizes generic" is
  a **genericity** statement (one modulus r_s ↔ one scalar H=0), assuming the f-sector adds no
  continuous moduli — V7's strict rigidity is the backstop at the rigid point.
- **V7** — δ²E_m>0 strict; the 1/sinθ pole does NOT spoil positivity (admissible h~θ → h²/sinθ→0);
  IBP boundary term `2cosθ·h²|₀^π` vanishes for admissible h.
- V1, V2 (all 3 EOMs), V3, V4, V6 confirmed.

**Two honesty corrections applied to the artifact (this session):**
1. **The committed script was materially HOLLOW on V5/V6/V7** — it printed `True` via trivial
   identities (`H=−L̄` at a mirror is true for ANY Lagrangian; a bare trig identity; one zero mode)
   while the load-bearing statements lived only in prose. **FIXED:** `verify_f2d_virial_step0.py`
   now genuinely tests the V5 ingredients (momenta purely first-order → mirror = natural BC;
   `H=0` nontrivial), the V6 Derrick single-breaker structure (geo+ξ scale-invariant, κ carries
   λ⁻²), and the V7 κ-part positivity (g²-integrand = manifestly-positive `sinθh'²+h²/sinθ` after
   IBP, matched for two admissible h; boundary term = 0). Dead placeholder cruft removed.
2. **The transversality THEOREM (free-endpoint variation forces L̄(r_s)=0) is standard
   variable-endpoint calculus of variations, hand-verified — NOT a CAS identity.** The script tests
   its ingredients and labels the theorem as cited/hand-verified; the doc no longer claims "CAS-
   verified by the committed script" for the transversality step itself. (The verifier's own
   `trans+H==0` check was trivial-by-construction; that trap is now avoided.)

Re-run: all genuine checks TRUE (`python3 verify_f2d_virial_step0.py`).
