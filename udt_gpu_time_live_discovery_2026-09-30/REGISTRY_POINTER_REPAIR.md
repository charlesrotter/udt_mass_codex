# Full406 failure and bounded operational repair

The first final full406 invocation failed after410.028s with exit1:
“control lacks premise registry: HANDOFF.md”. Exact stdout/stderr and resource
receipt remain checks/premise_final.*. It must not be reported as a passing audit.

The rewritten handoff said that exact406 grades were unchanged but omitted the
literal CURRENT_SCIENTIFIC_PREMISES.tsv route required by the existing verifier.
Restore that explicit pointer. Neither the registry nor the scientific argument,
equations, numerical fields, claims, source pins or direct reviews change.

The cheap normal development guard now mirrors this existing operational
requirement for LIVE/HANDOFF. One adversarial omission test removes the pointer
in memory and verifies early rejection. This is a routing regression, not a new
scientific premise or proof. The full premise verifier itself is unchanged.

The prior accepted570-path proposal, handoff, normal guard, maintenance tests and
central review record are preserved in integration_registry_pointer_initial/.
Reviewers preserve their actual prior final reports/attestations in their own
pre_registry_pointer_repair/ directories. A fresh scoped review must bind the
repaired versions; old acceptance does not cover the changed bytes. A new full406
run is required before banking. No repeated numerical solve is needed for this
operational correction, and none is represented as performed.
