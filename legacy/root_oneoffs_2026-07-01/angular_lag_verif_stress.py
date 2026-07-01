import sympy as sp
# Independent stress-tensor derivation, UDT metric, hedgehog n-field.
t,r,th,ph,c,xi = sp.symbols('t r theta phi c xi', positive=True)
phi = sp.Function('phi')(r)
# metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords=[t,r,th,ph]
sqrtg = sp.sqrt(-g.det())
print("sqrt(-g):", sp.simplify(sqrtg))   # expect c r^2 sin th (phi cancels)

# hedgehog n = (sin th cos ph, sin th sin ph, cos th), Theta=theta
n = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
# d_mu n_a
dn = sp.Matrix([[sp.diff(n[a],coords[mu]) for a in range(3)] for mu in range(4)])  # 4x3
# X = g^{mu nu} dn_mu . dn_nu
X = 0
for mu in range(4):
    for nu in range(4):
        X += ginv[mu,nu]*sum(dn[mu,a]*dn[nu,a] for a in range(3))
X = sp.simplify(X)
print("X = g^{mn} dn.dn (expect 2/r^2):", X)

# L = -(xi/2) X ;  T_{mn} = xi dn_m.dn_n + g_{mn} L
L = -sp.Rational(1,2)*xi*X
Tdd = sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Tdd[mu,nu] = xi*sum(dn[mu,a]*dn[nu,a] for a in range(3)) + g[mu,nu]*L
# raise one index: T^mu_nu = g^{mu al} T_{al nu}
Tud = sp.simplify(ginv*Tdd)
print("\nT^mu_nu (mixed):")
for i,nm in enumerate(['t','r','th','ph']):
    print(f"  T^{nm}_{nm} =", sp.simplify(Tud[i,i]))
print("\nT^t_t - T^r_r (expect 0):", sp.simplify(Tud[0,0]-Tud[1,1]))
rho = -Tud[0,0]; pr = Tud[1,1]
print("p_r + rho (expect 0):", sp.simplify(pr+rho))
