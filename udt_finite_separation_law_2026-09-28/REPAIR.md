# FSL1 repair 1 — endpoint frame orientation

The source-first/direct reviewer identified an omitted convention in
INITIAL_CANDIDATE section1: future unit time columns alone do not force the
endpoint frame map to have determinant+1. Oppositely oriented spatial frames
give determinant-1. Time orientation and spatial orientation are distinct.

Controlling clarification: choose endpoint orthonormal tetrads with consistent
spatial orientation along the supplied path, in addition to future time columns
u_e,u_o. Then Lambda=E_o^-1 P E_e lies in SO^+(1,3), as claimed. Such a choice
is available along the specified regular path; no global spacetime orientability
or preferred physical observer is required. More generally the frequency/direction
identities remain valid for time-orientation-preserving Lorentz maps with either
determinant. This is a frame convention, not a new physical premise.

INITIAL_CANDIDATE and its freeze remain unchanged. Equations(1)-(7), all exact
examples and the conclusion ceiling are unchanged. One source-preserving review
repair round is used; final review owns acceptance of this clarification.
