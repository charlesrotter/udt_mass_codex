# P1 PURITY HARNESS — MAP (pre-build, for sign-off)

**Status:** MAP / make-visible stage. NO code written yet. Awaiting Charles sign-off.
**Source spec:** SOLVER_INTEGRITY_UPGRADES_SPEC.md (P1). **Date:** 2026-06-23.
**Method note:** this is the MAP rung of How-We-Work — state the frame whole, ledger every
premise (chose or derived?), surface smuggled assumptions BEFORE building. Pre-work discussion
in lay terms; the ledger below is exact.

---

## 0. THE SPINE (the rule that keeps the harness from becoming a new import surface)

**The harness REFERENCES derivations; it NEVER re-asserts their results.**
A test that hard-codes a derived number (e.g. "kap8 must == 1", "a(φ)=e^{φ}") bakes a result into
a guard — if the derivation is later revised, the test silently smuggles the stale value. That is the
embedding risk Charles flagged (2026-06-23). So:
- P1 enforces **provenance** (every physics constant carries a tag) and **structure** (DOFs live,
  limits recovered, native vs import made visible).
- The **values** of derived couplings are sourced from P2's single action file, never restated in a
  test. P1 checks the *tag is present*; P2 makes the *value* sourced.

---

## 1. WHAT P1 IS (frame, whole)

A pytest suite that runs on every solver change and fails LOUDLY when a past failure mode reappears,
so integrity stops depending on an agent remembering to check. Four checks, each anchored to a real
banked bug. It guards the **current live production solver** (Charles ruling 2026-06-23: "guard live
solver now; RED documents gaps") — NOT a hypothetical future operator.

### What grounding the MAP found (verified against code, file:line — reshapes the spec's premises)

The spec implicitly assumed the live solver is the derived + native object. It is not. Three facts:

- **F-i. Live operator is `a = −1` (GR baseline), NOT the derived `a(φ)=e^{φ}`.**
  `p1_validate.py:53` stamps runs `(node-core, B=1/A free, a=-1)`. The derived vacuum≠GR operator lives
  in the derivation docs + the einstein_3d_general engine, but is NOT wired into the production residual
  `p1_residual_general_einstein.residual_vector_p1`. → P1 cannot *pin* `a(φ)=e^{φ}`; it can only require
  the `a`-exponent be TAGGED. Value enters at P2.
- **F-ii. `kap8 = 1 (DERIVED)` has not propagated; live callers pass `0.05`** (and 0.01, 0.03, 1e-2, 8π).
  `kap8` is a free argument everywhere (`p1_validate.py:40`, `p5a_prime_scaling.py`, `VERIF_divT_committed.py`,
  `coupled_tl_stage1a.py`, …). → P1 requires every `kap8` assignment be TAGGED; value sourced in P2.
- **F-iii. The native-object guard, as the spec writes it, points at the IMPORTED object.**
  The native-matter arc concluded the round/static-soliton line IS the imported S³ object. The P1
  production residual descends from it: matter stress uses a 4-component **S³ hedgehog**
  (`whole_metric_3d_matter.hedgehog_n`), and the default `core_mode="deg1"` **pins Θ(0)=π**
  (`p1_residual_general_einstein.py:166`, `Th[0]-PI`). The value-free native node (`core_mode="free"`)
  is documented (`:137-139`) as unwinding to vacuum. → The guard must CHARACTERIZE this state, not
  bless or condemn it (see §2.4).

---

## 2. THE FOUR CHECKS (grounded; design decisions resolved)

### 2.1 Liveness — "off-diagonals built but dead" bug
- **Target:** `residual_vector_p1(u, G, p, kap8, ...)` in `p1_residual_general_einstein.py:128`.
  8 fields: `a,b,c,d,Θ,e_rt,e_rp,e_tp`.
- **Test:** on a generic background, perturb each off-diagonal DOF (`e_rt,e_rp,e_tp`) at a body
  interior point; assert ‖ΔF‖ > tol. FAIL = that DOF is dead / residual secretly diagonal.
- **DESIGN DECISION (chose):** the background MUST be **off-round** — on a round config, symmetry
  legitimately decouples some DOFs and the test would false-flag "dead." Use the off-round config from
  `b1prime_3d_offround_validate.py:73-100` (smooth l=2 warp), where every DOF is physically expected to
  couple. Without this the test is meaningless.
- **Note:** time-row DOFs (`g_tr,g_tθ,g_tψ`) are currently ZEROED (stationary; Stage 5 unfreezes). The
  spec lists them; P1 asserts their **current frozen state with a labeled "STAGE-5 TODO"** characterization
  row, so the freeze is documented, not silent (BOUND not FREEZE discipline — the freeze is visible).

### 2.2 Provenance lint — smuggled `kap8=0.05` bug
- **Target scope (chose):** the operator/matter BODIES — `p1_residual_general_einstein.py`,
  `whole_metric_3d_matter.py`, the metric-build/coupling sites. **EXCLUDE** auto-generated
  `einstein_3d_general_gen.py` (~500 CSE temporaries `x0,x1,…` — guaranteed false positives) and
  numeric hyperparameters (wbc, tol, maxit, EXP_CLAMP, det-clamp).
- **Test:** physics literals (couplings, exponents, BC target values) must carry a tag
  `# DERIVED|POSTULATED|FREE|IMPORTED`. FAIL on an untagged physics literal.
- **kap8 (Charles ruling 2026-06-23 — avoid embedding):** require a TAG on every `kap8` assignment now;
  do NOT assert value==1 in the test. Value sourced from P2's action file. The lint will currently flag
  the un-tagged `0.05` callers — that RED is the feature (documents the un-migrated fix).
- **a(φ):** require the exponent be TAGGED; value (`e^{φ}`) sourced at P2.

### 2.3 Limit recovery — standing test
- **Refs:** repo has NO golden NPZ; references are symbolic (`verify_p1_flat_core.py`,
  `verify_p1_birkhoff_flat.py`) + recomputed seeds (`round_seed`).
- **Asserts (tolerance, NOT bitwise — chose; bit-equality is brittle across harmless FP reordering):**
  flat → ‖G‖<1e-13; Schwarzschild → vacuum residual <1e-12; ω→0 → returns the static soliton to ~1e-12;
  `a=−1` baseline reproduces the prior P2 result to ~1e-12; round → box-control (slow tier: a small
  R-sweep, ω²~1/R² with intercept≈0).
- **Tiering:** flat/Schwarzschild/limit asserts are fast (symbolic/single-eval) → per-edit tier.
  Box-control is an R-sweep → slow/nightly tier (marked `@pytest.mark.slow`).

### 2.4 Native-object guard — S³ Skyrme import (CHARACTERIZE, do not judge)
- **Charles ruling 2026-06-23:** treat as a **documented-gap (amber)**, not a hard-RED and not a blessing.
  The guard reports state; the physics migration resolves it.
- **Test (characterization):** assert + REPORT the current live matter state:
  (a) stress path uses the 4-component S³ hedgehog `hedgehog_n`;
  (b) default `core_mode="deg1"` pins Θ(0)=π (`:166`);
  (c) the value-free native node `core_mode="free"` exists and is the native target;
  (d) HARD-FAIL only on the labeled negative-control Skyrme ladder `Θ(core)=m·π` with `node_core=False`
      (`:169`) leaking into a non-control production call.
- **Self-resolving:** when the native-S² object replaces the pin in the production path (live-frontier
  work), rows (a)/(b) flip to assert the native winding `n=x/r` and `core_mode="free"`; the amber clears.
  No verdict on deg1 is hard-coded now (avoids the lint licensing the import).

---

## 3. PREMISE LEDGER (chose or derived?)

| # | Premise | chose / derived | Risk if wrong |
|---|---|---|---|
| 1 | Off-round background = b1prime l=2 warp config | **chose** (grounded in real config) | round bg → false "dead DOF" |
| 2 | Lint scope = operator/matter bodies, exclude gen + hyperparams | **chose** | too broad → unusable; too narrow → toothless |
| 3 | Limits checked to ~1e-12, not bitwise | **chose** | bitwise → brittle false RED |
| 4 | Guard CHARACTERIZES the live import, hard-fails only the m·π control | **Charles ruling** | judging deg1 now → licenses or alarm-fatigues |
| 5 | kap8 / a(φ) — TAG now, VALUE sourced at P2 | **Charles ruling** | pinning value → embedding stale result |
| 6 | Harness guards the CURRENT live solver (a=−1, S³) | **Charles ruling** | guarding a hypothetical → no traction on real gaps |
| 7 | Time-row DOFs frozen → characterized as STAGE-5 TODO | **chose** | silent freeze = hidden DOF |

Everything tagged "chose" is a design call I can defend; flag any you want changed. The "Charles ruling"
rows are your 2026-06-23 decisions, recorded.

---

## 4. ACCEPTANCE (from the spec, made concrete)

1. Suite green/amber-as-designed on current `main` (the import/kap8/a(φ) items report DOCUMENTED-GAP,
   not spurious RED; only genuine regressions are RED).
2. **Catch proof:** in a scratch branch, deliberately reintroduce each of the 4 historical bugs
   (kill an off-diagonal; strip a kap8 tag / inject bare 0.05 in the operator body; break a limit;
   leak the m·π Skyrme BC into production) and confirm the matching test goes RED. Prove it bites.
3. Layout: new `tests/` dir + minimal `conftest.py` (fixtures: Grid3D, round seed, off-round seed,
   P1 residual). pytest configured (`pytest.ini`). Fast tier per-edit; `@slow` for the R-sweep.

## 5. OUT OF SCOPE (explicit)

- Migrating the operator to `a(φ)=e^{φ}` or matter to native S² (that's P2 + live-frontier work; P1
  only GUARDS + documents the gap).
- Pinning any derived value (sourced at P2).
- The P2 action-file codegen, P3 skills, P4 cross-model, P5 LIVE.md (later items).

## 6. WHAT I NEED TO BUILD (on sign-off)

`tests/test_solver_integrity.py` + `tests/conftest.py` + `pytest.ini`, four checks per §2, acceptance
per §4. Verifier-before-record (fresh zero-context Claude, per P4 ruling) on the catch-proof. Commit
the test files WITH a short results doc `p1_purity_harness_results.md`.
