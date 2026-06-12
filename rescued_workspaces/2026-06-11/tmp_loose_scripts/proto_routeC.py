import sympy as sp
c, ph = sp.symbols('c phi', real=True)
kap = sp.Symbol('kappa', positive=True)
F = sp.Symbol('F', positive=True)
Y = {}
Y['u']  = sp.S(1)
Y['a0'] = sp.sqrt(sp.S(3)/(4*sp.pi))*c
Y['a1'] = sp.sqrt(sp.S(3)/(4*sp.pi))*sp.sqrt(1-c**2)*sp.cos(ph)
Y['g0'] = sp.sqrt(sp.S(5)/(16*sp.pi))*(3*c**2-1)
Y['g1'] = sp.sqrt(sp.S(15)/(4*sp.pi))*c*sp.sqrt(1-c**2)*sp.cos(ph)
B = F*(1+kap*c)
def grad_dot(g,h):
    return (1-c**2)*sp.diff(g,c)*sp.diff(h,c) + sp.diff(g,ph)*sp.diff(h,ph)/(1-c**2)
def Hij_okap(i,j):
    Yi,Yj = Y[i],Y[j]
    integ = (2*grad_dot(Yi,Yj)/B
             - 2*F*kap*(1-c**2)*(sp.diff(Yi,c)*Yj+sp.diff(Yj,c)*Yi)/B**2
             + 2*(1-c**2)*F**2*kap**2*Yi*Yj/B**3)
    integ = sp.series(sp.expand(integ), kap, 0, 2).removeO()
    integ = sp.expand_trig(sp.expand(integ))
    val = sp.integrate(sp.integrate(integ,(ph,0,2*sp.pi)),(c,-1,1))
    return sp.Rational(1,4)*sp.simplify(val)
print("H[a1,g1] O(kap):", Hij_okap('a1','g1'))
print("H[a0,g0] O(kap):", Hij_okap('a0','g0'))
