# Final integration check implementation repair

The first final-binding run verified all332 hashes and the261/8/253/71 binding
comparison, then git diff failed with `unable to create threaded lstat: Resource
temporarily unavailable` under the declared512 MiB one-thread check budget.
The repaired copy disables Git preloadIndex and sets index.threads=1 for that
same read-only diff. No expected hash, comparison, scientific assertion or limit
changes. Initial code/freeze/stdout/stderr/receipt remain fixed. This is runtime
compatibility for the prescribed resource bound, not a second scientific repair.
