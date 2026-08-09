# Startup-surface guard repair preregistration

Date: 2026-08-09  
Branch: `grok`  
Mode: bounded navigation/verifier repair; no scientific adjudication

## Trigger

After the 2026-08-09 lean startup rewrite, the repository was clean and the ordinary test suite
reported `70 passed, 1 xfailed`, but `python3 verify_current_scientific_premises.py` stopped at:

```text
control lacks premise registry: LIVE.md
```

Static inspection also found that the protected-atlas guard required by that verifier was absent
from the marked current blocks of `LIVE.md` and `HANDOFF.md`. `MEMORY.md`, root `README.md`, and
`research/README.md` still route primarily to the August 5 phi/orchestra frontier rather than the
August 9 CMB/free-data arc. These are startup-navigation regressions, not physics results.

## Authorized mutation set

- `LIVE.md`
- `HANDOFF.md`
- `README.md`
- `research/README.md`
- `MEMORY.md`
- `verify_current_scientific_premises.py`
- one pytest integration/catch-proof file under `tests/`
- this package's final verification report

`AGENTS.md`, `INDEX.md`, `CURRENT_RESEARCH_PROGRAM.md`, `INFLIGHT_STATE.md`, `CANON.md`, all
scientific packages, frozen evidence, protected local atlas contents, scripts producing scientific
results, data, and manifests are outside the mutation set.

## Required current-surface invariants

1. `LIVE.md` and `HANDOFF.md` marked current blocks must point to
   `CURRENT_SCIENTIFIC_PREMISES.tsv` and retain the protected-atlas authorization boundary.
2. Current startup controls must route to CMB peak optimization, the free-data inventory, and
   RA1/RA2 with `RA2-PARTIAL-WEAK`; BAO must remain `BANKED + TABLED`.
3. No marked current block may say that `x_max O1` is pending or that Global Cell Assembly is active.
4. `MEMORY.md`, root `README.md`, and `research/README.md` must identify the August 9 active arc while
   preserving phi/orchestra and the older law-order work as lineage/background.
5. The protected atlas remains untracked/local, unread, unmodified, uncited as evidence, and usable
   only after an explicit later dispatch.
6. No scientific label, equation, verdict, premise status, canon entry, or evidence package changes.

## Preregistered catch-proofs

The startup verifier or its pytest integration must reject, in isolated temporary controls:

- removal of the premise-registry pointer from the `LIVE.md` current block;
- removal of the protected-atlas authorization boundary from either current block;
- replacement of the active CMB/free-data route by stale `x_max O1 pending` wording;
- loss of `RA2-PARTIAL-WEAK` or the `BAO ... BANKED + TABLED` status;
- a stale August 5-only `MEMORY.md` top pointer.

The verifier itself must run under `pytest`, so the ordinary baseline cannot pass while the premise
and startup guard is failing.

## Certification contract

- `python3 verify_current_scientific_premises.py` passes.
- All preregistered catch-proofs turn red under their isolated mutations and pass on the repository.
- `python3 -m pytest -q` passes with the known hygiene xfail retained; the pass count may increase by
  the newly integrated startup-guard test.
- `git diff --check` passes.
- Current startup links and named targets exist.
- The final diff is confined to the authorized mutation set.

Maximum conclusion:

```text
STARTUP_SURFACE_GUARDS_RESTORED_AND_REGRESSION_LOCKED__NO_SCIENTIFIC_STATUS_CHANGE
```
