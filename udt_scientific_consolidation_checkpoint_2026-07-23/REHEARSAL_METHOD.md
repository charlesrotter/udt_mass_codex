# Startup rehearsal method

The preregistered goal was to test whether a zero-context instance reaches the
current honest frontier.

An ephemeral external Codex invocation was attempted but stopped before
repository disclosure because the separate remote session lacked a
task-specific disclosure grant. No repository payload was transmitted.

The completed rehearsal is therefore a safer deterministic zero-state test:

- `rehearse_startup_zero_state.py` receives no conversation state;
- it reads only `AGENTS.md`, the marked `LIVE.md` and `HANDOFF.md` blocks, and
  the checkpoint's three compact ledgers;
- it reconstructs the required branch instruction, honest claim, premise
  stamps, status excerpt, open seam, regression guards, and authority
  boundary;
- it rejects stale pointers, unbounded startup blocks, status loss, solved-
  branch overclaim, and missing authority limits.

This proves that the recorded startup route mechanically yields the intended
orientation. It is not an independent AI interpretation or scientific review.

## Second-pass reproducibility correction

The first implementation embedded the current commit hash and pre-run
worktree status in two manifested outputs. Those values are operationally
useful but necessarily change across commits and therefore made the
documented rehearsal command dirty a fresh clone.

The rehearsal now checks the stable `AGENTS.md` requirement to work on
`grok`, but it does not embed volatile Git metadata. Actual branch, HEAD,
remote synchronization, and dirt remain mandatory startup facts and are
checked separately by `verify_repository_gates.py`. This separation makes the
manifested zero-context orientation artifact byte-reproducible.
