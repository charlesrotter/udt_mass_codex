import sympy as sp
t,r,c,xi = sp.symbols('t r c xi', positive=True)
th,ph = sp.symbols('theta phi')
phi = sp.Function('phi')(r)
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv=g.inv(); coords=[t,r,th,ph]

def stress(n):
    dn=sp.Matrix([[sp.diff(n[a],coords[mu]) for a in range(3)] for mu in range(4)])
    X=sum(ginv[mu,nu]*sum(dn[mu,a]*dn[nu,a] for a in range(3)) for mu in range(4) for nu in range(4))
    X=sp.simplify(X)
    Lg=-sp.Rational(1,2)*xi*X
    Tdd=sp.zeros(4,4)
    for mu in range(4):
        for nu in range(4):
            Tdd[mu,nu]=xi*sum(dn[mu,a]*dn[nu,a] for a in range(3))+g[mu,nu]*Lg
    Tud=sp.simplify(ginv*Tdd)
    return Tud,X

# C2: radial twist Theta=Theta(r)
Th=sp.Function('Theta')(r)
n2=sp.Matrix([sp.sin(Th)*sp.cos(ph), sp.sin(Th)*sp.sin(ph), sp.cos(Th)])
T2,X2=stress(n2)
rho=-T2[0,0]; pr=T2[1,1]
print("C2 radial twist Theta(r): p_r+rho =", sp.simplify(pr+rho))
print("   T^th_th =", sp.simplify(T2[2,2]))

# Adversarial: a NON-hedgehog purely-angular config, e.g. winding number w in phi
w=sp.Integer(2)
n3=sp.Matrix([sp.sin(th)*sp.cos(w*ph), sp.sin(th)*sp.sin(w*ph), sp.cos(th)])
T3,X3=stress(n3)
print("\nNON-hedgehog (phi-winding w=2), purely angular: T^t_t-T^r_r =", sp.simplify(T3[0,0]-T3[1,1]))
print("   p_r+rho =", sp.simplify(T3[1,1]-T3[0,0]), " T^th_th=",sp.simplify(T3[2,2]),"T^ph_ph=",sp.simplify(T3[3,3]))

# Adversarial: purely-angular but theta-distorted Theta=g(theta) (no r-dep)
gth=sp.Function('g')(th)
n4=sp.Matrix([sp.sin(gth)*sp.cos(ph), sp.sin(gth)*sp.sin(ph), sp.cos(gth)])
T4,X4=stress(n4)
print("\nTheta=g(theta) purely angular: T^t_t-T^r_r =", sp.simplify(T4[0,0]-T4[1,1]))
print("   p_r+rho =", sp.simplify(T4[1,1]-T4[0,0]))
