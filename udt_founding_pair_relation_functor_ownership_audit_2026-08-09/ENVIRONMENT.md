# Reproduction environment

- Repository branch: `grok`
- Derivation base: commit `2a3608ac` after the four preregistered audit increments
- External reviewer: Codex `gpt-5.4`, ephemeral read-only sandbox, high reasoning, web disabled
- Local runtime: Python 3 standard library; no third-party dependency is required by either controller
- Exact controller: `python3 derive_founding_pair_relation_ownership.py` (verification is the default;
  `--write-atlas` is required for any generated-table mutation)
- Independent controller: `python3 verify_founding_pair_relation_independent.py`
- Repository gate: `python3 verify_repository_gates.py`

The external reviewer independently replayed the two finite controllers and the 15-entry source
manifest. Its raw response SHA-256 is recorded in `EXTERNAL_REVIEW.md`.
