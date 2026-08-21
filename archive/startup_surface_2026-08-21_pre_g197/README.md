# Pre-G197 startup surface

The exact pre-cleanup startup surface is preserved by git commit `8462797d` on branch `grok`.
That commit contains the then-current versions of:

- `AGENTS.md`;
- `LIVE.md`;
- `HANDOFF.md`;
- `CURRENT_RESEARCH_PROGRAM.md`;
- `CURRENT_SCIENTIFIC_PREMISES.md`;
- `INDEX.md`;
- `MEMORY.md`;
- `verify_current_scientific_premises.py`;
- `tests/test_startup_surface.py`.

G197 found that the surface repeated a long G129--G196 execution chronology in several files,
misstated `B,Q,S=0` where the intended bounded statement was that `B,Q` are metric-fixed and
`S=0`, and described `d_A(Z)` too broadly across turns or caustics. The live files were therefore
compressed and corrected. Fixed historical evidence packages were not rewritten.

To inspect the exact archived text without changing the worktree, use `git show 8462797d:<path>`.
This pointer is the archive; git remains the byte-exact rollback trail.
