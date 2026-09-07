# Finite evidence-packaging diagnostic

RC1 initial git add returned1 because .gitignore line38 ignores *.stdout.
The orchestration incorrectly continued to commit33768f3816b479bdae6ed2df92859e418d746e7e
with21 files, omitting five manifest-listed stdout payloads. It was NOT a
complete evidence commit and is not relabeled as one. All saved bytes remain
on disk; no scientific calculation or source was lost or changed.

Bounded remedy: inspect exact ignore matches (all five match .gitignore:38),
force-add ONLY those five authorized RC1 raw outputs, commit their preserved
bytes plus this note, and authenticate the original candidate manifest plus
tracked membership. No ignore/config change, numerical rerun, science repair,
resource increase or protected work is involved. Stop on any unexpected path
or hash discrepancy. The resulting second commit is the complete candidate
pin for review; the original argument and manifest hashes remain unchanged.
