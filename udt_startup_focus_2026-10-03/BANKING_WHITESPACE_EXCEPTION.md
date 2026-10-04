# Raw-capture whitespace exception at staging

The first exact-stage command staged the manifest scope, then its default
`git diff --cached --check` rejected a new blank line at EOF in the preserved
failed audit's checks/final_premises_windowed.stderr, line35. This is captured
raw output, not editable prose; its actual receipt hash remains authoritative.
The earlier simple parent whitespace scan tested trailing spaces only and did
not detect this EOF condition. No scientific or reviewed source bytes changed.

Preserve that raw stderr byte-for-byte. Check every other staged path with
ordinary git diff --check, excluding only this exact raw file. For the closure
helper's additional whole-stage check, temporarily disable only blank-at-eof
using command-local Git configuration; all other whitespace checks remain.
This is a documented capture-format exception, not a weakened scientific test.
The initial manifest is preserved; the final manifest adds only this note and
its predecessor. Required audits/reviews remain applicable to unchanged bytes.
The first stage command failed; only the subsequent exact-stage verification
with these checks may be called passed. No repository Git configuration changes.
