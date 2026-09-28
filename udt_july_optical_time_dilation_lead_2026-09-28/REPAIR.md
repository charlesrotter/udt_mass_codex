# Bounded review repair

The initial candidate is preserved in INITIAL_CANDIDATE.md and the initial
review freeze. This file controls the following precise correction to section 2:

Replace “If f is any decreasing positive profile” by “On an interval where
f is smooth and positive and f'<0 everywhere”. The variable expression
`kappa(x)=-2/f'(x)` is only finite there. A strictly decreasing profile can
have a stationary point: `f=exp(-x^3)` has f'(0)=0. That point does not admit
a finite kappa rewriting of nonzero optical advance as kappa times dphi.

This is a genuine domain qualification requested by the fresh reviewer, not
a change to the constant-kappa result, counterprofile, physical premises or
mathematical controls. Initial author positivity-encoding diagnostics are
separately recorded in AUTHOR_DIAGNOSTIC.md.

A second precision correction applies to candidate section 6's next dependency:
replace “derive or otherwise justify the complete metric/physical observer-and-path
assignment determining the rate” with “derive or otherwise justify physical
geometric and observer/path data sufficient to determine the rate or received-clock
map”. A complete metric is sufficient for evaluation, but full construction or
unique history selection is not a logically necessary prerequisite for every
bounded advance. The review requested this clarification; no new selection
principle is introduced.

Charles then emphasized that a reversal is unlikely. TIME_DEPENDENT_FOLLOWUP.md
records his wording and a bounded additional diagnostic within work-order
methods 3–4. It tests removal of the stationary restriction; it does not repair
the old static model into a native law. The candidate plus this domain repair
and that explicitly conditional follow-up constitute the final review target.
