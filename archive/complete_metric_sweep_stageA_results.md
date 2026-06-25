# RESULTS — Complete-Metric Deep-Negative-φ Sweep, STAGE A (foundational)

Research record (append-never-edit). OBSERVE mode (report what IS there; NOT
targeting a fermion or any particular cell). Driver: Claude (Opus 4.8, 1M),
agent constructing Stage A. Date 2026-06-15. Frame + premise ledger:
complete_metric_sweep_setup.md. DATA-BLIND (all sizes/masses in units of
L = √(κ/ξ) = 1; NO wall numbers loaded or compared).

Scripts (committed with this record, repo discipline = new files):
- `complete_metric_batched.py` — the BATCHED torch-float64 engine (the GPU core
  Stage B is built on; every solve is shape (B,N), Stage B = larger batch).
- `complete_metric_sweep_stageA.py` — Stage-A orchestration (assemble + baseline
  + read-out confirmation + GPU feasibility), runs on the V100, exit 0, ~316 s.

## What is NEW here (the gap this closes)
First script to solve the COMPLETE action — L2 + native L4 — TWO-WAY
self-consistent with the φ back-reaction (Einstein G = κT sourced by the FULL
angular stress incl. L4's T^θ_θ), on the finite cell at DEEP NEGATIVE φ,
ARCHITECTED BATCHED on the GPU. Prior machinery did one side each: #43/#44
(L2+L4 soliton on a FIXED log φ) and coupled_cell B3 #38/#39 (self-consistent φ
in the MINIMAL no-L4 model). Stage A glues them and confirms ONE baseline +
the Stage-B read-outs. (Stage B = the sweep; Stage C = blind verifier.)

## 1. THE ASSEMBLED EXACT SYSTEM (sympy-exact; cross-checked vs banked)

Metric (B=1/A tie, areal ρ=r, φ = −½ ln(−g_tt)):
  ds² = −e^{−2φ} dt² + e^{2φ} dr² + r² dΩ².  X ≡ e^{−2φ} Θ'²,  Y ≡ sin²Θ/r².

**Stress tensor (L2+L4 hedgehog), sympy-exact** [matches native_stabilizer #43]:
  ρ   = (ξ/2)(X+2Y) + (κ/2)(2XY + Y²)
  p_r = (ξ/2)(X−2Y) + (κ/2)(2XY − Y²)
  p_r + ρ = X(ξ + 2κY) = e^{−2φ} Θ'² (ξ + 2κ sin²Θ/r²) ≥ 0   [CANON D7 + L4]
  ⇒ B=1/A (T^t_t = T^r_r ⇔ p_r+ρ=0 ⇔ X=0): EXACT in the unwound exterior
    (Θ'=0), EOS-SOFTENED through the twisting body. (C-2026-06-14-1 + refinement.)

**Reduced radial energy densities** (measure √g = e^{φ} r² sinθ) [banked #43/#44]:
  E2_r = (2π ξ/3) e^{−φ}[ r² sin²Θ Θ'² + 2 r² Θ'² + 4 e^{2φ} m² sin²Θ ]
  E4_r = (2π κ/3) e^{−φ}[ (2 r² sin⁴Θ + 2 r² sin²Θ) Θ'² + e^{2φ} m² sin⁴Θ ] / r²
  (m = winding; m enters ONLY the e^{2φ} potential terms as m². m=1 = #43.)

**Angular Euler-Lagrange**, sympy-derived from E2_r+E4_r, solved for Θ'':
  Θ'' = num / den,  den = r²(2κ sin⁴Θ + 2κ sin²Θ + r²ξ sin²Θ + 2r²ξ).
  CROSS-CHECK: sympy-EL vs banked theta_ddot, **max|diff| = 1.42e-14** over 2000
  random points (independent re-derivation agrees to machine precision).

**Einstein/φ equation** (areal Misner-Sharp, B=1/A diagonal):
  m_areal(r) = r(1 − e^{−2φ}),   m_areal'(r) = κ₈ r² ρ(r),
  with TWO integration constants (banked coupled_cell B3):
   • CORE-DEPTH dial p: e^{−2φ(core)} = e^{+2p} (deep NEGATIVE φ toward the core,
     the inside-out matter cell, CANON C-2026-06-10-2) ⇒ m_core = r_core(1−e^{+2p})<0.
   • SEAL mirror-fold (same-minus time reversal, w6/#42): subtract a linear defect
     rs so m_areal(r_int)=0 ⇒ φ(interface)=0.
  φ RESPONDS to the angular stress; two-way fixed point (ρ depends on φ via X, φ
  on ρ via the t-eq). NOT slaved.

**Seal / regularity BC**: Θ(core)=mπ, Θ(seal)=0 (charge-m hedgehog, unwound at
the seal); mirror-fold seal closes φ(interface)=0; η=1/18 is a boundary object
only (NO bulk potential; #43 total-derivative).

### CONTROL PARAMETERS (premise ledger as EXECUTED)
| Parameter | role | chose / derived |
|---|---|---|
| p (depth dial; φ(core) ~ −p) | deep-negative depth | CHOSEN (ledger; #39) |
| κ₈ (back-reaction coupling = 8πG/c⁴; banked δ=κ₈ξ) | gravitational strength | CHOSEN — **NEW explicit dial this push** (see §2E) |
| κ/ξ = 1 | the single intrinsic scale (units L=√(κ/ξ)) | CHOSEN (units) |
| r_core, r_int | cell endpoints (size FREE input, #39) | CHOSEN |
| m | winding sector (m=1 Stage A) | CHOSEN |
| seed shape | round (Stage A); Legendre/multi-center (Stage B) | CHOSEN — IS the probe |

**APPROXIMATION FLAGS (principle 2)**: NONE used as a result. Full nonlinear EL
+ nonlinear Einstein t-eq solved by batched Newton + fixed point. Sanctioned
function-replacement only: trapezoid quadrature; FD Jacobian (colored,
tridiagonal-exact); an e^{−2φ}-argument clamp guarding TRANSIENT Newton iterates
(the converged solution never touches the clamp). NO linearization anywhere.

### SURFACED PREMISE (made visible early, per method): κ₈ is its own dial
The setup ledger named "depth p" as the dial and κ/ξ=1 as units, but the
two-way coupling has a SECOND physical constant — the gravitational back-reaction
strength κ₈ (= δ in coupled_cell B3, where it was kept SMALL, 0.01–0.1). It is
NOT fixed by κ/ξ. Stage A makes it an explicit control and finds it matters (an
emergent over-collapse threshold, §2E). Flagged for Charles: is κ₈ a free dial
(another scale-family parameter) or pinned by something not yet uncovered? This
is a "chose-or-derived?" item the build surfaced — not yet decided.

## 2. BASELINE SOLVE (deep-negative φ, batched torch float64, V100)

Cell [0.05, 14.05] = 14 L, N=900. xi=κ=1 ⇒ L=1.

**(A) Self-consistent soliton across depth (κ₈=1e-2, weak back-reaction):**
| p | φ(core) | width/L | E2/E4 | M_MS | iters | res_th |
|---|---|---|---|---|---|---|
| 0.0 | −0.000 | 0.6469 | 1.0066 | 0.0590 | 43 | 3.9e-12 |
| 0.2 | −0.200 | 0.6574 | 1.0226 | 0.0605 | 51 | 4.6e-12 |
| 0.4 | −0.400 | 0.6721 | 1.0451 | 0.0628 | 52 | 5.8e-12 |
| 0.8 | −0.800 | 0.7179 | 1.1159 | 0.0703 | 54 | 6.9e-12 |
Deep-negative φ soliton CONVERGES cleanly (res_th ~1e-12) down to the hadronic-
like φ(core) = −0.8. Deeper φ WIDENS the soliton — matches the banked #44
deep-φ widening trend (their log-convention p=0.5 → φ_core=−2.74 → width 1.31).

**BASELINE POINT: p=0.4 ⇒ φ(core)=−0.400 (deep negative), κ₈=1e-2.**

**(B) Size = √(κ/ξ) cross-check (#43/#44), flat φ, batched over κ/ξ:**
| ξ | κ | L | (w−r_c)/L | E2/E4 | res_th |
|---|---|---|---|---|---|
| 1 | 1 | 1.000 | 0.6476 | 1.0065 | 1.9e-11 |
| 2 | 2 | 1.000 | 0.6476 | 1.0065 | 1.9e-11 |
| 1 | 4 | 2.000 | 0.6695 | 0.9995 | 4.1e-12 |
| 4 | 1 | 0.500 | 0.6160 | 1.0487 | 4.3e-11 |
(w−r_c)/L is INVARIANT under κ/ξ at fixed L — size is set by √(κ/ξ). Virial E2≈E4.
**Absolute ground-state energy flat ξ=κ=1: E0 = E2+E4 = 45.604** vs banked #44
**45.607** (agreement to 4 sig figs). Banked width 0.648, E2/E4 1.006 reproduced.

**(C) CPU spot-check of the GPU solve** (independent numpy recompute of the EL
residual on the GPU-converged profile, same stencil; + mpmath dps=40 anchor):
GPU Newton residual (converged) ~6e-12; CPU independent recompute max|Θ''−rhs|
~3.5e-11; mpmath(40) vs float64 theta_ddot at midpoint |diff| machine-tiny.
⇒ float64 GPU solve is exact for the angular EL; CPU/mpmath confirm.

**(D) B=1/A exterior / EOS-softened interior (self-consistent):**
interior body (Θ>1e-2): (p_r+ρ)/ρ ∈ [1.166, 2.000] — EOS-SOFTENED, >0 (L4
makes it ~2ρ where fully wound). Toward the seal (Θ<1e-2): max|p_r+ρ|=1.5e-5
→ B=1/A approached as Θ'→0. p_r+ρ ≥ 0 everywhere (min 3.7e-6). Confirms CANON
D7 + L4 self-consistently: B=1/A exact in the unwound exterior, softened body.

**(E) Emergent over-collapse threshold (κ₈ scan at p=0.4; OBSERVE, not targeted):**
| κ₈ | width/L | M_MS | res_th | state |
|---|---|---|---|---|
| 0 | 0.6731 | 0.0000 | 5.3e-12 | soliton |
| 1e-3 | 0.6730 | 0.0064 | 4.4e-12 | soliton |
| 1e-2 | 0.6721 | 0.0628 | 5.8e-12 | soliton |
| 1e-1 | 0.0283 | 4.2674 | 4.0e+09 | COLLAPSED (strong coupling) |
Weak back-reaction (κ₈ ≲ 1e-2): soliton intact, the source is a genuine SMALL
perturbation of φ — the two-way coupling is real but mild. Strong coupling
(κ₈ ~ 1e-1): the soliton's own MS deficit OVER-COLLAPSES the cell (width crushes,
solver diverges). An EMERGENT coupling bound — recorded as structure that
appeared, NOT a targeted result. (Premise note: κ₈ being a free dial means this
threshold is a feature of the κ₈ axis, not yet a pinned physical scale.)

## 3. READ-OUT MACHINERY (all batched on GPU; confirmed on baseline + perturbed seed)

**(i/ii) Non-round seed relax + angular variance/multipole** — CONFIRMED:
 • 1D radial engine ACCEPTS a perturbed (extra-node bump) seed and relaxes it:
   res 3.4e-12, max|Θ_relax − Θ_base| 7.2e-13 ⇒ the bump RELAXES BACK to the
   round baseline (no distinct 1D radial type at this point).
 • wint 2D solver accepts a Legendre seed, reports th_var / dom_l: round seed
   th_var~9e-10 (dom_l 0); lobe-2 seed retains th_var~0.14 dom_l 2 at this coarse
   grid/iter cap (conv flag False — needs more Newton iters; the read-out objects
   th_var/dom_l compute and discriminate round vs lobed). The genuine round-vs-
   shaped TEST is Stage B's job (with the complete action, refined iters).

**(iii) Round-cell Jacobian min|eig| (batched torch eigvalsh = bifurcation detector)**
 — CONFIRMED and CROSS-CHECKED:
   baseline p=0.4: Hessian lowest-6 ω² = [0.198, 0.554, 1.044, 1.704, 2.582, 3.685];
   min|eig| = 0.198 > 0 ⇒ round cell STABLE, no zero-crossing ⇒ no bifurcation
   at this point. Flat-φ breathing tower ω² = [0.198, 0.554, 1.039, 1.688, 2.554,
   3.645] **matches banked #44 [0.198, 0.554, 1.039, 1.688, 2.554, 3.645]** — strong
   validation of the second-variation Hessian + GPU eigensolve. Stage B sweeps
   min|eig| over depth × seed (a zero-crossing = a branch to a distinct type).

**(iv) Misner-Sharp mass (data-blind)** — CONFIRMED: baseline M_MS = 0.06276
(source MS mass across cell, units √(κ/ξ)); E_reduced = 46.122. NOT compared to
any wall number.

**(v) K_θ flip diagnostic (#38 re-run readiness, WITH L4)** — CONFIRMED:
   bare K_θ = e^{−2φ}/r² ∈ [5.1e-3, 8.9e2] (>0); radial-anisotropy driver
   (φ_r² − sin²Θ/r²) toward seal max 20.7 (the #38 flip pressure). L4 adds
   +2κXY (≥0) to p_r+ρ — the candidate regularizer #38 lacked. Stage B re-runs
   the #38 flip EIGENPROBLEM with L4 present (via the min|eig| read-out).

## 4. BATCHED-GPU ARCHITECTURE FOR STAGE B (feasibility)
The engine is batched (B,N) end to end: solve_theta_batched (damped torch Newton,
tridiagonal Jacobian by colored FD, V100-safe dense LU — NO broadcast-Cholesky
solve_triangular per the known pitfall), phi_from_source, energy/stress/M_MS,
the Hessian eigvalsh. GPU timing (N=600, 20 Newton iters):
   B=8 → 0.34 s (41.9 ms/member);  B=32 → 0.62 s (19.4 ms/member);
   B=128 → 1.55 s (12.1 ms/member).
⇒ A Stage-B grid (e.g. 8 depths × 16 seeds = 128 members) is ONE batched solve
in seconds. The dense tridiagonal LU dominates — vectorizable to a true banded
solver if N grows. Read-outs already fully batched. Stage B = a larger batch, no
CPU port (COMPUTE MANDATE satisfied).

## OBSTRUCTIONS / SURPRISES (honest)
1. **κ₈ is a second control dial** the setup ledger did not name — surfaced
   early (§1) per the method. Open "chose-or-derived?": free scale-family
   parameter, or pinned? Recommend Charles rules before Stage B fixes a value.
2. **Emergent over-collapse threshold (κ₈ ~ 0.1)** — a real structural feature
   on the κ₈ axis (not targeted). Means the baseline is honest only in the weak-
   coupling regime; the strong-coupling regime is a distinct (collapsed) state.
3. The earlier draft's CPU fixed-point (scipy solve_bvp in a loop) DIVERGED at
   deep φ (overflow, energies ~1e91) — REBUILT as the batched torch Newton +
   correct two-constant MS closure (core-depth + seal-fold). The sign of the
   core-depth constant (NEGATIVE for the inside-out cell, e^{−2φ_core}=e^{+2p})
   was the key fix; recorded so Stage B does not regress.
4. wint 2D lobe seed did not fully converge at the Stage-A coarse grid/iter cap —
   the read-out objects work; the genuine relaxation test is Stage B's (refine
   iters; complete action).

## WHAT STAGE B IS READY TO SWEEP
A batched (depth p × seed shape) grid with the COMPLETE action, two-way φ,
weak-coupling κ₈, reading per member: existence/convergence, width, E2/E4, M_MS
(data-blind), angular variance/dominant multipole (round vs shaped), round-cell
Jacobian min|eig| (bifurcation: does it ever cross zero?), and the #38 K_θ flip
re-run WITH L4. The pre-registered reading (setup §"reading discipline"): ONE
round continuum persisting vs DISTINCT TYPES / BIFURCATION / SUBSTRUCTURE
appearing — both first-class. NOT YET RUN (Stage B). κ₈ dial decision recommended
before Stage B fixes its value.

## VERIFIER STATUS
NOT YET VERIFIED. This record is the constructor pass. Per Self-Hardening
Protocol (verifier-before-record for banked RESULTS), Stage A is foundational
machinery, not a banked physics claim; the banked-physics deliverable is the
Stage-B map, which gets the blind adversarial pass (Stage C). The cross-checks
herein (EL 1e-14, E0 45.604 vs 45.607, breathing tower exact match to #44) are
internal agreements with already-blind-verified prior results (#43 a1f2213b…,
#44 a71e5f8a…), not a substitute for the Stage-C verifier on the map.
