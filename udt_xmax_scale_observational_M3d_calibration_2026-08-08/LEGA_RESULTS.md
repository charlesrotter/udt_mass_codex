# M3d LEG A — mock-injection calibration (instrument-fidelity test) — RESULTS

Date 2026-08-08 | prereg 962bd0c6 (frozen before any mock ran) | agent: M3d LEG-A.
Terminology ruling in force: the object is "the observed clustering feature"; "acoustic"
only as attributed to the mainstream.

## 1. Design as executed (prereg SS1; every choice tagged)

Synthetic universes with ONE true scale, run through the FROZEN M3 -> M3c pipeline
unchanged, to measure whether our instrument manufactures the reported anomalies.

- **Skeleton = the real surveys** [THEORY: prereg SS1]: per (cap, shell), the four real
  DESI DR1 random files (BOSS: random0) are deterministically partitioned into LS
  randoms (10x data, the M3b-declared RAN_FACTOR) and a disjoint pool from which mock
  "galaxies" are drawn. Real footprints, real per-shell WEIGHTED densities
  (N_mock = round(real weighted count), mock weights = 1; disclosed), real weighted
  per-shell dN/dz (resampled). Real data POSITIONS never touched; mock catalogs carry
  tag='synthetic' (the M2 guard never flipped).
- **Feature injection** [THEORY: prereg SS1]: pair-splitting; a fraction f_pair of final
  points are companions at theta_t(z_parent) = ell_t/r_truth(z), random azimuth.
  Companions leaving the footprint (no LS random within r_memb = sqrt(6/(pi*lambda_LS)))
  are dropped and replaced by unpaired pool points — matching the real selection (a
  partner outside the survey is not observed); density preserved exactly.
- **Truth variants** (both run):
  (i) ell_t = 58.34 Mpc over the UDT P1-fitted r(z) (the frozen M3b ruler; gentle fall
      2.357 deg at z=0.725 -> 2.026 deg at z=1.075);
  (ii) published-shape drift (attributed instrument-test input): theta_ii(z) =
      theta_i(0.9) x (z/0.9)^(-0.774) deg = 2.157 x (z/0.9)^(-0.774) deg — the power-law
      approximation of the mainstream angular-BAO drift theta ~ 1/D_C(z) over
      0.70<=z<=1.10, amplitude anchored to variant i at z=0.9 (matched range).
      Fall: 2.550 -> 1.880 deg (steeper than variant i).
- **Shells**: the 8 LRG driver shells (z 0.70-1.10, dz=0.05) + QSO 0.95-1.10 and
  1.10-1.25 (the split-relevant set). BOSS arm: the 5 M3b CMASS shells (0.43-0.68),
  variant-i truth, 10 realizations.
- **Pipeline per mock = the frozen chain**: cap-combine LS w(theta), 40 log bins
  0.3-12 deg, 24 regions/cap (T=48 union jackknife) [v_bao, frozen] -> frozen 12-bin
  rebin C12 = A C40 A^T [build_cov, frozen] -> Hartlap inverse -> generalized-chi2 bump
  scan + profile center + Delta-chi2=1 error x Percival + 300-MVN local p [rerun_m3c
  machinery, frozen]. Category-A caching only: RR/region maps computed once per shell
  (randoms frozen across realizations); assembly uses v_bao._ls_from_blocks_general
  byte-identically (equivalence-checked, section 2).
- **Seeds** (frozen): variant i realizations 9000+r; variant ii 9100+r; BOSS arm
  9200+r; calibration 8990-family; asset partition 20260808+crc32.

## 2. Category-A soundness checks

- **Cached-assembly equivalence** (equivalence_check.json): one mock shell (LRG
  1.05-1.10) run BOTH through the cached-RR assembly and through the frozen one-shot
  v_bao.ls_w_theta_capcombine on identical catalogs -> max|dw|=0.0, max|dcov|=0.0
  (bit-exact). The RR caching is pure Category-A bookkeeping; the estimator math is
  v_bao's, untouched.
- **GPU block size**: 8192 vs 16384 give identical counts; 8192 kept (2.8 GB peak,
  fits alongside other work). Big-shell RR built via the exact 3-part split
  (auto(R1)+auto(R2)+cross, ordered-count symmetry) — same pair set, fp-order only.

## 3. f_pair amplitude calibration (F-FAIR-MOCK evidence)

Grid f in {0.10,0.20,0.30,0.45} on the 3 LRG driver shells (fpair_calibration.json);
A_b(f) fit linear; per-shell f solving A_mock=A_real: LRG0.70->0.414, LRG0.90->0.318,
LRG1.00->0.191; **f_pair = median = 0.318** (frozen for all shells/variants).
Amplitude match on the calibration shells: mock A_b40 med 0.0054/0.0083/0.0228 vs real
0.0069/0.0087/0.0153 — same order, matched by construction.
**BUT the significance is NOT matched (the load-bearing fairness fact, section 6):** at
matched amplitude the mock detection dchi2 runs **4.9-10.4x the real** dchi2 (same 40-bin
diagonal statistic), because the mock field is shot-noise + injected-ring only and lacks
the broadband angular clustering that inflates the real jackknife errors.

## 4. Metric tables M1-M4  (variant i = UDT ell=58.34 r(z); variant ii = published-shape drift)

N run: **variant i 15/15, variant ii 15/15, BOSS arm 10/10** (prereg fallback N=15/variant,
disclosed: r00 timing projected 2x25 at 6.1h > 6h budget -> n_real_decision.json).

- **M1 center recovery (variant i, 10 shells):** mean|bias_ln| = 0.065 (~6.5% low),
  median scatter_ln = 0.046, far-miss(|Δln|>0.5) = 0.00 on every shell. Centers recovered
  near-perfectly — a direct consequence of the too-clean mock (section 6).
- **M2 anti-drift false-positive rate:** variant i truth slope dlnθ/dln(1+z) = -0.81
  (gentle fall); **recovered slope mean +0.05, sd 0.86 -> 67% of realizations measure a
  TRUE falling drift as FLAT-OR-RISING.** Variant ii truth slope -1.64 (steeper);
  recovered -1.80, anti-drift 7%. So a shallow true drift IS routinely mismeasured as
  anti-drift; a steep one is not.
- **M3 THE false tracer-split rate (LRG 1.00-1.05 vs QSO 0.95-1.10):**
  **0/30 pooled** (variant i 0/15, variant ii 0/15). Mock split ratios span only
  1.00-1.23x (obs 1.65-1.74x) and split significances 0-3.0σ (obs 3.83-4.51σ); the
  frozen bar (≥1.75x AND ≥3.8σ) is never reached. Binomial 95% upper bound = 0.095.
- **M4 BOSS-density scatter (10 real., 5 CMASS shells, one true ell=58.34):** implied-ℓ
  from recovered centers spans **47-76 Mpc** (5-95 pct 52-74), 0% outside 40-80 Mpc —
  versus the observed M3b spread 4-212 Mpc. One true scale at CMASS density does NOT
  reproduce the huge observed scatter in these mocks.

## 5. Mechanical threshold application (prereg SS1 frozen rule)

Frozen rule: p>0.05 -> DOWNGRADE; p<0.01 -> RE-FIRMS; between -> CAL-MIXED. Applied to the
point estimates, WITH the N=30 binomial resolution and the fairness caveat attached:
- **M2 anti-drift -> DOWNGRADE** (variant i false-positive 0.67 >> 0.05). The observed
  anti-drift is method-artifact-consistent. **This verdict is CONSERVATIVE** w.r.t. the
  fairness bias (a cleaner mock recovers drift better, so the true false-positive rate is
  ≥0.67) -> banks cleanly.
- **M3 split -> point estimate 0/30 stamps the RE-FIRMS direction, discharge BLOCKED
  (fairness-limited), leaning WEAKLY re-firm.** The split gate is TWO gates (ratio≥1.75x
  AND σ≥3.8) and the too-clean bias acts in OPPOSITE directions on them: too-clean ->
  precise centers -> UNDER-scatter -> HARDER to reach ratio 1.75 (this gate BINDS: mock
  ratios cap at 1.14/1.23x vs the 1.75x needed); too-clean -> smaller errors -> EASIER to
  clear 3.8σ. So 0/30 is confounded on the BINDING (ratio) axis, not uninformative.
  Quantitative check (verifier): faking ratio 1.75x needs ~30% center displacement =
  ~6σ of the mock's 4.6% center scatter; a broadband inflation of ~2-3x (implied by the
  4.9-10.4x dchi2) lifts the scatter to ~10-14%, still short of the ~15-20% required to
  make ratio 1.75x common -> BORDERLINE, so **CAL-OBSTRUCTED(fairness)** is the honest call,
  leaning weakly toward re-firm (a fair mock plausibly still would not manufacture the
  ratio). Neither cleanly re-firmed nor shown to be an artifact.
- **M4 scatter -> CAL-OBSTRUCTED(fairness)** by the same too-clean bias (a noise-fair mock
  would scatter wider than 47-76 Mpc; cannot exclude that realistic noise reaches the
  observed range).
- **Prereg deviation (stated plainly):** SS1 set "N_mock = 25 minimum"; **15/variant** was
  run (budget-disclosed, n_real_decision.json). Harmless to the M3 conclusion: even the
  full 2x25=50 gives a binomial 95% upper bound 0.058 > the frozen 0.01 bar, so M3 could
  not be DISCHARGED (re-firmed) either way at this N — the obstruction is the mock's
  fairness, not the realization count.

## 6. Fair-mock discharge statement (F-FAIR-MOCK, the primary falsifier — it FIRES)

F-FAIR-MOCK points at this pipeline and it **FIRES on the strong side.** The mocks are fair
on the two axes the prereg named explicitly — real footprints/randoms, real per-shell
weighted densities, real dN/dz, and bump AMPLITUDE matched to the real A_b — so this is NOT
a weak/noisy rigged-deflation (that failure mode is excluded: a too-weak mock would
manufacture splits/scatter and force DOWNGRADE; we see the opposite). **The unfair axis is
detection SIGNIFICANCE:** injecting a single sharp ring onto a Poisson field with matched
amplitude yields 4.9-10.4x the real dchi2, because the mock omits the broadband angular
clustering that dominates the real jackknife covariance. A too-clean instrument recovers the
injected scale too precisely. For the split this cuts BOTH WAYS across its two gates:
too-clean under-scatters centers -> HARDER to reach ratio≥1.75x (the BINDING gate; mock
ratios cap at 1.14/1.23x), while smaller errors make σ≥3.8 EASIER — so 0/30 is confounded
on the binding (ratio) axis and leans WEAKLY toward re-firm rather than being fully
uninformative (verifier's quantitative check, §5: a fair ~2-3x scatter inflation reaches
~10-14%, short of the ~15-20% that would make ratio 1.75x common — borderline). For M4 the
too-clean bias runs one way (under-scatter). Consequently:
- Only **M2 (anti-drift) discharges cleanly -> DOWNGRADE**, and conservatively so: at our
  S/N a genuinely gentle falling drift is measured flat-or-rising 67% of the time, so the
  observed anti-drift carries no weight against a single smooth true curve.
- **M3 (the tracer split) and M4 (BOSS scatter) are NOT dischargeable from this leg.** The
  observed split/scatter do not reproduce here, but that is confounded with the mock being
  too clean; a fair re-test requires a mock whose w(θ) covariance (not just amplitude)
  matches real — e.g. drawing the seed field from a broadband-clustered process, or
  bootstrapping the real jackknife covariance into the injected mocks. Recorded as the
  concrete next build; NOT run in this frozen leg (adding broadband power now would be a
  post-hoc F-RETRO design change).

**Outcome (prereg SS5, all first-class): CAL-MIXED.** One component deflates (M2 anti-drift
= method artifact); two components (M3 split, M4 scatter) are CAL-OBSTRUCTED by a
now-identified fairness limitation of our own instrument. The split is neither vindicated
nor killed by Leg A. Blind verifier owed (fair-mock audit = its primary brief), then HOLD
for Charles. Verified-LEAD ceiling.

## LAB LOG (running)
- 2026-08-08/09: assets built (30 cap-shells; ls_factor=10.0 everywhere; pools >=9.5x N).
  RR caches: 30/30 banked over 11 foreground budgeted calls (biggest shells via the exact
  3-part staged split). One early background call stalled -> policy switched to synchronous
  foreground chunks only.
- 2026-08-09: sweep complete via ~30 synchronous foreground bounded calls (each <=~9min,
  per-shell checkpointed, resume-safe). N=15/variant (fallback, disclosed) + BOSS 10/10.
  Metrics + fairness audit computed. Headline: M3 false-split 0/30; M2 anti-drift 0.67
  (variant i) -> DOWNGRADE; F-FAIR-MOCK fires (mock 4.9-10.4x too significant) ->
  M3/M4 CAL-OBSTRUCTED(fairness); overall CAL-MIXED. HOLD for Charles; blind verifier owed.

## 7. CONSOLIDATED LANDING (post-verifier, 2026-08-09)

**Blind verifier: SUSTAINED-AMENDED** (RESULTS_VERIFIER_REPORT.md) — every metric reproduced
exact from the raw checkpoints; Leg B arithmetic confirmed; F-RETRO clean. Two amendments
applied above: (1) the fairness bias is TWO-DIRECTIONAL on the split's two gates (binding
ratio gate hardened by too-clean centers; σ gate eased) -> CAL-OBSTRUCTED(fairness) stands
but leans WEAKLY re-firm, with the verifier's ~15-20%-displacement-needed vs ~10-14%-reachable
borderline check; (2) prereg deviation flagged: N=15/variant vs "25 minimum" (budget), harmless
since even 2x25 gives binom-95 upper 0.058 > 0.01 so M3 is undischargeable either way at this N.

**Overall M3d landing = CAL-MIXED.** Per-metric:
- **M2 anti-drift -> DOWNGRADE (robust).** A true gentle fall reads flat-or-rising 67% at our
  S/N; conservative w.r.t. the fairness bias. The observed anti-drift carries no weight.
- **M3 tracer-split -> CAL-OBSTRUCTED(fairness), leans-weakly-re-firm. NOT vindicated, NOT
  killed.** 0/30 mocks reach the ratio≥1.75x & σ≥3.8 bar; confounded by the too-clean mock on
  the binding ratio axis.
- **M4 BOSS scatter -> CAL-OBSTRUCTED(fairness).** One true scale gives a tight 47-76 Mpc, not
  the observed 4-212 Mpc, but the too-clean bias precludes a clean discharge.
- **Leg B (literature cross-check) -> CAL-MIXED.** Both carried: the z~1 LRG shell sits within
  ~1.2σ of the published angular-BAO curve, AND the global fit misses (chi2 = 47.6/5, sys,
  p=4e-9). Local agreement with a global tension.

**Named next build (NOT run — would be F-RETRO here):** a fair mock whose w(θ) COVARIANCE
(not just amplitude) matches real — broadband-clustered seed field or bootstrapped-jackknife
covariance injected into the mocks — to resolve the split cleanly.

**Four-check:** pre-registered (962bd0c6, before any mock) ✓; bounded/full-space (N=15/variant
+ BOSS 10, budget-disclosed; fallback justified) ✓; blind-verified (SUSTAINED-AMENDED, metrics
reproduced exact) ✓; premises audited (F-FAIR-MOCK fires, fairness limitation surfaced and
carried on every M3/M4 verdict) ✓. **Status: verified LEAD** (same-session; the external bar
travels on the CAL-MIXED landing). HOLD for Charles.
