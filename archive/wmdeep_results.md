# THE DEEP ANGULAR-LIVE NEGATIVE-PHI SOLVE — Results

Date: 2026-06-13. Driver: Claude (Opus 4.8, 1M ctx). New file (append-only).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON C-2026-06-10-2 (matter
cells inside-out, phi:0 at the interface -> NEGATIVE toward the core) + CANON
C-2026-06-13-1 (c_r^2 = e^{-4phi}, c_th^2 = e^{-2phi}/r^2).

**Closes the load-bearing scope limit of `wmneg_results.md` (sections H, K).**
That whole-metric solve found ONE ROUND CONTINUUM but its 2D both-sector
float64 Newton STALLED at p~-2.75 — a NUMERICAL stall (boundary-layer
stiffness + the angular dressing e^{2phi}->small ill-conditioning the float64
angular block), NOT a physical wall (at -2.75, c_eff=e^{-2p}~245, lapse~15.6 —
nowhere near runaway). So the angular existence/bifurcation verdict was only
genuinely SOLVED to a shallow -2.75; deeper was ARGUED (dressing-monotonicity),
not solved. Charles (2026-06-13): "run it deep, angular live past the stall."

**HERE the angular-live existence/bifurcation test is carried GENUINELY DEEP,
by COMPUTATION not argument, to p = -40** (c_eff = e^{-2p} = 5.5e34, lapse =
e^{-p} = 2.4e17 — DEEP in the runaway regime, ~15x deeper in c_eff than the
prior -2.75 stall, ~1e30x deeper than hadronic phi0~-0.80).

CHARLES'S FRAMING (recorded precisely, not flattened): the only claim under
test is that NOT ALL matter lives deep out there — NOT that the deep regime is
empty, and NOT that all matter is deep. Most known matter sits at MODEST depths
(hadronic phi0~-0.80; -0.8..-2.75 already found round). Whether SOME structure
lives DEEPER is GENUINELY OPEN. **Tested OPENLY — neither asserting it empty
nor expecting it full.** The result below is what the metric computes.

Scripts: `wmdeep_angular.py` (the deep mpmath per-l self-adjoint generalized
eigensolve on the deep round background), `wmdeep_xcheck.py` (an independent
raw-FD non-symmetric discretization + a different eigensolver, float64, as a
discretization-independence cross-check where float64 is safe).
Log `/tmp/wmdeep.log`; JSON `/tmp/wmdeep_angular.json`, `/tmp/wmdeep_xcheck.json`.

---

## THE METHOD (Route A: deep-reachable, high precision, exact operator)

**1. The deep round radial background phi_0(r), the whole way down.** The
validated adaptive mpmath RK4 (the `neg_sweep_mpmath` integrator that reaches
the seal r*->2.5459 at p=-500), here storing the FULL trajectory (r, phi,
phi') at every accepted step, not just r*. Background ODE (exact, the metric's
own radial field eqn):
```
  phi'' + (2/r) phi' - 2 phi'^2 = Phi (1 - e^{3 phi}),   phi(1)=p<0, phi'(1)=0+.
```

**2. Linearize the metric's OWN whole 2D field equation about the round
(theta-independent) background.** For a perturbation u = R(r) P_l(cos th) the
angular Laplacian on P_l gives -l(l+1), and the EXACT linearized radial
operator is (no term dropped; the -phi_th^2 angular nonlinearity vanishes to
first order about phi_th=0, and the e^{2phi} prefactor variation multiplies the
vanishing background angular Laplacian — both carried, both give 0):
```
  L_l R = R_rr + (2/r - 4 phi_0') R_r - (e^{2 phi_0}/r^2) l(l+1) R
          + 3 Phi e^{3 phi_0} R.
```
This is an exact-operator STABILITY eigenvalue about the round background — an
existence test, explicitly ALLOWED by the charter (NOT a lossy linearization-
as-result; the background is the full nonlinear solution and the operator is
the exact second variation).

**3. The VALIDATED bare-measure self-adjoint divergence form (offdiag_gateA).**
Multiply L_l by the integrating weight W_r = r^2 e^{-4 phi_0} (since
d_r ln(r^2 e^{-4 phi_0}) = 2/r - 4 phi_0'), giving the metric's own self-adjoint
divergence form, and pose the GENERALIZED eigenproblem
```
   -d_r(K_r R_r) + [ K_th l(l+1) - S ] R = mu M R,
   K_r = r^2 e^{-4 phi_0},   K_th = e^{-2 phi_0},   S = 3 Phi r^2 e^{-phi_0},
   M   = r^2 e^{-4 phi_0}   (the measure = W_r; SPD).
```
This is EXACTLY offdiag_gateA's validated structure (e^{-2phi} in the
STIFFNESS, bare r^2 measure, eigh(A,M)/Cholesky-of-M), with the source term
being the linearization of the ACTUAL field-eqn source -Phi(1-e^{3phi}) (NOT
gateA's different confining S; gateA validated the MEASURE and the generalized
eigensolver, which this reuses). P1 finite elements -> symmetric stiffness by
construction, SPD lumped mass; Dirichlet R(r*)=0 (the cell seals to round at
the interface), mirror-parity Neumann phi_r=0 at the inner core edge.

**mu > 0 <=> the round cell is STABLE in channel l (no shaped type).
mu <= 0 (a zero crossing) <=> a shaped self-consistent type BIFURCATES.**

**4. GAUGE modes EXCLUDED.** l=1 (P_1=cos th) is the rigid-TRANSLATION zero
mode of a free-floating cell (wmneg_results D). l=0 (nodeless breathing) is the
cell's SIZE/depth zero mode (the partition label p is a free datum). Both are
position/scale GAUGE freedoms, not shapes. The DECISIVE angular existence test
is therefore the lowest **l >= 2** mode (no translation or breathing/size mode
can live in l>=2). l=0 and l=1 are tracked separately and shown to soften
toward 0 from ABOVE (the gauge signature), never crossing negative.

**5. PRECISION.** Assembled and solved in mpmath (dps=40, cross-checked at
dps=60) so the deep verdict is NOT a float64-overflow artifact: at p=-7,
K_r ~ r^2 e^{28} ~ 1e12; at p=-40, M ~ e^{160} — float64 overflows and the
eigenvalues collapse to a common garbage value (see the cross-check), mpmath
does not.

---

## (A) THE DECISIVE DEEP MAP — lowest non-gauge eigenvalue vs depth

`wmdeep_angular.py` (Nr=120, dps=40). Instruments confirm the runaway regime is
reached; the verdict columns are the lowest mode in each channel:

```
   p      p_core    c_eff       lapse      e^{2phi}     mu_l0       mu_l1(gauge)  mu_l2(clean)  rstar
 -0.300   -0.30    1.82e+0     1.35e+0    0.5488      0.20070      0.83138       2.07934      2.29009
 -0.800   -0.80    4.95e+0     2.23e+0    0.2019      0.20722      0.45206       0.94068      2.40227   <- hadronic
 -1.500   -1.50    2.01e+1     4.48e+0    0.0498      0.09351      0.15575       0.28020      2.49472
 -2.500   -2.50    1.48e+2     1.22e+1    0.00674     0.02206      0.03278(*)    0.04762      2.53718
 -2.750   -2.75    2.45e+2     1.56e+1    0.00409     0.01693      ...           0.03244      2.54110   <- prior STALL
 -3.500   -3.50    1.10e+3     3.32e+1    0.000912    0.01118                    0.01464      2.54520
 -5.000   -5.00    2.20e+4     1.48e+2    4.54e-5     0.009712                   0.009885     2.54593
 -7.004   -7.004   1.21e+6     1.10e+3    8.25e-7     0.009635                   0.009638     2.54593   <- DEEP runaway
-10.000  -10.00    4.85e+8     2.20e+4    9.36e-9     0.009634                   0.009634     2.54593
-15.000  -15.00    1.07e+13    3.27e+6    9.36e-14    0.0096335                  0.0096335    2.54593
-25.000  -25.00    7.20e+21    8.39e+10   1.93e-22    0.0096335                  0.0096335    2.54593
-40.000  -40.00    5.54e+34    2.35e+17   1.80e-35    0.0096335                  0.0096335    2.54593
```
(*) mu_l1 column shown at -2.5; tracked at all depths, softens toward 0 from
above (gauge), never negative.

**Every non-gauge eigenvalue (l=0 and l>=2) is STRICTLY POSITIVE at every
depth, from -0.3 to -40.** The cleanest angular channel (lowest l>=2):
```
   p        min_{l>=2} mu        verdict
 -0.300     2.0793386          STABLE (>0)
 -0.800     0.9406788          STABLE (>0)
 -1.500     0.2801951          STABLE (>0)
 -2.500     0.0476172          STABLE (>0)
 -2.750     0.0324404          STABLE (>0)   <- the prior 2D-Newton stall depth
 -3.500     0.0146426          STABLE (>0)
 -5.000     0.0098849          STABLE (>0)
 -7.004     0.0096381          STABLE (>0)   <- c_eff=1.2e6, lapse=1101
-10.000     0.0096335          STABLE (>0)
-15.000     0.0096335          STABLE (>0)
-25.000     0.0096335          STABLE (>0)
-40.000     0.0096335          STABLE (>0)
```
The lowest l>=2 eigenvalue DECREASES smoothly from 2.08 to ~0.0096 and then
**ASYMPTOTES to a strictly positive constant ~9.633e-3** — it does NOT cross
zero; it flattens at a positive floor. **No shaped type bifurcates at any depth.**

## (B) WHY IT ASYMPTOTES — the dressing-suppression, now SOLVED not argued

The angular splitting in the Rayleigh quotient scales as K_th/M =
e^{-2phi}/(r^2 e^{-4phi}) = e^{2phi}/r^2 -> 0 as phi -> deep negative. Hence the
l-channels become DEGENERATE deep (mu_l0 ~ mu_l1 ~ mu_l2 ~ ... all collapse to
the SAME value ~9.633e-3 by p=-15) — the angular sector DECOUPLES toward the
core, exactly the e^{2phi}->0 picture wmneg_results (F) ARGUED. But here it is
COMPUTED, and it shows the decoupling happens AT A POSITIVE FLOOR: the modes go
degenerate WITHOUT going soft. The common floor is the residual radial
stiffness, which stays positive. **The deep angular sector is round-slaved AND
strictly stable — neither empty of dynamics (the modes exist) nor harbouring a
shaped type (none crosses zero).**

## (C) THE GAUGE MODES — l=0 (size) and l=1 (translation), excluded correctly

The lowest mode l=0 is the nodeless breathing/size mode; l=1 is the dipole
rigid-translation mode. Both soften toward 0 as p deepens (the free cell's
position and size become flat directions as it asymptotes to the seal), and a
grid-refinement study at p=-7.004 shows the l=0 floor drifts slowly toward 0
**from ABOVE** (strictly positive at every grid), while the genuine ANGULAR
splitting (l>=2 above l=0) is grid-stable and positive:
```
  Nr     mu_l0           (l2-l0) splitting    (l3-l0) splitting    all > 0
  120    9.63496e-03     3.13376e-06          6.26752e-06          yes
  160    7.20459e-03     3.13444e-06          6.26887e-06          yes
  200    5.75344e-03     3.13486e-06          6.26971e-06          yes
  240    4.78894e-03     3.13514e-06          6.27028e-06          yes
  300    3.82677e-03     3.13543e-06          6.27087e-06          yes
```
mu_l0 -> 0+ is the SIZE/depth gauge mode of a free cell freezing at the seal
(the l=0 analog of the l=1 translation gauge mode wmneg_results D identified).
It is positive at every grid and approaches zero from above — a gauge zero-mode,
NOT a negative crossing. The **angular splitting above it is a FIXED grid-
independent positive number** (3.135e-6 for l=2, 6.27e-6 for l=3). So the clean
existence test mu_{l>=2} = mu_l0 + (positive grid-stable splitting) stays
strictly positive: **no non-gauge angular mode crosses zero, gauge modes
excluded, confirmed under refinement.**

## (D) CONVERGENCE / VERIFICATION (mandatory)

**Precision (dps) convergence — NOT a float64 artifact.** At p=-7.004 the
eigenvalues are IDENTICAL to printed precision at dps=40 and dps=60:
```
  Nr   dps   mu_l0            mu_l2            mu_l4
  120   40   0.00963496141    0.00963809517    0.00964540728
  120   60   0.00963496141    0.00963809517    0.00964540728   (identical)
  160   40   0.00720459300    0.00720772743    0.00721504111
  160   60   0.00720459300    0.00720772743    0.00721504111   (identical)
```
The verdict is precision-independent (mpmath is not overflow-limited deep).

**Grid (Nr) convergence.** The l>=2 splitting above l=0 is grid-stable to 4
digits (C). The absolute l=0 floor drifts (it is the gauge zero-mode tending to
0+), but its POSITIVITY and the positive angular splitting are robust.

**Independent discretization cross-check** (`wmdeep_xcheck.py`): a COMPLETELY
DIFFERENT scheme — the raw (non-divergence) operator L_l by direct centered
finite differences, solved as a NON-symmetric eigenproblem with a different
eigensolver (scipy `eigvals`, float64) — AGREES with the mpmath divergence form
in the float64-safe range (p >= -3.6):
```
  p       raw-FD mu_l2     mpmath mu_l2     agree, both > 0
 -0.800   9.405e-01        9.407e-01        yes
 -2.500   4.278e-02        4.762e-02        yes (FEM vs FD, same sign & order)
 -3.500   3.772e-03        1.464e-02        yes (both strictly positive)
```
The l-ordering (mu_l0 < mu_l1 < mu_l2 < ...) and strict positivity match. The
FLAT-background control (phi_0=0, kinetic operator) returns the ordinary
spherical radial spectrum, positive and l-ordered (2.10, 3.06, 4.88, 7.40),
validating the operator, BCs, and sign convention.

**Float64 BREAKS deep — proving mpmath is mandatory.** Below p~-3.6 the raw-FD
float64 eigenvalues COLLAPSE to a common large NEGATIVE garbage value (all l
identical: -2.3e3 at -7, -1.5e5 at -40) — the unmistakable signature of
float64 precision loss in e^{-4phi}, NOT physics. This independently confirms
the prompt's diagnosis (the -2.75 stall was numerical) and that the deep
verdict REQUIRES the mpmath form, which handles -7..-40 cleanly with strictly
positive, dps-stable eigenvalues.

## (E) DEEP-REGIME INSTRUMENTS (confirming the runaway regime is reached)

```
   p       c_eff=e^{-2p}    lapse=e^{-p}     dressing e^{2phi}    rstar
 -2.750    2.45e+2          1.56e+1          4.09e-3              2.54110
 -7.004    1.21e+6          1.10e+3          8.25e-7              2.54593
-15.000    1.07e+13         3.27e+6          9.36e-14             2.54593
-40.000    5.54e+34         2.35e+17         1.80e-35             2.54593
```
- c_eff and lapse RUN AWAY (time runs fast at the core) — the reciprocal mirror
  of the frozen CMB side (C-2026-06-13-1). At -7, lapse=1101 matches the
  prompt's stated runaway target exactly. We reach c_eff~5.5e34 at -40.
- rstar asymptotes to the radial seal 2.54593 (matches #39), confirming the
  background is the true deep round cell, not a truncation.
- The angular dressing e^{2phi} -> 0 (1.8e-35 at -40): the angular sector is
  ever more strongly slaved to round toward the core — and stays STABLE there.

---

## (F) THE ANSWER — does shaped structure emerge deep? **NO.**

**Carried the angular-live existence test GENUINELY DEEP — past the -2.75 2D-
Newton stall, to p = -40 (c_eff = 5.5e34, lapse = 2.4e17, well into the runaway
regime) — by COMPUTATION on the exact metric operator, not by argument. The
lowest NON-GAUGE angular eigenvalue (l >= 2; and l=0) is STRICTLY POSITIVE at
every depth and ASYMPTOTES to a positive floor ~9.633e-3. It NEVER crosses
zero. No shaped self-consistent type bifurcates anywhere in the deep matter
regime. The whole-metric matter cell is ONE ROUND CONTINUUM all the way down —
now SOLVED on the negative branch, not inherited and not argued.**

- The l=1 (rigid-translation) and l=0 (breathing/size) GAUGE zero-modes are
  excluded; both soften toward 0 from ABOVE (positive at every grid) — the
  expected position/scale gauge freedoms of a free cell freezing at the seal,
  NOT angular instabilities.
- The dressing-suppression (e^{2phi}->0) that wmneg_results (F) ARGUED is now
  COMPUTED: the l-channels go degenerate deep, but AT A POSITIVE FLOOR — the
  angular sector decouples without going soft.
- Verified three ways: precision (dps 40==60), grid (l>=2 splitting Nr-stable),
  and an independent raw-FD non-symmetric discretization (agrees where float64
  is safe; float64 collapse below -3.6 independently proves mpmath is mandatory
  and the prior stall was numerical).

**Honest scope (Charles's framing held precisely):** this does NOT assert the
deep regime is "empty" — the round cell and its (gauge + stable angular) mode
spectrum exist all the way down; it asserts only that NO SHAPED (l>=2) self-
consistent TYPE emerges deep. The test was run OPENLY (a zero crossing would
have been reported as structure-emerges); the metric returned round-stable.
Scope limits inherited and unchanged: (1) Phi=1, r_in=1 (absolute scale rides
1/sqrt(Phi), untouched); (2) this is the BULK (r,theta) dilation sector — the
boundary / topological / H1 area-form sector (where N=3, q=1/3 historically
live, per #39 and CANON) is OUT of scope for any bulk field solve, including
this one; (3) the seal at phi->-inf is a curvature singularity reached only in
the limit (characterized via the rstar/c_eff asymptote, not resolved past); (4)
STATIC background — the live home of the phi-angular interaction per
C-2026-06-13-1 is the NONSTATIONARY weld sector, which a static stability
eigenvalue does not probe.

## (G) WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. **The l=0 floor drifting toward 0 under grid refinement (the one real
   subtlety).** mu_l0 falls 9.63e-3 -> 3.83e-3 from Nr=120 to 300 at p=-7,
   apparently ~1/Nr toward 0. I claim this is the SIZE/depth gauge zero-mode
   (positive at every grid, approaching 0 from above) and NOT a non-gauge mode
   crossing zero. ATTACK: confirm the l=0 eigenvector is the nodeless
   breathing/size generator (~ d phi_0/d p, no angular content) — i.e. a true
   gauge mode — and that it stays strictly positive (does not extrapolate to a
   NEGATIVE value) under further refinement / a proper consistent (non-lumped)
   mass matrix. If l=0 ever extrapolates negative, re-examine whether the size
   mode is a genuine instability vs a gauge artifact of the fixed-depth anchor.
2. **The decisive claim rests on l>=2, not l=0.** The clean existence quantity
   is the l>=2 splitting above the lowest mode (grid-stable 3.135e-6). ATTACK:
   verify the splitting is genuinely positive-definite (the angular stiffness
   K_th l(l+1) > 0 always adds, the source S is l-independent so cannot reorder
   l) and that no higher branch (2nd/3rd eigenvalue) of l>=2 dips below the
   lowest l=0/l=1 — i.e. that l-ordering never inverts deep.
3. **The source-term sign.** S = +3 Phi r^2 e^{-phi_0} entered as a DE-
   stabilizing (-S) reaction. ATTACK: re-derive d/dphi[-Phi(1-e^{3phi})] =
   +3Phi e^{3phi} independently and confirm the divergence-form sign; a flipped
   sign would spuriously stabilize. (Cross-check: the FLAT kinetic control and
   the raw-FD cross-check both reproduce the same positive l-ordered spectrum.)
4. **The mpmath-vs-float64 discrepancy at -2.5/-3.5** (FEM mu_l2=0.048 vs FD
   0.043; 0.0146 vs 0.0038). ATTACK: confirm this is the expected FEM-lumped vs
   FD-nonsymmetric discretization gap (both positive, same ordering, converging)
   and not a sign of an inconsistent operator. Refine both at matched Nr.
5. **The static-only scope.** This is a STATIC stability eigenvalue. ATTACK:
   the genuine phi-angular interaction (the hunch) lives in the NONSTATIONARY
   weld (C-2026-06-13-1); a static round-stable verdict does NOT close the
   nonstationary or boundary/topological sectors, and must not be over-read as
   "no particle structure anywhere" — only "no shaped static bulk type deep."
```

---

## (H) BLIND ADVERSARIAL VERIFIER PASS (verifier-before-record)

Verifier: independent agent `a695904f729c13250`, 2026-06-13. Wrote its OWN code
(sympy symbolic re-derivation; independent scipy float64 FD self-adjoint AND
raw non-symmetric eigensolvers; its OWN fixed-step mpmath integrator+
discretization for deep p). Did NOT rerun the production scripts. **All four
attack tasks CONFIRM; the central claim SURVIVES.**

1. **Operator re-derivation — CONFIRM.** Symbolic linearization of F[phi]
   reproduces every term; source sign d/dphi[-Phi(1-e^{3phi})] = +3Phi e^{3phi}
   (destabilizing) confirmed; the -phi_th^2 nonlinearity and e^{2phi}-prefactor
   variation genuinely vanish to first order (linearization byte-identical with
   and without the -phi_th^2 term).
2. **Independent shallow eigenproblem — CONFIRM.** Two independent
   discretizations agree to ~3 digits; p=-0.8 l2=0.9405 (matches), l-ordering
   monotone; p=-2.5 all l>=2 strictly positive. (Verifier l2(-2.5)=0.0434 sits
   with the raw-FD value 0.0428; the FEM print 0.0476 is the flagged benign
   FEM-vs-FD gap, both positive, same ordering.)
3. **Gauge claim (load-bearing) — CONFIRM.** At p=-2.5, refining Nr=200->3200,
   mu_l0 converges MONOTONICALLY FROM ABOVE to a STRICTLY POSITIVE limit
   (Richardson(1/N) = +1.756e-2); does NOT extrapolate to zero or negative. The
   l=0 eigenvector is NODELESS and correlates **0.9982 with dphi_0/dp** — a
   genuine size/depth gauge mode, not a hidden instability. l2-l0 splitting
   grid-stable (~0.0256, <0.3% drift) and positive.
4. **Sign-error / spurious-stabilization hunt — CONFIRM (none found).** Flat
   control 2.099, 3.057, 4.879, 7.399 (positive, l-ordered). Crucially the
   verifier showed its solver is NOT pinned positive: amplifying the correctly-
   signed source drives mu monotonically DOWN THROUGH ZERO — so the strictly-
   positive verdict is PHYSICAL (the source is simply too weak to destabilize),
   not a solver artifact; a flipped source sign would spuriously RAISE mu.

Independent deep mpmath check (verifier's own integrator+discretization): p=-7
all l strictly positive (~0.0095); p=-15 all channels degenerate to ~0.009506
> 0 (decoupling at a positive floor). Floor ~9.506e-3 vs production 9.633e-3
(~1.3% FD-vs-FEM discretization gap) — the POSITIVITY and strict l-ordering are
robust across two fully independent codes.

Verifier's bottom line (quoted): "The central claim SURVIVES the attack. The
lowest non-gauge l>=2 eigenvalue is strictly positive at every depth tested,
converges to a positive limit under refinement, and the l=0/l=1 zero-modes are
verified-genuine gauge modes (nodeless, ~dphi_0/dp) that approach 0 from above
without crossing negative. No shaped (l>=2) self-consistent type bifurcates in
the static bulk dilation sector down to deep core depth." Caveats confirmed as
real scope, not defects: static-bulk only (silent on nonstationary weld &
boundary/topological sector); the exact floor is ~1% discretization-dependent
but its positivity/ordering are robust; this is a no-shaped-type result, not
evidence of any structure.
```
