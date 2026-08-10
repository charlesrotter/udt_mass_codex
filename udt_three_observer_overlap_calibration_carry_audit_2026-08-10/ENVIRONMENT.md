# Reproduction environment

- Branch: `grok`
- Frozen audit base: `ea243c7c`
- Source-freeze commit: `ecf93442`
- Runtime: Python 3; SymPy for the production controller; Python standard library/Fraction for the
  independent algebra verifier
- Production replay: `python3 derive_three_observer_overlap.py`
- Independent replay: `python3 verify_three_observer_overlap_independent.py`
- Repository gate: `python3 verify_repository_gates.py`
- External reviewer: Codex `gpt-5.4`, ephemeral read-only sandbox, high reasoning, web disabled

The accepted external review ran from an isolated intake containing only this package and the 17
manifest-listed source snapshots. Both controllers support `--source-snapshot-root` for that
bounded replay.
