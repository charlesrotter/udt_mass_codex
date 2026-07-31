# Stage A1 — audit report

Date: 2026-07-31. Contract: `PREREGISTRATION.md` (frozen before derivation). Script:
`derive_angular_A1.py` — 40 checks, 40 passed (31 SUBSTANTIVE + 9 GUARD), exit 0, deterministic
(stdout byte-identical across independent re-runs, verified), < 1 min CPU, exact SymPy, single
process. Outcome class **OA1-1**. Deliverables: `EXACT_DERIVATION.md`, `ANGULAR_A1_LEDGER.tsv`
(20 O + 15 R + 15 J rows), `angular_A1_results.json`, `DERIVATION_STDOUT.txt`,
`DECISION_SURFACE_UPDATE.md`. *(AMENDED 2026-07-31 post-verifier: 47 checks, 47 passed —
38 SUBSTANTIVE + 9 GUARD; see the amendment-implementation record at the end + `CORRECTION_LAYER.md`.)*

## Falsifier self-audit (the derivation agent's own pass; the blind verifier attacks it below)

- **F-A1 (integer/steering — the hardest self-audit).** No cycle/winding/holonomy content
  appears anywhere as a CLAIM: guard `G4` mechanically scans `EXACT_DERIVATION.md` and
  `ANGULAR_A1_LEDGER.tsv` for the A3-scoped vocabulary and requires every occurrence to sit on a
  scope-exclusion line — 0 violations. `DECISION_SURFACE_UPDATE.md` carries third-party registry
  QUOTES (C-3) and is excluded from the mechanical scan; hand audit: its own statements make no
  A3-scoped claim — the quoted vocabulary occurs only inside registry quotations and their
  premise-scope notes. The TA-3 mode layer is stated strictly at the function-decomposition
  (Category-A) layer; the mode index is explicitly distinguished from field-cycle content.
  Barren-flattery direction: the package does NOT conclude "nothing changes" — it derives two
  NEW census rows, a NEW load-bearing fork, and a semidirect slack structure; equally it does
  NOT inflate them (all posing-layer). Verifier: attack whichever direction the record landed.
- **F-A2 (template import).** No Kaluza-Klein / fiber-adapted parametrization used anywhere;
  `A1q` is the covariant-row-vs-fiber-adapted discriminator certificate (the T1j/anti-ADM
  analog). Harmonic analysis used only as Category-A organizing technique (TA-3 status
  paragraph); no decomposition adopted as physics. The ADM hazard for the t-sector: inherited
  T1 machinery only; no foliation object appears.
- **F-A3 (scope stamps).** Every section carries: A-L1 T² layer (full-S³ typed), A-L2 tri-grade
  ≤ 2 (higher typed), A-L4 line composition, A-L5 θ absent, N=2 wall layer, both lock-reading
  branches + the new spatial-reading fork carried, registered chart + Route C family for the
  family-specific legs (A1b/A1c/A1e/A1e2/A1f/A1p/A1r — stamped: derived ON the registered
  stationary family, angular-live; the general-matrix legs A1g–A1l/A1q/A2b are family-general).
- **F-A4 (assumption smuggle).** θ never appears; no topology/posture/census adoption; R-A
  typed not resolved (TA-4.4); the y-isometry is not silently re-frozen anywhere — O19 is
  varied everywhere it appears, and the y-independent stratum enters ONLY as the C-1 control.
- **F-A5 (bank contradiction).** None found: T1's O16/O17 structure is extended, not
  contradicted (the new chi-branch structure is the exact T1p2/p3/p4 transposition); Route B's
  K₄ survives verbatim (`A1m`); the lock behavior matches CANON C-2026-06-18-1 with the P8
  caveat untouched; A2b's wall causal type matches T1's T3b pattern.
- **F-A6 (symbolic failure).** None: 40/40 zero-residual, exit 0.
- **F-A7 (control failure).** Not fired: C-1 exact (`C1a`/`C1b`), C-2 transitive exact
  (`C2a`/`C2b`).

## Honest notes (for the verifier to probe)

1. The A1e fiber-rigidity derivation pins the clock row by "t untouched + canon form"; a
   compensating φ-redefinition is excluded because ũ = u is forced by the untouched clock row
   with c_E registered — the verifier should probe whether a joint (φ, c_E) redefinition could
   reopen k′ ≠ ±1 (the T1a analog question; the package's answer: c_E is registered data, and
   the A1r absorption is the ONLY derived joint action, which rescales z's period as overlap
   data rather than freeing k′).
2. The two-branch/removal chi-structure (A1h–A1j2) was derived with χ = χ(x); the χ(x,t) layer
   is handled only through A1g2/A1l (shift-row coupling; semidirect law). A2 owes the joint
   (ψ, χ) reduction on the full coupled slack system.
3. C1b/C2b are declaration-grade table comparisons (graded GUARD accordingly, T1-amendment
   precedent).
4. The A3a orthogonality check uses SymPy integer-symbol simplification (n integer, nonzero);
   the n = 0 leg is checked separately.

## Blind adversarial verifier record (required before bank per verifier-before-record)

- Verdict: **PASS-WITH-REQUIRED-AMENDMENTS** (the verifier's own section below is authoritative).
  Hardest targets per contract §5 were: TA-1's metric-opening leg, the residual-symmetry/slack
  derivation (A1e/A1h/A1j2 branch exhaustiveness — the T1 verifier caught exactly this class of
  slip, and this verifier caught it AGAIN: AM-A), and C-1/C-2 independently re-parsed.
  Same-session caveat applies; zero-context agent; chunked.
- Amendments: AM-A, AM-B, AM-C + two clarify-notes — ALL IMPLEMENTED 2026-07-31 (see the
  implementation record at the end and `CORRECTION_LAYER.md`).

## Blind adversarial verifier section — 2026-07-31 (zero-context agent; same-session caveat travels)

Script: `VERIFIER_INDEPENDENT_CHECK.py` (exact SymPy; independent rebuild of the registered
metric from the quadratic form; own TSV parsers; own mechanical sweeps) — ALL its checks pass,
exit 0. Duty 0: two reruns of `derive_angular_A1.py` exit 0, stdout+JSON byte-identical to the
packaged artifacts (stdout sha256 `12becae9…`, JSON sha256 `1dc4d899…`); 40 = 31 SUBSTANTIVE +
9 GUARD recounted honestly (guard list matches); guard wiring mutation-probed on a throwaway
copy (bare "winding" line -> G4 FAIL -> exit 1). Deleted after probe; nothing committed.

**VERDICT: PASS-WITH-REQUIRED-AMENDMENTS.** The angular-live posing, both controls, the fork
framing, the F-sweeps, and the ceiling all hold; but the residual-symmetry/slack census is
provably INCOMPLETE (the exact T1-AM-1 class of slip the package itself named as its hardest
target). Findings, per duty, severity, direction:

1. **AM-A (REQUIRED; Duty 1a; MODERATE; residual group larger than stated).** A missed lawful
   residual map on the FIBER leg: `z -> z + zeta(y)` maps the registered angular-live family TO
   ITSELF with `f~ = f + zeta'` (all other fields relabeled) — verified exactly (`V1b`). Its
   relatives: `zeta(x)` generates the m_z mixed row from the diagonal stratum (`V1c` — A1g covers
   only m_y; O19's m_z fork structure was analogy, not derivation) and `zeta(t)` moves N_z (A1g2
   analog). This refutes the EQUALITY in EXACT_DERIVATION §1.2.6 / ledger stamp 4 / O16 / J10
   ("residual symmetry ... = K4 x T1 x [T^2 translations + mirrors] |x {chi, y-reparam, psi}"),
   and A1e's "residual fiber maps are z -> +/-z + const" is true only within the z-only map class
   (A1e's k'^2 = 1 rigidity itself CONFIRMED, `V1a`; conditional on c_E-as-registered, as the
   honest note says). Load-bearing forward: the missed layer's invariant content on the y-cycle
   is exactly what Stage A3 will census — A3 would miscount the f-DOF if A1 banks without it.
   Amendment owed: derive the zeta-slack layer (cocycle laws, coupling to N_z/m_z/f, semidirect
   structure), rewrite the residual-symmetry statement and O16/O19/J07/J10 rows.
2. **AM-B (REQUIRED; Duty 1b; MINOR-MODERATE; orbit statement too small — conclusions survive).**
   Under the coordinate spatial pin, the JOINT (chi', zeta') slack branch set is a CONIC (not two
   points) and the orbit of m = (g_xy, g_xz) is the full level set of m^T B^{-1} m (B = angular
   block) — verified exactly with a witness taking m=(1,0) to (0,1) lawfully (`V1e`, `V1e2`).
   A1i's "{m, -m}" is only the y-leg slice. IRREDUCIBILITY SURVIVES (B pos-def: m never reaches
   0), the projected reading's full removal s = -B^{-1}m and the invariance of
   gamma_xx = g_xx - m^T B^{-1} m are verified (`V1f`) — so the NEW SPATIAL-READING FORK ITSELF
   is CONFIRMED both ways; restate the orbit/invariant. A1h is exhaustive within its stated
   chi-only class (`V1d`).
3. **AM-C (REQUIRED; Duty 3 C-3; MINOR; sweep under-covers its prereg spec).** The two-keyword
   sweep (`axisym|one-parameter`) misses at least one STANDING entry carrying an angular-frozen
   presentation premise in different words: registry entry #17 (~line 395, premises include
   "spherical-average interface reading", Status STANDING). Also "1-PARAMETER" (~line 835)
   escapes the hyphen-exact regex (likely incidental wording). The 10 flagged entries' quotes
   were spot-checked (3 of 10) against the registry: accurate. Amendment owed: widen the sweep
   vocabulary (spherical / spherical-average / even-sector / 1-parameter) or stamp the keyword
   set as a LAYER with remainder typed.
4. **Note (Duty 1c; no amendment forced).** A1q is computed and genuinely discriminating
   (`V1g`), but carries an un-flagged wrinkle: 1/g^{xx} = gamma_xx IS the projected spatial
   reading — the fork's projected branch pins exactly the fiber-adapted quantity A1q brands
   KK-type. The F-A2 line "this package pins the covariant row" is branch-scoped; a one-line
   clarification (the F-A2 hazard attaches to importing a PARAMETRIZATION, not to a derived
   reading functional) would close the loophole.
5. **Note (Duty 2; no amendment forced).** A2b's "the angular directions add NO wall strata":
   T^2 closedness derives the absence of BOUNDARY/completion strata; the absence of interior
   angular JUNCTION loci is inherited from the banked wall census (walls = x-loci, CANON,
   cited) — an inherited premise folded under a derived label; worth splitting in the record.

**Everything else attacked and CONFIRMED:** A1a/A1b/A1c lock legs and spectator status; A1d;
A1e2/A1f parities; A1g/A1g2 shift-row coupling; A1k additive cocycle; A1l semidirect law
(all re-derived on an independently rebuilt metric, `V1a`–`V1h2`, `V2d`–`V2f`); A2a periodicity
(configuration-space only, alphabet-neutral, no winding smuggle either way — fields are metric
components, hence single-valued; wrap content stays A3's), A2b wall determinant, A2c; TA-3
orthogonality/diagonalization/mode action/mirror negation incl. the norm leg (`V3a`, `V3b`);
extends-verdict spot-checks R3/R8/R12 sound; C-1 and C-2 re-parsed with the verifier's own
parsers — EXACT (`VC1`, `VC1b`, `VC2`); widened F-A1 scan (adds monodromy/homotopy/wrap) clean;
theta absent (`VF4`); y-isometry never silently re-frozen; NO unconditional rider of either
reading fork found (every irreducibility claim is fork-stamped); no contradiction with
T1/T2/Route B/CANON found (C-2026-06-18-1's off-diagonal-FREE clause and clock law quoted
accurately; the A1h/A1i branch is the exact T1 AM-1 transposition; routeC :25-31 supports O20).
The three amendments do not overturn OA1-1: F1/F2 ENLARGE derived structure (census
incompleteness, the package's own named hazard class), they do not invalidate any derived leg.
Banking waits on the amendments + same-verifier closure per contract §5(4).

## Amendment implementation record — 2026-07-31 (derivation agent; verifier's section above untouched)

All three required amendments + both clarify-notes implemented, derivation-grade; nothing
committed; `PREREGISTRATION.md` and `VERIFIER_INDEPENDENT_CHECK.py` untouched. Script grew
40 → **47 checks (38 SUBSTANTIVE + 9 GUARD), 47 passed, exit 0**, re-run ×2 byte-identical
(stdout + JSON regenerated by the script, never hand-edited).

- **AM-A:** ζ-slack layer derived (`A1s` residual ζ(y) with f̃ = f + ζ′ — V1b ported; `A1s2`
  ζ(x) generates m_z — V1c ported, O19's m_z now DERIVED; `A1s3` ζ(t) moves N_z; `A1s4` additive
  cocycle; `A1s5` semidirect under χ/ψ — composition DERIVED: the slack group is the semidirect
  tower ζ-under-χ-under-ψ × y-reparam). Residual-group statement RESTATED in EXACT_DERIVATION
  §1.2.6, ledger stamp 4, O16, J10 (+ O05/O17/J07 riders); A1e scoped to z-only maps;
  A3-relevance = one scope-note sentence in the decision surface (F-A1).
- **AM-B:** V1e/V1e2/V1f ported (`A1i2` orbit = level set of mᵀB⁻¹m, witness (1,0)→(0,1);
  `A1j3` γ_xx invariant + full removal s = −B⁻¹m). Orbit/invariant restated at every rider;
  irreducibility survives as NON-REMOVABILITY; fork framing unchanged.
- **AM-C:** sweep vocabulary widened (axisym / one-param / 1-param / spherical / even-sector);
  **10 → 17 anchors** (old strictly contained in new; entry #17 mechanically asserted flagged);
  seven new driver-note rows in the decision surface; registry NOT edited.
- **NOTE-1:** A1q branch-scope clarified (1/g^xx = γ_xx IS the projected reading; the F-A2
  hazard attaches to imported PARAMETRIZATION, not the derived functional).
- **NOTE-2:** A2b junction leg re-labeled INHERITED-PREMISE (banked wall census: walls = x-loci,
  CANON); T²-closedness leg stays DERIVED. Split in A2b, EXACT_DERIVATION R6, ledger O12/R06.

OA1-1, C-1/C-2 (both controls re-pass unchanged) and both reading forks unaffected. Banking
waits on same-verifier closure per contract §5(4).

## Blind verifier CLOSURE section — 2026-07-31 (same verifier, round 2; same-session caveat travels)

Duty results on the amended package: (1) `derive_angular_A1.py` rerun x2: exit 0, stdout+JSON
byte-identical to packaged artifacts (stdout sha256 `fe1565ba…`, JSON `731f1854…`); 47 = 38S+9G
recounted; A1s–A1s5/A1i2/A1j3 are genuinely substantive — mutation-probe on a throwaway copy
(A1s4 composition target flipped) FAILED the check and exited 1. (2) ζ-composition recomputed
independently: A1s4 (additive) and A1s5 (χ/ψ act on ζ's arguments; ζ acts on no layer) are
CORRECT, and the tower (ζ normal under χ normal under ψ) is right. (3) No surviving {m,−m}
orbit claim anywhere; the invariant mᵀB⁻¹m statement is carried at every rider checked
(A1i, A1j2, O16, O19, J10, stamp 4). (4) AM-C: 17 anchors strictly contain the old 10; entry
#17 now flagged; 2 of the 7 new anchors' quotes spot-checked against the registry — accurate.
(5) No new claim found; both reading forks still "decided by nothing"; PREREGISTRATION, my
round-1 section, and my script's round-1 body untouched; `VERIFIER_INDEPENDENT_CHECK.py`
re-run on the amended package: ALL PASS incl. C-1/C-2 own-parse and the widened F-A1/θ scans.

**VERDICT: FURTHER-AMENDMENTS-REQUIRED — exactly ONE precise, text-level item (AM-D).**
The restated slack-group statement retains one "×" overclaim: "the SEMIDIRECT TOWER (ζ normal
under χ normal under ψ) × [the field-absorbed y-reparametrization]" (EXACT_DERIVATION §1.2.6
item 4; ledger stamp 4; J10; echoed in the A1s5/A1m notes). Verified exactly (closure checks
`VX1`/`VX2` in my script): (i) h acts on ζ's y-argument — order gap ζ(h(y))−ζ(y) ≠ 0 — so the
y-reparam layer is NOT a direct factor (the ζ-layer IS normal under h: conjugate = ζ∘h);
(ii) general h does not even normalize the χ-layer (witness h = e^y: h⁻¹(h(y)+χ) is not a
y-shift), so the product form fails for general h (affine h only). A1s5's own note concedes
the argument action ("and by the y-reparametrization through the same argument action") and
then writes "times" — internally inconsistent. AM-D owed: replace the "×" with the derived
structure — EITHER state the four-layer form with h at the top (h acting on ζ by argument
composition; the χ-layer not normal under general h, consistent with h's J07 overlap-datum
framing) OR restrict the appended factor to the field-fixing residual h′ = 1 (which lives in
the T² translation factor already, itself acting on ζ's argument — say so). No derivation is
missing — both facts are one-line and now sit verified in my script; this is a restatement
edit at the named loci only. Everything else CLOSED. After AM-D lands verbatim-checkably,
this verifier's verdict converts to CLOSED without a further round PROVIDED the edit is
confined to the named loci and my script still passes.

**CLOSURE FINAL — 2026-07-31, same blind verifier: CLOSED.** AM-D confirmed at all named loci
(grep: zero surviving "× [y-reparam]"/"times the field-absorbed" claims; the "group GENERATED
by {ψ, χ, ζ, h} under the derived relations" form present in record, ledger, and script —
mathematically safe and matching my VX1/VX2 facts). `derive_angular_A1.py` re-run: 47/47, exit
0; `VERIFIER_INDEPENDENT_CHECK.py` re-run on the final package: ALL PASS (24 checks), exit 0.
Verdict: PASS (amended); OA1-1 stands as amended. Same-session caveat travels with the bank.

## DRIVER FOUR-CHECK (before bank, 2026-07-31)
1. **Pre-registered?** YES — frozen at 5a97ed1 before the derivation (TA-1..5, F-A1..7, ceiling).
2. **Full-space, or bounded slice justified?** Everything-on within Charles's cleared layer
   bound ("Go, torus-first"): T² stratum (full-S³ typed on the ledger), tri-graded jets ≤ 2
   (remainders typed), time-live-line, both fork readings carried, θ absent, N=2 walls with
   angular germs typed; no DOF frozen; the winding question barred to A3 by contract.
3. **Blind-verified on the load-bearing premise?** YES — round 1 attacked the metric-opening
   and symmetry-fate legs, found the missed ζ-layer (the T1-AM-1 error class transposed —
   caught again by the same discipline), the conic orbit, and the sweep gap; closure round
   verified the amendments, then found and closed AM-D (the direct-factor overclaim) —
   final verdict PASS (amended), CLOSED. Same-session caveat travels.
4. **Every forced premise audited?** YES — the NEW SPATIAL-READING FORK load-bearing,
   carried both ways, decided by nothing (verifier-confirmed both directions); the
   lock-reading fork travels with angular content a spectator; R-A typed; the y-isometry
   unfreezing = the A-L1 CHOSE, stamp travels; A2b's junction-loci leg re-labeled
   INHERITED-PREMISE; 17 registry entries flagged for driver review (list in the decision
   surface, registry unedited).
VERDICT: BANKABLE at the ceiling (OA1-1): the angular-live posing closes; no solve, no
winding census, no response law, no fork/topology decided, no physics. A2 needs its own go.
