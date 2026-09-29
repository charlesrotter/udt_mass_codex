# Independent check implementation repair

The first direct checker exited1 inside SymPy trigsimp with PolynomialDivisionFailed when reducing the boost-congruence generator. No failed scientific equality was reported. Initial script and stdout/stderr are preserved in INITIAL_FAILED_* files. The same expressions are now rewritten with exact exponential definitions before simplification, avoiding that hyperbolic reduction path. No metric, parameter, formula, test or conclusion changed.
