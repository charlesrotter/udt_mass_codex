> **CONDITIONS-CHANGED (2026-07-06 pre-native-era census) — NOT current native-micro canon; premise-scoped.**
> Companion verifier to the everything-on P2/P3/P4 arc (frame B, a(φ)=−1 / G=kap8·T), which is CONDITIONS-CHANGED
> (2026-07-06). Verifies DATA-BLIND machinery, banked no native-micro physics. Superseded frame; the 2026-07-01 native
> constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦) is the current frame. See
> pre_native_era_census.md + NEGATIVES_REGISTRY.

# P2 -- BLIND ADVERSARIAL VERIFIER report

**Verifier:** independent blind adversarial agent (Claude Opus 4.8 1M),
id `udt-verifier-p2-1781957826`.  **Date:** 2026-06-20.  **Branch:**
p2-matter-fullmetric (head 20401bf).  **DATA-BLIND** (no mass/ratio/wall
numbers loaded or computed).  **Append-never-edit.  NOT canon.**

Mandate: try to BREAK P2, then rule.  Did NOT run the full 8-field Newton
(deferred to P5 by design).  All checks below are independent re-runs / new
scripts / greps, not a re-read of the doc's own numbers.

---

## CLAIM-BY-CLAIM

### 1. P1-gap closure (the matter EL sees the off-diagonals) -- **STANDS**

- Reproduced `p2_divT_fd_gate.py`: autograd EL == FD-of-action on a fully
  non-diagonal metric (e_rt,e_rp,e_tp live), max rel-err **4.40e-6** (matches
  doc exactly).
- HONEST FRAMING NOTE: autograd-EL == FD-of-the-SAME-action is a
  self-consistency check (autograd differentiates the action it is handed);
  it is NOT independent physics by itself.  The doc states this.  The
  SUBSTANTIVE claim (off-diagonal dependence) is what matters, and I
  confirmed it INDEPENDENTLY:
  - Built my own off-diagonal amplitude scan A = 0 .. 0.16 (my own mix of
    the three off-diagonals).  Result: |EL_off - EL_dia|_max = **0.0 EXACTLY
    at A=0** and scales **PERFECTLY LINEARLY** (ratio dEL/A = 0.41188 constant
    across 5 octaves).  => the EL reduces to the diagonal EL as shear->0 and
    couples to the off-diagonals at FIRST ORDER.  Not vestigial, not circular.
- VERDICT: the P1 matter-EL/off-diagonal gap is **genuinely closed.**

### 2. Covariant divT = gate noise, not EL error -- **STANDS**

- Independently re-ran the COMMITTED (known-good S^3) path's off-round divT
  identity (committed `covariant_divT_field` + committed analytic EL +
  committed round_seed): rel-err = **1.00 @ Nr=64, 0.99 @ Nr=96**
  (L2(divT)=1e-2 >> L2(rhs)=6e-4, no cancellation).  The known-good path
  ALSO fails the SAME gate at the SAME resolution class => the failure is the
  covariant operator's own spectral noise, NOT a P2-specific EL defect.
- (Doc cites ~0.8 @ Nr=160; I get ~1.0 at lower Nr -- same regime, operator
  noise-dominated; the identity is not met at any tractable grid.)
- => the FD-variational gate (claim 1) is the correct substitute correctness
  check.  EL correctness does NOT rest only on the autograd self-check; it
  rests on the off-diagonal-dependence demonstration (claim 1, independent).

### 3. e_rt GENUINE -- **STANDS (numerically); INTERPRETATION CORRECTED below**

- Reproduced `p2c_shear_observe.py`: resE_rth Nth 8->28 = 0.1744 -> 0.1737
  (drift 0.4%), T^r_th = 3.47 rock-stable.  (a) Nth-stable: CONFIRMED.
- (b)/(c) sourced by theta-structure: independently confirmed with my own
  field scan (see interpretation).  T^r_th = 0 (machine) for theta-flat F.

### 4. e_rp, e_tp genuinely zero -- **STANDS**

- resE_rps ~ 3e-17, resE_thps ~ 2e-15, Nth-stable (machine floor).  Static
  native matter sources NO (r,psi)/(theta,psi) shear.  Confirmed by re-run.

### 5. Polar-singularity of pure-radial F(r) -- **STANDS (genuine, not a bug)**

- Reproduced `p2_validate_ab.py`: F=F(r) gives rho axis/equ ratio 13.9 AND
  breaks T^t_t=T^r_r (|diff|=1.6e-1); F=theta gives ratio 0.8 and
  T^t_t=T^r_r EXACTLY (0.0).
- KEY INDEPENDENT TEST (theta-resolution): for pure-radial F(r), rho at the
  pole DIVERGES with Nth -- pole rho 0.15->0.49->1.04->1.81 and axis/equ
  ratio 4.3->13.9->29.7->51.7 across Nth 8->32 (rho~1/sin^2 theta on axis).
  For axis-regular F=theta+h sin(theta), rho is Nth-STABLE (ratio 0.84 flat).
  => the polar singularity is REAL and resolution-divergent, NOT a fixed-grid
  artifact.  "Needs F(r,theta)" is correct.

### 6. Discipline -- **STANDS**

- Unit field |n|^2-1 = 4.4e-16 (machine).  Native cross-L4 == MAT L4 = 1.1e-13.
- Grep: no `m*pi` solved BC anywhere (only labelled comments + the m=1
  charge-1 winding; the negative-control "free" node is value-free d_r F=0).
- B=1/A NOT smuggled: `b=-a` appears ONLY in the two NON-solving diagnostic
  scripts (`p2_divT_fd_gate.py`, `p2c_shear_observe.py`), each explicitly
  flagged as a fixed TEST background.  Both ACTUAL solvers
  (`p2_round_s2_solver.py`, `p2_residual_fullmetric.py`) carry a,b as
  INDEPENDENT unknowns (a(seal)=0 gauge + b(core)=-p depth-dial only).
  CONFIRMED diagnostic, not a residual tie.
- Only declared freezes: a=-1 (P3), time row zeroed (P4).  Data-blind: yes.

### 7. Is "PARTIAL" honest? -- **YES**

- The two declared closures (3-D EL on the unit S^2; off-diagonal coupling)
  are genuinely DONE and independently verified.  The coupled round anchor is
  legitimately deferred (the autograd-EL column-FD Jacobian + no-cache
  allocator is the named throughput wall; I did not and need not run it).
  This is a real throughput deferral, NOT an inconclusive dressed as done.

---

## HEADLINE RULINGS

(a) **P1 gap genuinely closed?**  YES.  Off-diagonal dependence is real,
    first-order, ->0 as shear->0 (independent linear scan, ratio constant to
    5 sig figs).

(b) **e_rt genuine?**  YES numerically -- Nth-converged, sourced by the
    field's deviation from roundness, machine-zero for the round case.

(c) **INTERPRETATION -- is the "non-round native object" a real physics claim
    or just the hedgehog's standard angular profile?**  MIXED -- one part
    real, one part OVER-CLAIMED:

    - The polar-singularity finding (claim 5) is just STANDARD axis-regularity
      of an m=1 winding field (sinF must ->0 at the poles).  The doc itself
      uses F=theta as the axis-regular reference, so "needs F(r,theta)" is the
      textbook winding requirement, NOT a deep new asymmetry.  F=theta alone
      is axis-regular AND round (T^t_t=T^r_r exact).

    - CRUCIAL CORRECTION to claim 3's wording: the doc says T^r_th "=0 EXACTLY
      when F has no theta-dependence."  I find F=theta -- which DOES depend on
      theta -- gives T^r_th = **1.2e-13 (machine-ZERO)**.  The true
      discriminant is NOT "depends on theta" but "DEVIATES FROM THE ROUND
      PROFILE theta": T^r_th = 0 for both F(r) and F=theta, and grows
      (0 -> 1.71 -> 3.47 -> 7.37) with the amplitude s of the deviation
      h(r)sin(theta).  So the genuine T^r_th shear is sourced by a REAL
      departure from roundness -- but that departure (h=0.6 sin theta) was
      IMPOSED by the driver in the OBSERVE config, NOT selected by the metric.

    - RULING: e_rt responding to a genuine non-round matter config is REAL and
      correctly demonstrated.  But "the matter is intrinsically non-round in
      theta" (Sec 6, What-P3-inherits) is an OVER-CLAIM at this stage: the
      minimal axis-regular native deg-1 object is F=theta, which is ROUND.
      Whether the SOLVED object is non-round is exactly the coupled-solve
      question deferred to P5 -- it is not established here.  P3 should inherit
      "carry F(r,theta) for axis-regularity," NOT "the object is non-round."

---

## NET

**P2-PARTIAL STANDS.**  The two declared closures (3-D unit-S^2 matter EL;
genuine first-order off-diagonal coupling) are independently verified and
clean (no smuggled B=1/A, no Skyrme ladder, data-blind).  The shear
observation is reproduced and correct.  The covariant-divT-as-gate-noise
attribution is independently confirmed against the committed path.

**Flag (interpretation, non-blocking):** the "intrinsically non-round
object" reading over-reaches -- the axis-regularity / polar-singularity
finding is standard winding regularity (F=theta is round and regular), and
the T^r_th response is sourced by a driver-IMPOSED deviation from roundness,
not a metric-selected one.  Claim-3 wording ("=0 when F has no
theta-dependence") should read "=0 when F does not DEVIATE from the round
profile theta" (F=theta itself gives machine-zero T^r_th).

**What P3 correctly inherits:** a native S^2 unit-3-vector matter sector
whose stress AND autograd EL both live on, and couple to, the full
off-diagonal metric (FD-gate proven, first-order coupling verified); the
requirement that the native deg-1 profile be F(r,theta) for axis-regularity
(NOT a claim that the solved object is non-round); and the P5 need for a
research-grade driver for the coupled autograd-EL solve.  P3 may turn on
a(phi) in this verified matter coupling.
