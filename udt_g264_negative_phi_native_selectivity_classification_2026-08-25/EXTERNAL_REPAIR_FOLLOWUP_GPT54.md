# G264 external repair follow-up

## Disposition

`REJECT_REPAIR`

## Registered-scope finding

The reviewer accepted repairs R1--R3 and found the bounded scientific landing and ownership ceiling
unchanged. It rejected repair closure for one mechanical reason: the sealed repaired subtree omitted
`SOURCE_MANIFEST.tsv`, so `verify_package.py` could not rerun from the intake and failed with
`FileNotFoundError`.

The reviewer independently established inside a writable ephemeral copy that:

- `verify_metric_first.py` passed 250 cases and 1,000 exact assertions;
- `verify_independent.py` passed 12,000 exact and 6,025 numeric assertions;
- `verify_repair_catches.py` caught all 10 registered mutations;
- the metric-first verifier constructs metric derivatives, connection, curvature, scalar curvature,
  Kretschmann scalar, and both registered Einstein channels before comparing with the target forms;
- the legacy independent implementation is consistently regraded as a consistency replay;
- altered copies importing SymPy into the metric-first verifier or re-promoting the consistency replay
  were rejected;
- the negative-`phi` scientific classification and its nonselection ceiling were unchanged.

## Exact remaining defect

The first repair-follow-up builder placed the repaired package under `repaired/` without its frozen
source manifest or a repository-shaped source tree. The package verifier therefore could not execute
its registered frozen-source gate from the seal. This is a replay-packaging defect, not a defect in
the metric-first calculation or the G264 scientific result.

## Source

External Codex reviewer (`gpt-5.4`), sealed intake
`/tmp/udt_g264_repair_followup_hzqk15gj`, completed 2026-08-26.

