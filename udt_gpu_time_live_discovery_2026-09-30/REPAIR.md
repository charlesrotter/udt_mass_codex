# NGD1 controlling clock-parameter clarification

The independent numerical reviewer identified ambiguous wording in frozen
INITIAL_CANDIDATE.md: “Longitudinal affine null branches have dx/dt=+1 or-1”.
The branches can be affinely parameterized, but areal t generally is not their
affine parameter. The intended fact is that their coordinate slope is dx/dt=±1,
and the coordinate arrival map between the fixed clocks is to=te+d. It is that
arrival map which is affine in te. An affine tangent is proportional to
N^-2(1,±1,0,0), as independently checked; proper-clock conversion uses N.

Controlling wording: “Longitudinal null branches have dx/dt=±1. Their coordinate
arrival map is to=te+d; areal time is generally not an affine ray parameter.”
No equation, initial datum, ray readout, numerical result or evidence grade
changes. Initial candidate and its hash freeze remain preserved. Final central
text uses this precision. This is the one bounded same-premise semantic repair;
review/re-review checks the surviving interpretation, not just file hashes.
