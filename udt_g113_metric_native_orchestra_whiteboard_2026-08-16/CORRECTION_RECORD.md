# G113 correction record

The first execution of `verify_static_spherical_chord.py` returned one failed assertion:
`terminal_depth=false`.

Cause: the pair-block check reused an unconstrained SymPy function `f(r)`. SymPy therefore would
not simplify `log(f(r)^-2)/4` to `-log(f(r))/2`, because positivity had not been declared. The pair
matrix, determinant, center derivatives, and curvature checks all passed in that run.

Repair: the pair-block algebra now uses a separate positive symbol `f_pair`; the direct
four-dimensional curvature reconstruction continues to use the unrestricted differentiable
function `f(r)`. The repaired script passes all checks. The standalone standard-library replay also
passes and does not rely on SymPy simplification.

This was a symbolic-assumption defect in the verifier, not a change to the geometry or conclusion.
