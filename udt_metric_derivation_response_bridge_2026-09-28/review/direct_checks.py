"""Direct-stage checks by varied density coefficients and a two-entry Hessian."""
import json
import platform
import time
import sympy as s

start=time.monotonic()
r=s.symbols('r', positive=True)
alpha,eps,k=s.symbols('alpha eps k',real=True)
f=s.Function('f')(r)
h=s.Function('h')(r)
checks=[]

def zero(name,value):
    residual=s.simplify(value)
    if residual != 0:
        raise AssertionError((name,str(residual)))
    checks.append(name)

def scalar(profile):
    return -s.diff(profile,r,2)-4*s.diff(profile,r)/r+2*(1-profile)/r**2

R=scalar(f)
# First vary the entire density, then integrate h', h'' coefficients by parts.
var=s.expand(s.diff(r**2*(scalar(f+eps*h)+alpha*scalar(f+eps*h)**2),eps).subs(eps,0))
A0=s.diff(var,h)
A1=s.diff(var,s.diff(h,r))
A2=s.diff(var,s.diff(h,r,2))
zero('varied_density_linear_in_test',var-A0*h-A1*s.diff(h,r)-A2*s.diff(h,r,2))
bulk=s.simplify(A0-s.diff(A1,r)+s.diff(A2,r,2))
boundary=A1*h+A2*s.diff(h,r)-s.diff(A2,r)*h
zero('pointwise_integration_by_parts',var-bulk*h-s.diff(boundary,r))
zero('B14_reduced_bulk',bulk+2*alpha*r**2*s.diff(R,r,2))
zero('B14_fourth_derivative_coefficient',s.diff(bulk,s.diff(f,r,4))-2*alpha*r**2)

# Derive the only Christoffels needed for the radial scalar Hessian directly.
gtt=-f;grr=1/f
Gamma_rtt=-s.diff(gtt,r)/(2*grr)
Gamma_rrr=s.diff(grr,r)/(2*grr)
F=1+2*alpha*R
Htt=-Gamma_rtt*s.diff(F,r)/gtt
Hrr=(s.diff(F,r,2)-Gamma_rrr*s.diff(F,r))/grr
difference=s.simplify(Hrr-Htt)
zero('B14_full_response_difference',difference-2*alpha*f*s.diff(R,r,2))
zero('B14_source_sign_and_weight',bulk+r**2*difference/f)
control=1+k*r**4
zero('B14_control',bulk.subs(f,control).doit()-120*alpha*k*r**2)
zero('B14_zero_alpha_control',bulk.subs(alpha,0))

# This additional supplied control solves only the reduced fourth-order equation.
# It prevents mistaking profile stationarity for full trace-free response.
c=s.symbols('c',nonzero=True)
profile=1+c*r**3
Rp=scalar(profile)
Fp=1+2*alpha*Rp
Up=-s.diff(profile,r,2)/2-s.diff(profile,r)/r
Vp=(1-profile-r*s.diff(profile,r))/r**2
Htp=s.diff(profile,r)*s.diff(Fp,r)/2
Hap=profile*s.diff(Fp,r)/r
clock_minus_angle=s.simplify(Fp*(Up-Vp)-Htp+Hap)
zero('reduced_only_control_R',Rp+20*c*r)
zero('reduced_only_control_stationary',bulk.subs(f,profile).doit())
zero('reduced_only_control_full_shape',clock_minus_angle-100*alpha*c**2*r**2+40*alpha*c/r+2*c*r)
if clock_minus_angle==0:
    raise AssertionError('reduced-only control failed to expose full-response loss')
checks.append('reduced_only_control_full_shape_nonidentity')

print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,'elapsed_s':time.monotonic()-start,'python':platform.python_version(),'sympy':s.__version__,'bulk':str(bulk),'reduced_only_clock_minus_angle':str(clock_minus_angle),'scope':'Independent B14 metric variation and projection control; no new action or full solution claim.'},indent=2))
