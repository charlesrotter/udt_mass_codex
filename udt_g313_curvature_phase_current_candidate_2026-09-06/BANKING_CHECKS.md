# Final packaging diagnostics

No scientific candidate or frozen review byte changed during these checks.

The first current-artifact enumeration used ordinary `rg --files`, which obeys
repository ignores. It listed61 payloads but omitted17 copied `.stdout` files.
Their original archive correspondence and per-archive checks had already passed;
the final tree/staging completeness check exposed the omission BEFORE commit.

Diagnostic: `rg --files --hidden --no-ignore` scoped to this candidate found79
files at that moment (78 payloads plus the initial current manifest).
`git check-ignore` confirmed exactly the17 omitted stdout paths. These are
authorized new-package evidence, not protected/unrelated work. They are staged
explicitly with `git add -f --` on those exact paths; no ignore rule is changed.
The final current manifest is regenerated from all files without ignore filtering.
This note adds one payload. Final expected membership:80 files including the
manifest, whose79 rows exclude only itself. Git-index bytes and membership are
checked against that exact package tree before banking.

The unfiltered `git diff --cached --check` exited2 with one finding:

    replay_2026-09-06/PORTABLE_PATH_ONLY.diff:6: trailing whitespace.
    +<one space>

That file is an immutable generated unified diff. Its blank context line is
encoded by one space, as required by that representation; it matches the
reviewer's frozen bytes. It is deliberately NOT trimmed or silently relabeled a
clean whole-diff pass. The same whitespace check excluding exactly that preserved
raw diff exits0. Other authored/staged files pass; the raw evidence stays intact.

The final archive completeness and whitespace disposition are packaging checks,
not new scientific evidence or another independent review axis. Initial versions
of this not-yet-committed current manifest were working packaging metadata, not
the frozen candidate manifest. FROZEN_CANDIDATE_SHA256SUMS and both immutable
review/portability manifests are unchanged. Backup completeness and pre-reboot
unsaved-state disposition remain UNVERIFIED.
