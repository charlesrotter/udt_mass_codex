# P4 stability slice — exact derivation record (second variation about the banked massive solutions)

Date: 2026-07-31. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this run).
Script: `derive_stability_slice.py` (exact SymPy; no floats, no numeric eigensolvers, no GPU;
deterministic). Check counts and the substantive/guard split are stamped at the end of this
record after the final run. Outputs: `stability_results.json`, `DERIVATION_STDOUT.txt`,
`STABILITY_LEDGER.tsv`, `DECISION_SURFACE_UPDATE.md`.

**Standing scope stamps (travel with every statement):** jet <= 2, registered stationary
one-parameter presentation (fields (phi,f,bh)), registered positive triangular chart, READY
bin, enumerated pairing branches carried with a_F SYMBOLIC (P1-4D a_F=2lambda, P1-triad
a_F=1+2lambda, P2 a_F=0), quadratic class (fiberwise-quadratic p-unmixed; diagonal G_fh
computed, general G by constant congruence — Category-A, banked practice), BASE moduli for
S-i (dlambda constant; k_mod/k10/C retained), fields-census (BR-M) moduli for S-ii
(dlambda(x), dk_mod(x) mirror-odd — banked Route-P forcing), mirror parity eps_phi=-1
DEFINITIONAL (canon), f/bh parities SUPPLIED (both directions carried), wall structure = the
banked boundary-action-gate census (first germs pinned/forced per posture; SECOND-and-higher
germs unpinned), N=2 wall layer (N=4 typed), no dynamics (NV members UNDEFINED at this
layer), no numeric eigensolvers (exact operator solutions + named Category-A comparison
steps only). NOTHING adopted; the prereg §4 ceiling governs every verdict.

**Perturbation-space provenance (TS-1; F-S2 both directions policed):** all fields varied
JOINTLY (depth v_p, angular v_f/v_h, live moduli per census branch) — no fixed-background
Hessian anywhere; every constraint on the admissible space is a BANKED census fact (parity
trace kills; supplied f/bh parities; seam matching; germ pins), none invented.

---
## Stage A — S-i: the joint second variation and its exact operator structure (SA1-SA9, SC1-SC5)

**TS-2 (operator form, exact).** About any quadratic-class massive member (w = Ax^2+w1x+w0,
A = a_F^2 E0/(2g_p), disc<0 definite class, f'=(G^{-1}c)_f/w), the joint second variation over
(v_p, v_f, v_h, dlambda=mu) assembles exactly (SA1; first variation vanishes on-shell and on
{I_p=0} — SA2/SA3, the banked tie recomputed). Structure theorems, all zero-residual:
- **fh completion (SA5):** the angular block completes to a perfect square minus
  a_F^2*sigma*v_p^2/w (sigma = c^T G^{-1} c): the ONLY destabilizing channel is the
  f/h-momentum coupling; **pure depth cannot destabilize** (SA6: the depth cross+mass terms
  are an exact total derivative, so the pure-p form is boundary + int g_p w v'^2 >= 0).
- **Reduced Sturm-Liouville operator** L v = -g_p(w v')' - a_F^2 sigma v/w with EXACT solution
  basis v1 = w'/w (translation-descended) and v2 = E0 - sigma/w (energy-modulus direction),
  Wronskian g_p w W(v1,v2) = E0^2 a_F^2 (SA7-SA9): every spectral count below is decided by
  closed-form zero-locations of (v1, v2) combinations — no numeric eigensolver anywhere.
- **lambda sector (SC3):** the mu^2 diagonal is C = a_F'^2 E0 int pbar^2 > 0 on nonconstant
  massive members; C = 0 exactly at E0 = 0 (the tie's vacuity reproduced).
- **B identity (SC4/SC5, exact pointwise cancellation):** the lambda-field cross form on the
  (v2, matched-fh) pair reduces POINTWISE to a_F'(E0 v2 + a_F E0^2 pbar), so
  B = a_F' E0 int v2 dx on {I_p=0}; with crease normalization (sigma = E0) the convexity bound
  log t <= t-1 gives int v2 < 0 STRICT on nonconstant members [Category-A named]. (Structure
  fact; its instability implication needs kernel realization — posture-dependent, Stage B.)

**TS-4 (controls, F-S5).** The E0=0 constants member: the joint form is exactly
W0(g_p v_p'^2 + g_f v_f'^2 + g_h v_h'^2) — PSD with kernel = all 0-jet shifts + the ENTIRE
moduli sector (mu flat: the tie vacuous at E0=0) = precisely the banked flat directions
(SC1/SC2). **CONTROL PASS** (the run is valid per F-S5). Triad-locked control: Stage C, SD4.

**Zero-mode calibration (TS-3).** Known moduli reappear exactly: f/h shifts (density touches
only v'), k_mod/k10/C (absent from the form — vacuous rows), x-translation (Lv1=0; admissible
only where traces allow — crease kills it, an honest posture fact), lambda at E0=0.

**Posture setup facts (perturbation-space stage, exact):**
- **Double-crease (pure quotient posture): the massive locus is EMPTY** (SB2): w(+-l)=1 at
  both walls forces w1=0 and w-1 = A(x^2-l^2) sign-definite inside, so I_p != 0 for every
  nonconstant member. (No contradiction with the period gate: its quotient-UNTOUCHED row is
  about periods; this is a wall-trace fact. F-S6 sweep clean.) **EMPTY is now TOTAL over
  both E0 signs (verifier-completed, credited): the E0<0 gap is closed — disc<0 with w>0
  forces A>0, so the definite class has no E0<0 members (VERIFIER_INDEPENDENT_CHECK.py).** Single-cell cyclic: EMPTY
  (banked C2d, cited). So every massive S-i realization has at most ONE crease end — exactly
  the banked mixed crease|glue chain shape. The single-cell-with-crease and the chain cell
  are the same analysis object (Stage B).
## Stage B — S-i on the certified mixed crease|glue chain (SB1-SB17)

Arena: the period-gate-certified crease-pinned branch (ell=1 CHOSE-normalized, banked C6b),
s = sqrt(2A) in (1,3) covering the certified massive roots A*; g_p=1 scale (the form scales
by g_p>0: sign structure invariant); a_F symbolic (both P1 branches).

- **Crease end (SB1):** the crease conditions are exactly {w(crease)=1, sigma=E0*w(crease)},
  so v2 VANISHES AT THE CREASE automatically; its second zero x2 = 2/s - 1 is STRICTLY
  interior for every s>1 and v2 is sign-definite between (SB3/SB4); v2(1) != 0.
- **Free-fh-data branch (supplied f/bh wall data free) x germ-Hessian-flat realized wall
  response (the banked witness responses B=0 and (q/2)rho have zero second germ):**
  the reduced Dirichlet problem for L has EXACTLY ONE negative direction — v2 is a
  sign-definite Dirichlet zero mode of [-1,x2], strict domain monotonicity + oscillation
  [Category-A named] give n- = 1 (SB6); the free-p-trace (Robin) space adds none (exact
  harmonic-extension split, cross term vanishes, boundary Schur scalar positive — SB7).
  **VERDICT: UNSTABLE, index exactly 1 in the reduced sector (OS-2 on this branch-pair);
  the negative mode necessarily carries angular flux through the wall (nonzero v_f trace)
  — a wall-physical mode in the banked box-control sense.** On the JOINT space (fields+mu)
  the certified statement is index >= 1 exact; exactly-1 pending the lambda-Schur sign
  (same dilogarithmic obstruction as the odd-pinned branch; the verifier's joint Galerkin
  hunt at s* supports exactly-1 — corroboration, not banked). UNSTABLE is unconditional.
- **Odd-pinned-fh branch (zero angular traces):** eliminating the zero-trace fh sector is an
  EXACT rank-one penalty Q_p + (a_F^2 sigma/J)(int v_p/w)^2, J = int dx/w (SB12). The
  resolvent computations close in elementary closed form (SB8-SB10, SB14): the Dirichlet
  criterion is <g, L_D^{-1}g> = -J/s^2 - 2/(s^2(s-1)) and the crossing scalar is
  1 + tau<g,phi> = -2/(J(s-1)) < 0 MANIFESTLY — J cancels exactly, so the sign is uniform
  over the whole branch INCLUDING the transcendental massive roots. Rank-one crossing rule
  toy-verified exactly (SB11) AND properly verified by the blind verifier beyond the toy
  (8 random exact 5x5 matrices + the analytic interlacing argument — caveat retired,
  credited check). Free-p-trace version: crossing scalar
  -2(4s^2-3s+1)/(J(2s-1)w(1)) < 0 likewise (SB14). **VERDICT: the odd-parity f/bh pin
  EXACTLY ABSORBS the unique negative direction — the germ-independent zero-trace core is
  POSITIVE.** Remaining sectors (free wall-germ curvature; the lambda-Schur block, whose
  exact evaluation is dilogarithmic at the transcendental root): OS-5 UNDECIDABLE-AT-THIS-
  LAYER with the obstruction named (SB15).
- **Germ-curvature activation (structure theorem, SB16):** the wall response's SECOND germ —
  first-variation-INERT (banked) — ACTIVATES in the second variation and is UNPINNED by
  every banked requirement. Hence (i) NO stability certificate is possible at any
  trace-active posture at this layer; (ii) germ data can never veto a zero-trace negative
  direction; (iii) under the banked germ-Hessian-flat witness responses the verdicts above
  are complete. (The delta^2 analog of the banked N=4 activation.)
- **Chain inheritance (SB17):** any mixed-posture whole containing a certified massive
  crease cell inherits the cell's zero-trace-core verdicts by subspace monotonicity.

## Stage C — S-ii fields-census lock-emergence class + triad control (SD1-SD5)

- **Assembly (SD1, exact):** about the P1-4D landing (p==0, lambda==0 emerged, f/h affine,
  W==1) the joint form is g_p v_p'^2 + g_f v_f'^2 + g_h v_h'^2 + 4E0 v_lam v_p — the
  lambda(x)-depth cross term is the ONLY moduli-field coupling and the lambda diagonal
  VANISHES identically on the no-m-jet class.
- **Verdict (SD2, exact witness):** v_p = sin(pi x/l), v_lam = -t sin(pi x/l) (banked-
  admissible: exactly odd about both walls; ALL traces zero => germ-independent) gives
  Q = -g_p pi^2/l < 0 at t = g_p pi^2/(2E0 l^2). **Every E0 != 0 member of the no-m-jet
  landing class is a SADDLE — UNSTABLE (OS-2), unconditional on the banked space.**
- **Jet-quadratic sub-class (SD3, exact dichotomy):** with density term c_m lam'^2/2 the
  Dirichlet mode split gives per-mode blocks [[g_p k_n^2, 2E0],[2E0, c_m k_n^2]]:
  **STABLE-in-this-sector iff 64 E0^2 l^4 <= g_p c_m pi^4** — an exact threshold tying
  member energy to cell size and jet stiffness. OS-4 (both regimes populated).
- **Triad-locked control (SD4):** PSD with kernel exactly {constants} + arbitrary odd
  v_lam(x), v_kmod(x) — the banked infinite-dimensional massless-stratum free directions
  reappear exactly. **CONTROL PASS (F-S5).**
- **Typing (SD5):** NV UNDEFINED-AT-LAYER (F-S4); S-ii AM-1/AM-2/p0==0 conditionalities
  travel; N=4, corners, resonance, 4th-order, carriers, time-live untouched.
## Outcome and falsifier record (derivation-side)

**Outcome class: OS-4 (mixed, per candidate x posture x supplied-parity branch), containing
two OS-2 legs, one OS-5 leg, an EMPTY-DOMAIN map fact, and passing controls.** Script:
36/36 checks, exit 0 = 30 SUBSTANTIVE zero-residual/exact-condition checks + 6 GUARDS
(citation/typing/verdict-assembly rows, labeled in-script and in the JSON; SB12 relabeled
SUBSTANTIVE->GUARD per verifier amendment A2 — its coded condition is arithmetic-true-by-
construction; the underlying minimization was independently verified by the verifier),
deterministic (rerun byte-identical, verified), single CPU process, well under budget. FULL DECLARED
SCOPE at the banked layer — no scope-ladder reduction taken; the OS-5 remainders are
exactness obstructions (named), not throughput limits.

- **F-S1 (steering):** the tempting outcome was STABLE; the landed headline is mostly
  UNSTABLE — stated with witnesses and exact counts, not dramatized: the odd-pinned branch's
  POSITIVE core (the absorption theorem) and the S-ii stable jet-regime are recorded with
  equal precision. No step chosen for its verdict direction; the branch split falls out of
  the banked supplied-parity fork.
- **F-S2 (over/under-counting):** no fixed-background Hessian anywhere (fields + moduli
  jointly; the lambda block computed, not frozen); no invented constraints — every
  admissible-space cut is a banked census fact (parity trace kills, supplied parities, seam
  matching, germ pins); the fh-elimination penalty is DERIVED (exact rank-one), not imposed.
- **F-S3 (stamps):** every verdict row carries candidate/posture/census/pairing/chain-vs-
  single/jet-layer/perturbation-space stamps (ledger columns; standing block).
- **F-S4 (smuggle):** no dynamics (NV UNDEFINED-AT-LAYER); no posture/census/pairing
  adopted; hopfion results not used (method-shape only: joint constrained perturbation,
  wall-mode classification).
- **F-S5 (controls):** BOTH controls reproduce the banked flat-direction structure exactly
  (SC1/SC2, SD4). Run valid.
- **F-S6 (bank contradiction):** none found. The double-crease EMPTY fact refines (does not
  contradict) the period gate's quotient-UNTOUCHED row (periods vs wall traces); the tie,
  atlas, crease conditions, witness responses, and Slice-2b identities are recomputed
  zero-residual where used.
- **F-S7 (symbolic failure):** none; 36/36, exit 0. Two in-run check-coding defects were
  found and fixed during construction (an over-counted cross term in the SA1 hand target; a
  hand-algebra slip in the SB10 closed form caught by the independent assembly path — the
  criterion's manifest NEGATIVITY and the verdict were unaffected — the corrected closed
  form was confirmed against an independent direct assembly); this honesty note is the
  record of both; no check condition was weakened.

**Limits that travel:** (i) quadratic class throughout (diagonal G computed; general G by
constant congruence, Category-A); (ii) certified-branch results are at the banked ell=1
CHOSE normalization, s in (1,3) (the banked C6b interval); general {I_p=0} members carry
the closed-form criterion, not a verdict (R07); (iii) named Category-A steps: Picard/
regularity, log t <= t-1 convexity, integral positivity, strict domain monotonicity +
Sturm oscillation (prereg-sanctioned), rank-one crossing rule (toy-verified in-script;
PROPERLY verified by the blind verifier — 8 random exact 5x5 + analytic interlacing —
the toy-only caveat is RETIRED, credited check), Parseval; (iv) germ-carrying postures: verdicts complete only under germ-Hessian-flat
realized wall responses (the banked witnesses); free second-germ data makes stability
uncertifiable at this layer (SB16) — an N=2-layer fact, N=4 typed; (v) the lambda-Schur
block on the odd-pinned branch is the one sign question exactness could not close
(dilogarithmic integrals at transcendental A*) — OS-5, obstruction named; (vi) NV members,
resonance cells, corners, carriers, time-live: untouched; (vii) blind verifier pass:
DELIVERED — PASS-WITH-REQUIRED-AMENDMENTS (`VERIFIER_REPORT.md`; independent script
`VERIFIER_INDEPENDENT_CHECK.py`, exit 0), both amendments bookkeeping-grade and applied
(A1 reduced-sector scope propagation; A2 SB12 SUBSTANTIVE->GUARD; see
`CORRECTION_LAYER.md`); post-amendment rerun 36/36, exit 0 = 30+6, deterministic.
