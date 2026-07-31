# CORRECTION LAYER — P4 coupling derivation (amendments, 2026-07-31, verifier round 1)

Verifier verdict: **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`, blind
adversarial, same-session-spawned — that caveat travels). Four required amendments, all
implemented here, derivation-grade. Script `derive_coupling.py` amended: **25 checks →
30 checks (26 SUBSTANTIVE + 4 GUARD), exit 0, rerun byte-identical**; JSON + stdout
regenerated. Frozen contract `PREREGISTRATION.md` untouched; `VERIFIER_REPORT.md` and
`VERIFIER_INDEPENDENT_CHECK.py` preserved untouched. Everything below stays IF-ADOPTED
conditional (θ REGISTERED-NOT-ADOPTED; nothing adopted, no coupling selected, no spectrum).

## AM-1 — the θ′·θ″ misgrade (a computed error we made)

- **Found:** the shipped THB block table hand-graded θ′·θ″ as θ-ODD; its true K₄ character
  is TRIVIAL (χ_θ² = trivial; verifier confirmed 12/13 other blocks correct). Consequence:
  the shipped JSON menu wrongly ADMITTED bare θ′θ″ direct into the shear slot r_sh at
  χ_θ = χ_a and wrongly demanded module dressing in trivial rows (F-C2-adjacent, one
  block). The grading rule as written was also inconsistent (bounded "total jet order ≤ 2"
  yet listed θ′θ″ (total 3) and excluded θ″²).
- **Changed:** the block grading rule is now STATED and uniform, derived from the banked
  jet-layer ≤ 2 admission: factors = legal 2-jet entries ({1, cos, sin} × jets {θ′, θ″};
  the banked bound is each entry's JET ORDER ≤ 2), table = monomials of jet DEGREE ≤ 2
  (the quadratic layer the banked pairing/second-variation machinery carries; higher
  degrees typed by parity = odd-factor count mod 2). Parity is now COMPUTED symbolically
  per block (θ → s·θ, s = ±1), never hand-listed (`AM1` check). Table: 13 → 18 blocks
  (adds θ″², cos θ·θ′θ″, cos θ·θ″² even; sin θ·θ′θ″, sin θ·θ″² odd; removes none);
  θ′θ″ regraded EVEN. Menu regenerated (JSON, ledger, EXACT_DERIVATION Stage-1).
- **Corrected claim:** bare θ′θ″ enters TRIVIAL rows for every χ_θ; it does NOT sit in
  r_sh at χ_θ = χ_a. **Survived unchanged:** the six-member class-level menu, every
  exclusion, every S2/S3 computation (all use θ′ only through the canonical MB-J rep).

## AM-2 — the ε_θ = −1 crease jet-2 adjudication (an internal contradiction, adjudicated)

- **Found:** S2h claimed ε_θ = −1 "frees θ′" (lattice-capable), contradicting the
  package's OWN S1h census (ε_θ = −1 kills the θ″-trace): on-shell MB-J gives
  θ″ = −c_θw′/(g_θw²), and w′(crease) = ±√(2A) ≠ 0 on every nonconstant cell — the kill,
  if it applies on-shell, forces c_θ = 0 there. Load-bearing for the disjointness claim.
- **Adjudicated by derivation from the banked census (checks `AM2a`–`AM2c`):**
  - `AM2a` (the banked precedent, recomputed): the period-gate C6a mirror-jet kill
    (ε_φ = −1 DEFINITIONAL) applies ON-SHELL as a trace condition and BINDS cell data:
    p0″(crease) = 0 ⟺ 2A·w = w′², holding exactly on the certified crease branch where
    w′(crease) = −√(2A) ≠ 0. A declared-parity field has NO "fold-kink" escape; re-scoping
    θ's kill would dissolve C6a's own banked crease conditions (F-C5 contradiction). θ's
    jet-0 leg ({0,π} 2-torsion) is already banked (doorway C5d) — the census is uniform.
  - `AM2b` (the exact condition): θ″(crease) = c_θ√(2A)/g_θ on the crease branch; the kill
    solves EXACTLY to c_θ = 0 for every A > 0. Massive ⟺ A ≠ 0 ⟺ nonconstant.
  - `AM2c` (the constant stratum): w ≡ 1 ⟹ θ″ ≡ 0 identically — the kill is VACUOUS; no
    forcing; c_θ free there (this is where the AM-3 lattice lives). At ε_θ = +1 the jet-1
    kill forces c_θ = 0 on every stratum, constant included.
  - The banked f/h momenta are untouched (no declared crease parity; SB1's σ = E0·w(crease)
    is p0's kill rewritten) — no bank contradiction from the verdict.
- **VERDICT: the kill APPLIES; c_θ = 0 is FORCED on every nonconstant cell at ε_θ = −1;
  combined with ε_θ = +1, c_θ = 0 at ANY crease end of ANY nonconstant cell, BOTH signs.
  DISJOINTNESS STRENGTHENED** — the certified massive chain carries NO θ-momentum at all
  (momentum continuity spreads c_θ = 0 chain-wide); at ε_θ = −1 θ is FROZEN at the ℤ₂
  crease value. The shipped "ε = −1 frees θ′" remainder is WITHDRAWN (an off-shell parity
  fact that does not survive the on-shell kill). S2h + TC-4 rows restated everywhere.
  **Survived unchanged:** all cyclic-completion cuts (no crease on a cycle), the ε_θ = +1
  leg, the ℤ₂ crease datum, MB-P's sheet split, all TC-3 transport.
- Note: the verifier's upstream flag (the N=2 crease–glue–crease chain unadjudicated in
  the stability bank) travels upstream; under this verdict such a chain carries no c_θ
  lattice either way (both ends are creases of nonconstant cells ⟹ c_θ = 0).

## AM-3 — the pin-pin lattice (an under-claim in the anti-catalog direction)

- **Found (verifier-derived, verified here exactly, check `AM3`):** on the
  banked-PERMITTED mirrored crease|crease completion, CONSTANT stratum w ≡ 1, ε_θ = −1:
  both crease values pinned in {0, π} ⟹ (c_θ/g_θ)·2ℓ ∈ πℤ ⟹ **c_θ = πg_θm/(2ℓ), m ∈ ℤ**
  — a ℤ-lattice on an ACYCLIC completion at HALF the cyclic lock-class spacing (ratio 1/2
  exact). This contradicted the shipped framings "ℤ-cut on cyclic completions only" and
  "quotient integer content = ℤ₂ only" (it is NOT a winding homomorphism — Hom(D∞,ℤ) = 0
  does not close it). The package under-reported a cut: the opposite of catalog-steering.
- **Changed:** added to TC-2 and the TC-4 map (script, JSON, ledger, EXACT_DERIVATION);
  framing corrected everywhere (EXACT_DERIVATION, DECISION_SURFACE): **CYCLE-WINDING
  lattices** (2π-spaced increments, cyclic completions) vs **PIN-PIN lattices**
  (π-spaced-over-2ℓ, two-pinned acyclic completions, ε_θ = −1, constant stratum,
  MASSLESS-confined per the banked EMPTY facts: SB2 double-crease massive EMPTY both E0
  signs + the family-(ii) quotient exclusion).
- **AM-2 interaction, verified:** the lattice lives where w′ ≡ 0 — the AM-2 nonconstant
  forcing is inapplicable, and θ linear ⟹ θ″ ≡ 0 satisfies the jet-2 kill identically.
  The lattice is legal under the adjudicated census.
- **Honest limits survive:** E0 UNCUT everywhere; ℓ lattice-cut only at fixed c_θ ≠ 0
  (conditional, the S2g shape), never unconditionally. **Post-amendment disjointness,
  precise:** the certified massive family carries NO ℤ content and NO θ-momentum (AM-2);
  every derived ℤ-lattice (cycle-winding or pin-pin) lives on completions disjoint from
  it (cycles, or the massless double-crease stratum).

## AM-4 — the ledger stamp (F-C3 gap)

- **Found:** `COUPLING_LEDGER.tsv` alone carried no IF-ADOPTED banner; standalone, its
  TC2 column read unconditional.
- **Changed:** a banner line now opens the ledger stamping EVERY consequence row
  IF-ADOPTED conditional (θ REGISTERED-NOT-ADOPTED; g_θ free/unpinned; c_θ a θ-sector
  datum, not a banked parameter), consistent with the package's stamp discipline; the
  MB-J row also restated per AM-1/AM-2/AM-3.

## Net effect on the decision surface

Massive side POORER (strengthened disjointness: no θ-momentum at all on the certified
family); massless/quotient side RICHER (ℤ₂ sheets AND a pin-pin ℤ-lattice); E0/ℓ honest
limits intact; six-class menu intact; ceiling intact (nothing adopted, no recommendation).
