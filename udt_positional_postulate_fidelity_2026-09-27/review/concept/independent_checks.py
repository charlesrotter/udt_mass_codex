"""Source-first exact identities; no candidate/production imports or physical selection."""
import json
import platform
import sys
import sympy as s

checks = {}
def zero(name, expression):
    reduced = s.simplify(expression)
    checks[name] = {"pass": reduced == 0, "residual": str(reduced)}

d = s.symbols("d", real=True)
c, f, a, ell = s.symbols("c f a ell", positive=True)
beta = s.symbols("beta", real=True)
K = s.Matrix([[0,1],[1,0]])
D = s.diag(s.exp(-d), s.exp(d))
for i, term in enumerate(D.T*K*D-K):
    zero(f"dual_pairing_{i}", term)
zero("reciprocal_determinant", D.det()-1)
zero("even_trace", s.trace(D)/2-s.cosh(d))
zero("signed_factor_from_even_odd", s.exp(-d)-s.cosh(d)*(1-s.tanh(d)))
zero("pair_ratio_equals_squared_static_clock_ratio", s.exp(-2*d)-s.exp(-d)**2)
zero("signed_reverse_product", s.exp(-d)*s.exp(d)-1)
zero("even_candidate_reverse", 1/s.cosh(d)-1/s.cosh(-d))

# Primary f metric, positive regular static patch. Null dr/dt=c*f.
zero("radial_null", -f*c**2+(c*f)**2/f)
zero("local_proper_null_speed", ((c*f)/s.sqrt(f))/s.sqrt(f)-c)
zero("clock_times_ruler_scale", s.sqrt(f)/s.sqrt(f)-1)

# Complete regular shifted pair. Completion retains full pair plus density.
h = s.Matrix([[-a*a,-a*a*beta],[-a*a*beta,ell*ell-a*a*beta*beta]])
m = a*ell
C = s.diag(1,m)
hn = C.inv().T*h*C.inv()
zero("normalized_determinant", hn.det()+1)
for i, term in enumerate(C.T*hn*C-h):
    zero(f"pullback_recovery_{i}", term)
zero("normalized_spatial_schur", hn[1,1]-hn[0,1]**2/hn[0,0]-1/a**2)
zero("completed_clock_coefficient", hn[0,0]+a*a)

# G269's full transported comparison: screen retained, no physical readout adoption.
r = s.symbols("r", positive=True)
w = s.symbols("w", real=True)
Gamma = (r+1/r+r*w*w)/2
parallel = Gamma-1/r
zero("transported_clock_unit_norm", -Gamma**2+parallel**2+w*w+1)
zero("directional_frequency_contraction", Gamma-parallel-1/r)
zero("mutual_reversal_with_screen_carry", Gamma-((1/r+r+(1/r)*(r*w)**2)/2))
zero("planar_mutual_reduction", Gamma.subs(w,0)-(r+1/r)/2)

out = {"scope":"Exact source identities only; not a fidelity proof, native-admission test, empirical test, or completeness theorem.",
       "implementation":"Fresh source-first script; no imports from historical or parent candidate code.",
       "python":sys.version,"platform":platform.platform(),"sympy":s.__version__,
       "checks":checks,"all_pass":all(x["pass"] for x in checks.values())}
print(json.dumps(out,indent=2))
if not out["all_pass"]:
    raise SystemExit(1)
