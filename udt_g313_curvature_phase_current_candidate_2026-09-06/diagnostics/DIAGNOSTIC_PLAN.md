# Pre-freeze symbolic-domain diagnostic

At 18:51:11 UTC the initial checker passed the full curvature/quadratic tensor
and fourth-power guards, then failed `root_covector`. Both original scripts and
the exact failure are preserved beside this file before correction.

Question: is the extracted expression wrong, or is the symbolic domain (real
A including zero) too broad for an extraction dividing by a nonzero contraction?
No omitted physical term or field is authorized. This is exact algebra, not a
floating-point convergence issue. The parameter A is constant, not frozen away
from an authorized spacetime degree of freedom. The scope is this family only;
neither the controls nor the diagnostic cover all vacuum metrics.

Budget: five minutes, CPU only, at most two 60-second diagnostic/check calls.
Inspect the exact expression and difference, split A>0 and A<0, and recompute
the A=0 tensor/root rather than substituting into an expression derived by
division. Stop at implementation/domain defect, bounded incompatibility, or
unresolved symbolic ambiguity. Do not weaken the root or full-tensor criterion.
Any correction is pre-candidate-freeze and must retain both parameter signs and
the flat control. It is not a new physical premise or a post-review repair.
