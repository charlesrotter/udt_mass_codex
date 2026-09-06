# Structure hygiene protocol

`AGENTS.md` is the primary method authority. This file is the artifact-contract adapter. It checks
how work is recorded; it neither supplies physics nor proves that nature follows a result.

## Separate the jobs

| Job | Question |
|---|---|
| Construction hygiene | Are premises, restrictions, dependencies, evidence, and joins visible and reproducible? |
| Mathematical validity | Does the argument or computation satisfy the claimed equations, domain, and quantifier? |
| Physical status | Is the claim adopted, accepted, observed, or canonized under the proper authority? |

Strong hygiene does not establish physics. Weak hygiene can make a sound-looking result unusable.

## Defense in depth

1. Machine checks enforce reliable mechanical properties: import provenance, required tags,
   original-equation residual contracts, constraints, links, schemas, and declared coverage.
2. Artifact headers preserve scope, choices, evidence type, and build-on status.
3. Targeted audits compare current claims with their sources and dependencies.
4. Adversarial review examines the actual proof, computation, or synthesis proportionally.

Machine checks may enforce mathematical certification; this is not aesthetic merit. They may not
reject a valid admitted solution because it lacks a desired shape or interpretation. A Python import
scanner can expose dependencies but cannot decide whether an equation is native UDT.

## Artifact contract

Use `HYGIENE_HEADER_TEMPLATE.md` for new covered result documents. The machine gate is
`python3 -m pytest tests/test_hygiene_header.py`. The exact historical backlog remains sealed in
`hygiene_baseline_correction_2026-07-23/HYGIENE_LEGACY_BACKLOG.tsv`; do not enlarge or rewrite it to
make a new document pass.

Every covered note records:

- date and workflow state;
- question, quantifier, and exact bounded scope;
- whether it observes broadly, targets a legitimate bounded question, or risks answer-fitting;
- premise/choice ledger and excluded inputs;
- method or approximation domain and certification contract;
- evidence type, reviewer status, and independence properties;
- maximum conclusion, limitations, and build-on grade.

Targeted questions are allowed. The defect is hidden answer-fitting, selective outcome disposal, or
a conclusion wider than the declared slice. A valid witness can prove scoped existence and a valid
counterexample can refute a universal claim; neither supplies a completeness theorem.

## Build-on grades

| Grade | Permitted downstream use |
|---|---|
| `DEMO` | Illustration only. |
| `LEAD` | Exploratory candidate; restate uncertainty before chaining. |
| `CONDITIONAL` | May be used only with its premises, domain, and limitations retained. |
| `BANKED-FOR-STRUCTURE` | Hygiene-reviewed structure; still not physics canon. |

A recoverable failed checkpoint may be committed as `DEMO` or `LEAD`. Git preservation does not
promote it. Scientific promotion uses the evidence-appropriate freeze and review rules in
`AGENTS.md`.

## Review and invalidation

Review what changed. Editorial fidelity does not require rerunning unrelated historical science;
changed definitions, equations, premises, dependencies, scope, or numerical outcomes do require
substantive review. Record source/candidate versions, reviewer exposure, checks run, checks omitted,
and each independence axis separately.

When a premise or source version changes, flag every known positive and negative descendant for
review. Preserve unrelated descendants and existing grades. A flag means the explanation may be
stale; it is not an automatic refutation or acceptance.

## Minimal workflow

1. State the authorized question, scope, premises, exclusions, resources, stops, and maximum claim.
2. Explore or derive within that scope; retain failed attempts when informative.
3. Validate the claimed mathematical/numerical object and record the evidence type.
4. Write the header and build-on grade.
5. Run targeted checks, then the relevant regression at closure.
6. Obtain proportionate review before scientific promotion or a reviewed-synthesis label.
7. Give Charles a lay decision packet only when a new premise or major adoption is actually needed.

## Limits

No checklist is a completeness theorem. No reminder is permission enforcement. No checksum proves
truth or independence. No review changes `CANON.md`; Charles alone owns canonization.
