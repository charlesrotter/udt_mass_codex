# Off-Diagonal Angular Row II — BLIND ADVERSARIAL VERIFIER RESULTS

Status: independent hostile blind verifier pass on offdiagII_results.md.
NOT canonical (Charles canonizes). Append-only. New file.
Verifier: Claude (Opus 4.8, 1M), agent id `offdiagII-verify-2-2026-06-13`.
Date: 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md.
Independent machinery: my OWN sympy metric build + Schur, my OWN conforming
continuous-P1 FEM and a global spectral sine-Galerkin operator (NOT a re-run
of the challenger's offdiagII_* scripts). Log /tmp/offdiagII_verify.log.
Template discipline: the verdict is the SIGN/boundedness CHARACTER of the
operator (does a non-round type exist / is the static problem well-posed),
NOT a mode count or masses. No wall numbers loaded.

================================================================
## VERDICT: CONFIRMED (unbounded below / static C1 truncation incomplete).

The challenger's "third outcome" survives both decisive kill-shots and two
fairness checks, established with fully independent machinery. The static
single-cell C1 off-diagonal angular operator, with q slaved on the metric's
own EL and w=0, is UNBOUNDED BELOW wherever the on-shell attractive flip
(K_th<0) lives. It is NEITHER "round only" NOR "shaped type supported": there
is no finite, refinement-stable negative ground state, in ANY function space.
The static class is incomplete exactly where the flip turns on; completion is
handed to the w/seal/nonstationary sector.

Decided by: KILL-SHOT 1 (conforming-space reposing) is the load-bearing one —
it is the single test that could have flipped the verdict to
"shaped-type-supported", and it did not. KILL-SHOT 2 independently removes the
"prescription artifact" escape. Kill-shots 3 and 4 confirm fairness and fix
the physical reading.

================================================================
## ANCHOR (reproduced with independent sympy, before any eigenvalue trusted)

My own metric build (g with q=g_rth, w=0), own Schur K_th=(Hpp-Hpq^2/Hqq)/W:
  phi=0.5, r=0.5, pr=8, pth=0.5, theta=1.0:
    q* = 0.27618,  |q*|/bound = 0.3350,  Hqq = 3.7915 > 0 (genuine min)
    K_r = +0.2782 (>0),  K_th = -2.03257   (challenger anchor -2.0326)
  MATCH to <2e-3. The on-shell flip the prior verifier established is
  reproduced exactly by an independent derivation.

K_th<0 is EXTENDED and equator-peaked, and STRENGTHENS toward/past the seal
(independent map, r=0.6 wall, mild lobe):
    phi=+0.5 -> min K_th -0.78 ;  phi=0 -> -5.03 ;  phi=-1 -> -40.8 ;
    phi=-2 -> -303.   25/25 theta-points negative; min always at equator.
K_r stays STRICTLY POSITIVE on the seal side (0.27, 2.0, 109, 5962 for
phi=0.5,0,-1,-2): the pathology is in the angular channel only; the operator
is singly, not doubly, ill-posed (the challenger's K_r claim CONFIRMED).

================================================================
## KILL-SHOT 1 — CONFORMING SPACE (the decisive one). RESULT: does NOT flip.

The challenger's negative eigenvector is a checkerboard grid mode — the
FD hallmark. The test: re-pose the SAME on-shell operator in spaces where
checkerboard/grid modes CANNOT exist. If a finite refinement-stable negative
ground state survives, the verdict FLIPS to "shaped type supported." Two
independent conforming discretizations, both built from scratch:

(1A) CONTINUOUS P1 FEM (C0-conforming, 2x2 Gauss element integrals, true
     Galerkin mass+stiffness — no checkerboard null space):
       formed cell shift=0 :  lam0 = -253, -709, -1420, -2397  (Nth 15->39)
       shift=-1            :  lam0 = -2035, -5403, -10600, -17736
     lam0 -> -inf as the grid refines (lam0*dth^2 stays O(1), drifting only
     because the K_th<0 region deepens/grows with resolution). NO finite limit.

(1B) GLOBAL SPECTRAL sine-Galerkin (infinitely-smooth modes, no grid at all),
     equatorial wall slice, increasing polynomial degree Nmode 8->64:
       shift=0  on-shell:  -15.7, -70.3, -161, -288, -649, -1154   (~ -Nmode^2)
       shift=-1 on-shell:  -796, -3202, -7197, -12778, -28699, -50964
       CONTROL (K_th forced +): converges cleanly to +2.50 / +8.5 (FINITE).

The unboundedness reproduces in BOTH conforming spaces and scales as the
textbook backward-heat signature (lam0 ~ -1/dth^2 in h-refinement, ~ -Nmode^2
in p-refinement). The checkerboard in the challenger's FD scheme was
incidental; the divergence is a REAL property of the continuous operator
(K_th<0 over an extended region => the bilinear form INT K_th u_th^2 W is
genuinely unbounded below by high-frequency SMOOTH functions too). The clean
finite-positive control in the same smooth basis proves the tool is sound.
=> NO finite shaped type exists. Kill-shot 1 does NOT flip the verdict.

================================================================
## KILL-SHOT 2 — IS w=0-WITH-q-SLAVED A PRESCRIPTION ARTIFACT? RESULT: NO.

Independent metric build carrying BOTH q=g_rth and w=g_tth, with a time
gradient pt so the w-channel is active. Findings:
  - dL/dw=0 has NO solution for pt!=0 (sympy solve -> []; dL/dw monotone): w
    is a genuine runaway in the dynamical sector (prior verifier CONFIRMED).
  - BUT in the STATIC sector (pt=0, no time gradient — the actual scope of
    this gate) L is EVEN in w with a genuine MINIMUM at w=0: L_ww(+FD) =
    +16.18 > 0; L(w) sample symmetric, minimized at w=0; the joint 2D Newton
    for (q,w) stationarity lands at w=0 EXACTLY (residual 1e-16). So w=0 is
    NOT an arbitrary freeze — it is the static stationary point.
  - At w=0 the off-diagonal Hessian H_{qw} is DIAGONAL: L_pw = L_qw = 0
    exactly. Therefore the consistent JOINT (q,w) 2x2 Schur complement equals
    the q-only Schur EXACTLY: K_th_joint = K_th_qonly = -2.03256.
  - (Away from w=0, L_pw,L_qw are nonzero; the decoupling is specifically at
    the static stationary point, which is where the reduction is taken.)

So eliminating q AND w consistently does NOT restore ellipticity: K_th stays
-2.033. The wrong-sign coefficient is INTRINSIC to the static metric, not a
manufactured product of an inconsistent partial elimination.
=> Kill-shot 2 does NOT flip the verdict (no prescription artifact).

================================================================
## KILL-SHOT 3 — CONTROL FAIRNESS + BACKGROUND VALIDITY. RESULT: fair / robust.

(a) Control isolation: the flip-off control replaces K_th by the bare diagonal
    e^{-2phi}/r^2 (the q-Schur-correction removed) — the correct "round-only"
    reference. It is finite-positive (1.02, 2.78, 20.5 for phi=0.5,0,-1); the
    Schur correction (-1.80, -7.81, -61.4) is exactly what drives it negative.
    Turning ONLY the on-shell q-Schur on flips the sign. Control is fair.

(b) Background validity — the STRONGEST independent finding: the flip is NOT
    an artifact of the ansatz's angular lobe. At pth=0 EXACTLY (purely radial
    background, q*=0) K_th is already -5.03; sweeping pth 0 -> -0.3 barely
    moves it (-5.031 -> -5.052). The negativity is driven by the RADIAL
    gradient pr through Hpq=d2L/dpth dq (nonzero whenever pr!=0), not by
    phi_th. Re-running my conforming FEM on a PURELY RADIAL background (no
    lobe) gives essentially identical divergence (lam0 -253 vs -253, -2408 vs
    -2397). The result is robust to using a trivially-valid radial background,
    so it is not an artifact of the formed-cell ansatz not solving the EL.

(c) Independent T2 (vanishing PSD higher-gradient regularizer) in my conforming
    FEM: lam0 monotone 0.94 -> -40.7 -> -875 -> -1362 -> -1419 (eps 1e-1->0),
    no finite limit — reproduces the challenger's T2 independently.
=> Kill-shot 3 does NOT flip the verdict.

================================================================
## KILL-SHOT 4 — PHYSICAL READING. "Incomplete static class" vs "unstable bg".

"Unbounded below" admits two readings: (i) the static C1 truncation is
INCOMPLETE (a regularizing w/seal/boundary/nonstationary term is missing) —
the challenger's reading; or (ii) the formed cell is genuinely DYNAMICALLY
UNSTABLE / the wrong background. The evidence favors (i):
  - The divergence is in the ANGULAR second-derivative coefficient only
    (K_r>0, K_th<0); a true dynamical instability of the round cell would be
    a finite-wavelength negative mode with a finite growth rate, not a
    high-frequency-divergent (no-lowest-eigenvalue) spectrum. An operator with
    NO lowest eigenvalue is not a physical instability — it is a missing
    higher-gradient (ellipticity-restoring) term: the textbook signature of a
    truncated/incomplete action, not of a saturating instability.
  - w is a runaway in the dynamical sector with no static kinetic term, and
    the seal/area-form (#36) and the now-propagating nonstationary sector
    (CANON C-2026-06-13-1) are precisely the channels that can supply the
    missing regularizer. The missing instrument is the w/boundary/nonstationary
    one (orchestra principle 5): a solo static-cell probe cannot see it.
  - Charter principle 2 honored throughout: every coefficient is the exact
    nonlinear on-shell value (depth e^{-2phi} up to ~6000 at phi=-2 carried).
=> Reading (i) is correct: static class incomplete, completion outside scope.

================================================================
## SURVIVING STATEMENT (exactly what is true)

On a formed cell (radial-dominant wall; robust to angular content), with q
slaved on the metric's own static EL and w=0 (the static stationary point),
the on-shell C1 angular Schur coefficient K_th goes NEGATIVE over an extended,
equator-peaked, seal-strengthening region (driven by the radial gradient via
the q-channel). The resulting static angular operator is UNBOUNDED BELOW
there — confirmed basis-independently (FD checkerboard, conforming continuous
P1 FEM, AND global spectral Galerkin all diverge; the K_th-positive control
converges finite). There is NO finite refinement-stable negative ground state,
so NO shaped type is established; and the operator is NOT sign-definite, so
"round only" is refuted as a complete static statement. The static single-cell
C1 truncation is INCOMPLETE exactly where the flip turns on.

================================================================
## SCOPE / PREMISE SET (for NEGATIVES_REGISTRY)

Background: static, single-cell, C1-dilation. Source: matter potential
-Phi(.5 e^{-2phi}+e^phi), V=Phi(2e^{-2phi}+e^phi)>0. BCs: Dirichlet-type
angular endpoints. Reduction: q slaved on dL0/dq=0 (its own EL), w=0 (the
static stationary point; runaway only in the dynamical pt!=0 sector). Region:
phi in [-2,+3], radial-dominance 13-50x, m=0,1,2, ell=2,3. NOT reached: deep
core phi->-inf; dynamical w; nonstationary backgrounds — exactly where the
missing regularizer could live. If the w/seal/nonstationary completion is
later supplied, this "no shaped type within static C1" loses blocking
authority and must be re-graded.

================================================================
## WHAT IT MEANS FOR THE OFF-DIAGONAL FRONTIER

The off-diagonal angular row is NOT closed and does NOT yield a type within the
static class. It is HANDED to the w/seal/nonstationary completion. The static
result is a load-bearing diagnostic: it PROVES the static single-cell C1
truncation is incomplete (the missing instrument is real and necessary), and
it localizes where the next gate must be posed — the regularizing term lives
in the w-direction / the seal area-form (#36) / the nonstationary weld sector
(CANON C-2026-06-13-1). Whether a finite shaped type exists once that term is
supplied is the next gate and is genuinely open.

================================================================
## FILES (this verifier; immutable)
- /tmp/v1_kth_independent.py — independent metric build, Schur, anchor, K_th
  map, K_r positivity.
- /tmp/v2_conforming.py — independent conforming continuous-P1 FEM (kill-shot 1A,
  + radial-background and T2 checks).
- /tmp/v3_spectral.py — independent global spectral sine-Galerkin (kill-shot 1B),
  on-shell divergence + finite control.
- /tmp/v4_joint_qw.py — independent joint (q,w) Schur / w-runaway / static
  w-minimum (kill-shot 2).
Log: /tmp/offdiagII_verify.log.
