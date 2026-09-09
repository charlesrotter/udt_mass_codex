"""Independent source-first Bessel arithmetic; finite checks, not asymptotic proof."""
import json
import platform
import mpmath as m
m.mp.dps=50
b=m.mpf(3)/4
e=m.mpf(1)/6
J,Y=m.besselj(0,b),m.bessely(0,b)
def f(t):
    return 3*m.pi/4*(J*m.bessely(0,b*t)-Y*m.besselj(0,b*t))
def fp(t):
    return 3*m.pi*b/4*(-J*m.bessely(1,b*t)+Y*m.besselj(1,b*t))
def L(t,x):
    v,w=f(t),fp(t)
    return e*e/2*(t*t*(w*w+b*b*v*v)+t*v*w*(1+m.cos(2*x))-m.mpf(9)/4)
def LT(t,x):
    return e*e*t*(fp(t)**2*m.cos(x)**2+b*b*f(t)**2*m.sin(x)**2)
assert abs(f(1))<m.mpf('1e-45')
assert abs(fp(1)-m.mpf(3)/2)<m.mpf('1e-45')
assert abs(J*(-b*m.bessely(1,b))-(-b*m.besselj(1,b))*Y-2/m.pi)<m.mpf('1e-45')
integral_errors=[]
ode_errors=[]
for t in (m.mpf(2),m.mpf(8),m.mpf(20)):
    ode_errors.append(abs(m.diff(f,t,2)+fp(t)/t+b*b*f(t)))
    for x in (m.mpf(0),m.pi/5,m.pi/2):
        integral_errors.append(abs(L(t,x)-m.quad(lambda u:LT(u,x),[1,t])))
assert max(ode_errors)<m.mpf('1e-45')
assert max(integral_errors)<m.mpf('1e-45')
c=e*e*27*m.pi/64*(J*J+Y*Y)
rows=[]
for t in (1,2,10,100,1000,10000):
    t=m.mpf(t)
    vals=[L(t,x) for x in (0,m.pi/4,m.pi/2)]
    rows.append(dict(t=str(t),f=m.nstr(f(t),18),
        L_min=m.nstr(min(vals),18),L_max=m.nstr(max(vals),18),
        Lmean_over_t=m.nstr(L(t,m.pi/4)/t,18),
        area_rate_ratio_max=m.nstr(m.exp(-min(vals)/4),18),
        Lminusct_range=[m.nstr(min(vals)-c*t,18),m.nstr(max(vals)-c*t,18)]))
print(json.dumps(dict(python=platform.python_version(),mpmath=m.__version__,dps=m.mp.dps,
    amplitude=str(e),b=str(b),c=m.nstr(c,30),
    max_integral_error=m.nstr(max(integral_errors),10),
    max_ode_error=m.nstr(max(ode_errors),10),rows=rows,
    result='PASS_FINITE_ARITHMETIC_ONLY'),indent=2))
