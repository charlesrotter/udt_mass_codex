# TPP1 supervisor and extraction supplement

Actual context `/root/tpp_runtime`, same inherited model, continuing the scoped
runtime review. This supplements RUNTIME_REVIEW.md; it does not rewrite that
earlier22-invocation resource snapshot. No additional physics or GPU worker was
run by this reviewer. All its new executions were bounded CPU checks.

The initial supervisor had four concrete control omissions: initial artifact
bytes were not required in source bindings; distinct case IDs could share one
resolved run directory; source/spec bindings were only checked at queue entry;
and a nonfinite persisted deadline could bypass the remaining-time comparison.
The parent preserved the original and repaired all four before actual queue
smoke. Per-case launch now rechecks required code, current spec and initial bytes;
run targets are unique and saved deadline finiteness is explicit.

The first reviewer proof accidentally copied an already-repaired edition during
concurrent edits and failed its source-binding setup. That failed checker,
source copy, fixtures and receipt are preserved. The corrected proof targets the
parent's authentic pre-review edition and demonstrates all four omissions with
fake child processes. `supervisor_guards.stdout` then passes21 repaired-control
cases, including those omissions, schema/resource/source problems, diagnostic
and incomplete prior attempts, an expired deadline and output reservation. These
are executions of actual supervisor logic with explicit fake Popen, not GPU or
full-process interruption tests.

`supervisor_artifacts.stdout` supplies the latter evidence separately. The actual
two-case queue pauses after one completion, resumes to finish the second, and
does not launch again when revisited complete. A third case receives forwarded
SIGTERM15 and resumes. All three final g/v arrays match the uninterrupted original
engineering run bit-for-bit; successful endpoints, receipt stdout/stderr hashes,
case/return states and finite manifest-bound wall records were independently
checked. Its four actual worker attempts add5.914532499s, giving26 workers and
301.457598050s total, below600s. This does not certify every crash, a power loss,
arbitrary edited receipt, long-run performance or nonlinear stability.

The parent then explicitly delegated authorship of the production extraction
adapter to this context. `assemble_windows.py` gained optional explicit receipt,
run, source-spec and output paths; default behavior and arrays remain unchanged.
`assemble_campaign.py` joins the bound manifest to actual launch/receipt records,
successful worker endpoints and authenticated checkpoint source signatures. Its
receipt bridge is explicitly a schema adapter, not another execution receipt.
It reserves conservative uncompressed g/v sizes plus overhead before extraction,
authenticates completed derived outputs before reusing them and preserves partial
assemblies for review. Production generation now budgets the analysis tree and
binds both adapters. Extraction is documented as serial while the queue is paused
or complete; no concurrent budget-reservation guarantee is claimed.

Author regression passed: all arrays in three existing Kasner windows are
unchanged using temporary/tmp outputs, actual supervised case windows match the
original uninterrupted engineering trajectory, and repeated extraction reuses
authenticated outputs. The first adapter edition and its passed regression are
preserved before strengthening actual launch.json binding. The final regression
is `campaign_adapter_launch_bound.*`. Neither regression is independent review
of its author's code. The parent separately inspected the refactor/adapter and
ran the final negative checks recorded in `checks/adapter_parent_launch_bound.*`
and `PARENT_ADAPTER_REVIEW.md`. That separate-context contribution is attributed.

No production datasets were emitted or multi-hour job launched. The generator's
78-dataset/234-run recipe is a supplied finite parameter grid; the first-three-case
equation/constraint/output gate remains required before continuing the future
dispatch. This supplement accepts the tested operational preparation with those
limits, not the uncomputed production outcomes.
