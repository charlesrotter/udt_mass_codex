#!/usr/bin/env python3
"""Exact analysis of the saved raw metric-three-jet output; source-exposed checks.

This is parent verification/record algebra, not fresh implementation independence.
"""
from pathlib import Path
import hashlib
import itertools
import json
import platform
import sympy as S

source = Path(__file__).parent/'checks/initial_rate.stdout'
raw = source.read_bytes()
data = json.loads(raw)
p,r,px,rx,pxx,rxx = S.symbols('p r p_X r_X p_XX r_XX',real=True)
s = S.Symbol('s',real=True,nonzero=True)
env = {str(x):x for x in (p,r,px,rx,pxx,rxx,s)}
env['Matrix'] = S.Matrix
read = lambda key:S.sympify(data[key],locals=env)
P,PD,L,L0,rem = map(read,['P','P_T_general_profile_jet','L_harmonic','L0','S'])
K,E,B,ED,BD = map(read,['K','E','B','E_T','B_T'])
d=p*p+r*r; W=p*rx-r*px;k=(d-s*s)/(2*s);tau=S.trace(K)
H=S.Matrix([[p,r],[r,-p]])
J=S.Matrix([[0,1],[-1,0]])
Hp=S.Matrix([[px,rx],[rx,-px]])
Hpp=S.Matrix([[pxx,rxx],[rxx,-pxx]])
checks=[]
def check(name,values):
    if not isinstance(values,(list,tuple,S.MatrixBase)):
        values=[values]
    bad=[str(S.factor(v)) for v in values if S.factor(v)!=0]
    checks.append({'name':name,'components':len(values),'nonzero':bad})
    if bad:
        print(json.dumps({'checks':checks},indent=2));raise AssertionError(name)

# Compact analytic identities are derived after the initial raw capture.
Ric3d=S.zeros(3);Ric3d[1:3,1:3]=-Hpp
check('E_T_compact_identity',ED-Ric3d-2*K*(tau*S.eye(3)-K)**2)
wantBD=S.zeros(3);wantBD[0,0]=-2*W
wantBD[1:3,1:3]=3*W*S.eye(2)+(3*d-5*s*s)/(2*s)*J*Hp+(p*px+r*rx)/s*J*H
check('B_T_compact_identity',BD-wantBD)
check('inverse_contraction_term_vanishes_for_this_initial_data',S.trace(K*E*B))
compactPD=-32*(pxx*rx-px*rxx)-16*k*W*(5*d/s+11*s)
check('general_jet_rate_compact_identity',PD-compactPD)
check('saved_quantity_recontracted_with_explicit_indices',PD-16*(
    sum(ED[i,j]*B[i,j]+E[i,j]*BD[i,j] for i,j in itertools.product(range(3),repeat=2))
    +4*sum(K[i,j]*E[j,h]*B[h,i] for i,j,h in itertools.product(range(3),repeat=3))))
PDh=S.factor(PD.subs({pxx:-p,rxx:-r}))
check('harmonic_rate',PDh-(32*W-16*k*W*(5*d/s+11*s)))
check('matched_small_amplitude_reference',L0-(11*s/2+2/s))
check('fractional_rate_closed_form',L-(11*s/2+5*d/(2*s)+2*s/(s*s-d)))
gap=d/(2*s)*(5+4/(s*s-d))
check('finite_amplitude_rate_gap',L-L0-gap)
check('undivided_remainder',rem-8*d*W/s**2*(5*s*s+4-5*d))

eps,c2,c3=S.symbols('epsilon c2 c3',real=True)
s0=-S.Rational(2,3)
scaled={p:eps*p,r:eps*r,px:eps*px,rx:eps*rx,s:s0+c2*eps**2+c3*eps**3}
matched=S.factor(rem.subs(scaled,simultaneous=True))
original=S.factor((PDh-(11*s0/2+2/s0)*P).subs(scaled,simultaneous=True))
coeff=lambda expr,n:S.factor(S.diff(expr,eps,n).subs(eps,0)/S.factorial(n))
check('matched_order4_completion_independent',coeff(matched,4)-112*d*W)
check('matched_order5_zero',coeff(matched,5))
check('original_background_order4_completion_dependence',coeff(original,4)-W*(112*d-S.Rational(32,3)*c2))
check('original_background_order5_if_c3_present',coeff(original,5)+S.Rational(32,3)*c3*W)
check('L0_slope_at_s0',S.diff(L0,s).subs(s,s0)-1)

# This extension follows the reviewer's independently derived decomposition suggestion.
# The pre-extension author analysis and successful capture are preserved.
fixed_scaled={p:eps*p,r:eps*r,px:eps*px,rx:eps*rx,pxx:eps*pxx,rxx:eps*rxx}
mc=lambda M,n:M.subs(fixed_scaled,simultaneous=True).applyfunc(lambda z:coeff(z,n))
background_term=S.factor(16*S.trace(mc(E,0)*mc(BD,2)))
first_order_products=S.factor(16*S.trace(mc(ED,1)*mc(B,1)+mc(E,1)*mc(BD,1)))
check('background_E_times_second_order_B_T',background_term-80*s*s*W)
check('first_order_curvature_rate_products',first_order_products-8*(s*s*W-4*(pxx*rx-px*rxx)))
check('leading_full_rate_decomposition',background_term+first_order_products-coeff(PD.subs(fixed_scaled,simultaneous=True),2))
check('background_term_half_at_s0_harmonic',background_term.subs(s,s0)-S.Rational(1,2)*coeff(PDh.subs(fixed_scaled,simultaneous=True),2).subs(s,s0))

# A concrete exact rational harmonic point; no fitted outcome/observational claim.
point={s:s0,p:S.Rational(1,10),r:0,px:0,rx:S.Rational(1,8),pxx:-S.Rational(1,10),rxx:0}
witness={key:str(S.factor(expr.subs(point))) for key,expr in
         {'kappa':k,'P':P,'P_T':PDh,'L0':L0,'L':L,'L_minus_L0':gap,'S':rem}.items()}
assert S.factor(gap.subs(point))<0 and S.factor(L.subs(point))<0
checks.append({'name':'rational_safe_witness_has_strict_negative_fractional_gap','components':2,'nonzero':[]})

# Original-background cancellation chosen algebraically after discovery; an explicit control.
a,X=S.symbols('a X',real=True)
equal={p:a*S.cos(X),r:a*S.sin(X),px:-a*S.sin(X),rx:a*S.cos(X)}
cancel=S.trigsimp(coeff(original,4).subs(equal).subs(c2,S.Rational(21,2)*a*a))
check('equal_quadrature_original_background_order4_cancellation',cancel)
check('equal_quadrature_matched_order4_survives',S.trigsimp(coeff(matched,4).subs(equal))-112*a**4)

# Explicitly authorized outside-safe-box cancellation control, not a safe-box extension.
outside={p:s*S.cos(X),r:s*S.sin(X),px:-s*S.sin(X),rx:s*S.cos(X)}
check('outside_initial_P_cancels',S.trigsimp(P.subs(outside)))
check('outside_initial_P_rate_nonzero',S.trigsimp(PDh.subs(outside))-32*s*s)

# Six original density records, common marking; the equation/harmonic identity are supplied.
dirs=[S.eye(3)[:,i] for i in range(3)]+[S.eye(3)[:,i]+S.eye(3)[:,j] for i,j in [(0,1),(0,2),(1,2)]]
Kx=K.diff(p)*px+K.diff(r)*rx
qT=[-2*(v.T*K*v)[0] for v in dirs]
qTX=[-2*(v.T*Kx*v)[0] for v in dirs]
def recover(values):
    M=S.diag(*values[:3])
    for index,(i,j) in enumerate([(0,1),(0,2),(1,2)],3):
        M[i,j]=M[j,i]=(values[index]-values[i]-values[j])/2
    return -M/2
Kr,Kxr=recover(qT),recover(qTX)
check('six_original_records_recover_K',Kr-K)
check('six_original_mixed_second_records_recover_K_X',Kxr-Kx)
ss=(Kr[1,1]+Kr[2,2])/2;pp=(Kr[2,2]-Kr[1,1])/2;rr=-Kr[1,2]
ppx=(Kxr[2,2]-Kxr[1,1])/2;rrx=-Kxr[1,2]
dd=pp*pp+rr*rr;ww=pp*rrx-rr*ppx;kk=(dd-ss*ss)/(2*ss)
recovered=32*ww-16*kk*ww*(5*dd/ss+11*ss)
check('harmonic_P_T_from_second_record_jets',recovered-PDh)

out={'python':platform.python_version(),'sympy':S.__version__,
     'source_stdout_sha256':hashlib.sha256(raw).hexdigest(),
     'classification':'source-exposed parent exact analysis and saved-quantity recomputation, not independent scientific review',
     'checks':checks,'compact_P_T':str(compactPD),'L0':str(S.factor(L0)),
     'L_minus_L0':str(gap),'S':str(S.factor(rem)),
     's0':str(s0),'L0_s0':str(S.factor(L0.subs(s,s0))),
     'background_E0_BD2_contribution':str(background_term),
     'first_order_curvature_rate_products':str(first_order_products),
     'matched_S_order4':str(coeff(matched,4)),'original_S_order4':str(coeff(original,4)),
     'original_S_order5':str(coeff(original,5)),'exact_rational_witness':witness,
     'safe_domain_sign_proof':'s<0,0<d<s^2 for nonaligned data; hence d/(2s)*(5+4/(s^2-d))<0 and L0<0',
     'record_order':'second total-order q_T and q_TX SUFFICIENT ONLY with supplied harmonic family/Ric=0/flat gamma; general metric third jet sufficient; no minimality claim',
     'outside_control':'P=0, P_T=32s^2; outside original amplitude-safe box, analytic constrained datum considered individually',
     'completion_control':'equal quadrature with c(epsilon)=(21/2)a^2 epsilon^2 cancels original-background order4; matched order4 remains112a^4; algebraically chosen after discovery'}
print(json.dumps(out,indent=2))
