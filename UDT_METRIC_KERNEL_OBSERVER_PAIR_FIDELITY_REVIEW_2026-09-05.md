# Observer-pair chapter fidelity review

## Scope and authority

- **Review date:** 2026-09-05
- **Review authorization:** Sections 4--5 of
  `UDT_Next_Step_After_Two_Stages.md`; Sections 1--3 supplied the preserved
  scope and repair criteria
- **Scientific source snapshot:**
  `f23199e4a47aaf83acb9ea7d1ad382cd814159c2`
- **Reviewed manuscript:** `UDT_METRIC_KERNEL_DEVELOPMENT.md`
- **Accepted pre-metadata manuscript SHA-256:**
  `3eec21f7b26119d1f0d895f42907c8e544d5a0c0cbb6f1262d77fd88632951f9`
- **Reviewer:** fresh separate GPT-5 Codex context
  `/root/observer_pair_manuscript_fidelity`
- **Verdict:** `ACCEPT`

This is a documentation-fidelity review. It does not improve a scientific
grade, adopt a premise, select a metric history, or canonize any result.
Remote freshness was not independently tested inside the reviewer's sandbox;
the primary session had already completed the mandatory synchronized checkout,
and the reviewer confirmed the named evidence paths were unchanged locally
relative to the fixed scientific snapshot.

## Material reviewed source first

The reviewer read the accepted sources before reading the synthesis:

- G166 `AUDIT_REPORT.md` and `EXACT_DERIVATION.md`;
- G167 `AUDIT_REPORT.md` and `EXACT_DERIVATION.md`;
- G176 `ADOPTION_RECORD.md`, `AUDIT_REPORT.md`, and
  `EXACT_DERIVATION.md`;
- G177 `AUDIT_REPORT.md`, `EXACT_DEPENDENCY_AUDIT.md`, and
  `LOAD_BEARING_DEPENDENCY.tsv`;
- G178 `AUDIT_REPORT.md` and `EXTERNAL_REVIEW_ADJUDICATION.md`;
- G179 `AUDIT_REPORT.md` and `EXACT_DERIVATION.md`;
- G180 `AUDIT_REPORT.md` and `EXACT_DERIVATION.md`;
- the G197 provenance audit, terminology crosswalk, and
  `PROVENANCE_LEDGER.tsv`;
- the active uncompressed evaluator's audit and exact derivation; and
- exact current G166, G167, and G176--G180 registry rows.

It then reviewed the manuscript's authority header, contents, reader
orientation, shared conventions, Section 3 join, completed Section 4, moved
Section 6 prerequisites, and Appendices A--D. Protected and unrelated local
work was excluded.

## Review question

The bounded question was whether the chapter reconstructs the accepted
completed-pair kernel with matching objects, domains, units, and calibration,
without deriving a physical pair assignment, widening the ambient geometry,
suppressing the G176 working premise, or importing a historical control.

The accepted answer is yes. The final reviewed prose preserves:

- supplied ordered depth `delta_AB`, presentation `phi`, raw
  `phi_control`, and completed `Phi` as differently typed objects;
- the complete upstream `B,Q,S,Y,Z` pullback and its Lorentzian regular
  domain;
- G176 as a working owner clarification, not a metric-derived or canonical
  statement;
- angular, screen, mixing, and shift participation before terminal readout;
- arbitrary-coframe scope as evaluator generality, not a widened physical
  metric family;
- time-live differentiation as kinematics, not a dynamical law; and
- documentation gaps, scientific gaps, and deliberately supplied inputs as
  separate categories.

## Defects and source-preserving repairs

The drafting and review passes found and repaired the following bounded
documentation defects before acceptance:

1. The shared observer convention used `g(u,u)=-c_E^2`, while the G348
   transfer source uses a unit timelike observer in `omega=-g(k,u)`. The
   convention now states `g(u,u)=-1` for Sections 6--7 and relates `c_E u`
   explicitly to the dimensionful norm.
2. Section 3.7 still called the completed-pair formulas unsynthesized. It now
   says that W1's conditional formulas are reconstructed in Section 4 while
   W5 and W6 remain outside this edition.
3. Section 3.3 omitted the raw-control/completed-scalar distinction. It now
   separates `delta_AB`, presentation `phi`, raw `phi_control`, completed
   `Phi`, and endpoint potential `V`.
4. The G180 common-scale result was implicit. Section 4 now records the exact
   common-rescaling laws for `m`, `Phi`, and the completed determinant, while
   retaining that they do not select a scale or profile.
5. Appendix B initially made post-pullback quantities sound conditional only
   on a supplied metric and germ. It now separates the raw pullback from the
   consequences that additionally require the G176 working clarification.
6. G166 was cited but its exact matched block was not displayed. Section 4 now
   shows that determinant-one block and limits the numerical equality of
   `delta_AB`, `phi_control`, and `Phi` to the calibrated reduction; the
   further equality with presentation `phi` is limited to the matched primary
   radial realization.
7. Two mechanical drafting slips were corrected: a missing TeX `\\quad` and
   an over-specific `central radial` label.

No repair changed the fixed scientific source snapshot, an evidence grade, a
premise, or a scientific conclusion.

## Checks and limits

- Fresh reviewer exact-grade comparison: **7/7 passed** for G166, G167, and
  G176--G180.
- Primary-session exact-grade comparison: **14/14 passed** for every registry
  item reproduced anywhere in the manuscript.
- Fresh reviewer relative-link check: **38 checked, zero missing**.
- Primary-session Markdown check: **51 total links, zero missing local
  targets**.
- Linked contents: **13/13 anchors resolved**.
- Fresh reviewer independent small algebra: **9/9 identities passed**.
- Primary-session independent exact-arithmetic replay: **1,500/1,500 trials
  passed** across the full block pullback, shifted determinant decomposition,
  completed normalization, and primary angular tape formula.
- `python3 verify_current_scientific_premises.py`: **exit 0**, including the
  335-row premise registry and its reported startup/premise guards.
- `git diff --check`: **passed** on the accepted pre-metadata manuscript.

These are fidelity, consistency, and regression checks. They are not an
independent proof of every historical theorem and not an empirical validation
of UDT. The historical large evidence suites were intentionally not replayed
for this prose-only increment.

## Scope ceiling

The accepted chapter evaluates a completed local reciprocal pair only after a
regular metric/coframe, pair realization, chart/orientation data, and the G176
working clarification are supplied. It does not select events, pair or path
populations, a global history, source or matter content, a light or detector
law, an observational distance, an absolute scale, physical `X_max`, or
canon. Sections 5 and most later development remain explicitly partial or
unsynthesized.
