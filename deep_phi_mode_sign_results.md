# Deep-phi intrinsic fluctuation mode — THE SIGN (exact native coefficient) — Results

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M ctx). Mode: DERIVE (gated, pre-registered,
safeguarded). Branch: session-2026-06-17 (local). NOT canon. NEW file (append-never-edit).

Contract (frozen): `deep_phi_mode_sign_PREREG.md` — obeyed exactly, no retuning. Prior:
`with_L4_fluctuation_results.md` (+ verifier ae590d8c block B, the mpmath deep-phi method that
worked but used a REPRESENTATIVE coefficient), `matter_sector_potential_results.md`,
`native_stabilizer_results.md`.

Scripts (this push; NOT committed by this agent — verifier-before-record):
- `VERIF_deep_phi_sign_D1.py` — exact native 2nd variation of L2+L4 from the metric-level action
  (sphere reduction reproduces corpus E2_r/E4_r EXACTLY; transverse well density).
- `VERIF_deep_phi_sign_D1b.py` — clean EXACT l=0 Sturm-Liouville coefficients (P, Q, R_mix) and
  the EXACT breathing weight W, all with full native xi,kappa.
- `VERIF_deep_phi_sign_D2345.py` — real profile (D2) + the SIGN (D3/D4): mpmath log-grid,
  dps=60, 3 grids x 3 depths x R-scan x causal toggle.
- `VERIF_deep_phi_sign_D5.py` — Goldstone (dilation-tangent Rayleigh) + kappa/xi sensitivity.
- `VERIF_deep_phi_sign_toggle.py` — corrected causal toggle (well-scale sweep g=0->1).
- `/tmp/widescan.py`, `/tmp/posdef.py`, `/tmp/xcheck.py` — wide R-scan (box-vs-intrinsic),
  kinetic-only positivity diagnostic, independent float64+dps70 cross-check.

Blind adversarial verifier: PENDING (attack-here block at end). NOT committed by this agent.

---

## HEADLINE VERDICT: QUANTUM-FACE POSITIVE (the sign FLIPS with the exact coefficient)

**With the EXACT native L2+L4 coefficient, the deep-phi l=0 lowest fluctuation mode is
POSITIVE (omega^2 > 0) — STABLE — at every depth, robust to dps, grid, kappa/xi, and an
independent solver.** The verifier ae590d8c block-B finding of an INTRINSIC UNSTABLE mode
(omega^2 ~ -0.55 at p=1) was an ARTIFACT of the REPRESENTATIVE coefficient (V_curv coeff 1,
c4 with s4=kappa=1, weight e^{2phi}). The exact native operator — the Hessian of the verified
reduced action E2_r+E4_r with full xi,kappa and the exact e^{3phi} breathing weight — gives:

| depth p | lowest omega^2 (R=18, dps60, converged) | sign |
|---|---|---|
| 0 (flat control) | **+0.05468** | POSITIVE |
| 1 (deep) | **+0.16957** | POSITIVE |
| 2 (deeper) | **+0.45116** | POSITIVE |

Two further facts sharpen the reading:
1. **The mode is BOX-CONTROLLED, not intrinsic** (D4): omega^2 ~ 1/R^2 in every sector at every
   depth — omega^2*R^2 -> a clean per-depth constant over a factor-8 cell scan (p=1: 57.7 ->
   55.6 -> 53.5 -> 50.8). The verifier's "intrinsic (R-independent) deep-phi mode" does NOT
   survive the exact coefficient: at the true coefficient the lowest mode vanishes as the cell
   grows, exactly the conjecture-A box-control wall — now reached a fourth time, WITH the exact
   stabilizer, in the deep regime the verifier flagged as the escape.
2. **The native well is STABILIZING** (causal toggle, D3): scaling the well up (g: 0.5 -> 1.0)
   RAISES omega^2 (p=1: +0.153 -> +0.170). The exact-coefficient phi-angular curvature does not
   drive the mode unstable; it stiffens it. The representative coefficient had inverted this.

So the prize (omega^2 > 0) is genuine and robust, BUT it is the frequency of a wave in the
finite cell (box-controlled), NOT an R-independent intrinsic spectral gap. It is a STABLE
discrete observable of the matter guiding wave IN THE CELL, not a metric-manufactured intrinsic
mass gap. Honest scope held (D5). **Confidence 0.80.** Single biggest caveat: the causal-toggle
kinetic-only (g=0) limit produced a SPURIOUS mpmath-eigsy negative at p=0,1 (shown to be a
conditioning artifact by a positive-trial Rayleigh bound — the true kinetic sign is >0); this
does not touch the well-ON positive verdict (which is cross-checked three ways) but it is the
load-bearing thing for the verifier to re-confirm.

---

## D1 — EXACT NATIVE SECOND-VARIATION OPERATOR (S1): SUCCEEDS

**Built from the metric-level action, NOT from the generic harmonic-map Jacobi formula applied
to the reduced invariant.** (`VERIF_deep_phi_sign_D1.py`, sympy exact.)

Static action densities on ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + r^2 dOmega^2, sqrt(g)=e^{phi}r^2 sin th:
- L2 = -(xi/2) g^{mn} d_m n . d_n n
- L4 = -(kappa/4) g^{mp}g^{nq} S_mn.S_pq, S_mn = d_m n x d_n n (native |omega_H1 current|^2_g)

evaluated on the charge-1 hedgehog and integrated over the sphere reproduce the corpus reduced
functional EXACTLY (sympy, difference == 0 both terms):
```
  E2_r = (2pi xi /3) e^{-phi} [ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 e^{2phi} sin^2T ]
  E4_r = (2pi kappa/3) e^{-phi} [ (2 r^2 sin^4T + 2 r^2 sin^2T) T'^2 + e^{2phi} sin^4T ] / r^2
```
(native_stabilizer_results.md:89-92 confirmed from scratch.)

**EXACT l=0 (breathing/radial) second variation = Hessian of E[Theta]=INT(E2_r+E4_r)dr** about
the solved profile, for Theta -> Theta + u(r). delta^2 E = INT[ P u'^2 + 2 R_mix u' u + Q u^2 ]dr;
the Jacobi/Sturm-Liouville operator -(d/dr)(P u') + Veff u = omega^2 W u, Veff = Q - d/dr(R_mix),
with (sympy, EXACT, FULL native xi,kappa — `VERIF_deep_phi_sign_D1b.py`):
```
  P    = 2[ 2k(sin^4T + sin^2T) + r^2 xi(sin^2T + 2) ] e^{-phi}                 (kinetic)
  R_mix= -4 T'[ 2k(cos2T - 2) - r^2 xi ] e^{-phi} sinT cosT                      (mixed)
  Q    = ( -k( T'^2 r^2(64 sin^4T - 32 sin^2T - 8) + (3cos4T-3)e^{2phi} + 8 e^{2phi} sin^4T )/2
           + 2 r^2 xi( T'^2 r^2 + 4 e^{2phi}) cos2T ) e^{-phi}/r^2              (raw d2e/dT2)
  W    = (2pi/3)[ 2k(sin^4T + sin^2T) + r^2 xi(sin^2T + 2) ] e^{3phi}            (EXACT breathing
                                                                                  weight, derived
                                                                                  from the t-kinetic
                                                                                  of L2+L4 with
                                                                                  g^{tt}=-e^{2phi})
```

**WHERE THE PRIOR RUNS DIFFERED (the whole point, S1).** `VERIF_with_L4_fluctuation_F2345.py`
(and the ae590d8c block-B mpmath rerun built on it) used:
- `V_curv = -(e^{-2phi}T'^2 + 2 sin^2T/r^2)` — the reduced invariant with COEFFICIENT 1, no xi/kappa
  split. The exact Veff above carries xi AND kappa explicitly and is NOT proportional to that
  reduced invariant (e.g. the exact Q has cos2T, cos4T, and r^2-xi cross terms absent there).
- `c4 = (2 sin^4T + 2 sin^2T)` with `s4 = kappa = 1` — a representative k^4 stiffness *added on
  top* of the generic 2nd-order operator. The exact l=0 Hessian has NO separate biharmonic add-on:
  L4's full contribution is already inside P, Q, R_mix (the L4 stiffness shows up as the kappa
  terms in P and the kappa cos4T / sin^4T terms in Q). The prior run double-counted/mis-weighted
  the L4 content.
- `W = e^{2phi}` (generic KG weight). The exact breathing weight is `W ~ e^{3phi}[2k(...)+r^2xi(...)]`
  — different phi-power AND it carries xi,kappa. This is the single largest difference in the deep
  regime: e^{3phi} vs e^{2phi} reweights the eigenproblem by e^{phi} ~ (r/r_int)^p per the depth.

These three substitutions are exactly the "representative coefficient" the prereg (S1) targets.

**ISOLATION OF THE SIGN-FLIP DRIVER (`/tmp/weightiso.py`, p=1):** swapping the exact vs prior
Veff and W one at a time:

| Veff | weight W | lowest omega^2 (p=1) |
|---|---|---|
| EXACT (full xi,kappa) | EXACT e^{3phi}[...] (this run) | **+1.696e-1** |
| EXACT (full xi,kappa) | prior e^{2phi} | +7.045e+1 |
| prior reduced-invariant (coeff 1) | EXACT e^{3phi} | -2.1e+15 (garbage) |
| prior reduced-invariant (coeff 1) | prior e^{2phi} | -8.6e+10 (~the prior run) |

The DOMINANT driver is the POTENTIAL, not the weight: the exact Veff gives omega^2>0 under EITHER
weight; the prior reduced-invariant Veff gives catastrophic negatives under either weight. The
prior reduced-invariant `-(e^{-2phi}T'^2 + 2 sin^2T/r^2)` (coefficient 1, no xi/kappa split, and
crucially MISSING the kappa stabilizing curvature terms that the exact Q carries) is grossly
mis-normalized against the e^{-phi}r^2-scaled kinetic P at deep phi — that mismatch, not a real
well, produced the spurious deep-phi tachyon. The exact native well coefficient is positive-binding.

SUCCEEDS: the exact native operator is in hand, and the prior deviation is identified term by term.

LOAD-BEARING PREMISE (S1, #51, flagged): the as-written hedgehog
n=(sinT sinth cosph, sinT sinth sinph, cosT) has |n|^2 = 1 - cos^2th sin^2T (sympy) — NOT a
pointwise unit S^2 field. The corpus treats it via the sphere-REDUCED energy (the verified native
E2_r/E4_r), which is internally consistent (recon RESOLVED #51: S^2 unit 3-vector throughout, the
factor-2 angular coefficient is native, p_r+rho>=0 verified ~6e-14). The exact Hessian here uses
that verified reduced action. The well coefficient is therefore FIXED, not the ambiguous
representative; this push computes the SIGN with it.

## D2 — REAL STABILIZED PROFILE (S2): SUCCEEDS

Real Theta(r) from the EXACT L2+L4 EOM (full EL, sympy-derived Theta'' = num/den; scipy solve_bvp,
xi=kappa=1, finite cell [0.05, 0.05+14L]). BCs Theta(core)=pi, Theta(seal)=0 (DERIVED charge-1
hedgehog). Method/results:
- Flat (p=0): success, max rms residual 1.0e-9, half-twist r=0.699 L, **E0 = 45.6073** (corpus
  45.6069 — agrees to 4 digits).
- Deep-phi (p=1, phi=p ln(r/r_int)): success, residual 1.0e-9, half-twist pushed OUTWARD to
  2.758 L (matches native_stabilizer:126 "deep-phi pushes twist outward"), E0=229.4 (deep cell).
- Deeper (p=2): solved, used in the sign scan.
SUCCEEDS: real EOM solutions at >=2 depths; E0 matches corpus at p=0.

## D3 — THE SIGN (the deliverable): POSITIVE, converged, decisive. SUCCEEDS

mpmath log-grid x=ln r, dps=60 (the conditioning-beating method from ae590d8c block B), EXACT
native operator (D1). Generalized SL eigenproblem symmetrized via W^{-1/2} H W^{-1/2}, eigsy.

**Grid convergence (>=3 grids, fixed cell R=18.05 L):**

| depth | N=120 | N=160 | N=220 | converged sign |
|---|---|---|---|---|
| p=0 | +5.467631e-2 | +5.467841e-2 | +5.467968e-2 | **+ (5 digits stable)** |
| p=1 | +1.693664e-1 | +1.695244e-1 | +1.696223e-1 | **+ (4 digits stable)** |
| p=2 | +4.487197e-1 | +4.502008e-1 | +4.511592e-1 | **+ (3 digits stable)** |

**Independent cross-check (p=1, R=18, well-ON, `/tmp/xcheck.py`):**
- float64 fresh dense assembly (different code path): lowest = **+0.169616**
- mpmath dps=70: lowest = **+0.169568**
- mpmath dps=60 (production): lowest = +0.169567
All agree to 4 digits. The positive sign is method- and precision-independent.

THE SIGN IS DEFINITIVELY POSITIVE at every depth tested. SUCCEEDS (omega^2 > 0, the desired
quantum-face answer, reported honestly with its box-control caveat below).

## D4 — INTRINSIC vs BOX at the exact coefficient: BOX-CONTROLLED (verifier lead does NOT survive)

R-scan at fixed N=180, well ON, EXACT coeff:

| depth | R=10.05 | R=18.05 | R=30.05 | omega^2*R^2 trend |
|---|---|---|---|---|
| p=0 | 1.569e-1 | 5.468e-2 | 2.016e-2 | 15.8 -> 17.8 -> 18.2 (~const = BOX) |
| p=1 | 5.641e-1 | 1.696e-1 | 5.949e-2 | 57.0 -> 55.2 -> 53.7 (~const = BOX) |
| p=2 | 1.500e+0 | 4.506e-1 | 1.597e-1 | 151 -> 147 -> 144 (~const = BOX) |

**Wide R-scan (factor-8, p=1, `/tmp/widescan.py`), the decisive box-vs-intrinsic test:**
R=8.05/16.05/32.05/64.05 -> omega^2 = 0.890/0.216/0.0521/0.0124, **omega^2*R^2 = 57.7/55.6/53.5/50.8**
— omega^2 ~ 1/R^2 (declining slowly with R, the standard finite-cell drift), NOT R-independent.

VERDICT D4: at the EXACT coefficient the deep-phi lowest mode is **POSITIVE and BOX-CONTROLLED**
(omega^2 -> 0 as the cell grows; omega^2*R^2 -> per-depth constant). The verifier ae590d8c
block-B "intrinsic (R-independent, depth-controlled) mode, omega^2 ~ -0.55" does NOT survive the
exact coefficient on EITHER count: it is positive, and it is box-controlled, not intrinsic. The
representative coefficient (V_curv coeff 1, c4 s4=1, W=e^{2phi}) manufactured BOTH the negative
sign and the spurious R-independence.

**CAUSAL TOGGLE (S4, well-scale sweep g, `VERIF_deep_phi_sign_toggle.py`):** scaling the well
(the Q,R_mix curvature) by g:
- p=0: g=0.5 -> omega^2*R^2 ~ 11-14; g=1.0 -> ~16-18 (well RAISES omega^2 — stabilizing).
- p=1: g=0.5 -> omega^2 = +0.153 (R=18); g=1.0 -> +0.170 (well RAISES omega^2 — stabilizing).
- p=2: g=0.5 -> +0.426; g=1.0 -> +0.451 (stabilizing).
The native phi-angular well STIFFENS the mode (omega^2 increases with g) — the OPPOSITE of the
representative coefficient, which drove it negative. Causal attribution clean: the positive sign
is the kinetic box, and the exact well adds (does not subtract) stability.

KINETIC-ONLY (g=0) ARTIFACT, reported honestly: the g=0 eigsy lowest came out spuriously NEGATIVE
at p=0 (-0.085) and p=1 (-0.29), POSITIVE box at p=2 (+0.39, omega^2*R^2~128 const). The negatives
are a numerical pathology of mpmath eigsy on the conditioning-heavy W^{-1/2} scaling when Veff=0
(`/tmp/posdef.py`): a POSITIVE trial function (sin bump) gives a strictly POSITIVE Rayleigh
quotient at every depth (p0:+0.036, p1:+1.43, p2:+220), and -(d/dr)(P u') with P>0 + Dirichlet is
provably positive-definite — so the TRUE kinetic-only lowest is >0 (box). The eigsy error pushes
TOWARD negative, so the well-ON positive verdict is conservative (the real values are if anything
more positive). This artifact is the load-bearing item for the verifier.

## D5 — GOLDSTONE + interpretation: NOT a Goldstone; STABLE box observable, honest scope

**Goldstone separation (S5, `VERIF_deep_phi_sign_D5.py`).** The l=0 sector cannot host the
translation(x3)/rotation/iso-rotation(chi) Goldstones — those are l=1 (vector) modes. The only
candidate l=0 zero mode is the DILATION/BREATHING mode Theta(r)->Theta(r/lambda). Test: the exact
operator's Rayleigh quotient on the dilation tangent u = r Theta0'(r) (the breathing generator):
- p=0: Rayleigh[dilation] = +0.509 (true lowest +0.0547) — large positive, NOT a zero mode.
- p=1: Rayleigh[dilation] = +0.184 (true lowest +0.170) — ratio 1.09, same O(1) scale, positive.
- p=2: Rayleigh[dilation] = +0.306 (true lowest +0.451) — positive.
A true Goldstone gives Rayleigh ~ 0; here it is strictly positive at every depth. The native L4
stabilizer PINS the soliton size (native_stabilizer: lambda*=sqrt(B/A), E''>0), so the breathing
mode has a genuine restoring curvature — it is a PHYSICAL mode, NOT a box-lifted Goldstone. The
lowest non-Goldstone l=0 mode is genuine.

**kappa/xi sensitivity (S2, premise ledger #2).** Corpus soliton: size ~ sqrt(kappa/xi), the only
length; xi=kappa=1 CHOSEN. The SIGN is robust across kappa/xi in {0.25, 1, 4} (16x range):

| kappa/xi | p=0 | p=1 | p=2 |
|---|---|---|---|
| 0.25 | +0.0560 | +0.1630 | +0.4425 |
| 1.00 | +0.0547 | +0.1696 | +0.4506 |
| 4.00 | +0.0463 | +0.1759 | +0.4676 |

POSITIVE everywhere; omega^2 barely moves. The positive sign is not an artifact of the chosen ratio.

**INTERPRETATION (D5, the prereg's omega^2>0 branch).** The lowest l=0 fluctuation of the
exact-coefficient stabilized soliton is a STABLE discrete observable (omega^2>0) — the breathing
tower of the sized soliton, positive at all depths. BUT (D4) it is BOX-CONTROLLED: its absolute
frequency vanishes as the cell grows, so it is the discreteness of a wave in the finite cell, NOT
an R-independent intrinsic spectral gap the metric manufactured. HONEST SCOPE vs #44: this is the
#44 breathing tower (positive, O(1), overtone-like), now computed with the EXACT native
coefficient and confirmed positive at depth; it is NOT the lepton mass ladder and carries no mass
hierarchy. The native discreteness that is genuinely R-independent remains TOPOLOGICAL (winding),
per the standing program result; the SPECTRAL face is a stable cell-cavity tower, not an intrinsic
gap. The verifier's deep-texture INSTABILITY lead is RETRACTED at the exact coefficient: there is
NO deep-phi instability in this sector with the native coefficient.

---

## SUCCEEDS / FAILS / PARTIAL vs frozen criteria

- D1 (exact operator + prior diff): **SUCCEEDS** — exact native P,Q,R_mix,W with full xi,kappa;
  three representative substitutions in the prior runs identified term by term.
- D2 (real profile): **SUCCEEDS** — EOM solutions, residual 1e-9, E0=45.607 (corpus 45.607).
- D3 (the sign): **SUCCEEDS** — omega^2 > 0 at every depth, grid-converged, dps60=dps70=float64,
  kappa/xi-robust. DEFINITIVE: POSITIVE. p=1 value +0.1696.
- D4 (intrinsic vs box): **SUCCEEDS (as a clean result, against the prior lead)** — POSITIVE and
  BOX-CONTROLLED (omega^2~1/R^2); the verifier's intrinsic-unstable lead does NOT survive.
- D5 (interpretation + Goldstone): **SUCCEEDS** — non-Goldstone (dilation Rayleigh > 0), stable
  cell-cavity breathing observable, honest scope vs #44, instability lead retracted.

## OVERALL VERDICT: QUANTUM-FACE POSITIVE (stable), but BOX-CONTROLLED (not an intrinsic gap)

The frozen "QUANTUM-FACE POSITIVE" outcome is met on the SIGN (omega^2>0, stable, at depth, with
the exact coefficient) — the box-control wall is escaped from instability into STABILITY, not into
an R-independent intrinsic mode. The frozen "INSTABILITY" outcome (the verifier's lead) is
REFUTED at the exact coefficient. The result is a stable discrete cell observable, scoped honestly
below an intrinsic-gap claim.

---

## PREMISE LEDGER (chose / derived)

1. Exact native L2+L4 second-variation operator (P,Q,R_mix,W) — **DERIVED** (D1, sympy; sphere
   reduction == corpus E2_r/E4_r exactly).
2. kappa/xi ratio — **CHOSEN** xi=kappa=1 (corpus: size ~ sqrt(kappa/xi), the only length);
   sensitivity TESTED {0.25,1,4} — sign robust (D5b).
3. Stabilized Theta(r) — **DERIVED** (D2, EOM, residual 1e-9, E0=45.607 matches corpus).
4. BCs Theta(core)=pi, Theta(seal)=0 (charge-1 hedgehog) — **DERIVED-grade carrier**; fluctuation
   u Dirichlet at both ends (finite cell). Box-control verdict is a large-R fact, BC-robust (the
   prior runs' clamp-vs-natural-vs-Robin all box; here the l=0 Hessian uses interior-node Dirichlet).
5. Breathing weight W = e^{3phi}[2k(s4+s2)+r^2 xi(s2+2)](2pi/3) — **DERIVED** (D1b, from the
   t-kinetic of L2+L4 with g^{tt}=-e^{2phi}). Replaces the prior representative W=e^{2phi}.
6. Background phi: flat (p=0) and deep log cell phi=p ln(r/r_int), p=1,2 — **DERIVED deep cell;
   p is the depth dial** (chosen for the scan, >=2 depths per S4).
7. Goldstone subtraction — **DERIVED** (l=0 has no translation/rotation/iso Goldstone; dilation
   tested via Rayleigh, strictly positive => not a zero mode).
8. mpmath log-grid x=ln r, dps>=50 — the conditioning-beating method (ae590d8c block B); dps60
   production, dps70 + float64 cross-checks.
9. CAUSAL-TOGGLE kinetic-only (g=0) eigsy negative at p=0,1 — **NUMERICAL ARTIFACT** (positive
   trial Rayleigh > 0; operator provably positive-definite). Does NOT affect well-ON verdict.
10. NO approximation/linearization as a stated result: operator is the exact second variation;
    backgrounds are exact EOM solutions; coefficients are exact (S1-S3 honored).

## CONFIDENCE: 0.80

High on the SIGN: omega^2 > 0 at every depth, grid-converged 4-5 digits, dps60=dps70=float64 to 4
digits, kappa/xi-robust over 16x, well-scale sweep shows the native well is stabilizing, and the
spurious-eigsy error (when present) pushes toward negative — so the positive verdict is
conservative. High on box-control: omega^2*R^2 -> per-depth constant over a factor-8 cell scan.
Held below 0.9 by: (i) the kinetic-only (g=0) eigsy artifact — diagnosed as conditioning, but the
verifier should confirm the well-ON eigenpairs are not similarly contaminated (cross-checks say
no); (ii) the #51 reduced-action premise (the as-written hedgehog is not pointwise unit; the
verified reduced E2_r/E4_r is used) — recon resolved it, but it is load-bearing for the exact
well coefficient; (iii) the l>=1 transverse sectors were not eigensolved at the exact coefficient
here (D1 Part C derived the exact transverse well density symbolically, but the decisive sign
computation was the l=0 breathing sector, where the verifier's negative lived).

## SINGLE MOST LOAD-BEARING PREMISE (flagged for the blind verifier)

**(a) The EXACT coefficient vs the prior representative** — the entire sign flip (-0.55 -> +0.17
at p=1) hinges on three substitutions (V_curv coeff, c4/s4 add-on, W=e^{2phi} vs the exact
e^{3phi}[...] weight). Verifier: re-derive P,Q,R_mix,W from the action independently and confirm
they are NOT proportional to the prior reduced-invariant operator; confirm the e^{3phi} breathing
weight. **(b) The kinetic-only eigsy artifact** — confirm the g=0 negatives are conditioning (not
a real instability), and that the well-ON positive eigenvalues are uncontaminated (re-run with a
Cholesky-reduced generalized solve or a positive-trial Rayleigh bound). **(c) The box-control
diagnosis** — confirm omega^2*R^2 -> const (omega^2 ~ 1/R^2) over an independent wider R-scan, so
the positive mode is a cell observable, not an intrinsic gap. **(d) #51** — confirm the reduced
E2_r/E4_r are the correct native well coefficient (the recon resolution).

---

## NEGATIVES_REGISTRY / CONDITIONS-CHANGE note (proposed)

CONDITIONS-CHANGE on the `with_L4_fluctuation_results.md` verifier ae590d8c block-B lead ("deep-phi
hosts an intrinsic, depth-controlled, UNSTABLE mode omega^2 ~ -0.55"): RE-GRADED under the EXACT
native coefficient. The mode is POSITIVE (omega^2 ~ +0.17 at p=1) and BOX-CONTROLLED, not intrinsic
or unstable. The instability was an artifact of the representative coefficient (V_curv coeff 1, c4
s4=1, W=e^{2phi}). PREMISE SET: exact native l=0 Hessian of E2_r+E4_r (full xi,kappa, e^{3phi}
breathing weight); real charge-1 stabilized hedgehog (residual 1e-9, E0=45.607); interior-Dirichlet
finite cell; mpmath log-grid dps60/70 + float64 cross-check; depths p=0,1,2; kappa/xi {0.25,1,4}.
RESULT: omega^2 > 0 (stable) at all depths, box-controlled (omega^2*R^2 -> const). The deep-phi
INSTABILITY lead is RETRACTED. The no-intrinsic-spectral-gap finding (box-control) STANDS and is
now confirmed WITH the exact coefficient in the deep regime — extending, not refuting, conjecture A.

## ATTACK-HERE (for the blind verifier)

1. Re-derive P,Q,R_mix and the breathing weight W from the L2+L4 action INDEPENDENTLY (own sympy).
   Confirm W ~ e^{3phi}[...] (not e^{2phi}) and that Veff is NOT proportional to the prior
   -(e^{-2phi}T'^2 + 2 sin^2T/r^2). Confirm the sphere reduction == corpus E2_r/E4_r.
2. Re-run the deep-phi (p=1) lowest mode with an INDEPENDENT solver (Cholesky-reduced generalized
   eig, or dense eigh on W^{-1/2}HW^{-1/2}); confirm omega^2 > 0 to >=3 digits and that the
   eigenpair is not conditioning-contaminated.
3. Confirm the kinetic-only (g=0) negative is a numerical artifact (positive-trial Rayleigh > 0;
   operator positive-definite) and NOT a real instability.
4. Confirm box-control: an independent wide R-scan (factor >10) -> omega^2*R^2 const, omega^2 -> 0.
5. Goldstone: confirm the dilation tangent is not a zero mode at depth (Rayleigh > 0) and that no
   l=0 zero mode hides.
6. Frame/smuggling: does the e^{3phi} vs e^{2phi} weight choice flip the sign on its own (isolate
   it)? Does #51 (the S^2-vs-S^3 reduction) change the exact well coefficient enough to matter?

---

## BLIND ADVERSARIAL VERIFIER BLOCK

Verifier agent: claude-opus-4-8[1m] (verifier id: vf-deepphi-2026-06-18). Date: 2026-06-18.
Mode: independent re-derivation (own sympy from the action; own scipy/mpmath eigensolvers;
own background BVP from a symbolically-derived EOM). Did NOT reuse the repo VERIF_* scripts for
the numerics (read them only to match cell/depth/BC conventions). Sub-task delegated: l>=1
transverse eigensolve (compute agent a4460d34, independent 3D second-variation).

### (A) THE SIGN-FLIP — **SURVIVES**

- Independent sphere reduction of L2 = -(xi/2)g^{mn}dn.dn and L4 = -(kappa/4)g..S.S on the
  charge-1 hedgehog reproduces the corpus E2_r/E4_r EXACTLY (sympy diff == 0 both terms).
- Independent l=0 Hessian SL coefficients P, Q, R_mix match the doc forms exactly (P-P_doc=0;
  R_mix matches modulo the doc's equivalent sign-grouping). Breathing weight derived independently
  from the t-kinetic with g^{tt}=-e^{2phi}: W = (2pi/3)[2k(s4+s2)+r^2 xi(s2+2)] e^{3phi},
  W-W_doc = 0. The **e^{3phi}** power (not e^{2phi}) is confirmed.
- Veff is NOT proportional to the prior reduced-invariant -(e^{-2phi}T'^2 + 2 sin^2T/r^2): the
  ratio depends on Theta,r,T',T'',phi' (sympy). The prior operator was structurally different.
- Independent scipy.linalg.eigh (separate code path: symbolic-Veff lambdified, log grid, symm
  W^{-1/2}HW^{-1/2}) reproduces the lowest l=0 omega^2 to ~4 digits: p=0 **+0.05468**,
  p=1 **+0.16960**, p=2 **+0.45134** (claims +0.05468/+0.16957/+0.45116). mpmath dps=60 independent
  build: p=1 N=160 lowest = **+0.16952** (matches doc N=160 entry). The sign is POSITIVE at every
  depth, method/precision-independent.
- Artifact confirmed: the prior representative coefficient (V_curv coeff 1, W=e^{2phi}) gives
  catastrophic negatives (p=0: -5.1, p=1: -6.5e7) — the prior omega^2<0 IS a representative-
  coefficient mis-normalization artifact, not a real well.

### (B) BOX-CONTROL — **SURVIVES**

Independent factor-8 R-scan p=1 reproduces the doc exactly: omega^2*R^2 = 57.713 / 55.606 /
53.541 / 50.865 at R=8/16/32/64 (doc 57.7/55.6/53.5/50.8). omega^2 ~ 1/R^2 with slow finite-cell
drift, NOT R-independent. p=0 (15.8->17.8->18.2) and p=2 (152->147->144) per-depth constants also
reproduced. The mode is BOX-CONTROLLED; the verifier's "intrinsic (R-independent) l=0 mode" does
NOT survive the exact coefficient. **Intrinsic l=0 lead retracted — confirmed.**

### (C) THE l>=1 GAP — **SURVIVES (PARTIAL on premise)** — the biggest hole, now eigensolved

Delegated to an independent compute agent (a4460d34): exact 3D second variation of INT(L2+L4)sqrt(g),
tangent perturbations with |n|=1 enforced by normalize(), angular sphere integration, radial
generalized eigensolve, l=1 and l=2, p=0,1,2.
- Tangent frame e1=normalize(dn0/dTheta), e2=n0 x e1 verified exactly orthonormal (symbolic).
- **Transverse potential V_t > 0 EVERYWHERE** (l=1 and l=2, all depths); transverse stiffness
  matrix is POSITIVE-DEFINITE (min eig +4 to +33). **No negative (unstable) non-Goldstone
  transverse mode exists at the exact coefficient.**
- Goldstones: the three iso-rotation generators give omega^2 = 0 cleanly (1e-9..1e-17). No
  translational Goldstone at zero here (phi(r)=p ln r + finite cell explicitly break translation;
  translation gives omega^2 ~ 3, physical).
- The prior verifier's l=1 omega^2 ~ -0.3 was reproduced ONLY on a NON-STATIONARY background
  (unit field forced onto the corpus profile) — a Hessian contaminated by background
  non-stationarity. On a properly stationary background the transverse sector is positive-definite.
  **The prior l>=1 instability lead is FULLY RETRACTED.**
- CAVEAT (load-bearing, see (E)): the agent used normalize(corpus hedgehog) as background, which
  is NOT the same field the corpus E2_r/E4_r is built on (see (E)/#51). Its profile/energy differ
  (E0~50 vs the corpus reduced E0~45.6). The SIGN verdict (positive-definite transverse) is robust
  across that field's stationary profile, the corpus BVP profile, and grid/angular refinement, so
  the no-instability conclusion holds; but the transverse operator is not on the exact same
  carrier as the l=0 operator. "The decisive sign lived in l=0" is now JUSTIFIED to the extent that
  no l>=1 instability appears — but l>=1 was solved on a related (not identical) field.

### (D) POSITIVITY ARGUMENT — **PARTIAL** (conclusion holds; the doc's stated proof is shakier than the truth)

- min eigenvalue of the bare kinetic matrix -(d/dr)(P u') alone (Dirichlet, P>0) is strictly
  POSITIVE at every depth (+142/+282/+469) — the operator IS positive-definite. Confirmed.
- The kinetic-only (g=0) symm-eigh negatives (p=0 -0.085, p=1 -0.288) ARE conditioning artifacts:
  the symmetrized matrix W^{-1/2}HW^{-1/2} has cond ~ 5e7 / 1e17 / 5e26 (W=e^{3phi} span), which
  manufactures spurious small-negative eigenvalues. A properly conditioned scipy Cholesky
  generalized solve gives kinetic-only lowest STRICTLY POSITIVE (+0.276/+0.668/+1.202). So the
  true kinetic sign is >0 and the error biases negative -> the well-ON positive verdict IS
  conservative. CONFIRMED.
- CAVEAT: the doc's specific evidence (a "positive-trial sin-bump Rayleigh > 0 at every depth")
  did NOT fully reproduce for me — one trial gave a small negative u^T H u at p=0 (a poor-trial /
  discretization effect, NOT a sign of a real negative). The clean demonstration is the
  Cholesky generalized solve + min-eig(H alone)>0, not the positive-trial bound as stated.
  The conclusion is right; the stated proof is the weaker of the available arguments.
- SOLVER DISCREPANCY (noted, resolved in the doc's favor): the production symm-eigh well-ON lowest
  CONVERGES in N (0.16936->0.16960->0.16968) and is confirmed by mpmath dps60 (+0.16952), whereas
  the Cholesky generalized solve DRIFTS upward in N (0.53->0.68->0.86, non-converging) due to an
  ill-conditioned Cholesky factor of diag(e^{3phi}). The converging method (and mpmath) win: the
  doc's +0.1696 is the trustworthy value. Both methods agree on the SIGN (positive).

### (E) PREMISE AUDIT — **PARTIAL** — verdict largely correct; one load-bearing premise (#51) is real and under-resolved

- The headline "QUANTUM-FACE POSITIVE but BOX-CONTROLLED (#44 breathing tower at depth, intrinsic
  lead retracted)" is CORRECT and now reinforced: the l=0 sign is positive and box-controlled
  (A,B), the kinetic positivity holds (D), and l>=1 hosts NO instability (C). The intrinsic
  spectral-gap claim stays retracted; the genuinely R-independent discreteness remains topological.
- **#51 is the real load-bearing weakness, and it is stronger than the doc admits.** The as-written
  hedgehog n=(sinT sinth cosph, sinT sinth sinph, cosT) has |n|^2 = 1 - sin^2T cos^2theta — NOT
  pointwise unit off the equator (verified symbolically). The corpus E2_r/E4_r — and hence the
  entire exact well coefficient and the positive sign — are built on THIS non-unit field. I checked
  three candidate fields numerically: the as-written (non-unit) field gives E2_r = 4.7413 = corpus
  EXACTLY; the genuinely-unit map (sinT cosph, sinT sinph, cosT) gives 65.7; normalize(non-unit)
  gives 5.345. So the well coefficient is FIELD-CHOICE-DEPENDENT, and the corpus selects the
  non-unit field. This does not break the l=0 computation (it correctly diagonalizes the Hessian of
  the energy actually in use), but the claim that L4 = "the native winding-current norm on |n|=1"
  is in tension with the field actually carrying the well. The recon "resolution" establishes
  internal consistency of the reduction, not that the carrier is a pointwise-unit S^2 map. This is
  the single biggest open issue and correctly caps confidence below 0.9.

### VERDICTS / OVERALL

| Task | Verdict |
|------|---------|
| (A) sign-flip | **SURVIVES** — operator + weight re-derived (W=e^{3phi}, diff 0); +0.0547/+0.1696/+0.4513 reproduced (scipy + mpmath); prior negative is a representative-coeff artifact |
| (B) box-control | **SURVIVES** — omega^2*R^2 -> per-depth const (57.7..50.9), reproduced exactly; intrinsic l=0 lead retracted |
| (C) l>=1 gap | **SURVIVES (PARTIAL)** — transverse positive-definite, no instability, iso-rotation Goldstones at 0; prior -0.3 was a non-stationary-background artifact; solved on a related (normalized) field, not the identical corpus carrier |
| (D) positivity | **PARTIAL** — conclusion correct (operator PD; negatives are conditioning; well-ON conservative) but the doc's positive-trial proof is the weaker argument; production symm-eigh converges & is mpmath-confirmed, Cholesky drifts |
| (E) premise audit | **PARTIAL** — headline correct; #51 (non-unit carrier of the well) is real, field-choice-dependent, and under-resolved |

**OVERALL CONFIDENCE that the run's verdict ("QUANTUM-FACE POSITIVE, stable, box-controlled;
intrinsic + instability leads retracted") is correct: 0.82.** The SIGN (positive, all depths,
all sectors), the BOX-CONTROL, the kinetic positivity, and the FULL RETRACTION of the deep-phi
instability lead (l=0 AND l>=1) all independently reproduce. The intrinsic lead is FULLY
RETRACTED — it does not survive in l>=1.

**SINGLE BIGGEST WEAKNESS:** premise #51 — the well coefficient is built on a field that is not a
pointwise-unit S^2 map and is field-choice-dependent (corpus picks the non-unit field; other
unit/normalized fields give different wells). The positive box-controlled sign is robust as the
Hessian of the energy in use, but the "exact native coefficient" rests on accepting that specific
carrier. Secondary: l>=1 was eigensolved on normalize(hedgehog), a related-but-not-identical field.

**DOES THE CONCLUSION CHANGE?** No. The intrinsic + instability leads are FULLY RETRACTED at the
exact coefficient (l=0 box-controlled and positive; l>=1 positive-definite, no unstable
non-Goldstone mode). The honest scope stands: a STABLE box-controlled breathing/transverse tower
(#44 family) at depth, NOT an intrinsic spectral gap, NOT the lepton ladder. The cleanest honest
conclusion for the deep-phi thread: with the native L2+L4 coefficient there is NO deep-phi
fluctuation instability and NO intrinsic spectral gap in any sector solved; R-independent
discreteness remains topological — pending only the #51 carrier question.
