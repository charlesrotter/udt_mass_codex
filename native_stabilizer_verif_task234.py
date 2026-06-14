import sympy as sp

# ============================================================
# Independent verifier for Tasks 2 (Derrick), 3 (EOS / stress),
# 4 (potential total-derivative). Built from the metric + action,
# NOT lifted from the constructor's hedgehog formulas.
# ============================================================
# Metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2
# Coordinates (t,r,theta,phi_az). Hedgehog unit 3-vector:
#   n = (sinT sinth cosp, sinT sinth sinp, cosT),  T=Theta(r).
# This is the deg-1 winding carrier; Theta(r) is the radial twist profile.

t, r, th, p = sp.symbols('t r theta phi_az', real=True)
phi = sp.Function('phi')(r)        # background dilation (general)
c, xi, kappa = sp.symbols('c xi kappa', positive=True)
T = sp.Function('Theta')(r)

coords = (t, r, th, p)

# metric (lower) and inverse
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()
sqrtg = sp.sqrt(sp.simplify(-g.det()))   # = c*e^{0}*r^2 sin th? check
sqrtg = sp.simplify(sqrtg)
print("sqrt(-g) =", sqrtg)

# unit vector
n = sp.Matrix([sp.sin(T)*sp.sin(th)*sp.cos(p),
               sp.sin(T)*sp.sin(th)*sp.sin(p),
               sp.cos(T)])
dn = [sp.Matrix([sp.diff(comp, coords[m]) for comp in n]) for m in range(4)]

# ---- L2 = -(xi/2) g^{mn} d_m n . d_n n  (sign: energy density positive) ----
# kinetic scalar K2 = g^{mn} d_m n.d_n n
K2 = 0
for m in range(4):
    for nn in range(4):
        K2 += gi[m,nn]*(dn[m].T*dn[nn])[0]
K2 = sp.simplify(K2)
print("K2 =", K2)

# ---- L4 native: |omega_H1|^2_g = g^{mp}g^{nq} F_mn F_pq, F_mn = n.(d_m n x d_n n)
def cross(a,b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])
F = [[ (n.T*cross(dn[m], dn[nn]))[0] for nn in range(4)] for m in range(4)]
K4 = 0
for m in range(4):
    for nn in range(4):
        for pp in range(4):
            for qq in range(4):
                K4 += gi[m,pp]*gi[nn,qq]*F[m][nn]*F[pp][qq]
K4 = sp.simplify(K4)
print("K4 (|omega_H1|^2_g) =", K4)

# ============================================================
# TASK 2: Derrick scaling, FLAT background phi=0.
# Energy = integral over static slice of energy density * sqrt(g_spatial).
# Spatial metric (flat phi): dr^2 + r^2 dOmega^2, sqrt = r^2 sin th.
# Energy density(static) = (xi/2)K2_spatial + (kappa/4)K4 with
# proper spatial inverse metric. Build E2(r-integrand), E4(r-integrand),
# then scale Theta(r)->Theta(r/lambda) and read lambda powers.
# ============================================================
lam = sp.symbols('lambda', positive=True)
# evaluate at phi=0
sub0 = {phi: 0}
# spatial kinetic scalar at phi=0: g^{rr}=1, g^{thth}=1/r^2, g^{pp}=1/(r^2 sin^2)
# (drop time row). Recompute spatial-only:
K2_sp = (dn[1].T*dn[1])[0]/1 \
      + (dn[2].T*dn[2])[0]/r**2 \
      + (dn[3].T*dn[3])[0]/(r**2*sp.sin(th)**2)
K2_sp = sp.simplify(K2_sp)
# K4 spatial: only spatial indices; reuse K4 but phi=0 makes time part:
# F_0n involves d_t n = 0 (static) so time drops automatically. set phi=0.
K4_sp = sp.simplify(K4.subs(sub0))
print("K2_sp =", K2_sp)
print("K4_sp =", K4_sp)

# integrate over angles th,p with measure sin th  (full solid angle)
def ang_int(expr):
    e = sp.integrate(expr*sp.sin(th), (th,0,sp.pi))
    e = sp.integrate(e, (p,0,2*sp.pi))
    return sp.simplify(e)

# radial energy densities (per dr), pulling r^2 from volume element
e2_dens = (xi/2)*K2_sp * r**2
e4_dens = (kappa/4)*K4_sp * r**2
E2_rad = ang_int(e2_dens)
E4_rad = ang_int(e4_dens)
print("E2 radial integrand =", sp.simplify(E2_rad))
print("E4 radial integrand =", sp.simplify(E4_rad))

# Derrick: replace Theta(r)->Theta(r/lambda). Equivalent: change variable
# u=r/lambda. For a term ~ Theta'(r)^2 * r^2 : Theta'(r)=Th'(u)/lambda,
# dr=lambda du, r^2=lambda^2 u^2 => integrand scales lambda^{+1}.
# For a term ~ sin^2Theta (no Theta') * r^2: => lambda^{+3}? Let's let sympy
# do it structurally by classifying each monomial.
Thp = sp.Derivative(T, r)
# Substitute scaling explicitly via u-variable bookkeeping:
# We separate E2_rad into pieces with Theta'^2 and without.
E2_exp = sp.expand(E2_rad)
E4_exp = sp.expand(E4_rad)

def derrick_power(expr):
    # expr is integrand in r. Sub r->lambda*u, Theta(r)->Theta(u),
    # Theta'(r)-> (1/lambda) Theta'(u), dr-> lambda du. Return dict pow->coeff.
    u = sp.symbols('u', positive=True)
    Tu = sp.Function('Theta')(u)
    e = expr
    # replace Derivative(Theta(r),r) with Derivative(Theta(u),u)/lambda
    e = e.subs(sp.Derivative(T, r), sp.Derivative(Tu, u)/lam)
    e = e.subs(T, Tu)
    e = e.subs(r, lam*u)
    e = e*lam   # from dr = lambda du
    e = sp.expand(e)
    return e, u

E2s, u = derrick_power(E2_exp)
E4s, u = derrick_power(E4_exp)
print("E2 scaled (collect lambda):", sp.collect(sp.simplify(E2s), lam))
print("E4 scaled (collect lambda):", sp.collect(sp.simplify(E4s), lam))

# ============================================================
# TASK 3: stress tensor via HILBERT variation T_mn = -2/sqrt(-g) dS/dg^{mn}
# For these algebraic-in-g Lagrangians, T^a_b = ... compute p_r+rho.
# Easier robust route: T_mn = -2 dL/dg^{mn} + g_mn L  (L = matter Lagrangian
# density scalar, S=int L sqrt(-g)). Use L = -(xi/2)K2 - (kappa/4)K4 with
# the full (time-included) metric so g^{tt},g^{rr} are independent variables.
# ============================================================
# Treat the inverse-metric diagonal entries as independent symbols.
gtt, grr, gThTh, gPP = sp.symbols('gtt grr gThTh gPP')  # these are g^{mu nu} diag
# Build K2, K4 in terms of these symbols generically:
# d_m n only nonzero for m=r (Theta'), m=theta, m=phi_az. d_t n=0.
dnr, dnth, dnp = dn[1], dn[2], dn[3]
A_rr = (dnr.T*dnr)[0]
A_thth = (dnth.T*dnth)[0]
A_pp = (dnp.T*dnp)[0]
A_rth = (dnr.T*dnth)[0]  # check cross terms (should vanish by symmetry)
K2g = grr*A_rr + gThTh*A_thth + gPP*A_pp + 2*0  # diagonal field grads
# F_mn nonzero spatial pairs: (r,theta),(r,phi),(theta,phi)
Frt = F[1][2]; Frp = F[1][3]; Ftp = F[2][3]
# K4 = g^{mp}g^{nq}F F summed; for diagonal g and antisym F:
# = 2[ grr*gThTh*Frt^2 + grr*gPP*Frp^2 + gThTh*gPP*Ftp^2 ]
K4g = 2*(grr*gThTh*Frt**2 + grr*gPP*Frp**2 + gThTh*gPP*Ftp**2)
Lmat = -(xi/2)*K2g - (kappa/4)*K4g

# T_mn = -2 dL/dg^{mn} + g_mn L. We want mixed T^t_t and T^r_r.
# rho = -T^t_t, p_r = T^r_r.  T^a_b = g^{ac} T_cb.
# Since fields don't depend on g^{tt}, dL/dg^{tt}=0 -> T_tt = g_tt L.
# T^t_t = g^{tt} T_tt = g^{tt} g_tt L = L. So rho = -T^t_t = -L.
rho = -Lmat
# T_rr = -2 dL/dg^{rr} + g_rr L. T^r_r = g^{rr} T_rr = -2 g^{rr} dL/dg^{rr} + L
dL_dgrr = sp.diff(Lmat, grr)
T_r_r = -2*grr*dL_dgrr + Lmat
p_r = T_r_r
prho = sp.simplify(p_r + rho)
print("rho =", sp.simplify(rho))
print("p_r =", sp.simplify(p_r))
print("p_r+rho (in g-symbols) =", prho)

# now substitute back the UDT inverse metric diag values
backsub = {grr: sp.exp(-2*phi), gThTh: 1/r**2, gPP: 1/(r**2*sp.sin(th)**2)}
prho_udt = sp.simplify(prho.subs(backsub))
print("p_r+rho (UDT) =", prho_udt)
# simplify the angular structure: should be e^{-2phi}Theta'^2 (xi + 2 kappa sin^2Theta/r^2)
target = sp.exp(-2*phi)*sp.Derivative(T,r)**2*(xi + 2*kappa*sp.sin(T)**2/r**2)
print("p_r+rho - target =", sp.simplify(prho_udt - target))

# ============================================================
# TASK 4: is the eta transgression Xi=dTheta_form a total derivative =>
# zero bulk EL? Take a generic radial total-derivative Lagrangian density
# L_td = d/dr G(Theta(r), r) and confirm its Euler-Lagrange wrt Theta is 0.
# ============================================================
G = sp.Function('G')
Gfun = G(T, r)
Ltd = sp.diff(Gfun, r)   # total r-derivative
# EL operator for L(Theta,Theta',r): dL/dTheta - d/dr(dL/dTheta')
ThetaP = sp.Derivative(T, r)
dL_dTheta = sp.diff(Ltd, T)
dL_dThetaP = sp.diff(Ltd, ThetaP)
EL = sp.simplify(dL_dTheta - sp.diff(dL_dThetaP, r))
print("Task4: EL[ d/dr G(Theta,r) ] =", EL)
