# H3 — PRE-REGISTRATION / solve-MAP: stationary Q_H=1 hopfion on N=0 (FROZEN before compute)

**Mode: pre-registration contract, armchair, NO solve. Frozen BEFORE the hopfion solve (pre-register-before-
testing). Charles-authorized 2026-07-05. Owes a blind verifier before the solve is authorized (Charles: "no
nonlinear solve until this MAP is banked and verified"). DATA-BLIND: no masses/labels/data/fitting.**

## The question (frozen)
Does the native L2+L4 S² carrier admit a stationary **Q_H=1** hopfion on the selected N=0 background, and does
it localize in the BULK so that **√(κ/ξ) ≪ ρ(r_hopf)** rather than becoming core-pinned?

## ★ LOAD-BEARING CLARIFICATION (verifier-corrected a58e9a878c48aff42 — sharpens the H3/H4 split, answers item 6)
In the **static φ-blind sector** there is NO φ-mediated force: the measure √h=r²sinθ is φ-free (B=1/A), the
angular coupling is shift-weight-1 / φ-blind (couples to bare ḡ), and δS_m/δφ=0 ⇒ **no dynamical force pins
the hopfion to any location** (it is free to sit anywhere). **BUT — verifier correction — the hopfion is NOT
metric-free / "invisible to everything":** its ENERGETICS contract with the bare spatial metric
ḡ^{ab}=diag(1,1/ρ²,1/(ρ²sin²θ)) in BOTH L2 and L4, so **the energy sees the areal radius ρ**. The reduction to
flat-space Faddeev–Skyrme holds because **ρ=r is a theorem** (C-2026-06-10-1) ⇒ ḡ_spatial = dr²+r²dΩ² = EXACTLY
Euclidean R³ — not because "the hopfion sees nothing," and not merely "locally flat." Correct decomposition:
- φ-invisibility (measure/coupling/no-source) removes the DILATION e^{2φ} — necessary, not sufficient;
- **ρ=r** makes the residual bare geometry EXACTLY flat → this is what reduces the ENERGETICS to flat
  Faddeev–Skyrme (if ρ(r)≠r, H3 would be a curved-space solve);
- metric-freeness applies ONLY to the CHARGE Q_H (a 3-form, orientation-only) — which is why existence/topology
  is ρ-independent (H1/H2) but the size/energetics are not.
No hidden fold/boundary/curvature re-coupling for a BULK hopfion (support interior, n→n_∞ on a clean slice; the
seal/fold BCs never enter) — re-coupling appears only if the object is pushed to the core/fold = the H4 pinning
question. So **H3 tests: (a) EXISTENCE of a stationary Q_H=1 minimizer, and (b) its SIZE ratio ℓ_hopf/ρ_c** (see
the corrected outcomes). The dynamical position-pinning FORCE is a BACKREACTION effect (Q6) ⇒ DEFERRED to H4.

## The 8 frozen specifications (Charles)

**1. Energy functional.** E[n] = ∫_cell √h d³x [ (ξ/2) ḡ^{ab}∂_a n·∂_b n + (κ/4)|ω_H1|²_ḡ ], with n:cell→S²
(|n|=1); ḡ = the bare/undilated matter metric (φ-blind, C-2026-07-05-1); √h the native φ-free measure; ω_H1 =
ε_abc n_a dn_b∧dn_c (pullback S² area 2-form), |ω_H1|²_ḡ the Faddeev term. **No V(n)** (forbidden under full
SO(3), F2). On the round N=0 background (ρ=r theorem) this reduces to the standard Faddeev–Skyrme energy
E = ∫dr r² ∫dΩ[ (ξ/2)|∇n|² + (κ/4)|F|² ], F_ij = n·(∂_i n×∂_j n). Minimize at fixed Q_H=1.

**2. Fixed-Q_H=1 constraint + numerical measurement.** Q_H = (1/16π²)∫ ε_ijk A_i F_jk d³x (Whitehead/Hopf
integral), where F_jk = n·(∂_j n×∂_k n) is the pullback area form and A the vector potential with F=∇×A
(constructed numerically in Coulomb gauge ∇·A=0 by solving ∇²A=−∇×F, or via the preimage-linking method).
Q_H is a topological integer, PROTECTED under gradient flow (cannot change continuously) — so a Q_H=1 initial
config relaxes WITHIN the sector. Fix by: (a) initialize in the Q_H=1 sector (ansatz winding integers); (b)
MEASURE Q_H post-relaxation, require |Q_H − 1| < tol (round to 1). Q_H measurement is validated in item 8.

**3. Admissible ansatz.** The standard **axially-symmetric toroidal** hopfion ansatz (Q_H = m·l for winding
integers m,l; Q_H=1 = (m,l)=(1,1)) — the simplest hopfion IS axisymmetric, so a **2D reduction in (ρ,z) or
toroidal (η,ξ) coords** should hold Q_H=1 honestly. **Honesty gate:** MEASURE Q_H of the ansatz (item 2) and
require =1; if the axisymmetric ansatz cannot carry Q_H=1 honestly, ESCALATE to bounded 3D. Do NOT impose a
profile BC that fakes the winding (the R0/S³-Skyrme trap — the winding must be carried by the honest map, not
a hand-pinned Θ(core)=π-type BC; here regularity is n→const at core, see item 4). **Scope (verifier):
axisymmetry is justified SPECIFICALLY for Q_H=1 (and 2) — the (1,1) toroidal unknot is the established
axisymmetric minimizer (Faddeev–Niemi / Battye–Sutcliffe / Hietarinta–Salo); Q_H≥7 minimizers are
knotted/non-axisymmetric, so the 2D reduction must NOT be reused at higher charge (the 3D-escalation clause
covers that failure mode).**

**4. Boundary conditions.** **Constant exterior** n→n_∞ (= the N=0 ambient value, e.g. n_∞=ẑ) at the outer
edge of a LOCAL bulk computational ball (NOT the cell seal); **regular core** (n smooth, single-valued at the
hopfion center); **NO private seal, NO private φ-well** (the hopfion is φ-blind; φ is the fixed background).
The outer ball radius R_box ≫ √(κ/ξ) (so the exterior is genuinely constant) but ≪ cell size (a bulk ball) —
and R_box-independence of E, Q_H, size must be checked (else it's box-controlled, outcome D).

**5. Background fields fixed from N=0.** Per the ambient-invisibility clarification, the static φ-blind matter
energy does NOT see φ (φ-free measure + φ-blind coupling), so the ONLY background input is the geometry: ρ=r
(theorem, C-2026-06-10-1) and the cell's ρ-range (ρ_c=1 gauge → ρ_s, running to r_CMB; read from
`cascade_stageB_results.md` at solve time). So the local bulk solve is effectively flat-R³ Faddeev–Skyrme;
the cell enters only through the SIZE COMPARISON √(κ/ξ) vs ρ over the cell's range. (φ(r) is read but does not
enter the static matter energy — confirm this null-dependence numerically as a consistency check.)

**6. φ-backreaction: EXCLUDED at H3, DEFERRED to H4** (per the ★ clarification — at fixed background the
static φ-blind hopfion is ambient-invisible; gravitation + the dynamical pinning force are backreaction = H4).

**7. Grid bounds + anti-hang.** 2D axisymmetric grid, BOUNDED (Nρ≤64, Nz≤64 or toroidal Nη≤64, Nξ≤64 — 2D is
far cheaper than the 3D coupled jacrev solves); relaxation = gradient flow / arrested Newton with the Q_H
sector fixed; **ONE clean process**; bound iterations; **NEVER background-poll a solve** (ANTI-HANG). If it
would exceed budget, REDUCE and report tool-limited (outcome D). Escalate to bounded 3D only if item-3 honesty
gate demands, and only within anti-hang limits.

**8. Verifier requirements before banking ANY positive.**
- **MMS / known-hopfion validation (mandatory):** reproduce the KNOWN flat-space Q_H=1 Faddeev–Skyrme hopfion
  — its **actual published NUMERICAL minimizer energy in an explicitly stated (ξ,κ) normalization** (NOT the
  Vakulenko–Kapitansky value: VK is a LOWER BOUND E ≳ c|Q_H|^{3/4}, not the minimizer energy — verifier
  correction) PLUS its toroidal shape (energy-density ring radius, size) — as proof the method RESOLVES the
  object. If it can't reproduce the known hopfion → outcome D (tool-limited), NOT a physics verdict.
- **Lattice-Hopf pitfall (verifier, name it):** naive finite-difference Q_H drifts OFF integer on coarse grids;
  the "Q_H=1 to integer tol on the known hopfion" guard is correct but REQUIRES a grid fine enough (or a
  geometric/solid-angle lattice-Hopf construction) to resolve the integer — else a real hopfion is mis-flagged.
- Q_H measured = 1 (integer within tol); grid-convergence (E, size stable under refinement); R_box-
  independence (not box-controlled).
- Size √(κ/ξ) computed in ρ-units; compared to the cell's ρ-range (the localization check).
- **Blind adversarial verifier** on any positive before banking (verifier-before-record).

## FROZEN OUTCOMES (verifier-corrected — B was UNREACHABLE as first frozen; now compared to the CORE scale ρ_c)
**Verifier catch (load-bearing):** comparing ℓ_hopf=√(κ/ξ) to "ρ everywhere in the cell" is rigged — the N=0
cell's ρ runs to r_CMB (~Gpc), so any microscopic hopfion ALWAYS has a bulk region with ρ≫ℓ_hopf ⇒ B trivially
false, A trivially true. The honest comparison is to the **CORE/MINIMUM scale ρ_c** (∝√κ, C-2026-07-03-3):
**ℓ_hopf/ρ_c ∝ 1/√ξ** (ρ_c/ℓ_hopf ∝ √ξ; constraint ξN<2 for ρ_c real). ξ is a FREE coupling (CHOSE),
data-blind, so H3 cannot return a DEFINITE bulk-vs-pinned verdict — that needs (i) H4's pinning FORCE and (ii)
a value/anchor for ξ. **H3's honest deliverable = EXISTENCE + the ξ-parametrized ratio ℓ_hopf/ρ_c ∝ 1/√ξ**
(the universal dimensionless Faddeev–Skyrme number × the √κ gauge factor).
- **A — EXISTS + ξ-RATIO:** a finite localized Q_H=1 minimizer exists; report ℓ_hopf/ρ_c ∝ 1/√ξ (the FS number
  × gauge factor). ⇒ hopfion route survives to H4 (backreaction/gravitation, mass, the dynamical pinning FORCE,
  and the ξ-anchor that turns the ratio into a definite bulk-vs-core verdict).
- **B — CORE-SCALE at ξ~O(1):** the minimizer exists but ℓ_hopf ≳ ρ_c at O(1) coupling (ℓ_hopf/ρ_c ∝ 1/√ξ is
  NOT ≪1 for admissible ξ) — a cell/core-scale object, not a cleanly-separated particle, for natural ξ. ⇒ H1's
  localization premise is conditional on large ξ; flag for H4/ξ-anchor, consider reframe. (A SIZE fact vs ρ_c;
  the dynamical-pinning FORCE is H4.)
- **C — NO SOLUTION:** no stationary Q_H=1 localized minimizer under native L2+L4 on flat R³ (via ρ=r) at all.
  ⇒ hopfion route fails cleanly. (Would contradict the known flat-space Faddeev–Skyrme result ⇒ suspect D first.)
- **D — SOLVER INCONCLUSIVE:** classify as tool-limited ONLY if the mandatory known-hopfion benchmark (item 8)
  fails / the method demonstrably cannot resolve the object. Not a physics verdict.
**Note:** A vs B is now the ξ-ratio itself (continuous), reported as a number, NOT a bare binary — the binary
verdict is deferred to H4+ξ-anchor. C and D remain clean binaries at H3.

## Discipline
No masses, no labels, no observational data, no fitting. No nonlinear solve until THIS MAP is banked AND
blind-verified. Anti-hang binding. The static-sector ambient-invisibility (★) is the load-bearing framing —
if a blind verifier finds the hopfion is NOT ambient-invisible at fixed background (e.g. a φ-channel the R0/H1
analysis missed), the H3/H4 split re-opens and this pre-registration is revised before any solve.
