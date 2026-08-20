G184_REPAIR_ACCEPTED

- `python3 verify_package.py` passed read-only in the package root and reported `status: PASS`, `helper_live_replayed: true`, `read_only_replays: true`, `default_entrypoint_read_only: true`, with a successful live replay entry for `verify_default_read_only_entrypoint.py`.
- `python3 verify_default_read_only_entrypoint.py` passed directly with no environment variables. The sealed intake tree hash was `7d3eef45c5ab378820bfa8ce8587d18aebaddc7795b2ff139ed1bc22651af7f4` both before and after both required runs, and all 35 scoped files still matched the sealed hashes in `REVIEW_SCOPE.json`.
- Recursion prevention is only the nested skip path required by the preregistration: the helper sets `G184_SKIP_DEFAULT_CHECK=1` before invoking `verify_package.py`, and `verify_package.py` omits the helper only when that flag is present. Default artifact writes are now behind explicit write flags only.
- The original repair-required review remains preserved, and the bounded scientific landing and preregistered counts are unchanged.
