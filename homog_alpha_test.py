import sympy as sp
import numpy as np

# ------------------------------------------------------------------
# Augmented dilation equation:
#   Z (rho^2 phi')' = 4 e^{-2phi} rho'^2 + alpha * xi * e^{alpha phi} * rho^2 * I_r
# with xi=1, I_r>=0.  Solve for required I_r given a geometry (phi,rho).
#   I_r = [ Z (rho^2 phi')' - 4 e^{-2phi} rho'^2 ] / ( alpha * e^{alpha phi} * rho^2 )
# ------------------------------------------------------------------

r, k, Z, alpha = sp.symbols('r k Z alpha', positive=False, real=True)
k_p, Z_p = sp.symbols('k Z', positive=True)

# de Sitter static patch: rho = r, phi = -1/2 ln(1 - k r^2)
rho = r
phi = -sp.Rational(1,2)*sp.log(1 - k*r**2)

phip = sp.diff(phi, r)
rhop = sp.diff(rho, r)
lhs_inner = rho**2 * phip
lhs = Z * sp.diff(lhs_inner, r)          # Z (rho^2 phi')'
src_free = 4 * sp.exp(-2*phi) * rhop**2  # 4 e^{-2phi} rho'^2

# RESIDUAL R = Z(rho^2 phi')' - 4 e^{-2phi} rho'^2   (independent of alpha)
R = sp.simplify(lhs - src_free)
print("=== de Sitter residual R(r) = Z(rho^2 phi')' - 4 e^{-2phi} rho'^2 ===")
print("R =", R)

# required I_r
weight = alpha * sp.exp(alpha*phi) * rho**2   # alpha * e^{alpha phi} * rho^2
I_req = sp.simplify(R / weight)
print("\n=== required I_r(r) ===")
print("I_r =", I_req)

# limits
print("\nR at r->0 :", sp.limit(R, r, 0))
print("R -> horizon (r->1/sqrt(k), k>0): behaviour of first term is +inf")
Rk = R.subs(k, k_p).subs(Z, Z_p)
print("R(r) simplified (k,Z>0):", sp.simplify(Rk))

# ------------------------------------------------------------------
# Numeric: sign & profile of required I_r for alpha<0, sweep k,Z
# ------------------------------------------------------------------
def resid(rv, kv, Zv):
    return Zv * kv*rv**2*(3 - kv*rv**2)/(1 - kv*rv**2)**2 - 4*(1 - kv*rv**2)

def I_required(rv, kv, Zv, av):
    Rv = resid(rv, kv, Zv)
    w = av * (1 - kv*rv**2)**(-av/2.0) * rv**2
    return Rv / w

print("\n\n=== NUMERIC required I_r(r) for de Sitter, alpha<0 ===")
for kv in [0.5, 1.0, 2.0]:
    for Zv in [1.0, 8.0]:
        for av in [-2.0, -1.0, -0.5]:
            rs = np.linspace(0.05, 0.98/np.sqrt(kv), 60)
            Iv = np.array([I_required(rr, kv, Zv, av) for rr in rs])
            Rv = np.array([resid(rr, kv, Zv) for rr in rs])
            neg = np.any(Iv < 0)
            # where does R (hence sign) flip
            sflip = np.where(np.diff(np.sign(Rv)) != 0)[0]
            rflip = rs[sflip[0]] if len(sflip) else None
            const_test = (Iv.max()-Iv.min())/max(abs(Iv).max(),1e-30)
            print(f"k={kv} Z={Zv} a={av}: I_r range [{Iv.min():.3g},{Iv.max():.3g}] "
                  f"negative-somewhere={neg} R-signflip@r={None if rflip is None else round(rflip,3)} "
                  f"(horizon={0.98/np.sqrt(kv):.3f}) rel-variation={const_test:.2f}")
