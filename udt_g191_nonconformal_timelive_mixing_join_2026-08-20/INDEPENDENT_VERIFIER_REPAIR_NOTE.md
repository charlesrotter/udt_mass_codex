# Independent verifier repair note

The first independent run stopped only in the numerical `H -> 0` regression probe. Production had
already passed exact symbolic limits. The verifier evaluated `log(1+2 H lambda)` with ordinary
`log` and used `H=1e-8`; the largest finite-H truncation error was about `6.3e-7`, above that probe's
`2e-7` threshold.

Before accepting an independent result, the verifier was repaired to use `log1p` and `H=1e-10` for
that limit probe. No production formula, witness, sample seed, RK4 grid, preregistered `2e-9` main
comparison tolerance, or scientific claim changed. The complete replay then passed 387,680
assertions. This note preserves the failed first attempt and the bounded numerical repair.
