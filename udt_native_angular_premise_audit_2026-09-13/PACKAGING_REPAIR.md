# NAP1 packaging diagnostic P1

The first preservation check exited1 at its unrelated-untracked-status equality.
It used the absolute __file__ parent to filter Git's relative status names, so
the new package's own untracked files were mistakenly included in that comparison.
The initial script and complete failing stdout/stderr/capture remain preserved.

Smallest repair: normalize the package path relative to the measured current
working directory before filtering names. No workspace file was removed or
changed to make the check pass, no protected payload was read, and no scientific
equation/tolerance changed. The subsequent actual check owns the result.
This is an implementation defect in packaging validation, not a scientific
refutation or a justified claim that original unrelated work changed.
