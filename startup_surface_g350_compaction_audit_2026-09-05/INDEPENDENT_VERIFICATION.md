# Independent verification record

Date: 2026-09-05

## Initial blind verification

Agent: `/root/g350_startup_verifier`
Verdict: `REFUTED`

The passing 60-test draft had two false-pass gaps:

1. removing G350's attribution from the live next gate still passed because `G350` appeared
   elsewhere in the current block;
2. appending `Universal Reciprocity is DERIVED.` still passed while the correct provisional
   statement remained elsewhere.

This refusal was accepted. No result was banked.

## Repair-only blind verification

Agent: `/root/g350_startup_repair_verifier`
Verdict: `VERIFIED-WITH-CAVEATS`

- Focused suite: 62 passed, 1 deselected.
- Baseline temporary startup copy: pass.
- G350 next-gate attribution mutation: failed with the intended bound-attribution diagnostic.
- Additive Universal Reciprocity promotion: failed with the intended contradictory-promotion
  diagnostic.
- Full 333-row premise verifier: pass.
- False passes: none for the two registered repairs.

## Final exact-tree blind verification

Agent: `/root/g350_startup_final_verifier`
Verdict: `VERIFIED-WITH-CAVEATS`

- AST inspection: exactly one `validate_startup_surface` definition and one call; no legacy
  validator definition remains.
- Full premise verifier: exit 0.
- Lightweight active validator: pass.
- Focused suite: 62 passed, 1 deselected.
- `git diff --check`: pass.
- Independent temporary-copy baseline: pass.
- Six mutations independently failed for their intended reason: stale 333-to-320 registry count,
  lost G350 next-gate attribution, additive Universal Reciprocity derivation promotion, protected
  path removal, archive-route removal, and G338--G349 range removal.
- Startup-only review found no changed premise row, canon change, scientific strengthening, or
  protected-work access.

The final verifier's caveat was that it inspected an uncommitted local surface and could not prove
remote freshness under its read-only `.git` permission. The main session had synchronized before
editing; final durability is a commit-and-push gate rather than a scientific caveat.
