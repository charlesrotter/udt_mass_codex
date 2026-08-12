# Frozen-source verification after startup navigation advances

`SOURCE_MANIFEST.tsv` records the exact bytes used when this audit was preregistered and run.
`SOURCE_BASE_COMMIT.txt` fixes those bytes at commit
`7d19b7f9dc535ac1cad0bc4602086d0c7840a473`.

One listed source, root `CURRENT_SCIENTIFIC_PREMISES.md`, is also an intentionally mutable startup
navigation file. After the result was verified, the standing authorization to advance startup
documents changed its worktree bytes. That must not rewrite the historical source manifest.

The verifier therefore checks listed mutable startup sources against their exact Git blob at
`SOURCE_BASE_COMMIT.txt`; immutable scientific sources continue to be checked directly from the
worktree. This preserves both the audit's input provenance and current startup navigation.

