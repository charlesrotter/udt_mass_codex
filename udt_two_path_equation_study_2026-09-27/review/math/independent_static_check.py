#!/usr/bin/env python3
"""Source-first exact computation, no parent module/artifact imports.

CHOSEN/UNADOPTED action q(R)=R+alpha R**2 and DDR response identification.
FREE alpha has dimension L**2. All integration constants are mathematical data.
No fit, physical source, boundary condition, or additional independent field.
"""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
x0, r, th, ph = s.symbols("x0 r theta phi", real=True)
coords = [x0, r, th, ph]
alpha = s.symbols("alpha", real=True)
f = s.Function("f")(r)
g = s.diag(-f, 1/f, r**2, r**2*s.sin(th)**2)
gi = g.inv()
checks = {}
def zero(name, expr):
    value = s.simplify(s.trigsimp(expr))
    checks[name] = str(value)
    if value != 0:
        raise AssertionError((name, value))

# Full four-dimensional connection, including theta/phi derivatives.
C = [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b]) +
    s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
    for c in range(4)] for b in range(4)] for a in range(4)]
Ric = s.Matrix(4,4,lambda a,b:s.simplify(sum(
    s.diff(C[c][a][b],coords[c])-s.diff(C[c][a][c],coords[b]) +
    sum(C[c][c][d]*C[d][a][b]-C[c][b][d]*C[d][a][c] for d in range(4))
    for c in range(4))))
R = s.simplify(s.trace(gi*Ric))
R_formula = -s.diff(f,r,2)-4*s.diff(f,r)/r+2*(1-f)/r**2
zero("scalar_from_connection", R-R_formula)
for i in range(4):
    for j in range(4):
        if i != j:
            zero(f"Ric_offdiag_{i}{j}",Ric[i,j])
A = -s.diff(f,r,2)/2-s.diff(f,r)/r
B = (1-f-r*s.diff(f,r))/r**2
for i,z in enumerate([A,A,B,B]):
    zero(f"Ric_mixed_{i}",(gi*Ric)[i,i]-z)

H = s.Matrix(4,4,lambda a,b:s.simplify(s.diff(R,coords[a],coords[b])-
    sum(C[c][a][b]*s.diff(R,coords[c]) for c in range(4))))
box = s.simplify(s.trace(gi*H))
box_formula = f*s.diff(R,r,2)+(s.diff(f,r)+2*f/r)*s.diff(R,r)
zero("box_full_hessian",box-box_formula)
for i,z in enumerate([s.diff(f,r)*s.diff(R,r)/2,
        f*s.diff(R,r,2)+s.diff(f,r)*s.diff(R,r)/2,
        f*s.diff(R,r)/r, f*s.diff(R,r)/r]):
    zero(f"H_mixed_{i}",(gi*H)[i,i]-z)
F = 1+2*alpha*R
q = R+alpha*R**2
E = s.simplify(F*Ric-q*g/2+2*alpha*(g*box-H))
Em = s.simplify(gi*E)
traceE = s.simplify(s.trace(Em))
zero("trace_response",traceE-(-R+6*alpha*box))
zero("temporal_minus_radial",Em[0,0]-Em[1,1]-2*alpha*f*s.diff(R,r,2))
zero("temporal_minus_angular",Em[0,0]-Em[2,2] -
     (F*(A-B)-2*alpha*(s.diff(f,r)/2-f/r)*s.diff(R,r)))
for b in range(4):
    div = sum(s.diff(Em[a,b],coords[a])+sum(
        C[a][a][c]*Em[c,b]-C[c][a][b]*Em[a,c] for c in range(4)) for a in range(4))
    zero(f"offshell_divergence_{b}",div)
for i in range(4):
    zero(f"alpha_zero_{i}",Em[i,i].subs(alpha,0)-(gi*Ric)[i,i]+R/2)

# Necessity: alpha != 0 and f>0 give R''=0; solve R=a*r+b directly.
a,b,c,d = s.symbols("a b c d",real=True)
f_affine = 1-b*r**2/12-a*r**3/20+c/r+d/r**2
def put(expr,profile):
    return s.simplify(expr.subs(f,profile).doit())
zero("affine_curvature_general_integral",put(R,f_affine)-(a*r+b))
trace_affine = s.expand(put(traceE,f_affine))
zero("trace_affine_formula",trace_affine-(-a*r-b+
    6*alpha*a*(2/r-b*r/3-a*r**2/4+c/r**2)))
# r**2 coefficient in constant trace is -3*alpha*a**2/2; no division by F.
lambda0 = s.symbols("lambda0",real=True)
trace_poly = s.Poly(s.expand(r**2*(trace_affine-4*lambda0)),r)
zero("trace_polynomial_leading",trace_poly.coeff_monomial(r**4)+3*alpha*a**2/2)

# All components, generic Einstein branch including F=0 overlap.
f_e = 1+c/r-b*r**2/12
for i in range(4):
    zero(f"Einstein_complete_E_{i}",put(Em[i,i],f_e)+b/4)
# All components, F=0 branch, retaining the extra 1/r**2 constant.
f_d = 1+c/r+d/r**2+r**2/(24*alpha)
zero("degenerate_R",put(R,f_d)+1/(2*alpha))
for i in range(4):
    zero(f"degenerate_complete_E_{i}",put(Em[i,i],f_d)-1/(8*alpha))
for i,z in enumerate([-d/r**4,-d/r**4,d/r**4,d/r**4]):
    zero(f"constant_R_tracefree_Ricci_{i}",
         put((gi*Ric)[i,i]-R/4,f_affine.subs(a,0))-z)

# Concrete refuters for guards: angular omission and zero-response substitution.
# On r>0 alpha=1,c=0,d=1, f_d>0 everywhere; TF(E)=0 yet S != 0 and E != 0.
mutations = {
    "discard_degenerate_nonEinstein": str(put((gi*Ric)[2,2]-R/4,f_d).subs({alpha:1,c:0,d:1,r:1})),
    "replace_DDR_by_zero_response": str(put(Em[0,0],f_e).subs({b:12,c:0,r:s.Rational(1,2)})),
    "omit_angular_equation": str(put(Em[0,0]-Em[2,2],1+d/r**2).subs({d:1,r:1})),
}
if any(s.sympify(value)==0 for value in mutations.values()):
    raise AssertionError(("nonvacuity mutations",mutations))

result = {
    "status":"PASS", "evidence_type":"exact symbolic independently implemented scoped checks",
    "python":platform.python_version(),"sympy":s.__version__,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks":checks,"check_count":len(checks),"refuting_controls":mutations,
    "derived_scalar":str(R),"trace_affine":str(trace_affine),
    "trace_polynomial_coefficients":list(map(str,trace_poly.all_coeffs())),
    "scope":"smooth full four-dimensional reciprocal static spherical positive-f interval; chosen unadopted response; no global dynamics claim",
}
(HERE/"CHECK_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":result["status"],"exact_checks":len(checks),"refuting_controls":mutations,
                  "python":result["python"],"sympy":result["sympy"]},indent=2))
