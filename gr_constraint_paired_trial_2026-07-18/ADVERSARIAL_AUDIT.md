# Adversarial audit — GR-constraint paired trial

Date: 2026-07-18
Mode: two fresh read-only reviewers; no delegated edits

## Reviewer 1 — selector and algebra challenge

Reviewer: `/root/gr_constraint_selector_challenge`
Verdict: `VERIFIED-WITH-SCOPE-CAVEAT`

The reviewer independently reproduced:

- generic KKT equations `grad S_0 + lambda grad C=0`, `C=0`;
- aligned root `(1,2,0)`;
- reactive metric-only root `(0,0)` with `C=-1` and constrained root `(1/2,1/2,-1)`;
- finite-penalty residual `-1/(alpha+1)` and reaction limit `-1`;
- the metric-plus-scalar Noether identity, up to the declared convention;
- `w_lambda=-4-w_C` for a homogeneous constraint;
- the added `lambda delta q` boundary term.

The strongest A-selection argument read “the metric is the theory” as a literal ban on every varied
nonmetric field. It failed because accepted status S10 explicitly keeps multiplier, hard-constraint,
and readout routes live. Such a ban would be a new off-shell closure rule.

The strongest B-selection argument read derived Reciprocity as requiring an exact multiplier
reaction. It failed because no native `C[g]` exists and no theorem selects multiplier enforcement
over hard restriction, unrestricted-then-restrict, or readout implementations.

The reviewer required the top outcome to mean bounded non-exclusion, not complete UDT universes.
The report now makes that limitation prominent and adds an explicit category-A four-dimensional
bulk existence witness. There is still no branch selection and no native constraint.

## Reviewer 2 — GR bundle, boundary, and ontology challenge

Reviewer: `/root/gr_bundle_boundary_audit`
Verdict: `VERIFIED-WITH-BOUNDARY-CAVEAT`

The reviewer found no hidden promotion of locality, EH/Lovelock, derivative order, spatial infinity,
GHY/ADM, source, carrier, or density normalization. The KKT, penalty, and boundary conclusions were
scoped correctly.

The reviewer caught that a bulk Noether identity does not establish the full active diffeomorphism
group on a finite mirrored cell. Boundary- and mirror-preserving maps, embeddings, allowed data,
corners, and generators remain unresolved. The report and ledger now state
`RETAIN_TRIAL_CONDITIONAL` only for bulk covariance and mark the full finite-cell group
`UNRESOLVED_TRIAL`.

The reviewer also sharpened the auxiliary interpretation: nonpropagating is not law-neutral. A
multiplier changes the metric equation whenever the normal reaction is nonzero. Branch B remains
only a trial until `C[g]` and its authority are derived and no independent ontology enters.

## Reconciliation

Both reviewers agree that:

1. covariance alone does not choose the field census;
2. the current post-July foundation selects neither A nor B;
3. `BOTH_CONDITIONALLY_ADMISSIBLE` is defensible only as selector-level compatibility and
   non-exclusion;
4. the illustrative anchors and 4D bulk witness are not complete UDT universes;
5. finite-cell boundary completion remains `OPEN`;
6. no action, source, carrier, mass, or density normalization was promoted.

Both reviewers left the repository unchanged. Their catches were incorporated by the primary before
freezing the package; no reviewer wrote or modified an artifact.
