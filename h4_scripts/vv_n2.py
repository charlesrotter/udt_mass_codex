import sympy as sp

def hdr(t): print("\n"+"="*72+"\n"+t+"\n"+"="*72)

# ============================================================
hdr("V1. sqrt(h)K identity and K = -2 det(K^A_B)  (independent build)")
r, phi, lam = sp.symbols('r phi lambda', real=True)
a,b,s = sp.symbols('a b s', real=True)
ap,bp,sp_ = sp.symbols('ap bp sp', real=True)  # r-derivatives
h = sp.Matrix([[a,s],[s,b]]); hinv=h.inv(); hdet=h.det(); sqh=sp.sqrt(hdet)
dh = sp.Matrix([[ap,sp_],[sp_,bp]])
Klow = sp.Rational(1,2)*sp.exp(-phi)*dh
Kmix = hinv*Klow
Kup  = hinv*Klow*hinv
Ktr  = sp.trace(Kmix)
KK   = sum(Kup[i,j]*Klow[i,j] for i in range(2) for j in range(2))
Kcurl= sp.simplify(KK - Ktr**2)
print("K + 2 det(K^A_B) =", sp.simplify(Kcurl + 2*Kmix.det()))
target = -sp.Rational(1,2)*sp.exp(-2*phi)*(ap*bp - sp_**2)/sqh
print("sqrt(h)K - [-1/2 e^-2phi (a'b'-s'^2)/sqrt(h)] =", sp.simplify(sqh*Kcurl - target))
print("shift: K(phi+lam)/K(phi) =", sp.simplify(Kcurl.subs(phi,phi+lam)/Kcurl),"(expect e^-2lam)")

# ============================================================
hdr("V2. CF1 total-derivative test at FULL nonlinear order")
# density D(a,b,s,phi; a',b',s') = -1/2 e^-2phi (a'b'-s'^2)/sqrt(ab-s^2)
# A total r-derivative of ANY state function F(a,b,s,phi) is LINEAR in (a',b',s',phi').
# D contains a'b' and s'^2 -> quadratic. Confirm by mixed partials wrt velocities.
Ap,Bp,Sp,PHp = sp.symbols('Ap Bp Sp PHp')
A_,B_,S_,PH_ = sp.symbols('A_ B_ S_ PH_')
D = -sp.Rational(1,2)*sp.exp(-2*PH_)*(Ap*Bp-Sp**2)/sp.sqrt(A_*B_-S_**2)
print("d^2 D/da'db' =", sp.simplify(sp.diff(D,Ap,Bp)), "(nonzero -> a'b' cross term -> NOT linear in velocities)")
print("d^2 D/ds'ds' =", sp.simplify(sp.diff(D,Sp,Sp)), "(nonzero -> s'^2 term)")
print("=> D is not d/dr F(state); no algebraic identity forces int D dr = 0.  Full-order CF1 argument SOUND.")

# ============================================================
hdr("V3. *** SHARPEST *** Is the LINEARIZED source a total derivative? (forced-cancel at O(amp)?)")
# Perturb round background h0=diag(r^2, r^2 sin^2 th), phi=0.
# a=r^2(1+e*al(r,x)), b=r^2 sin^2(1+e*be), s=r^2 sin*e*ga, phi=e*ps(r)
th,e = sp.symbols('theta epsilon', real=True)
al=sp.Function('al'); be=sp.Function('be'); ga=sp.Function('ga'); ps=sp.Function('ps')
# keep angular dependence generic via functions of r only for the r-structure (phi longitudinal)
aa = r**2*(1+e*al(r)); bb = r**2*sp.sin(th)**2*(1+e*be(r)); ss = r**2*sp.sin(th)*e*ga(r); pp = e*ps(r)
def sqrthK(a_,b_,s_,phi_):
    hd=a_*b_-s_**2
    return -sp.Rational(1,2)*sp.exp(-2*phi_)*(sp.diff(a_,r)*sp.diff(b_,r)-sp.diff(s_,r)**2)/sp.sqrt(hd)
Dfull = sqrthK(aa,bb,ss,pp)
D0  = Dfull.subs(e,0)
D1  = sp.simplify(sp.diff(Dfull,e).subs(e,0))   # linear-in-amplitude source density
print("background sqrt(h)K (round, phi=0):", sp.simplify(D0), " (expect -2 sin th)")
print("\nLINEARIZED source density D1 =")
sp.pprint(sp.simplify(D1))
# Is D1 a total r-derivative of some G(al,be,ga,ps)? It is linear, so check if the
# non-derivative (al,be,ga themselves) pieces vanish -> pure d/dr(...) means integrand
# over compact support integrates to boundary = 0.  Extract coefficient of al(r) (no deriv):
alv=sp.Symbol('alv'); alp=sp.Symbol('alp')
D1e = D1.subs({sp.Derivative(al(r),r):alp, al(r):alv,
               sp.Derivative(be(r),r):sp.Symbol('bep'), be(r):sp.Symbol('bev'),
               sp.Derivative(ga(r),r):sp.Symbol('gap'), ga(r):sp.Symbol('gav'),
               sp.Derivative(ps(r),r):sp.Symbol('psp'), ps(r):sp.Symbol('psv')})
print("\ncoeff of al (undifferentiated) in D1:", sp.simplify(sp.diff(D1e,alv)))
print("coeff of be (undifferentiated) in D1:", sp.simplify(sp.diff(D1e,sp.Symbol('bev'))))
print("coeff of ps (undifferentiated) in D1:", sp.simplify(sp.diff(D1e,sp.Symbol('psv'))))
print("(If a total r-derivative d/dr[c1 al + c2 be + ...] then undiff coeffs come only via c_i'(r);")
print(" nonzero undiff coeffs with r-dependence => generically NOT a pure total derivative.)")

# ============================================================
hdr("V4. DIRECT refutation of forced cancellation: explicit compact profile with int != 0")
# Choose s=0, phi=0, a=b=f(r)^2, f compact bump returning to ambient. sqrt(h)K = -2 f'^2.
R=sp.Symbol('R',positive=True)
f = 1 + (r*(R-r))**2   # smooth, but f(0)=f(R)=1 (returns to ambient value 1)
a_ = f**2; b_=f**2;
Dtoy = -sp.Rational(1,2)*(sp.diff(a_,r)*sp.diff(b_,r))/sp.sqrt(a_*b_)   # = -2 f'^2
I = sp.integrate(Dtoy,(r,0,R))
print("f(0),f(R):", f.subs(r,0), f.subs(r,R))
print("int_0^R sqrt(h)K dr =", sp.simplify(I), " -> substitute R=1:", sp.simplify(I.subs(R,1)))
print("=> nonzero for a compact deformation returning to ambient => NO forced cancellation. CF1 genuinely OPEN.")

# ============================================================
hdr("V5. Monopole reduction: homogeneous exterior with A(r)=4 pi r^2 gives dphi=-dq/r; flux factor Z")
Zf,C,phinf = sp.symbols('Z_phi C phi_inf', real=True, positive=True)
phip = C/(Zf*r**2)                    # from Z phi' A = const with A=4 pi r^2 absorbed into C
phi_ext = sp.integrate(phip,r)        # = -C/(Z r)
print("phi' = C/(Z r^2) -> phi =", sp.simplify(phi_ext),"+ phi_inf  => dphi = -(C/Z)/r, dq=C/Z")
# flux Q_phi = sqrt(h) Z phi' integrated over solid angle, sqrt(h)=r^2 sin th, ambient
Qflux = sp.integrate(sp.integrate((r**2*sp.sin(th))*Zf*phip, (th,0,sp.pi)),(sp.Symbol('psi'),0,2*sp.pi))
print("Q_phi = int sqrt(h) Z phi' dOmega =", sp.simplify(Qflux)," = 4 pi C ; with dq=C/Z => Q_phi = 4 pi Z dq. CHECK")

# ============================================================
hdr("V6. MS mass: 1-2m/rho=e^-2phi rho'^2, rho=r, phi=phi_inf-q/r -> m=-q at O(1/r)")
q=sp.Symbol('q',real=True)
phi_sol = phinf - q/r
m = sp.Rational(1,2)*r*(1 - sp.exp(-2*phi_sol)*sp.diff(r,r)**2)
print("phi_inf=0: m series:", sp.series(m.subs(phinf,0),r,sp.oo,2))
print("=> leading -q ; sub-leading -q^2/r (nonlinear). m=-q=M identification holds at O(1/r).")

# ============================================================
hdr("V7. G^(2)_AB == 0 for a GENERAL non-round 2-metric (no local R^(2) stress)")
x,y=sp.symbols('x y', real=True)
g11=sp.Function('g11')(x,y); g12=sp.Function('g12')(x,y); g22=sp.Function('g22')(x,y)
gm=sp.Matrix([[g11,g12],[g12,g22]]); gi=gm.inv(); coords=[x,y]
def christ(gm,gi,coords):
    n=2; Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m_ in range(n):
            for k in range(n):
                Ga[l][m_][k]=sum(gi[l,p]*(sp.diff(gm[p,m_],coords[k])+sp.diff(gm[p,k],coords[m_])-sp.diff(gm[m_,k],coords[p])) for p in range(n))/2
    return Ga
Ga=christ(gm,gi,coords)
def Ricci(Ga,coords):
    n=2; Ric=sp.zeros(n,n)
    for m_ in range(n):
        for k in range(n):
            val=0
            for l in range(n):
                val+=sp.diff(Ga[l][m_][k],coords[l])-sp.diff(Ga[l][m_][l],coords[k])
                for p in range(n):
                    val+=Ga[l][l][p]*Ga[p][m_][k]-Ga[l][k][p]*Ga[p][m_][l]
            Ric[m_,k]=val
    return Ric
Ric=Ricci(Ga,coords)
Rs=sum(gi[i,j]*Ric[i,j] for i in range(2) for j in range(2))
G2=sp.zeros(2,2)
for i in range(2):
    for j in range(2):
        G2[i,j]=sp.simplify(Ric[i,j]-sp.Rational(1,2)*gm[i,j]*Rs)
print("G^(2)_11 =",G2[0,0],"  G^(2)_12 =",G2[0,1],"  G^(2)_22 =",G2[1,1])
print("=> Einstein tensor identically 0 in 2D for general metric: R^(2) exerts no local stress. CHECK" if G2==sp.zeros(2,2) else "NONZERO!")
