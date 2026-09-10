#!/usr/bin/env python3
"""ER1 author exact identities/controls; stdout only, no independent-review claim."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

if not __debug__:
    raise RuntimeError("Scientific evidence requires ordinary Python, not -O")

checks = []


def zero(v):
    values = list(v) if isinstance(v, s.MatrixBase) else [v]
    return all(s.simplify(x) == 0 for x in values)


def check(name, condition, detail):
    if condition is not True and condition is not s.true:
        raise AssertionError(name)
    checks.append({"name": name, "pass": True, "detail": detail})


t, x, y, z = s.symbols('t x y z', real=True)
coords = (t, x, y, z)
N = s.Function('N')(*coords)
bet = s.Matrix([s.Function('beta'+str(i))(*coords) for i in range(3)])
theta = s.Matrix([1, *bet])
u = s.Matrix([1/N, 0, 0, 0])
ul = -N*theta
P = s.eye(4)+ul*u.T
X = s.eye(4)[:, 1:]-s.Matrix([1, 0, 0, 0])*bet.T
dul = s.Matrix(4, 4, lambda i, j: s.diff(ul[j], coords[i])-s.diff(ul[i], coords[j]))
w4 = (P*dul*P.T/2).applyfunc(s.simplify)
F = s.Matrix(3, 3, lambda i, j: s.diff(bet[j], coords[i+1])-s.diff(bet[i], coords[j+1])
             -bet[i]*s.diff(bet[j], t)+bet[j]*s.diff(bet[i], t))
check('rest_annihilation', zero(theta.T*X), 'theta(X_i)=0 for arbitrary smooth beta')
check('projector_idempotent', zero(P*P-P), 'covector projector with U_flat(U)=-1')
check('projected_exterior_equals_general_F', zero(w4[1:, 1:]+N*F/2), 'arbitrary smooth lapse/shift, all temporal derivatives retained')
check('rest_pullback_equals_spatial_block', zero(X.T*w4*X-w4[1:, 1:]), 'time row/column of projected w vanish')
check('temporal_orthogonality', zero(w4*u), 'vorticity annihilates observer U')
check('lapse_derivatives_cancel_after_projection', not any(w4.has(s.diff(N, c)) for c in coords), 'does not remove lapse values or affect other kinematics')

q11,q12,q13,q22,q23,q33 = s.symbols('q11 q12 q13 q22 q23 q33')
Q = s.Matrix([[q11,q12,q13],[q12,q22,q23],[q13,q23,q33]])
# Q is the symbolic inverse of the supplied rest form; no inverse is fitted.
gi = s.zeros(4)
gi[0,0] = -1/N**2+(bet.T*Q*bet)[0]
gi[0,1:] = -bet.T*Q
gi[1:,0] = -Q*bet
gi[1:,1:] = Q
W_full = s.trace(gi*w4*gi*w4.T)
W_rest = N**2*s.trace(Q*F*Q*F.T)/4
check('full_metric_contraction_equals_rest_formula', zero(W_full-W_rest), 'symbolic inverse rest form; no flat metric substitution')

r,b,q,eps = s.symbols('r b q epsilon', real=True)
nw = 1+t+y
a = 1+t+x*x
G0 = s.Matrix([[2,1,1],[1,3,1],[1,1,2]])
gam = a*a*G0
bw = s.Matrix([r,b*x+q*t,0])
thw = s.Matrix([1,*bw])
gw = -nw*nw*(thw*thw.T)
gw[1:,1:] += gam
uw = s.Matrix([1/nw,0,0,0])
uwl = gw*uw
Pw = s.eye(4)+uwl*uw.T
duw = s.Matrix(4,4,lambda i,j:s.diff(uwl[j],coords[i])-s.diff(uwl[i],coords[j]))
ww = (Pw*duw*Pw.T/2).applyfunc(s.simplify)
giw = s.zeros(4)
Qi = G0.inv()/a**2
giw[0,0] = -1/nw**2+(bw.T*Qi*bw)[0]
giw[0,1:] = -bw.T*Qi
giw[1:,0] = -Qi*bw
giw[1:,1:] = Qi
check('G0_positive_principal_minors', [G0[:i,:i].det() for i in (1,2,3)] == [2,5,7], 'Sylvester criterion; N>1/2,a>3/4 on stated patch')
check('witness_inverse_metric', zero(gw*giw-s.eye(4)), 'full mixed four-dimensional metric inverse')
check('witness_unit_observer', zero((uw.T*gw*uw)[0]+1), 'U=N^-1 partial_t')
check('witness_rest_metric', zero((s.eye(4)[:,1:]-s.Matrix([1,0,0,0])*bw.T).T*gw*(s.eye(4)[:,1:]-s.Matrix([1,0,0,0])*bw.T)-gam), 'gamma is observer-rest form; t slices need not be spacelike')
Ww = s.factor(s.trace(giw*ww*giw*ww.T))
target = nw**2*(b-r*q)**2/(7*a**4)
check('coupled_exact_W', zero(Ww-target), 'retains simultaneous lapse, spatial form and live shift')
point0 = {t:0,x:0,y:0,z:0,r:1,b:3,q:1}
point1 = {t:s.Rational(1,8),x:s.Rational(1,5),y:s.Rational(1,6),z:0,r:1,b:3,q:1}
W0 = Ww.subs(point0)
W1 = s.factor(Ww.subs(point1))
check('origin_W', W0 == s.Rational(4,7), 'direct projected metric derivative and full contraction')
check('interior_point', all(abs(point1[c])<s.Rational(1,4) for c in coords), 'second point strictly inside declared patch')
check('nonconstant_W', W1 != W0 and W1 > 0, str(W1))
check('zero_spatial_curl_nonzero_rotation', Ww.subs({**point0,b:0}) == s.Rational(1,7), 'r=q=1, b=0; live shift term alone survives')
check('joint_nonzero_variations', all(s.diff(v,c).subs(point1) != 0 for v,c in [(nw,t),(nw,y),(gam[0,0],t),(gam[0,0],x),(bw[1],t),(bw[1],x)]), 'lapse, spatial form, shift vary simultaneously at interior point')

directions = [s.eye(3)[:,i] for i in range(3)]
directions += [s.eye(3)[:,i]+s.eye(3)[:,j] for i,j in [(0,1),(0,2),(1,2)]]
for idx,v in enumerate(directions):
    J = s.zeros(4,2); J[0,0]=1; J[1:,1]=v
    h = J.T*gw*J
    gv = (v.T*gam*v)[0]
    bv = (bw.T*v)[0]
    check(f'pair_{idx}_pullback', zero(h-s.Matrix([[-nw**2,-nw**2*bv],[-nw**2*bv,gv-nw**2*bv**2]])), 'actual constant-direction coordinate immersion')
    check(f'pair_{idx}_determinant', zero(h.det()+nw**2*gv), 'm²=-det h=N² gamma(v,v)>0')
    check(f'pair_{idx}_same_origin_different_b', zero(h.subs({t:0,x:0,y:0,z:0,b:0})-h.subs({t:0,x:0,y:0,z:0,b:3})), 'all values agree at origin but W differs; first jets required')

# Ordinary Riemannian curvature of the coefficient-field gamma on the chosen t=0
# coordinate space. This is deliberately not an observer-rest hypersurface assertion.
g3 = gam.subs(t,0)
g3i = G0.inv()/(1+x*x)**2
spatial = (x,y,z)
GG = [[[s.simplify(sum(g3i[i,l]*(s.diff(g3[l,j],spatial[k])+s.diff(g3[l,k],spatial[j])-s.diff(g3[j,k],spatial[l])) for l in range(3))/2) for k in range(3)] for j in range(3)] for i in range(3)]
origin3 = {x:0,y:0,z:0}
Ric3 = s.Matrix(3,3,lambda j,k:sum(s.diff(GG[i][j][k],spatial[i])-s.diff(GG[i][j][i],spatial[k])+sum(GG[i][i][l]*GG[l][j][k]-GG[i][k][l]*GG[l][j][i] for l in range(3)) for i in range(3)).subs(origin3))
R3 = s.simplify(s.trace(G0.inv()*Ric3))
check('coordinate_rest_form_nonflat_diagnostic', R3 == -s.Rational(40,7), 'auxiliary coordinate Riemannian metric gamma at t=0; no integrable-rest or field equation claim')

controls = []


def reject(name, correct, mutant):
    if not zero(correct-target) or zero(mutant-correct):
        raise AssertionError(name)
    controls.append({'name':name,'caught':True,'exact_difference':str(s.factor(mutant-correct))})


reject('ordinary_spatial_curl_only',Ww,nw**2*b**2/(7*a**4))
reject('drop_lapse_weight',Ww,(b-r*q)**2/(7*a**4))
reject('drop_nonconstant_rest_scale',Ww,nw**2*(b-r*q)**2/7)
reject('flat_rest_inverse',Ww,nw**2*(b-r*q)**2/2)
reject('omit_antisymmetrization_half',Ww,4*Ww)
check('catch_vorticity_sign', not zero(ww[1:,1:]-nw*F.subs({N:nw,bet[0]:bw[0],bet[1]:bw[1],bet[2]:bw[2]}).doit()/2), 'tensor test needed; W cannot catch overall sign')
controls.append({'name':'vorticity_sign_caught_at_tensor_level','caught':True})
ue_flat = -nw*s.Matrix([1,*(eps*bw)])
Pe = s.eye(4)+ue_flat*uw.T
due = s.Matrix(4,4,lambda i,j:s.diff(ue_flat[j],coords[i])-s.diff(ue_flat[i],coords[j]))
we = Pe*due*Pe.T/2
fe = s.simplify(-2*we[1,2]/nw)
check('exact_amplitude_interaction', zero(fe-eps*b+eps**2*r*q), 'direct projected exterior derivative for beta -> epsilon beta')
check('linear_term_has_nonzero_finite_remainder', s.expand(fe-eps*b) == -eps**2*r*q, 'order-epsilon² term; no finite-time evolution inference')
check('scalar_readout_cannot_select_shift', s.diff(-s.log(nw),b) == 0 and s.diff(Ww,b) != 0, 'same lapse/Phi for all b; retained shifts carry additional data')

result = {'status':'PASS','kind':'author exact symbolic identities and diagnostic controls, not proof by finite sampling or independent review',
          'checks':checks,'check_count':len(checks),'controls':controls,'control_count':len(controls),
          'W_symbolic':str(Ww),'W_origin':str(W0),'W_interior':str(W1),'gamma_coordinate_R_origin':str(R3),
          'versions':{'python':platform.python_version(),'sympy':s.__version__},
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
