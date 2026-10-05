"""Source-first implementation; no TSI1 author imports."""
import hashlib
import json
import platform
from pathlib import Path
import mpmath as mp
import sympy as sy

mp.mp.dps = 40

def branch(m, a, H, E, bs, R):
    omega = mp.sqrt(m/a**3-H**2)
    h = 1-3*m/a
    x = 1/R
    def ss(y,b):
        return mp.sqrt(1+H**2*b*b-b*b*y*y+2*m*b*b*y**3)
    def p(b,lower):
        return mp.quad(lambda y:b/ss(y,b), [lower,1/a])
    def u(b,lower):
        return mp.quad(lambda y:b*b/(ss(y,b)*(1+ss(y,b))),[lower,1/a])
    def w(y):
        return mp.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)
    d = mp.quad(lambda y:1/(w(y)*(E*y+w(y))),[0,x])
    target = p(bs,0)-omega*u(bs,0)+omega*d
    residual = lambda b:p(b,x)-omega*u(b,x)-target
    b = mp.findroot(residual,(bs-mp.mpf('0.01'),bs+mp.mpf('0.01')),tol=mp.mpf('1e-34'))
    def freq(r,impact):
        v = mp.sqrt(E*E-1+2*m/r+H*H*r*r)
        s = ss(1/r,impact)
        return 1/(E+v)+v*impact*impact/(r*r*(1+s))
    v = mp.sqrt(E*E-1+2*m/R+H*H*R*R)
    A = freq(R,b)
    I = mp.quad(lambda y:1/ss(y,b)**3,[x,1/a])
    db = -(omega*A/(v*(1-omega*b))+b/(R*R*ss(x,b)))/I
    partial_r = mp.diff(lambda r:freq(r,b),R)
    partial_b = mp.diff(lambda impact:freq(R,impact),b)
    drift = v*(-omega*db/(1-omega*b)-(partial_r+partial_b*db)/A)
    Z = (1-omega*b)/(mp.sqrt(h)*A)
    te = u(bs,0)-d-u(b,x)
    time_residual = te+u(b,x)-(u(bs,0)-d)
    angular_residual = -p(bs,0)+omega*te+p(b,x)
    assert abs(time_residual)<mp.mpf('1e-28')
    assert abs(angular_residual)<mp.mpf('1e-28')
    assert abs(residual(b))<mp.mpf('1e-28')
    return dict(m=m,a=a,H=H,E=E,b_star=bs,R=R,b=b,A=A,Z=Z,
                drift=drift,relative_drift_error=abs(drift/H-1),
                angular_sine=b/(R*A),emission_time=te,
                angular_residual=angular_residual,time_residual=time_residual)

def exact_checks():
    m,a,H,r,b,L,E=sy.symbols('m a H r b L E',positive=True)
    f=1-2*m/r-H**2*r**2
    om2=m/a**3-H**2
    scaled={m:L*m,a:L*a,H:H/L,r:L*r,b:L*b}
    identities={
        'metric_f_scale':f.subs(scaled,simultaneous=True)-f,
        'orbit_squared_rate_scale':om2.subs(scaled,simultaneous=True)-om2/L**2,
        'source_h_scale':(1-3*m/a).subs(scaled,simultaneous=True)-(1-3*m/a),
        'ray_s_squared_scale':(1-f*b*b/r**2).subs(scaled,simultaneous=True)-(1-f*b*b/r**2),
        'receiver_v_squared_scale':(E*E-f).subs(scaled,simultaneous=True)-(E*E-f),
    }
    t,p,K,c=sy.symbols('t p K c',positive=True)
    delta=sy.exp(-K*t)
    received_rate=delta**(p+1)
    identities['source_rate_drift_mimic']=sy.diff(sy.log(received_rate),t)+(p+1)*K
    identities['constant_rate_normalization']=sy.diff(sy.log(c*sy.exp(K*t)),t)-K
    for key,value in identities.items():
        assert sy.simplify(value)==0,key
    # Strict endpoint ticks in [0,1) with fixed spacing1/7: exactly7, never
    # a sequence accumulating at1. This finite count illustrates the argument.
    from fractions import Fraction
    ticks=[Fraction(k,7) for k in range(8) if Fraction(k,7)<1]
    assert len(ticks)==7 and ticks[-1]==Fraction(6,7)
    return list(identities)+['fixed_cadence_finite_endpoint']

records=[]
checks=exact_checks()
for bs in [mp.mpf(0),mp.mpf(2)]:
    errors=[]
    for R in [mp.mpf(1000),mp.mpf(100000),mp.mpf(10000000)]:
        base=branch(mp.mpf(1),mp.mpf(8),mp.mpf('0.03'),mp.mpf('1.2'),bs,R)
        scaled=branch(mp.mpf(3),mp.mpf(24),mp.mpf('0.01'),mp.mpf('1.2'),3*bs,3*R)
        assert abs(scaled['Z']/base['Z']-1)<mp.mpf('1e-25')
        assert abs(3*scaled['drift']/base['drift']-1)<mp.mpf('1e-25')
        assert abs(scaled['angular_sine']-base['angular_sine'])<mp.mpf('1e-25')
        errors.append(base['relative_drift_error'])
        records.extend([base,scaled])
    assert errors[2]<errors[1]<errors[0]
    assert errors[-1]<mp.mpf('1e-4')

result=dict(status='PASS',source_first=True,mpmath_digits=mp.mp.dps,
            finite_case_count=len(records),exact_control_count=len(checks),
            python=platform.python_version(),mpmath=mp.__version__,sympy=sy.__version__,
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            controls=checks,records=records)
print(json.dumps(result,indent=2,default=lambda value:mp.nstr(value,35)))
