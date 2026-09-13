# Frozen finite convergence gate — failure retained

After the symbolic normal-form repair, all30 primary records were captured.
At Q=0.3cos(21/40), eta=0.15, the frozen clock-second-coefficient comparison
failed: final error0.0003058256669758626 exceeds0.8 times the first error plus1e-8,
namely0.00022747466775052932. The first d=0.2 estimate happens to lie unusually
close to the limiting coefficient; the five estimates need not converge
monotonically from that point. No finite d interval was proved by the candidate.
The analytic Taylor/rank question remains subject to independent review.

Do not call the original frozen numerical plan a pass. The current code only
continues after failed convergence guards to preserve the remaining planned
checks; it reports every failed guard and exits1 if any remain. Equations,
parameter samples, tolerances and comparison criteria are unchanged. Initial and
simplifier-repaired code, freeze and failed captures remain. No smaller sample
range or relaxed threshold is substituted as a retrospective confirmation.
