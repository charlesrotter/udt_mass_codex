"""Author exact profile/constraint identities plus explicitly non-certified numerical illustrations."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s
import mpmath as mp

t,k,x,e = s.symbols('t k x e',positive=True)
f = s.Function('F')(t)
df = s.diff(f,t)
ode = -df/t-k*k*f
tests=[]
def zero(name,v):
    r=s.simplify(s.expand_trig(s.expand(v)))
    assert r==0,(name,r)
    tests.append(name)
L=t*t*(df*df+k*k*f*f)/2+t*f*df/2-s.Rational(9,8)
lam=e*e*(L+t*f*df*s.cos(2*k*x)/2)
p=e*f*s.cos(k*x)
zero('L_antiderivative',s.diff(L,t).subs(s.diff(f,t,2),ode)-t*(df*df+k*k*f*f)/2)
zero('lambda_t_constraint',s.diff(lam,t).subs(s.diff(f,t,2),ode)-t*(s.diff(p,t)**2+s.diff(p,x)**2))
zero('lambda_x_constraint',s.diff(lam,x)-2*t*s.diff(p,t)*s.diff(p,x))
zero('initial_L',L.subs({f:0,df:s.Rational(3,2),t:1},simultaneous=True))
zero('initial_lambda_delta',lam.subs({f:0,df:s.Rational(3,2),t:1},simultaneous=True))
for B in (s.besselj,s.bessely):
    b=B(0,k*t)
    zero('Bessel_ODE_'+B.__name__,s.diff(b,t,2)+s.diff(b,t)/t+k*k*b)
Fexpr=3*s.pi/4*(s.besselj(0,k)*s.bessely(0,k*t)-s.bessely(0,k)*s.besselj(0,k*t))
zero('Bessel_initial_value',Fexpr.subs(t,1))
# Initial derivative uses standard canonical Bessel Wronskian 2/(pi*k).
zero('Wronskian_normalization_arithmetic',3*s.pi/4*k*(2/(s.pi*k))-s.Rational(3,2))
T=s.symbols('T',positive=True)
h=s.Function('h')(T)
# t=T^(4/3), F=2h. Derivative conversion written independently of Bessel expression.
dt_dT=s.Rational(4,3)*T**s.Rational(1,3)
Ft=2*s.diff(h,T)/dt_dT
Ftt=s.diff(Ft,T)/dt_dT
zero('G327_ODE_exact_conversion',
 (Ftt+Ft/T**s.Rational(4,3)+s.Rational(9,16)*2*h)*dt_dT**2/2
 -(s.diff(h,T,2)+s.diff(h,T)/T+T**s.Rational(2,3)*h))
Z0=s.Rational(16,9)*T**s.Rational(2,3)
orth_coeff=Z0*(s.Rational(9,16)*h-Ft/(8*T**s.Rational(4,3)))
zero('G327_orthonormal_tidal_conversion',orth_coeff-(-s.diff(h,T)/(3*T)+T**s.Rational(2,3)*h))
# Background-normalized coordinate tidal coefficient includes the tetrad variation.
zero('G327_equation15_with_basis_conversion',orth_coeff+4*h/(9*T*T)
 -(-s.diff(h,T)/(3*T)+4*h/(9*T*T)+T**s.Rational(2,3)*h))
bad_lam=e*e*L
bad_momentum=s.simplify(s.diff(bad_lam,x)-2*t*s.diff(p,t)*s.diff(p,x))
sample=bad_momentum.subs({e:s.Rational(1,6),t:2,k:s.Rational(3,4),f:1,df:1,x:s.pi/3},simultaneous=True)
assert s.simplify(sample)!=0
tests.append('mutant_omitted_spatial_lambda_rejected_by_momentum')

def rows(dps):
    mp.mp.dps=dps
    kk=mp.mpf(3)/4; ee=mp.mpf(1)/6
    A=-3*mp.pi/4*mp.bessely(0,kk); B=3*mp.pi/4*mp.besselj(0,kk)
    c=kk*(A*A+B*B)/mp.pi
    D=mp.sqrt(2*(A*A+B*B)/(mp.pi*kk))
    def FF(v):
        return A*mp.besselj(0,kk*v)+B*mp.bessely(0,kk*v)
    def FP(v):
        return -kk*(A*mp.besselj(1,kk*v)+B*mp.bessely(1,kk*v))
    assert abs(FF(1))<mp.mpf('1e-45')
    assert abs(FP(1)-mp.mpf(3)/2)<mp.mpf('1e-45')
    out=[]
    for v in [1,2,10,100,1000]:
        tt=mp.mpf(v); fv=FF(tt); fp=FP(tt)
        Lv=tt*tt*(fp*fp+kk*kk*fv*fv)/2+tt*fv*fp/2-mp.mpf(9)/8
        oscill=abs(tt*fv*fp/2)
        dmin=ee*ee*(Lv-oscill);dmax=ee*ee*(Lv+oscill)
        Hmin=mp.exp(-dmax/4);Hmax=mp.exp(-dmin/4)
        # xi=0: P_x=0. Dimensionless orthonormal tidal contrast, not an energy.
        tidal=tt*tt*(ee*kk*kk*fv-ee*fp/(4*tt)+tt*ee**3*fp**3/4)
        out.append([tt,ee*abs(fv),ee*mp.sqrt(fv*fv+(fp/kk)**2),dmin,dmax,Hmin,Hmax,tidal])
    # Simple positive integrand quadrature on one bounded interval checks primitive.
    tt=mp.mpf(2); fv=FF(tt);fp=FP(tt)
    prim=tt*tt*(fp*fp+kk*kk*fv*fv)/2+tt*fv*fp/2-mp.mpf(9)/8
    integral=mp.quad(lambda v:v*(FP(v)**2+kk*kk*FF(v)**2)/2,[1,2])
    assert abs(prim-integral)<mp.mpf('1e-45')
    return c,D,out

low=rows(60); high=rows(90)
differences=[]
for u,v in zip(low[2],high[2]):
    for aa,bb in zip(u,v):
        differences.append(abs(aa-bb)/(1+abs(bb)))
assert max(differences)<mp.mpf('1e-45')
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
 'mpmath':mp.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'exact_predicates':tests,'count_exact_predicates':len(tests),
 'numeric_method':'60 versus 90 digit mpmath, same library, illustrative NOT interval-certified',
 'numeric_tolerance':'1e-45 relative/(1+abs(value)); not a proof of asymptotics',
 'max_precision_comparison':mp.nstr(max(differences),12),
 'c':mp.nstr(high[0],30),'D':mp.nstr(high[1],30),
 'columns':['t','max_abs_P','relative_profile_phase_norm','min_delta_lambda','max_delta_lambda','min_Hrho_ratio','max_Hrho_ratio','tidal_contrast_over_Hrho_squared_at_xi0'],
 'rows':[[mp.nstr(v,20) for v in r] for r in high[2]],
 'actual_mutant_residual':str(sample)},indent=2))
