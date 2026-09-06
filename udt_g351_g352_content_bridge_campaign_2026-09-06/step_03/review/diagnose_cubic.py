import json, sympy as s
x,y=s.symbols('x y',real=True)
S=4*(x*x+y*y)
actual=s.factor(sum((s.diff(S,z)/(4*S))**2 for z in (x,y)))
expected=1/(4*(x*x+y*y))
print(json.dumps(dict(actual=str(actual),expected=str(expected),structural_equal=actual==expected,
                     exact_difference=str(s.cancel(actual-expected)),wrong_coefficient_difference=str(s.cancel(actual-2*expected))),indent=2))
assert s.cancel(actual-expected)==0
assert s.cancel(actual-2*expected)!=0
