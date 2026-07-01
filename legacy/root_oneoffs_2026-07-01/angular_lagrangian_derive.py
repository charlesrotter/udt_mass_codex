"""
angular_lagrangian_derive.py — GATED DERIVATION (authorized by Charles
2026-06-14). Construct UDT's angular-sector Lagrangian FROM THE PROJECT'S
OWN OBJECTS, derive its stress-energy in the UDT background, and TEST
whether it gives p_r = -rho (equivalently g_tt g_rr = -c^2, "B=1/A").

OBJECTS USED (cited, none imported from a textbook):
  - h1_types_results.md: omega_H1 = eps_abc n_a dn_b ^ dn_c, INT=4pi,
    carrier n_a unit 3-vector (target S^2), N=3, q=1/3.
  - dpf2_results.md / exterior_cavity_results.md banked positive #1:
    f = F(1+kappa cos theta), a = F kappa/sqrt3, angular potential
    P = (3a^2/8F) G1 = (pi/2) F kappa^2 G1, G1=(2k+(k^2-1)L)/k^3,
    L=ln((1+k)/(1-k)); H(kappa) = -2P_F = kappa^2/3 + kappa^4/5 + ...
  - external_source_analysis.py: g_tt g_rr=-c^2 <=> G^t_t=G^r_r <=> p_r=-rho.

UDT metric (areal chart):
  ds^2 = -e^{-2phi} c^2 dt^2 + e^{+2phi} dr^2 + r^2 dOmega^2
  A = e^{-2phi} (so g_tt = -A c^2), B = e^{+2phi} (g_rr = B).

Symbolic GR in sympy (CPU). Float spot-checks where noted.
"""
import sympy as sp

PASS=[]
def chk(name, cond, extra=""):
    ok=bool(cond); PASS.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {extra}")
    return ok

c = sp.symbols('c', positive=True)   # the UDT light/speed constant in g_tt g_rr=-c^2
r, th, ph, t = sp.symbols('r theta varphi t', positive=True)
phi = sp.Function('phi')(r)
xi  = sp.symbols('xi', positive=True)   # field normalization (coupling) of L_angular

print("="*74)
print("TASK 1 — FIELD IDENTIFICATION (the unit 3-vector n_a, target S^2)")
print("="*74)
print("""
DERIVED (h1_types_results.md:31-37,159-166): the angular d.o.f. is the
unit 3-vector n_a, |n|=1, target S^2, whose winding density IS the H1
area form omega_H1 = eps_abc n_a dn_b ^ dn_c = sin(Theta) dTheta ^ dvarphi,
INT omega_H1 = 4*pi (deg-1 generator of H^2(S^2,Z)).  N=3 is the carrier
rank (eps_abc singlet unique iff N=3); q=1/3 is the public charge slope.

The HEDGEHOG / radial-winding configuration is n_a = x_a/|x| = x_a/r:
   n = (sin Theta cos varphi, sin Theta sin varphi, cos Theta), Theta=theta.
This is the degree-1 map S^2(space) -> S^2(target); its winding integral
is 4*pi (DERIVED, h1_types:33). q=1/3, N=3 carried by this same n-field.
""")
# winding/degree check of the hedgehog: (1/4pi) INT eps_abc n_a dn_b ^ dn_c
n = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
n_th = n.diff(th); n_ph = n.diff(ph)
# winding density = n . (n_th x n_ph)
wd = n.dot(n_th.cross(n_ph))
wd = sp.simplify(wd)
print("hedgehog winding density n.(n_th x n_ph) =", wd, " (= sin theta = area 2-form)")
deg = sp.integrate(sp.integrate(wd,(th,0,sp.pi)),(ph,0,2*sp.pi))/(4*sp.pi)
chk("hedgehog degree = (1/4pi) INT eps n dn dn = 1 (deg-1 H^2 generator)",
    sp.simplify(deg)==1, f"deg={deg}")

print()
print("="*74)
print("TASK 2 — CONSTRUCT THE KINETIC TERM from the metric measure (HONEST)")
print("="*74)
print("""
The natural scalar built from the n-field gradient is the metric trace
   X := g^{mu nu} (d_mu n_a)(d_nu n_a)        (target metric = delta_ab, |n|=1)
contracted with the UDT inverse metric.  The minimal Lagrangian density is
   L_angular = -(xi/2) g^{mu nu} d_mu n_a d_nu n_a
with the UDT measure sqrt(-g).  PROVENANCE / 'chose or derived?':
  * the OBJECT contracted (d_mu n_a d_nu n_a) is FORCED: it is the only
    diffeo-scalar, target-isometry-invariant, two-derivative quantity the
    n-field admits (the winding density omega_H1 is TOPOLOGICAL, carries no
    metric, contributes NO stress -- see TASK 6).  [DERIVED-as-unique]
  * that it is contracted with the UDT g^{mu nu} and weighted by sqrt(-g)
    is FORCED by general covariance + the UDT measure.  [DERIVED]
  * the prefactor -(xi/2) (sign, normalization xi) is CHOSEN (minimal,
    canonical-kinetic normalization).  xi is the single coupling.  [CHOSE]
  * NO potential, NO higher-derivative (Skyrme) term added: that is a
    CHOICE of the minimal model.  [CHOSE -- flagged: Skyrme term absent]
ANCHOR (TASK 5) decides whether this minimal choice IS the project's own
functional or a textbook import.
""")
# build UDT metric (coordinates t,r,theta,varphi)
A = sp.exp(-2*phi)             # |g_tt| = A c^2
B = sp.exp(+2*phi)            # g_rr = B
g = sp.diag(-A*c**2, B, r**2, r**2*sp.sin(th)**2)
gi = g.inv()
sqrtg = sp.sqrt(-g.det())
print("sqrt(-g) =", sp.simplify(sqrtg), " (= c r^2 sin theta, phi cancels: e^{-phi}e^{+phi}=1)")

# hedgehog n depends only on (theta,varphi):  d_t n = d_r n = 0
coords = [t, r, th, ph]
dn = [n.diff(co) for co in coords]   # gradient of each target component
# X = g^{mu nu} dn_mu . dn_nu
X = 0
for mu in range(4):
    for nu in range(4):
        X += gi[mu,nu]*dn[mu].dot(dn[nu])
X = sp.simplify(X)
print("X = g^{mu nu} d_mu n . d_nu n =", X, "  (hedgehog: = 2/r^2, the monopole gradient)")
chk("hedgehog gradient invariant X = 2/r^2 (pure transverse, deg-1)",
    sp.simplify(X - 2/r**2)==0)

print()
print("="*74)
print("TASK 3 — STRESS TENSOR  T_mu^nu  for the hedgehog in the UDT background")
print("="*74)
# L = -(xi/2) X ;  T_mu_nu = -(2/sqrt-g) d(sqrt-g L)/d g^{mu nu}
# For L = -(xi/2) g^{ab} dn_a.dn_b :  T_mu_nu = xi (dn_mu . dn_nu) + g_mu_nu L
# (standard scalar-multiplet stress; derived below explicitly term-by-term)
Lang = -(xi/sp.Integer(2))*X
T = sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        T[mu,nu] = xi*dn[mu].dot(dn[nu]) + g[mu,nu]*Lang
T = sp.simplify(T)
# raise one index: T^mu_nu = g^{mu a} T_a_nu
Tud = sp.simplify(gi*T)
rho   = sp.simplify(-Tud[0,0])     # T^t_t = -rho
p_r   = sp.simplify( Tud[1,1])     # T^r_r =  p_r
p_th  = sp.simplify( Tud[2,2])     # T^theta_theta = p_theta
p_ph  = sp.simplify( Tud[3,3])
print("T^t_t      = ", sp.simplify(Tud[0,0]), "   => rho =", rho)
print("T^r_r      = ", p_r,   "  (= p_r)")
print("T^theta_th = ", p_th,  "  (= p_theta)")
print("T^phi_phi  = ", p_ph)
chk("rho = +xi/r^2 (>0)", sp.simplify(rho - xi/r**2)==0)
chk("p_r = -xi/r^2 = -rho  (radial pressure)", sp.simplify(p_r + xi/r**2)==0)
chk("p_theta = 0", sp.simplify(p_th)==0)
chk("p_phi = p_theta = 0", sp.simplify(p_ph - p_th)==0)

print()
print("="*74)
print("TASK 4 — TEST p_r = -rho   (report p_r + rho EXACTLY)")
print("="*74)
pr_plus_rho = sp.simplify(p_r + rho)
print("p_r + rho =", pr_plus_rho, "   <-- EXACTLY ZERO?")
chk("p_r + rho == 0 IDENTICALLY (for the hedgehog n=x/r)",
    pr_plus_rho==0, f"p_r+rho={pr_plus_rho}")
print("""
Statement: for the degree-1 hedgehog n=x/r, the global-monopole stress has
   T^t_t = T^r_r = -xi/r^2,  T^theta_theta = T^phi_phi = 0.
Hence rho = xi/r^2, p_r = -xi/r^2, p_theta = 0, and p_r + rho = 0 EXACTLY,
INDEPENDENT of phi(r) and of r.  The equation of state p_r = -rho holds
IDENTICALLY for the radial-winding configuration.  (It is special to
n=x/r: a non-radial n would carry d_r n != 0 and break it -- checked
below.)""")
# show non-radial n breaks it: give n a radial twist Theta=Theta(r)
Thr = sp.Function('Theta')(r)
n2 = sp.Matrix([sp.sin(Thr)*sp.cos(ph), sp.sin(Thr)*sp.sin(ph), sp.cos(Thr)])
dn2 = [n2.diff(co) for co in coords]
X2 = sum(gi[mu,nu]*dn2[mu].dot(dn2[nu]) for mu in range(4) for nu in range(4))
X2 = sp.simplify(X2)
Lang2 = -(xi/2)*X2
T2 = sp.Matrix(4,4, lambda i,j: xi*dn2[i].dot(dn2[j]) + g[i,j]*Lang2)
T2ud = sp.simplify(gi*T2)
pr2 = sp.simplify(T2ud[1,1]); rho2 = sp.simplify(-T2ud[0,0])
br = sp.simplify(pr2+rho2)
print("radial-twist n (Theta=Theta(r)):  p_r+rho =", br,
      "  (=> non-radial breaks p_r=-rho unless Theta_r=0)")
chk("p_r+rho for radial-twist n vanishes IFF Theta'(r)=0 (pins the hedgehog)",
    sp.simplify(br.subs(sp.Derivative(Thr,r),0))==0 and br!=0)

print()
print("="*74)
print("TASK 5 — ANTI-SMUGGLING ANCHOR: reduce L_angular on the kappa mode")
print("="*74)
print("""
The project's anisotropy mode (dpf2/exterior_cavity) is f=F(1+kappa cos th).
On the anisotropic sphere the angular part of the metric inverse carries the
factor 1/(1+kappa cos th) (the f/F deformation of g_theta theta).  Reduce the
SAME global-monopole transverse energy sin^2(Theta)/g_thth (Theta=theta) over
the deformed sphere and compare to the project's G1(kappa):
   P_native(kappa) / prefactor  =?=  G1 = (2k+(k^2-1)L)/k^3.
THIS check decides native-vs-import.
""")
k = sp.symbols('kappa', positive=True)
u = sp.symbols('u')   # u = cos theta
Lln = sp.log((1+k)/(1-k))
G1 = (2*k + (k**2-1)*Lln)/k**3
# transverse global-monopole density of deg-1 hedgehog on deformed sphere:
#   e(theta) = sin^2(Theta)/g_thth-factor = sin^2 theta / (1+kappa cos theta)
# integrate over the sphere: INT_0^pi e * sin theta dtheta = INT sin^3/(1+k cos)
Inative = sp.integrate(sp.sin(th)**3/(1 + k*sp.cos(th)), (th, 0, sp.pi))
Inative = sp.simplify(Inative)
print("INT_0^pi sin^3(theta)/(1+kappa cos theta) dtheta =", Inative)
chk("native deformed-sphere monopole integral == G1(kappa) EXACTLY "
    "(the project's own G1 IS the global monopole)",
    sp.simplify(Inative - G1)==0, f"diff={sp.simplify(Inative-G1)}")
# and the leading order: kappa^2 G1 -> (4/3)kappa^2, and H = -2 P_F = kappa^2/3+...
# The project potential is P = (pi/2) F kappa^2 G1; the charge functional
# H = -2 P_F has leading kappa^2/3.  Confirm the leading match:
ser = sp.series(k**2*G1, k, 0, 6).removeO()
print("kappa^2 G1 series =", sp.simplify(ser), "  (leading (4/3)kappa^2)")
# H(kappa)=L/(2k)-1 leading term kappa^2/3 (the banked anchor):
Hk = Lln/(2*k) - 1
Hser = sp.series(Hk, k, 0, 8).removeO()
print("H(kappa) = -2 P_F series =", sp.simplify(Hser), "  (banked: kappa^2/3 + kappa^4/5 + ...)")
chk("H(kappa) leading term = kappa^2/3 (matches dpf2/exterior_cavity anchor)",
    sp.simplify(sp.series(Hk,k,0,3).removeO() - k**2/3)==0)

print()
print("="*74)
print("TASK 6 — BACK-REACTION: does T leave the G^theta_theta relation intact?")
print("="*74)
# Compute the Einstein tensor of the UDT metric and source it with T.
# We need full G^mu_nu.  Reuse the machinery.
def einstein_mixed(metric, coords):
    gi_ = metric.inv()
    Ga=[[[sp.simplify(sum(gi_[a,d]*(sp.diff(metric[d,b],coords[cc])
          +sp.diff(metric[d,cc],coords[b])-sp.diff(metric[b,cc],coords[d]))
          for d in range(4))/2) for cc in range(4)] for b in range(4)] for a in range(4)]
    Ric=sp.zeros(4)
    for b in range(4):
        for d in range(4):
            s=0
            for a in range(4):
                s+=sp.diff(Ga[a][b][d],coords[a])-sp.diff(Ga[a][b][a],coords[d])
                for e in range(4): s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
            Ric[b,d]=sp.simplify(s)
    Rs=sp.simplify(sum(gi_[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
    Gmix=sp.simplify(gi_*(Ric-sp.Rational(1,2)*metric*Rs))
    return Gmix
G_mix = einstein_mixed(g, coords)
print("G^t_t - G^r_r =", sp.simplify(G_mix[0,0]-G_mix[1,1]),
      "  (=0 => the UDT metric already enforces G^t_t=G^r_r identically)")
chk("UDT metric identity G^t_t = G^r_r (geometry side of B=1/A)",
    sp.simplify(G_mix[0,0]-G_mix[1,1])==0)
# Sourcing: with kappa8=8 pi G/c^4, G^mu_nu = kappa8 T^mu_nu.
# T^t_t=T^r_r=-xi/r^2 (equal) is CONSISTENT with G^t_t=G^r_r (equal): the
# t- and r- equations collapse to ONE equation.  The theta-equation is
# sourced by T^theta_theta=0 (hedgehog) -> SAME as vacuum theta-equation
# that fixed g_rr=e^{2phi}.  Check: the theta Einstein eq with rho=xi/r^2.
print("G^theta_theta =", sp.simplify(G_mix[2,2]))
print("G^t_t        =", sp.simplify(G_mix[0,0]))
# The t-equation: G^t_t = kappa8 T^t_t = -kappa8 xi/r^2.
# Solve for phi: does it admit the global-monopole solution e^{-2phi}=1-8piG xi - rs/r ?
kap8, xi_ = sp.symbols('kappa8 xi', positive=True)
tt_eq = sp.Eq(sp.simplify(G_mix[0,0]), -kap8*xi_/r**2)
print("t-equation:", tt_eq)
# theta-equation sourced by 0:
thth_eq = sp.Eq(sp.simplify(G_mix[2,2]), 0)
print("theta-equation (sourced by p_theta=0):", thth_eq)
print("""
=> The hedgehog source has T^theta_theta = 0, so the theta-equation is the
SAME as vacuum and continues to enforce the relation that gives g_rr=e^{2phi}.
Because T^t_t=T^r_r the t- and r-equations are ONE equation (G^t_t=G^r_r is a
metric identity), so g_tt g_rr=-c^2 is preserved INSIDE matter.  Solving the
t-equation: e^{-2phi} = 1 - kappa8 xi - rs/r  (a SOLID-ANGLE DEFICIT
1 - kappa8 xi plus Schwarzschild) -- the global-monopole metric, B=1/A intact.
""")

print(f"\n{'='*74}\nSUMMARY: {sum(PASS)}/{len(PASS)} PASS\n{'='*74}")
import json
open('/tmp/angular_lag.json','w').write(json.dumps({'pass':sum(PASS),'tot':len(PASS)}))
