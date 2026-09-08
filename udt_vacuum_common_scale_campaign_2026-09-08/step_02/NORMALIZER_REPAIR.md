# One same-premise repair: exact trigonometric normalization

Initial code b5d2bf791b4eae5ef83c0f4e85a6181436293e188c98215c1ba313044a51dae6
and all initial output remain unchanged. Initial run exit1,1.108180490s,
maxrss62372KiB, at product_development_original_Ricci. The sole purported
nonzero component was

    -sinh(2*t)*tanh(t)/2 + cosh(2*t)/2 - 1/2.

The normalizer S.simplify left it unevaluated. A finite diagnostic actually
returned zero using BOTH S.simplify(S.expand_trig(e)) and
S.factor(e.rewrite(S.exp)). Directly, sinh(2t)=2sinh(t)cosh(t),
tanh(t)=sinh(t)/cosh(t), cosh(2t)=1+2sinh(t)^2 make it identically
zero for real t, where cosh(t) never vanishes. This is not a tolerated
nonzero residual, failed theorem, or adjusted diagnostic geometry.

Exact diagnostic child (under explicit BLAS/OMP/MKL threads1,
timeout60s, ulimit-v524288KiB and ulimit-t60s) was python3 -B -c:

    import sympy as S; t=S.symbols("t",real=True); e=-S.sinh(2*t)*S.tanh(t)/2+S.cosh(2*t)/2-S.Rational(1,2); print("initial",S.simplify(e)); print("expanded",S.simplify(S.expand_trig(e))); print("exponential",S.factor(e.rewrite(S.exp)))

Actual tool output, exit0:

    initial -sinh(2*t)*tanh(t)/2 + cosh(2*t)/2 - 1/2
    expanded 0
    exponential 0

The repair wrapper check_boundary_repaired.py verifies the frozen original
SHA and replaces exactly ONE residual-normalization expression in memory,
expanding trigonometric identities before simplification. It then executes
the same original tests, with unchanged expected values, rejection paths,
full tensors, metrics and exact-zero requirements. No tolerance or sampling
is introduced; the original code is not overwritten or falsely marked PASS.
Fresh review must inspect this change and replay both failure and repair.
This uses the step's single grouped repair allowance; any further load-bearing
failure must be reported/narrowed, not silently repaired again.
