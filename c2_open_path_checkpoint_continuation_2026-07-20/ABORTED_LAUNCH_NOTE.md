# Aborted first official launch

The first eight-worker launch began at 2026-07-20T15:32 local time and wrote only the eight
`RESTART` records preserved in `EXTENDED_TRANSCRIPT.txt`. The controller was manually interrupted
before any worker returned a path result. It produced no raw result file and supplies no scientific
outcome. The interruption was an orchestration/monitoring error, not a solver classification.

The replacement official launch uses the unchanged committed implementation and controls, writes
to `RAW_EXTENDED_PATHS.json`, and preserves its separate transcript as
`OFFICIAL_EXTENDED_TRANSCRIPT.txt`.
