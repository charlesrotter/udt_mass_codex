"""PSC1 independent local calculations; not a physical field solver."""
import json
import platform
import sympy as s

checks = {}
def zero(name, expr):
    value = s.simplify(expr)
    assert value == 0, (name, value)
    checks[name] = str(value)

# Direct second derivative of entropy density times area; A'=theta A.
lam=s.symbols('lambda', real=True)
F0=s.symbols('F0', positive=True)
F1,F2,Rkk,theta=s.symbols('F1 F2 Rkk theta', real=True)
A = 1 + theta*lam + (theta**2/2-Rkk)*lam**2/2
F = F0+F1*lam+F2*lam**2/2
entropy=s.expand(A*F)
theta0=-F1/F0
zero('entropy_first_derivative_stationary',s.diff(entropy,lam).subs(lam,0).subs(theta,theta0))
second=s.diff(entropy,lam,2).subs(lam,0).subs(theta,theta0)
expected=-F0*Rkk+F2-s.Rational(3,2)*F1**2/F0
zero('entropy_second_derivative',second-expected)
production=-lam*s.Rational(3,2)*F1**2/F0
zero('production_cancels_extra_gradient',lam*second-production-lam*(-F0*Rkk+F2))
checks['positive_production_example']=str(production.subs({lam:-1,F0:2,F1:3}))
assert production.subs({lam:-1,F0:2,F1:3}) == s.Rational(27,4)

# Genuine metric-curvature witness, static conformal Lorentz metric.
# R = -6 exp(-2w) (Delta w+|grad w|^2); scalar Box uses 4D conformal factor.
x,y=s.symbols('x y',real=True)
w=x*x*y+x**5
grad=lambda a,b:s.diff(a,x)*s.diff(b,x)+s.diff(a,y)*s.diff(b,y)
box=lambda a:s.exp(-2*w)*(s.diff(a,x,2)+s.diff(a,y,2)+2*grad(w,a))
R=-6*s.exp(-2*w)*(s.diff(w,x,2)+s.diff(w,y,2)+grad(w,w))
F=1+2*R
X=s.exp(-2*w)*grad(F,F)
# div[3/(2F) dF dF] = 3/2[(Box F/F-X/F^2)dF+dX/(2F)].
Bx=s.Rational(3,2)*((box(F)/F-X/F**2)*s.diff(F,x)+s.diff(X,x)/(2*F))
By=s.Rational(3,2)*((box(F)/F-X/F**2)*s.diff(F,y)+s.diff(X,y)/(2*F))
origin={x:0,y:0}
curl=(s.diff(By,x)-s.diff(Bx,y)).subs(origin).doit()
assert curl == 51840, curl
checks['metric_obstruction_curl_dx_By_minus_dy_Bx']=str(curl)
zero('metric_F_origin',F.subs(origin)-1)
zero('metric_R_origin',R.subs(origin))
zero('metric_R_gradient_y',s.diff(R,y).subs(origin)+12)
zero('metric_BoxF_gradient_x',s.diff(box(F),x).subs(origin)+1440)

# The polynomial is a mathematical nonselection/control example.
r,alpha,beta,B,Xr,eps,rho,Brho,Xrho=s.symbols('R alpha beta BoxR X epsilon rho Boxrho Xrho')
f=r+alpha*r**2+beta*r**3
F=s.diff(f,r)
trace=F*r-2*f+3*(s.diff(F,r)*B+s.diff(F,r,2)*Xr)
zero('polynomial_exact_trace',trace-(-r+6*alpha*B+beta*(r**3+18*r*B+18*Xr)))
expanded=s.expand(trace.subs({r:eps*rho,B:eps*Brho,Xr:eps**2*Xrho}))
zero('shared_flat_linear_trace',expanded.coeff(eps,1)-(-rho+6*alpha*Brho))
mass=(F-r*s.diff(F,r))/(3*s.diff(F,r))
zero('polynomial_background_mass',mass-(1-3*beta*r**2)/(6*alpha+18*beta*r))
zero('polynomial_flat_mass',mass.subs(r,0)-1/(6*alpha))
zero('background_mass_slope',s.diff(mass,r).subs(r,0)+beta/(2*alpha**2))
m2,C,D,Lambda=s.symbols('m2 C D Lambda')
Flinear=C*(r+3*m2)
zero('constant_pole_ode',(r+3*m2)*s.diff(Flinear,r)-Flinear)
fquad=C*r**2/2+3*C*m2*r+D
zero('constant_pole_primitive',s.diff(fquad,r)-Flinear)
zero('constant_pole_mass',(Flinear-r*s.diff(Flinear,r))/(3*s.diff(Flinear,r))-m2)
zero('fixed_Lambda_vacuum_derivative',s.diff(F*r-2*f+4*Lambda,r)-(r*s.diff(F,r)-F))
k,omega,m=s.symbols('k omega m',real=True)
t=s.symbols('t',real=True)
wave=s.exp(s.I*(k*x-omega*t))
zero('flat_scalar_dispersion',(-s.diff(wave,t,2)+s.diff(wave,x,2)-m**2*wave)/wave-(omega**2-k**2-m**2))
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
                  'checks':checks,'count':len(checks)},indent=2))
