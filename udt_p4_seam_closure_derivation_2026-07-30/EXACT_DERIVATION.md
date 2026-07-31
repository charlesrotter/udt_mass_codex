# P4 seam-closure derivation — exact record

Date: 2026-07-30. Contract: `PREREGISTRATION.md` (frozen before this run).
Script: `derive_seam_closure.py` — post-amendment **50/50 checks (37 SUBSTANTIVE =
29 original + 8 verifier-credited; + 13 GUARD), exit 0**; stdout preserved
(`DERIVATION_STDOUT.txt`); machine record `seam_closure_results.json`.
Ledger: `FORCING_LEDGER.tsv`. Status: blind-verified **PASS-WITH-REQUIRED-AMENDMENTS**
(`VERIFIER_REPORT.md`, 2026-07-30) with all amendments applied
(`CORRECTION_LAYER.md`; grade in `AUDIT_REPORT.md`) — **not committed, nothing
adopted** (the ceiling of §4 of the contract honored; the driver banks).

**AMENDMENT BANNER (2026-07-30, per the verifier's A1 + recommendations —
`CORRECTION_LAYER.md`):** the conditional-forces-fold premise set below is stated on
its FULL form **{no seam surface term (WE C¹)} ∧ {Branch-G on BOTH sides of the seam
(interior AND beyond)} ∧ {ρ'(r_s)=0}** — the pre-amendment headline dropped the
interior-branch premise (the package body, K3d, knew it; the drop was headline-level
only). The verifier's counter-computation is adopted as credited check AM1 (the odd
mirror of a Branch-P interior fails the G φ-equation with exact residual
−4e^{−2φ}ρ'²/(Zρ²)); the function-level F-C2 discharge is adopted as credited checks
AM2a–AM2g. Four trivial-by-construction rows relabeled SUBSTANTIVE → GUARD (honest
split); no pre-amendment computed claim changed; verdict OC2 stands.

**FULL STAMPS (F-C3, apply to every claim below):** arena = round-static radial
reduction (1D r-profiles; banked Branch-G/P reduced Lagrangians, fold-JC machinery
reused); census branch = NONE used; pairing = NONE used; crease reading =
pointwise-in-r on the 1D reduction — the screen/angular action of any involution is
NOT specified here (the banked 07-20 angular non-uniqueness stands untouched);
stratum = n/a. **Guards held:** G18 never assumed (the fold enters only as an
interrogated candidate); no x_max content; no anchor values (ln(1101) does not appear);
no floats/numeric solvers/GPU.

---

## TS1 — the bridge floor: what K1+K2 establish EXACTLY, and the residual freedom

**K1 (§235/§236, recomputed natively — honesty note first).** The banked §235 script
(`legacy/root_oneoffs_2026-07-01/native_phi_sign_mirror_bridge_audit.py`) is a
dataclass PRINTER: it records the five facts and computes nothing; re-running it is
trivially green and has no evidential weight. The five facts were therefore
**recomputed from the metric form** here (checks S1a–S1e, all zero-residual):

1. φ→−φ swaps the radial and time weights: e^{2φ} ↔ e^{−2φ} (S1a, both directions).
2. The angular block g_AB = r²ω_AB carries no φ (S1b).
3. At φ=0 the radial weight is 1 — both φ-signs meet at the same angular geometry
   and flat radial value (S1c).
4. −r²Δ_S² has φ-independent spectrum l(l+1) (computed on all three ℓ=1 harmonics,
   eigenvalue 2; the operator is built from ω only) (S1d).
5. L1 = (−r²Δ)/2 = identity on ℓ=1 (S1e).

§236 (banked, cited): the bridge "does not by itself define an action split"; η/2 per
side is "plausible coupling rule, not derived"; the missing object is "a boundary
action or amplitude" — i.e. **the bridge's own record already names the boundary
action as what it lacks** (the same object as K6's OPEN gate).

**The derived handshake at φ=0 (the floor, exact).** Any two radial regimes meeting
at a locus where φ=0 share, AT that locus: the induced angular geometry, the flat
radial weight f=1, and the (φ-independent) angular spectrum with the ℓ=1 identity
sector. That is the whole derived content. It is a statement of **seam-DATA
matching**, not of profile relation in r — exactly the line the adoption-day record
drew (K2, `weld_two_sided_results.md:39-41`, verbatim: "a sign/bridge statement at
the phi=0 surface, not a mirrored profile in r").

**K2 made computational — the underdetermination witness (S1f).** Two DISTINCT
exterior germs both satisfy the full handshake: germ A = the banked flat-exterior
glue (φ₊ ≡ 0 — the CANON C-2 zero-tail matter-cell configuration, banked-in-use);
germ B = the odd-mirror germ (φ₊(r_s+u) = −φ₋(r_s−u)). Both have seam value 0 on the
seam locus; their first jets differ by φ₋'(r_s) — symbolically nonzero for a generic
nontrivial cell. **The bridge does not pin the gluing** (zero-residual + certified
nonvanishing).

**The residual freedom, parametrized** (supported by the banked structure computed in
K4/K6 below): a closure of the seam is a choice of
`τ ∈ { FOLD-QUOTIENT, PARTNER(branch₊), GLUE + surface term B, OPEN-END }` with data:

| τ | seam conditions (computed) | extra data |
|---|---|---|
| FOLD-QUOTIENT (single copy, Z₂ identification) | δφ(r_s)=0 essential (K4b); natural BC ρ'(r_s)=0 (K4c/K4d); φ'(r_s) free ⇒ q output | none |
| PARTNER (two-sided, no surface term) | WE continuity: [φ]=[ρ]=0, [π_φ]=0 ⇒ [φ']=0 (K4e), [π_ρ]=0 ⇒ [ρ']=0 (K4f) — ρ'(r_s) FREE (K4g); continuation then DATA-DETERMINED (not arbitrary) by ODE uniqueness | branch beyond (G/P/flat) |
| GLUE + B (banked matter-cell case) | jump ΔΠ = q/2 (banked, weld :30-32); well-posed iff a seam functional B with B'(ρ_s)=ΔΠ is added (K6c) | the surface term B — exactly the 07-18 OPEN object |
| OPEN-END (bare free endpoint) | π_φ(r_s)=0 ⇒ q=0 AND ρ'(r_s)=0 (K6d) | none — but it kills the flux seal |

---

## TS2 — the forcing interrogation, per candidate

### K3 — the Branch-G exact odd-fold symmetry: **PERMITS unconditionally; FORCES only on a named data locus; FORBIDS a mirrored-P region** (F-C2 adjudicated explicitly)

Banked identities re-run zero-residual (Category-A soundness of this reading): L_G
exactly invariant under the odd fold; L_P not (exact residual −4·sinh(2φ)ρ'²); the
odd-mirror extension of a G-solution is an exact G-solution; of a P-solution it
violates BOTH P EOMs (the two banked residual forms reproduced exactly); the mirror
image of a P-solution solves the flipped-weight Lagrangian — which is neither P nor G
(certified nonzero differences) (K3a–K3e).

**The equations-vs-solutions gap, adjudicated by computation (the new leg).** The
reflected field φ̃(x) = −φ(2r_s−x), ρ̃(x) = ρ(2r_s−x) has seam Cauchy data
(−φ_s, +φ'_s, ρ_s, −ρ'_s). Exact solve (K3f): reflected data = original data **iff
φ_s = 0 AND ρ'_s = 0** — and on that locus the match is identical in all four slots
(K3g). Since the reflection maps G-solutions to G-solutions (K3c) and the G Cauchy
problem has a unique solution (Picard — Category-A cite; RHS smooth in the jet for
ρ≠0), the unique C¹ continuation **IS the mirror exactly on that locus**. Off the
locus (ρ'_s ≠ 0) the mirror's data differ from the continuation's by −2ρ'_s ≠ 0
(K3h): the mirror is then NOT the continuation — **the symmetry of the equations
forces nothing by itself; forcing enters only through data + uniqueness (F-C2
discharged: no symmetry-of-equations was promoted to a symmetry of solutions
anywhere).**

**Verdict [premise set restored per amendment A1]:** CONDITIONAL-FORCES-FOLD, exactly:
`{no seam surface term (⇒ WE C¹ matching)} ∧ {Branch-G on BOTH sides of the seam
(interior AND beyond)} ∧ {ρ'(r_s)=0} ⟹ fold FORCED (unique continuation = odd
mirror)`;
`ρ'(r_s) ≠ 0 ⟹ fold IMPOSSIBLE as a C¹ configuration` [branch-INDEPENDENT: the
mirrored profile's ρ'-jump −2ρ'_s is kinematic — unaffected by A1];
and for a **Branch-P interior**, a mirror-image REGION beyond obeying the same P
equations does not exist (K3d) — a fold at a P-interior can only be the QUOTIENT
reading (consistent with the fold-JC verifier's covering-space CAUTION), or the
beyond is a different branch. [A1, the interior-branch premise made explicit: the
forcing runs through K3c, which requires the INTERIOR solution to be Branch G. For
a Branch-P interior satisfying the other conditions, the odd mirror fails the G
φ-equation with exact residual **−4e^{−2φ}ρ'²/(Zρ²)** — nonzero wherever ρ'≠0 in
the interior (verifier counter-computation V2d, adopted as credited check AM1,
function-level) — so the unique G continuation EXISTS (Picard) but is NOT the
mirror: "fold FORCED" would be false as read without this premise.] Each condition
is itself underived: the surface-term status is the OPEN 07-18 gate (K6); "G
beyond" is the banked PONDER-tag consilience, not a derivation (and the interior
branch is a per-configuration datum); ρ'(r_s)=0 is exactly the K4 discriminator.
**The chain FORCES nothing unconditionally.**

### K4 — the ρ'(r_s)=0 discriminator: **CONSTRAINS (exact); the banked decider is ABSENT**

Both readings computed from the same momenta (π_φ = Zρ²φ'; π_ρ^P = −4e^{−2φ}ρ';
π_ρ^G = −4ρ' — guard-checked against the Lagrangians):

- **Fold/quotient:** the odd identification acts on variations, δφ(r_s) solves
  v = −v ⇒ δφ(r_s)=0 ESSENTIAL (K4b) ⇒ π_φ unconstrained ⇒ φ'(r_s) free ⇒
  q = Zρ_s²φ'(r_s) an OUTPUT; δρ free ⇒ natural BC on the doubled momentum
  p_ρ^tot = −8cosh(2φ)ρ' (K4c) ⇒ **ρ'(r_s) = 0** (K4d). [Reproduces the banked
  fold-JC pins from this script's own reading.]
- **Partner/two-sided, no surface term:** Weierstrass–Erdmann gives CONTINUITY only:
  [π_φ]=0 ⇒ φ'₊ = φ'₋ (K4e); [π_ρ]=0 at the seam (φ=0 there) ⇒ ρ'₊ = ρ'₋ for both
  P|P and P|G pairings (K4f) — **ρ'(r_s) stays a free symbol** (K4g, certified).

So the discriminator is derivable — fold ⟺ ρ'(r_s)=0 (plus the free-endpoint posture
class), partner ⟺ ρ'(r_s) free — but **no banked structure decides ρ'(r_s)**: the
fold-JC premise ledger itself records the pin as "needs partner=mirror-image =
closed-cell premise" (`universe_cell_fold_jc_sigma_results.md:104`, cited), and the
banked corpus contains a live NON-fold seam in actual use: the matter-cell
flat-exterior glue with interface jump ΔΠ = q/2 (`weld_two_sided_results.md:30-32`,
cited). **The corpus is arena-split: universe-cell seam = fold (canon-ASSUMED input);
matter-cell seam = partner-type glue (banked-in-use).** Neither is derived from a
common principle.

### K5 — the WR-L signature-flip seam: **CONSTRAINS (premise-level, cross-arena); decides nothing at the φ=0 seam** (cited-structural; no computation faked)

The recorded models keep the two surfaces DISTINCT: the CMB odd fold has
(φ=0, A=1, ρ'=0); the WR-L wall has (φ→+∞, A→0, null causal character) — verbatim
"They are distinct in the recorded models"
(`asymptotic_boundary_lineage_audit_2026-07-19`, quoted in LIVE.md). The WR-L records
are mirror-free (provenance audit §2a-i, exhaustive grep). What K5 DOES do: the
Charles-accepted horizon reading (C-2026-07-09-1a: "trapped interior beyond … not a
wall of space") establishes that the strongest banked finiteness anchor is
**compatible with "something beyond" a bounding surface** — which softens, at the
premise level and across arenas, the "closed cell, nothing beyond" reading that the
fold leg explicitly rides (fold-JC :31-33). It does not act on the φ=0 seam directly
and cannot force partner-glue there (the surfaces are recorded as distinct objects).

### K6 — the boundary-variational structure: **CONSTRAINS (exact): a closure is NECESSARY, but the structure does not SELECT one**

Computed per candidate:

- FOLD: seam boundary variation vanishes identically under the fold's own pins
  (δφ=0 essential, ρ'=0 natural) — well-posed with NO surface term (K6a).
  [Clarifying note, per the verifier's cosmetic finding: K6a's expression mixes the
  single-copy π_φ with the DOUBLED ρ-momentum; MOOT here — δφ=0 (essential) kills
  the π_φ term identically whether the single or doubled (2π_φ) momentum is used;
  the ρ leg is the doubled-action momentum, as banked.]
- PARTNER: the two-sided boundary terms cancel exactly under WE continuity —
  well-posed with NO surface term (K6b).
- GLUE (banked matter-cell): the banked jump ΔΠ = q/2 leaves δS_seam = (q/2)δρ ≠ 0
  unless a seam surface functional B with B'(ρ_s) = q/2 is added (K6c, solved
  exactly; nonclosure certified) — **the required B is precisely the underived
  differentiable finite-cell boundary action, the 07-18 OPEN gate**
  (`native_action_final_adjudication_2026-07-18`: "complete action, … finite-cell
  boundary action, normalized boundary charge/mass: OPEN").
- OPEN-END (the "no choice" posture): itself a definite closure — the bare free
  endpoint forces π_φ(r_s)=0 ⇒ **q = 0** and ρ'(r_s)=0 (K6d). Leaving the gluing
  "unchosen" is not variationally neutral; it kills the flux seal.

**Verdict:** well-posedness holds under fold AND partner AND glue+B — K6 does not
force a closure type. Its exact content is sharper than silence: **the variational
problem demands A closure (every posture, including 'none', is one) but supplies no
selector; the selecting object would be the derived boundary action B — exactly the
banked OPEN gate, and exactly the object §236 already named as the bridge's missing
upgrade.** (Consistent with Stage-1 census :431 "Parity fixes phi|_Σ, not B[φ]"; the
Route-D N3 wall/corner slots and Stage-3 gate-5 census type these as
supplied-structure slots — cited.)

### K7 — horizon-CMB consistency: **SILENT as a decider** (consistency holds both ways)

φ=0 is the unique fixed point of φ→−φ (K7a — the note's §3 observation; the source
itself tags it "either a triviality or a derivation seed — this note does not decide
which", and it remains undecided here). The note's §2 taxonomy keeps dissolution
surfaces (φ=0) and horizon-class surfaces distinct — matching K5's recorded-model
distinctness. Neither the fold nor the partner reading at the φ=0 seam contradicts
the banked horizon structure; §5 audit target 2 (the quantitative inside-out mirror
map) is OPEN in-source. Silence stays silence.

---

## TS3 — composite verdict

**OC2 — BRIDGE-ONLY is what banked structure derives. The closure is genuinely free
on the banked record, with the partner-glue alternative live — indeed banked-IN-USE
at the matter-cell seam (flat-exterior glue with ΔΠ = q/2), while the fold at the
universe-cell seam is canon-ASSUMED input, not derived. No candidate K3–K7 forces a
closure unconditionally.**

With the OC4-grade precision the contract asks for anyway — the exact missing data,
named:

- **D-a: the seam surface-action status** — the differentiable finite-cell boundary
  action B (the 07-18 OPEN gate). Its presence/absence decides whether WE C¹ matching
  applies (K6; also the object §236 named).
- **D-b: the ρ'(r_s) pin / beyond-ontology datum** — equivalently the choice between
  the free-endpoint ("nothing beyond") posture and the two-sided posture (K4). The
  banked corpus holds both in use in different arenas and contains no decider.
- **D-c: the branch beyond** (G / P / flat) — "G beyond" is a PONDER-tag, underived
  (K3); a P-beyond mirror region is FORBIDDEN (K3d), a fact that itself constrains
  the fold to the quotient reading for P-interiors. [A1: the forcing theorem
  additionally requires the INTERIOR branch to be G — a per-configuration datum,
  not a new free choice; for a P interior the theorem's antecedent simply fails.]

**The sharpening (new, conditional, both directions honest — F-C1) [premise set per
amendment A1]:** on {B ≡ 0 at the seam, **Branch-G on BOTH sides (interior and
beyond)**, ρ'(r_s)=0} the fold is FORCED (K3f/K3g + uniqueness + AM1);
for ρ'(r_s) ≠ 0 the fold is IMPOSSIBLE as a C¹ configuration (K3h;
branch-independent). So the closure question is **derivation-decidable conditional
on D-a + D-b** (with the interior branch read off the configuration and D-c ruled
alongside) — it has been reduced from an open-ended ontology question to two named
banked-open data.

**Standing-falsifier check (the banked angular-completion unsatisfiability):**
NOT FIRED, by scope: no unconditional fold was derived, so there is nothing for the
falsifier to attack; the conditional fold **names its arena** — the round-static
radial reduction, pointwise-in-r on the 1D profile — and asserts NO point involution
of the banked toric arena and NO screen-block realization (the banked 07-20 angular
non-uniqueness and the {R-A, pointwise crease, banked-complete membership}
unsatisfiability are untouched; the setwise escape remains exactly as banked). Had
this push derived an unconditional pointwise fold on the toric arena it would have
collided with the unsatisfiability; it did not.

**ELEVENTH-catch watch (named scope class):** every claim above is stamped
(arena / census branch = none / pairing = none / crease reading / stratum = n/a).
The known scope edges: (i) the 1D radial reduction — nothing here speaks for the
angular/screen action of any involution; (ii) the WE leg presumes continuity of
(φ, ρ) at the seam (the banked JC2/orbifold posture, CHOSE-cited in fold-JC — carried
here as the same CHOSE); (iii) K3's uniqueness cite requires ρ ≠ 0 at the seam
(Picard regularity); (iv) K5/K7 rows are cited-structural, not computed.

---

## TS4 — consequences as map facts, per verdict (no adoption, no eulogy, no relief)

**Under the LANDED verdict (OC2):**

- **G18 re-grade the driver would PROPOSE to Charles:** neither confirmed nor
  refuted. PROPOSAL = G18 stays OWNER-RATIFIED-PROPOSAL working premise, now with a
  derived REDUCTION attached: its truth-value is equivalent to the two named data
  {D-a: seam boundary action; D-b: ρ'-pin/beyond-ontology}, with the conditional
  forcing theorem showing it becomes derivation-decidable once D-a is closed (and
  D-b thereby constrained or ruled). The clause's content is REPLACED-as-a-question:
  from "is the mirror true?" to "what is B at the seam, and is the seam single-copy
  or two-sided?".
- **FALLS-2 consumers (Route P; angular-completion core):** status UNCHANGED —
  conditional on G18 exactly as the consumer ledger stamped them; not voided, not
  restored. New map fact: their premise now has a derivational anchor CONDITIONAL on
  {D-a, D-b, Branch-G on both sides of the seam [A1]} — the first path on record by
  which the parity chain could be put on derived footing.
- **E0-collapse / fields-massive branch:** remains fold-conditional; the ¬fold
  branch stays LIVE (nothing here closes it, and nothing here opens it further —
  the freedom was already banked; this push made it exact and finite-dimensional).
- **Constants-side triad branch:** unchanged (P1-triad massless lock etc. ride the
  G18-conditional parities; no new status).

**Had OC1 landed (fold derived unconditionally) — recorded for the ledger, did not
land:** G18 would be CONFIRMED-BY-DERIVATION; FALLS-2 restored to unconditional;
E0-collapse unconditional-on-R-A-only; the unsatisfiability would have had to be
survived setwise/arena-wise. **Had OC3 landed (partner-glue derived) — did not
land:** G18 REFUTED; FALLS-2 void; fields-massive branch opened outright.

---

## TS5 — decision surface

See `DECISION_SURFACE_UPDATE.md`.

---

## Honest substantive/guard split and reuse declaration

**Post-amendment: 50/50 pass, exit 0 = 37 SUBSTANTIVE (29 original + 8
verifier-credited AM1/AM2a–g) + 13 GUARD.** The pre-amendment count was 42/42 = 33
SUBSTANTIVE + 9 GUARD; per the verifier's split audit, 4 of those SUBSTANTIVE rows
were trivial-by-construction — S1f_handshake_germA_flat (0−0 by construction),
S1f_handshake_germB_mirror_seam_value_identity (a substitution identity), and the
K3g phip/rho slots (identically zero even off-locus; the reflection preserves those
slots by construction) — witness-ASSEMBLY steps, not computations. They are now
relabeled GUARD with honest in-script notes; nothing hides behind them (the
verifier: "nothing hides behind them"); so the honest original-computation count is
**29 substantive**. The 8 verifier-credited legs are adopted computations from
`VERIFIER_INDEPENDENT_CHECK.py`: the banked EOMs verified as genuine Euler-Lagrange
equations of the banked reduced Lagrangians (AM2a–d — stronger grounding than the
package's jet-level reuse declaration), mirror-of-G solves G and mirror-of-P fails P
at FUNCTION level with the exact residuals (AM2e–g — the function-level F-C2
discharge), and the A1 counter-computation (AM1). Also per amendment: the dead
variable `germB_val` removed; the K6a single/doubled-momentum mixing noted in-script
(moot — δφ=0 essential kills the π_φ term).

Banked machinery reused (not re-derived): the reduced Lagrangians, banked EOMs
(now additionally VERIFIED as Euler-Lagrange, AM2a–d), doubled-action momenta, and
mirror-jet identities from `derive_universe_fold_d1.py` (blind-verified 2026-07-02) —
re-run here zero-residual as Category-A soundness of this script's reading. New legs:
S1f (underdetermination witness), K3f–K3h (selection adjudication), K4e–K4g
(two-sided WE), K6a–K6d (per-candidate well-posedness + q=0 forcing). The §235
script's no-computation status is reported honestly (its facts recomputed
independently; the verifier confirmed the printer status at source). Three
check-formulation bugs found and fixed during the original run (sympy exp/cosh
canonicalization ×2; one mis-assembled witness expression) — recorded here; no
physics content changed; the verifier corroborated both canonicalization fixes as
genuine SymPy-path issues (its own independent script hit the identical need on the
same two expression families) and confirmed no check condition was weakened.
