# ACI1 bounded normalizer repair follow-up

The first repaired capture is also preserved. Rewriting every assertion into
exponentials exposed a second exact-normalization failure at cosh.distance_redshift:

    [exp(2HT)+1-sqrt(exp(4HT)+2exp(2HT)+1)]
      /sqrt(exp(4HT)+2exp(2HT)+1).

The radicand is (exp(2HT)+1)^2, whose square root is exp(2HT)+1 because H,T
are positive reals. The exact value is zero. A finite diagnostic evaluated
factor(expression,deep=True), simplify of the original cosine/arctangent form,
and trigsimp of that original form; each returned exact zero. No tolerance,
branch-forcing option or numerical approximation was used.

The final wrapper preserves ordinary simplify for assertions it already solves;
only unresolved expressions use the hyperbolic expansion/exponential rewrite,
followed by deep exact factorization. The recorded contractions use the same
normal form. This stays within the one bounded same-premise repair round; both
earlier attempts and the frozen original program remain unchanged. There is no
formula, metric, theorem, expected value or scientific-scope change. All failed
and final receipts remain separate. A further unresolved failure would be
reported rather than broadening this repair indefinitely.
