# Phase-2a Results — Bare Time-Live Whole-Metric Solve (ROTATION / the off-diagonal companion)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = OBSERVE (report what is there;
no result forced). DATA-BLIND (no mass/ratio/wall numbers; sizes in cell-radius R units or
dimensionless ratios). Category-A (GR numerics borrowed for tractability ONLY; no physics,
no matter, no scale imposed). GPU (V100 float64) available and verified; the decisive result
is symbolic (sympy-exact), CPU/GPU parity not load-bearing here. Frame:
time_live_bare_solve_DESIGN.md (DECISIONS-LOCKED + RED-TEAM-REVISIONS) +
phase0_time_live_results.md (Birkhoff bank + B1 ROTATION open question) +
phase1_geon_results.md (the l=2 diagonal geon = OUTCOME B, box-controlled) + CANON
C-2026-06-18-1 (held metric structure) + C-2026-06-10-2 (finite mirrored cell + seal).

Scripts (all NEW, prefix phase2a_; nothing committed changed):
- phase2a_gauge_test.py       -- step 1 GATE: gauge-vs-physical of the found B1 frame-drag (Komar J, Kretschmann, rigid-rotation subtraction)
- phase2a_general_profile.py  -- step 1 (whole): the GENERAL stationary axial-shift vacuum ODE + J on every branch (not just the verifier's one profile)

---

## THE VERDICT: OUTCOME C-rot (the bare vacuum frame-drag is PURE GAUGE). Rotation alone adds nothing.

The Phase-0 B1 open question -- is the off-diagonal g_tpsi frame-drag a genuine bounded
physical rotating mode or a coordinate/gauge relabeling? -- is RESOLVED. The constraint-
satisfying, CORE-REGULAR vacuum frame-drag on the finite mirrored cell is **PURE GAUGE**: it
carries **Komar angular momentum J = 0**, leaves the **Kretschmann curvature invariant
UNCHANGED to all computed orders (O(eps^0), O(eps^1), O(eps^2) all = 0)**, and is exactly the
profile a rigid coordinate rotation psi -> psi - alpha(t) generates. Step 2 (solve the
rotating configuration) and steps 3-4 (J, M, box-control) are therefore SHORT-CIRCUITED:
there is no physical rotating vacuum configuration on the bare core-regular cell to solve for.

**Single most decisive number: the Komar angular momentum of the regular vacuum frame-drag
is J = 0** (exactly; the J-carrying coefficient is the singular 1/r branch's amplitude C1,
and core regularity forces C1 = 0).

This is the rotation-sector analogue of the Phase-0 Birkhoff bank: just as a round vacuum cell
cannot carry mass (Birkhoff), a source-free vacuum interior cannot carry angular momentum
(no Komar J without an enclosed source). It is a clean, structurally-rigorous CLOSURE of the
rotation companion at the bare single-shift order, NOT a solver limitation.

---

## STEP 1 (THE GATE) -- gauge-vs-physical of the frame-drag: PURE GAUGE

### The setup
Phase-0/verifier found that the stationary axial shift g_tpsi = eps*w(r,theta) with the joint
profile **w = r^2 sin^2(theta)** (a linearized-Kerr-like frame-drag) satisfies all O(eps) vacuum
constraints {G_tpsi=0 (elliptic), G_rpsi=0, G_thetapsi=0}. The OPEN question (verifier-flagged,
2026-06-18): is that r^2-growing profile a BOUNDED PHYSICAL rotating mode, or a rotation GAUGE
mode (a coordinate relabeling)?

### Three gauge-invariant tests (phase2a_gauge_test.py, sympy-exact)

**(T1) Rigid-rotation gauge subtraction.** A pure coordinate rotation psi -> psi - alpha(t)
generates, on the flat background, an off-diagonal g_tpsi = alpha'(t) * r^2 sin^2(theta) -- spatial
profile EXACTLY r^2 sin^2(theta). The found profile MATCHES this rigid-rotation gauge profile
identically. Smoking gun (confirmed by T2/T3).

**(T2) Komar angular momentum J (the gauge-invariant conserved charge).** For the general
stationary axial shift, the O(eps) Komar integrand is
    F^{tr} = nabla^t xi^r - nabla^r xi^t = (r * d_r W - 2 W) / r ,   xi = d/dpsi (axial Killing vector).
For the found profile W = r^2 sin^2(theta): r*d_r W - 2 W = r*(2 r sin^2) - 2 r^2 sin^2 = 0,
so **F^{tr} = 0 and Komar J/eps = 0 exactly**. The found mode carries NO real angular momentum.

**(T3) Kretschmann invariant.** For the found profile, R_abcd R^abcd = 0 at O(eps^0) (flat bg),
O(eps^1), AND O(eps^2) -- the frame-drag changes NO curvature invariant. A pure gauge transform
cannot change an invariant; this is consistent with (and corroborates) the gauge verdict.

### Step 1 (whole, not slice) -- the GENERAL profile, not just the verifier's one solution
(phase2a_general_profile.py). To avoid declaring the rotation sector's verdict from one corner,
I solved the FULL O(eps) vacuum equation for the general stationary l=1 (Lense-Thirring) axial
sector g_tpsi = eps * f(r) * sin^2(theta). The vacuum equations give:

    G_tpsi = 0  ->  -r^2 f''/2 + f = 0     (the standard Lense-Thirring frame-drag radial eqn)
    G_rpsi = 0  ->  0 = 0       (no time-derivative constraint; stationary is consistent)
    G_thetapsi = 0 -> 0 = 0

    General solution:  f(r) = C1 / r + C2 * r^2     (two homogeneous branches)

    Komar J/eps as a function of f:  J/eps = r*(2 f - r f')/3   ->   J/eps = C1  (r-INDEPENDENT)

So the conserved Komar angular momentum is carried ENTIRELY by the C1 (1/r) branch:
- **C2 * r^2 branch: REGULAR at the core, J = 0** (= the verifier's profile = rigid-rotation gauge).
- **C1 / r branch: J = C1 != 0** (genuine Lense-Thirring spin), but **SINGULAR at the core r -> 0**.

CROSS-CHECK (textbook): this is exactly the Hartle (1967) slow-rotation vacuum frame-drag basis
{r^2, 1/r}: the r^2 / uniform-omegabar term is rigid frame rotation (gauge, J=0); the 1/r term
(omegabar ~ 1/r^3 falloff) is real Lense-Thirring spin (J!=0) sourced by an enclosed mass. The
category-A numerics reproduce the known GR result identically.

### The closure
On the FINITE MIRRORED CELL with **core regularity** (C-2026-06-10-2; the regularity row of the
DESIGN), the singular C1/r branch is excluded -> C1 = 0 -> **only the regular C2*r^2 (J=0,
pure-gauge) branch survives**. The matter slot is EMPTY, so there is no enclosed source to supply
the central singularity the J-carrying branch requires. Therefore the bare vacuum core-regular
cell carries NO physical angular momentum: **rotation, at the bare single-shift linear order, is
pure gauge.**

---

## STEPS 2-4 -- SHORT-CIRCUITED BY THE STEP-1 GATE (honest, not skipped)

Per the DO instruction ("If it's pure gauge, say so cleanly and stop"), steps 2-4 are not run as
a solve, because there is no physical rotating vacuum configuration on the bare core-regular cell:
- **Step 2 (existence/convergence of the rotating config):** the only core-regular vacuum
  frame-drag is the pure-gauge profile; there is nothing nontrivial to converge to. The nonlinear
  Newton/continuation solve (machinery ready, reused from phase1_geon_solve.py) was NOT run because
  its target object does not exist at this order. (NOT solver-limited: a symbolic NO-object.)
- **Step 3 (J and M):** J = 0 (the decisive charge, computed). M is not separately a rotation
  result -- the bare diagonal mass was already settled in Phase-1 (single bare l=2 mode: net-NEGATIVE
  Misner-Sharp mass). Rotation adds no positive-mass content because it adds no physical content.
- **Step 4 (box-control gate):** moot -- a pure-gauge mode has no physical frequency or charge to
  test for box-control. (For completeness: even the J-carrying singular branch is scale-homogeneous --
  J/eps = C1 with C1 a free amplitude, no intrinsic scale -- so it would NOT escape box-control either.)

---

## VALIDATION (per DO + DESIGN 5.2/5.3)

- **omega -> 0 / J -> 0 recovers Phase-1:** the rotation sector is STATIONARY (the constraint
  G_rpsi = G_thetapsi = 0 = 0 carries no time-derivative); setting the gauge amplitude C2 -> 0
  removes the frame-drag entirely and returns the flat round vacuum background = Phase-1's
  background. With C2 != 0 the geometry is gauge-equivalent to that same flat background (J=0,
  curvature invariants unchanged). Consistent with Phase-0 Birkhoff and Phase-1's flat bg. PASS.
- **Gauge-invariance test for J:** J = C1 is r-INDEPENDENT (the Komar charge is the same on every
  enclosing sphere -- the hallmark of a genuine conserved charge / vacuum solution), and J = 0 for
  the surviving regular profile. The test IS the gauge-invariant diagnostic the DO asked for. PASS.
- **Category-A conditioning:** all symbolic (sympy 1.13.1, exact); the result is a closed-form ODE
  solution f = C1/r + C2 r^2 and an exact integral J/eps = C1, reproduced two ways (direct Komar
  integrand on the found profile -> 0; general radial solve -> J = C1, C1=0 by regularity). Matches
  textbook Hartle. No floating-point floor involved; GPU not load-bearing. PASS.
- **No scale smuggled:** the only quantities are r (the chart radial coordinate), the gauge amplitude
  C2, and the (excluded) source amplitude C1. No xi/kappa, no hidden length, no R_seal dependence in
  the verdict (the verdict is the local J=0, independent of where the seal sits). Data-blind. PASS.

---

## PREMISE LEDGER (chose / derived / leading-order)

| Item | tag | note |
|---|---|---|
| Exponential dilation g_tt=-e^{-2phi}, B=1/A tie (c=1) | DERIVED (C-2026-06-18-1) | held; the rotation sector sits on the flat (m=0) regular background of Phase-1 |
| Vacuum T_munu = 0 (matter slot EMPTY) | CHOSE | the bare-first decision (DESIGN, locked) -- LOAD-BEARING: it is exactly the empty slot that forces C1=0 (no enclosed source for J) |
| Stationary axial shift g_tpsi = eps f(r) sin^2(theta) (l=1 Lense-Thirring sector) | CHOSE + LEADING-ORDER | the rotation/J-carrying angular harmonic; O(eps) single-shift |
| Flat round background for the O(eps) shift | DERIVED (Phase-1) | the bare round static vacuum bg is flat (m=0) by core regularity |
| Core r->0 regularity (excludes the 1/r branch) | DERIVED/forced (C-2026-06-10-2 + DESIGN reg. row) | THE decisive premise: it kills the J-carrying singular branch |
| Komar J = -(1/8pi) oint nabla^a xi^b dS_ab, xi=d/dpsi | DERIVED (standard) | the gauge-invariant conserved-charge definition |
| Single l=1 harmonic, single off-diagonal shift, O(eps) | CHOSE + LEADING-ORDER | the existence/gauge question; higher-l axial + nonlinear NOT opened (see ATTACK) |
| Areal radius (rho = r chart) | CHOSE | chart-independence not separately tested; J is a chart-invariant charge though |

REGIME STAMP: O(eps) LINEAR single off-diagonal axial shift (l=1 Lense-Thirring sector), stationary,
on the flat core-regular finite-cell vacuum background. EXACT (sympy), all-orders-in-eps for the
Kretschmann check, closed-form for the radial ODE and the Komar charge. NOT a nonlinear solve; the
NONLINEAR rotating problem and higher-l / mixed sectors are explicitly left open (ATTACK-HERE).

---

## ATTACK HERE (for a blind verifier)

- **KOMAR NORMALIZATION / SIGN:** recompute J independently (e.g. ADM angular momentum from the
  asymptotic g_tpsi falloff, or the Komar integral with an explicit second convention / xAct).
  Confirm (i) the GENERAL integrand F^{tr} = (r f' - 2 f)/r * sin^2(theta) structure, (ii) J/eps = C1
  is r-INDEPENDENT (genuine charge), (iii) the regular r^2 branch gives J = 0 and the 1/r branch gives
  J != 0. The verdict hinges on J=0 for the regular branch -- if a different normalization makes the
  regular branch carry J!=0, the gauge verdict is wrong.
- **IS THE r^2 BRANCH REALLY GAUGE (not just J=0)?** J=0 is necessary, not obviously sufficient.
  Confirm via the EXPLICIT diffeomorphism: show psi -> psi - alpha(t) with alpha'(t)=const maps flat
  Minkowski to the C2*r^2 frame-drag (T1), i.e. the r^2 profile is generated by a coordinate rotation
  and removed by un-rotating. T3 (Kretschmann unchanged to O(eps^2)) corroborates but a clean
  diffeomorphism exhibit closes it. (The TIME-DEPENDENT version g_tpsi = alpha'(t) r^2 sin^2 is the
  exact coordinate-rotation frame-drag; the stationary C2 case is its constant-alpha' limit.)
- **CORE REGULARITY PREMISE:** the entire closure rests on excluding the 1/r branch by core
  regularity. CHALLENGE: is there a relaxed core condition (the canon phi -> -infinity inside-out
  endpoint, C-2026-06-10-2) under which a J-carrying branch is admissible WITHOUT an external matter
  source? If a regular-at-the-canon-core J-carrying vacuum frame-drag exists, the verdict reopens.
  (Prior: no -- J requires an enclosed source, the matter slot is empty -- but this is the premise to
  attack hardest.)
- **NONLINEAR / O(eps^2):** this is O(eps) single-shift. A NONLINEAR rotating geon (the wave's own
  l>=2 content sourcing an l=1 frame-drag at O(A^2), a la Phase-1's backreaction) was NOT solved. Does
  a finite-amplitude l=2 standing wave generate a net rotational stress that sources a regular-core
  J!=0 frame-drag? (This is the genuine open continuation -- the gauge result here is the LINEAR
  single-mode statement, exactly as Phase-1's box-control was the O(A^2) single-mode statement.)
- **HIGHER-l AXIAL / MIXED-l:** only the l=1 (pure-rotation, J-carrying) axial harmonic was solved.
  Higher-l axial (l>=2 odd-parity / Regge-Wheeler) modes carry no net J but could host odd-parity
  standing waves; not opened here (they are the odd-parity companion of Phase-1's even-parity l=2,
  and like it are expected box-controlled -- but UNTESTED).
- **SCALE SMUGGLE / DATA-BLIND:** confirm no dimensionful quantity beyond the chart r entered; J/eps
  is a pure number (C1) with no intrinsic scale; the verdict (J=0) is R_seal-independent. Confirm.

---

## STATUS

Phase-2a COMPLETE. **OUTCOME C-rot** banked: the bare vacuum frame-drag on the finite core-regular
cell is PURE GAUGE (Komar J = 0, Kretschmann unchanged to O(eps^2), = rigid-rotation relabeling).
The J-carrying Lense-Thirring branch (f ~ 1/r) is singular at the core and requires an enclosed
source the empty matter slot cannot supply -- so rotation, at the bare linear single-shift order,
ADDS NOTHING (no positive mass, no escape from box-control, no physical conserved charge). This is
the rotation-sector twin of Phase-0's Birkhoff bank: a source-free vacuum interior carries neither
mass nor angular momentum.

Combined with Phase-1 (OUTCOME B: the diagonal l=2 geon is box-controlled, net-negative mass), the
BARE time-live whole-metric solve has now found that NEITHER the diagonal standing-wave sector NOR
the rotation/off-diagonal sector yields a physical particle-like object at the explored
(single-mode, O(eps)/O(A^2)) order. Per the DESIGN's orchestra/fallback logic this routes to the
GATED open continuations (NOT to patching): (a) the NONLINEAR rotating geon (l=2 wave sourcing an
l=1 frame-drag at O(A^2)); (b) multi-mode / mixed-l ensembles; (c) the gated NATIVE-matter step
(Einstein saying a mass/angular-momentum background requires an enclosed source = the matter sector
back in). Nothing committed changed. Awaiting Charles.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent a0165d6126d2a9712): STANDS

Independent re-derivation (own sympy Christoffel->Ricci->Einstein, own Komar contraction, own
Riemann->Kretschmann; did not read author scripts). All four load-bearing claims reproduced.
- (a) VACUUM ODE CONFIRMED: independent G_tpsi = eps(-r^2 f'' + 2f) sin^2(th)/(2r^2) => f''=2f/r^2,
  independent dsolve gives f = C1/r + C2 r^2; G_rpsi = G_thetapsi = 0 identically. Exact match.
- (b) KOMAR J CONFIRMED (the central point): independent F^{tr} = eps(r f' - 2f) sin^2(th)/r matches;
  conserved density r(r f' - 2f) = -3C1 (constant, r-independent => genuine charge) for the 1/r
  branch (full-sphere flux ~ -8pi C1 eps != 0), and = 0 for the r^2 branch. The REGULAR (r^2)
  branch carries ZERO angular momentum; the J-carrying (1/r) branch is the singular one. "No regular
  J-carrying vacuum branch the author missed: the ODE is 2nd order, the two-branch basis is complete,
  only r^2 is core-regular." (Verifier's normalization differs by an overall convention constant; the
  r-independence and the zero/nonzero split -- the load-bearing facts -- are normalization-independent.)
- (c) PURE GAUGE CONFIRMED: psi -> psi - Omega*t on flat Minkowski generates g_tpsi = Omega r^2 sin^2(th)
  at linear order = exactly the C2 (r^2) profile (removable by un-rotating).
- (d) TEXTBOOK BASIS CONFIRMED: {r^2 rigid/gauge, 1/r real Lense-Thirring enclosed-spin} matches
  slow-rotation GR.
- KRETSCHMANN CONFIRMED with a precision note: for f=r^2 exactly K = 4eps^4(...)/(...)^4; O(eps^0),
  O(eps^1), O(eps^2) all identically zero (corroborates gauge at the linear scope). K is nonzero only
  at O(eps^4) -- EXPECTED, because eps f sin^2 added to a FIXED flat g_tt is the linearized rotation
  piece, not the full rotation diffeo (which would also add Omega^2 r^2 sin^2 dt^2). At the stated
  linear scope, curvature is unchanged. (Not a defect.)
- NET: "bare time-live vacuum rotation on a core-regular finite empty cell is pure gauge and carries
  no physical angular momentum -- sound. No errors found."

## DRIVER-LEVEL BLIND VERIFIER — 2026-06-18 (agent a80a2ba1293f453ef): STANDS
Independent re-derivation (own Einstein tensor + Komar). (a) G_tphi=eps(-r^2 f''+2f)sin^2/(2r^2), G_rphi=G_thphi=0 => f''=2f/r^2 => f=C1/r+C2 r^2 (exact match). (b) Komar flux ∝ r(2f-r f')/3, r-independent. (c) C2 r^2 branch: flux=0 (J=0), explicitly = psi->psi-Omega t on flat Minkowski (pure gauge); C1/r branch: flux=4pi C1 eps, singular at core. (d) regularity excludes 1/r => C1=0 => J=0. Rotation-sector Birkhoff analogue holds. SCOPE: O(eps) linear stationary l=1 axial; structural Komar/Birkhoff core EXACT; nonlinear O(A^2) rotating geon + higher-l axial OPEN. No errors.
