# P1 -- BLIND ADVERSARIAL VERIFIER report

**Verifier:** Claude (Opus 4.8, 1M) -- independent blind adversarial verifier.
**Date:** 2026-06-19. **Branch:** p1-offdiag-wiring. **Mode:** DATA-BLIND (no
mass/ratio/wall numbers handled). **Constraint honored:** NO full 8-field Newton
solve run. All checks are single Einstein/residual evaluations, greps, sympy
truth, and reasoning. Append-only.

Target: `archive/pre_2026-07-01/p1_offdiag_wiring_results.md`, `p1_residual_general_einstein.py`,
`p1_validate.py`. Reproduction scripts (NEW files): `_verif_hybrid_sweep.py`,
`_verif_b_and_nth.py`.

---

## HEADLINE -- hybrid accuracy vs off-diagonal magnitude A (the load-bearing curve)

Independent test: analytic steep diagonal background (b = p*ln(r/r_seal), p=0.4,
matching the soliton's 1/r-derivative core) + a smooth controllable off-diagonal
warp of magnitude A. TRUTH = exact sympy 4x4 mixed Einstein on the same analytic
metric. Compared the P1 hybrid bracket [einstein_mixed(full)-einstein_mixed(diag)]
to the true delta [G_true(full)-G_true(diag)]. max|err| over the body:

```
   A      | rth err   rps err   thps err | tt(diag-backreac)  rr | |e_rt|max
 0.0e+00  | 2.6e-13   0         0        | 2.8e-12   3.7e-12       | 0
 1.0e-04  | 5.0e-05   3.5e-05   5.1e-05  | 1.7e-06   3.2e-06       | 9.2e-05
 1.0e-03  | 5.0e-04   3.5e-04   5.1e-04  | 1.8e-05   3.2e-05       | 9.2e-04
 1.0e-02  | 5.0e-03   3.5e-03   5.1e-03  | 5.4e-04   5.5e-04       | 9.2e-03
 5.0e-02  | 2.6e-02   1.8e-02   2.6e-02  | 1.4e-02   1.4e-02       | 4.6e-02
 1.0e-01  | 5.3e-02   3.7e-02   5.0e-02  | 5.7e-02   5.6e-02       | 9.2e-02
 2.0e-01  | 1.2e-01   8.3e-02   8.9e-02  | 2.7e-01   2.6e-01       | 1.8e-01
```

READING:
- **A=0: cancellation is machine-exact** (2.6e-13). The bracket vanishes by
  construction -> diagonal sector provably uncorrupted. Confirms b1.
- **The hybrid does NOT blow up as A grows** through A=0.2. The "difference cancels
  the common steep-core error" mechanism is real and holds smoothly. NO catastrophe.
- **BUT it is not "machine-clean ~1e-3".** The off-diagonal-block error scales
  ~LINEARLY in A: err_rth ~= 0.5*A (rel err ~50% of A). The diagonal back-reaction
  error scales ~QUADRATICALLY at small A (1.7e-6 -> 1.8e-5 -> 5.4e-4) then overtakes
  the off-diagonal error by A~0.1-0.2.
- **REGIME OF VALIDITY:** hybrid trustworthy while A is small. The cancellation
  controls the *common* core error but leaves a residual delta-discretization error
  PROPORTIONAL to A. The hybrid is accurate to ~O(A) relative on the off-diagonal
  blocks and ~O(A^2) on the diagonal back-reaction. There is NO regime where it is
  exact at finite off-diagonal -- the doc's "O(1e-3) cancellation" is the value at
  ONE operating amplitude, not a floor. P2 MUST carry: hybrid validity degrades
  linearly with off-diagonal magnitude; large/strong shear (A >~ 0.1) is outside
  the trustworthy regime and needs the genuine pole-stable general Einstein (P5).

CAVEAT on my own test: the warp shape differs from the soliton's; the curve is the
SCALING LAW (error ~ A), which is shape-robust, not a per-point match to the solve.

---

## CLAIM-BY-CLAIM

**(b1) zero-offdiag hybrid==weyl exactly -- STANDS.** Reproduced
max|G_hybrid-G_weyl| = 0.000e+00. Structural: bracket = einstein_mixed(g)-
einstein_mixed(g) = 0 identically when off-diag=0. Not too-clean; it is by
construction and that is honest.

**(b2) live G^r_th, selective G^r_ps -- STANDS.** Reproduced G^r_th(deep)=3.40e-3
(matches doc exactly), G^r_ps(deep)=1.02e-16 (machine-0). Off-diagonal reaches the
field equations; a theta-only warp sources only the (r,theta) block. I added an
e_tp-only stress test: G^th_ps=4.2e-3 (live), G^r_th=3.2e-5 -- selectivity holds
to ~1% cross-leak (minor, spectral coupling; not load-bearing).

**(b3) hybrid vs independent path = 0 -- STANDS but PARTIAL/over-described as
"independent".** The doc/script call b3 an INDEPENDENT path. It is independent only
in the CONTRACTION/INVERSE (spectral einstein_mixed vs CORE.christoffel/einstein +
linalg inverse). BOTH paths use the SAME spectral derivatives (G.d_r/d_th/d_ps) for
dg and dGamma. So b3 does NOT test the differentiation discretization -- the part
that actually carries the conditioning error. b3=0 is real (contraction algebra is
correct) but does not establish accuracy vs truth. The genuinely independent truth
check is my sympy sweep above. NET: b3 stands as an algebra cross-check; do not read
it as "the hybrid matches true Einstein."

**Wiring is genuine general-Einstein (off-diag back-reacts on diagonal rows) --
STANDS.** My sweep's tt/rr columns are the diagonal-block back-reaction from the
bracket; they are nonzero and grow with A (1.7e-6 -> 0.27). Off-diagonals genuinely
feed the diagonal field equations. NOT "diagonal in disguise."

**(a) off-diag free to grow, not pinned -- STANDS.** Grep + code read: off-diag BC
rows pin e_rt/e_rp/e_tp = 0 only at core[0] and seal[-1]; body interior is
unconstrained (only its Einstein row). b2/e_tp tests show e_rp,e_tp CAN be nonzero
geometrically, so their staying ~1e-10 in the solve is a solve outcome, not a pin.
(Could not re-run the solve per constraint; the freedom is verified structurally.)

**e_rt is a coarse-Nth artifact -- PARTIAL / NOT fully supported by what is
checkable.** I tested the two sub-claims:
  (i) Wiring does not spuriously make off-diag G on a truly round field: CONFIRMED.
      Pristine radial seed embedded in 3-D gives G^r_th(deep) = 8e-18..9e-17 at
      Nth=6,8,12,16 (machine-0 at all Nth). Good.
  (ii) The G^r_th that e_rt absorbs SHRINKS with Nth (the artifact claim): NOT
      supported as stated. With a RESOLVED l=2 angular variation (fixed amp 1e-3)
      imposed on diagonal b, G^r_th(deep) is FLAT vs Nth: 1.25e-3 (Nth=6) ->
      1.25e-3 (Nth=20). So G^r_th is a GENUINE, Nth-stable geometric response to
      angular variation in the diagonal fields -- NOT a discretization artifact of
      the Einstein operator. The doc's artifact claim therefore rests ENTIRELY on
      the unverified premise that the CONVERGED SOLVE's angular spread in a,b,c,d is
      itself a coarse-Nth artifact that tightens with Nth. That premise needs the
      higher-Nth round re-solve the doc already flags -- I could NOT check it (no
      solve allowed). HONEST STATUS: e_rt~1.3e-2 may be the off-diagonal correctly
      absorbing a REAL (Nth-stable) G^r_th sourced by a (possibly artifactual,
      possibly physical) angular spread. The "it's just a grid artifact" framing is
      not yet earned; it is plausible but UNVERIFIED. Mildly OVER-CLAIMED.

**(c) divT O(0.1) in r,theta is the gate's own Nth error; matter EOM at floor --
PLAUSIBLE, not independently reverified.** The attribution is internally consistent:
the matter EL residual (the equation actually solved) is the floor quantity; the
divT_identity takes extra spectral theta-derivatives of Christoffel*T, which at
Nth=6 carry the same Nth-limited error my G^r_th-vs-Nth tests show the operator has.
The ps-channel being clean (8e-11, Fourier accurate at Nps=8) while r,theta are
O(0.1) (GL Nth=6) is the expected signature. Could not re-run divT at higher Nth
without the solve. Attribution accepted as plausible, flagged not-reverified.

**THE P2-INHERITANCE GAP (matter EL on diagonal metric only) -- REAL, UNDERCUTS the
OBSERVATION partially.** matter_el_3d and the stress are built on g_full in the
residual (stress_tensor sees off-diagonals via ginv), BUT the matter EQUATION OF
MOTION (matter_el_3d) is varied on the DIAGONAL warps a,b,c,d only -- it does not
see e_rt/e_rp/e_tp. CONSEQUENCE for the OBSERVATION "static matter doesn't source
shear": the matter's own field configuration cannot RESPOND to the off-diagonals, so
the test shows that the off-diagonal Einstein rows + the (diagonal-fed) stress do not
DRIVE rp,tp -- it does NOT show that a fully self-consistent matter (one that sees
the shear) would leave them zero. The observation is correctly SCOPED in the doc
(flagged as P2's job) but the headline "static native matter does not drive the
shear sector" is stronger than what is shown. What IS shown: with matter blind to
off-diagonals, an imposed l=2 matter shape does not source rp,tp. What is NOT shown:
that self-consistent non-round matter leaves them zero. P2 must re-take this
observation once the EL sees the full metric.

**DISCIPLINE GREP -- CLEAN.** Only `m*PI` in code is line 169, the explicitly
labelled `node_core=False` negative-control branch; default deg1 path uses Th[0]-PI
(node value) + Th[-1]-0. No B=1/A tie (a,b independent; max|a+b| witness reported
nonzero). No dropped/added term, no kept linearization (the EXP_CLAMP in build_metric
is an overflow guard, not a linearization). a=-1 (P3) and time row zeroed (P4) are
the only declared freezes. CLEAN.

**OVER/UNDER-CLAIM on "genuinely general-Einstein".** HONEST overall. The doc
repeatedly and prominently flags the hybrid as an engineering choice, not a drop-in,
and states the only thing the analytic Weyl supplies is the zero-off-diagonal
backbone value. That is accurate. The two places it leans slightly hot: (1) implying
the off-diagonal accuracy floor is ~1e-3 (it is ~O(A), shown above); (2) the
e_rt-as-pure-artifact framing (unverified premise, above). Neither is a smuggled
mechanism; both are resolution/regime caveats.

---

## NET VERDICT: P1 STANDS (with caveats P2 must carry)

The off-diagonals are GENUINELY wired into the field equations (live in their own
rows AND back-reacting on the diagonal blocks -- verified vs exact sympy truth), the
hybrid reduces machine-exactly to the analytic Weyl at zero off-diagonal (diagonal
sector + round soliton provably uncorrupted), discipline is clean (no Skyrme-as-solve,
no B=1/A, no linearization, declared freezes only), and the off-diagonals are free
to grow (not pinned). The wiring is real and the validation gates b1/b2 reproduce
exactly.

CAVEATS P2 MUST CARRY:
1. **Hybrid regime of validity is FINITE, not exact.** Off-diagonal-block error
   ~0.5*A (linear), diagonal back-reaction ~O(A^2). Trustworthy for small shear;
   degrades smoothly; outside the trustworthy regime by A >~ 0.1. There is no
   machine-precision floor at finite off-diagonal. Strong-shear phases need P5's
   genuine pole-stable general Einstein, not the difference hybrid.
2. **Matter-EL gap.** The matter EOM does not see the off-diagonals, so the
   OBSERVATION "static matter does not drive the shear sector" is scoped to
   off-diagonal-blind matter. Must be re-taken in P2 with the full-metric EL.
3. **e_rt-as-coarse-Nth-artifact is UNVERIFIED.** G^r_th itself is Nth-stable (real
   geometric response); the artifact claim depends on the converged angular spread
   shrinking with Nth, which needs the flagged higher-Nth round re-solve. Until then,
   do not bank "round soliton has exactly zero physical off-diagonal content."
4. **b3 "independent" is contraction-only** (shares spectral derivatives); the real
   independent accuracy check is the sympy-truth scaling law here.

COULD NOT CHECK (no-solve constraint, stated explicitly): the actual converged
round/l=2 8-field solutions, the higher-Nth shrinkage of the converged angular
spread, and divT at higher Nth. None of these change the wiring-correctness verdict;
they bear on caveats 2 and 3.
