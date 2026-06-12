import sympy as sp
r, th = sp.symbols('r theta', positive=True)
Qf, mu = sp.symbols('Q_f mu', positive=True)
f = sp.Function('f', positive=True)(r, th)
q = sp.Function('q', real=True)(r, th)
v = sp.Function('v', positive=True)(r, th)   # v = 1 + w > 0
Wfac = v**2
D2 = r**2*Wfac - f*q**2
sqrtmg = r*sp.sin(th)*sp.sqrt(D2)/v
print("sqrt(-g) at q=0:", sp.simplify(sqrtmg.subs(q,0)))
g = sp.Matrix([[-f,0,0,0],[0,1/f,q,0],[0,q,r**2*Wfac,0],[0,0,0,r**2*sp.sin(th)**2/Wfac]])
ginv = g.inv()
F_low = sp.zeros(4,4); F_low[2,3] = Qf*sp.sin(th); F_low[3,2] = -Qf*sp.sin(th)
F_up = ginv*F_low*ginv
F2 = sp.simplify(sum(F_low[i,j]*F_up[i,j] for i in range(4) for j in range(4)))
L_flux = sp.simplify(-(sp.Rational(1,4)/mu)*sqrtmg*F2)
print("L_flux:", L_flux)
print("L_flux q=0:", sp.simplify(L_flux.subs(q,0)))
wtad = sp.simplify(sp.diff(L_flux, v))
target = (Qf**2/(2*mu))*sp.sin(th)*f*q**2*v/D2**sp.Rational(3,2)
print("tadpole residual:", sp.simplify(wtad - target))
