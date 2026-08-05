# Preregistration refinement 01 — fixed-history versus current navigation

Date: 2026-08-05

Recorded after preregistration commit `b70850fd` and before any current-navigation mutation.

The preregistration required the “existing quarantine gates” to pass. Direct inspection of
`startup_orientation_quarantine_audit_2026-08-05/verify_quarantine.py` shows that it contains
fixed-base assertions requiring the post-cleanup `LIVE.md` and `HANDOFF.md` current blocks and the
then-current `CURRENT_RESEARCH_PROGRAM.md` to remain byte-identical forever. Those assertions are
historically correct for the cleanup commit but are intentionally incompatible with any later
authorized current-navigation update.

This refinement does not alter that historical verifier. The applicable gate is instead:

1. all byte-identical archived pre-cleanup snapshots and fixed cleanup evidence remain unchanged;
2. the startup markers, stale-layer exclusions, retained binding-method text, links, premise
   registry, protected-untracked path set, and other non-fixed-current hygiene checks still pass;
3. a new verifier checks the repaired current blocks and the exact frozen mass-branch sources; and
4. running the old historical verifier may fail only its expected fixed-current identity assertion,
   which will be explicitly reported rather than concealed.

The allowed paths, scientific interpretation, and maximum conclusion in `PREREGISTRATION.md` are
unchanged.
