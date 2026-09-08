"""Post-exposure exact validation of the single author normalizer repair.

This does not modify or reclassify the preserved failed initial check.
"""
import json
import platform
import sympy as S

t = S.symbols('t',real=True)
q = S.symbols('q',positive=True)  # q=exp(t)>0, a mathematical substitution.
e = -S.sinh(2*t)*S.tanh(t)/2+S.cosh(2*t)/2-S.Rational(1,2)
as_laurent = -(q*q-q**-2)/2*((q-q**-1)/(q+q**-1))/2+(q*q+q**-2)/4-S.Rational(1,2)
expanded = S.simplify(S.expand_trig(e))
independent_laurent = S.factor(as_laurent)
hostile = S.simplify(S.expand_trig(e+1))
assert expanded == 0
assert independent_laurent == 0
assert hostile == 1
print(json.dumps({'kind':'post-exposure exact normalizer validation; no metric/proof change',
    'python':platform.python_version(),'sympy':S.__version__,
    'initial_simplify':str(S.simplify(e)),
    'expanded_residual':str(expanded),'independent_Laurent_residual':str(independent_laurent),
    'injected_nonzero_residual_survives':str(hostile),
    'domain':'real t, q=exp(t)>0; cosh(t)>0 excludes denominator zero'},indent=2))
