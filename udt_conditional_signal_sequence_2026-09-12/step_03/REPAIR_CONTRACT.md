# CSS3 finite numerical chart-coverage repair

First run checks/evolving failed original endpoint residual at epsilon0,s=.4.
The preserved check_evolving_initial.py is the exact initial implementation.
endpoint_diagnostic deliberately disables guards only to inspect the finite
failed root, not to accept it. For epsilon0 s=.4,.8,1.2 the q1 coordinate
saturates its supplied bound8; residuals .00616045,.0708307,.128233 remain.
This is failure of the initial finite solver procedure, not a reception no-go.
The separate-context affine review has already disclosed successful receivers
and some timing/area outcomes before this repair; discovery is not blind.

Smallest repair: enlarge only both numerical sky-chart bounds from8 to32.
This admits additional unknown launch directions on the same positive-x sky
chart; these directions were free boundary unknowns, never physical inputs.
Keep all twelve cases, source proper-clock schedule, receiver, equations,
initial guess, time window, max_nfev30 and every tolerance unchanged. No source
metric, physical parameter, outcome target or acceptance accuracy is fitted.
This supersedes only that bound in CHECK_CONTRACT.md; its initial text remains.
Freeze this repair/code before its outcomes. Rerun every original check, retain
all original failure and diagnostic outputs, and request the fresh reviewer
to assess repair and successful outputs at the same scientific scope.
