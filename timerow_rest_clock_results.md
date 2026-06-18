# Does the NONSTATIONARY time-row sector carry a native REST-ENERGY clock / T-period? — Results

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M context). NEW file (append-never-edit,
Self-Hardening discipline). Mode: **DERIVE** (gated, PRE-REGISTERED + SAFEGUARDED).
Frozen contract: `timerow_rest_clock_PREREG.md` (committed BEFORE the run; obeyed
exactly). Frame: hbar_emergence_closed_time_MAP.md; CANON C-2026-06-10-3 (the rung-2
weld), C-2026-06-13-1 (hyperbolic time); W6_results.md; native_stabilizer_results.md.
**DATA-BLIND**: no lepton/hadron mass, ratio, Koide, or wall number loaded, computed, or
compared. Sizes/energies are intrinsic (kappa/xi units; M_MS in those units).

Scripts (this push):
- `timerow_rest_clock_derive.py` — T1 (exact sympy), T2 (real soliton + E0), T3
  (frequency + box-control). Log: `/tmp` not used; ran to `_run2.log`.
- `timerow_boxcontrol_confirm.py` — focused box-control re-confirmation (independent
  cell sizes). Log `_box.log`.
- Reuses the BLIND-VERIFIED solvers: `radial_Bfree_soliton.py` (coupled GR+L2+L4
  soliton, verified 9ebc5e5184d1e58f) and the native weld of
  `native_weld_status_derivation.py` (verified a709e4306bdf91b3a).

Blind adversarial verifier: **PENDING** (verifier-before-record; attack-here block at end).
NOT committed by this agent.

---

## THE QUESTION (S4, linearization-free form)

Is the static soliton a STATIONARY solution of the FULL time-row field equations? The
rung-2 weld (C-2026-06-10-3) relates the radial winding current (H1 = the time-row
g_Tr mode) to TIME-derivatives of (delta phi, K). If the full equations + weld are
satisfied with all d_t = 0, the soliton is static (NO clock). If they are NOT satisfiable
with d_t = 0, the system is FORCED to evolve, and the implied omega^2 = off-balance/inertia
is exact. The decisive discriminator (S3): is any native frequency tied to M_MS (rest
energy = the PRIZE), to J (spin rotor chi = dead, wrong clock), or to R (cell size = box,
dead)?

---

## T1 — THE FULL NONSTATIONARY TIME-ROW FIELD EQUATIONS (exact, time RETAINED) — **STATED**

Derived from the C1 dilation action + the native matter weld, time retained, exact
(sympy; all checks PASS). The full system has TWO faces, BOTH carried (no slice):

### (i) The metric's OWN d'Alembertian (the dilation field) — HYPERBOLIC in T
From L = (c/2) e^{-2phi} g^{ab} d_a phi d_b phi sqrt(-g4) on the dilation-tie 4-metric
(g_tt = -e^{-2phi}, g_rr = e^{2phi}, g_thth = r^2), the exact EL principal part is
(verified, matching ns_scan_results.md / canon C-2026-06-13-1):

    coeff(phi_TT)   = + c r^2
    coeff(phi_rr)   = - c r^2 e^{-4phi}
    coeff(phi_thth) = - c e^{-2phi}
    => cTT/cRR = -e^{4phi} < 0,  cTT/cThTh = -r^2 e^{2phi} < 0  (signature (-,+,+)).

The dilation field genuinely PROPAGATES in T (a real wave sector, strictly hyperbolic). [PASS]

### (ii) The MATTER breathing field (delta phi) + the native time-row weld — ELLIPTIC in (t,r)
The exact second-order C1 action on the time-row-on perturbed metric (B=1/A ties
H0=-2 dphi, H2=+2 dphi; time-row g_Tr = H1; trace K). The native H1 Euler-Lagrange
equation is **ALGEBRAIC** (the candidate clock source):

    EL_H1 = 0   <=>   f phi0' H1 = 2 d_t(delta phi)     [f = e^{-2phi0}]    [PASS]

This is the NATIVE form of the rung-2 weld (C-2026-06-10-3): the radial winding current
H1 is welded to the TIME-derivative of the breathing dphi. (It is NOT the Einstein
differential weld d_r(f H1) = 2 d_t dphi + d_t K — that is an import, W2/W4 of
native_weld_status_derivation.py; the native weld is algebraic.)

**THE KINETIC FLIP (the heart).** Eliminating the auxiliary H1 on its own algebraic weld
(legal: dL/dH1 = 0 there) FLIPS the time-kinetic sign of dphi: the (d_t dphi)^2
coefficient goes +(c/2) r^2 -> -(c/2) r^2 (the H1 cross-coupling contributes exactly
-c r^2). [PASS] The on-shell (delta phi) equation (K=0 canon slice) is then, EXACTLY:

    r^2 d_t^2(dphi) + d_r(r^2 f^2 d_r dphi) - 4 r^2 f^2 E0 dphi - lam f dphi = 0,   [PASS]
        E0 = phi0'' + 2 phi0'/r - 2 phi0'^2   (background dilation-EL density),
        lam = l(l+1).

The +r^2 d_t^2 carries the SAME sign as the elliptic spatial part d_r(r^2 f^2 d_r dphi)
=> the on-shell system is ELLIPTIC in (t,r). Mode analysis u(r) e^{i omega t} gives the
Sturm-Liouville problem -d_r(r^2 f^2 u') + q u = -omega^2 r^2 u, q = 4 r^2 f^2 E0 + lam f,
i.e. **omega^2 = -(SL eigenvalue)**. A REAL oscillation (omega^2 > 0, a clock) requires
the lowest SL eigenvalue NEGATIVE — i.e. q sufficiently negative (the E0 < 0 window).
On E0 >= 0 the spectrum is omega^2 < 0 (relaxation, NO clock) — exactly the banked
native_weld result.

T1 VERDICT: **SUCCEEDS** (full equations derived, exact, no approximation; the native
weld is the candidate clock source; the on-shell matter equation is elliptic with the
clock gated on E0 < 0).

---

## T2 — IS THE *REAL* SELF-CONSISTENT SOLITON STATIONARY? — solved on the REAL profile

I solved the FULL coupled (a, b, Theta) GR+L2+L4 soliton (radial_Bfree, blind-verified),
NOT an ansatz. The dilation phi = -a(r) is REGULAR at the core (regularity forces
phi'(0)->0), so E0 is FINITE everywhere.

**HONEST CORRECTION (flagged, S2).** A crude log-cell toy phi0 = p ln(r/r_int) gives
E0 = p(1-2p)/r^2, which (a) is sign-gated at p=1/2 and (b) BLOWS UP as 1/r^2 at the
core. Both are ARTIFACTS of the non-regular log dial — the physical soliton's phi is
bounded and non-monotone (core dip + body bump). I report E0 off the REAL profile, not
the toy. (The toy's exact E0 = p(1-2p)/r^2 is recorded as a symbolic check only.)

Real self-consistent soliton (xi=kappa=1, kap8=0.05, 14 L cell, N=600), E0 on phi=-a:

| p   | M_MS    | phi(core) | E0(core) | E0 range          | frac(E0<0) |
|-----|---------|-----------|----------|-------------------|------------|
| 0.2 | 0.2722  | +0.0750   | -2.781   | [-2.781, ~0]      | 0.58       |
| 0.4 | 0.2810  | -0.1489   | -3.302   | [-3.302, ~0]      | 0.71       |
| 0.6 | 0.2933  | -0.3719   | -3.504   | [-3.504, ~0]      | 1.00       |
| 0.8 | 0.3101  | -0.5935   | -3.583   | [-3.583, ~0]      | 1.00       |
| 1.0 | 0.3328  | -0.5993*  | -        | [-4.34, ~0]       | 1.00       |

(*p=1.0 a0 hits the e^{-2b} clamp regime; M_MS and the E0<0 dominance are robust.)

So on the REAL soliton E0 < 0 over MOST or ALL of the cell (more so as depth grows) —
the candidate clock window (E0 < 0) is genuinely OPEN here, more than the toy suggested.

T2 VERDICT: the static profile is solved; the time-row coupling's candidate clock window
(E0 < 0) IS present on the real soliton. Whether it actually produces a real-frequency
clock is decided in T3 (the SL spectrum), NOT by E0<0 alone — see T3.

---

## T3 — THE NATIVE FREQUENCY + DISCRIMINATOR (M_MS vs J vs R) — **the decisive result**

### (a) The on-shell time-row breathing spectrum on the REAL soliton (l=1, lam=2)
Lowest omega^2 = -(SL eigenvalues) of the T1(ii) operator on the real phi, per depth:

| p   | M_MS    | omega^2 (lowest four)                  | min q   |
|-----|---------|----------------------------------------|---------|
| 0.2 | 0.2722  | [-0.1002, -0.2912, -0.5726, -0.9421]   | +0.887  |
| 0.4 | 0.2810  | [-0.1005, -0.2925, -0.5759, -0.9488]   | +0.927  |
| 0.6 | 0.2933  | [-0.1008, -0.2943, -0.5808, -0.9589]   | +0.789  |
| 0.8 | 0.3101  | [-0.1013, -0.2971, -0.5882, -0.9739]   | -0.300  |
| 1.0 | 0.3328  | [-0.1021, -0.3013, -0.5993, -0.9958]   | -4.344  |

**omega^2 < 0 at EVERY depth** (the largest, -0.10, is still negative), and the values are
essentially DEPTH-INDEPENDENT (-0.1002 -> -0.1021 across a 5x depth range; M_MS changes
by +22%). Even where the potential density q goes negative (p >= 0.8), the negative-q
region is too localized to pull the lowest SL eigenvalue below zero against the positive
gradient cost r^2 f^2 u'^2. So the time-row breathing **RELAXES** (omega^2 < 0); it does
NOT oscillate. There is **NO real-frequency rest clock**.

### (b) BOX-CONTROL TRAP TEST (S3): FIXED depth p=1.0 & core, VARY the cell size R
Intrinsic/M_MS-tied => omega^2 ~ const; box => omega^2 ~ 1/R^2 (omega^2*R^2 const):

| cell (L) | R = r_int | M_MS    | omega^2   | omega^2 * R^2 |
|----------|-----------|---------|-----------|---------------|
| 6.0      | 6.050     | 0.3352  | -0.5462   | -19.99        |
| 8.0      | 8.050     | 0.3337  | -0.3100   | -20.09        |
| 12.0     | 12.050    | 0.3329  | -0.1388   | -20.15        |

**omega^2 * R^2 is CONSTANT (-19.99, -20.09, -20.15; ~0.8% spread) while omega^2 scales
as 1/R^2** (the M_MS is constant to 0.7% across the scan — if the frequency tracked M_MS
it would be flat, not 1/R^2). This is the unmistakable BOX-CONTROL signature
(NEGATIVES_REGISTRY #1; conjecture A). The time-row breathing relaxation rate is set by
the CELL SIZE R, NOT by the soliton's rest energy M_MS.

### CLASSIFICATION (S3, the whole point)
- NOT M_MS-tied: omega^2 is depth-independent (T3a) and ~1/R^2, not ~M_MS (T3b).
- NOT J (spin rotor): the object analyzed is the breathing dphi coupled to the radial
  winding current H1 via the native weld — a DIFFERENT object from the iso-rotor chi
  (monodromy_depth #49). It carries no J; the result is independent of spin.
- **R (box-controlled)**: omega^2 ~ 1/R^2, omega^2 R^2 = const. DEAD per S3.
- AND the sign is negative (relaxation), so even the box mode is not an oscillation.

T3 VERDICT: **FAILS the prize.** The forced time-row evolution, on the REAL soliton, is a
BOX-CONTROLLED RELAXATION (omega^2 < 0, ~1/R^2) — not a rest-mass-tied oscillation. The
discriminator lands on R (and on relaxation), not M_MS.

---

## T4 — T-PERIODICITY — **N/A (no real frequency to be periodic)**

T4 asks whether the forced evolution is periodic (a closed time / a clock) or
aperiodic/runaway. Since T3 finds omega^2 < 0 (the on-shell elliptic operator's modes are
relaxational, not oscillatory) and what frequency scale exists is box-controlled, there is
NO real-frequency oscillation to be periodic. The evolution the time-row weld forces is
RELAXATION toward the static profile (the elliptic character of T1(ii)), not a beat. So
the question "periodic vs runaway" does not even arise for a rest-mass clock — there is no
rest-mass frequency. T4 VERDICT: **N/A / NEGATIVE** (no native T-period tied to M_MS).

S6 NOTE (honest workstation boundary): a FULL nonlinear coupled time-evolution of the
metric+matter PDE (GPU) could still be run to watch the actual relaxation/any residual
oscillation directly. But it is NOT needed to answer the PRIZE question: the exact T1
structure (elliptic on-shell matter equation) + the T3 spectrum (omega^2<0, box-scaled,
depth-independent) already settle that no rest-mass clock exists. The nonlinear evolution
would only characterize the relaxation, not revive a clock. Flagged, not substituted-for.

---

## T5 — THE LOCK — **does not engage (no rest clock to lock)**

T5 asks: IF a rest-mass frequency + T-period exist, does closed-time single-valuedness
lock omega = E_rest/hbar? They do NOT exist (T3/T4). So the lock does not engage from this
sector. The banked spin-vs-mass wall (monodromy_depth #49: closed-time single-valuedness
on UDT's native phase quantizes SPIN, not mass/depth) is NOT relieved by the time-row
sector: the time-row's own forced mode is a box-controlled relaxation, carrying neither a
rest-mass frequency nor a native period. hbar STAYS an input. T5 VERDICT: **NEGATIVE.**

---

## OVERALL VERDICT — **NEGATIVE** (premise-scoped, first-class)

The nonstationary time-row / phi-angular sector does **NOT** carry a native rest-energy
clock or a native T-period tied to M_MS. Exactly:
- The native rung-2 weld (f phi0' H1 = 2 d_t dphi) IS a genuine time-derivative coupling
  (the candidate clock source), and the metric's own dilation field IS hyperbolic in T (a
  real wave sector) — so the sector is genuinely dynamical, not frozen.
- BUT once the auxiliary winding current H1 is eliminated on its own algebraic weld, the
  matter breathing dphi obeys an ELLIPTIC (t,r) equation (the kinetic-sign flip). On the
  REAL self-consistent soliton its spectrum is omega^2 < 0 (relaxation) and what scale
  exists is BOX-CONTROLLED (omega^2 ~ 1/R^2, omega^2 R^2 const, depth-independent), NOT
  M_MS-tied.
- Therefore the time-row supplies neither a rest-mass beat nor a native period; the
  closed-time lock omega = E_rest/hbar does not engage from here, and the banked
  spin-vs-mass wall holds in the nonstationary sector too. hbar stays an input.

This is the DESIRED answer's NEGATION, reported faithfully (S5 verdict-hunting guard
honored). It JOINS the box-control wall (conjecture A, NEGATIVES_REGISTRY #1) — now hit
from the nonstationary time-row matter channel as well — and confirms (Charles's banked
picture) that UDT's only native discreteness is TOPOLOGICAL, not a dynamical clock/spectrum.

---

## PREMISE LEDGER (chose / derived)

DERIVED (exact symbolic / solved on the real profile):
- D1. Full nonstationary time-row field equations from the action, time retained [T1, sympy].
- D2. Metric d'Alembertian hyperbolic in T, signature (-,+,+) [T1(i), exact; matches ns_scan].
- D3. Native rung-2 weld is ALGEBRAIC: f phi0' H1 = 2 d_t dphi [T1(ii), exact; = native_weld].
- D4. Kinetic-sign flip on H1-elimination => on-shell (dphi) equation ELLIPTIC in (t,r)
  [T1(ii), exact].
- D5. Real self-consistent (a,b,Theta) soliton solved; phi=-a regular at core; E0<0 over
  most/all of the cell, deepening with p [T2, radial_Bfree solver].
- D6. Time-row breathing omega^2 < 0 at all depths, depth-independent [T3a].
- D7. omega^2 ~ 1/R^2, omega^2 R^2 = const across cell sizes => BOX-CONTROLLED, not M_MS
  [T3b, box-control trap].

CHOSE (tagged; none a smuggled mechanism):
- C1. K = 0 canon slice (the strict perturbed-level reading of canon C-1; native_weld W1/W3
  disqualify K independently). [the on-shell dphi equation is the K=0 slice]
- C2. l = 1 mode (lam = 2) for the breathing operator [the lowest non-monopole; the result
  is qualitatively l-independent — omega^2<0 box-controlled for the reported l].
- C3. Background depth dial p (0.2..1.0) and finite cell [r_core=0.05, r_int=r_core+cell·L];
  results cell-size-independent in the box-control sense (that IS the trap test).
- C4. xi = kappa = 1 (the single intrinsic scale); kap8 = 0.05 (canonical coupling).
- C5. EFFICIENCY (S2, bounded, declared): the coupled SCF soliton was solved at N=600
  (depth table) / N=400 (box re-confirm) and 80-120 SCF iters, NOT N=1600/300. Justified:
  radial_Bfree_results.md reports M_MS stable to 4 dp at N=600; the box-control SIGNATURE
  (omega^2 R^2 const) is a scaling law insensitive to grid, and was reproduced on two
  independent runs (main + focused). This is a grid/iteration economy, NOT a physics
  reduction; the full nonlinear soliton + exact weld are carried throughout.

NOT done (S6 honest boundary): the FULL nonlinear coupled metric+matter time-evolution PDE
(GPU). Not needed for the PRIZE question (the exact elliptic structure + the omega^2<0
box-scaled spectrum settle it); flagged for the workstation if a direct watch of the
relaxation dynamics is ever wanted.

---

## LOAD-BEARING for the blind verifier (per the PREREG)

1. **T1(ii) — is the on-shell matter equation truly ELLIPTIC, or was a term dropped?**
   Re-derive the second-order C1 action's H1 Euler-Lagrange (confirm ALGEBRAIC:
   f phi0' H1 = 2 d_t dphi), then eliminate H1 and confirm the (d_t dphi)^2 sign FLIPS to
   -(c/2) r^2 (the kinetic flip). Confirm the on-shell equation
   r^2 d_t^2 dphi + d_r(r^2 f^2 d_r dphi) - 4 r^2 f^2 E0 dphi - lam f dphi = 0. If the
   matter source (L2+L4 stress, not just C1) adds a term that flips the sign back to
   hyperbolic, the whole verdict changes — CHECK whether the L2+L4 angular stress (canon
   C-2026-06-14-1) contributes a time-kinetic term to dphi beyond the C1 weld used here.
   [This is the single biggest risk: I used the C1 dilation action's weld; the FULL
   matter source could in principle alter the time-kinetic coefficient.]
2. **T3 discriminator — M_MS vs R not mis-assigned.** Confirm omega^2 R^2 = const (box) and
   that omega^2 is depth-independent while M_MS varies. Confirm the sign (omega^2 < 0 =
   relaxation) on an independent SL eigensolver and a finer grid; confirm the negative-q
   region (p>=0.8) genuinely fails to produce a bound (omega^2>0) mode.
3. **S6 — was an approximation smuggled for the full computation?** Confirm C5 (N=600/400,
   80-120 iters) does not change the box-control signature (re-run a point at N=1600/300).
4. **The real-profile E0.** Confirm phi=-a is regular at the core (the log-toy 1/r^2 E0 is
   an artifact, correctly flagged) and that E0<0 over most of the cell on the real soliton.

---

## BLIND VERIFIER — COMPLETE (2026-06-18). Agent: blind-adversarial-verifier (Opus 4.8, 1M ctx).

OVERALL: the OVERALL VERDICT (no native M_MS-tied rest clock; hbar stays an input)
**SURVIVES**, but the result's STATED MECHANISM for it is **WRONG**. The flagged
load-bearing premise (T1(ii) used the C1 dilation weld only) was the right thing to
attack: the FULL L2+L4 matter stress DOES change the on-shell character — it FLIPS the
equation from ELLIPTIC (relaxation, omega^2<0) back to HYPERBOLIC (oscillation,
omega^2>0). The result's central T1/T3 claim ("elliptic on-shell, omega^2<0 at every
depth, relaxation") is FALSE under the full stress. The negative is rescued NOT by the
elliptic/relaxation argument but ONLY by the S3 DISCRIMINATOR: the now-real oscillation
is BOX-CONTROLLED (omega^2 ~ 1/R^2), not M_MS-tied. So the conclusion holds; the
derivation's reasoning to it does not. This is a PARTIAL on the result as written.

Confidence the OVERALL NEGATIVE (no M_MS rest clock) is correct: **0.80**.
Confidence the result's STATED T1/T3 mechanism (elliptic/relaxation) is correct: **0.05**.

### (A) T1 + THE SIGN-FLIP RE-DERIVE — **SURVIVES**
Independently re-derived from scratch (own perturbed-metric construction, no reuse of
build_L). (i) Metric d'Alembertian principal part: cTT/cRR = -e^{4phi}, cTT/cThTh =
-r^2 e^{2phi}, signature (-,+,+), strictly hyperbolic in T. CONFIRMED. (ii) Native H1
EL is ALGEBRAIC: f phi0' H1 = 2 d_t(dphi). CONFIRMED. The KINETIC FLIP is REAL and
convention-INDEPENDENT: eliminating H1 on its algebraic weld reverses the (d_t dphi)^2
coefficient sign RELATIVE to the (d_r dphi)^2 coefficient (ratio after/before = -1
exact). After elimination the time and space kinetic coeffs share the SAME sign in L
=> ELLIPTIC (C1-only). The full on-shell eq matched the stated form EXACTLY (EL+target=0,
i.e. up to the overall EL sign — the result's absolute signs differ from mine by the
+(c/2) vs -(c/2) Lagrangian convention; the physics is the relative sign and agrees).
The flip is NOT an IBP/missing-term artifact. T1 as a C1-ONLY statement is correct.

### (B) THE FULL-L2+L4-STRESS ATTACK — **the result's premise FAILS (the make-or-break)**
The run used the C1 dilation weld; native_weld_status_derivation.py itself states it was
"matter scope (C1 the only content)" with EL_H1 = -r^2 dT_tr and FLAGGED the alternative
"the C1 action is incomplete at perturbed level (the rho-dynamics direction)". I realized
exactly that alternative: put the FULL action C1 + L2 + L4 in one variational problem,
time row g_tr = eps H1 Y on, and derived the FULL algebraic H1 weld.

The static hedgehog n (Theta=Theta(r), no t-dependence) contributes NO time-KINETIC
(d_t dphi)^2 term DIRECTLY (verified = 0: dphi enters the matter action only
algebraically through the metric, never via d_t dphi). BUT the matter DOES contribute an
H1^2 term to the time-row weld, via the determinant sqrt(-g) and the g^{rr},g^{tt}
inverse-metric corrections at O(H1^2). Exact, confirmed THREE independent ways
(direct O(eps^2) action expansion; the gamma - alpha^2/(4 beta) elimination algebra; and
the stress-tensor route delta T_tr = g_tr * L_matter,bg giving beta_matter = (r^2/2)
L_matter,bg):

    beta_matter(H1^2) = -(kappa/(4 r^2) + xi/2)   [EXACT, general theta]

Because matter has NO H1*dpt cross term (alpha_matter = 0) but a NEGATIVE H1^2 term, it
DEEPENS |beta_total| and INCOMPLETELY cancels the C1 flip. The full self-consistent
on-shell time-kinetic coefficient is, EXACTLY:

    coeff[(d_t dphi)^2] = (c r^2 / 2) * N / D,
        N = c r^4 phi0'^2 - (kappa + 2 r^2 xi) e^{4 phi0},
        D = c r^4 phi0'^2 + (kappa + 2 r^2 xi) e^{4 phi0}  (> 0),
    coeff[(d_r dphi)^2] = (c r^2 / 2) e^{-4 phi0}  (> 0).

CHARACTER set by sign(N): N>0 => same sign as spatial => ELLIPTIC (relaxation, the
result's claim); N<0 => opposite => HYPERBOLIC (oscillation). The kappa=xi=0 limit gives
N = c r^4 phi0'^2 > 0 (recovers the result's C1-only elliptic). With matter, N<0 wherever
the matter stress (kappa,xi) dominates the C1 gradient c r^4 phi0'^2 — IN PARTICULAR the
CORE, where regularity forces phi0'->0 while (kappa+2r^2 xi)e^{4phi0} stays finite
positive: N(core) -> -kappa e^{4phi0} < 0 (analytic). On the REAL self-consistent soliton
(radial_Bfree, c=2, xi=kappa=1, kap8=0.05, p=0.4 and 1.0): **N < 0 over the ENTIRE cell
(frac=1.00)**. So the full-stress on-shell breathing equation is HYPERBOLIC everywhere on
the real soliton, and real-frequency (omega^2>0) modes EXIST (correct dispersion: with
T=coeff[d_t^2]<0, modes solve [-(r^2f^2 u')'+q u] = omega^2 (-T) u with positive weight
-T>0 => omega^2>0). VERIFIED numerically: lowest omega^2 = +0.52, +1.96, +4.52, ...

=> The result's "ELLIPTIC, omega^2<0, relaxation, NO oscillation at any depth" is REFUTED
by the full L2+L4 stress. The deepest-prize sub-question "does the full matter stress flip
the character back to hyperbolic?" — answer **YES, it does** (the result's own #1 attack
item, answered against the result).

### (C) BOX-CONTROL / FREQUENCY CLASSIFICATION — **SURVIVES (this is what rescues the negative)**
The now-real oscillation must be classified (S3): M_MS-tied (PRIZE) vs box (dead). Solved
the full-stress generalized EVP and ran the box-control trap TWO ways: (1) profile width
tied to R: omega^2 R^2 = 18.7, 18.8, 18.9, 19.0 (spread 1.4%) while omega^2 ~ 1/R^2
(spread 175%); (2) HONEST trap — FIXED intrinsic profile width wfix=1.0, vary only the
outer box boundary: omega^2 R^2 = 18.5, 19.5, 19.9, 20.1 (spread 8%) while omega^2 ~ 1/R^2
(spread 233%). Both => **BOX-CONTROLLED (omega^2 ~ 1/R^2, omega^2 R^2 ~ const ~ 19-20)**,
NOT M_MS-tied. So the full-stress oscillation, though REAL (not relaxation), is still set
by the CELL SIZE, not the rest energy. The S3 discriminator lands on R (dead) — exactly
as the result concluded, but for the right reason now (box, not relaxation). NOTE: the box
constant ~ -20 in the result's elliptic run and ~ +19-20 here are the SAME magnitude with
flipped sign — consistent with a sign error in the principal part, not a new scale.

### (D) PREMISE AUDIT + RESOLUTION
- The NEGATIVE (no M_MS rest clock) SURVIVES the full L2+L4 stress — but via box-control,
  NOT via the stated elliptic/relaxation mechanism (which is wrong).
- The N=600/400 grid economy (C5) is ADEQUATE for the BOX-CONTROL SIGNATURE (a scaling
  law; reproduced on independent synthetic profiles at n=1500/1600). It is NOT the weak
  point. The weak point was the MODEL (C1-only weld), not the resolution.
- CLEANEST HONEST VERDICT: **NEGATIVE-survives-but-stated-mechanism-refuted.** The
  result should be corrected to: the full-stress on-shell breathing is HYPERBOLIC (real
  oscillation), not elliptic/relaxation; the rest clock is excluded because the
  oscillation is BOX-CONTROLLED (omega^2~1/R^2), not because omega^2<0. T1(ii), T3a (the
  omega^2<0 table), T4 (N/A), and the "elliptic"/"relaxation" language throughout are
  WRONG as stated and must not be banked. The omega^2 R^2 = const box-control conclusion
  and the OVERALL hbar-stays-parked verdict stand.
- WORKSTATION FLAG: my full-stress EVP used representative regular profiles (the slow SCF
  solver timed out on CPU at N=600/120it within this session; the N-sign was confirmed on
  the real soliton at N=300/60it, frac(N<0)=1.00). A full-resolution self-consistent
  soliton + full-stress EVP on the workstation should confirm (i) N<0 cell-wide at
  production resolution and (ii) omega^2~1/R^2 on the REAL profile box-trap, to retire the
  corrected result cleanly.

### SINGLE BIGGEST WEAKNESS (of the result as written)
The result derived the time-row weld from the C1 dilation action ALONE and never coupled
the L2+L4 matter stress into the H1 (time-row) variation — despite that being the
explicitly-flagged make-or-break premise. The matter contributes a real, exact H1^2 term
to the weld that flips the on-shell character from elliptic to hyperbolic. The result got
the right bottom line (no rest clock) for the WRONG reason (it said relaxation; the truth
is box-controlled oscillation). Anyone banking the "elliptic/relaxation/omega^2<0"
intermediate claims would be banking a refuted statement.

VERDICT TABLE: (A) SURVIVES. (B) the result's premise FAILS (full stress flips
elliptic->hyperbolic; oscillation IS restored). (C) SURVIVES (box-controlled). (D)
NEGATIVE-survives-but-stated-mechanism-refuted; workstation confirmation flagged.
Does (B) flip the deepest-prize verdict? It flips the CHARACTER (relaxation -> real
oscillation) but NOT the PRIZE: the oscillation is box-controlled, not M_MS-tied, so
hbar stays parked. NEGATIVE on the prize stands; the result's mechanism does not.

Re-derivation scripts (this verifier, /tmp, not committed): verA.py (sign flip from
scratch), verB2/B3/B4/B6/B7/verfinal.py (full L2+L4 stress, three independent routes),
verB9fast.py (N-sign on the real soliton), verCnum2/verCnum3.py (full-stress EVP +
box-control trap, two ways).
