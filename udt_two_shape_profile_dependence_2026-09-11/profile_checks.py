#!/usr/bin/env python3
"""TI3 exact construction/checks; source-exposed reuse is not independent review."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(__file__).resolve().parent
pins = json.loads((BASE / 'SOURCE_PINS.json').read_text())['sources']
for name, expected in pins.items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
source = json.loads((ROOT / 'udt_two_shape_evolution_2026-09-11/checks/initial_rate.stdout').read_text())
p,r,px,rx,pxx,rxx = S.symbols('p r p_X r_X p_XX r_XX', real=True)
s = S.Symbol('s', real=True, nonzero=True)
local = {str(v):v for v in (p,r,px,rx,pxx,rxx,s)}
rawP = S.sympify(source['P'], locals=local)
rawPD = S.sympify(source['P_T_general_profile_jet'], locals=local)
d = p*p+r*r
k = (d-s*s)/(2*s)
W = p*rx-r*px
V = pxx*rx-px*rxx
P = -32*k*W
PD = -32*V-16*k*W*(5*d/s+11*s)
K = S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
tau = S.trace(K)
def dx(z):
    return z.diff(p)*px+z.diff(r)*rx+z.diff(px)*pxx+z.diff(rx)*rxx
Kx=dx(K)
KT=tau*K-2*K*K
checks=[]
def clean(z):
    return S.factor(S.trigsimp(z))
def check(name, zs):
    if not isinstance(zs,(list,tuple,S.MatrixBase)):
        zs=[zs]
    bad=[str(v) for z in zs if (v:=clean(z))!=0]
    checks.append({'name':name,'components':len(zs),'nonzero':bad})
    if bad:
        print(json.dumps({'status':'FAIL','checks':checks},indent=2))
        raise AssertionError(name)
def require(name, value):
    checks.append({'name':name,'true':bool(value)})
    if not value:
        print(json.dumps({'status':'FAIL','checks':checks},indent=2))
        raise AssertionError(name)
check('same_pinned_raw_metric_three_jet_P',P-rawP)
check('same_pinned_raw_metric_three_jet_rate',PD-rawPD)
check('full_constraints_general_profile', [tau*tau-S.trace(K*K),
      *[Kx[0,i]-(dx(tau) if i==0 else 0) for i in range(3)]])
check('s_constant_is_load_bearing', dx(K[0,0]-tau))
J=S.Matrix([[0,1],[-1,0]])
H=S.Matrix([[p,r],[r,-p]])
Hx=dx(H)
Qm=J*Hx
E=S.diag(2*s*k,-k*(s+p),-k*(s-p))
E[1,2]=E[2,1]=-k*r
Bm=S.zeros(3); Bm[1:3,1:3]=Qm
Ric3T=S.zeros(3); Ric3T[1:3,1:3]=-dx(dx(H))
ET=Ric3T+2*K*(tau*S.eye(3)-K)**2
BT=S.zeros(3); BT[0,0]=-2*W
BT[1:3,1:3]=3*W*S.eye(2)+(3*d-5*s*s)/(2*s)*Qm+(p*px+r*rx)/s*J*H
check('accepted_matrix_contraction_correspondence',
      16*S.trace(ET*Bm+E*BT+4*K*E*Bm)-PD)
check('metric_inverse_contraction_term_retained_then_zero',S.trace(K*E*Bm))

q,D=S.symbols('Q D', real=True)
L=11*s/2+5*D/(2*s)-2*s*q/(s*s-D)
L0=11*s/2-2*q/s
Delta=D/(2*s)*(5-4*q/(s*s-D))
check('general_ratio_only_nonzero_W', PD/P-L.subs({D:d,q:V/W}))
check('matched_reference_correction',L-L0-Delta)
check('explicit_small_amplitude_remainder',
      Delta-D/(2*s)*(5-4*q/s**2)+2*q*D**2/(s**3*(s**2-D)))
Sformal=8*d/s**2*(5*(s*s-d)*W-4*V)
check('matched_undivided_expression_only_equal_to_comparison_where_W_nonzero',
      PD-(11*s/2-2*V/(s*W))*P-Sformal)
check('orientation_profile_sign_control', [P.subs({r:-r,rx:-rx,rxx:-rxx})+P,
      PD.subs({r:-r,rx:-rx,rxx:-rxx})+PD])

x,theta=S.symbols('X theta',real=True)
a,b=S.symbols('a b',positive=True)
n=S.Symbol('n',integer=True,positive=True)
lam=S.Symbol('lambda',nonnegative=True)
def jets(f,g):
    return {p:f,r:g,px:S.diff(f,x),rx:S.diff(g,x),
            pxx:S.diff(f,x,2),rxx:S.diff(g,x,2)}
harm=jets(a*S.cos(n*x),b*S.cos(n*x+theta))
check('Hn_W',W.subs(harm)+a*b*n*S.sin(theta))
check('Hn_V',V.subs(harm)+n*n*W.subs(harm))
check('Hn_reference_unit_mode_recovers_TI2', L0.subs(q,-1)-(11*s/2+2/s))
check('Hn_frequency_reference_difference',L0.subs(q,-n*n)-L0.subs(q,-1)-2*(n*n-1)/s)

f=a*(1+lam*(1-S.cos(x))); g=b*S.sin(x)
off=jets(f,g)
Wo=a*b*((1+lam)*S.cos(x)-lam)
Vo=a*b*lam
check('Flambda_W', W.subs(off)-Wo)
check('Flambda_V', V.subs(off)-Vo)
point={v:clean(z.subs(x,0)) for v,z in off.items()}
check('same_K_at_X0_all_lambda', K.subs(point)-K.subs(point).subs(lam,0))
check('same_KX_at_X0_all_lambda',Kx.subs(point)-Kx.subs(point).subs(lam,0))
check('same_KT_at_X0_all_lambda',KT.subs(point)-KT.subs(point).subs(lam,0))
# Every four-dimensional metric jet of total order <=2 is covered: constant g00/g0i;
# spatial blocks gamma,I, gamma_T,-2K, gamma_TT,-2KT, gamma_TX,-2KX;
# all purely spatial and all transverse-coordinate derivatives are zero.
metric2={'value':S.eye(3),'T':-2*K,'X':S.zeros(3),'Y':S.zeros(3),'Z':S.zeros(3),
         'TT':-2*KT,'TX':-2*Kx,'TY':S.zeros(3),'TZ':S.zeros(3),
         'XX':S.zeros(3),'XY':S.zeros(3),'XZ':S.zeros(3),
         'YY':S.zeros(3),'YZ':S.zeros(3),'ZZ':S.zeros(3)}
dirs=[S.eye(3)[:,i] for i in range(3)]
dirs += [S.eye(3)[:,i]+S.eye(3)[:,j] for i,j in ((0,1),(0,2),(1,2))]
record_res=[]
for mat in metric2.values():
    for v in dirs:
        z=(v.T*mat*v)[0].subs(point)
        record_res.append(z-z.subs(lam,0))
check('six_densities_entire_total_order_two_jet',record_res)
check('same_P_at_X0',P.subs(point)-P.subs(point).subs(lam,0))
check('different_rate_at_X0',PD.subs(point)-PD.subs(point).subs(lam,0)+32*a*b*lam)
third=(-2*dx(Kx)).subs(point)
require('third_record_jet_distinguishes_lambda2_from_lambda0',
        any(clean(z)!=0 for z in third.subs(lam,2)-third.subs(lam,0)))
# Polarization commutes with every marked derivative, including TXX.
m00,m11,m22,m01,m02,m12=S.symbols('m00 m11 m22 m01 m02 m12')
M=S.Matrix([[m00,m01,m02],[m01,m11,m12],[m02,m12,m22]])
dens=[(v.T*M*v)[0] for v in dirs]
recovered=S.diag(*dens[:3])
for idx,(i,j) in enumerate(((0,1),(0,2),(1,2))):
    recovered[i,j]=recovered[j,i]=(dens[3+idx]-dens[i]-dens[j])/2
check('six_direction_polarization_any_derivative',recovered-M)

anchor={a:S.Rational(1,100),b:S.Rational(1,100),s:S.Rational(-2,3)}
anchors={}
for lv in (0,2):
    sub={**anchor,lam:lv}
    pp=clean(P.subs(point).subs(sub)); pd=clean(PD.subs(point).subs(sub))
    rate=clean(pd/pp); ref=clean(L0.subs(q,lam).subs(sub))
    anchors[str(lv)]={name:str(val) for name,val in
       {'P':pp,'P_T':pd,'L':rate,'L0':ref,'L_minus_L0':rate-ref,'d_P_squared':2*pp*pd}.items()}
    require(f'anchor_lambda{lv}_sign', (rate<0) if lv==0 else (rate>0))
    require(f'anchor_lambda{lv}_safe_global_bound',
            (anchor[a]*(1+2*lv)<S.Rational(1,4)) and (anchor[b]<S.Rational(1,4)))
check('anchor_opposite_rate_difference', S.sympify(anchors['2']['P_T'])-
      S.sympify(anchors['0']['P_T'])+S.Rational(64,10000))

# For lambda>0 choose positive-sine zero cos X=lambda/(1+lambda).
cz=lam/(1+lam); sz=S.sqrt(1-cz**2)
zero={v:clean(z.subs({S.cos(x):cz,S.sin(x):sz})) for v,z in off.items()}
check('Flambda_zero_P',P.subs(zero))
check('Flambda_zero_rate',PD.subs(zero)+32*a*b*lam)
check('Flambda_zero_is_simple',S.diff(Wo,x).subs({S.cos(x):cz,S.sin(x):sz})+a*b*S.sqrt(1+2*lam))
false_harm=PD.subs({pxx:-p,rxx:-r})
false_error=clean((PD-false_harm).subs(point))
check('wrong_harmonic_prior_changes_original_rate', false_error+32*a*b*(lam+1))
require('wrong_harmonic_prior_detected_at_anchor',false_error.subs({**anchor,lam:2})!=0)

eps,d1,w,v,c2,c3=S.symbols('epsilon d1 w v c2 c3',real=True)
s0=S.Rational(-2,3)
se=s0+c2*eps**2+c3*eps**3
Pe=16*(s*s-eps**2*d1)*eps**2*w/s
Se=8*eps**4*d1/s**2*(5*(s*s-eps**2*d1)*w-4*v)
check('matched_S_exact_amplitude_polynomial',Se-
      (8*eps**4*d1/s**2*(5*s*s*w-4*v)-40*eps**6*d1**2*w/s**2))
original=Se+(L0-L0.subs(s,s0))*Pe
series=S.series(original.subs({s:se,q:v/w}),eps,0,6).removeO().expand()
leading=8*d1/s0**2*(5*s0*s0*w-4*v)
comp=16*s0*(S.Rational(11,2)*w+2*v/s0**2)
check('original_reference_completion_through_fifth_order',
      series-eps**4*(leading+comp*c2)-eps**5*comp*c3)
check('harmonic_original_reference_recovers_TI2',comp.subs(v,-w)+S.Rational(32,3)*w)

out={'status':'PASS','python':platform.python_version(),'sympy':S.__version__,
     'route':'source-exposed exact profile/constraint/record algebra; no fresh raw tensor reproof',
     'source_pins_sha256':hashlib.sha256((BASE/'SOURCE_PINS.json').read_bytes()).hexdigest(),
     'checks':checks,'anchors':anchors,'general':{'P':str(P),'P_T':str(PD),'L':str(L),
     'L0':str(L0),'L_minus_L0':str(Delta),'matched_S_algebraic_extension':str(Sformal)},
     'offset':{'W':str(Wo),'V':str(Vo),'zero_P_T':str(-32*a*b*lam),
               'X0_false_harmonic_prior_error':str(false_error)},
     'completion':{'matched_epsilon4':str(clean(leading)),
                   'original_extra_c2_epsilon4_c3_epsilon5':str(clean(comp))},
     'existence':'analytic argument reviewed separately; passing algebra does not prove CK hypotheses',
     'no_claims':['PDE trajectory','native equation selection','TI3 promotion','global classification']}
print(json.dumps(out,indent=2))
