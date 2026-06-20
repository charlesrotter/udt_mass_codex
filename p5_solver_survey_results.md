# P5-STEP-1 — GR-CORPUS SOLVER SURVEY-AND-SELECT (ranked recommendation)

Research record (append-never-edit). **NOT canon.** Mode: MAP/SURVEY (no solver
build; only tiny illustrative timing checks). For Charles's sign-off BEFORE any P5
build. Driver: claude-opus-4-8[1m]. Date: 2026-06-20. Principle 4 binding (mine the
GR corpus; transform a proven method, do not reinvent). DATA-BLIND.

Parent: `EVERYTHING_ON_SOLVER_P5_MAP.md` (this fills in + ranks §III). The operator
matched against is the live stack: `whole_metric_3d_core` (general 4x4 G) + the
P1/P4 pole-stable hybrid `G = G_weyl(diag) + [kernel(full) - kernel(diag)]`;
`p2_matter_s2_fullmetric` (native S^2 unit-3-vector EL, autograd of S=INT sqrt(-g)(L2+L4)
on the full off-diagonal metric); `p3fix_aphi_ruler` (the a(phi) ruler weight);
`p4_time_live` (open-time harmonic balance, d_t^2 -> -omega^2, omega free); bases
Cheb_r x GL_theta x Fourier_psi (`full3d_spectral`); the dense-Newton ANCHOR
(`full3d_newton`, jacrev + direct LM, ~1e-13 small grid = the correctness reference).

---

## 0. THE OPERATOR IN ONE PARAGRAPH (what every method must match)

Unknowns: 5-8 fields on a (Nr,Nth,Nps) spectral tensor grid — diagonal Weyl warps
a,b,c,d (B=1/A FREE), optional spatial off-diagonals e_rt,e_rp,e_tp, the native S^2
matter profile F, plus (time-live) amplitudes a1,b1,F1 and a FREE eigenvalue omega.
Residual = mixed Einstein G^mu_nu - kap8 T^mu_nu (4 diagonal + 3 spatial off-diagonal
+ the live t-row) + the native-S^2 matter EL (autograd of the action) + strong BC
rows (winding node F[core]=pi/F[seal]=0, seal gauge, depth dial). The matter EL is
varied on the FULL off-diagonal metric (P2). a(phi)=ruler weight W(phi) multiplies T
(P3; k=0 -> GR). The TIME row is harmonic-balanced: omega is an eigenvalue, sought
free. **The conditioning root: the steep soliton core b = p*ln(r/r_seal) gives a
1/r-derivative core that makes the raw general-Einstein kernel badly conditioned at
the Cheb core edge (G^t_t~16 vs the true ~0.28) — this forced the pole-stable hybrid,
and it is THE problem any P5 preconditioner must attack.**

What has already FAILED (do not repeat): matrix-free Jacobi-PCG LM stalls off-round
~1e-5 (#60, the PCG step is not a descent direction); plain warm-start continuation
DRIFTS (interp injects non-axisym structure into steep solitons; m=1 0.292->0.332).
What WORKS but does not scale: the dense jacrev-Newton ANCHOR (~1e-13, ~16 quadratic
iters), throughput-bound by the Jacobian BUILD.

---

## 1. THE THROUGHPUT-VS-CONDITIONING VERDICT (measured this session — decisive)

**The ~1700s/solve is NOT the broken-NVML allocator. It is the jacrev Jacobian
BUILD, fundamentally.** Measured on this V100/torch-float64 stack:

| grid | quantity | CACHING allocator (default) | NO-CACHE (the scripts' workaround) |
|------|----------|------------------------------|------------------------------------|
| (16,6,8), nF=4224,nU=3840 | jacrev build | 9.19 s | 9.18 s |
| (24,8,8), nF=9728,nU=7680 | jacrev build | 49.5 s | 49.5 s |

Per-iteration cost split at (24,8,8): **jacrev BUILD = 49.5 s, lstsq SOLVE = 0.82 s,
residual eval = 0.021 s.** => ~98% of each Newton iteration is the Jacobian build;
the direct linear step and residual are negligible. ~16 quadratic iters => ~800 s at
Nr=24 (consistent with the documented ~1700 s at larger/coupled grids).

TWO load-bearing corrections to the standing assumption:
1. **The caching allocator does NOT crash here and is the SAME speed** (cache==nocache
   to 3 sig figs). The "broken-NVML no-cache allocator" is not the throughput wall and
   is not even required for jacrev at these grids on the current stack. (The original
   NVML assert may have been chunk-size/driver-state specific; with
   `PYTORCH_NVML_BASED_CUDA_CHECK=0` the default caching allocator ran clean and free.)
2. **Therefore fixing the allocator is NOT the cheap big win the P5 map hypothesized.**
   The cheap win, if any, is elsewhere: the Jacobian BUILD is O(nF) reverse-mode passes
   (vmapped) — cost grows ~ (grid)^2. The way to make the EXACT Newton step affordable
   is to STOP building the full dense Jacobian, OR to apply J/J^T matrix-free inside a
   Krylov solve with a real preconditioner (so the build never happens). The dense
   anchor cannot itself be scaled much by an allocator fix; it is build-bound by design.

VERDICT: throughput is a **conditioning/Jacobian-build** problem, not an allocator
problem. P5 must remove the dense build, not tune memory.

---

## 2. RANKED RECOMMENDATION

| Rank | Method (GR-corpus lineage) | Fit to our operator | Attacks steep-core conditioning? | Throughput on V100 | Anchor-checkable? | Hybrid upgrade needed? |
|------|----------------------------|---------------------|----------------------------------|--------------------|-------------------|------------------------|
| **1** | **Newton-Krylov / JFNK + physics-based (operator-split / radial-elliptic) preconditioner** (Knoll-Keyes survey; KADATH's Newton-Raphson; standard NR) | HIGH — keeps Newton quadratic + anchor correctness; matrix-free JVP already exists (`lm_step`); handles coupled Einstein+S^2+a(phi)+free-omega via an augmented residual | YES, directly — the preconditioner is built to invert the steep-radial elliptic part (the conditioning root); this is the textbook cure for the #60 PCG stall (Jacobi was the wrong preconditioner, not CG) | BEST — no dense build; cost = (Krylov iters x JVP); a good PC makes Krylov iters O(10s) not O(stall) | YES — must reproduce the anchor on every shared case to floor | NO for round/mild off-round (the tractable channel); the hybrid's small-shear regime is enough to START; upgrade only if the converged solve runs A>~0.1 |
| **2** | **Self-Consistent Field, KEH/Hachisu transformed** (Komatsu-Eriguchi-Hachisu 1989; Hachisu 1986; the RNS/boson-star workhorse — integral Green's-function inversion) | MEDIUM-HIGH — purpose-built for coupled Einstein-matter EQUILIBRIA; the integral inversion SIDESTEPS the steep-operator conditioning entirely (its core selling point) | YES, by construction — never forms/inverts the stiff differential operator; inverts a flat-space Green's function instead | GOOD — each SCF sweep is cheap; convergence is linear (slower than Newton near the floor) | YES — at the floor it must match the anchor | RISK: classic KEH assumes stationarity + a specific gauge/conformal split; transforming it to time-live harmonic-balance + native-S^2 + a(phi) without freezing a DOF/gauge is the work and the smuggle-risk |
| 3 | **Sparse-direct on the spectral block structure** (make the EXACT dense Newton step affordable) | MEDIUM — the anchor's exact step, cheaper | NO (does not change conditioning; only the cost of the exact step) | conditional — spectral operators are DENSE in each 1-D direction; block-sparse only across the tensor product; engineering-heavy, uncertain payoff | YES — IS the anchor, faster | inherits the hybrid as-is |
| 4 | **Boson-star / gravitating-soliton frequency-eigenvalue solver** (Kaup/Ruffini-Bonazzola lineage; FBS, rotating boson-star chains) | HIGH on STRUCTURE (matter+metric+free-omega = our exact time-live object) but the established codes are 1-D/spherical | partially (shooting tames radial stiffness in 1-D) | N/A as a standalone 3-D engine | the 1-D/round limit IS an anchor case | — its 3-D generalization just becomes method 1 or 2; best used as a VALIDATION oracle + omega-branch seed, not the 3-D engine |
| 5 | **Multigrid (geometric/algebraic) as the PC inside method 1** | MEDIUM — optimal elliptic PC in principle | YES if it can coarsen the steep core | high build complexity on Cheb x GL x Fourier non-uniform bases | via method 1 | via method 1 |
| 6 | **Pseudo-arclength continuation** (Keller) — a TOOL, not a base solver | pairs with method 1/2 for the free-omega branch + folds | no (orthogonal concern) | cheap wrapper | yes | — adopt ONLY after a base solver converges; it is the principled replacement for the FAILED warm-start, used for omega-branch/fold tracking |

**TOP PICK: #1 Newton-Krylov / JFNK with a physics-based preconditioner.**
**RUNNER-UP: #2 KEH/Hachisu SCF (the de-risking fallback if the PC proves too hard).**

### Why #1 over #2 (the decisive trade-offs)
- The dense anchor PROVES a Newton solution exists at the floor (~1e-13) and converges
  quadratically. The ONLY thing missing is affordability of the step. JFNK keeps EXACTLY
  that Newton (anchor-identical fixed point, quadratic tail) while removing the dense
  build via matrix-free JVP/VJP — which the codebase ALREADY has (`full3d_solver.lm_step`).
- The #60 stall was diagnosed as "PCG step not a descent direction" with a JACOBI
  preconditioner. That is a textbook symptom of an INADEQUATE preconditioner on a stiff
  elliptic operator, NOT a failure of Krylov. The Knoll-Keyes physics-based-PC program
  exists precisely for this: precondition with the dominant physical (radial-elliptic /
  steep-core) operator, not an algebraic diagonal. This converts the failed #60 line into
  the recommended line by swapping ONE component (the preconditioner), reusing the rest.
- KADATH — the modern GR spectral workhorse for strongly nonlinear coupled
  Einstein-matter (incl. boson stars) — uses exactly Newton-Raphson on a spectral
  multidomain discretization. Our stack is a single-domain version of the same; #1 is the
  closest faithful transform of that proven lineage.

### Why #2 is the runner-up (not the lead)
- KEH/Hachisu is the most BATTLE-TESTED method for our equilibrium class and its
  Green's-function inversion structurally dodges the conditioning root — a genuine
  advantage. BUT it is built around stationarity and a conformal/gauge split; bending it
  to (a) time-live harmonic balance with a free omega and (b) the native-S^2 unit-vector
  EL on the full off-diagonal metric, WITHOUT freezing a DOF or importing a gauge, is
  real research risk and a smuggle surface (premise ledger below). It converges linearly,
  so it cannot hit the ~1e-13 anchor floor as cheaply as Newton near convergence.
  Recommended posture: **build #1; hold #2 as the de-risk fallback** if a working PC for
  the coupled off-round operator proves elusive.

---

## 3. PREMISE LEDGER PER RANKED METHOD (smuggle risks + guards)

### #1 Newton-Krylov / JFNK + physics PC
| risk | how it could smuggle | guard |
|------|---------------------|-------|
| PC changes the fixed point | a too-aggressive/inconsistent PC could converge to a different solution | a preconditioner only reshapes the PATH, never the zero set; VERIFY converged solution is PC-INDEPENDENT (run 2 PCs, same answer) + matches the dense anchor on shared cases (P5-anchor, P5-precond) |
| Inexact JVP hides a dropped term | matrix-free JVP via autograd must differentiate the SAME residual the anchor uses | byte-equality of the residual VALUE to `full3d_newton.residual_vector_vsafe` (already the anchor's own residual); the JVP is autograd of it, not a hand-coded linearization |
| Krylov tolerance masquerades as convergence | loose inner tol -> outer "Newton" that isn't quadratic | require the quadratic tail to reproduce the anchor's iter count + floor on round/mild cases before trusting off-round |
| Hybrid outgrown silently | off-round solve pushes shear A>~0.1 outside hybrid validity (P1: err~0.5*A) | monitor max off-diagonal magnitude; if A>~0.1, the hybrid result is solver-limited -> upgrade to true general Einstein (scope expansion, §5) |
| Box-control baked in by the PC | a PC tied to cell size R could induce R-dependence | Gate A (R-independence) on every "intrinsic" off-round result; PC must be R-agnostic |

### #2 KEH/Hachisu SCF (transformed)
| risk | how it could smuggle | guard |
|------|---------------------|-------|
| Frozen DOF / gauge to make SCF close | classic KEH fixes a conformal factor / a gauge / an integrability constant | FORBIDDEN beyond declared (P5-frozen, binding "everything-on"); flag EVERY field held fixed within a sweep; the time-live + B=1/A-free content must remain live |
| Imported BC via a borrowed template | RNS/boson-star templates carry their own surface/asymptotic BCs | keep the NATIVE BC set (winding node, seal gauge, depth dial); grep for any Skyrme/B=1/A/asymptotic-flatness import (#61) |
| Green's-function inversion assumes a background | the flat-space Green's function presumes an asymptotic structure UDT may not share (finite mirrored cell, no spatial infinity — CANON) | the inversion kernel must respect the finite-cell domain, NOT a 1/r asymptotic; verify against the anchor on the finite cell |
| Linear convergence read as a floor | SCF stalls above the anchor floor and is called "converged" | must reach the anchor floor on shared cases; report the achieved floor honestly |

### #3 Sparse-direct
| risk | guard |
|------|-------|
| Assumed sparsity that isn't there (spectral = dense per direction) | measure the actual fill before committing; if dense, abandon — it is the anchor with more engineering |

### #4 Boson-star frequency-eigenvalue (as oracle)
| risk | guard |
|------|-------|
| Spherical reduction smuggles roundness | use ONLY as the round/1-D anchor + omega seed; never as the off-round verdict engine |

### #6 Pseudo-arclength continuation
| risk | guard |
|------|-------|
| Re-finds nearby critical points (the warm-start drift failure mode) | the principled arclength predictor-corrector with a TANGENT solve (not naive interp) + a base solver that DESCENDS; validate against direct solves at each step (the gate the warm-start FAILED) |

---

## 4. THE POLE-STABLE-HYBRID VERDICT (upgrade needed? cost?)

**For the recommended top method (#1) on the TRACTABLE channel (round / mild
off-round / the P4 time-live round wave): NO upgrade needed to START.** The hybrid is
exact at zero off-diagonal (machine-0, both P1 and P4 verifiers, bitwise containment),
and accurate to ~O(A) on the off-diagonal blocks / ~O(A^2) on the diagonal
back-reaction for small shear A. The P4 surviving-d_t^2 channel and the round/near-round
time-live solve live in that regime.

**Upgrade IS required IF the off-round solve self-consistently runs to large shear
(A >~ 0.1).** Then the hybrid's linear-in-A error corrupts the off-diagonal field
equations (P1 verifier headline: err_rth ~= 0.5*A). This is the P5-hybrid risk in the
map and a REAL possible scope expansion: a genuinely well-conditioned GENERAL 4x4
Einstein (not the difference-hybrid) on the steep core. Likely route: the analytic
pole-stable Weyl engine (`einstein_3d_eval`, which symbolically cancels cot/1/sin) is
already general for the DIAGONAL Weyl class; the upgrade is to extend that ANALYTIC
cancellation to the spatial off-diagonal metric components (sympy-derive G^mu_nu for
the full off-diagonal metric, evaluate only smooth warp derivatives spectrally) —
medium effort (a `gen_einstein_3d_*` extension), not a rewrite. RECOMMENDATION: build
#1 on the hybrid; instrument max|A|; trigger the analytic-general-Einstein upgrade only
if/when the converged solve demands it (don't pre-pay the scope).

---

## 5. CONCRETE P5-BUILD SHAPE FOR THE TOP METHOD (#1) — for scope judgment, NOT a build

Phased, every phase anchor-gated:

- **P5a — PRECONDITIONER PROTOTYPE (the crux; de-risk first).** Build a physics-based
  preconditioner that inverts the dominant steep-radial-elliptic block of the coupled
  operator (operator-split: metric-Laplacian-like part + matter-EL part). Test it as a
  Krylov PC on the EXISTING `lm_step` matrix-free JVP. SUCCESS GATE: the #60 axisym
  CONTROL (a known relax-to-round) converges to the round floor (Phi~1e-9, tvar->1e-3)
  where Jacobi-PCG stalled at 1e-5. If P5a fails after honest effort -> switch to #2
  (KEH). This phase decides feasibility cheaply.
- **P5b — ANCHOR REPRODUCTION.** On every case the dense anchor can run (round, mild
  off-round, small grids), JFNK must reproduce it to floor (~1e-13) with the quadratic
  tail. Gate: PC-independence (two PCs, same converged solution). This is the #1-risk
  guard (convergence-to-wrong-answer).
- **P5c — OFF-ROUND AT SCALE.** Run the off-round static coupled solve (P2-shear: are
  the solved off-diagonals zero or genuinely nonzero?) at 32^3-class grids the anchor
  cannot reach. Instrument max|A| vs the hybrid validity bound; box-control (Gate A) on
  any intrinsic result. Report grid/Nth-convergence.
- **P5d — TIME-LIVE FREE-OMEGA.** Augment the residual with the P4 harmonic-balance
  t-row + omega as an unknown (one extra residual = a phase/normalization closure);
  solve for the free-omega eigenvalue on the off-round carrier. Pair with #6
  pseudo-arclength continuation for the omega-branch / folds (the principled replacement
  for the failed warm-start).
- **P5e — DEEP-phi + a(phi).** Turn the ruler weight k!=0 (P3) and push toward the deep
  core where a(phi) departs from GR O(1); needs an honest deep core (P6). Anchor-gated.

Throughput expectation: each JFNK iteration becomes (Krylov_iters x JVP_cost). JVP cost
~ one residual+grad ~ O(0.1-1 s) at these grids (vs the 49.5 s dense BUILD); a good PC
gives O(10) Krylov iters/Newton step => ~seconds-to-tens-of-seconds per Newton iter,
i.e. potentially 1-2 orders faster than the dense anchor AND scalable to 32^3 — the
payoff that makes the off-round time-live solve reachable. (Contingent on P5a; that is
why P5a is gated first.)

---

## 6. COMPLETENESS BAR (restated, binding for any P5 result)
A P5 off-round result MEANS something only when: (1) the new solver reproduces the
dense anchor on every shared case to floor; (2) the #60 axisym CONTROL converges;
(3) converged to floor + grid/Nth-converged + box-control (Gate A) checked; (4) the
pole-stable hybrid verified valid in the solved shear regime (or upgraded per §4);
(5) the converged solution is preconditioner-INDEPENDENT. Until all hold, OFF-ROUND =
solver-limited, not a verdict (Risk 1, the program's load-bearing feasibility risk).

---

## 7. CORPUS LINEAGE (Principle 4 — what is being transformed, not invented)
- JFNK + physics-based PC: Knoll & Keyes, *JCP* 193 (2004) "Jacobian-free
  Newton-Krylov methods: a survey of approaches and applications".
- Spectral Newton-Raphson for coupled Einstein-matter (incl. boson stars): Grandclement,
  *JCP* 229 (2010) "KADATH: a spectral solver for theoretical physics" (arXiv:0909.1228);
  LORENE lineage.
- SCF: Hachisu (1986) self-consistent field; Komatsu, Eriguchi & Hachisu (1989) KEH; the
  RNS rotating-neutron-star code.
- Frequency-eigenvalue gravitating solitons: Kaup; Ruffini-Bonazzola; fermion-boson &
  rotating boson-star families (recent: arXiv:2403.13052, 2512.07610).
- Pseudo-arclength continuation: Keller (1977).
Each is matched to OUR operator in §2-§5; none is imported as new physics — the field
equations remain the native general Einstein + native S^2 L2+L4 + a(phi) ruler.

---

## 8. VERIFIER NOTE
Survey + timing measurements only (no solver built). The throughput split (§1) is the
one empirical claim and is reproducible: `/tmp/p5_alloc_timing.py`,
`/tmp/p5_alloc_timing2.py`, `/tmp/p5_split.py` (scratch, not committed) time
`full3d_newton.jacobian_jacrev` cache-on vs no-cache and the build/solve/residual
split. A blind verifier should re-time on a fresh process (the allocator decision is
import-time) and re-confirm cache==nocache speed + build-dominated cost before the §1
verdict ("allocator is not the wall") is banked.
