# BLIND VERIFIER REPORT — P4 coupling derivation (udt_p4_coupling_derivation_2026-07-31)

Verifier: blind adversarial, same-session-spawned (NOT a hosted external model — this
caveat travels with the verdict). Date: 2026-07-31. Zero prior context; adjudication
against the frozen contract `PREREGISTRATION.md` (commit 5afbab6) only.

## Duty 0 — rerun / contract-first
- Contract-first CONFIRMED via git: 5afbab6 (08:18) commits PREREGISTRATION.md + LIVE.md
  only; all six artifacts written after (08:30–08:32 mtimes), none yet committed.
- Rerun in scratchpad: exit 0; stdout byte-identical (sha256 f8c19548...) and
  coupling_results.json byte-identical (sha256 071882c3...) to the package copies.
- Check split audited: 25 = 21 SUBSTANTIVE + 4 GUARD (S1g, S2f, S3b, S4b). The four
  guards are genuinely citation/map rows (assert True + cited banks) — split honest.
- No floats / numeric solvers / random / GPU in the script (grep + read: confirmed;
  the single "float" grep hit is the word in a comment context — none in code).

(Findings below written incrementally; verdict at end.)

## Independent script
`VERIFIER_INDEPENDENT_CHECK.py` (this package, preserved; 21/21 own-checks pass): re-derives
the lattice cut, spacing, lock-class law, witness J=pi, f-contrast, sigma-additivity (+ its
diagonal-scoping necessity), n^2-share, J05 identity, 3-moment completion, det factorization,
sheet signs, Hom(D-inf,Z)=0 — all independently CONFIRMED — then runs the attack legs below.

## Priority (1) — the lattice cut: CONFIRMED
c_theta = g_theta(2pi n_w − ΣJ_s)/ΣJ_i re-derived from the doorway integer condition + the
MB-J closure (momentum continuity is stamped as completion data — fine). Spacing 2pi g/ΣJ_i
and lock-class c = pi g n_w/ell confirmed by independent integration. 2pi provenance clean:
enters only via single-valuedness of e^{i theta} (the banked doorway condition itself carries
it; nothing inserted). n^2-share exact; sigma-additivity correctly scoped to diagonal Gram
(I verified off-diagonal breaks it — the package's Category-A congruence caveat is honest).
THE ESCAPE IS REAL: re-derived the banked C6c kill — a REAL-target moment on a cycle obeys
closure = 0 (slope killed => E0=0); the circle target replaces "=0" by "in 2piZ". The escape
rides ONLY on the registered target, exactly as claimed; the f-contrast recomputation in
S2c is faithful to the banked mechanism.

## Priority (2) — disjointness: HOLDS AT THE BANKED LAYER, with two real gaps
Banked scaffolding checked at source: period-gate completion menu (chains/rings, 2-valent
seams; quotient carries the LIVE cycle gamma_T with identically-vanishing periods); the
certified massive C6b witness has ONE crease end; stability SB2 double-crease massive EMPTY
(TOTAL both E0 signs) + family-(ii) quotient parity-collapse exclusion. Both directions of
S2h re-run. Findings:
- **(A2, amendment required)** S2h's eps_theta=−1 leg is UNDER-DERIVED and in tension with
  the package's OWN S1h census. S1h: the eps=−1 crease KILLS the theta''-trace. On-shell
  MB-J gives theta'' = −c_theta w'/(g_theta w^2); on the certified witness w'(crease) = −1
  ≠ 0 (generally ±sqrt(2A) ≠ 0 on every nonconstant crease-compatible cell), so the jet-2
  kill forces c_theta·w'(crease) = 0 ⇒ c_theta = 0 at eps=−1 creases TOO. S2h claims eps=−1
  "frees theta'" and kills c_theta only at eps=+1. Either S1h's jet-2 kill applies on-shell
  (then c_theta = 0 both signs — disjointness STRENGTHENED, S2h/TC-4 rows change) or the
  kill must be re-scoped (mirror acts on w nontrivially — w'(crease) ≠ 0 means w is NOT
  even about the crease, so the naive parity ladder may not bind theta on-shell); the
  package asserts both halves without reconciling. This adjudication is LOAD-BEARING: if
  the kill does NOT apply, a hypothetical two-crease massive chain would carry a piZ two-pin
  lattice (see next), touching the honest-limit.
- **(Upstream caveat, not this package's error)** the stability bank's "every massive S-i
  realization has at most ONE crease end" is derived from single-cell facts (SB2 + C2d);
  an N=2 crease–glue–crease chain with per-cell I_p=0 (two mirror-image C6b cells) is not
  covered by that argument. The coupling package cites the bank in good faith; flag travels
  upstream. Under EITHER A2 resolution with the kill live, such a chain carries no c_theta
  lattice, so the honest-limit survives; if the kill is re-scoped away, this gap becomes
  material.
- **Cycle+pin completion:** none found in the banked census (confirmed): rings have no
  ends, chains no cycles, the quotient's cycle has winding hom = 0 (Hom(D-inf,Z)=0,
  re-proven). S2f's justification wording ("acyclic") is looser than the census (which
  types gamma_T as a LIVE cycle with vanishing periods) — the conclusion stands via S4a.

## Priority (3) — menu completeness: one admission-chain ERROR + one grading defect
- **(A1, amendment required — the one computed error found)** the THB block table misgrades
  thp*thpp (theta'·theta'') as theta-ODD (parity 1). True character: chi_theta^2 = TRIVIAL
  (verified symbolically; 12/13 other blocks correct). The shipped JSON menu table therefore
  wrongly ADMITS bare theta'·theta'' DIRECT into the shear slot r_sh at chi_theta = chi_a
  (and wrongly demands module dressing in trivial rows) — an F-C2-adjacent admission-chain
  error for one block. Class-level menu (6 classes) and all headline cuts are UNAFFECTED
  (the canonical MB-J rep and every S2 computation use theta' only).
- The block list's grading rule is inconsistent as stated: the comment bounds "TOTAL jet
  order <= 2" yet includes thp*thpp (total 3) and excludes thpp^2 (highest-derivative 2).
  Class-level completeness is unaffected (such blocks live inside MB-J "even combos"), but
  S1d's "exhaustive" is exhaustive only relative to an imprecisely-specified list — state
  the rule and regenerate. No genuinely NEW lawful class found: I hunted products (covered
  by the cross classes), theta-dependent weights (MB-W + the S1e seam-locus rule), wall-bulk
  mixes (MW-N + J05's two-seat proof S1f — re-proven independently), nonlocal/anchored
  (exclusion witness −s^2 re-run). The two audited exclusions (bare theta 2pi-residual;
  anchored-nonlocal co-translation) are sound at source.
- **(A3, amendment required — missed integer leg, massless-confined)** on the banked
  PERMITTED crease|crease (mirrored) completion, CONSTANT stratum w ≡ 1 (crease conditions
  0=0; even w, so the A2 tension vanishes), eps_theta = −1 pins BOTH crease values in
  {0, pi}: the MB-J lift increment obeys (c_theta/g_theta)·2ell ∈ piZ ⇒ c_theta =
  pi·g_theta·m/(2ell), m ∈ Z — a Z-lattice cut on an ACYCLIC completion, HALF the cyclic
  lock-class spacing. This contradicts the package's framing that the Z-cut lives on cyclic
  completions ONLY and S4a's "quotient integer content = crease Z2 data only" (the two-pin
  lattice is not a winding hom, so Hom(D-inf,Z)=0 does not close it). It is CONFINED to
  massless sectors (double-crease massive EMPTY + family-(ii) quotient exclusion, banked),
  so the honest limits on E0/ell and the certified-massive disjointness SURVIVE — but TC-2/
  TC-4 understate the massless integer content.

## Priorities (4)+(5) — stability transport and label map: CONFIRMED
3-moment completion identity, det B3 = g_theta k^2 det B2 at a_F=0, and the opposite-sheet
cos(0)/cos(pi) signs re-proven independently (P4b/P4c/P4d). a_F = 2·lambda = 0 at the P1-4D
landing and a_F = 1 at P1-triad match the banked branch values; the P1-triad cross channel
honestly left as a NAMED SEAT. S3b's verbatim-transport is a GUARD (cited, not computed) and
is labeled so — honest. Hom(D-inf,Z) = 0 re-proven; (Z2)^2 = 4 sheets; "labels sheets, never
states" framing held everywhere.

## Falsifier hunts
- **F-C3 (first):** stamps present in script details, EXACT_DERIVATION standing block, JSON.
  ONE gap: COUPLING_LEDGER.tsv carries NO IF-ADOPTED banner or column (a single incidental
  "IF adopted" in the MB-Xf row); as a standalone file its TC2 cut column reads unconditional.
  Amendment: add the conditional banner/stamp to the ledger.
- **F-C1:** attacked both directions. Cutting legs are computed; the honest-none legs (S2f
  E0-no-close, S2g theta-free ring law) — S2g computed, S2f a guard citing banks (acceptable:
  it is a map fact). The A3 miss is an UNDER-claim of a cutting leg on the massless side —
  i.e., the package under-reported a cut, the opposite of catalog-steering; no steering found.
- **F-C2:** admission chains genuinely derived except the A1 one-block misgrade (above).
  No naturalness smuggle found.
- **F-C4:** IF-ADOPTED/REGISTERED framing survives everywhere sampled (19 script, 7 EXACT,
  DECISION_SURFACE explicit "nothing adopted/no recommendation"); the DECISION_SURFACE's
  "the two live ones" is descriptive (cut-content vs typed), not a recommendation — but it
  edges toward member-highlighting; watch it at adoption time. No creep found.
- **F-C5:** no bank contradiction found; A2 is an INTERNAL S1h-vs-S2h tension; A3 contradicts
  only the package's own summary rows, not a bank.
- **F-C6:** none; exit 0; deterministic; byte-identical rerun.
- **Contract TC-1..TC-5 + ceiling:** all five targets delivered in the contracted form;
  ceiling honored (nothing adopted, no coupling selected, no spectrum claimed — "labels
  never states" held; DECISION_SURFACE contains no recommendation).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS
The load-bearing spine — the six-class menu, the exclusions, the lattice cut and its 2pi
provenance, the lock-class spacing, the n^2 form, the slope-kill escape, the E0-no-close,
the stability transport, the label map — is CONFIRMED by independent re-derivation (21/21).
No refutation. Four REQUIRED amendments:
- **AM-1 (A1):** fix the thp*thpp parity to EVEN in THB; regenerate the menu table (it
  currently mis-admits bare theta'·theta'' into r_sh at chi_a); state the block-grading
  rule precisely (and either include thpp^2-type blocks or bound by total order honestly).
- **AM-2 (A2):** adjudicate the eps_theta = −1 crease jet-2 condition under MB-J closure
  (S1h theta''-kill vs S2h free-c_theta — currently contradictory on the certified witness,
  where on-shell theta''(crease) = c_theta/g_theta ≠ 0); restate S2h's eps=−1 remainder and
  the TC-4 chain row per the outcome. Note: c_theta = 0 both signs would STRENGTHEN
  disjointness; the alternative re-scoping must be derived, not assumed.
- **AM-3 (A3):** add the two-pin piZ lattice on the banked mirrored-cell (double-crease,
  eps=−1) constant stratum — c_theta = pi g_theta m/(2ell) — to TC-2 and the TC-4 map
  (massless-confined; honest limits unchanged); correct "the Z-cut lives on cyclic
  completions" and "quotient integer content = Z2 only" accordingly.
- **AM-4:** stamp COUPLING_LEDGER.tsv with the IF-ADOPTED conditional (banner or column).
Upstream flag (not an amendment here): the stability bank's "at most ONE crease end" is
single-cell-derived; the N=2 crease–glue–crease per-cell-I_p=0 chain is unadjudicated there.

Blind verifier, same-session-spawned (not a hosted external model), 2026-07-31.

# CLOSURE ROUND — 2026-07-31 (same blind verifier, same-session-spawned caveat travels)

Adjudicating the amendment layer (CORRECTION_LAYER.md; contract, my round-1 report, and my
script untouched — confirmed by mtime/content). Independent closure checks appended to
`VERIFIER_INDEPENDENT_CHECK.py` (now 27/27 own-checks pass).

## Duty 1 — rerun/split
Amended script: exit 0; TWO reruns byte-identical to each other AND to the shipped
DERIVATION_STDOUT.txt + coupling_results.json (sha256 85653cc5… / 70708f68…). 30 = 26
SUBSTANTIVE + 4 GUARD: the five new checks (AM1, AM2a, AM2b, AM2c, AM3) are all genuine
zero-residual computations — SUBSTANTIVE labels honest; the 4 guards unchanged. Purity holds.

## Duty 2 — AM-2 adjudicated HARDEST: SOUND, and genuinely forced
I attacked the convenient-direction worry with an independent re-derivation (C1a/C1b/C2):
- The precedent is REAL, not analogy: solving {p0(crease)=0, p0''(crease)=0} on-shell
  (p0 = ln w/a_F) for (w1, w0) reproduces the banked C6b crease branch EXACTLY
  (w1 = 2A−√(2A), w0 = 1+A−√(2A)) — i.e. the period gate's own crease conditions ARE the
  even-jet kill applied on-shell, binding cell data, with w'(crease) = −√(2A) ≠ 0 and odd
  jets free. A lawful re-scoping that spares θ would dissolve the rule that generates the
  bank's own crease conditions (F-C5) — my round-1 "mirror acts on w nontrivially" escape
  is thereby closed: the bank imposes jet-level kills, not global parity, and does so
  on-shell. The adjudicated direction is DERIVED, not chosen to resolve my finding.
- The forcing re-derived at general A: θ''(crease) = c_θ√(2A)/g_θ; solveset ⇒ c_θ = 0 for
  every A > 0; constant stratum genuinely vacuous (θ'' ≡ 0). Massive ⟺ A ≠ 0 checks out
  (E0 = 2A·g_p/a_F²).
- Chain-wide spread of c_θ = 0: rides momentum continuity — the SAME supplied completion
  datum S2c's lattice cut rides, used symmetrically in the cutting and killing directions;
  stamped, not smuggled. Acceptable.
- Withdrawal completeness: the "ε=−1 frees θ′" remainder is withdrawn in S2h (script),
  EXACT_DERIVATION Stage-2, ledger MB-J row, decision surface, TC-4 rows. ONE residue:
  EXACT_DERIVATION line ~63 (Stage-1 S1h summary) still reads "θ′-trace LIVE" without an
  AM-2 cross-reference. As a KINEMATIC slot-census fact it is true (and MW-N needs it);
  only the on-shell MB-J consequence changed. RECOMMENDED (not required): add "(on-shell
  MB-J consequence: see AM-2)" there.
- My round-1 upstream flag (N=2 crease–glue–crease chain): under this verdict such a chain
  forces c_θ = 0 at both creased ends regardless of its (unadjudicated) massive status —
  immaterial for the θ-layer, as claimed. The upstream flag itself still travels.

## Duty 3 — AM-1: rule genuinely derived; table complete
Factors = the banked jet-ORDER ≤ 2 entries; monomial DEGREE ≤ 2 = the quadratic layer the
banked pairing/second-variation machinery carries (higher degrees TYPED by the parity rule,
not silently dropped — honest, and the parity typing is exact since χ_θ² = trivial).
Independent enumeration (C3): jet monomials of degree ≤ 2 over {θ′, θ″} = 6; × {1, cos, sin}
= 18 — the table is COMPLETE under the stated rule. Parity now computed symbolically per
block and cross-checked against the odd-count rule in-script; my round-1 misgrade is fixed
in the shipped JSON (C4: θ′θ″ direct in trivial rows, absent from r_sh@χ_a; θ″²-family
present and correctly graded). Class-level menu unchanged — correct.

## Duty 4 — AM-3 integration: consistent and accurate
Pin-pin lattice verified in-package (AM3 check) and independently (C5: half-spacing ratio
1/2 exact). CYCLE-WINDING vs PIN-PIN framing now consistent across EXACT_DERIVATION (S2f,
TC-4, amendment section), DECISION_SURFACE (honest-limits block restated), ledger MB-J row.
AM-2 interaction verified both ways (lattice lives exactly where the forcing is vacuous).
Post-amendment honest limits ACCURATE: E0 uncut everywhere (the pin-pin lattice is
massless-confined by banked SB2-both-signs + family-(ii) quotient exclusion — cited
correctly); ℓ conditional-only (fixed-c_θ shape); disjointness now DERIVED at both ε signs
— a stronger and cleaner statement than round 1's census-observed version.

## Duty 5 — F-C3 / F-C4
Ledger IF-ADOPTED banner present and complete (θ REGISTERED-NOT-ADOPTED; g_θ free; c_θ a
θ-sector datum); stamps intact elsewhere. F-C4: amended DECISION_SURFACE keeps explicit
"no coupling is recommended / the decision is yours"; the amendment framing ("massive side
POORER, massless side RICHER") is descriptive, not steering. No adoption creep found.

## CLOSURE VERDICT: **CLOSED**
All four required amendments implemented at derivation grade; AM-2 — the load-bearing one —
survives independent adversarial re-derivation (the direction is forced by the banked C6a/
C6b precedent, which I reproduced from scratch). No further amendments REQUIRED. One
RECOMMENDED cosmetic: the S1h "θ′-trace LIVE" cross-ref (above). Upstream flag unchanged
(stability bank's "at most ONE crease end" is single-cell-derived — travels upstream, not
blocking here). Package outcome stands as OC-2 with: six-class menu (18-block table),
cycle-winding + pin-pin lattices (massless side), c_θ = 0 forced at every crease end of
every nonconstant cell (massive side), E0/ℓ never unconditionally cut, nothing adopted.

Blind verifier, same-session-spawned (not a hosted external model), 2026-07-31.
