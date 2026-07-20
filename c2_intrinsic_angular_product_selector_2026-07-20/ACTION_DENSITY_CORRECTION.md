# Pre-bank action-density correction

The preregistration requires expansion of the complete local action density
`sqrt(-g) C_abcd C^abcd`. During the premise audit after the first independent replay, the twist
script was found to expand the Weyl-squared scalar alone. The background script already retained the
volume factor.

On the registered oriented local chart, `F>0` and the exact determinant is `-F^2`, so the required
factor is `sqrt(-g)=F`. The symbolic twist derivation and the independent Torch implementation are
therefore corrected to multiply by `F` before extracting the quadratic coefficient. This correction
was committed before rerunning either implementation.

The factor is independent of `r`, `u`, and `epsilon`. It therefore rescales the local twist Euler and
endpoint expressions at each angular point but does not change their zeros, the constant-twist zero
mode, the background Bach equations, or the registered selector classification. The recorded
quadratic formula and all numerical witnesses must nevertheless include it exactly.

No curvature sign, profile, tolerance, boundary condition, physical scale, action premise, carrier,
or outcome class was changed. The earlier unbanked twist replay is superseded and supplies no
scientific result.
