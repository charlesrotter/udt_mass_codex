# Source-preserving exposed-review clarifications

INITIAL_CANDIDATE.md remains unchanged. The fidelity reviewer requested explicit
map direction: J takes sky-angle differentials to physical source rest-screen
displacements. The source-size-to-sky map is J^{-1} only where det J!=0.
At a caustic the phase map remains regular but that inverse does not exist.

The displayed M|delta theta|^2/2 remainder concerns x_e(theta_o), the
size-from-sky map, when its Hessian is bounded on the stated patch. A finite
angle error inferred from source size requires an independently controlled
inverse-map remainder. No bound M or finite-source accuracy is supplied here.

D_A denotes the angular-area distance sqrt(|det J|), as in the current ACP
readout. In an anisotropic image the two directional length factors are distinct;
D_A is not asserted to convert every source length into its observed angle.
These clarifications preserve every equation, assumption and derived scope.

The exposed decision brief initially said “nonradial massive ray.” The fidelity
review caught this misleading phrase: the ray is null; m>0 is the supplied
geometric parameter. DECISION_BRIEF now says “nonradial ray with m>0.” The
pre-correction text is retained under initial_text/DECISION_BRIEF.md. No equation
or physical mass law changed. Final review must use the corrected brief.

Before integration freeze the fidelity reviewer also caught a units phrase in
central R16: H has inverse-length units, so the corrected text says the result
does not fix1/H in light-years. No scale value or equation changed. The
maintenance suite is repeated on the corrected integration; its first receipt
remains under checks/before_units/.
