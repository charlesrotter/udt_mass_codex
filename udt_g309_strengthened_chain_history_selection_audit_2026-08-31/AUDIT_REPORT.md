# G309 audit report

Date: 2026-08-31
Status: `EXTERNAL_GPT54_ACCEPTED_WITH_STATED_CAVEATS__PREREGISTERED_REPLAY_REPAIR_IMPLEMENTED__REPAIR_FOLLOWUP_PENDING`

## Landing

```text
FOUNDED_STRENGTHENED_CHAIN_REMAINS_COMPATIBILITY_ONLY
__ROUND_HOPF_TIME_LIVE_COUNTERFAMILY_SURVIVES
__CONDITIONAL_TRACEFREE_RESIDUAL_CLOSES_POSITIVE_STANDARD_COMPLETION_TO_ONE_SCALE
__HOPF_STRUCTURE_DOES_NOT_OWN_OR_CALIBRATE_THAT_RESIDUAL
```

The recent postulate and Hopf work has not selected a field equation. An exact smooth deformation
of the positive round time-live metric preserves a whole quiet half-history, global hyperbolicity,
compact `S3` slices, both Hopf families, and normalized Hopf time carry, while changing invariant
curvature. The founded/working evaluator and compatibility statements do not reject it.

G301's conditional trace-free Ricci equation does reject the deformation. In this positive round
branch it forces

\[
aa''-a'^2-1=0,
\]

whose complete standard solution is

\[
a(T)=X\cosh((T-T_0)/X).
\]

Accordingly, the conditional branch has no remaining free profile—only one curvature scale, with
time origin removable by isometry. The unresolved question is whether UDT's founding structure
owns that equation. The Hopf results provide downstream consilience, not a derivation of ownership.

See `EXACT_DERIVATION.md` and the three machine-readable evidence files for the bounded proof.

The fresh external reviewer found no scientific defect and independently reproduced the
load-bearing curvature and residual results. It found a medium replay-portability defect because
the production script required unavailable SymPy, plus a low clarification that repository-only
gates were reported rather than sealed-replayed. The preregistered repair replaces the production
replay with a dependency-free exact implementation and makes the package verifier execute it.
Repair-only external follow-up remains pending; the scientific landing is unchanged.
