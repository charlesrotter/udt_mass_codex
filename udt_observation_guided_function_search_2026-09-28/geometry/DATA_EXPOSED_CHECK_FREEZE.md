# Data-exposed geometry checks

2026-09-28, after INITIAL_FREEZE. Parent explicitly released full_fits.json,
diagnostics.json, curves.tsv, sensitivity.json and the family definitions in
data/fit_empirical.py. This author has now seen the fitted coefficients, score
summaries and parent BAO statistic summaries. This is exposed analysis, not
confirmation. No coefficient or family is refitted or retuned.

Question: apply the already frozen homogeneous inverse to the F2 and F3 point
estimates, and use the F4 spline as an interpolation-domain contrast. Check
F'>0, curvature/proper/affine behavior of the literal tails, and exhibit smooth
extensions that preserve the fitted interval while differing asymptotically.
No extension is proposed for physical adoption or fitted to new observations.

F2=x exp(a x+b x^2); F3=x exp(a x+b x^2+c x^3). For exponent p(x),
P=1+x p'(x), F'=exp(p)P. Analyze roots of P using exact rational versions of
the saved decimal point estimates, with 20-digit isolating intervals and
80-digit evaluations where needed. These exact calculations refer to the
specified decimal coefficients, not to exact measured quantities. F4 uses
the frozen natural cubic definition and float64 polynomial roots; no formal
interval-certification claim. Do not import its module, which would reset the
child resource limit and carries data-fitting machinery not needed here.

Compute H/h0=e^(x-p)/P, q_dec=-p'-P'/P, and AP=e^x x/P only on P>0. Propagate
the saved marginal shape-parameter covariance by the stated local Jacobian
for F2/F3 inside the data interval; it quantifies conditional fit uncertainty,
not family/systematic/global-tail uncertainty. F4 is a point-estimate domain
diagnostic only; parent already withholds its Gaussian BAO quadratic.

Preserve all input hashes, exact coefficient values, root intervals, sampled
tables and plots. Bounds/resources are unchanged: two threads, 2 GiB, 600 s
per process; no protected reads, data edits, refits, fit family additions or
new physical premises. Parent owns empirical eligibility and reviewer dispatch.
