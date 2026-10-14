# FKA1 controlling repair — clock rates and finite intervals

First review/repair round. The initial candidate remains byte-identical to
SCIENCE_FREEZE.json. The fidelity reviewer independently identified this
precision defect during direct review; the coordinator accepts the objection.

INITIAL_CANDIDATE section2 says equal source tick intervals are received with
interval ratio Z=f'(y). This statement is exact for infinitesimal intervals,
or finite intervals on which Z is constant. For a general finite source
interval [y1,y2], the correct statement is

    Delta b=f(y2)-f(y1)=integral from y1 to y2 of Z(u)du,
    Delta b/Delta y=(1/(y2-y1)) integral from y1 to y2 of Z(u)du.

Thus the finite ratio is the interval mean of Z, not an arbitrary pointwise
value. A local Taylor replacement needs an approximation and error control.
The infinitesimal cadence ratio remains 1/Z. No approximation is used in FKA1.

This correction applies to the candidate's compressed clock description.
Its chain-rule, Gram, completion, local-germ and constant-Z controls survive.
The existing central R6 already states the finite integral correctly. This is
a mathematical precision repair, not a changed physical postulate or adoption.
Both designated reviewers must review this correction and the final integrated
wording. No unchanged frozen edition is silently rewritten.
