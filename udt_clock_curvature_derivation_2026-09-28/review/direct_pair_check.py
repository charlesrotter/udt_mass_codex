#!/usr/bin/env python3
"""Extend reviewer coordinate implementation to the frozen candidate's new joins."""
import json
import sympy as s
import source_first_coordinate_check as base
t,x,N,L,b=base.t,base.x,base.N,base.L,base.b
D0,D1,a,H=base.D0,base.D1,base.a,base.H
Bplus=H+a;Bminus=H-a
identity=D0(Bplus)-D1(Bplus)+D0(Bminus)+D1(Bminus)+2*Bplus*Bminus-base.scalar
assert s.cancel(identity)==0

u=s.Matrix([1/N,0]);n=s.Matrix([-b/L,1/L])
checks=[]
for eps in (1,-1):
    ell=u+eps*n
    acc=s.Matrix([sum(ell[c]*s.diff(ell[i],base.coords[c]) for c in range(2))
        +sum(base.Gamma[i][c][d]*ell[c]*ell[d] for c in range(2) for d in range(2)) for i in range(2)])
    residual=(acc-(H+eps*a)*ell).applyfunc(s.cancel)
    assert residual==s.zeros(2,1)
    checks.append({'epsilon':eps,'null_nonaffinity_components':2,'residual':'0 identically'})

F=s.Function('F')(t,x)
restricted=s.cancel(base.scalar.subs({N:1/s.sqrt(F),L:s.sqrt(F),b:0}).doit())
target=s.diff(F,t,2)-s.diff(1/F,x,2)
assert s.cancel(restricted-target)==0
f=s.Function('f')(t,x)
F0,eps=s.symbols('F0 eps',positive=True)
linearized=s.diff(target.subs(F,F0+eps*f).doit(),eps).subs(eps,0)
assert s.cancel(linearized-s.diff(f,t,2)-s.diff(f,x,2)/F0**2)==0
k=s.symbols('k',nonzero=True,real=True)
good=s.cos(k*x)*s.cosh(k*t/F0)
bad=s.cos(k*x)*s.cos(k*t/F0)
op=lambda q:s.diff(q,t,2)+s.diff(q,x,2)/F0**2
assert s.simplify(op(good))==0
assert s.simplify(op(bad).subs({t:0,x:0}))==-2*k**2/F0**2

shift_scalar=s.cancel(base.scalar.subs({N:1,L:1,b:t}).doit())
measure_scalar=s.simplify(base.scalar.subs({N:1,L:s.exp(t),b:0}).doit())
assert shift_scalar==-2 and measure_scalar==2
wrong_a=D1(s.log(N))
wrong_shift=2*(D0(H)+H**2-D1(wrong_a)-wrong_a**2)
assert s.cancel(wrong_shift.subs({N:1,L:1,b:t}).doit())!=shift_scalar
wrong_H=D0(-s.log(N))
wrong_measure=2*(D0(wrong_H)+wrong_H**2-D1(a)-a**2)
assert s.simplify(wrong_measure.subs({N:1,L:s.exp(t),b:0}).doit())!=measure_scalar

print(json.dumps({'bidirectional_interlock_residual':'0 identically','both_directions':checks,
    'restricted_F_equation_residual':'0 identically','linearized_principal_part':'f_tt + F0^-2 f_xx',
    'ellipticity_domain':'F>0; prescribed derivative-free curvature; not a UDT-wide dynamical statement',
    'actual_rejections':['omit shift time derivative','omit measure time derivative','wrong-sign hyperbolic linearized mode'],
    'controls':{'shift_scalar':str(shift_scalar),'time_measure_scalar':str(measure_scalar)},
    'author_code_exposure':False,'reuse':'source-first reviewer coordinate implementation, not author code'},indent=2))
