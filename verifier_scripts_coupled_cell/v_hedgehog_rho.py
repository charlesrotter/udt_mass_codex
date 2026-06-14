import sympy as sp

r, theta, phi_f, xi, rs, delta, rc, ri, p, lam = sp.symbols(
    'r theta phi xi rs delta r_core r_int p lambda', positive=True, real=True)
phi = sp.Function('phi')

# ---- Independent stress-energy from the angular hedgehog n = x/r ----
# minimal L = -(xi/2) g^{mn} d_m n_a d_n n_a, n unit hedgehog.
# For a unit hedgehog n=(sin th cos ph, sin th sin ph, cos th) (i.e. Theta=theta),
# d n_a d n^a over the unit 2-sphere = |grad n|^2.
# In flat-ish coords with metric e^{2phi}dr^2 + r^2 dOmega^2:
# the hedgehog gradient energy density (the angular-only piece) ~ 1/r^2.
# Let me derive rho directly from T_mn = xi[ d_m n.d_n n - (1/2) g_mn (dn)^2 ].

# n components in cartesian-from-spherical, Theta=theta (pure hedgehog):
nth = sp.Matrix([sp.sin(theta)*sp.cos(sp.Symbol('ph')),
                 sp.sin(theta)*sp.sin(sp.Symbol('ph')),
                 sp.cos(theta)])
ph = sp.Symbol('ph')
# grad over angular metric: g^{th th}=1/r^2, g^{ph ph}=1/(r^2 sin^2 th)
dn_th = nth.diff(theta)
dn_ph = nth.diff(ph)
grad2 = (dn_th.dot(dn_th))/r**2 + (dn_ph.dot(dn_ph))/(r**2*sp.sin(theta)**2)
grad2 = sp.simplify(grad2)
print("dn.dn (g^ab d_a n . d_b n) =", grad2, "  -> times r^2 =", sp.simplify(grad2*r**2))

# (dn)^2 = grad2 ; energy density rho = T^t_t with -(1/2)g term:
# T_tt: rho = (xi/2)*grad2  (kinetic-free static => Lagrangian density = -(xi/2)grad2,
# T^t_t = -rho). Standard sigma-model: rho = (xi/2)*grad2.
rho = sp.simplify((xi/2)*grad2)
print("rho =", rho)
# radial pressure p_r = T^r_r. For pure angular field, T^r_r = -(xi/2)grad2 = -rho
print("p_r = -rho exact? rho*r^2 =", sp.simplify(rho*r**2))
