# Microphysics E1 — composite two-domain closure (particle cell IN the real N=0 fundamental): derivation, residual system, probe pass

**Date:** 2026-07-03. **Stage:** E1 of `microphysics_reentry_miniMAP.md` (pre-registered; cheap
analytic/probe pass ONLY — no BVP solves run). **Scripts:** `microphysics_E1_composite_conditions.py`
(sympy, 24/24 PASS) + `microphysics_E1_probe_pass.py` (numeric probes on the blind-verified E0
tables; output `microphysics_E1_probe_results.json`). **Status: BANKED, BLIND-VERIFIED — agent
a50cf068b5ecf05e2, 8/8 attacks HOLD, two corrections applied in place (see VERIFIER RECORD at
end).** Data-blind (no particle masses/data
touched). Everything below is scoped to **round-static, diagonal, areal, CONCENTRIC** (four
independent CHOSE, canon C-2026-06-18-1, plus concentricity) — no claim is a frame verdict.

## 0. The composite problem (objects, all cited)

Domains: particle cell `[0, r_p]` with the DERIVED native S² L2+L4 carrier
(canon C-2026-06-14-1 + refinement; reduced Lagrangian = Step-0 V2,
`f2d_virial_step0_results.md:34-38` == `cell_solver_f2d.py:14-44`), ambient `[r_p, r_sU]` = the
real N=0 fundamental's bulk (potential-only φ-blind `L_m = −U(ρ)`, the T3 slice family, CHOSE per
bracket; `cell_solver_universe_T3.py:8`), shared movable seal at `r_p`, outer boundary = the odd
CMB fold with its DERIVED pins (`universe_cell_fold_jc_sigma_results.md:26-35`). Both media are
round-static **Branch-P** reductions — the seal is a **P|P interface** (matter-content jump only);
the G↔P weight-jump machinery of `seal_matching_junction_results.md` is NOT triggered at `r_p`.

CAS re-derivations of the building blocks (independent of the banked scripts): ambient EOMs ==
banked T3 EOMs (K0a); carrier f-EL == banked f-PDE, rigid residual `ξ(1−N²)cosθ` (K0b, K0b');
`H_amb` == `cell_solver_universe_T3.py:119` (K2a); H_cell matter density == the f2d moment form
(K2b); H conservation for both (K3a,b). Moments: `I_r, I_θ, I_s, I_4θ, I_4r` as in
`cell_solver_f2d.py:21-22, 202-207`.

Throughout: `E_ang(r) ≡ (ξ/2)(I_θ + N²I_s) + (κN²/2)I_4θ/ρ²` (the carrier's transverse angular
energy) and `K_geo ≡ (Z/2)ρ²φ'² − 2e^{−2φ}ρ'²` (gradient content).

## 1. THE DERIVED CONDITION SET (concentric composite)

From the two-domain action `S = ∫₀^{r_p} L̄_cell + ∫_{r_p}^{r_sU} L̄_amb`, varying fields, the
shared seal position, and the outer fold position. The two-domain corner machinery for SHARED
fields is INHERITED (blind-verified, `embedded_cell_closure_H_amb_results.md:19-38`); the f-sector
(a field present on ONE side only) is NEW and derived here (K1, K1').

**At r = 0 (particle core; class adjudicated in §3):** natural BCs from stationarity alone
(momenta `π_φ = Zρ²φ'`, `π_ρ = −4e^{−2φ}ρ'`, `π_f = −½A f_r` with `A > 0` on θ∈(0,π); K1', K6'):

    φ'(0) = 0,   ρ'(0) = 0,   f_r(0,θ) = 0   (even mirror fold; values φ_c, ρ_c FREE)

**At r = r_p (shared movable seal; φ, ρ continuous — posture CHOSE-cited, JC2/orbifold):**

    C1a  [π_φ] = 0   ⇔  φ'_cell(r_p) = φ'_amb(r_p)      (JC1, dilation flux continuous)
    C1b  [π_ρ] = 0   ⇔  ρ'_cell(r_p) = ρ'_amb(r_p)      (JC2 in reduced variables)
    C1c  π_f(r_p,θ) = 0  ⇔  f_r(r_p,θ) = 0  ∀θ          (NEW: one-sided natural BC — the
         carrier ends mirror-flat at the seal; DERIVED, not chosen; K1/K1')
    C2   H_cell(r_p) = H_amb(r_p)  ⇔  E_ang(r_p) = U(ρ(r_p))     (K4: with C1a,b,c the
         geometry parts cancel identically; C2 collapses to a LOCAL energy match)

**At r = r_sU (odd CMB fold, free position — same CHOSE posture the banked E_m(core)=2 rides on):**

    φ(r_sU) = 0 (essential, odd identification),   ρ'(r_sU) = 0 (free Δρ),
    H_amb(r_sU) = 0 (transversality; K6),   φ'(r_sU) free ⇒ q = Zρ_s²φ' is an OUTPUT.

Plus pole BCs `f(r,0)=0, f(r,π)=π` (degree/regularity, carried by the ansatz) and the carrier's
confinement to `[0,r_p]` (frame-level content assignment, CHOSE — see ledger #8).

## 2. THE H_amb ADJUDICATION (the key frame question) — **H_amb ≡ 0 REMAINS FORCED**

In the composite: (i) `L̄_amb` is unchanged and r-autonomous ⇒ `H_amb` conserved on `[r_p, r_sU]`
(K3); (ii) the outer odd fold's variational status is untouched by a deep-interior insertion ⇒
transversality still gives `H_amb(r_sU) = 0` (K6); (iii) conservation propagates 0 to the seal.
**The insertion/moved inner boundary does NOT change what the variational principle demands of
the ambient constant:** the seal variation yields C2 (a BALANCE, `H_cell = H_amb`), not a new pin;
the ambient's constant is set at the outer fold ALONE. Hence

    H_amb ≡ 0  on the ambient segment   ⇒   C2 reads  **H_cell(r_p) = 0**
    ⇒ (H_cell conserved)  H_cell ≡ 0 through the cell
    ⇒ (even-fold core, K5)  **E_ang(core) = 2**  — the particle-core critical closure.

What DOES change vs the pure universe cell: the ambient LOSES its inner even fold (cut out by the
particle), so `U(ρ_c)=2` is no longer a condition on the ambient — **the criticality condition
migrates to whatever closes the center: the particle core inherits it as E_ang(core) = 2.**

Conditional premises (all tagged, ledger below): free-fold posture (CHOSE — the same one canon's
E_m(core)=2 rides on; if revisited, both change together), continuity posture, source-free Class-A
seal (no S_seal), concentric round-static. **Named fork (stated, canon-blocked):** an
"empty-P-medium exterior" target would give `H_amb = −2`, not 0 (`universe_cell_fold_jc_sigma_
results.md:62-64`) — blocked by no-spatial-infinity canon, carried openly.

**Revision this forces on the banked lay picture:** `embedded_cell_closure_H_amb_results.md:47-55`
("the ambient Misner–Sharp density selects which cell sizes can close") is WRONG in its
position-dependence: `H_amb` is one conserved number, ≡ 0, at EVERY position (E0 confirms to
1e-10; and 2m/ρ ≡ 1 — the fundamentals are everywhere-marginal). The ambient still pins the cell,
but through **C1's gradients + C2's `U(ρ_p)`** (position-dependent), never through H. The scale
pin survives; its carrier variable was misidentified.

## 3. The particle-core closure — even mirror fold FORCED (within probed classes)

The finite-cell canon's wording for matter cells ("φ: 0 at the interface → −∞ at the core",
C-2026-06-10-2) does NOT survive this reduction's own equations; derivation, not choice:

1. **Regular endpoint, ρ_c > 0:** stationarity alone forces the even fold (natural BCs; §1) —
   same mechanism as the universe's inner fold (D1), now including `f_r(0,θ)=0` via `π_f` (K1').
2. **φ → −∞ with ρ bounded below: EXCLUDED (exact).** The flux law `(ρ²φ')' = (4/Z)e^{−2φ}ρ'² ≥ 0`
   (K7; matter-independent since ALL matter here is φ-blind) makes `Φ = ρ²φ'` monotone
   non-decreasing; Φ finite at the seal bounds `φ' ≤ Φ(r_p)/ρ_min²` ⇒ φ bounded below. No dive.
3. **ρ → 0 regular center: EXCLUDED (banked, blind-verified)** — R2 of
   `universe_cell_vacuum_impossibility_results.md:75-82` holds for an ARBITRARY φ-blind ρ''-source;
   the carrier's own `−κN²I_4θ/ρ³` source additionally diverges inward (and `I_4θ ≥ 1`, K12, so it
   cannot be tuned away).
4. **ρ → 0 singular power-law core (φ = β ln s + φ₀, ρ = a s^α): EXCLUDED** — the φ-EOM's two
   sides scale as `s^{2α−2}` vs `s^{2α−2−2β}` (K7'); β > 0 forces the RHS to dominate with no LHS
   term to match (α = 1/2 kills the LHS leading term but leaves RHS ~ `s^{−1−2β}` unmatched).

**Scope (honest):** classes 1–4 cover regular + power-law asymptotics; exotic (log-corrected,
essential-singular, ρ→∞) cores are NOT exhaustively excluded. **Canon-wording flag for Charles**
(parallel to the C-2026-07-02-1 Δφ re-reading): within round-static Branch-P, the matter-cell core
is an even fold at finite depth `φ_c < φ_loc` (φ monotone up through the cell by the flux law),
not φ→−∞.

**Native mechanism analogs (derived, not posited):**
- **E_m(core)=2 analog: YES.** `E_ang(core) = 2` is the same transversality closure; for the rigid
  N=1 carrier the cell is EXACTLY a universe-type potential cell with the DERIVED potential
  `U_eff(ρ) = ξ + κ/(2ρ²)` (K8'; rigid solves the f-PDE only at N=1, K0b'), and the closure is
  `U_eff(ρ_c) = 2 ⇔ ρ_c = √(κ/(2(2−ξ)))`.
- **Flux-seal analog at r_p: NO.** The embedded seal is the "independent-partner glue"
  configuration of D1 (`universe_cell_fold_jc_sigma_results.md:32-33`) — a continuity interface,
  no fold pins, no seal source (Class-A EMBEDDED). The particle's public charge is NOT sealed-in
  flux but the continuous ambient flux through its seal: `q_p = Zρ_p²φ'(r_p)` = the value the pure
  profile already carries there (E0 `pi_phi_qflux` column; Gauss/JC1). q_p is an OUTPUT.
- **Derived core shape:** `ρ''(0) = −(e^{2φ_c}/4)κN²I_4θ(0)/ρ_c³ < 0` strictly (I_r(0)=0,
  I_4θ ≥ 1): every embedded L2+L4 cell has a **core throat** (ρ_c is a local max, ρ dips then must
  recover to meet ρ'_loc ≥ 0 — an interior ρ-turning sphere). The universe cell rises from its
  core (σ(0) = U'(1)e^{2φ_c}/4 > 0); the particle cell inverts.

## 4. The residual system (E1 deliverable) + counting

Unknowns (shooting from the core), given bracket (family, Z, a*) and carrier (ξ, κ, N):
`φ_c, ρ_c, g(θ) = f(0,·) [M modes], r_p, r_sU` → **M + 4**.

    R1(θ):  f_r(r_p, θ) = 0                        [M rows]   (C1c)
    R2:     E_ang(r_p) − U(ρ(r_p)) = 0             [1]        (C2, collapsed form)
    R3:     φ(r_sU) = 0                            [1]        (odd-fold pin)
    R4:     ρ'(r_sU) = 0                           [1]        (odd-fold pin)
    R5:     H_amb(r_sU) = 0                        [1]        (fold transversality)

(C1a,b are consumed as continuity of the shot; equivalently swap R5 → `E_ang(core) = 2` via the
conservation chain — same count.) **Conditions M + 4 vs unknowns M + 4: SQUARE.** Isolated
solutions generic — the old over-determination does NOT recur, with ONE bookkept subtlety: the
observational anchor Δφ = ln(1101) is NOT imposed on the composite (it selected the bracket via
the pure cell); imposing it exactly would over-determine by 1 unless the slice parameter a* is
freed. Difference = O(cell back-reaction). Tagged CHOSE (anchor at bracket level; Δφ floats by
O(ε) in the composite — the real universe's anchor is measured WITH its particles in it).

What structurally changed vs the failed CLOSED cell (3v3, `H=0` unreachable, collapse-or-inflate,
`embedded_cell_closure_H_amb_results.md:11-13`): the mirror seal conditions `φ'_s = ρ'_s = 0` are
REPLACED by matching to ambient gradients + R2; the closure target is the SAME `H = 0` (per §2).
**In the gradient-free limit the embedded problem REDUCES CONTINUOUSLY to the closed Class-A H=0
problem** (the extra condition R2 becomes degenerate there: `U_loc − 2 = K_geo^{amb} → 0`, K13).

## 5. Off-center positions (guardrail-2 controls) — the honest local-approximation verdict

**(a) What is derivable:** for a particle at station r₀ with cell size r_p, treating the ambient
across the cell as uniform incurs field errors `O(r_p·G_loc)`, `G_loc = max(|φ'|, |ρ'|/ρ)`
(E0 dense profiles: G_loc = 3e-5…1e-2 plateau, 0.24–0.80 seal wall), and the ambient gradient
sources an ℓ=1 (tidal) distortion of the same order that the round machinery drops.

**(b) What is NOT derivable at E1 level (two obstructions, stated plainly):**
1. **Foliation transplant:** off-center, the particle's areal field ρ̃ (its own S² fibers) is NOT
   the universe's ρ; the ambient matter law `U(ρ_universe)` does not transplant into the cell's
   local chart without a 3-D (non-reduced) matching derivation we do not have. Matching ρ̃_p to
   ρ_loc would be an UNLABELED approximation — refused (Principle 2).
2. **Stiffness:** the linearized ambient amplifies seal-data perturbations to the fold by
   ‖Ψ(r_s ← station)‖₂ ≈ 1e6–2.4e8 (P6b, both brackets probed). The pure-profile station values
   are therefore effectively EXACT pins along the growing directions (admissible ambient response
   confined to the ~2-dim non-growing family): the cell cannot push the ambient; the ambient
   dictates. Any "local values + slack" picture is wrong beyond |δy| ~ 1e-6.

**VERDICT (per the pre-registered escape clause):** the literal off-center small-cell
approximation is NOT controlled at E1 level. **E1 is scoped to the CONCENTRIC case — which
expresses the full plateau-vs-wall contrast EXACTLY**: sweeping the seal radius r_p moves the
seal environment from gradient-free (r_p → 0: the particle at the universe's center fold = the
labeled turning-point slice) through the plateau to the gradient-carrying wall (r_p near r_sU:
the controls). Both slices are reported below (guardrail 2 satisfied within the concentric
family; literal off-center = named E2+ work requiring the 3-D matching).

## 6. Probe-pass findings (cheap, no solves; all four E0 brackets; plateau AND wall)

**P0 — bracket universality split (guardrail 1).** The plateau/turning-point bracket is
**family-UNIVERSAL by derivation**: every fundamental has (φ, ρ, U)_plateau ≈ (−7.004, 1, 2)
because the anchor pins φ_c = −ln(1101) and criticality pins U(ρ_c) = 2 (ρ_c = 1 WLOG). The wall
bracket is **family/Z-SENSITIVE**: `U_seal = 2 − q²/(2Zρ_s²)` spans 0.052 (A1 Z8), 0.671 (A3 Z8),
1.409 (A1 Z1), 1.686 (A3 Z1). Any closure that exists only via wall stations is family-sensitive;
plateau closures would be canonical.

**P1 — a family-robust distinguished station emerges.** U_loc crosses 2 (⇔ K_geo = 0, the exact
gradient-energy balance; K13) at **r*/r_s = 0.948–0.954 in ALL FOUR brackets** — a wall-side
balance sphere at ~95% radius, where C2 asks the carrier for exactly the critical value
E_ang(r_p) = 2 = E_ang(core) while real gradients flow through the seal. (VERIFIER-CORRECTED:
every bracket has exactly ONE genuine interior U=2 crossing — the originally-reported "extra
sign changes" (A1 Z8 "2", A3 Z1 "4") were a counting artifact, 0 ↔ 4e-16 machine-noise
transitions at the core fold's geometric refinement points. One distinguished station, no extra
structure — the r* headline is STRENGTHENED.)

**P2 — the embedded-Derrick "tax" (new exact identity).** Pohozaev/scaling identity (K9), the
free-boundary Derrick V6 generalized to the embedded cell, on-shell with H ≡ 0:

    S_a − S_b = ρ_p π_ρ(r_p) = −4 e^{−2φ_p} ρ'_p ρ_p  ≡  −τ(r_p)   (τ ≥ 0 since ρ'_loc ≥ 0)

τ(r) on the pure profiles: ZERO exactly at both folds, max 8.3–33 at r/r_s ≈ 0.90–0.92, and
τ/r → U'(ρ_c) = 0.014–0.075 near the core (probe matches the analytic law to 4 digits). The old
"gradient-carrying ambient is the obstruction / turning points are the escape" wall now has a
DERIVED quantitative face: a seal at position r pays the tax τ(r) in the integral balance below.

**P3 — the bulge theorem (structure of any closure).** Substituting pointwise H = 0 into the
Derrick identity (K10) gives, for ANY solution:

    ξ ∫(I_θ + N²I_s) dr = 4 r_p + κN² ∫ I_4r dr + τ(r_p)
    ⇒ mean(I_θ + N²I_s) ≥ 4/ξ,  while BOTH endpoint values are < 4/ξ
      (core: = (2/ξ)(2 − κ-part) ; seal: ≤ 2U_loc/ξ with the κ-part subtracted)
      [verifier scope note: plateau stations carry U_loc−2 ≈ +5e-7…2e-4 > 0, so the seal-side
      strict inequality needs the κ-part to exceed that — true across the probed grid (κ ≥ 0.01),
      not literally universal as κ → 0]

⇒ **any embedded L2+L4 closure is an interior angular-energy BULGE object** (angular energy rises
above both its core and seal values; with V7 — rigid is a strict minimum at fixed geometry — the
bulge is a genuinely non-perturbative deformation). Wall seals (τ > 0) demand MORE bulge;
fold-adjacent seals demand least.

**P4 — rigid-N=1 EXCLUDED everywhere (clean single-signed result, the probes' teeth).** The rigid
carrier's energy conditions are satisfiable at every station (`ρ_c/ρ_p = √((U_loc−ξ)/(2−ξ))`, P5
column in the JSON) — but the Derrick balance gives `dens_a − dens_b = 4 − 2ξ` pointwise (K11), so
closure needs ξ ≥ 2, while the core closure `ξ + κ/(2ρ_c²) = 2` needs ξ < 2 (κ > 0).
**Contradiction: the rigid-N=1 cell (= the derived monotone-U_eff potential cell) closes NOWHERE —
every bracket, every position, every κ > 0.** Consistent with, and sharper than, the closed-cell
scan negative; any closure must carry genuine θ-deformation (with V1: for N ≥ 2 it must anyway).

**P5 — necessary-condition maps (characterize, never filter).** From E_ang ≥ ξN + κN²/(2ρ²)
(Cauchy–Schwarz, K12: I_θI_s ≥ 1, I_4θ ≥ 1, rigid saturates): a seal at r REQUIRES
`ξN + κN²/(2ρ_loc²) ≤ U_loc(r)`; the core requires `ξN < 2` and `ρ_c ≥ N√(κ/(2(2−ξN)))` (a
derived core-size floor ∝ the canon carrier scale √κ). Over the bounded (ξ,κ,N) grid, per bracket
(JSON `necessary_map`): three regimes appear — fully-admissible (small couplings), fully-excluded,
and **position-selective** (6–30 of 44 cells per bracket, one sign change in r):
- N=1, moderate ξ: plateau-admissible, wall-EXCLUDED (the Z=8 brackets, with U_seal = 0.05–0.67,
  exclude the wall hardest — ξN ≤ 0.052 at the A1 Z8 seal vs ξN ≤ 2 plateau);
- **N=2, κ ≈ 1: the INVERSION — plateau-EXCLUDED, wall-only-admissible** (VERIFIER-CORRECTED:
  present in THREE of four brackets — A1 Z1 (2 cells), A3 Z1 (3), A3 Z8 (2); absent only in
  A1 Z8, whose U_seal = 0.052 admits almost nothing at the wall. The original "(Z=1 brackets)"
  attribution and its U_seal~1.4–1.7 mechanism sentence fit only half the evidence; the
  mechanism (κ/ρ² cost dropping at the wall's larger ρ_s) needs restating against the full set).
  The necessary conditions can select EITHER environment depending on couplings: position
  selectivity is real, two-sided, and broader than first reported —
  reported for both slices, no slice preferred.

**P6 — what E1 does NOT establish.** "Closes nowhere" is NOT proven: for non-rigid carriers with
ξN < 2 and bracket-admissible (ξ,κ), no residual is provably single-signed — the binding question
(can the cell's (φ,ρ,f) BVP actually CONNECT the critical core to the matched seal with the bulge
paid?) is exactly the gated E2 composite solve. E1's clean kills are: rigid-N=1 (everywhere),
ξN ≥ 2 (everywhere), and per-bracket wall/plateau (ξ,κ) exclusion regions. The stiffness finding
(§5b) mandates that E2 solve the two domains COUPLED — station tables are a bracket, not a
boundary condition.

## 7. Premise ledger (chose-or-derived; every fixed value tagged)

| # | Premise | Tag |
|---|---------|-----|
| 1 | Round + static + diagonal + areal | CHOSE ×4 (canon C-2026-06-18-1); ω≠0 = pre-named next freedom |
| 2 | CONCENTRIC particle (cell shares the universe's center/foliation) | CHOSE (E1 scope; literal off-center = E2+ after the 3-D matching, §5) |
| 3 | Ambient = banked N=0 fundamental; slice family + a* per bracket | CHOSE (T3 slice family, `cell_solver_universe_T3.py:8`) — bracketed per guardrail 1, both Z, both families |
| 4 | Ambient matter law U fixed in the composite (no re-tuning by the particle) | THEORY (a Lagrangian is not a per-solution knob); the PROFILE re-solves |
| 5 | Anchor Δφ = ln(1101) applied at bracket level, floats O(ε) in the composite | CHOSE (else over-determined by 1 unless a* freed; §4) |
| 6 | Carrier = L2+L4 ONLY; (ξ, κ) FREE-and-explored; N free integer | THEORY (canon C-2026-06-14-1 + refinement); no tuning beyond L2+L4 (forbidden) |
| 7 | Z shared across the seal; value ∈ {1,8} | THEORY (one theory both media) / FREE-explored (Route-A/B tension standing) |
| 8 | Carrier confined to `[0, r_p]`; ambient matter only outside | CHOSE (frame-level content assignment per miniMAP; "why n ends at the seal" not derived) |
| 9 | Seal: φ, ρ continuous; source-free (Class A EMBEDDED, no S_seal) | CHOSE-cited (banked posture, `embedded_cell_closure_H_amb_results.md` premises 2–3); Class B would add a seal source — not posited |
| 10 | Seal position r_p free variable of the total action | CHOSE (banked embedded posture; alternative = externally pinned seal) |
| 11 | Outer fold position free (transversality) | CHOSE (banked free-endpoint posture — SAME premise as canon E_m(core)=2; linked CONDITIONS-CHANGED) |
| 12 | Empty-P-medium exterior fork (H_amb = −2) | STATED, canon-blocked (no spatial infinity) |
| 13 | Even-fold core class for the particle | DERIVED within {regular, power-law} classes (§3); exotic asymptotics open; canon-wording flag raised |
| 14 | H_amb ≡ 0 on the ambient segment | DERIVED conditional on #9–#11 (§2) |
| 15 | C1a/b/c + C2-collapse + fold pins + flux law + Derrick/bulge + bounds | DERIVED (CAS K0–K13, 24/24) |
| 16 | Probe grids (ξ, κ, N lists), station placement, FD steps, IVP tolerances | Category-A conditioning (coverage/soundness, not physics) |
| 17 | Station values as the seal bracket in probes | LABELED leading order in cell back-reaction; validity sharply bounded by the 1e6–1e8 amplification (§5b) — never treated as exact |

## 8. Counting summary

Exact concentric composite: **M+4 conditions vs M+4 unknowns — SQUARE** (isolated solutions
generic); the single potential over-determination (the anchor) identified and resolved as an
O(back-reaction) bracket-level pin (ledger #5). Old closed cell: 3v3 square with unreachable
H = 0; the composite reaches the same H = 0 target through a larger admissible set (seal
gradients freed) at the price of R2 + the Derrick tax. Gradient-free limit = the closed cell
exactly (§4).

## 9. Standing for the verifier (attack surface, named)

Load-bearing pieces: (a) the §2 adjudication chain (autonomy + outer-fold transversality +
conservation ⇒ H_amb ≡ 0 ⇒ H_cell(r_p) = 0); (b) the C2 collapse `E_ang(r_p) = U(ρ_p)` (K4) and
its reliance on C1c; (c) the Pohozaev sign (K9) — the tax orientation decides whether walls tax
or subsidize; (d) the rigid-N=1 contradiction (K11) — E1's only everywhere-negative; (e) the
counting (§4) incl. the anchor bookkeeping; (f) the core-class exclusions (§3, esp. the flux-law
argument and the power-law clash K7'); (g) the C-S bounds (K12) feeding every necessary map.

## LAB-LOG

- 2026-07-03: `microphysics_E1_composite_conditions.py` — 24/24 PASS (sympy; two sign-orientation
  bugs in the driver's first K3 bookkeeping caught by the harness itself and fixed; K7' fixed for
  a positive radial symbol). `microphysics_E1_probe_pass.py` — all four brackets probed; JSON
  written; runtime seconds; single process; no BVP solves. NOT committed (verifier-before-record).

---

## VERIFIER RECORD (blind adversarial pass — agent a50cf068b5ecf05e2, 2026-07-03)

**All 8 attacks: HOLDS (two with corrections, applied above in place).** Independent sympy
re-derivation of the full chain (own Lagrangian assembly, own EL/H/Noether/Pohozaev incl. a
brute-force sign-assignment search); independent probe recomputation from the E0 JSON
(different integrator, analytic U''); purity 32/1xfail; data-blind clean.

- **H_amb≡0 → C2 = H_cell(r_p)=0 → E_ang(core)=2 migration: HOLDS** — no variational cross-talk
  between seal and fold; δr_p coefficient is the DIFFERENCE (balance, not pin); premise set =
  the same free-fold/continuity/source-free set canon E_m(core)=2 rides on. The corrective to
  the banked lay wording is right; nothing banked rides on the old position-dependent wording.
- **SQUARE counting: HOLDS** — recounted M+4 vs M+4; the load-bearing structural difference vs
  the old over-by-2 model-ambient scheme is the ambient becoming DYNAMICAL with its real free
  outer fold (net −2), not dynamical r_p, not the seal class. Δφ-anchor treatment honest.
- **C2 ⇔ E_ang(r_p)=U(ρ_p) (K4): HOLDS** (own sympy; curvature ±2 terms cancel identically).
- **Core-class exclusion: HOLDS and EXTENDED** — verifier probed three exotic classes the
  deriver did not (essential-singular φ with power ρ; ρ→∞ power core; log-corrected dive):
  all excluded. Remaining gap: combined essential/oscillatory asymptotics only. Canon
  adjudication: airtight-within-stated-classes, NOT absolute — the C-2026-06-10-2 wording
  call is Charles's.
- **Rigid-N=1 kill + ξN≥2: HOLDS** — embedded-Derrick identity re-derived by an independent
  route; C-S machinery stress-tested on 500 non-monotone profiles. Negative scope stamp
  carried: round-static, diagonal, areal, concentric, Branch-P, source-free Class-A seal,
  free outer fold, κ>0, seal strictly interior.
- **Probe windows: HOLDS-WITH-TWO-CORRECTIONS (both applied above + the counting bug fixed in
  microphysics_E1_probe_pass.py, JSON regenerated: every bracket = exactly 1 genuine U=2
  crossing; the N=2 inversion present in 3 of 4 brackets, absent only A1 Z8).**
- **Local-approximation refusal: HOLDS** — ‖Ψ‖ reproduced to 4 digits with a different
  integrator; if anything the stiffness is understated; foliation-transplant refusal = a
  correct Principle-2 call.
- **Ledger addendum (inherited premise, owed by §2):** the +2 angular integrand being physical
  is an inherited D1-verifier condition — canon E_m(core)=2 carries it, and K5's "−2" rides on
  the same term. Cosmetic bands: r* = 0.9480–0.9542; tax argmax ≈ 0.90.
