# BLIND ADVERSARIAL VERIFIER — Coupled Time-Live Non-Round Native Catalog Solve

**Verifier:** claude-opus-4-8[1m] (independent blind adversarial pass).
**Date:** 2026-06-19.
**Target:** `archive/pre_2026-07-01/coupled_timelive_solve_results.md` (SCOPED NEGATIVE verdict) under the
frozen `archive/pre_2026-07-01/coupled_timelive_solve_CONTRACT.md`.
**Mode:** DATA-BLIND (no lepton/mass/ratio/wall number loaded or compared). I re-ran
the solver from independent harnesses (my own loops, not the driver's `coupled_tl_gates`
where avoidable; cross-checked GPU and CPU) and re-derived the structural arguments.
**NOTE on infra:** concurrent GPU jobs early in the session corrupted/slowed the V100;
I isolated to single clean processes and cross-checked on CPU. All numbers below are
from clean isolated runs.

---

## CLAIM-BY-CLAIM

### A) CALIBRATION (Stage 1a) + anti-import grep — **STANDS**
Independent run of `coupled_tl_stage1a.py`:
- `core_mode='deg1'`: **M_MS = 0.280991** (dead-center the 0.28-0.30 target), core
  Th(0)=π with **sin Θ(0)=1.22e-16 (a node)**, seal=0 (node), B=1/A FREED
  (max|a+b|_body = 0.162 ≠ 0 — not over-imposed). Body residuals res_tt=2.3e-5,
  res_rr=2.4e-4, res_thth=1.1e-4 (converged, O(1e-4)).
- `core_mode='free'`: M_MS = 9e-6, Th(0)→-0.04 (≈0) — the free-value node genuinely
  **UNWINDS to vacuum**. The driver's honest finding is reproduced exactly.

Anti-import grep: the regex `m\s*\*\s*pi|m\*np\.pi|core.*pi` is NOT empty — it matches
docstrings/comments/prints (e.g. the comment `# core NODE = pi`). The driver's literal
phrasing "exit 1 / NO core-twist BC in any code path" is slightly imprecise (grep exits
0 on comment hits). BUT the substantive claim holds: the only actual CODE core BC is
`F[:,0] = Tc[:,0] - PI` (a single fixed node value), and `F[:,0] = (Tc[:,1]-Tc[:,0])/h`
(regularity) — there is NO `m*pi` parametrized ladder and NO m-scan anywhere in code.
Seed amplitudes use `m_for_seed*PI` as an initial guess only, never a solved BC.

**Is core=π a smuggled m=1 Skyrme import? — MY HONEST JUDGMENT: NO, it is a legitimate
node value, but it IS a chosen topological sector (correctly flagged COMPROMISE #1).**
Reasoning: the native EL restoring term ∝ sinΘcosΘ vanishes at r→0 only for
Θ(0)∈{0,π/2,π,...}; regularity of Y=sin²Θ/r² then forces sinΘ(0)=0, leaving {0,π,2π}.
So π is one of the EL's OWN discrete node values — not a value imported from Skyrme. The
distinction the driver draws (a node value selecting the deg-1 homotopy class vs `m*π`
as a free, scanned ladder index) is real and correct. The genuine cost — honestly
flagged — is that holding degree-1 requires CHOOSING the opposite-node sector (core=π,
seal=0), because the maximally-agnostic free node unwinds (M_MS~0, shown). This is a
topological-sector choice, not a dynamical answer-pin, and the doc tags it as such.

### B) BACK-REACTION GENUINELY FINITE-AMPLITUDE — **STANDS**
Independent A=0 vs A=4 background comparison (`solve_coupled_breather`, N=400, cell=14):
- **max|da| = 1.0092, max|db| = 0.2261, max|dTh0| = 0.1686.**
- w2_low: 0.07311 (A=0) → 0.03291 (A=4); M_MS: 0.28109 → 0.27501.

The metric (a,b) AND matter (Th0) genuinely re-solve with amplitude. This matches the
driver's reported max|da|~1.0, max|dTh0|~0.17. The back-reaction is NOT a frozen-bg
linearization; the test is NOT void. A=0 reproduces the proxy spectrum, A>0 departs
(softens). Code inspection confirms `rho_kin(A,u,w2)` enters BOTH the (t,t) source
(rho_tot = rho_static + rho_kin) and the (r,r) pressure, and the loop re-solves Th0, a,
b, and the mode u each outer iteration. Genuinely coupled.

### C) GATE A — BOX-CONTROL (the decisive gate) — **STANDS**
Independent cell-size scans (I built my own loop, not the driver's harness):

A=0 (CPU, N=300): w2_low = 0.15156 (cell 8) → 0.07354 (cell 14) → 0.01998 (cell 28).
  cell 14→28 doubling ratio = **3.68x ≈ 4** (the 1/R² box signature).
A=4 (GPU, N=300): w2_low = 0.10497 (cell 8) → 0.03282 (cell 14) → 0.00799 (cell 28).
  cell 14→28 doubling ratio = **4.11x ≈ 4** (1/R² PERSISTS at finite amplitude).

These reproduce the driver's columns (A=0: 0.148/0.073/0.020; A=4: 0.104/0.033/0.008)
to ~1-2%. **w2_low quarters each time the cell doubles, at BOTH A=0 AND A=4.** The
lowest level is the CELL WALL, not intrinsic — Gate A A1 FAILS for a "new intrinsic
level," exactly as the driver reports. The verdict does NOT flip to POSITIVE: the level
is not flat across cell size; it scales to zero with the box. Structural sanity check:
the mode operator is a Dirichlet-type radial operator on [r_core, r_seal], whose lowest
eigenvalue ~ (π/L)² ~ 1/L² by construction — so box-control is the EXPECTED structure,
and an O(1) back-reaction shifts coefficients but not the 1/L² scaling. Consistent.

### D) GATE B — REAL VERDICT vs SOLVER STALL — **STANDS**
Independent grid scan (cell=14, A=4): N=300 → w2_low=0.032823, N=500 → 0.032969,
**spread = 0.44%.** (The driver reports N=300/500/800 = 0.03280/0.03324/0.03365, 2.5%;
my N=300 matches their N=300 to 5 digits.) The level is GRID-STABLE. The B1 control
(static round soliton + A=0 mode) converges to floor on the same machinery (stage-1a
res_th~1e-11, body Einstein residuals O(1e-4)). => this is a LEGITIMATE VERDICT, NOT
INCONCLUSIVE. Box-control is a physical property of the level, not a solver artifact.

### E) THE VERDICT (per contract §4) — **STANDS: SCOPED NEGATIVE is the correct call**
The decision table requires, for SCOPED NEGATIVE: {floor = l(l+1)W_inf} + {box
continuum}, back-reaction does NOT manufacture a new bound level, on a Gate-B-converged
solve. All confirmed: Gate A FAILS for any new intrinsic level (A,C above); Gate B
PASSES (D); the back-reaction is active but SOFTENS toward ω²→0 (tachyon onset),
the OPPOSITE of opening a new bound rung. POSITIVE is correctly NOT claimed (no level
passes Gate A). INCONCLUSIVE is correctly NOT claimed (grid-converged).
Forbidden-move audit:
  (i) box-control dressed as a result? NO — it is REPORTED as the verdict.
  (ii) inconclusive dressed as a null? NO — Gate B passes (grid spread 0.44-2.5%).
  (iii) target/load a data number? NO — grep of all scripts finds only the frozen
       regime params (p=0.4, kap8=0.05, rc=0.05, xi=kap=1); no lepton/mass constants.
  (iv) B=1/A over-imposed? NO — a,b solved independently ((r,r)→a, (t,t)→b);
       max|a+b|_body=0.16≠0; B=1/A recovered only in exterior as a result.
  (v) matter frozen? NO — Th0 deforms (dTh0=0.169) and the mode u re-solves each outer.

### F) OVER/UNDER-CLAIM AUDIT — **STANDS (no material over-claim)**
- The doc does NOT claim a discrete mass ladder; it explicitly identifies the box modes
  as box-controlled and the intrinsic content as the already-banked l(l+1) charge
  barrier (not new). Correct.
- The doc CORRECTLY leaves open SCOPE COST #2: the live mode tested is the ROUND
  radial breather — the TIME axis is genuinely live, but the SPATIAL non-roundness is
  the round-profile reduction; a full non-round l>=2 live-time mode was NOT solved. This
  is flagged prominently (§4, §5.2, §6) and the verdict is explicitly SCOPED to the
  round-breather time-live sector. Not over-stated.
- Minor imprecision (not material): the §2 grep is described as "exit 1 / empty" when it
  actually exits 0 on comment matches; the load-bearing claim (no m*π code BC) is true.
- The consistency claim with `depth_selector_breather_results.md` is legitimate: that
  same-day reduced U(D) model reached the same "half-well / tachyon cap / ~1 boundary
  state" and EXPLICITLY left the fully-coupled nonlinear back-reaction OPEN; this push
  closes exactly that gap. Caveat (fair): both share the round-breather reduction, so
  they are not independent on the spatial-non-roundness axis — but the doc already names
  that as the residual scope cost, so no over-claim.
- COMPROMISE #4 (pressure proxy pr_tot = pr_static + rho_kin as an upper bound) is
  honestly flagged and shown non-load-bearing for the Gate-A scaling verdict. Confirmed:
  the box-control is about ω²'s R-scaling, robust to the pressure proxy.

---

## NET

**The SCOPED NEGATIVE verdict STANDS.** Every load-bearing claim reproduces under
independent re-runs (calibration M_MS=0.281; back-reaction max|da|=1.01, max|dTh0|=0.17;
A=0 and A=4 both 1/R² box-controlled with cell-doubling quartering ratios 3.68 and 4.11;
grid spread 0.44%). The back-reaction is genuinely finite-amplitude (not void), it is
ACTIVE and DIFFERENT from the A→0 proxy, and it does NOT open a new bound level — it
softens toward a tachyon. Gate A fails for a new intrinsic level; Gate B passes
(grid-converged → real verdict, not a stall). No data number is loaded; B=1/A is not
over-imposed; matter is not frozen. The one genuine judgment call — pinning core=π — is
a legitimate node value selecting the deg-1 homotopy class (not an `m*π` Skyrme ladder),
correctly flagged as a topological-sector CHOICE, and the free-node unwinding is shown.
The verdict is appropriately SCOPED to the round-breather time-live sector, with the
spatial-non-roundness (l>=2 live-time) reduction honestly left open as the residual cost.

Caveats for Charles (none blocking): (1) the §2 grep "exit 1/empty" phrasing is imprecise
(it exits 0 on comment hits); harmless. (2) the result and the same-day reduced U(D)
breather share the round-breather reduction, so the spatial-non-round axis remains the
genuine open frontier — the doc says so. (3) GPU was degraded by my own concurrent runs
mid-session; final numbers are from isolated GPU + CPU cross-checks and agree.
