# BLIND VERIFIER REPORT — udt_p4_period_gate_2026-07-30

Verifier: blind adversarial verifier, **same-session-spawned** agent instance
(zero prior task context; NOT a hosted external model — the same-session caveat
travels with this record). Date: 2026-07-30. Independent script:
`VERIFIER_INDEPENDENT_CHECK.py` (14 groups, ALL PASS, exit 0; own layout, own
routes, adversarial numerics used only as corroboration).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (two bookkeeping amendments; no
substantive claim broken; no falsifier fired)

The claimed MIXTURE outcome (OQ3 sector map + OQ4 no-quantization + Q-A
no-selection) SURVIVES the adversarial pass, including the hardest attacks on the
two owner-pleasing-adjacent legs (quantization silence; sector map). Every
substantive computation I re-derived independently checks out; the cycle census
is complete against the banked R9 spec; no live integer seat was missed.

## Duty 0 — rerun / contract-first / split

- **Contract-first VERIFIED in git:** `PREREGISTRATION.md` committed at 6f093dc
  (2026-07-30 21:54:30) with only LIVE.md; all six derivation artifacts written
  22:13–22:16, currently uncommitted. Frozen-before-derivation holds.
- **Rerun:** exit 0, ×2, stdout **byte-identical across both reruns AND
  identical to the banked `DERIVATION_STDOUT.txt`**; regenerated
  `PERIOD_LEDGER.tsv` (20 rows) and `period_gate_results.json` byte-match the
  banked artifacts. 28/28, 0 FAIL.
- **Split audited:** 22 substantive + 6 guards; the 6 guards are exactly
  S0a/C1d/C4b/C5b/C6e/C6g — citation/typing/table rows, honestly labeled. No
  substantive claim rides only on a guard.
- Exact SymPy only in the derivation script (no floats/numeric solvers/GPU);
  deterministic; single process; ~1 min.

## Duty 1 — the no-quantization headline (attacked hardest): **HOLDS**

- **(a) Cycle census completeness — re-derived.** The binding R9 wording
  (`POSED_INVERSE_PROBLEM.md` §3, R9) licenses periods over exactly
  "**completion-class cycles, K₄-orbifold cycles, J11 loop holonomies**" —
  1-cycles and loop holonomies ONLY. **No 2-cycles / 2-form flux periods are in
  the spec**, so the potential G13-flux gap is OUT OF CONTRACT; additionally (my
  own adjudication) it is doubly benign: the capped arena with π₁ trivial
  (104/104 |det| = 1, independently re-read from the banked TSV: all dets ∈
  {+1, −1}) has H₂ = 0 by Poincaré duality for the closed orientable case; lens
  |det| = n > 1 gives torsion H₁ ⇒ torsion H₂ ⇒ real-coefficient periods vanish;
  and G13's F = dS is exact, so its periods vanish identically anyway. The
  wall-gate verifier's certification ("live content = completion-class + J07/J11
  cocycle cycles") is exactly what this package ran. 1D chain-completion
  case-split is exhaustive: two mirrors ⇒ D∞; periodic ⇒ Z; any free end ⇒
  acyclic; a single mirror on a ring is impossible (a circle reflection has two
  fixed points ⇒ back to D∞). No dropped class found.
- **(b) Real-targets theorem — verified.** All banked holonomy targets checked
  real: K₄ characters ±1 (banked), anchored weights e^{a_F p0} ∈ R₊, E08 u-law
  and T3 twisted law with Q = e^{φK}, ρ = e^{φH} (both re-read verbatim from the
  Route B bank; the u := s·σ(φ) variable change makes the script's
  u₁₂ = u₁ + e^{−φ₁}u₂ the banked form exactly). The census fields (φ, f, bh)
  are real; **f is certified in the banked higher-isometry audit as "the
  connection moment of the extra circle"** — a real metric coefficient, not an
  angle, so the atan-branch multivaluedness never engages.
- **Angular-coordinate compactness adjudicated (my duty):** the toric angles ARE
  compact, but every 1-cycle along them is either capped-contractible (π₁
  trivial ⇒ zero period for closed forms automatically) or torsion (⇒ vacuous by
  n·P = 0 over R). Compactness reintroduces 2πZ only through a circle-valued
  FIELD — and none is banked. The package's "one doorway" statement in
  `DECISION_SURFACE_UPDATE.md` is exactly right.
- **Structural-i contrast:** the July-5 i-flow record lives on a superseded lane
  and contributes nothing to the current P4 banked census; the e^{2πi} = 1
  contrast is correctly tagged OUTSIDE-census (F-P2 clean — a contrast, not a
  smuggled mechanism). I reproduced the SymPy defect: `solveset(exp(I*t)−1, t,
  Reals)` indeed returns the incomplete {0}; the workaround (direct exact
  evaluation) is necessary and sound.
- **One integers-exist note (no amendment needed):** discrete DOMAIN labels do
  exist in the bank — K₄ characters ±1, cap dets ±1, and the Hopf chirality pair
  Q = ±1 (consumer-audit C04/G13 row). The package names the first two classes;
  all three are completion/domain DATA of the same kind: none cuts a continuum
  family parameter, and R9's period conditions on their classes are vacuous. The
  no-quantization claim is about family-parameter lattices and is correctly
  scoped.

## Duty 2 — the sector map (C6b attacked hardest): **HOLDS**

- **Ring law re-derived** (V3): Δπ_p = a_F·E0·L with g_p cancelling
  (heterogeneous members legal); sealed seams ⇒ Σ E0_i L_i = 0. M-WALL = [π_p] =
  2a_F ℓ E0 = a_F·M-GEN re-derived and matched verbatim against the banked
  Slice-2b identity. Flux-seal ⟺ 𝔅_Q = 0 and [π_φ] = −c_E𝔅_Q confirmed in the
  wall-gate bank. The common-a_F premise is stamped.
- **SOS forcing re-derived** (V5): the exact SOS identity checks; on the
  definite class Σ E0_i L_i = 0 forces all E0_i = 0 — all-definite cyclic chains
  are massless. 1-cell cyclic re-solved independently (V6): sp.solve returns
  {w1 = 0, E0 = 0} uniquely, then c = 0: constants only; massive locus EMPTY.
- **Crease conditions re-derived from the mirror-jet kill myself** (V7):
  p0(−ℓ) = 0 ∧ p0″(−ℓ) = 0 ⟺ w(−ℓ) = 1 ∧ 2A·w(−ℓ) = w′(−ℓ)² — exact identity
  p0″·a_F·w² = 2Aw − w′² confirmed. ε_φ = −1 is CANON-definitional (layer 3).
- **Realizability certificate independently verified** (V8): crease-pinned
  branch satisfies both conditions with disc = −2A < 0 (nodeless);
  I_p(1/2)·a_F = π − 4 re-integrated exactly; Dalzell 22/7 − π = a
  nonnegative-integrand integral re-integrated exactly; **I_p(9/2)·a_F computed
  in exact CLOSED FORM by an independent route: −4 + π/6 + (2/3)atan 5 +
  (5/3)log 13 > 0**, which exceeds the package's piecewise lower bound
  (2/3)log(5/2) (bound chain sound); adversarial numeric corroboration locates
  the IVT root at A* ≈ 1.4129 ∈ (1/2, 9/2) with I_p(A*) ≈ 0 and E0 > 0. The
  Category-A stamps (IVT; log-monotonicity) match the banked A2/sign-change
  precedent; π − 4 equals the banked Slice-2b `ADOPTED_Ip_signchange` c = 1
  endpoint (both values verified in the banked record).
- The mixed-sign cyclic witness is honestly typed NOT-certified-nonempty
  (limit v); the ℓ = 1 normalization is tagged CHOSE.

## Duty 3 — Hom(D∞, R) = 0: **HOLDS** (proved by a second route)

Affine reps re-built independently; r γ_T r⁻¹ = γ_T⁻¹ exact; my V1 uses the
conjugation argument (h(γ) = h(rγr⁻¹) = h(γ⁻¹) = −h(γ) ⇒ h(γ) = 0) — independent
of the package's generator-torsion route; both give Hom(D∞, R) = 0 (consistent
with abelianization Z₂×Z₂). Orbifold identification matches the banked
mirrored-cell/fold posture (seam package). Integral corroboration EXTENDED
adversarially to a transcendental profile (e^x + 1/(x²+3) + x·cos x): period
still identically zero (V2) — stronger than the package's degree-5 test.

## Duty 4 — multi-cell tie and W_F·L̃ = E0: **HOLDS**

On-shell identity re-derived by my own route (V4, zero residual); the banked
single-cell tie 2E0·I_p = 0 (Slice-2b, a_F′ = 2 both P1 instances — read
verbatim from the bank) is exactly the N = 1 instance of Σ E0_i I_p,i = 0. The
package's REFINES-not-contradicts reading is correct.

## Duty 5 — J11/NV classification: **HOLDS**

E08 associativity and the two-sided twisted law re-verified on my own
composition (V10/V12); law and Q/ρ forms match the Route B bank verbatim
(including composition order γ₂∘γ₁). Loop holonomy: I proved surjectivity onto
ALL of R (every target value attained) and degree-≤1 affinity in the segment
data — continuum classification, no lattice. NV holonomy on torsion cycles is
finite-set-valued ({±1}-type) — discrete domain labels, banked upstream, cutting
no continuum parameter (consistent with the package's scoping).

## Duty 6 — honesty items

- SymPy `solveset(exp(I*t)−1, t, Reals)` defect REPRODUCED (returns {0});
  the routed-around certificate (direct exact evaluation e^{2πi} = 1, 2π ≠ 0;
  e^{πi} = −1) is sound.
- The three pre-bank hardenings: **not diffable** — no earlier draft is in git
  (only the final script exists; the package is uncommitted). I verified the
  FINAL forms are the strong ones claimed (C3c exact evaluation + solveset; C5a
  exact solveset/EmptySet; C2c is_nonnegative + solveset — no soft `ask`, no
  vacuous disjunct anywhere in the final script). Accepted with that caveat.

## Duty 7 — falsifier hunts

- **F-P3 (FIRST):** full stamps present and correct on the standing block, all
  20 ledger rows, JSON, and per-check details (posture / census / pairing /
  completion branch / cycle / family / jet ≤ 2 / arena / parity / quadratic
  class). The arena-transfer premise (W-1D jump laws into the chain
  computation) is honestly stamped. NOT FIRED.
- **F-P1:** the two owner-pleasing legs carry the hardest in-package treatment
  as flagged (C6b's nonconstructive steps named; ℓ = 1 CHOSE; the silence leg
  has derived reasons per condition plus the named doorway). OQ4 is stated with
  positive-result care. The T2-comfortable outcome (posture selection) is
  correctly reported NOT-landed. NOT FIRED.
- **F-P2:** no integer condition exists; the 2πZ contrast is certified
  OUTSIDE-census (verified). NOT FIRED.
- **F-P4:** grep + read: no posture/census/pairing/G18/completion adoption
  anywhere; all conditions carried per-branch symbolically. NOT FIRED.
- **F-P5:** banked cross-checks all reproduce (cap TSV, Slice-2b identities and
  π − 4 endpoint, E08/T3 laws, flux-seal pin, wall-gate R9 typing). NO
  CONTRADICTION.
- **F-P6:** no symbolic failure in the banked run; the one solver-path defect is
  disclosed and reproduced. NOT FIRED.
- **F-P7:** the sectors reading appears only as computed Q-C rows; the
  DECISION_SURFACE prose says "characterized only, not adopted" and resolves no
  fork by it. NOT FIRED.

## Duty 8 — contract compliance

TP-1..TP-6 all addressed (census table; derived conditions; Q-A; Q-B; Q-C;
decision surface). All four candidate families appear in all applicable ledger
blocks (20 = 4×3 + 4 + 4) — **none dropped** (the owner's rider honored). Full
declared scope run (no scope-ladder narrowing; none needed). The §4 ceiling is
respected: nothing adopted, no spectrum claimed, no physics.

## Required amendments (bookkeeping, both cheap)

1. **`AUDIT_REPORT.md` is a promised deliverable (prereg §2 list, §5(5)) and
   does not yet exist** — it must be written before commit (the prereg
   four-check + this verifier record).
2. **EXACT_DERIVATION.md "byte-identical ×3" / status line:** update the status
   line ("blind verification pending") to record this pass, and note the
   hardening claim's non-diffability (no draft in git) — one sentence each.

## Notes that travel (no action required)

- C1b's `is_zero(0+0)` and C4a's second witness line are decorative as coded;
  the substantive content is carried by the solvesets + prose and is
  independently confirmed here (V1/V2). Cosmetic only.
- Discrete domain labels exist in the bank (K₄ ±1, cap dets ±1, Hopf Q = ±1);
  the no-quantization claim is correctly scoped to family-parameter lattices.
- The field-period c-commonality ([π_f] = 0 across seams) rides the sealed-seam
  premise class via the stamped arena-transfer premise.

---

## AMENDMENT CLOSURE (same blind verifier, second pass, 2026-07-30)

**Verdict: CLOSED.**

1. **Rerun + byte-integrity:** `derive_period_gate.py` rerun by me post-amendment:
   28/28, exit 0; stdout byte-identical to the banked `DERIVATION_STDOUT.txt`;
   regenerated ledger + JSON hash-identical (md5) to the copies I preserved during
   the verification pass. Substantive artifacts UNTOUCHED by the finishing pass:
   `PERIOD_LEDGER.tsv` / `period_gate_results.json` / `DERIVATION_STDOUT.txt`
   md5-identical to my preserved originals; `PREREGISTRATION.md` git-diff vs
   6f093dc EMPTY; `derive_period_gate.py` mtime/behavior unchanged (identical
   outputs); my `VERIFIER_REPORT.md` (pre-append) and
   `VERIFIER_INDEPENDENT_CHECK.py` untouched. The sha256 prefixes cited in
   `CORRECTION_LAYER.md` §3 (3f1960b1 / 6f60eac3 / 0eb88666) independently
   reproduced — all three match.
2. **`AUDIT_REPORT.md` faithfulness:** VERIFIED point by point against my report —
   contract-first at 6f093dc (correctly stated as prereg+LIVE.md only); 14 groups;
   the 2-cycle OUT-OF-CONTRACT-and-doubly-benign ruling (correctly limited:
   "recorded, not banked as a contract result", limit 1); the angular-compactness
   adjudication; the DOUBLY-PROVEN Hom(D∞,R)=0 with the transcendental-profile
   extension; my closed form −4 + π/6 + (2/3)atan5 + (5/3)log13 and the A* ≈ 1.4129
   root credited (correctly tagged corroboration-not-banked, limit 5); the
   silence-and-sector attacked-hardest-and-HELD record (F-P1 memorial); the
   discrete-domain-labels note (correctly HARDENED into scoping limit 4: "do not
   cite it wider"); both amendments memorialized as bookkeeping. The composite
   verdict carries all stamps: R9 cycle-class scope binding (limit 1); sectors =
   characterized typing only (limits 6, F-P7); census/pairing/posture none adopted
   (limit 2); L4/J11 completion-data conditionality (limit 3); Category-A + ℓ=1
   CHOSE (limit 5); quadratic-class/jet/arena-transfer (limit 7); the
   same-session verifier caveat (limit 8). Mixed-sign ring nonemptiness stays
   typed OPEN. One unverifiable color claim noted, not a defect: "a first for the
   arc alongside Route D" is arc-history color outside my blind scope.
3. **AM-2 + header sync:** `EXACT_DERIVATION.md` status line updated to
   VERIFIED-WITH-AMENDMENT and the [AM-2] non-diffability note appended exactly as
   specified (+8 lines, 260→268; body verbatim — anchor spot-checks on the Hom
   theorem, C2c SOS row, C6b certificate, outcome class, falsifier record, and
   limits (viii) all byte-unchanged; my one grep miss was a line-wrap artifact).
   `DECISION_SURFACE_UPDATE.md`: header parenthetical synced only (+82 bytes,
   consistent with the header edit alone); tail and all rows unchanged — the
   beyond-the-two-amendments housekeeping edit is honestly disclosed in
   `CORRECTION_LAYER.md` §1 and is the same bookkeeping class. NO row, verdict,
   or proposal changed.
4. **`CORRECTION_LAYER.md` did-NOT-change list:** verified by hash (ledger, JSON,
   stdout, script, prereg, verifier artifacts) and by inspection (verdicts,
   census, conditions, ledger rows, honesty items). Accurate.

No new defect. Nothing committed by me.
