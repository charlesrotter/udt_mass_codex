import sympy as s, json, sys
# Independent original-ray derivation; no proposer implementation imported.
e,v,b,t=s.symbols("e v b t", real=True)
c=s.exp(-2*e)
arrival=(b+c*t)/(c-v)
No=s.exp(-e)*s.sqrt(1-s.exp(4*e)*v*v)
Ne=s.exp(-e)
Z=No*s.diff(arrival,t)/Ne
logder=s.simplify((s.diff(Z,e)/Z).subs(e,0))
assert s.simplify(logder-2*v/(1-v*v))==0
z2=s.simplify(Z**2)
assert s.simplify(z2-(1+s.exp(2*e)*v)/(1-s.exp(2*e)*v))==0
# At fixed physical v0, coordinate speed varies; the observable is constant.
v0=s.symbols("v0",real=True)
assert s.simplify(s.diff(z2.subs(v,s.exp(-2*e)*v0),e))==0
# Reciprocal descriptions add, not cancel, in the quadratic response.
D,Q=s.symbols("D Q",real=True)
assert s.expand(D*Q+(-D)*(-Q))==2*D*Q
print(json.dumps({"kind":"independent exact symbolic original-ray control", "domain":"0<v<1, small e with exp(2e)*v<1, b>0 and regular outward branch", "checks":4, "log_derivative":str(logder), "sympy":s.__version__, "python":sys.version, "limits":"No ensemble or stationarity/locality theorem; no QFT or empirical check"},indent=2))
