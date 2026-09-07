# TM1 one same-premise repair

The initial candidate and author checks are preserved at commit
1e3517f24f5528784237474e6f402b0eb0def08c, argument SHA
589eff684d768831a1390b525e2257ba78f0048b6966c8ae2579097585d1ec44.
The fresh direct review found exactly one required defect R1: unqualified
H1=0 does not imply H(kappa1)=0 for a nonlinear H. Its componentwise
counterexample H(x)=x(x-1) and independent checks are preserved in review/.

Repair: replace 'an operator H' with 'a fixed linear operator H' in §4
(including the grammatical article adjustment). Then
H(kappa1)=kappa H1=0 for all real kappa. This narrows a mathematical
hypothesis to the intended processing class; it adopts no processing rule
or physical assumption and certifies no released data. No other scientific
argument, source, code or original check output is changed. The broader
wording is not treated as having passed. One allowed repair consumed.

Focused re-review must verify the exact diff, linear implication, preserved
counterexample and unchanged source/kinematic scope before downstream use.
