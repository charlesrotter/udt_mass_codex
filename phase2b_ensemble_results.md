# Phase-2b Results — Multi-Mode / Ensemble ("the orchestra") of the Bare Time-Live Whole-Metric Solve

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = OBSERVE (report what is there;
no result forced). DATA-BLIND (no mass/ratio/wall numbers; sizes in cell-radius R units
or dimensionless ratios). Category-A (GR numerics borrowed for tractability ONLY; no
physics, no matter, no scale imposed). Frame: time_live_bare_solve_DESIGN.md
(DECISIONS-LOCKED), phase1_geon_results.md (the single-mode Phase-1 result + the scoped
(4) net-negative single-mode mass that this push attacks), CANON C-2026-06-18-1 + C-2026-06-10-2.

Scripts (all NEW, prefix phase2b_; nothing committed changed):
- phase2b_cross_stress.py   -- EXACT symbolic derivation of the general-l even-parity
  reconstruction + the MULTI-MODE (cross) GW stress; the TWO selection rules (verified).
- phase2b_self_coeffs.py    -- EXACT per-l self-source numerator coefficients (l=2 == phase1).
- phase2b_ensemble_solve.py -- the N-mode self-gravitating packet: dense Newton + amplitude
  continuation, Misner-Sharp mass; the composition mass sweep.
- phase2b_cross_and_box.py  -- the degenerate cross-channel test + the box-control gate.
- (logs) phase2b_output.log, phase2b_ensemble_run.log, phase2b_cross_box_run.log.

---

## THE THREE-OUTCOME VERDICT: OUTCOME B-ens (ensembles exist, arbitrary, box-controlled, NO net positive mass, NO selection).

The orchestra adds NO structure a single note lacks. Multi-mode self-gravitating packets
EXIST and converge cleanly, but every composition carries NET-NEGATIVE Misner-Sharp mass,
there is NO preferred/selected composition, and the whole sector remains box-controlled
(scale-free). The Phase-1 scoped (4) negative — a single bare standing wave carries no
positive mass — is NOT lifted by the ensemble; it is GENERALIZED to it.

Single most decisive number: the static mass of the full mixed orchestra (l=2,3,4
fundamentals) is **M = m(R)/A^2 = -0.00551, R-INVARIANT to 3 sig figs across R = 1,2,4,8
(-0.005513, -0.005523, -0.005528, -0.005530) and N-stable to 7 digits (N=60..160)** —
a scale-free NEGATIVE number set by mode shape, not the box, and never positive.

THE REASON (derived, exact — the heart of this push): in the bare diagonal vacuum the
O(A^2) static l=0 mass is sourced by a stress that is QUADRATIC in the wave, so for a
superposition the cross (interference) terms survive the time- AND angle-average under
TWO selection rules — a cross term between modes i,j contributes to the static mass ONLY
if l_i = l_j AND w_i = w_j. Every physically-distinct mode pair (different multipole, or
different radial overtone => different frequency) therefore has ZERO cross coupling, and
the mass is STRICTLY ADDITIVE over individually-negative modes: M = sum_i (negative) < 0.
The only surviving cross channel is exact degeneracy (same l, same w = the azimuthal
m-multiplet, which shares the radial profile), and there the cross term is just the
polarization of the SAME negative-definite self-stress (S_cross(i=i) = 2 S_self) — it
re-sums negative self-energy, never flips the sign. The orchestra's interference is
killed by the averaging; mixing cannot manufacture positive mass.

---

## PART 1 — THE MULTI-MODE STRESS (exact symbolic, verified) — the two selection rules

General-l even-parity Zerilli reconstruction (DERIVED, over-constraint PASS for l=2,3,4;
== phase1 at l=2): the l=2 forms with the constant 3 promoted to l(l+1)/2:
  H0 = H2 = [-i r^2 w^2 G + i r G' + i (l(l+1)/2) G]/(r w),  H1 = r G' + G,
  K = [i r G' + i (l(l+1)/2) G]/(r w),  master G'' = (l(l+1)/r^2 - w^2) G, Psi_l = r j_l(wr).

The O(A^2) time-and-angle-averaged static l=0 G_tt gives the SAME Misner-Sharp F-operator
(2/r^2)(rF)' and a SOURCE S_total = sum over mode-pairs. The two selection rules
(CONFIRMED both by the complex double-copy time-average and the explicit real cos/sin
route, diff = 0):
- TIME RULE: a cross term i<->j carries e^{-i(w_i - w_j)t}; the static backreaction needs
  the t-independent piece => survives ONLY if **w_i = w_j**. Unequal frequencies average to 0.
- ANGLE RULE: the l=0 projection of P_{l_i} P_{l_j} (and the derivative-coupling stress)
  is nonzero ONLY if **l_i = l_j** (Legendre orthogonality; (2,4),(2,3),(3,4) all vanish;
  (2,2),(3,3),(4,4) survive).

=> ONLY EQUAL-(l, w) mode pairs source the static mass. The exact per-l self-source
numerators (over 40 r^4 w^2) were extracted symbolically; l=2 reproduces the phase1
gw_source_S verbatim, and l=3,4 carry rational coefficients (denominators 7, 9, 3 from
the Legendre integrals — recorded exactly in phase2b_self_coeffs.py, NOT rounded). The
diagonal (i=j) cross reduces to 2 S_self exactly.

---

## PART 2 — EXISTENCE + CONVERGENCE (the multi-mode solve) — PASS

Dense explicit-Jacobian LM/Newton + amplitude continuation, Chebyshev pseudospectral on
r in [eps R, R], matter slot EMPTY, held tie g_tt g_rr = -1, core regular Psi ~ r^{l+1},
Dirichlet wall, m(0)=0 core BC; normalization ||Psi_i||^2 = share_i A^2 (one row per mode,
shares sum to 1 so total packet power = A^2). The common static F dresses every wave operator.

- A self-consistent bound multi-mode configuration EXISTS and CONVERGES to the residual
  floor (~1e-11 to 1e-13) for every composition tested, up to A ~ 0.2-0.3.
- VALIDATION (single-mode limit): a single l=2 fundamental recovers Phase-1 exactly —
  w(A=0.1) = 5.7625161, m(R)/A^2 = -0.00905 (matches phase1c), source matches phase1
  gw_source_S to 5.5e-17.
- N-refinement (l2+l3+l4, A=0.1): M = -0.0055132 STABLE to 7 digits across N=60,80,120,160
  (resid ~1e-11) => spectrally converged, GENUINE, NOT solver-limited.

---

## PART 3 — *** THE MASS QUESTION *** (the point) — every ensemble is NET-NEGATIVE

M = m(R)/A^2 (Misner-Sharp deficit m = A^2 r F(R)) at the largest converged A (R=1):

| Composition | cross-pairs | M = m(R)/A^2 |
|---|---|---|
| single l=2 fundamental (Phase-1 ref) | [] | -0.0359 (A=0.2) |
| l=2 fund + l=2 1st overtone (n=1,2; diff w) | [] | -0.0603 |
| l=2 + l=3 fundamentals (mixed-l) | [] | -0.0306 |
| l=2 + l=4 fundamentals (mixed-l) | [] | -0.0188 |
| l=2 + l=3 + l=4 (full mixed orchestra) | [] | -0.0209 |
| l=3 fundamental alone | [] | -0.0252 |
| l=4 fundamental alone | [] | -0.0007 |
| DEGENERATE 2x l=2 fundamental (cross ACTIVE) | [(0,1)] | -0.1061 |

EVERY composition is NEGATIVE. No mode-mix gives positive M. (An earlier non-converged
run showed spurious positive values at residual ~0.5 from a normalization-row bug; with
the corrected square normalization those vanish — they were numerics, not physics.)

THE DEGENERATE CROSS CHANNEL (the only one where interference survives) was exercised
directly: the cross term is ACTIVE, and M becomes MORE negative (-0.106 vs -0.036 single),
because S_cross(i=i) = 2 S_self adds the same negative self-stress. Structurally a single-l
cavity fundamental is unique up to scale, so the only same-(l,w) multiplicity is the
azimuthal m-multiplet (identical radial profile); the cross channel has NO independent
shape to bind and cannot reach positive mass.

ANSWER: an ensemble CANNOT carry net-positive mass via interference / cross-mode binding.
The interference channel is killed by the time/angle average except at exact degeneracy,
and even there it only re-sums negative self-energy. WHICH mixes give positive vs negative:
NONE give positive; ALL give negative.

---

## PART 4 — SELECTION / STRUCTURE — none (free, arbitrary, additive)

- NO preferred composition: with no surviving cross coupling between distinct modes, the
  total mass and the static F are LINEAR (additive) functionals of the per-mode powers
  share_i A^2. Any superposition is admissible; nothing extremizes, binds, or is selected.
- NO discrete selection, NO preferred ratio, NO non-box feature from cross-mode coupling.
  The cross-mode coupling that COULD have produced selection is exactly the channel the
  two selection rules switch OFF for all physically-distinct modes.
- The inter-mode frequency ratios are the scale-free content (w_i/w_0 = 1, 1.2125, 1.4197
  for l=2,3,4 fundamentals) but they are JUST the j_2, j_3, j_4 first-zero ratios — a
  mixed-l spherical-cavity Bessel ladder, NOT a new intrinsic structure.

---

## PART 5 — BOX-CONTROL GATE (DESIGN 5.1) — BOX-CONTROLLED (all three criteria FAIL the escape)

1. 1/R scaling: w_i * R is CONSTANT to 0.000e+00 % drift across R = 1,2,4,8 (every mode).
   Pure 1/R box ladder.
2. Wall-relocation invariance of the mass coefficient: M = m(R)/A^2 = -0.005513, -0.005523,
   -0.005528, -0.005530 across R = 1,2,4,8 — a dimensionless, R-INVARIANT NEGATIVE number
   (the small residual drift << the historical few-% threshold). The dimensionless content
   is R-free but NEGATIVE and structure-free.
3. Intrinsic lock: NONE. No frequency or mass tracks any intrinsic dimensionful quantity;
   everything is the cell-size box ladder + a scale-free negative shape number.

The inter-mode RATIOS are the physical (scale-free) content, but they are the trivial
mixed-l Bessel ladder, NOT a new structured feature. Consistent with the banked
single-cell box-controlled negatives (Registry #1/#44/CS4) and with Phase-1 OUTCOME B.

---

## PREMISE LEDGER (chose / derived / leading-order)

| Item | tag | note |
|---|---|---|
| Exponential dilation g_tt=-e^{-2phi}, B=1/A tie (c=1) | DERIVED (C-2026-06-18-1) | held structure |
| Vacuum T_munu=0 (matter slot empty) | CHOSE | bare-first decision (DESIGN, locked) |
| Round static bare background = FLAT (m=0) | DERIVED (Phase-0/1) | Schwarzschild eqn + core regularity |
| General-l even-parity Zerilli reconstruction | DERIVED | over-constraint PASS l=2,3,4; ==phase1 at l=2 |
| Multi-mode O(A^2) cross stress + TWO selection rules | DERIVED | time (w_i=w_j) + angle (l_i=l_j); two routes agree, diff=0 |
| per-l self-source numerators | DERIVED (exact, sympy) | l=2 == phase1 to 5.5e-17; l=3,4 rational coeffs (not rounded) |
| O(A^2) backreaction truncation (single harmonic per mode) | CHOSE | same order as Phase-1; the additive-mass result is an O(A^2) statement |
| phi-dressing of each wave operator | CHOSE | as Phase-1 C5 (existence of bend robust; sign result is the mass, not the bend) |
| per-mode normalization ||Psi_i||^2 = share_i A^2 | CHOSE | square + consistent; the relative weights {a_i} are the free sweep knob (NOT a hand-picked composition) |
| Misner-Sharp deficit mass m = A^2 r F(R) | DERIVED | the Phase-1 read-off, generalized |
| Areal radius (rho = r chart) | CHOSE | chart-independence not separately tested |

REGIME STAMPS:
- Cross-stress + selection rules: exact (sympy), flat round vacuum background, l=2,3,4.
- Ensemble solve: O(A^2) backreaction (single harmonic per mode), dense Newton + amplitude
  continuation, converged to floor ~1e-11 for A <~ 0.2-0.3, R in {1,2,4,8}, N=60..160 stable.
  GENUINE (NOT solver-limited): N-refinement flat to 7 digits.

---

## ATTACK HERE (for a blind verifier)

- THE SELECTION RULES (the load-bearing claim): re-derive (independent CAS) that the
  O(A^2) static l=0 cross stress survives ONLY for l_i=l_j AND w_i=w_j. Attack the angle
  rule especially: confirm the DERIVATIVE-coupling stress terms (not just P_{l_i}P_{l_j}
  but the theta-derivative combinations) ALL l=0-project to zero for l_i != l_j — the
  whole no-cross conclusion rests on this. If ANY mixed-l derivative-coupling term has a
  nonzero l=0 projection, the additive-mass verdict is wrong.
- THE ADDITIVITY => NEGATIVITY chain: with no cross terms, M = sum of per-mode masses, each
  < 0 (Phase-1 + the l=3,4 single-mode runs here, also negative). Confirm the l=3 and l=4
  single-mode masses are genuinely negative (not a transcription error in the per-l
  coefficients) — re-run a single-l mode from the symbolic source directly.
- THE PER-L COEFFICIENTS: the l=3,4 self-source numerators carry rational coefficients
  (denoms 7,9,3). Re-extract them independently and confirm; a wrong coefficient would
  shift the (still-negative?) mass. The l=2 column is anchored to phase1 (5.5e-17 match).
- TRUNCATION HONESTY: the additive-mass result is an O(A^2) statement. At O(A^4) the
  cross terms between non-degenerate modes re-appear (the e^{+-i(w_i-w_j)t} pieces beat
  against another factor) — does a higher-order (O(A^4)) or multi-time-harmonic solve open
  a genuine cross channel that could carry positive mass? This push closes the O(A^2)
  orchestra; it does NOT close O(A^4)+.
- THE DEGENERATE CHANNEL: confirm the azimuthal m-multiplet really shares the radial
  profile (so the cross channel has no independent shape) — i.e. that there is no
  same-(l,w) pair with DIFFERENT radial shape in the single-l Dirichlet cavity. If a
  genuine shape-distinct degeneracy exists, the cross channel must be re-examined.
- ROTATION / OFF-DIAGONAL (Phase-2 companion, NOT exercised): the g_Tpsi frame-dragging
  geon (Phase-0 B1) could lock onto angular momentum and is a DIFFERENT object; the
  diagonal additive-negative-mass verdict does NOT cover it.
- NORMALIZATION-BUG SCAR: the first run showed spurious POSITIVE masses at residual ~0.5
  (over-determined norm rows). Confirm the corrected square normalization (M per-mode
  share rows) is what produced the converged (resid ~1e-11) negative results — re-run and
  check ok=True everywhere.

---

## STATUS

Phase-2b COMPLETE. OUTCOME B-ens banked: the multi-mode orchestra of bare diagonal vacuum
standing waves EXISTS and converges, but is an arbitrary additive superposition with
NET-NEGATIVE mass, NO preferred/selected composition, and full box-control (scale-free).
The derived, verified TWO selection rules (cross stress survives only for same-l AND
same-w) are the structural reason: the interference channel that could have made the
orchestra more than the sum of its notes is switched OFF for all physically-distinct
modes, and the sole surviving (degenerate) channel only re-sums negative self-energy. A
bare-vacuum multi-mode geon is NOT a particle at O(A^2). Per the orchestra principle this
scopes the DIAGONAL multi-mode sector (not "ensembles fail"); the open routes are the
rotation/off-diagonal companion (Phase-2 B1), the O(A^4)+ / multi-time-harmonic regime
(where non-degenerate cross terms re-enter), and the gated NATIVE-matter step. Nothing
committed changed. Awaiting blind verifier + Charles.

## DRIVER-LEVEL BLIND VERIFIER — 2026-06-18 (agent a80a2ba1293f453ef): STANDS (O(A^2))
Independent re-derivation; hardest scrutiny on the selection rules. ANGLE RULE: initially looked refuted with the PLAIN 2nd derivative (<P2 P4''>=1!=0), but that is not a scalar on S^2 — the correct self-adjoint LAPLACE-BELTRAMI operator gives <P_i Lap P_j> = -l(l+1)<P_iP_j>, vanishing off-diagonal; every covariant bilinear vanishes unless l_i=l_j. Rule SOUND. TIME RULE: DC part nonzero only if w_i=w_j (numerically ~0 for the actual ratios). RECONSTRUCTION: G=r j_l(wr) gives linear vacuum dRicci=0 to 1e-16 (l=2,3,4). ADDITIVITY->NEGATIVITY: share-weighted single-mode sum matches solver to 1-2% (orchestra -0.0206 vs -0.0209); box-control M=-0.00551 R-invariant across R=1,2,4,8. DEGENERATE channel MORE negative (-0.1061). NORMALIZATION-BUG: direct Misner-Sharp integration gives m/norm^2=-0.905 INDEPENDENT of normalization (A=0.1,0.5,2.0 identical; =Phase-1) => correct normalization CANNOT give positive mass; the resid~0.5 positives were genuine non-convergence. Single l=2,3,4 all negative (-0.905,-0.657,-0.096). Box-controlled. SCOPE: O(A^2); O(A^4)/multi-time-harmonic non-degenerate cross terms OPEN. STANDS at O(A^2).
