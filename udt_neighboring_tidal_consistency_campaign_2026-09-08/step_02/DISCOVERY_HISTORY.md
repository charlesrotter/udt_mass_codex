# NT2 discovery and implementation history

Question frozen after NT1's final reviewed result; NT2 is the second and last
substantive campaign step. Author derived the Lorentz normal-form argument and
profile-metric realization before reading any NT2 reviewer source-first findings.
Only reviewer startup/readiness and seal-location messages were received.

The first symbol check at00:16:36UTC exited1 after its first five guards passed.
It mistakenly expected the two coordinate columns' Euclidean Gram matrix to be
diag(4,3); direct counting gives diag(3,3). The independent rank-two/null-kernel
checks had already passed. Original check_symbol_initial.py and symbol_initial.*
are retained. Corrected check_symbol.py passes six guards. This coordinate Gram
test checks injectivity only; it is not physical energy or invariant positivity.

The first actual-development check at00:22:30UTC exited1 with a TypeError because
the SymPy column-matrix callback accepted one argument rather than two. Its first
ten guards (full Ricci/curvature/jet/frame/K projection) had passed; its buffered
final stdout was empty. The exact script check_development_initial.py and streams
development_initial.* survive. Only the callback signature changed to (i,col).
The corrected baseline passes all13 guards, including intrinsic Hamiltonian and
momentum constraints over the full symbolic neighborhood. No equation, candidate
claim, profile freedom, domain, or resource cap changed in either correction.

These are exposed PRE-FREEZE implementation errors, not reviewer-discovered
mathematical repairs. No post-review repair cycle has yet been used. Both source
snapshots are preserved and all actual failed runs remain in the evidence set.
Seven deliberately defective mutants all exit1 at claim-relevant guards:
omitted Bianchi, reversed aligned null sign, missing mixed curvature, nonharmonic
profile, reversed K sign, omitted H_u and doubled normalized first curvature jet.
They are selected diagnostic mutations, not proof of exhaustive fault coverage.
The nonharmonic mutant has a Ricci defect proportional to u, vanishing at the
central event but not on a neighborhood. K-sign mutation is caught by its full
normal projection, not by sign-insensitive squared constraints.

The author symbol calculation reuses NT1's exact matrix conditionally; the
development calculation reuses geometry() from an unchanged accepted-method
utility. Shared code is not independent verification. The separate reviewer
must assess both analytic proof and actual-development join in phase B. Existing
NT1 repair/false-pass evidence and review limits remain inherited.
