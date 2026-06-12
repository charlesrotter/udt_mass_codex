import sympy as sp

# Scalar cross-check: a CANONICAL scalar psi(r) on this metric.
# Stress tensor T_{mu nu} = d_mu psi d_nu psi - g_{mu nu}(1/2 (dpsi)^2)  (massless canonical)
# psi = psi(r) only.
phi, r, th = sp.symbols('phi r theta', real=True)
psi = sp.Function('psi')(r)

g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# (dpsi)^2 = g^{mu nu} d_mu psi d_nu psi = g^{rr} psi'^2
dpsi2 = ginv[1,1]*sp.diff(psi,r)**2
dpsi2 = sp.simplify(dpsi2)
print("(dpsi)^2 = g^rr psi'^2 =", dpsi2)

# T_{mu nu} = d_mu psi d_nu psi - g_{mu nu} (1/2)(dpsi)^2
def dmu(mu):
    return sp.diff(psi,r) if mu==1 else 0
T_low = sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        T_low[mu,nu] = dmu(mu)*dmu(nu) - g[mu,nu]*sp.Rational(1,2)*dpsi2

# Mixed T^mu_nu = g^{mu a} T_{a nu}
T_mix = sp.simplify(ginv*T_low)
Ttt = sp.simplify(T_mix[0,0]); Trr = sp.simplify(T_mix[1,1])
print("T^t_t =", Ttt)
print("T^r_r =", Trr)
diff = sp.simplify(Trr - Ttt)
print("T^r_r - T^t_t =", diff)
phir = sp.Function('phi')(r)  # just for display
print("claimed: -e^{-2phi} psi'^2 =", sp.simplify(-sp.exp(-2*phi)*sp.diff(psi,r)**2))
print("MATCH:", sp.simplify(diff - (-sp.exp(-2*phi)*sp.diff(psi,r)**2))==0)
