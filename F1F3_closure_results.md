> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE scalar-tensor ("vacuum≠GR from box-f", a(φ)=e^{+φ}, free-X) operator, superseded 2026-07-01 by the native
> constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in this sweep (armchair closure record).
> Its 'scalar-tensor resolution' headline is stale — native frame has EH=boundary term + φ-blind matter; the EH-not-native dispositions
> align with the native result.

# F1 + F3 CLOSURE RECORD — tying off the gravity-action + a(phi)-coupling foundation

**Mode:** OBSERVE, DATA-BLIND, READ-ONLY on committed docs (this is the ONLY new file).
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21.
**Status:** UNVERIFIED closure record — record-candidate, ATTACK-HERE block at the end;
a blind adversarial pass is required before this is treated as banked. **NOT canon.**
**Compute:** none new (this is a closure/disposition record over already-machine-checked
results); no solves run. Bounded analytic confirmation only by re-reading the chains.

**Purpose (Charles's "finish everything" directive):** F1 (gravity curvature action)
and F3 (the a(phi) rest-mass coupling) are RESOLVED — both DERIVED this session. This
record ties off their hanging residuals to a CLEAN state: it (1) confirms the derivation
chain is airtight and re-states the FORCED-vs-OPEN split crisply; (2) formally closes
each superseded gravity-side residual from F0 (N1, N4, N5, N6, N7, N8) with a disposition;
(3) documents the FREE X dial as the one principle-unfixed parameter (honest open, not a
smuggled value); (4) closes "a=-1 silently used in P1-P5d" by pointing to the re-audit.

**Sources (all committed, read this session):**
`native_dilation_weight_derivation_results.md` (the derivation + its embedded Sec 9
verification), `matter_regrade_derived_operator_results.md` (+ its embedded VERIFICATION
block, agent a4aa12aa522f06b6c), `F0_SYSTEMATIC_AUDIT_results.md` (the N1-N8 gravity-side
items + verifier verdicts), `branch_G_characterization_results.md` (the X-window + "does
anything fix X" finding), `P1P5_reaudit_vs_derived_operator_results.md` (the a=-1
downstream impact), `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (the scoreboard + F1/F3 entries).

---

## 1. THE DERIVATION IS AIRTIGHT — confirmation + FORCED/OPEN split (crisp)

I re-walked the R1-on-the-action chain and the R2/R3 cross-checks; the chain HOLDS, with
exactly the conditional steps named below. I did NOT re-derive from scratch — I confirmed
each link and tagged where a step is conditional.

### The chain (each link confirmed)
1. **Ground truth (DERIVED, corpus):** metric form `g_tt=-e^{-2phi}c^2`, `g_rr=e^{+2phi}`,
   angular `r^2 dOmega^2`, reciprocity `g_tt g_rr = -c^2` (B=1/A). Re-verified the induced
   transformation under `phi -> phi+lambda` (lambda const): the (t,r) "gradient block"
   scales `e^{-2lambda}/e^{+2lambda}`, the angular block AND `sqrt(-g)=c r^2 sin(theta)`
   are INVARIANT (the dilation factors cancel under B=1/A). This is NOT a uniform conformal
   rescaling — it acts on the gradient block only. **Every weight is derived from THIS
   actual induced transformation, not from an imported conformal-weight table.**
2. **The lever (P3, CHOSE — flagged visible):** R1-on-the-action = invariance under the
   GLOBAL constant shift `phi -> phi + const`. NOT full local Weyl (that washes phi out —
   wrong), NOT dropped (that gives back plain EH — wrong). The constant mode is gauge; the
   varying part stays physical. **This is the ONE interpretive premise the derivation
   rests on**, blessed by Charles, named P3. The angular obstruction (below) PROVES phi is
   not washed out, which is the internal check that P3 is the constant-shift reading and
   not a smuggled local Weyl.
3. **The universal rule (DERIVED):** weight each term by the EXACT INVERSE of its own bare
   constant-shift weight. ONE rule; the exponent per term = the number of metric/clock
   factors it carries. This yields:
   - **Kinetic weight `e^{+2phi}`** (the depth-field kinetic couples to `g^{rr}~e^{-2phi}`,
     two metric powers). [DERIVED, script 1]
   - **Rest-mass coupling `a(phi)=e^{+phi}`** (a point particle's `dtau` carries one clock
     power `sqrt(-g_tt)~e^{-phi}`). [DERIVED, script 2] — **this is F3's answer.**
   - **Gradient-sector curvature weight `e^{+2phi}`** = SAME as kinetic (geometry and
     depth-field share one weight on this sector). [DERIVED, scripts 3-5]
4. **The central finding (DERIVED):** R carries TWO shift-weights at once (0 from the
   phi-free angular `2/r^2`, and `-2lambda` from the gradient/frame pieces). **No single
   power weight can homogenize it** — `e^{+2phi}` fixes kinetic + gradient curvature but
   leaves the angular `2/r^2` term picking up `e^{+2lambda}`. The angular curvature is the
   one place a depth scale can legally enter. (Conditional on premise P7' — "the shift acts
   at fixed invariant SO(3)-orbit area" — which the verifier confirmed is chart-independent
   and physically the right choice, now NAMED.)
5. **R2 cross-check (DERIVED, ANALYTIC):** a weight that is itself a clock/ruler dilation
   must compose by the same Cauchy equation that forced g_tt -> every weight is a PURE
   EXPONENTIAL (no polynomial admixture). R2 REFINES the FORM, does NOT fix the exponent.
   CONFIRMS R1, no over-determination.
6. **R3 cross-check (DERIVED, script 6):** B=1/A is UPSTREAM of the kinetic exponent — it
   is precisely B=1/A that makes `g^{rr}=e^{-2phi}`, sourcing the `+2`, and it EXPLAINS the
   `+2`-vs-`+1` anisotropy (inverse-metric two powers vs clock one power). CONFIRMS R1.

### Verification status of the chain
Both the derivation doc (Sec 9: blind adversarial verifier agent `aa01430609f471615`,
Ricci cross-chart-validated to 1e-12; blind independent re-derivation agent
`af91bb6b7fdf512b6`) and the matter re-grade (VERIFICATION block, agent
`a4aa12aa522f06b6c`) returned **SUPPORTED** (the weight doc: SUPPORTED-WITH-REVISIONS,
the revisions now folded in). Every symbolic claim was reproduced; no fatal refutation.

### FORCED (pinned by R1, confirmed by R2/R3 — NOT open)
- Depth-field kinetic weight = **`e^{+2phi}`**.
- Rest-mass coupling = **`a(phi)=e^{+phi}`** (power +1; STATIC worldline — see conditional).
- Gradient-sector curvature weight = **`e^{+2phi}`** (same as kinetic).
- The universal RULE (weight = exact inverse of bare shift-weight; exponent = valence).
- R2 -> every weight a pure exponential; R3 -> sources the `+2` and the `+2`-vs-`+1` split.
- **BIRKHOFF BROKEN:** non-constant weight + two independent players -> `box f = 2phi''+4phi'/r`
  survives in vacuum -> **vacuum != GR**. Robust to the exact power. (This is F1's teeth.)
- **a(phi) is NOT -1** — F3 answered; the coupling is FORCED by the same rule that fixes
  the geometry weight. F1 and F3 untie TOGETHER (as N7 predicted).

### CONDITIONAL steps (named, not hidden — each is an honest premise, not a gap)
- **P3** (the constant-shift reading of R1-on-the-action) — CHOSE, the interpretive lever.
  The whole derivation rests on it. Internally checked (the angular obstruction proves it
  isn't local Weyl); externally it is Charles-blessed. This is the load-bearing premise.
- **P7'** (the shift acts at fixed invariant orbit-area) — CHOSE, physically justified,
  chart-independent (verifier-confirmed). Carries the "angular sector is special" conclusion.
- **a(phi)=e^{+phi} is STATIC-ONLY at the headline level.** For a moving worldline the
  three blocks scale `e^{-2λ}/e^{+2λ}/1` and NO single a(phi) restores invariance (same
  anisotropy obstruction that hits the angular curvature). The terrestrial cross-check
  PASSES and is banked: the observable `m c^2 a(phi) dtau/dt = m c^2 e^{phi} e^{-phi} = m c^2`
  is depth-INDEPENDENT — `e^{+phi}` is exactly the NO-ANOMALY value (the depth-flat choice),
  so a *function* `e^{phi}` does NOT conflict with the constant-a!=-1 terrestrial warning.

### OPEN (under-determined — reported, not forced; see Sec 3 + Sec 4)
- The **angular-curvature obstruction fork** (Branch G gauge-it-away vs Branch P keep-it-physical).
- The **kinetic/curvature ratio X** (one continuous dial; Sec 3).
- Whether the admitted non-trivial vacuum yields DISCRETE structure (a SOLVER question,
  not an F1/F3 question — answered NO classically on the derived operator by P5e_proper/STEP2).

---

## 2. FORMAL CLOSURE OF THE F0 GRAVITY-SIDE RESIDUALS (N1, N4, N5, N6, N7, N8)

Each F0 gravity-side item (N1-N8) is disposed below. The unifying fact: **the gravity
operator is now DERIVED from R1 (a two-player scalar-tensor operator with `vacuum != GR`),
not SELECTED as the assumed Einstein-Hilbert tensor.** Most residuals were artifacts of the
old "assumed-EH, single-player, slaved-phi" frame and dissolve under the derivation.

### N1 / N5 — "c slaved to phi" / "one-player, metric determined by phi" -> **CLOSED**
- **N1** (c slaved to phi, not an independent field) and **N5** ("metric-determined-by-phi",
  phi slaved, single DOF — the variational constraint behind the legacy C1 action).
- **Disposition: CLOSED by the TWO-PLAYER move.** The derivation treats phi and the metric
  as INDEPENDENT dynamical players (premise P4, Charles ruling 2026-06-21); the corpus's
  slaving `phi=-1/2 ln(-g_tt)` is NOT used at any step. With phi independent, the action
  class and field equations are the two-player scalar-tensor ones, and `box f` survives in
  vacuum (the whole `vacuum != GR` result is a DIRECT consequence of un-slaving). N1/N5
  named the slaving as the smuggled single-DOF assumption; the derivation does not make it.
  **Confirmed CLOSED** (ledger scoreboard already records N1/N5 RESOLVED via two-player).
- Residual scope note: N1's "varying-c absorbable" verdict was scoped to "c slaved to phi";
  that scope is now simply not the live theory (two-player), so the scoped verdict is moot,
  not contradicted.

### N7 — "F1 and F3 are entangled (the absorbability presupposes EH)" -> **CLOSED**
- **N7** (F0): the Bianchi argument that makes any matter weight `e^{(a+1)phi}` absorbable —
  and thereby "defangs" a(phi) and licenses a=-1 — PRESUPPOSES the EH left side. So a(phi)
  cannot be settled while the curvature action is open. Take F1 and F3 TOGETHER.
- **Disposition: CLOSED by taking them together — which is exactly what the derivation did.**
  R1 fixes the curvature weight (`e^{2phi}`, vacuum!=GR) and the rest-mass coupling
  (`a=e^{+phi}`) by the SAME rule in ONE derivation. The entanglement was honored, not
  worked around. Downstream confirmation (matter_regrade, blind-verified): the derived
  operator's divergence `nabla^mu E_munu = -(1/2)EOM_phi phi' != 0` identically, so the EH
  Bianchi tautology that N7 flagged as the load-bearing step is DEAD — there is no relabeling
  that makes the weighted matter stress conserved. **a(phi)=e^{+phi} is PHYSICAL** precisely
  because F1 changed (the teeth come from the OPERATOR, not from a=+1 vs -1). N7's
  prescription ("settle them together") is satisfied; **CLOSED.**

### N4 — "legacy C1 'uniqueness' only within analytic classes + Schwarzschild fed in" -> **SUPERSEDED**
- **N4** (F0): the legacy C1 action's "uniqueness" was claimed only WITHIN analytic function
  classes AND fed Schwarzschild vacuum in as an admissibility INPUT (a circular-risk
  selection: the answer "EH/Schwarzschild" was partly assumed to pick the action).
- **Disposition: SUPERSEDED — N4 no longer bites.** N4 was a critique of a SELECTION argument
  (C1 chosen by uniqueness-within-a-class, with Schwarzschild admissibility as an input). The
  operator is **no longer selected — it is DERIVED from R1** as the inverse-shift-weight on
  each action term. The derivation does not invoke any "uniqueness within analytic classes,"
  and it does NOT feed Schwarzschild in: on the contrary, it OUTPUTS `vacuum != GR` (box f
  survives), so Schwarzschild is no longer an input OR the generic output. The circular-risk
  (assume Schwarzschild -> get EH -> get Schwarzschild) is broken at its root because the
  derivation's vacuum is a `{m,q}` scalar-tensor family, not Schwarzschild. **N4 critiques a
  superseded construction; it carries NO blocking authority over the derived operator.**
  (Precisely: N4 attacked the provenance of the assumed-EH action; that action is no longer
  the live gravity action.)

### N6 — "asymptotic-flatness branch selection vs finite-cell 'no spatial infinity'" -> **DISSOLVED (scoped)**
- **N6** (F0): "asymptotic flatness pins the vacuum branch (A=1, Schwarzschild over the
  negative-mass Branch-I)" is in TENSION with the finite-cell canon's "no spatial infinity"
  — the branch-selection BC lives at an infinity the finite-cell frame denies.
- **Disposition: DISSOLVED for the derived operator; what remains is a finite-cell BC choice,
  not a tension.** N6 was a tension between (a) an asymptotic-flatness branch-selection rule
  used to pick the OLD EH-vacuum branch and (b) the finite-cell canon. Two things dissolve it:
  1. The derived vacuum is NOT a single Schwarzschild branch selected by asymptotic flatness —
     it is a two-parameter `{m, q}` scalar-tensor family (Branch G), parameterized by two
     continuous integration constants. There is no longer a discrete "Schwarzschild vs
     negative-mass Branch-I" choice forced by an `A=1` condition at infinity; the family is
     continuous and the integration constants are fixed by the cell's ACTUAL boundary (the
     seal), not by behavior at a denied spatial infinity.
  2. The seal/boundary is the finite-cell's own BC surface (F4: derived seal-fold, both
     involutions give a CONTINUOUS junction — seal_junction_condition_results). So the
     vacuum branch is fixed by the finite-cell seal data, which is exactly where the
     finite-cell canon says the BC lives. The asymptotic-flatness rule N6 worried about is
     simply not used by the derived operator + finite cell.
- **Scope (honest):** what is NOT yet done is the explicit `{m,q}` selection from the seal
  junction on the derived operator (a NEEDS-A-SOLVE item — the bounded coupled re-run, flagged
  in matter_regrade Sec 6). So N6's TENSION is dissolved (the asymptotic-infinity branch rule
  is gone), but the CONSTRUCTIVE replacement (seal-data fixes {m,q}) is characterized, not yet
  numerically executed. **N6 disposition: DISSOLVED as a tension; the replacement BC is a
  named solve, not a hanging contradiction.**

### N8 — "local-Lorentz / local-c held universal INCLUDING at the extremes" -> **SCOPED (still an admitted premise)**
- **N8** (F0): local-Lorentz invariance / local-c-constant (Sense-1) was held universal,
  INCLUDING at the deep/extreme regimes UDT targets; if local physics is modifiable at depth,
  the absorbability lemmas (and more) could void.
- **Disposition: SCOPED — partially RELIEVED, but local-Lorentz at the extremes REMAINS an
  admitted premise of the derived operator.**
  1. The specific WORRY N8 attached to ("if local physics is modifiable at depth the
     absorbability lemmas void") is now MOOT in the direction that mattered: the absorbability
     lemma is ALREADY dead (N7/matter_regrade) for an independent reason (vacuum != EH). So
     N8 can no longer void a lemma that no longer holds.
  2. HOWEVER, the derivation itself ASSUMES local-Lorentz structure: the metric FORM
     (CANON C-2026-06-18-1) was derived from "remain relativistic" = local-Lorentz holds; the
     point-particle `dtau = sqrt(-g_tt)/c dt` used to fix `a(phi)=e^{+phi}` presumes a local
     light-cone (local-c) at the particle. So local-Lorentz/local-c IS still assumed by the
     derived operator, and it is assumed to hold at all depths.
  3. The known LIMIT (P1P5_reaudit (ii), M7): the deep core `phi -> -inf` (where `e^{-2phi}`
     is O(5)+ and a(phi) would depart O(1)) is never honestly reached numerically (core cutoff
     rc=0.05). So "local-Lorentz holds at the extremes" is an assumption that has NOT been
     stress-tested in the deepest regime.
- **N8 disposition: SCOPED, NOT closed.** Local-Lorentz/local-c at the extremes is an
  ADMITTED foundational premise of the derived operator (it descends from the "remain
  relativistic" metric derivation, CANON C-18-1). It is no longer a THREAT to a specific
  lemma (the lemma is gone), but it is a standing assumption to flag — recorded here so it is
  visible. (This is consistent with the ledger's note that N8 is "largely SUPERSEDED-by-
  derivation" — the threat is superseded; the underlying premise is retained, not derived
  away.) **It does not block F1/F3 closure but is named as a retained premise.**

### N2 / N3 — for completeness (not gravity-action residuals of the derivation)
- **N2** (mu^2=pi/3 fit to mesons): RESOLVED-quarantined (LEGACY-only, not in the live
  program). Not used by the derived operator. Out of F1/F3 closure scope; flagged so it never
  re-enters. **N3** (the "two incompatible gravity actions" scare): verifier-REFUTED (false
  alarm; C1 <=> EH+minimal-scalar, identical field equation; the one non-EH alternative was
  Cassini-killed and explicitly not banked). Both already CLOSED in the scoreboard.

---

## 3. THE FREE X DIAL — the ONE principle-unfixed parameter (honest open)

**Statement:** the kinetic-to-curvature ratio **X** (the relative coefficient of the bare
kinetic term `X e^{2phi}(dphi)^2` and the curvature term `e^{2phi} R`) is a single,
continuous, dimensionless parameter that **R1, R2, and R3 do NOT fix.** This is an HONEST
OPEN PARAMETER, not a smuggled value.

- **Why it is genuinely free [DERIVED, branch_G Sec 3]:** R1/R2/R3 fix that BOTH the kinetic
  and the curvature term wear the SAME weight `e^{2phi}`, but X is the ratio of two
  coefficients that both already wear that weight — the shared weight is pinned, the ratio is
  not. X is dimensionless. Nothing in Branch G's action, its vacuum solutions, or any
  self-consistency condition picks a point.
- **What constrains X (INEQUALITIES, never a value):**
  - **No-ghost** (Einstein-frame health, `2omega+3>0`, `omega=-X/4`) => `X < 6` (large
    POSITIVE X is a GHOST, forbidden).
  - **Cassini** (`|gamma-1| = 4/|X-8| < 2.3e-5`) => `|X-8| > 1.74e5` => `X < -1.7e5`.
  - **Healthy + Cassini-safe window = the half-line `X <~ -1.7e5`** (X large NEGATIVE).
- **So X is ONE-SIDED, not a two-sided family:** large positive X is a ghost (excluded),
  large negative X is HEALTHY and gives `gamma -> 1` (clears Cassini; `gamma-1 ~ -2e-5` at
  `X=-2e5`). The old `f(phi)R` `gamma=9` death does NOT transfer (different exponent +2 not
  -8, intrinsic bare kinetic present, phi unslaved). A healthy Cassini-passing window EXISTS.
- **This is NOT a smuggled value.** No step of the derivation, and no banked result, fixes X
  to a number or tunes it toward "passes Cassini." The honest status: the theory is a smooth
  one-parameter (X) family, bounded to the half-line `X <~ -1.7e5` by ghost+Cassini, with
  NOTHING internal selecting a point on it. At large |X| the theory -> GR + a weakly
  (1/X)-coupled massless scalar with 1/r hair (the decoupling limit).
- **What could fix X later (honest, not promised):**
  - **F7-side / cosmic anchoring:** X sets how strongly the scalar couples; a cosmic
    observable sensitive to the scalar's strength (lensing, growth, the CMB consilience
    roadmap) could in principle pin X from data — but that is DATA-fixing, not principle-
    fixing, and is gated behind the data-blind posture.
  - **A deeper internal principle not yet found** (e.g., a quantization/improvement-term
    condition, or the conjectured scale-symmetry conserved charge once its improvement term
    is built — scale_symmetry_bootstrap flagged that charge as a CONJECTURE). None exists now.
  - **Honest default:** until one of those lands, X stays a FREE DIAL within the healthy
    half-line. This is the cleanest possible state for an unfixed parameter: bounded,
    one-sided, named, and not tuned. **F1/F3 closure does NOT require fixing X** — it requires
    naming it as the one principle-unfixed parameter, which is done here.

---

## 4. "a=-1 SILENTLY USED IN ALL P1-P5d" — CLOSED (pointer)

- **The silent fact (F3 ledger entry):** every P1-P5d solve used `a=-1` (matter weight = 1,
  the GR-coupled baseline). With `a(phi)=e^{+phi}` now DERIVED (matter weight `e^{2phi}`),
  that baseline is superseded.
- **Disposition: CLOSED — the downstream impact is fully covered by
  `P1P5_reaudit_vs_derived_operator_results.md`.** That re-audit classifies every P-result
  (INTACT machinery / SUPERSEDED-BUT-REESTABLISHED / CHANGED / UNCHECKED-GAP). Summary of its
  findings relevant here:
  - **CHANGED:** P3 (the largest — `a=-1` absorbable baseline OVERTURNED; `a=e^{+phi}` derived
    and physical; curvature side not GR); the soliton EXTERIOR (-> scalar-tensor `{m,q}` hair,
    B=1/A breaks once hair is live); every `M_MS` mass NUMBER read at `a=-1`+EH (needs re-run —
    data-blind, never banked as physics).
  - **SUPERSEDED-BUT-REESTABLISHED:** P5d (round time-live continuum) and the off-round
    box-control gate (P5e) were RE-RUN on the derived operator (STEP2 + P5e_proper) and the
    "discreteness requires quantization" headline SURVIVES on `vacuum!=GR` + physical matter.
  - **INTACT (operator-agnostic machinery):** P1 off-diag wiring, P2 carrier/EL + L2/L4
    native-ness + S2-vs-S3 settlement + charge, P4 time-wiring, P5a/a'/b numerics.
  - **The loud UNCHECKED-GAP (carried, not part of F1/F3):** P5c's multi-basin family/stability
    landscape was never re-run on `vacuum!=GR` + `a=e^{phi}`. This is a SOLVER gap (a later
    bounded re-run), NOT an F1/F3 foundational hole.
- So the "silent a=-1" is no longer silent: it is named, the value is derived, and every
  downstream result is graded. **F3's silent-load-bearing-fact is CLOSED** (pointer-resolved
  to the re-audit; nothing in F1/F3 hangs on it).

---

## 5. PREMISE LEDGER (this closure record)

| # | Premise / claim | Status |
|---|---|---|
| C1 | The R1-on-the-action derivation chain holds as written | CONFIRMED (re-walked; both prior verifiers SUPPORTED) |
| C2 | P3 (constant-shift = R1-on-action) is the load-bearing interpretive lever | CHOSE (Charles-blessed; the one premise the whole chain rests on) |
| C3 | P7' (shift at fixed invariant orbit-area) | CHOSE, chart-independent (verifier-confirmed upstream) |
| C4 | a(phi)=e^{+phi} is STATIC-ONLY at headline; terrestrial cross-check passes | DERIVED+CONDITIONAL (named restriction, banked) |
| C5 | N1/N5 closed by two-player; phi independent, slaving not used | DERIVED upstream; CONFIRMED CLOSED |
| C6 | N7 closed by deriving F1+F3 together; absorbability tautology dead (nabla E != 0) | DERIVED upstream (matter_regrade, blind-verified); CONFIRMED CLOSED |
| C7 | N4 superseded — operator DERIVED from R1, not selected by uniqueness-within-class; Schwarzschild not fed in (vacuum!=GR is OUTPUT) | DERIVED (disposition); N4 loses blocking authority |
| C8 | N6 dissolved — vacuum is continuous {m,q} family fixed by seal data, not asymptotic-flatness branch rule; explicit seal->{m,q} solve is a NAMED solve | DERIVED (structure) + NEEDS-A-SOLVE (the explicit selection) |
| C9 | N8 scoped — local-Lorentz/local-c at extremes is a RETAINED admitted premise (descends from C-18-1); its threat-to-the-lemma is moot (lemma already dead) | ADMITTED (retained premise, named, not derived away) |
| C10 | X (kinetic/curvature ratio) is the ONE principle-unfixed parameter; bounded to X<~-1.7e5 by ghost+Cassini; no value smuggled | DERIVED (X free) — honest open parameter |
| C11 | "a=-1 in P1-P5d" downstream impact fully graded | DERIVED upstream (P1P5_reaudit); CONFIRMED CLOSED (pointer) |
| C12 | This record runs no new compute; it disposes already-verified results | METHOD note |

---

## 6. WHAT REMAINS GENUINELY OPEN IN F1/F3 (the honest residue after closure)

After this closure, F1 and F3 are RESOLVED (derived + verified) and their residuals are
disposed. What remains is NOT a hole in the derivation — it is the named open frontier:

1. **The free X dial** — bounded (`X <~ -1.7e5`), one-sided, but UNFIXED by R1/R2/R3. The one
   principle-unfixed parameter of the gravity sector. Could be fixed later by data (F7/cosmic
   consilience) or by a deeper internal principle not yet found. (Sec 3.)
2. **The Branch G vs Branch P fork** — whether the angular-curvature potential is gauged away
   (Branch G, clean scalar-tensor) or kept physical (Branch P, the phi-angular discreteness
   hunch). R1/R2/R3 do not decide; both are being characterized (Branch G done; Branch P is the
   live hunch line). This is a DIRECTION choice, not a flaw in the derivation.
3. **a(phi)=e^{+phi} is static-headline** — the moving-worldline weight is anisotropy-obstructed
   (no single a(phi) for a geodesic); the terrestrial no-anomaly cross-check passes, but the
   moving-particle coupling is characterized as obstructed, not given a single closed form.
4. **N8's retained premise** — local-Lorentz/local-c assumed to hold at the deepest extremes
   (`phi -> -inf`), never numerically stress-tested there (core cutoff rc=0.05). A named premise,
   not a derivation gap.
5. **NEEDS-A-SOLVE (not F1/F3 foundational, but the constructive completions):** the explicit
   seal -> `{m,q}` branch selection on the derived operator (N6's replacement BC); the quantitative
   coupled soliton on `vacuum!=GR`+`a=e^{phi}`; P5c's family landscape re-run (the loud P1P5_reaudit
   gap). All bounded later solves, gated; none reopens F1 or F3.

**One-line closure:** F1 and F3 are DERIVED TOGETHER from R1-on-the-action (`vacuum != GR`,
`e^{2phi}` weights, `a(phi)=e^{+phi}`), verified twice; N1/N5/N7 are CLOSED (two-player +
derive-together), N4 is SUPERSEDED (operator derived, not selected), N6 is DISSOLVED (continuous
`{m,q}` family fixed by seal data, not asymptotic-flatness), N8 is SCOPED (retained local-Lorentz
premise, threat-to-lemma moot); the only principle-unfixed parameter is the one-sided, bounded,
honestly-open X dial; and the silent `a=-1` is fully graded by P1P5_reaudit. **F1/F3 are CLEAN.**

---

## 7. ATTACK HERE (for the blind verifier — required before banking)

1. **Is the derivation chain ACTUALLY airtight, or does this record overstate "confirmed"?**
   Re-check that P3 (constant-shift) is the ONLY interpretive lever and that the FORCED items
   (e^{2phi}, a=e^{+phi}, vacuum!=GR) genuinely follow from it without a second hidden choice.
   In particular: does "vacuum != GR" depend on X being non-zero, or on the SHAPE of f only?
   (Confirm box f = 2phi''+4phi'/r is X-independent — the Birkhoff break should not need X.)
2. **N4 disposition — is "superseded, no longer bites" correct, or does the derivation SECRETLY
   re-import a uniqueness-within-class or a Schwarzschild admissibility step?** Check the
   derivation never feeds Schwarzschild in as an input (it should OUTPUT vacuum!=GR).
3. **N6 dissolution — is the {m,q} family REALLY fixed by the finite-cell seal, or is an
   asymptotic-flatness condition still smuggled in to fix one of {m,q}?** This is the riskiest
   disposition: confirm no spatial-infinity BC is used by the derived operator's vacuum.
4. **N8 — is local-Lorentz REALLY still assumed by the derived operator, or did I overstate the
   retention?** Check the a(phi)=e^{+phi} derivation's use of dtau=sqrt(-g_tt)/c dt (a local
   light-cone). And confirm the "threat-to-the-lemma is moot" claim (the absorbability lemma is
   independently dead, so N8 can't void it).
5. **X free — does ANY constraint I missed fix X to a value** (not just bound it)? Re-derive the
   no-ghost X<6 and Cassini X<-1.7e5; confirm both are inequalities and nothing internal selects
   a point. Check the claim that large-positive-X is a ghost (sign of 2omega+3).
6. **Did this record CLOSE anything that should stay OPEN?** Especially: is N6 truly dissolved
   or merely deferred (the explicit seal->{m,q} solve is unrun — is calling the tension
   "dissolved" premature)? Is N8 "scoped" honest or should it be "OPEN"? Grade the dispositions
   for over-closure (the failure mode of a "finish everything" record).
7. **Pointer integrity:** confirm P1P5_reaudit_vs_derived_operator_results.md actually grades the
   a=-1 downstream impact as summarized in Sec 4 (P3 CHANGED, P5d/P5e REESTABLISHED, P5c gap).
---

## VERIFICATION (2026-06-21) — blind over-closure pass, agent a45d3c75a8520bba9
VERDICT: CLEAN — honest tie-off, open residuals kept visible, no over-closure.
Specific: N6 disposition accepted as "DISSOLVED (tension) + NAMED-SOLVE (seal->{m,q} unrun)"; minor phrasing nit
("seal data fixes {m,q}" slightly oversells the seal — seal_junction shows it gives a CONTINUOUS BC selecting no
fixed radius — neutralized by the NEEDS-A-SOLVE tag, no over-closure). N8 correctly SCOPED (retained admitted
premise), free-X honestly OPEN (X-window inequalities independently recomputed), FORCED/OPEN split accurate.
