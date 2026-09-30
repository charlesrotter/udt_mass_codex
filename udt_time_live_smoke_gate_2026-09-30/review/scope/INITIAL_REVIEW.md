# SMK1 initial scope/workflow review

Verdict on the work-order scope: **VERIFIED-WITH-CAVEATS**. Engineering acceptance
and final integrated-byte attestation remain pending. Reviewer `/root/smk_scope`
is an actual separate context, with inherited model and no cross-model claim.
The reviewer saw the parent's task description, then the work order and code,
and subsequently the first smoke results. This is not a blind outcome review.

The broader objective survives intact. WORK_ORDER.md says smoke testing is an
entry stage and is not completion or replacement of hours-to-days exploration.
It requires a gate for each new solver, dimensional release, or materially
changed workload, then representative sizing and a written six-hour production
tranche/24–48-hour extension dispatch. More runtime inside the original symmetry
slice is explicitly insufficient to fulfill the broader objective. These are
workflow gates, not a proof of mathematical completeness or a new research
premise. They do not automatically authorize or certify an unbuilt 3D solver.

The unchanged NGD1 control is appropriately restricted. Central R12N states
periodic orthogonally transitive two-Killing geometry, areal foliation, Lambda=0
and Ric=0 as conditional comparison assumptions. Its omissions include twist,
general rays, 3D spatial variation, matter/source sectors, selected observers,
physical scale and X_max. The work order, runner module description and initial
SMOKE_RESULT retain this scope. The actual imported evolution file matches its
LAUNCH.json hash. No native Ricci dynamics is adopted by this wrapper review.

The acceptance tests concern preservation, mathematical validity and resource
controls. They do not require a desired physical curve. Prior NGD1 numerical and
original-metric evidence may be inherited only for the unchanged control; the
restart wrapper does not inherit a general 3D certificate. Source hashing is
correspondence evidence, not an independent numerical proof.

Independent CPU regressions all passed in 0.042 seconds, using tiny arrays:
committed state round trip, ignoring a later uncommitted record, changed-signature
rejection, corrupt committed-payload rejection, nonfinite-state rejection,
tiny-output rejection, and source-hash correspondence. Exact command:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 timeout 180s python3 udt_time_live_smoke_gate_2026-09-30/review/scope/check_scope_checkpoint.py > udt_time_live_smoke_gate_2026-09-30/review/scope/cpu_check.stdout 2> udt_time_live_smoke_gate_2026-09-30/review/scope/cpu_check.stderr
```

CPU_CHECK_RESULT.json records versions and inspected source hashes. These tests
reuse checkpoint_io; they are independent execution and independent adversarial
fixture construction, not an independent checkpoint implementation. No GPU was
used and no prior scientific audit was re-proved. Parent startup and scientific
guard/full406 checks remain attributed evidence.

Open observations sent to the parent before engineering acceptance:

1. The initial runner commits a checkpoint before testing constraint >2e-6.
   This could make a rejected state the latest format-valid resume record.
   Smallest repair: check semantic validity before commitment and on resume,
   preserve rejected diagnostics separately, and catch-proof the rejection.
2. The initial result records log-ratio comparison error but not actual clock
   readouts. The work order calls for readable actual clock ratios from saved
   checkpoints. Retain sampled logZ/Z outputs with the te=1,to=4,d=3 marking;
   do not identify sample extrema as continuum extrema.
3. The initial harness waits up to20 seconds for an interrupt checkpoint and
   then gives child.wait another60 seconds. A literal60-second per-child bound
   needs a single deadline. The observed initial children were far below this
   bound; the concern is enforcement, not an observed resource overrun.

No final integration prose or accepted map existed when this initial review was
written. The later review must examine those actual bytes and the disposition of
these observations. Protected payloads, registry grades, CANON and scientific
sources were not changed by this reviewer.
