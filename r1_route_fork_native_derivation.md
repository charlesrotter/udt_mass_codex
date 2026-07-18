# R1 — The Route Fork: native-derivation attempt (FORCED-A / FORCED-B / FREE)

**Date:** 2026-07-04. **Contract:** `PURSUIT_CHARTER_2026-07-04.md` §3, step R1 (the emphasized
pursuit; armchair-first). **Mode:** derivation only — CAS algebra, no solves, data-blind (no
observational number enters any step; Cassini etc. are NAMED as R2 levers only, never used).
**Script:** `r1_route_fork_cas.py` (sympy, 22/22 PASS; every symbolic claim below carries its
check ID). Purity harness `python3 -m pytest tests/` = 32 passed / 1 xfail (unchanged).
**Status: PROVISIONAL — blind adversarial verifier NOT yet run (owed before banking); NOT
committed.** All reductions are round-static, diagonal, areal/concentric where reduced
(inherited CHOSE ×4, canon C-2026-06-18-1) — but the verdict's load-bearing steps (§2–§4) are
shift-algebra statements made at general transverse `h_AB` wherever possible; round enters only
in the reduced-Lagrangian exhibits.

---

## VERDICT (stated first): **FREE — with a sharpening.**

The positional-dilation principle, applied through the SAME forcing logic that fixed every
other piece of the native action, neither forces nor forbids the mixing term `2√h e^φKφ'`. It
ADMITS it. Moreover the rule-admissible action is not a binary fork but a **two-parameter
family (Z_φ, μ)** — `Z_φ` the invariant-kinetic normalization, `μ` the mixing coefficient
(`μ√h e^φKφ'`) — of which **Route A is the μ=0 slice (Z free)** and **Route B is the single
point (Z, μ) = (8, 2)**. Each route's identity is carried by exactly one extra premise that the
principle does not supply (§5). The decision therefore passes to OBSERVATION (R2) — and the
derivation sharpens what R2 must measure: **the single dimensionless ratio s = 2μ/Z** (the
vacuum-deformation exponent; Route A: s = 0, Route B: s = 1/2) (§6).

Premise set of the verdict: §7. What would change it: §8.

---

## 1. The forcing rule, reconstructed (with citations)

Everything "forced" in the native action was forced by exactly THREE criteria — no others were
ever used as binding:

**(RULE-1) Shift-weight compensation (R1-on-the-action).** Weight each admitted term by the
EXACT INVERSE of its bare weight under the global depth shift φ→φ+λ; in Branch G every bulk
term must end up weight-0; in Branch P the transverse-extrinsic term is licensed to stay
uncompensated by the derived χ-pinning switch. This is P3, the one interpretive lever (CHOSE,
Charles-blessed): `native_dilation_weight_derivation_results.md` §3 (the universal rule; the
e^{2φ} weights, a(φ)=e^{+φ}); `native_field_equations_constrained_two_player_results.md:100-102`
(the 𝒦 bookkeeping: "𝒦 carries shift-weight −2, so it must be compensated by e^{2φ} to preserve
R1, or left uncompensated to break it"); `gp_switch_criterion_results.md` Results 1–3 (the ONLY
shift-breaker is 𝒦; W_χ = e^{2φ}(G)/1(P) fixed by χ-pinning). **Type of the rule: it pins
WEIGHTS (φ-exponents) of admitted terms. It has never pinned a COEFFICIENT** — cf. the free X
in the 4D-frame derivation (`native_dilation_weight_derivation_results.md` §7 "the
kinetic-to-curvature ratio X: R1/R2/R3 fix that BOTH wear e^{2φ} but not their relative
coefficient"; `archive/pre_2026-07-01/F1F3_closure_results.md` §3 "the ONE principle-unfixed parameter"), and the free
Z_φ in the constrained frame (`native_geometric_action_results.md:70-71` "R1 shift symmetry
fixes the FORM φ'² but not its coefficient").

**(RULE-2) Angular flatness — a VALUE criterion.** The transverse (angular-mismatch) block must
assign ZERO action-density to flat geometry; within the stated class {R^{(2)}, K_ABK^AB, K²; same
W_χ on the extrinsic block; no derivative-mixing} this uniquely fixes 𝒦 = K_ABK^AB − K² (b=a,
d=−a): `native_geometric_action_results.md` §(A), blind-verified off-round. Note the class
premises are themselves NAMED CHOSE there ("the angular-flatness / no-derivative-mixing /
same-W_χ premises of the uniqueness class | CHOSE (named)").

**(RULE-3) R2/R3 form constraints.** R2 (composition/Cauchy) forces every weight to be a PURE
exponential; R3 (reciprocity B=1/A) sources the +2 exponent and the +2-vs-+1 anisotropy
(`native_dilation_weight_derivation_results.md` §4). Both refine FORM; neither fixes a
coefficient.

That is the whole rule set. `𝒦`'s uniqueness, the W_χ values, all the e^{kφ} weights, and
a(φ)=e^{+φ} are exhausted by RULE-1..3 plus the constrained-metric frame (itself CHOSE, banked).

---

## 2. The mixing term under the rule: ADMITTED, not required, not forbidden

Candidate: `μ √h e^φ K φ'` (Route B: μ=2; round reduction per steradian `2μρρ'φ'`; d2c M1d).

**(a) Not FORBIDDEN.** Its shift-weight is exactly 0 — `K→e^{-λ}K`, `e^φ→e^{+λ}e^φ`, `φ'`
invariant — so RULE-1 admits it in BOTH branches with NO compensator [A2; confirms d2b E3 "the
mixing term is shift-invariant, hence R1-LEGAL in Branch G", and d2c M2 "branch-blind"]. RULE-2
(flat-value) has no grip: the term vanishes identically on the flat reference (φ'=0), as does
φ'² itself [B1c] — **the entire φ-kinetic sector lives in the intersection of the two criteria's
blind spots** (RULE-1 admits any weight-0 term; RULE-2 cannot see terms that vanish on flat).
RULE-3: the term's weight e^0 is a legal pure exponential; nothing else applies.

*Interrogated sub-fork (the one place a FORBIDDEN-A verdict could have hidden):* one could
upgrade RULE-2 from a VALUE criterion ("flat costs zero action") to a STATIONARITY criterion
("flat solves the vacuum equations") — under which the mixing term IS excluded in G, since flat
fails the Route-B G φ-EOM (residual −4) [B2b, = d2c M4b]. **That upgrade is inadmissible as the
forcing rule, by an internal consistency check: flat-stationarity equally kills the banked
Branch P itself** — the derived P equation `Z(r²φ')' = 4e^{−2φ}` has flat-residual +4 ≠ 0 [B2a].
A criterion that would forbid the banked, χ-pinning-derived Branch P cannot be "the same logic
that forced everything else." Whether flat must be (approximately) a G-vacuum solution is an
OBSERVATIONAL question — exactly R2's confrontation — not a native principle. (This is the
"folds away / reduces to" interrogation the charter demanded, run in reverse: the only candidate
native exclusion of the mixing term smuggles in "vacuum = flat," a GR-flavored import.)

**(b) Not REQUIRED.** The compensation bookkeeping is COMPLETE without it: every term of the
banked Route-A Branch-G action is already exactly weight-0 (√h measure φ-free [A1]; φ'², R^{(2)},
e^{2φ}𝒦, φ-blind L_m all weight-0 [A2]), and the banked Branch-P action breaks the shift ONLY by
the χ-pinning-licensed uncompensated 𝒦 [D1, reproducing d2b §2]. **There is no orphan
shift-weight anywhere in the banked action for the mixing term to be the unique compensator of**
[D1]. RULE-1 requires a compensator only for an admitted weight-carrying term; the mixing term
is weight-0 and compensates nothing.

**(c) Therefore ADMITTED-not-required ⇒ the rule leaves the fork FREE.** And the admission is
not binary: since `φ'²` and `e^φKφ'` are BOTH weight-0, both flat-value-invisible, and mutually
independent (the M5/E3 identity shows the mixing is a φ̃-kinetic minus a ρ'² gradient, not a
multiple of φ'²), the rule-compliant kinetic sector is the two-parameter family

    (Z_φ/2)φ'² + μ e^φKφ' ,   Z_φ and μ both principle-unfixed.

Equivalently, decomposed by provenance [C3, exact IBP identity]:

    (Z₀/2)φ'² + c_L·(−e^{2φ}R_L)  ⇒  Z_φ = Z₀ + 8c_L ,  μ = 2c_L ,

with Z₀ (independent invariant kinetic) and c_L (weighted-longitudinal-curvature block) both
free. **Route A = (Z₀ free, c_L=0). Route B = (Z₀=0, c_L=1).** Two distinguished points on a
free two-parameter sheet; the principle picks neither, and it does not even pick the sheet's
binary A/B slice.

---

## 3. Z_φ = 8: chose or derived? (both routes examined)

**Under Route B: Z_φ=8 is DERIVED — but conditional on TWO premises, both CHOSE.** The chain
(reconstructed and CAS-re-derived from scratch): the longitudinal (t,r)-block 2D curvature is
`R_L = 2e^{−2φ}(φ''−2φ'²)` [C1, computed from the block metric diag(−e^{−2φ}c², e^{2φ}) by an
independent Christoffel/Ricci routine — matches `native_geometric_action_results.md:73`]; its
R1-weighted form `−e^{2φ}R_L = 4φ'²−2φ''` integrates by parts against √h (using `(√h)' = √h e^φK`)
to `√h[4φ'² + 2e^φKφ']` minus a pure boundary term `(2√hφ')'` [C2, exact]. So Z=8 and μ=2 are one
integrand — the "inseparable package" (blind-verified upstream) is CONFIRMED from scratch. The
two conditions:
- **(b1) "the longitudinal kinetic IS the R1-weighted longitudinal-block curvature"** — CHOSE.
  Nothing in RULE-1..3 says the kinetic must descend from curvature; the original 4D derivation
  explicitly treated the curvature-descended kinetic AND an independent kinetic (free X) as
  coexisting (`native_dilation_weight_derivation_results.md` §5), which is precedent AGAINST
  (b1) being forced.
- **(b2) unit relative normalization c_L=1** between the longitudinal-curvature block and the
  transverse block (whose a=1 was itself only a normalization of the transverse-only class) —
  CHOSE. With c_L free, Route B's own premise delivers Z=8c_L, μ=2c_L [C3]: even granting (b1),
  "8" is 8 only if c_L=1. A "one curvature, one coefficient" reading would fix c_L=1 — but WHICH
  curvature object (the 2D block R_L; R^{(3)}; the 4D R) is itself underdetermined, and the three
  give DIFFERENT actions (R^{(3)} = R^{(2)}+𝒦+4e^{−2φ}φ'/ρ ≠ the native integrand,
  `native_geometric_action_results.md:47`; 4D √−g R is EMPTY — pure boundary; the weighted 4D
  e^{2φ}R from the old frame has an e^{+2φ} potential, not P's e^{−2φ} — a different theory
  again). So "curvature completion" is a FAMILY of premises, not a principle.

**Under Route A: Z free is CONSISTENT with the rule — not suspicious.** The charter asked: if
the rule pins all weights, isn't a free Z anomalous? No — resolved by typing the rule: RULE-1
pins **weights (φ-exponents)**, RULE-2 pins the **transverse-block coefficient ratios** (a
value criterion with no grip on the φ-sector [B1c]). Z is a coefficient of an
already-weight-0 term, i.e. exactly the object NEITHER criterion reaches. Precedents: the free X
dial (4D frame, `archive/pre_2026-07-01/F1F3_closure_results.md` §3 — "the one principle-unfixed parameter", bounded by
observation not principle) and the banked "Z_φ free from shift"
(`native_geometric_action_results.md:70-71`). The fork's coefficients (Z, μ) are the
constrained-frame descendants of the same known blind spot. The asymmetry "everything forced
except Z" dissolves: everything WEIGHT-like is forced; nothing COEFFICIENT-like ever was.

**The live solvers' Z=8:** remains exactly what the banked re-tag says — Route-B's number
carried as a Route-A probe, not derived (`f_rtheta_free_field_MAP.md` OBS-2;
`cell_solver_universe_T3.py:12-18`). Nothing here changes that posture; this derivation removes
any hope that the number 8 could be promoted without buying (b1)+(b2).

---

## 4. The equivalence question — SETTLED: not equivalent; and the precise sense in which they almost are

The d2c identity (M5) generalizes exactly [E3]: with **φ̃ = φ + (2μ/Z)ln ρ**,

    (Z/2)ρ²φ'² + 2μρρ'φ'  ≡  (Z/2)ρ²φ̃'²  −  (2μ²/Z)ρ'²      (Route B: −ρ'² exactly).

**(i) In VACUUM Branch G the routes are dynamically isomorphic — this is new and sharper than
"minus a ρ'² term."** The full reduced vacuum-G Lagrangian maps EXACTLY onto the Route-A form at
the SAME Z under the constant field rescaling ψ = kφ̃, σ = ρ/k, k² = Z/(Z+μ²) [E4]. So no
vacuum-G dynamics alone can ever distinguish the routes up to relabeling of solutions —
consistent with (and explaining) d2b's verifier extension "T-G1 route-robust."

**(ii) But the isomorphism is dynamics-only, NOT physics — the routes are NOT equivalent
theories.** Three independent breaks, each exact:
- **The metric anchoring:** the observables are built from (φ, ρ) — g_tt = −e^{−2φ}c²,
  g_rr = e^{+2φ}, area 4πρ², a(φ)=e^{+φ} on matter. Under the E4 map,
  g_rr → e^{2ψ/k}(kσ)^{−4μ/Z} [E6]: for μ≠0 the "equivalent" variables are NOT the
  dilation/areal pair of any same-form UDT metric. Rescaling φ is not a gauge move — φ's
  normalization is pinned upstream by the metric form (canon C-2026-06-18-1), which the fork
  does not touch. (This is also why a(φ)=e^{+φ} is fork-consistent: it rides g_tt, upstream of
  the fork, identical in both routes.)
- **Branch P kills the map:** in tilde variables the P gradient coefficient becomes
  `2e^{−2φ̃}ρ^{4μ/Z} + 2μ²/Z` — explicitly ρ-dependent iff μ≠0 [E5]; no constant rescaling (nor,
  by the anchoring argument, any observable-preserving redefinition) removes μ where the depth
  field is dynamically anchored (P's source, matter, junctions — d2c M9's coupled JCs and the
  φ'-jump are the junction face of the same fact).
- **Symmetry relocation:** the mixing term flips sign under the φ-reflection φ→2a−φ [F1], so
  Route B's bulk symmetry class in G is φ̃→φ̃+c and φ̃→2a−φ̃, not φ's [F2]. Route B RELOCATES
  the entire shift/fold/monodromy structure from φ to φ̃ (the flux is q_B = Zρ²φ̃'; d2c M8c/M9c
  are the junction shadow of this). The banked canon-fold pins still survive Route B — via the
  jump analysis (d2c M6/M7), not via bulk symmetry — no contradiction, but the natural
  fold-anchoring moves.

**(iii) What the −ρ'² term physically encodes:** it is −(2μ²/Z)ρ'² — the induced depth-kinetic
cost of transverse growth. Route B asserts that **changing the transverse area itself drags the
depth field** (areal growth carries dilation flux: Φ = Zρ²φ' + 2μρρ' [E1]); equivalently the
physical depth acquires a geometric component (2μ/Z)ln ρ. This is a φ-ANGULAR coupling at the
KINETIC level (dilaton gradient × transverse expansion — as the off-round verifier put it),
distinct from and additional to Branch P's potential-level coupling (the e^{−2φ} source). Its
cleanest physical face: **Route-B G-vacuum clocks are slaved to the areal radius**,
e^{−2φ} ∝ ρ^{+2s}, s = 2μ/Z [E2a] — Route A's vacuum clocks are position-free.

---

## 5. The two routes' identities, as premises (the crisp ledger)

| | extra premise beyond RULE-1..3 | status |
|---|---|---|
| **Route A** | sector-orthogonality / "no derivative-mixing" (sets μ=0; then Z free) | **CHOSE** — named as such in the banked uniqueness class (`native_geometric_action_results.md` ledger); RULE-1 cannot supply it (the mixing term is R1-legal, d2b E3 + [A2]) |
| **Route B** | (b1) kinetic = weighted longitudinal-block curvature AND (b2) c_L=1 (sets Z₀=0, c_L=1 ⇒ Z=8, μ=2) | **CHOSE ×2** — (b1) has explicit precedent against forcedness (the free-X coexistence, §3); (b2) is a normalization across blocks that no stated principle ties |
| general rule-compliant action | none — (Z, μ) free | what RULE-1..3 actually deliver [A2, B1c, C3, D1] |

Neither route is forced; neither is forbidden. **FREE.**

---

## 6. What OBSERVATION discriminates (the R2 feed)

1. **The vacuum-deformation exponent s = 2μ/Z — the primary, quantitative lever.** For every
   (Z, μ) the Branch-G "flat-analog" vacuum is ρ = ar+b, φ = φ₀ − s·ln ρ [E2a — generalizing
   d2c M4c], i.e. clock rate e^{−2φ} ∝ ρ^{2s} in the exterior. Route A: s=0 (flat solves G
   [E2b]). Route B: s=1/2. **R2 should be framed as a MEASUREMENT/BOUND on s, not a binary A/B
   test:** a solid macro bound |s| < s_max kills Route B (s=1/2) if s_max < 1/2, but leaves the
   small-μ family alive — say so up front to avoid a false binary. (Cassini-class solar-system
   bounds, terrestrial clocks, the a(φ) both-extremes rule — per the charter's R2 list; no
   number used here.)
2. **G|P junction structure (internal/structural):** μ≠0 couples the junction conditions and
   makes φ' itself jump at a G|P seal (d2c §1.3); with μ=0 they decouple. Downstream face: the
   Route-A sign obstruction (the G|P particle architecture closes NOWHERE, d2c §2.3) is OPEN at
   μ≠0 via φ̃-monotonicity — so an eventually-CONFIRMED G|P-architecture particle would itself
   be evidence for μ≠0. Necessary-not-sufficient, as banked.
3. **Flux-without-twist (structural):** under μ≠0 a canon-fold (untwisted) odd+odd closed
   G-domain can carry q = (2μ/Z)·Z·ln(ρ₂/ρ₁)/∫dr/ρ² ≠ 0 (d2b E3) — under μ=0 it cannot. Any
   banked structure that REQUIRES a flux-carrying pure-G segment between canon folds would
   discriminate.
4. **Ladder interiors (R3's job):** fold pins and E_ang(core)=2 are family-robust ([E7] extends
   the d2c M6 robustness to ALL (Z,μ), so the R3 re-run is well-posed across the whole sheet);
   interior profiles and rung numerics are not — the ladder's survival/movement under (Z,μ)≠(8,0-mixing)
   is a discriminator against the banked Stage-D data ONLY in the consilience sense (data-blind
   discipline applies).

Named NON-discriminators (derived here, save R2 the dead ends): vacuum-G dynamics alone
(isomorphic, [E4]); kinetic-signature/ghost-type health (indefinite for ALL (Z>0, μ) — the
conformal-mode-type indefiniteness is route-blind [G1]).

---

## 7. Premise set of the FREE verdict (every fixed thing tagged)

| # | premise | tag |
|---|---|---|
| 1 | P3: R1-on-the-action = global constant-shift invariance | **CHOSE** (inherited, Charles-blessed; the whole action program rides it) |
| 2 | Constrained two-player metric form (φ longitudinal, h_AB transverse) | **CHOSE** (banked, `native_field_equations…md` ledger) |
| 3 | P7'-analog: the shift acts at fixed transverse geometry (h_AB inert) | **CHOSE** (inherited; verifier-confirmed chart-independent upstream) |
| 4 | Term inventory class: local, second-order, built from {φ', K_AB, R^{(2)}, h}, same-W_χ extrinsic block | **CHOSE** (inherited from the banked uniqueness class; completeness within it checked at [A2] — at this order the weight-0 φ-sector candidates are exactly φ'² and e^φKφ'; the K-quadratics are flat-value-excluded [B1b]) |
| 5 | RULE-2 in VALUE form (not stationarity) | **DERIVED-disambiguated here** [B2a/B2b]: the stationarity form is inconsistent with the banked Branch P — the only self-consistent reading is value-form |
| 6 | χ-pinning switch fixes W_χ only | DERIVED (banked, blind-verified) |
| 7 | Matter φ-blind (channel-corrected) | DERIVED upstream, conditional on R1+P5 (CHOSE) levers |
| 8 | Round reduction per steradian for the exhibits; Z>0 for fold nondegeneracy | convention (controlled by reproducing banked L̄ forms); Z>0 = banked probe posture (d2c verifier correction 1) |
| 9 | Flat reference for RULE-2 = (φ=0, ρ=r) | **CHOSE-cited** (the banked flatness test; the G cancellation itself holds for any φ [B1a]) |
| 10 | All symbolic claims | DERIVED (CAS 22/22, `r1_route_fork_cas.py`) |

**Every CHOSE I made MYSELF in this task** (beyond inherited ones): the (Z, μ) parameterization
of the admissible family (a bookkeeping choice; [C3] ties it exactly to the (Z₀, c_L)
provenance decomposition); the log-space comparison in E6 (a CAS mechanics choice, not physics);
premise 9's reuse of the banked flat reference. Nothing else was fixed by me.

---

## 8. What would change the verdict

- **A coefficient-pinning principle** (the known blind spot, twice precedented as honestly-open:
  X, Z). If Charles adopts a "single weighted-curvature origin" postulate — all geometric terms
  descend from ONE curvature object with ONE coefficient — the verdict moves toward FORCED-B,
  **but only after a further choice of WHICH curvature object** (R_L-block vs R^{(3)} vs
  weighted-4D-R give three DIFFERENT actions, §3(b2)); as posed today it is a premise family,
  not a principle. STOP-flagged as Charles's call, not resolvable here.
- **Refutation of the B2 disambiguation:** if flat-stationarity could be derived natively
  WITHOUT killing Branch P (I found no way — the P source is the very mechanism the ladder
  rides), the mixing term would be FORBIDDEN in G and the verdict would move toward FORCED-A
  (in G). Attack here first.
- **A new shift-invariant term at the stated order that I missed** [attack A2/B1]: it would not
  change FREE but would widen the family R2 must bound.
- **Dropping premise 2 or 3** (the constrained frame / inert-h shift): the fork as posed
  dissolves and the question re-poses in whatever frame replaces it.

## ATTACK HERE (for the blind verifier)

1. **The B2 disambiguation is load-bearing for "not forbidden":** re-derive both flat residuals
   ([B2a] +4 for banked P; [B2b] −4 for Route-B G) independently; hunt any OTHER native reading
   of the flatness criterion that excludes the mixing term but spares Branch P.
2. **The no-orphan claim [D1]:** re-run the full shift audit of both banked actions from
   scratch (including matter, measure, boundary terms); any uncompensated residue I missed
   would convert the mixing term into a candidate REQUIRED compensator and break FREE.
3. **The inventory completeness (premise 4):** enumerate weight-0, flat-value-passing φ-sector
   scalars at second order independently. Is e^φKφ' really the only mixing candidate? (e.g.
   e^φK_AB∂h-contractions beyond the trace; terms with R^{(2)}φ'-structure need a length scale —
   confirm.)
4. **The vacuum-G isomorphism [E4] and its physics-breaking [E5/E6]:** verify k²=Z/(Z+μ²) from
   scratch; confirm the map fails once ANY φ-anchored structure (a(φ), P-source, JC data)
   enters; confirm no cleverer (non-constant) redefinition preserves the metric FORM while
   equating the routes (§4's anchoring argument — the weakest-stated link; make it exact).
5. **The Z=8 provenance conditions (b1)/(b2):** is there a stated principle anywhere in the
   corpus that ties the cross-block normalization c_L=1 (I found none)? Check the three
   curvature-object candidates really give three different actions.
6. **The s = 2μ/Z generalization [E2a]:** independently solve the general-(Z,μ) G system;
   confirm the flat-analog family and that s is the ONLY vacuum-deformation invariant at this
   order (does the ρ-EOM add a second observable?).

## LAB-LOG

- 2026-07-04: derivation + `r1_route_fork_cas.py` built and run — 22/22 PASS (one E6 comparison
  initially failed on sympy power/log canonicalization, fixed by comparing in log space —
  mechanics, not physics). pytest 32/1xfail unchanged. Single process, seconds, no solves,
  data-blind. NOT committed; blind adversarial verifier pass OWED before banking
  (verifier-before-record). STOP-flags for Charles carried out of scope: (i) the
  "single-curvature-origin" premise family (§8, would-force-B-modulo-a-choice); (ii) the fork is
  a two-parameter SHEET, so R2 should be framed as bounding s = 2μ/Z, not as a binary A/B test.

---

## VERIFIER RECORD (blind adversarial pass — agent a31db58f300da6011, 2026-07-04): ALL 8 ATTACKS HOLD — SAFE TO BANK

Own reduction from the source actions (own Christoffel/Ricci/EL; r1_bv_main.py 35/35 +
r1_bv_inventory.py 4/4); the deliverer's CAS 22/22 reproduces; pytest 32/1xfail; data-blind clean.

**The gate (B2) HOLDS, STRENGTHENED:** both flat-stationarity residuals re-derived exactly
(banked Route-A P: +4; Route-B G: −4; general μ: −2μ — the criterion kills every μ≠0 AND banked
P equally); "value-form" is the source derivation's own wording throughout (not a retrofit);
THREE candidate exclusion readings hunted and closed — transverse-scoped stationarity SPARES the
mixing anyway (all ρ-ELs vanish on flat); φ-EOM stationarity is outside RULE-2's scope and kills
P; φ-reflection-evenness kills banked P's own e^{−2φ}ρ'² identically. The one surviving
exclusion ("flat must be a G-vacuum solution") is precedent-free, extensionally "vacuum = flat"
(a GR-flavored import), and is exactly R2's empirical question — correctly a Charles-level
what-would-change item, not a native principle.

**Verifier sharpenings (recorded, none against the verdict):** (i) the rule-typing precedent
hunt found NO coefficient RULE-1 ever pinned (X free, Z free; the b=a,d=−a pins are RULE-2
transverse-ratio grips, correctly typed); (ii) **E6b (exact, closes the anchoring gap): for any
μ≠0, Branch G admits NO solution with φ≡const and ρ'≠0** — flat observables are Route-A-reachable
and Route-B-unreachable; the solution sets differ at the (g_tt, g_rr, area) level, so NO
redefinition can equate the routes while preserving anchoring ⇒ s = 2μ/Z is genuinely
observable; (iii) the R⁽³⁾ identity citation is the ρ=r form (general ρ gains
4e^{−2φ}(φ'ρ'−ρ'')/ρ — cosmetic scope note). Also verified exact: the weight-0/no-orphan audit
at GENERAL transverse h_AB (incl. matter, a(φ)dτ, IBP boundary); the order-≤2 inventory closes
(φ'' is IBP-identical to −mixing — relabels the sheet, doesn't widen it); the (Z,μ) sheet
rule-admissible everywhere; all three curvature objects pairwise differ at EL level; fold-pin
det = −4ρ²(WZ+μ²) ≠ 0 across the sheet (R3 well-posed; matches d2c M6 at (8,2)); the flat-analog
+ single-exponent claim (s is the ONLY route-dependence in vacuum-G observables); Z=8+μ=2 one
integrand (IBP-inseparable). The two STOP-flags correctly deferred to Charles.
