# Conceptual/source review — frozen initial candidate

Verdict: **REPAIR_REQUIRED**, with the central synthesis and coverage claims retained.
The required changes below are source-preserving clarification repairs; no new
physical premise, result regrade, or kernel change is needed.

Reviewer/context/model limits are unchanged from `SOURCE_FIRST.md`. This is the
same separate context proceeding from source-first reconstruction to candidate
review. The parent saw source-first findings before freezing; `INITIAL_FREEZE.json`
discloses this. The parent also reported several anticipated repairs while this
direct record was being completed. I have not read the repaired candidate when
saving this initial-candidate verdict; the final review will be separately exposed.

## Candidate and version checks

Reviewed all eight `initial_candidate/` artifacts, including their metadata. The
six requested substantive surfaces were THEORY_BRIEF, AUDIT, archive plan,
SOURCE_CLAIM_MAP, maintained-doc patch, and the parent's SOURCE_READ_LEDGER. The
coverage tables and summary were checked with a separate reviewer implementation.
All twelve hashes in `INITIAL_FREEZE.json` matched at direct-check execution.
Exact candidate/support hashes, actual commands, versions and results are in
`DIRECT_METADATA_CHECKS.json`; the eight principal pins are:

| Artifact | SHA-256 |
|---|---|
| THEORY_BRIEF.md | 06e52051bc838b8a6c1df2cfb9042e3cb2c639d0942a522b361ec49c748656f6 |
| AUDIT.md | 0d23e27bc717ed5516cef074ec707bab286fc3c8a7c2fd93c300f30bee8c3712 |
| ARCHIVE_AND_CROSSCHECK_PLAN.md | 66bb35c311c050082158114526d96d4fd833b0597503dab62098d4c1fba606c4 |
| SOURCE_CLAIM_MAP.tsv | dcea251f0dcf79ec1aceaa67a14300851776627eaf55d4898aab9e431317808c |
| MAINTAINED_DOCS.patch | bdf818c1096afef876da63dfe2f5ce57a77f51cf7a307d89dcd37951d48b121a |
| REGISTRY_COVERAGE.tsv | fc130b2367375b43d7b86221bb8683e32863def35a318eed4f56a6c1f4891c20 |
| FAMILY_ROUTING.tsv | a07c35fe5d08370b48f46546e90bbcca13617a66d3ab1eb88745a8f581bdc9d7 |
| COVERAGE_SUMMARY.json | 0067370c8b359c1939da3fcab94a6d6650919406e8efb6afd154786dccd55efc |

## Defects, survivors and smallest repairs

**C1 — radial direction omitted.** AUDIT A06 calls
`dr/dt=c_E exp(-2 phi)` a radial null rate without restricting the direction.
G265's source has `|dr|/dt=c_E f`; the ingoing branch has negative `dr/dt`.
The local measured positive speed and coordinate-rate distinction survive.
Required repair: use `|dr/dt|=c_E exp(-2 phi)`, or explicitly restrict to an
outgoing branch. This is a sign/scope repair, not a physical objection.

**C2 — retrospective interpretation attributed to the original prompts.**
THEORY_BRIEF's opening says the original prompts “also propose a non-transfer
interpretation of the underlying relation.” Their actual wording proposes
infinite foundational speed while requiring metric causality. G294 and the later
W6 adoption explicitly retype connectedness as nonpropagating membership. The
intended connection and current W6 interpretation survive; their chronology
must remain visible. Required repair: name original infinite-c wording and its
later W6 clarification rather than treating the current nonpropagating type as
already stated in the origin prompt.

**C3 — generic completion versus founded ordered-depth shorthand.**
THEORY_BRIEF's “Given an ordered depth delta, a regular calibrated pair has ...”
compresses the founded ordered block and general W1 completion into one sentence.
G166/G176 and founding sections 3–7 distinguish the founded supplied signed depth,
the generic terminal `Phi`, and the additional exact/null correspondence needed
to match them. All displayed founded-block formulas survive. Required narrowing:
name the founded ordered block and matched unit calibration; describe generic
completion separately. Do not imply that every completed terminal scalar is
automatically the directed depth of every observer comparison.

**C4 — G269's depth should be explicitly null-query typed.** AUDIT A05 correctly
states the screen inequality but uses unqualified `delta` immediately after
discussing endpoint and terminal objects. G269 independently defines its depth by
`delta_null=-log(omega_A/omega_B)` on the supplied affine null path. Its equality
with another pair scalar needs the matched calibration/correspondence already
distinguished by the sources. Required clarification: define that null depth
locally and use it in G269's formula. The theorem, screen condition, and working
physical interpretation survive unchanged.

Two smaller clarity points should be repaired in the same pass. First, “explain
the observed conversion scale called c” can suggest deriving the numerical value
of the observed anchor. Say that the research seeks a positional-clock
interpretation of the observed `c_E`, whose value remains an observational input.
Second, retain the current `WORKING/OPEN` asymptotic global-completion description
of `X_max`, so “open global-completion idea” does not lose its active working
status or asymptotic meaning. Neither clarification changes the central finding.

## Coverage and archive claims

A09 is appropriately bounded; **no coverage overstatement found at its stated
metadata scope**. My implementation independently found:

- 406 current rows, 406 candidate rows, exact ID equality, no duplicate ID, and
  equality of all nine current registry fields on every row.
- All 397 old IDs retained. Exactly G415–G423 added; none removed. The four
  fields actually stored in the old map all match current values.
- All inherited inspection dispositions preserved exactly: 107 controlling-source
  scope inspections, 5 separate-context source inspections, 78 G255 recovery
  traces, and 207 registry/family traces without reopening original arguments.
- Twenty-two old family records unchanged in their inherited fields; one new
  family; every current ID assigned exactly once and every family count correct.
- Forty-eight parent source pins match. The old source ledger has 147 entries;
  its depth categories are counted in the check output, not promoted to new reads.

The candidate expressly declines full historical row-byte identity, blanket
proof review, all-source rereading, and a complete dependency graph. Reading the
two banking scope records supports the additions' editorial classification but
does not reproduce their original derivations, numerical work or review history.
The packet's broad per-row inherited label is conservative: selected sources were
read more deeply during this audit, with that detail in the separate read ledger.

The archive plan explicitly says its four roles are a proposed classification,
not a classification of all 33,248 tracked files. I independently counted 33,248.
Protected, unrelated untracked and fixed-path records remain excluded. The plan
preserves failed/negative work, requires a later bounded inventory/reference/
retrieval exercise and performs no relocation. The 406-row map does not establish
archive readiness. No contrary implication was found.

## Sentence fidelity and fresh-reader questions

The purpose is visible before algebra and remains an intended physical program.
Premises are distinguishable from calibration and conclusions: Dual Reciprocity
does additional work; W1/W5/W6 and DDR/locality remain provisional; a physical
light/source/response connection stays open. The kernel is downstream of complete
metric evaluation and no fitted post-readout correction is introduced. Sign of
the redshift attachment is preserved with `delta_z=-delta_source,observer`.
The GR filter and conditional G301 survivor are not confused with a native field
equation. Supplied initial/query data remain legitimate.

The draft points back to LIVE for the actual open gate and calls the operational
attachment audit a proposal rather than a launch or replacement of DCR1/FE1.
Thus a fresh reader can answer purpose, premise, kernel, physical-gap and next-
action questions after the repairs above. This is a source-exposed fresh-reader
assessment, **not a new startup rehearsal** or approval for live integration.

The proposed maintenance patch applies in read-only `git apply --check`, exit 0.
Its touched surfaces are the three declared files; current paragraphs were read
where needed. It does not edit LIVE, the exact registry, CANON or historical
snapshot bodies. The new evaluator note faithfully distinguishes the old
arbitrary-calibration control from later completed-pair normalization. The stale
closing FE1 recommendation is correctly redirected to LIVE's DCR1 discussion.
An INDEX pointer marked “reviewed draft” becomes accurate only after repairs and
actual final review; the initial candidate is not yet that state.

For the lecture controls, I independently opened the cited Einstein and Carroll
primary texts. Einstein's gravitational spectral section supports the statement
that positional gravitational clock rates/redshift were already within GR;
Carroll explicitly limits local inertial equivalence and discusses redshift.
The Tong URL returned a retrieval error in this review and was not independently
validated here. These are external comparison references, not UDT premises.
I did not recertify every historical, empirical or quantum-gravity assertion in
the supplied lecture. Primary links inspected:
[Einstein](https://www.gutenberg.org/cache/epub/5001/pg5001-images.html),
[Carroll](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll4.html).

## Check history and omissions

`check_direct_metadata.py` imports no parent checker/builder or scientific package.
Its first run had a reviewer coding error in `Counter(mapping)` versus
`Counter(mapping.keys())`; the failure and exact repair are preserved in
`CHECK_IMPLEMENTATION_HISTORY.md`. The corrected run exits 0. This is independent
correspondence implementation, not independent scientific evidence or a complete
test framework. The separate exact Fraction G269 witness remains the limited
computation recorded in the source-first stage.

Not repeated: full premise verification, underlying source production/review
suites, all 406 proofs, raw arrays/observations, source intake authentication,
all-repository dependency closure, empirical GR validation, protected payloads,
live startup rehearsal, archive rehearsal, live edits, scientific promotion or
publication. HEAD remained the pinned baseline and tracked diff was empty at the
metadata check. Parent startup/verifier evidence remains attributed.

The strongest surviving result is a bounded faithful orientation of the intended
program, its existing conditional relations and its open physical joins. The
initial candidate needs the narrow repairs above before a fidelity-reviewed
label. No objection here establishes scientific truth, falsity or canon.
