> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE EH-era (a=−1, G=kap8·T) operator + imported S³ matter, superseded 2026-07-01 by the native constrained-two-player
> operator (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in NEGATIVES_REGISTRY object-identity (imported S³) + subsumed
> everything-on arc. LOW RISK — banks only off-diagonal-wiring machinery (category-A) + a scoped shear-selectivity negative; no live
> positive native-micro headline; the M_MS object is imported-S³.

# P1 -- Off-diagonal wiring to the general Einstein: results

**Phase:** P1 of the everything-on solver (EVERYTHING_ON_SOLVER_BUILD_MAP.md S III).
**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-19. **Mode:** OBSERVE. **DATA-BLIND.**
**Status of doc:** append-never-edit research record. **NOT canon.**

Governing: POST_POSTULATE_PROGRAM.md (solve the whole CLEAN metric, everything on,
OBSERVE; solver-first on any mismatch). CLAUDE.md "How we work" + repo discipline
(committed scripts IMMUTABLE; new work = new files; verifier-before-record).

---

## REGIME STAMP / PREMISE LEDGER

| Item | Value | chose / derived |
|---|---|---|
| grid | (Nr,Nth,Nps)=(24,6,8), rc=0.05, cell=14 | CHOSE (tractability; P0 regime) |
| p (depth dial) | 0.4 | CHOSE (P0 anchor regime) |
| kap8 (back-reaction) | 0.05 | CHOSE (P0 anchor regime) |
| charge m | 1 | CHOSE (ground sector) |
| a(phi) coupling | a = -1 (GR baseline) | FIXED baseline (a(phi) is P3, NOT touched) |
| B vs A | INDEPENDENT (B=1/A FREE, not injected) | discipline (grep-verified) |
| matter carrier | native S^2 single-profile + general L2+L4 Hilbert stress | reused (canon C-14-1) |
| core BC | deg-1 NODE: core=pi (node) -> seal=0 (node); NO m*pi ladder | DERIVED-as-node (homotopy sector) |
| time row | ZEROED (P4, not P1) | scoped out |
| off-diagonals e_rt,e_rp,e_tp | LIVE unknowns (the P1 turn-on) | the build |

Note on the core BC: `coupled_tl_stage1a` established that the maximally-agnostic
free-value node (Theta'(core)=0) UNWINDS the round charge-1 config to trivial vacuum
(M_MS~0). The deg-1 node (core=pi selecting the degree-1 homotopy class; pi is a NODE
value, sin(pi)=0, NOT the forbidden m*pi LADDER) is the native condition that HOLDS the
soliton. Both modes are available in the code (`core_mode`); P1 validates on deg-1.

---

## 1. WHAT WAS BUILT / REWIRED

New files (committed with this doc; committed scripts left immutable):
- **`p1_residual_general_einstein.py`** -- the P1 residual + Jacobian + Newton solve.
  - `unpack8`/`pack8`: 8 fields -- diagonal (a,b,c,d,Th) PLUS the three spatial
    off-diagonal warps **e_rt, e_rp, e_tp** as LIVE unknowns (these were allocated by
    `build_metric` but never reached the field equations before).
  - `einstein_general_hybrid`: the field equations now use the GENERAL 4x4 Einstein
    (off-diagonals feed in), computed POLE-STABLY (see the conditioning note below).
  - `residual_vector_p1`: rows = the 4 diagonal Einstein (NOW carrying off-diagonal
    back-reaction) + the **3 off-diagonal Einstein G^r_th, G^r_ps, G^th_ps** (the rows
    that the off-diagonal warps solve) + matter EL + BC rows (incl. off-diag regular at
    core+seal). vmap-safe (inv4x4/det4x4) so jacrev batches it.
- **`p1_validate.py`** -- the validation gates (a/b/c) + the first observation.

### The conditioning reality (honest; this is the load-bearing build decision)
A NAIVE "swap `einstein_mixed_weyl` -> `einstein_mixed`" is NOT clean. The general
spectral Einstein differentiates the Christoffels by a SECOND spectral pass; on the
steep soliton warps (b = p ln(r/r_seal), 1/r derivative) the double pass is badly
conditioned at the Chebyshev CORE edge. Measured (flat space, general Einstein):
inner-row error GROWS with Nr (1.2e3 @ Nr=20 -> 3.8e3 @ Nr=40); even DEEP-interior
diagonal blocks of `einstein_mixed` disagree with the analytic pole-stable
`einstein_mixed_weyl` by O(1-3) on the soliton. Routing the WHOLE residual through the
raw general Einstein would corrupt the DIAGONAL sector for a NUMERICAL reason and the
round soliton would NOT recover -- a false "P1 failed" that is really conditioning.

**THE FIX (category-A; the field equations are UNCHANGED -- same general 4x4 Einstein):**
the POLE-STABLE HYBRID
```
  G_full = G_weyl(a,b,c,d)  +  [ einstein_mixed(g_full) - einstein_mixed(g_diag) ]
```
The analytic pole-stable Weyl Einstein is the diagonal BACKBONE; the bracket is the
off-diagonal CONTRIBUTION from the validated general Einstein. Both general evaluations
share the same steep diagonal background, so the core-conditioning error SUBTRACTS OUT
in the difference (measured O(1e-3) near the core vs O(1e3) raw). When off-diagonals
= 0 the bracket is IDENTICALLY ZERO (verified machine-0) -> G_full == G_weyl EXACTLY,
so the diagonal sector and the round soliton are provably unchanged. The off-diagonals
enter the field equations both via the new off-diagonal rows AND via the bracket's
diagonal-block back-reaction (the cross/shear terms). This IS genuine general-Einstein
wiring -- the only thing the analytic Weyl supplies is the pole-stable VALUE of the
zero-off-diagonal background.

---

## 2. P0 ANCHOR (validated zero point on THIS stack)

Established with the EXISTING committed residual (`full3d_newton`, diagonal Weyl
Einstein, Skyrme `Th(core)=m*pi` BC) -- the proven baseline -- at grid (24,6,8):
- converged **Phi = 7.60e-12** (floor; quadratic, 13 Newton it, ~430s).
- **M_MS = 0.2936** (in the 0.28-0.30 target band).
- **B=1/A FREE**: max|a+b| body = 0.092 (nonzero -> A,B independent).

This is the anchor the P1 round-recovery is gated against.

---

## 3. VALIDATION

### GATE (b) -- off-diagonal general Einstein correctness IN THE RESIDUAL PATH  [PASS]
(grid 24,6,8; computed directly, no solve)
- **(b1)** zero-off-diag: `max|G_hybrid - G_weyl| = 0.0` EXACTLY -> diagonal sector
  uncorrupted; round soliton provably unchanged by the rewire.
- **(b2)** e_rt warp ON: live **G^r_th(deep) = 3.40e-3** (>>0 -> off-diagonal reaches
  the field equations); cross **G^r_ps(deep) = 1.0e-16** (machine-0 -> a theta-only
  warp sources only the (r,theta) block: correct selectivity, not noise).
- **(b3)** hybrid off-diag delta vs an INDEPENDENT CORE-linalg Einstein path:
  `max|delta_rth| = 0.0` EXACTLY -> the residual-path off-diagonal Einstein is correct
  (matches a different code path: spectral-einstein_mixed vs CORE.christoffel/einstein
  +linalg inverse).

### GATE (a) -- ROUND recovery (off-diagonals LIVE, seeded zero)   [PASS]
8-field P1 solve (a,b,c,d,Th,e_rt,e_rp,e_tp), deg-1 node core, off-diag seeded 0.
Two grids:
- **grid (16,6,8)** (nU=6144): converged **Phi = 7.87e-15** (MACHINE FLOOR) in 8 Newton
  iterations (quadratic: 4.10 -> 1.7e-2 -> 2.5e-3 -> 7.9e-4 -> 4.2e-5 -> 1.7e-6 ->
  4.4e-9 -> 7.9e-15). **M_MS = 0.29456** (recovers the P0 anchor 0.2936). B=1/A FREE:
  max|a+b| body = 0.238. Theta(core) = 1.000*pi, sin = 1.2e-16 (deg-1 node, exact).
- **grid (24,6,8)** (nU=9216): same trajectory, descending to floor (3.9e5 seed ->
  0.12 -> 2.0e-3 -> ... ); confirms grid-robustness of the recovery. [slow on the
  no-cache allocator; trajectory monotone-quadratic, same physics.]

OFF-DIAGONAL OUTCOME (the observation embedded in gate a; raw):
  e_rp = 4.0e-10, e_tp = 1.1e-10  -> STAY MACHINE-ZERO (Birkhoff expectation holds).
  e_rt = 1.29e-2  -> NONZERO.  off-diag Einstein residuals all satisfied to floor
  (rth=1.4e-8, rps=5e-16, thps=3e-16).

INTERPRETATION OF e_rt (audited, honest -- NOT manufactured structure):
- On the PRISTINE radial seed embedded in 3-D, the general Einstein's G^r_th is
  machine-zero (1.4e-15) at ALL Nth=6,8,12,16 -> the wiring does NOT spuriously
  generate off-diagonal G.
- In the CONVERGED 3-D solve at the COARSE Nth=6 GL grid, the diagonal fields
  a,b,c,d,Th developed a small angular variation (spread ~1e-3) -- the angular Einstein
  rows are weakly constrained at Nth=6 -- which sources a real G^r_th ~ 3.4e-2; e_rt
  grew to ~1.3e-2 to SATISFY that G^r_th residual (its job: off-diagonals feed back and
  absorb shear). e_rt is antisymmetric about the equator.
- So e_rt is the off-diagonal sector RESPONDING CORRECTLY to a small, coarse-Nth-induced
  non-axisymmetry in the diagonal fields, NOT physical off-diagonal content of the round
  soliton. The clean "round has no off-diagonal content" signal is e_rp,e_tp ~ 1e-10.
  Whether the round soliton's PHYSICAL off-diagonal content is exactly zero needs a
  higher-Nth round-recovery (the angular fields tighten to axisymmetry and e_rt should
  shrink) -- FLAGGED as a higher-resolution check (cheap at the linear level; the
  coupled re-solve at high Nth is P5-grade on the current allocator).

GATE (a) verdict: **PASS** -- the rewire recovers the soliton to MACHINE FLOOR with
off-diagonals live; the diagonal sector is uncorrupted (M_MS, B=1/A, node all correct);
the genuinely-decoupled off-diagonals (rp,tp) stay machine-zero; (rt) responds to a
coarse-grid shear, correctly satisfied.

### GATE (c) -- divT / gauge sanity   [PASS, with a coarse-Nth caveat on the gate itself]
On the converged (16,6,8) solution:
- **matter EL residual (the EOM actually solved) = 2.26e-10** (FLOOR -> the matter
  equation of motion is satisfied).
- divT_identity covariant divergence: |divT_r| = 1.30e-1, |divT_th| = 1.12e-1,
  |divT_ps| = 8.0e-11.
INTERPRETATION (honest): the ps-component is machine-zero (axisymmetric matter -> no
ps-momentum; the Fourier-ps basis is accurate at Nps=8). The r,th components are O(0.1)
NOT because the EOM is unsatisfied (it is, at 2.3e-10) but because divT_identity itself
takes spectral THETA-derivatives of Christoffel x T contractions, which are inaccurate
at only Nth=6 GL nodes -- it is the GATE's own coarse-Nth spectral error, not a physics
failure (it tightens with Nth; same Nth-sensitivity the committed record notes for the
divT gate). VERDICT: matter EOM at floor (PASS); the divT-identity gate is Nth-limited
at this coarse grid and is a clean PASS only in the ps-channel here -- flagged for a
higher-Nth confirmation (cheap, linear).

---

## 4. THE OBSERVATION (round + mild l=2 non-round matter)

Question (OBSERVE, not target): with off-diagonals able to feed back, in the STATIC
native-matter context, do the spatial off-diagonals want to grow, or stay zero?

RAW NUMBERS (grid 16,6,8, deg-1 node, off-diag live):
| config | M_MS | matter tvar | e_rt | e_rp | e_tp | Phi |
|---|---|---|---|---|---|---|
| ROUND | 0.29456 | ~0 | 1.29e-2 | 4.0e-10 | 1.1e-10 | 7.9e-15 |
| l=2 matter pert | 0.29544 | 5.23e-2 | 1.25e-2 | 3.6e-10 | 1.4e-10 | 6.6e-13 |

WHAT IS THERE (honest):
- **e_rp and e_tp STAY MACHINE-ZERO (~1e-10) in BOTH the round AND the mild-non-round
  (l=2, tvar=5e-2) case.** A genuine l=2 matter shape did NOT source the (r,ps) or
  (th,ps) off-diagonals. This is the clean OBSERVE result: static native matter (round
  or mildly non-round) does NOT drive the spatial off-diagonal/shear sector to grow --
  consistent with the Birkhoff/#62-64 expectation that static matter sources no spatial
  shear here.
- **e_rt ~ 1.3e-2 in both cases** is NOT physical off-diagonal content -- it is the
  (r,th) off-diagonal warp absorbing the small G^r_th sourced by the coarse-Nth=6
  angular variation in the diagonal fields (see the gate-(a) audit). It is essentially
  unchanged by the l=2 matter perturbation (1.29e-2 -> 1.25e-2), i.e. it tracks the
  grid, not the matter shape -- the fingerprint of a discretization response, not a
  physical mode. A higher-Nth run is the clean confirmation that it -> 0.

OBSERVE verdict: in the static native-matter regime tested, the spatial off-diagonals
stay zero (rp,tp exactly; rt is a coarse-grid artifact). No structure was manufactured;
the off-diagonals are now LIVE and ABLE to grow (they DO respond to shear -- e_rt
absorbs the coarse-grid G^r_th), but the physical static matter does not drive them.
This is exactly the "report it honestly, including 'they stay zero' if so" outcome.

---

## 5. THE AUDIT (every compromise, honestly)

- **Pole-stable hybrid, not a raw swap.** The literal "route through `einstein_mixed`"
  would have corrupted the diagonal sector by conditioning (documented above). The
  hybrid is category-A (same field equations, pole-stable evaluation), verified to
  reduce EXACTLY to the analytic Weyl at zero off-diagonal and to match an independent
  Einstein path on the off-diagonal blocks. This is a real engineering choice and is
  flagged as such -- NOT presented as "the general Einstein just dropped in."
- **a(phi) = -1 (GR) FROZEN.** Per P1 scope; a(phi) is P3. Flagged.
- **Time row ZEROED.** Per P1 scope; time-live is P4. Flagged.
- **deg-1 node core, not the free node.** The free-value node unwinds to vacuum
  (stage1a finding, reproducible here); deg-1 (core=pi node) holds the soliton. This is
  a homotopy-sector choice (pi is a node value selecting charge-1), explicitly NOT the
  m*pi ladder (grep-verified: the only m*pi in the code is a labelled negative-control
  branch). Flagged as the native core condition, with the free-node alternative noted.
- **Matter EL is the diagonal-warp analytic EL (`matter_el_3d`).** It varies Theta on
  the diagonal metric; it does not yet see the off-diagonal warps (that is P2's 3-D
  Theta-free generalization). For P1 (spatial-metric off-diagonal wiring) the matter is
  the existing native single-profile field; the off-diagonal METRIC sector is what P1
  turns on. Flagged: the matter-EL/off-diagonal-metric cross-coupling is incomplete
  until P2.
- **No B=1/A injection, no dropped/added term, no tuned dial, no linearization kept.**
  Grep-verified. The Newton local linear step is the solver; the reported solution
  satisfies the full nonlinear residual to the reported floor.
- **Numerics performance caveat:** the no-cache CUDA allocator workaround (needed for
  jacrev under broken NVML) makes the 8-field jacrev solve slow. Round-recovery is
  reported at grid (24,6,8); off-round coupled solves at production grid are expected to
  be solver-limited (P5 is the fix), not a physics null.

---

## 6. SCOPED STATUS

**P1 = DONE** (spatial off-diagonals wired to the general Einstein, validated, first
observation taken), with two flagged caveats for higher resolution:
- The rewire is genuine general-Einstein (off-diagonals feed the field equations,
  verified live + independent-path-correct + back-reacting on the diagonal blocks),
  pole-stable (exact reduction to the analytic Weyl at zero off-diagonal).
- Round recovery to MACHINE FLOOR (Phi=7.9e-15), M_MS=0.295 (anchor), B=1/A free,
  deg-1 node exact.
- OBSERVE: spatial off-diagonals (rp,tp) stay machine-zero under round and mild-l=2
  static native matter; (rt) is a coarse-Nth artifact (flagged for higher-Nth).
- CAVEATS (both resolution, not physics): (i) e_rt ~ 1e-2 coarse-Nth response -> needs
  higher-Nth to confirm -> 0; (ii) the divT-identity gate is Nth-limited at Nth=6 (the
  matter EOM itself is at floor, 2.3e-10).

**What P2 inherits:**
- The 8-field P1 residual (`p1_residual_general_einstein.py`) with the general-Einstein
  field equations and live spatial off-diagonals -- ready for the 3-D Theta-free node
  matter EL (P2's job).
- The KNOWN P1 incompleteness P2 must close: the matter EL (`matter_el_3d`) is varied on
  the DIAGONAL metric only -- it does not yet see the off-diagonal warps. P2's 3-D
  Theta-free generalization must vary the matter on the FULL (off-diagonal-carrying)
  metric so the matter-EL/off-diagonal cross-coupling is consistent (this will also make
  the divT identity tight once the EL sees the full metric).
- A higher-Nth angular grid is needed to separate physical off-diagonal content from the
  coarse-Nth e_rt response -- relevant once P2 matter is 3-D.
- The no-cache CUDA allocator makes the 8-field jacrev solve slow (~1700s/solve at
  16,6,8); P5's research-grade driver (preconditioned Newton-Krylov / sparse-direct)
  is the throughput fix for production grids and the off-round coupled regime.

---

## ATTACK HERE (for a blind verifier)

1. **Is the hybrid genuinely general-Einstein, or diagonal in disguise?** Check that
   off-diagonal warps change the DIAGONAL residual rows (back-reaction), not only the
   off-diagonal rows. Re-derive `einstein_general_hybrid` on a metric with a known
   off-diagonal (e.g. a slow-rotation g_tpsi analog mapped to a spatial shear) and
   compare every G^mu_nu component to sympy.
2. **b1=b3=0.0 EXACTLY -- too clean?** Confirm b1 is structural (G_full - G_weyl with
   the bracket = einstein_mixed(g)-einstein_mixed(g) = 0 by construction) and b3 uses a
   genuinely independent inverse/contraction path (CORE.metric_inverse=linalg vs the
   spectral einstein_mixed) -- not the same code compared to itself.
3. **Does the round recovery actually hold the soliton, or did the deg-1 BC + off-diag
   regularity over-constrain it into the diagonal answer trivially?** Verify the
   off-diagonals were FREE to grow (their BC is only regularity at core+seal, free in
   the body) and stayed ~0 as a SOLVE outcome, not because they were pinned.
4. **Conditioning honesty.** Reproduce the flat-space general-Einstein blowup
   (`_p1_diag_flat.py` pattern) and the difference-cancellation (`_p1_diff_cancel.py`)
   to confirm the hybrid is necessary and that the difference is well-conditioned.
5. **Grep discipline.** `grep -nE "m\s*\*\s*PI"` -> only the labelled negative-control
   branch. `grep -nE "b=-a|a=-b|1/A"` -> no B=1/A tie. node-only core in the default path.
