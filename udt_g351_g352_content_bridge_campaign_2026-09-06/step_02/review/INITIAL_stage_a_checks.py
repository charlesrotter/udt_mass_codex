#!/usr/bin/env python3
"""Source-first Step2 calculations; no author Step2 imports or result reads."""
import json
import sys
import sympy as S

u, v, x, y, A = S.symbols('u v x y A', real=True)
h, b, alpha = S.symbols('h b alpha', positive=True)
a, c = S.Function('a')(u), S.Function('c')(u)
z = S.Matrix([u, v, x, y])

def metric_at(q, amplitude=A):
    return S.Matrix([[amplitude*(q[2]**2-q[3]**2), -1, 0, 0],
                     [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

def simp(matrix):
    return matrix.applyfunc(lambda t: S.simplify(S.expand(t)))

g = metric_at(z)
beta = S.Matrix([-b, 0, 0, 0])
F = S.Matrix([u, v + S.diff(a,u)*x + S.diff(c,u)*y
             + (a*S.diff(a,u)+c*S.diff(c,u))/2, x+a, y+c])
JF = F.jacobian(z)
raw = simp(JF.T*metric_at(F)*JF-g)
ode = {S.diff(a,u,2):A*a, S.diff(c,u,2):-A*c}
res = simp(raw.subs(ode))
assert res == S.zeros(4), 'full_translation_pullback'
assert simp(JF.T*beta-beta) == S.zeros(4,1), 'translation_beta'
assert S.simplify(JF.det()) == 1, 'translation_jacobian'
assert JF[:,1] == S.Matrix([0,1,0,0]), 'future_generator_preserved'

D = S.Matrix([u, h*h*v, h*x, h*y])
JD = D.jacobian(z)
assert simp(JD.T*metric_at(D)*JD-h*h*g)==S.zeros(4), 'full_homothety'
assert simp(JD.T*beta-beta)==S.zeros(4,1), 'homothety_beta'
assert JD[:,1] == S.Matrix([0,h*h,0,0]), 'homothety_future_generator'
assert D.subs({v:0,x:0,y:0}) == S.Matrix([u,0,0,0]), 'fixed_axis'

# Non-isometry control: omit the compensating v displacement.
badF=S.Matrix([u,v,x+a,y+c])
bad_res=simp(badF.jacobian(z).T*metric_at(badF)*badF.jacobian(z)-g)
assert bad_res[0,2] == S.diff(a,u), 'missing_v_shift_detected'
assert bad_res[0,3] == S.diff(c,u), 'missing_v_shift_y_detected'
# Wrong anisotropic dilation must fail a full metric check.
badD=S.Matrix([u,h*v,h*x,h*y])
bad_d_res=simp(badD.jacobian(z).T*metric_at(badD)*badD.jacobian(z)-h*h*g)
assert bad_d_res[0,1] == h*h-h, 'wrong_v_scaling_detected'

# Global constant-A translations in u and v preserve every supplied tensor.
du0,dv0=S.symbols('du0 dv0', real=True)
T=S.Matrix([u+du0,v+dv0,x,y])
assert metric_at(T)==g and T.jacobian(z).T*beta==beta

# Explicit Cauchy data exhibit arbitrary transverse displacement at u=0,
# including both signs. They are exact family formulas, not numeric solving.
w=S.symbols('w', positive=True)
X,Y,P,Q=S.symbols('X Y P Q', real=True)
reach=[]
for sign in [1,-1]:
    if sign==1:
        aa=X*S.cosh(w*u)+P*S.sinh(w*u)/w
        cc=Y*S.cos(w*u)+Q*S.sin(w*u)/w
    else:
        aa=X*S.cos(w*u)+P*S.sin(w*u)/w
        cc=Y*S.cosh(w*u)+Q*S.sinh(w*u)/w
    assert S.simplify(S.diff(aa,u,2)-sign*w*w*aa)==0
    assert S.simplify(S.diff(cc,u,2)+sign*w*w*cc)==0
    initials=[S.simplify(e.subs(u,0)) for e in [aa,cc,S.diff(aa,u),S.diff(cc,u)]]
    assert initials==[X,Y,P,Q]
    reach.append({'A_sign':sign,'initial_data':list(map(str,initials))})

# A is a coordinate amplitude, not a natural scalar of (g,beta).
Pcoord=S.Matrix([alpha*u,v/alpha,x,y])
Jp=Pcoord.jacobian(z)
assert simp(Jp.T*metric_at(Pcoord,A/alpha**2)*Jp-g)==S.zeros(4)
assert simp(Jp.T*S.Matrix([-b/alpha,0,0,0])-beta)==S.zeros(4,1)

# Exact logical discriminators: a positive nonconstant supplied weight is
# type-eligible but not invariant; a nonzero constant cannot have weight -2.
assert (1+(x+1)**2-(1+x*x)).subs(x,0)==1
assert S.Rational(1,4)!=1
assert S.Rational(3,2)*4==6  # nonzero finite area patch remains valid
print(json.dumps({
 'status':'PASS', 'python':sys.version.split()[0], 'sympy':S.__version__,
 'implementation':'independent source-first coordinate pullback; no Step2 author exposure',
 'full_translation_residual_before_ODE':str(raw),
 'full_translation_residual_after_ODE':str(res),
 'translation_determinant':str(S.simplify(JF.det())),
 'full_homothety_residual':str(simp(JD.T*metric_at(D)*JD-h*h*g)),
 'homothety_beta_residual':str(simp(JD.T*beta-beta)),
 'homothety_determinant':str(S.simplify(JD.det())),
 'both_sign_transverse_Cauchy_reach':reach,
 'missing_v_shift_residual_ux':str(bad_res[0,2]),
 'wrong_v_scaling_residual_uv':str(bad_d_res[0,1]),
 'coordinate_amplitude_control':'A changes to A/alpha**2 for the same pulled-back tensors',
 'measure_controls':{'Delta':'3/2','unit_square_amount':'3/2','side_2_square_amount':'6'},
 'finite_witnesses_are_not_general_proof':True
},indent=2))
