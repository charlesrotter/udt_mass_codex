# Reviewer path-display diagnostic

At 03:04:26 UTC the reviewer's first final-correspondence wrapper returned a
RuntimeError because its raw pathname-list equality was false. All scientific
hashes, thirteen final frozen targets, candidate-body identity, six tracked paths,
focused startup validation and git diff --check had passed. Both pathname lists
contained 52 entries. The first wrapper was run through a tool heredoc and was
not frozen as a source file; its exception was seen in the tool transcript.

A subsequent exact set comparison found just this representation mismatch:

    baseline display string: '"Mass creates gravity.txt"'
    git ls-files pathname:   'Mass creates gravity.txt'

The baseline used git-status quoting, whereas git ls-files returned the actual
pathname without display quotes. No protected payload bytes were read and no
file was missing or modified. check_final_correspondence.py now uses NUL-delimited
actual git pathnames and decodes the one JSON-compatible quoted baseline entry.
It records the transformation explicitly. This is a reviewer metadata-check
repair; no parent file, mathematical claim or author result changed.
