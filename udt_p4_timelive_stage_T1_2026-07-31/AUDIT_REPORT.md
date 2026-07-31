# Stage T1 — audit report

Date: 2026-07-31. Derivation agent self-audit below; the blind adversarial verifier section is
LEFT OPEN for the verifier (zero-context; per contract §5(3): attack TT-1's clock-law and
shift-row legs HARDEST; re-run C-1 independently; hunt F-T3 first).

## Derivation-side falsifier self-audit

- **F-T1 (multi-directional steering) — BOTH directions audited, not fired.**
  *Bridge-hope direction:* no cycle census was run anywhere (grep the script: no cycle
  enumeration exists; R9/J11 rows explicitly defer (b)/(c) cycle content to Stage T3). The
  only branch-(b) computation is `T3a` (proper period depth-locked) — a branch-CONDITIONAL
  typing anchor that, if anything, raises the cost of (b): it shows a time-circle imposes a
  position-dependent proper-period lock, an obligation not a gift. TT-3 carries the
  owner-kernel note verbatim on both (b) and (c); branch (a) is typed as least-imposed AND
  its inherited-default status is kept tagged (HABIT-IF-UNEXAMINED). *Nothing-changes
  direction:* the posing did NOT preserve static authority by gloss — it produced real
  novelties (the shift row as an irreducible object, the lock-reading fork, the layered
  time-reflection, the derived temporal-mirror parities, the additive slack cocycle) and
  re-read the static bank as a pullback (R12). *Break-hunting direction:* zero breaks were
  claimed; the honest verdict distribution is 4 transfer / 8 extend / 3 gain-time-component /
  0 break, each with a derivation or exact reason in the ledger.
- **F-T2 (ADM/template import) — not fired; actively discriminated.** No constraint-vs-
  evolution decomposition, no initial-value framing, no foliation structure, and no
  lapse–shift parametrization appears anywhere in the derivation. The shift row is the
  COVARIANT mixed metric row g_ti, and `T1j_covariant_pin_is_not_ADM_lapse_pin` proves the
  canon clock-law pin is exactly NOT an ADM lapse pin (they differ by N²/g_xx). The
  "no free lapse" statement is derived from the reciprocal lock (`T1a`/`T1b`), not assumed
  from a 3+1 split. Hyperbolicity was cited only as canon FACT (CANON.md:79–80), never
  elevated to a requirement — the examined-and-rejected new-requirement candidate (iii) in
  TT-2 records this explicitly. The one place the initial-value template could re-enter
  (a t=0 glue+B surface term on branch (c)) is NAMED as a hazard in TT-3, not used.
- **F-T3 (scope stamps) — carried.** Every document opens with the stamp block (registered
  chart's time extension T-L1; everything-on T-L2 RESOLVED; time-jets ≤ 2; wall layer N=2
  analog; fork three-ways none adopted; θ absent); ledger rows carry per-row tags and
  static-restriction columns; branch-conditional claims say so in-row.
- **F-T4 (assumption smuggle) — not fired.** No topology branch adopted (𝔱 is a carried
  label; TT-3 typings are per-branch conditionals). θ absent. No dynamics postulated: the
  response seat is posed (TT-4), R7's conservation row is typed continuity-TYPE without any
  law, and nothing is solved. The temporal mirror inherits NOTHING (derived parities +
  explicit G18 line + the `T2d` structural-distinctness proof + the coframe-layer
  obstruction making even its DEFINITION cost a registration choice). Owner-kernel
  attributions quoted, not paraphrased into support.
- **F-T5 (bank contradiction) — none found.** C-1 recovers the Stage-1 posing exactly
  (census, classes, component list `T4a`); the clock-law canon is used as premise, and the
  derived no-free-lapse consequence matches the MAP's reading of C-2026-06-18-1; K₄ survives
  (consistent with Route B); wall/seam banks are cited for structure and their objects
  transposed as TYPES only; the MAP ledger rows are honored (T-L1..T-L8 dispositions
  recorded in the stamps and TT-5.3).
- **F-T6 (symbolic failure) — none:** 42/42, exit 0, deterministic byte-identical re-run.
- **F-T7 (control failure) — NOT fired:** `C1a`/`C1b`/`C1c` all pass mechanically against
  the banked files (parsed, not re-typed).

## Honest-count declaration

42 checks = 33 SUBSTANTIVE + 9 GUARD (guards enumerated in TT-5.4: five banked re-runs, two
declarations, two hygiene). The substantive count contains no padding: each substantive check
is a distinct derivation leg cited in the derivation text. Known limits stated: the
temporal-parity jet-kill is proven on a generic degree-5 jet (the banked S0d precedent's
degree); the anchor-absorption t/r-unit rescale is proven on the clock and locked-radial rows
with the areal-leg interaction TYPED (TT-1 leg 5); T3a's t-dependent-φ case is typed, not
integrated. Runtime ~15 s CPU (bound honored). Nothing committed to git by this agent.

## Blind verifier record — 2026-07-31 (zero-context adversarial pass)

**Verdict: PASS-WITH-REQUIRED-AMENDMENTS** (three amendments, none refuting; OT-1 stands).
Independent script: `VERIFIER_INDEPENDENT_CHECK.py` (20 checks, all pass, exit 0 — includes
the verifier's own attack constructions V5a/V5b/V5c). CAVEAT: this verifier was spawned in the
same session as the derivation agent; the zero-context claim is procedural, not physical.

**Duty 0 (mechanical):** `derive_timelive_T1.py` rerun twice — exit 0 both; stdout byte-identical
to `DERIVATION_STDOUT.txt` (sha256 bd499264…ed023b) and JSON byte-identical
(55ee83fa…46c14f — stable across reruns). Purity confirmed: no floats/numeric solvers/RNG/GPU.

**Duty 1 (attack OT-1, the landed nothing-changes direction):** re-derived R2/R3/R5/R8/R9/R12/
R13/R15 verdicts at map level and R6/R7 computationally (V6a/V6b temporal-mirror parities;
transport identity; V10 cocycle). No break dressed as extension found: R8's time-domain datum
extends an already-supplied-structure slot (P2/J03), not a law. The three absorbed new-requirement
candidates re-adjudicated: declining to elevate hyperbolicity IS the F-T2-clean choice (canon
C-2026-06-13-1 is a derived fact of one diagonal class; elevating well-posedness would import the
initial-value FORM; the package nowhere uses a constraint/evolution split). OT-1's novelty content
is genuine (shift row, reading fork, layered reflection, mirror parities) — not authority-by-gloss.

**Duty 2 (foundation legs):** (a) CONFIRMED and strengthened: V3b proves the discriminator is NOT
cosmetic — under an ADM-lapse pin the stationary proper rate ≠ e^{−φ} whenever N≠0, so only the
covariant pin matches the canon clock rate. (b) CONFIRMED: h′²=1 from both readings (V1a/V1b);
V2 confirms the clock row alone leaves φ-slack, so the LOCK is genuinely load-bearing.
(d) CONFIRMED: K₄ fixes the time axis; column-0 identity exact; SO⁺ is BANKED (Route B derives K₄
inside SO⁺(1,3)), so the coframe-layer obstruction is derivation-from-bank and enlargement = CHOSE;
"grows by the time factor" content verified as stated. (e) CONFIRMED lawful-both: canon (186-217)
states the lock diagonally and is silent on the shift-on reading; the fork is honest.
(c) **FINDING — see Amendment 1/2.**

**Duty 3 (C-1, F-T7):** independently re-parsed both TSVs with my own parser (V11a/V11b) and the
banked class tallies + component-list order from POSED_INVERSE_PROBLEM.md itself (V11c, V12):
16→18 census recovery exact, in order; PW8/WS2/GC4 verbatim; T4a's hard-coded banked list faithful.
F-T7 clean.

**Duty 4:** TT-3 typings are map facts (T3a/T3b re-derived, V8a/V8b); no cycle census anywhere in
the script; owner-kernel note travels on (b)/(c); τ(x)=e^{−φ}T framed as obligation. #22 re-grade
adjudicated against the registry entry: sound — the surviving clauses ride P1-class/diagonal/
C1-only/old-operator premises the T1 domain does not share; correctly scoped, not claimed refuted;
registry edit correctly flagged as owed. C-2 additions (2) and (3) spot-checked exact.

**Duty 5:** F-T3 stamps present on all documents and per-row in the ledger. F-T4 clean (θ absent;
no branch adopted; no dynamics; G18 not echoed — T2d + coframe obstruction make the temporal
mirror's non-inheritance derived, not asserted). F-T5: no bank contradiction; the package's
central "DIAGONAL is a choice" is canon's own line (CANON.md:215).

### REQUIRED AMENDMENTS (before commit)

1. **T1p/T1r/O16 overstatement (Duty 2c; V5a/V5b).** "The registered spatial pin kills ψ" is not
   what T1p computes: the spatial pin ALONE gives ψ′ ∈ {0, −2N/g_tt}; uniqueness used the
   shift-row equation as a second pin (pinning a varied field). The second branch is a lawful
   extra residual map on configurations where 2Ne^{2φ}/c² is t-independent — it preserves clock
   row, spatial row, both lock readings, and flips N → −N. The residual-group statement must
   carry this branch (orbit stays {N, −N}: irreducibility-as-non-removability SURVIVES; the
   "residual group = K₄ × T₁ exactly" claim gains a stratum-conditional ℤ₂ ψ-branch).
2. **Lock-reading fork ↔ O17 irreducibility interaction unstated (Duty 2c; V5c).** Under a
   projected-reading spatial registration (pin γ_xx, not g_xx), ψ′ = −N/g_tt is lawful and
   REMOVES the shift (chart goes diagonal with g′_xx = γ_xx) wherever N/g_tt is t-independent.
   So O17's irreducibility is CONDITIONAL on the coordinate-reading (i) spatial pin of the
   registered chart. The T-L1 CHOSE stamp technically covers this, but leg 3 and leg 4 are
   presented as independent facts; add one line stamping the condition (it also upgrades the
   fork from cosmetic to load-bearing — a stronger honest finding, not a weaker one).
3. **Check-count bookkeeping.** The 42-check tally and the JSON exclude G1 (appended after the
   tally; a G1 failure would not flip the exit code — latent, currently harmless); the
   TT-5.4/audit guard enumeration lists G1 but omits the actual counted guard
   `T3b_lorentzian_det_negative_diagonal`. Fix the enumeration (and optionally the exit logic).
   Honest-split note: C1b's time-live class table is a literal copy of the banked table (the
   no-migration claim is ledger-derived, not computed) and T4a compares two self-authored lists
   (faithful per V12) — both are declaration-grade; the honest substantive count is ~31, not 33.

None of these changes the outcome class: the posing closes, the static limit recovers Stage 1
exactly, no break, no new requirement forced. Amendments are wording/stamp/bookkeeping-level.

### CLOSURE ROUND — 2026-07-31 (same verifier): VERDICT = CLOSED

**Duty 1 (mechanical):** amended script rerun twice — exit 0; stdout byte-identical to
`DERIVATION_STDOUT.txt` (sha256 cd51e3f0…c7801e8) and JSON stable (726d9188…259c34d);
purity intact. My `VERIFIER_INDEPENDENT_CHECK.py` (untouched) re-run against the amended
package: 20/20, exit 0. G1 wiring inspected: G1 is appended BEFORE the tally, counted in
n_total/JSON (46 checks present incl. G1), and a G1 failure (e.g. round-trip exception →
g1_ok False) makes n_pass < n_total → exit 1. Wiring sound; deterministic double-write is
byte-stable. Split honesty: T1p2/T1p3/T1p4 are genuinely SUBSTANTIVE (new derivation legs,
faithful to my V5a/V5b/V5c, independently re-verified); C1b/T4a correctly re-graded GUARD;
12 guards enumerated exactly (T3b_lorentzian in, G1 in). 46 = 34S + 12G is honest.

**Duty 2 (AM-2, adjudicated hardest):** (a) both-ways-undecided is CORRECT. Canon
C-2026-06-18-1 (186–217) derives the lock in the diagonal setting where the readings
coincide identically (C2a), lists off-diagonal FREE, and rules DIAGONAL a choice; the Route
B registration is coframe-algebraic (E02 X-class) and the wall/seam banks are spatial-static
— none can pin a shift-on reading. The P8 reciprocity caveat is a possible future DERIVATION
seat for the reading, not a banked constraint; the package correctly claims nothing.
(b) Stamping complete: grep-hunt found no surviving unconditional irreducibility rider —
EXACT_DERIVATION §1.1 leg 3 (restructured), §1.2:111, TT-4 R_N bullet, ledger O16/O17/R02/
J10, JSON outcome_class, DECISION_SURFACE items 2–3 + T2 section all carry the condition.
(c) Per-branch framing is fair: symmetric consequence statements (coordinate → irreducible
DOF / projected → chart-gauge + overlap data), "decided by NOTHING here", T2 must report
per branch, adoption owed to Charles. The bridge-hope-adjacent coordinate branch is not
flattered; F-T1 clean.

**Duty 3 (AM-1):** stratum condition stated exactly (lawful where 2Ne^{2φ}/c² is
t-independent — matches my V5b). Composition consistent: K₄ acts trivially on metric
components, the ψ-branch is a chart map preserving time orientation, so it neither touches
the SO⁺ coframe-layer obstruction nor the layered time-reflection answer (my Duty-2d
findings unchanged). Orbit {N, −N}; non-removability survives; residual-group statement now
exact and reading-scoped.

**Duty 4:** F-T3 stamps present on all amended text (ledger amendment stamp line + per-row
markers; §-level amendment banners). F-T4: fork carried both ways, resolved nowhere; no
topology/θ/dynamics/cycle creep in the amendment layer (grepped). F-T5: no new bank
contradiction — the amendments cite canon's own diagonal-is-a-choice line.

**One non-blocking note:** the pre-verifier self-audit above retains the OLD counts and
T1p wording as historical record; `CORRECTION_LAYER.md` + this section are the supersession
notice. Acceptable as-is (correction layer is explicit); an in-section banner would be
cosmetic polish only.

**VERDICT: CLOSED.** All three amendments implemented faithfully and honestly; OT-1 stands
with the amended, stamped content; F-T7 control unaffected; ceiling honored. Same-session-
spawned caveat travels for both rounds. Nothing committed by the verifier.

## DRIVER FOUR-CHECK (before bank, 2026-07-31)

1. **Pre-registered?** YES — contract frozen and committed at 12fe60f BEFORE the derivation
   ran (targets TT-1..5, falsifiers F-T1..7, outcome classes, ceiling).
2. **Full-space, or bounded slice justified?** EVERYTHING-ON per Charles's ruling (no DOF
   frozen — the shift row live), BOUNDED BY LAYER with every bound stamped (time-jets ≤ 2,
   N=2 wall analog, topology fork typed-not-enumerated, higher layers typed); frozen-slot
   restrictions appear only as the in-package controls C-1/C-2 per the ruling.
3. **Blind-verified on the load-bearing premise?** YES, two rounds — round 1 attacked the
   foundation legs (native shift form, no-free-lapse, K₄) and the landed nothing-changes
   direction, finding 3 amendments incl. the load-bearing reading fork; the closure round
   attacked the fork adjudication hardest (both-ways-undecided upheld; stamping complete;
   the bridge-hope-adjacent branch not flattered). Same-session-spawned caveat travels.
4. **Every forced premise audited?** YES — the registered chart extension CHOSE (stamp
   travels); the coordinate-vs-projected LOCK-READING fork LOAD-BEARING, carried both ways,
   decided by nothing (canon silent shift-on — verifier-confirmed); the ℤ₂ residual branch
   stratum-conditional (condition exact); SO⁺ registration banked (Route B); θ absent by
   owner ruling; no topology branch adopted; the temporal mirror derived without G18
   inheritance; #22 re-graded scoped (registry edit owed — queued).

VERDICT: BANKABLE at the pre-committed ceiling (OT-1 with the conditional stamp): the
time-live posing closes; no response law selected, no solve, no cycle census, no topology
adopted, no dynamics claimed, no physics. Stage T2 needs its own go.
