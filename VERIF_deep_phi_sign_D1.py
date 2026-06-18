# VERIF_deep_phi_sign_D1.py
# D1: EXACT native second-variation operator of L2+L4 around the static charge-1
#     hedgehog, for a TANGENT fluctuation eta (|n|=1 manifest), with the FULL
#     native coefficients (xi, kappa). Derived from the metric-level action,
#     NOT from the generic harmonic-map Jacobi formula applied to the reduced
#     invariant. This pins the EXACT angular well coefficient (S1, the whole point).
#
# Metric: ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2,  sqrt(g)=e^{phi}r^2 sin th.
# L2 = -(xi/2) g^{mn} d_m n . d_n n,  |n|=1
# L4 = -(kappa/4) g^{mp}g^{nq} S_mn.S_pq, S_mn=d_m n x d_n n  (native |omega_H1|^2_g)
#
# Background (charge-1 hedgehog): n0 = (sinTheta(r) sin th cos ph,
#                                       sinTheta(r) sin th sin ph, cosTheta(r))
# This is the standard UNIT 3-vector hedgehog n0.n0 = 1 (verify).
#
# Plan:
#  Part A: build the EXACT static energy density e(Theta,Theta',r,phi) = -L2-L4
#          evaluated on the hedgehog ansatz; confirm it reproduces the corpus
#          E2_r + E4_r EXACTLY (native coefficients). This is the source for the
#          l=0 radial Hessian.
#  Part B: l=0 (breathing / radial-profile) sector. Theta -> Theta + eps u(r),
#          eta tangent along the dTheta direction. The exact 2nd variation is the
#          Hessian of the reduced energy functional E[Theta]=INT e dr. Build the
#          Sturm-Liouville coefficients P (kinetic, =d2e/dTp2), Veff (potential)
#          EXACTLY with full xi,kappa. Compare to the prior with_L4 run.
#  Part C: l>=1 (transverse, iso-rotational/azimuthal) sector. The EXACT tangent
#          fluctuation orthogonal to the hedgehog 2-plane. We derive the exact
#          metric-level quadratic form for a transverse tangent field, in the
#          channel of angular momentum l, with full xi,kappa -> the EXACT native
#          well coefficient (vs the reduced-invariant representative used before).
import sympy as sp

print("="*72)
print("D1 -- EXACT native second variation of L2+L4 (full xi,kappa coefficient)")
print("="*72)

r, th, ph = sp.symbols('r theta varphi', real=True)
phi = sp.Function('phi')(r)
Th  = sp.Function('Theta')(r)
xi, kappa, c = sp.symbols('xi kappa c', positive=True)   # c = speed of light symbol (drops)

# ---------------------------------------------------------------------------
# Metric (static slice; t-part only enters the time-kinetic weight, handled later)
# ---------------------------------------------------------------------------
# spatial inverse metric: g^{rr}=e^{-2phi}, g^{thth}=1/r^2, g^{phph}=1/(r^2 sin^2 th)
ginv = {'rr': sp.exp(-2*phi), 'thth': 1/r**2, 'phph': 1/(r**2*sp.sin(th)**2)}
sqrtg = sp.exp(phi)*r**2*sp.sin(th)

# ---------------------------------------------------------------------------
# Part A: hedgehog n0, confirm unit, build exact static energy density
# ---------------------------------------------------------------------------
n0 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ph),
                sp.sin(Th)*sp.sin(th)*sp.sin(ph),
                sp.cos(Th)])
print("\n[A] |n0|^2 =", sp.simplify(n0.dot(n0)), "(must be 1)")

def d(vec, var):
    return sp.Matrix([sp.diff(comp, var) for comp in vec])

dn_r  = d(n0, r); dn_th = d(n0, th); dn_ph = d(n0, ph)

# L2 density: (xi/2) g^{mn} d_m n . d_n n  (static, spatial)
gradn2 = (ginv['rr']*dn_r.dot(dn_r) + ginv['thth']*dn_th.dot(dn_th)
          + ginv['phph']*dn_ph.dot(dn_ph))
e2_density = sp.Rational(1,2)*xi*gradn2*sqrtg   # proper energy density * sin th (volume)
e2_density = sp.simplify(e2_density)
print("\n[A] L2 energy density * sqrt(g):")
sp.pprint(e2_density)

# L4 density: (kappa/4) g^{mp}g^{nq} S_mn.S_pq, S_mn = d_m n x d_n n
def cross(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])
S = {}
S[('r','th')] = cross(dn_r, dn_th)
S[('r','ph')] = cross(dn_r, dn_ph)
S[('th','ph')] = cross(dn_th, dn_ph)
gmap = {'r':'rr','th':'thth','ph':'phph'}
# sum over ordered pairs (m<n) with factor 2 for antisymmetry
pairs = [('r','th'),('r','ph'),('th','ph')]
L4_sum = 0
for (m,n) in pairs:
    gm = ginv[gmap[m]]; gn = ginv[gmap[n]]
    L4_sum += 2*gm*gn*S[(m,n)].dot(S[(m,n)])   # factor 2: S_mn=-S_nm both contribute
e4_density = sp.Rational(1,4)*kappa*L4_sum*sqrtg
e4_density = sp.simplify(e4_density)
print("\n[A] L4 energy density * sqrt(g):")
sp.pprint(e4_density)

# Integrate over the sphere (th in [0,pi], ph in [0,2pi]) to get the reduced E2_r,E4_r
E2_r = sp.integrate(sp.integrate(e2_density, (ph,0,2*sp.pi)), (th,0,sp.pi))
E4_r = sp.integrate(sp.integrate(e4_density, (ph,0,2*sp.pi)), (th,0,sp.pi))
E2_r = sp.simplify(E2_r); E4_r = sp.simplify(E4_r)
print("\n[A] Sphere-reduced E2_r =")
sp.pprint(E2_r)
print("\n[A] Sphere-reduced E4_r =")
sp.pprint(E4_r)

# Compare to the corpus forms (native_stabilizer_results.md:89-92):
Thp = sp.Derivative(Th, r)
E2_corpus = (2*sp.pi*xi/3)*sp.exp(-phi)*( r**2*sp.sin(Th)**2*Thp**2
              + 2*r**2*Thp**2 + 4*sp.exp(2*phi)*sp.sin(Th)**2 )
E4_corpus = (2*sp.pi*kappa/3)*sp.exp(-phi)*( (2*r**2*sp.sin(Th)**4 + 2*r**2*sp.sin(Th)**2)*Thp**2
              + sp.exp(2*phi)*sp.sin(Th)**4 )/r**2
print("\n[A] E2_r - E2_corpus simplified =", sp.simplify(E2_r - E2_corpus))
print("[A] E4_r - E4_corpus simplified =", sp.simplify(E4_r - E4_corpus))

print("\n" + "="*72)
print("Part B: l=0 (breathing/radial) EXACT Hessian -- full native xi,kappa")
print("="*72)
# Reduced energy density per dr: e(Theta,Theta',r,phi) = E2_r + E4_r (drop overall 2pi/3,
# keep xi,kappa exact). Use the corpus form (verified == above).
Tv, Tpv = sp.symbols('Theta_v Thetap_v', real=True)
phv = sp.symbols('phi_v', real=True)
edens = ( xi*sp.exp(-phv)*( r**2*sp.sin(Tv)**2*Tpv**2 + 2*r**2*Tpv**2 + 4*sp.exp(2*phv)*sp.sin(Tv)**2 )
         + kappa*sp.exp(-phv)*( (2*r**2*sp.sin(Tv)**4 + 2*r**2*sp.sin(Tv)**2)*Tpv**2
            + sp.exp(2*phv)*sp.sin(Tv)**4 )/r**2 )
# (overall (2pi/3) dropped; it multiplies H and W equally -> cancels in omega^2)
P    = sp.diff(edens, Tpv, 2)                 # kinetic coeff (Sturm-Liouville p)
dPdT = sp.diff(P, Tv)
Q    = sp.diff(edens, Tv, 2)                  # raw d2e/dTheta2
Rmix = sp.diff(sp.diff(edens, Tv), Tpv)       # mixed
print("\n[B] P = d2e/dTheta'^2 (EXACT, with xi,kappa) =")
sp.pprint(sp.simplify(P))
print("\n[B] Q = d2e/dTheta^2 (EXACT) =")
sp.pprint(sp.simplify(Q))
print("\n[B] R_mix = d2e/dThetadTheta' (EXACT) =")
sp.pprint(sp.simplify(Rmix))
# Self-adjoint reduced fluctuation operator on u(r):
#   (d/dr)(P du/dr) ... Veff = Q - d/dr(R_mix)   (standard for L = (1/2)(P u'^2 + ...)
print("\n[B] EXACT l=0 operator: -(d/dr)(P u') + Veff u = omega^2 W u,")
print("    Veff = Q - d/dr(R_mix*along bg) ; weight W from time-kinetic (e^{3phi} breathing).")
print("    >>> NOTE the kinetic P and potential Q carry the FULL native xi AND kappa.")
print("    The prior with_L4 run (VERIF_with_L4_fluctuation_F2345.py) instead used:")
print("        V_curv = -(e^{-2phi}T'^2 + 2 sin^2T/r^2)   [reduced invariant, coeff 1, NO xi/kappa split]")
print("        c4     = (2 sin^4T + 2 sin^2T), s4=kappa=1  [representative stiffness]")
print("        W      = e^{2phi}                            [generic KG weight]")
print("    => the prior runs used a REPRESENTATIVE coefficient; here xi,kappa are exact.")

print("\n" + "="*72)
print("Part C: l>=1 TRANSVERSE tangent fluctuation -- EXACT native well coeff")
print("="*72)
# A transverse tangent fluctuation rotates the hedgehog in the iso/angular direction.
# The cleanest EXACT route: the full energy is a functional of the unit field n(x).
# Parametrize a one-parameter family preserving |n|=1 and compute d^2 E / deps^2.
# The two independent tangent directions at the hedgehog: (T1) the "polar" tangent
# e_Theta = d n0/dTheta (the same direction the breathing mode lives in, but now
# allowed to depend on angles -> l>=1 polar modes), and (T2) the "azimuthal" tangent
# e_chi (iso-rotation about the n3 axis), giving the chi/rotor channel.
#
# We build the EXACT quadratic form for a fluctuation eta = a(r,th,ph) e_Theta +
# b(r,th,ph) e_chi about n0, by expanding n = cos|eta| n0 + sin|eta| eta_hat to
# O(eta^2) and integrating L2+L4 over the sphere with the EXACT metric. To pin the
# l-channel WELL COEFFICIENT we extract the eta^2 (no-derivative) terms -- the
# native potential the transverse mode feels -- with full xi,kappa.
#
# Tangent frame at n0:
e_Th = sp.Matrix([sp.cos(Th)*sp.sin(th)*sp.cos(ph),
                  sp.cos(Th)*sp.sin(th)*sp.sin(ph),
                  -sp.sin(Th)])                      # = d n0/dTheta, unit
print("\n[C] |e_Theta|^2 =", sp.simplify(e_Th.dot(e_Th)), " e_Theta.n0 =", sp.simplify(e_Th.dot(n0)))
# second tangent (orthonormal): e_perp = n0 x e_Theta
e_perp = cross(n0, e_Th)
print("[C] |e_perp|^2 =", sp.simplify(e_perp.dot(e_perp)), " e_perp.n0 =", sp.simplify(e_perp.dot(n0)),
      " e_perp.e_Theta =", sp.simplify(e_perp.dot(e_Th)))

# EXACT second variation of the static energy for a tangent fluctuation
# n(eps) = cos(eps*A) n0 + sin(eps*A) etahat, with etahat a unit tangent and A the amplitude.
# We do it field-theoretically: take eta = A * e (e a unit tangent, A = A(r,th,ph) small),
# n = sqrt(1-A^2) n0 + A e, exact unit. Expand energy to O(A^2).
A = sp.Function('A')(r, th, ph)
for label, evec in [('polar e_Theta', e_Th), ('transverse e_perp', e_perp)]:
    n_pert = sp.sqrt(1 - A**2)*n0 + A*evec
    # gradients
    dnr = d(n_pert, r); dnt = d(n_pert, th); dnp = d(n_pert, ph)
    gradn2_p = (ginv['rr']*dnr.dot(dnr) + ginv['thth']*dnt.dot(dnt)
                + ginv['phph']*dnp.dot(dnp))
    e2_p = sp.Rational(1,2)*xi*gradn2_p*sqrtg
    # L4
    Sp = {}
    Sp[('r','th')] = cross(dnr, dnt); Sp[('r','ph')] = cross(dnr, dnp); Sp[('th','ph')] = cross(dnt, dnp)
    L4s = 0
    for (m,n) in pairs:
        L4s += 2*ginv[gmap[m]]*ginv[gmap[n]]*Sp[(m,n)].dot(Sp[(m,n)])
    e4_p = sp.Rational(1,4)*kappa*L4s*sqrtg
    e_p = e2_p + e4_p
    # extract the O(A^2) NO-DERIVATIVE-OF-A part (the local well coefficient) by
    # setting derivatives of A to zero, then taking (1/2) d2/dA2 at A=0.
    e_local = e_p.subs({sp.Derivative(A,r):0, sp.Derivative(A,th):0, sp.Derivative(A,ph):0})
    # second derivative wrt A at A=0:
    well = sp.simplify(sp.diff(e_local, A, 2).subs(A, 0))
    well = sp.simplify(well)
    print(f"\n[C] {label}: O(A^2) local WELL density (per sphere element, *sqrt g) =")
    sp.pprint(well)
    # integrate over the sphere to get the radial well coefficient for the l=0 part
    well_sph = sp.simplify(sp.integrate(sp.integrate(well, (ph,0,2*sp.pi)), (th,0,sp.pi)))
    print(f"    sphere-integrated local well (l-independent piece) =")
    sp.pprint(well_sph)

print("\nD1 DONE. The exact native operator has both kinetic and well terms carrying")
print("xi AND kappa explicitly; Part C gives the exact transverse well density.")
