import sympy as sp

# Exterior (T=0), phi=const=0 (leading window geometry), W_chi=1, e^{-phi}=1, phi'=0.
# E^{AB} = 1/2 h^{AB}𝒦 - 2 K^{AC}K_C^B + 2 K K^{AB} - d_r pi^{AB},
#          pi^{AB}=sqrt(h)(K^{AB}-K h^{AB}),  K_AB=1/2 d_r h_AB.
# Background round h=diag(r^2, r^2 sin^2). Diagonal TRACELESS perturbation:
#   h_thth = r^2 (1+eps*u(r)*P),  h_psps = r^2 sin^2 (1-eps*u(r)*P)
r, th, eps = sp.symbols('r theta eps', positive=True)
P = sp.symbols('P')  # angular profile value (algebraic, no angular derivatives enter E^{AB})
u = sp.Function('u')

def build(hthth, hpsps):
    h = sp.Matrix([[hthth,0],[0,hpsps]])
    hinv = h.inv()
    sqh = sp.sqrt(h.det())
    Klow = sp.Rational(1,2)*sp.diff(h,r)
    Kmix = hinv*Klow
    Kup  = hinv*Klow*hinv
    Ktr  = sp.trace(Kmix)
    KK = sum(Kup[i,j]*Klow[i,j] for i in range(2) for j in range(2))
    Kcurl = KK - Ktr**2
    # K^{AC}K_C^B  (upper-mixed) -> component [A][B] = sum_C Kup[A,C]*Klow?? need K^{AC} K_C^B
    KACKCB = Kup*Klow*hinv  # (K^{AC})(K_C{}^B): Kup is K^{AC}, Kmix is K_C^B ; product Kup*Kmix
    KACKCB = Kup*Kmix
    piAB = sqh*(Kup - Ktr*hinv)
    return h,hinv,sqh,Kcurl,Ktr,Kup,KACKCB,piAB

# perturbed
hthth = r**2*(1+eps*u(r)*P)
hpsps = r**2*sp.sin(th)**2*(1-eps*u(r)*P)
h,hinv,sqh,Kcurl,Ktr,Kup,KACKCB,piAB = build(hthth,hpsps)

# E^{thth}
dpiAB = sp.diff(piAB, r)
E = sp.Rational(1,2)*hinv*Kcurl - 2*KACKCB + 2*Ktr*Kup - dpiAB
Ethth = E[0,0]
# linearize in eps
Ethth_lin = sp.series(Ethth, eps, 0, 2).removeO()
E0 = Ethth_lin.subs(eps,0)
E1 = sp.simplify(sp.diff(Ethth_lin, eps).subs(eps,0))
print("background E^{thth} (should be 0 for round vacuum):", sp.simplify(E0))
print()
print("O(eps) coefficient of E^{thth} (=0 is the shear eq):")
E1s = sp.simplify(E1)
print(E1s)
# strip common factor, get radial ODE in u
# collect as polynomial in r; expect form  c2 u'' + c1 u'/r + c0 u/r^2  times P
E1s2 = sp.simplify(E1s/P)
print()
print("divided by P:", E1s2)
# indicial: substitute u=r^n
n = sp.symbols('n')
ind = sp.simplify(E1s2.subs(u(r), r**n).doit())
ind = sp.simplify(ind * r**(2-n) )  # normalize
print()
print("indicial expression (u=r^n), normalized:", sp.expand(ind))
sol = sp.solve(sp.Eq(ind,0), n)
print("indicial roots n =", sol)
