# Blind adversarial verifier report — seam-closure derivation

Verifier: blind verifier, same-session-spawned (zero-context agent; **caveat: not a hosted
external model** — same model family as the driver; the same-session caveat travels with
this record). Date: 2026-07-30. Contract: `PREREGISTRATION.md` (verified contract-first in
git: commit 2254888 contains ONLY the preregistration + LIVE.md; all derivation artifacts
are post-contract/untracked at verification time). Independent script:
`VERIFIER_INDEPENDENT_CHECK.py` (31 checks, written from scratch, function-level where the
package worked at jet level; preserved alongside this report).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (one required amendment; verdict OC2 itself stands)

The landed verdict — **OC2, BRIDGE-ONLY derived; closure genuinely free; conditional-forces-
fold locus; K6 necessary-but-not-selected; arena-split; banked decider absent; standing
falsifier not fired** — survived adversarial re-derivation on every load-bearing leg. One
headline statement (the conditional-forces-fold premise set) is stated too weakly and is
false as read for a Branch-P interior; the fix is a premise addition, not a verdict change.

---

## REQUIRED AMENDMENT A1 — the conditional-forces-fold premise set must include **Branch-G INTERIOR**

**The broken statement (as written):** "{no seam surface term (⇒ WE C¹ matching)} ∧
{Branch-G beyond} ∧ {ρ'(r_s)=0} ⟹ fold FORCED (unique continuation = odd mirror)" —
stated this way in `EXACT_DERIVATION.md` (K3 verdict; TS3 sharpening), `FORCING_LEDGER.tsv`
(K3 row; COMPOSITE row), `DECISION_SURFACE_UPDATE.md` (item 1), the script comment above
K3h, and `seam_closure_results.json` (`TS2_verdicts.K3`, `TS3_composite`).

**Counter-computation (independent, zero-residual: check V2d).** The forcing argument runs
through K3c ("the reflection maps G-solutions to G-solutions") — which requires the INTERIOR
solution to be Branch G. For a **Branch-P interior**, the odd mirror fails the G φ-equation
with exact residual **−4e^{−2φ}ρ'²/(Zρ²)** (nonzero wherever ρ'≠0 in the interior; verified
at function level, not just at the seam jet). So with a P interior satisfying all three
stated conditions, the unique G continuation EXISTS (Picard) but is **not** the mirror —
"fold FORCED" is false as read. The package demonstrably knew this (K3d; the P-interior
quotient-only clause sits in the same K3 verdict paragraph) — the premise was dropped from
the headline, not from the reasoning.

**Fix (each locus):** state the premise set as **{no seam surface term (WE C¹)} ∧
{Branch-G on BOTH sides of the seam (interior and beyond)} ∧ {ρ'(r_s)=0}** in all six
loci above. No other claim changes; the ρ'_s≠0 C¹-impossibility leg (K3h) is unaffected
(it is branch-independent: the mirrored profile's ρ'-jump −2ρ'_s is kinematic).

---

## Per-duty findings (compressed)

**(0) RERUN.** Exit 0; **42/42 (33 SUBSTANTIVE + 9 GUARD)** — counts independently
recomputed from the JSON and from the source; stdout and JSON **byte-identical** on rerun
(0.85 s, pure CPU SymPy, deterministic, no floats/numeric solvers/GPU — grep-verified).
Contract-first verified in git. Forbidden-content grep: G18/x_max/ln(1101)/anchor/census/
pairing appear ONLY inside negation/guard statements or as the TS4 re-grade SUBJECT (which
the contract requires); no smuggle. **Split audit:** the guard list (S1b, S1c, S1e, K3e×2,
K4a×3, K7a) is honest; however ~4 SUBSTANTIVE rows are trivial-by-construction
(S1f_handshake_germA_flat ≡ 0−0; K3g phip/rho slots identically zero even off-locus) —
witness-assembly steps, not computations. RECOMMENDED (not required): relabel those rows or
footnote the count; nothing hides behind them.

**(1) Bridge underdetermination — GENUINE.** §235/§236 read at source
(`negative_phi_native_geometry.md:16668-16770`): the five facts match verbatim; §236's own
limits ("does not by itself define an action split"; "requires a boundary action or
amplitude"; "plausible coupling rule, not derived") are quoted accurately — the bridge's own
record names the boundary action as the missing upgrade. **The banked §235 script
(`legacy/root_oneoffs_2026-07-01/native_phi_sign_mirror_bridge_audit.py`) is confirmed a
pure dataclass PRINTER — zero computation** — the honesty item is accurate and the native
recomputation (S1a–S1e) was necessary; I recomputed the five facts independently (V6a/V6b:
weight swap; ℓ=1 eigenvalue 2 on all three harmonics). Both witness germs re-derived (V6c/
V6d): flat glue and odd mirror both pass the full handshake at the seam locus; first jets
differ by φ₋'(r_s). No missed handshake condition found in §235/§236 or the fold-JC seam
conditions that cuts the germ space (φ-continuity and pointwise ρ-identification are
CHOSE-cited postures and both germs satisfy them). Decisive corroboration: the corpus itself
banks BOTH germs in use (flat glue at the matter cell; fold-assumed at the universe cell).

**(2) Conditional-fold locus.** Reflection seam data recomputed from the mirror map at
function level (V3a–V3c): (−φ_s, +φ'_s, ρ_s, −ρ'_s) — correct. The iff (φ_s=0 ∧ ρ'_s=0)
re-derived (V3d). **Picard leg SOUND at the locus:** the G first-order system
(φ,φ',ρ,ρ')' = (φ', −2φ'ρ'/ρ, ρ', −(Z/4)ρφ'²) has jacobian singular ONLY at ρ=0 (V4a); at
(φ=0, ρ'=0, ρ=ρ_s≠0) all entries are finite (V4b) — φ=0 is not a singular point (φ is
absent from the G RHS); r_s is not special (autonomous system). The ρ_s≠0 requirement is
honestly listed as scope edge (iii). **Off-locus C¹ gap −2ρ'_s confirmed (V3e). Regularity
class adjudication:** C¹ is the right class FOR the no-surface-term (WE) posture; the banked
corpus does hold a weaker class — the glue-with-jump (ΔΠ=q/2, weld) — under which a KINKED
mirrored profile with a matching surface term B would be readmissible; the package's
conditioning on D-a (the surface-action status decides whether WE C¹ applies) covers exactly
this, and the impossibility claim is correctly scoped "as a C¹ configuration". No overclaim.

**(3) K4.** Momenta re-derived from the Lagrangians (V5a–V5c); the doubled momentum
−4e^{−2φ}ρ'−4e^{2φ}ρ' = **−8cosh(2φ)ρ'** verified (V5d; matches the banked fold-JC route
[π_ρ]=8cosh(2φ_s)ρ'_s up to orientation); essential BC v=−v⟹v=0 and natural BC ρ'_s=0
(V5e/V5f); WE continuity-only for both P|P and P|G (V5g/V5h). **"Banked decider ABSENT"
CONFIRMED at source:** `universe_cell_fold_jc_sigma_results.md:104` ledger row reads
"ρ'(r_s)=0 | DERIVED, robust (any φ_s, 3 routes; **needs partner=mirror-image = closed-cell
premise**)" — the pin rides an undecided CHOSE; and fold-JC :31-33 records the
independent-partner fork giving NO ρ'-pin. Minor cosmetic: K6a mixes the single-copy π_φ
with the doubled π_ρ (moot — δφ=0 essential kills the term).

**(4) K6 re-run.** Fold: boundary terms vanish under its own pins (re-derived). Glue+B:
B'(ρ_s)=ΔΠ=q/2 (V7a) — and the required B is verified to be the 07-18 OPEN object at source
(`native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md:31,206` and
M19 row: "Complete differentiable finite-cell boundary action … remain open — OPEN").
**q=0 forcing re-derived (V5i):** bare free endpoint ⟹ π_φ(r_s)=0 ⟹ φ'_s=0 ⟹ q=0 (needs
ρ_s≠0, same scope edge). "Necessary but not selected" is the correct reading: all three
closures well-posed; the "no choice" posture is itself the q=0 closure.

**(5) Arena-split — CONFIRMED at source.** `weld_two_sided_results.md` :30-33: "The
interface stress is a SINGLE jump: ΔΠ = q/2 (Π_inner=−q/2, Π_outer=0 — the exterior is
FLAT, CANON C-2 zero tail)"; :39-41: "Exterior mirroring is NOT USED anywhere in the banked
chain … a sign/bridge statement at the phi=0 surface, not a mirrored profile in r; the
banked cell glues to the flat exterior, full stop." Matter seam = glue-with-jump IN-USE;
universe seam fold = canon-assumed (now G18 per C-2026-07-30-1). No banked reconciliation
found; the split is real.

**(6) Standing falsifier — NOT FIRED is correct, and the distinction is REAL, not
wordplay.** The banked unsatisfiability (5978573; LIVE.md) is a statement about realizing
the fold as a **point involution of the toric arena** (R-A) under the pointwise crease
within banked-complete membership. The conditional fold here is a **1D radial-profile
relation** with the screen/angular action explicitly unspecified (scope edge (i)); these are
different mathematical objects — a radial mirror relation asserts nothing about how (or
whether) an involution acts on the toric arena, and the banked escapes (¬R-A / setwise /
new class) remain exactly as banked. The package correctly notes an unconditional pointwise
toric fold WOULD have collided; none was derived.

**(7) K3 / F-C2 discharge — SOUND.** Re-derived: L_G invariance and the L_P residual
−4sinh(2φ)ρ'² at jet level; mirror-of-G solves G and mirror-of-P fails P with the exact
banked residuals at FUNCTION level (V2a–V2c — stronger than the package's jet-level check).
The adjudication structure is correct: the symmetry alone forces nothing; forcing enters
only through the data locus + uniqueness — no symmetry-of-equations was promoted anywhere.
(The one place the chain under-states its premises is A1 above.)

**(8) Bug fixes — SOUND at final resting places; independently corroborated.** (a)/(b) the
exp/cosh canonicalization ×2 (the `check()` rewrite-to-exp fallback; K3d's explicit
rewrite): these only STRENGTHEN the prover (a genuine nonzero cannot become zero under
rewrite+simplify); my own independent script hit the identical canonicalization need on the
same two expression families — the disclosed fixes are genuine SymPy-path issues, not
weakened conditions. (c) the mis-assembled witness: the final S1f checks are correct; a dead
variable (`germB_val`, script line 122, computed-and-unused) remains as harmless fossil.
No check condition was weakened by any fix.

**(9) Falsifier hunts.** **F-C3 (hunted FIRST):** full five-slot stamps (arena / census
branch / pairing / crease reading / stratum) present in the script header, the JSON stamps
object, the EXACT_DERIVATION header ("apply to every claim below") + per-claim scope-edge
list, and the ledger stamps column. No unstamped claim found; no eleventh catch. **F-C1
(both directions):** the fold-favorable content (the conditional theorem, the ρ'_s=0
natural-BC leg) got the HARDER audit here and yielded A1; the bridge-only verdict's own
load-bearing leg (the underdetermination witness) was re-derived and is genuine — and is
corroborated by the corpus itself using both closures. The OC1/OC3 counterfactual rows match
the banked consumer ledger (FALLS-2 = Route P parities + angular-completion core;
"unconditional-on-R-A-only" honestly retains the R-A conditioning under OC1). No easier
ride detected. **F-C2:** discharged (duty 7). **F-C4:** no smuggle (duty 0 greps; the fold
enters only as interrogated candidate). **F-C5:** every cited bank locus checked at source
(§235/§236, weld :30-33/:39-41, fold-JC :20-24/:31-33/:104, 07-18 M19/report, CANON
C-2026-06-10-2 / C-2026-07-09-1a / C-2026-07-30-1, consumer ledger, provenance §2a-i
WR-L-mirror-free, "distinct in the recorded models" at LIVE.md:992) — no contradiction; TS4's
consumer map facts match the banked conditionals exactly. **F-C6:** no symbolic failures.

**(10) Contract compliance.** TS1–TS5 all addressed (TS5 = `DECISION_SURFACE_UPDATE.md`,
handle-not-recommendation as required). Ceiling respected: no closure adopted; the G18
re-grade is PROPOSED-to-Charles language throughout; no census/pairing adoption; no
massive-branch language beyond computed map facts; x_max/anchors untouched. Note: the
contract's deliverable list includes `AUDIT_REPORT.md` + four-check before commit — still
owed at the driver stage (correctly so at this point in the sequence; the package honestly
self-labels "not yet blind-verified, not committed").

## Amendments summary

- **A1 (REQUIRED):** add **Branch-G INTERIOR** (i.e., "Branch G on both sides") to the
  conditional-forces-fold premise set at all six loci (EXACT_DERIVATION K3 verdict + TS3;
  FORCING_LEDGER K3 + COMPOSITE rows; DECISION_SURFACE_UPDATE item 1; script comment above
  K3h; JSON TS2_verdicts.K3 + TS3_composite). Counter-computation: V2d (mirror of a P
  interior fails the G φ-equation with exact residual −4e^{−2φ}ρ'²/(Zρ²)).
- **Recommended (non-blocking):** relabel/footnote the ~4 trivial-by-construction
  SUBSTANTIVE rows; delete the dead `germB_val` line; note the K6a single/doubled momentum
  mixing.

Not committed by the verifier (per instruction).

---

# AMENDMENT CLOSURE (same blind verifier, second round — 2026-07-30)

## VERDICT: **CLOSED**

**(1) Rerun.** `derive_seam_closure.py`: exit 0, **50/50 = 37 SUBSTANTIVE (29 original +
8 verifier-credited) + 13 GUARD**; run twice — byte-identical stdout and JSON, and both
match the package artifacts exactly (sha256 f8c472ba… / c0b8b772…, matching the ×3 claim
in CORRECTION_LAYER §3.6). Full pre/post script diff audited line-by-line:
- **Credited checks faithful:** AM2a–d ≡ my V1a–d (EOMs as genuine Euler-Lagrange, same
  claims, same solve-and-compare structure); AM2e–f ≡ V2a–b (mirror-of-G solves G at
  function level, identical impose-EOM substitution machinery); AM2g ≡ my corrected V2c
  (exact residual −(4ρ'²/(Zρ²))(e^{−2φ}+e^{2φ}), with the same exp-canonicalization my
  script needed); AM1 ≡ V2d (mirror of a P interior fails the G φ-equation, exact
  residual −4e^{−2φ}ρ'²/(Zρ²), zero-residual identity + certified nonzero). All eight
  reproduce my computations; none is weakened.
- **Relabels hide nothing:** the 4 relabeled rows (S1f germA-flat, S1f germB seam-value
  identity, K3g phip/rho slots) keep their EXACT original expressions and still run and
  pass — only the kind label changed, each with an honest in-script note; the
  load-bearing S1f rows (on-locus handshake; certified-nonzero jet gap) and K3g slots
  (phi, rhop — zero exactly on the locus) remain SUBSTANTIVE. Count arithmetic verified:
  33−4+8 = 37; 9+4 = 13. The `check_bool` unification and `credit` plumbing change no
  check condition (diff-verified per check).

**(2) A1 installed at all six loci**, on the full form {no seam surface term (WE C¹)} ∧
{Branch-G on BOTH sides of the seam (interior AND beyond)} ∧ {ρ'(r_s)=0}, with the
impossibility leg correctly marked branch-INDEPENDENT: EXACT_DERIVATION K3 verdict
(:109-113) + TS3 sharpening (:234) + amendment banner; FORCING_LEDGER K3 + COMPOSITE
rows; DECISION_SURFACE item 1 (with an explicit P-interior antecedent-fails clause);
the script comment above K3h; JSON TS2_verdicts.K3 + TS3_composite + the new
`amendment` key. **Grep for surviving premise-dropped forms:** the only "Branch-G
beyond"-without-both-sides hits are quotations of the original statement inside the
correction records (CORRECTION_LAYER :11/:22; this report :24) and the legitimately
beyond-only **D-c datum** (EXACT_DERIVATION :227; AUDIT_REPORT :135) — which now
carries the correct A1 clarification that the interior branch is a per-configuration
datum whose failure voids the antecedent, not a new free choice. No headline-form
statement survives.

**(3) Recommendations.** K6a momentum-mixing note added (and mathematically correct:
2π_φ·0 = π_φ·0 = 0); dead `germB_val` removed; the honest split restated at every
count locus (EXACT_DERIVATION header + honest-split section — which also discloses the
pre-amendment 42/42 = 33+9 count rather than erasing it; ledger COMPOSITE row; JSON
counts split original/credited; stdout summary line).

**(4) CORRECTION_LAYER did-NOT-change list — verified by comparison** against the
pre-amendment artifacts held from round 1: OC2 composite, the bridge floor + witnessed
underdetermination, the conditional locus (iff / on-locus identity / Picard with
ρ_s≠0), the off-locus C¹ impossibility (now explicitly branch-independent — an
addition, not a change), K4 (discriminator + decider-absent), K6
(necessary-not-selected + q=0 forcing), the arena-split, the falsifier non-firing, the
D-a/D-b/D-c reduction, and TS4's map facts with G18 PROPOSAL-only — all textually
unchanged except the A1-required insertions (the one TS4 edit is the FALLS-2
derivational-anchor condition set gaining "Branch-G on both sides [A1]", which A1
itself requires). Regeneration of DERIVATION_STDOUT.txt / seam_closure_results.json is
disclosed. **AUDIT_REPORT faithful to round-1 findings:** contract-first-in-git,
31/31 independent checks, V2d + the function-level F-C2 discharge credited by name,
the harder-audit-fell-on-the-fold-favorable-legs record, the A1 disposition, and both
caveats (same-session-spawned; not a hosted external model) present.

No new defect found. The required amendment is correctly and completely applied;
verdict **OC2 stands on its corrected premise set**. Not committed by the verifier
(per instruction).
