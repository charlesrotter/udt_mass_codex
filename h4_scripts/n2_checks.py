import sympy as sp

print("="*70)
print("CHECK 1: sqrt(h) K  identity  and  K = -2 det(K^A_B)")
print("="*70)
r, phi = sp.symbols('r phi', real=True)
# general 2x2 transverse metric h = [[a,s],[s,b]] (functions of r)
a,b,s = sp.symbols('a b s', real=True, positive=False)
ap,bp,sp_ = sp.symbols('ap bp sp', real=True)  # r-derivatives
h = sp.Matrix([[a,s],[s,b]])
hdet = h.det()
sqh = sp.sqrt(hdet)
hinv = h.inv()
efac = sp.exp(-phi)
# K_AB = 1/2 e^{-phi} dh/dr
dh = sp.Matrix([[ap,sp_],[sp_,bp]])
K_low = sp.Rational(1,2)*efac*dh
K_mix = hinv*K_low            # K^A_B
Ktr = sp.trace(K_mix)
K_up = hinv*K_low*hinv        # K^{AB}
# compute K_AB K^AB = sum K^{AB} K_AB
KK = 0
for i in range(2):
    for j in range(2):
        KK += K_up[i,j]*K_low[i,j]
Kcurl = sp.simplify(KK - Ktr**2)   # 𝒦
detKmix = sp.simplify(K_mix.det())
print("𝒦 + 2 det(K^A_B) simplifies to:", sp.simplify(Kcurl + 2*detKmix))
# sqrt(h) 𝒦
sqhK = sp.simplify(sqh*Kcurl)
target = -sp.Rational(1,2)*sp.exp(-2*phi)*(ap*bp - sp_**2)/sqh
print("sqrt(h)𝒦 - [-1/2 e^{-2phi}(a'b'-s'^2)/sqrt(h)] =", sp.simplify(sqhK - target))

print()
print("="*70)
print("CHECK 2: is sqrt(h)𝒦 a total r-derivative (CF1 exact-cancellation attempt)?")
print("="*70)
# Let a(r),b(r),s(r), phi(r). density D = -1/2 e^{-2phi}(a'b'-s'^2)/sqrt(ab-s^2)
# Test exactness: does there exist F(a,b,s,phi) with dF/dr = D for ALL profiles?
# Necessary: D must be expressible as F_a a' + F_b b' + F_s s' + F_phi phi'
# But D contains a'*b' (product of two derivatives) => cannot be linear in first derivatives
# => NOT of the form dF/dr for a state function F(a,b,s,phi). Demonstrate:
ar,br,sr,phir = sp.symbols('a b s phi', cls=sp.Function)
t = sp.symbols('t')  # use t as r
A,B,S,PH = ar(t),br(t),sr(t),phir(t)
D = -sp.Rational(1,2)*sp.exp(-2*PH)*(sp.diff(A,t)*sp.diff(B,t)-sp.diff(S,t)**2)/sp.sqrt(A*B-S**2)
# If D were d/dt F(A,B,S,PH), then dD/d(a') would be independent of a' (since F depends only on state).
# d/d(a') of D:  treat a'(=Ap) as variable
Ap,Bp,Sp,PHp = sp.symbols('Ap Bp Sp PHp')
Dsub = -sp.Rational(1,2)*sp.exp(-2*sp.Symbol('PH'))*(Ap*Bp-Sp**2)/sp.sqrt(sp.Symbol('A')*sp.Symbol('B')-sp.Symbol('S')**2)
dDdAp = sp.diff(Dsub, Ap)
print("d(density)/d(a') =", dDdAp, " -> depends on b' => density has a'*b' cross term")
print("=> NOT linear in velocities => NOT a total r-derivative of any state function F.")
print("=> No Gauss/divergence identity forces the compact-support integral to vanish. CF1 OPEN.")

print()
print("="*70)
print("CHECK 3: round reduction — 𝒦 round, source, monopole equation")
print("="*70)
# round: h = r^2 Omega, a=r^2, b=r^2 sin^2, s=0
th = sp.symbols('theta')
ar2 = r**2; br2 = r**2*sp.sin(th)**2
hro = sp.Matrix([[ar2,0],[0,br2]])
dhro = sp.diff(hro,r)
Klow_ro = sp.Rational(1,2)*sp.exp(-phi)*dhro
Kmix_ro = hro.inv()*Klow_ro
Ktr_ro = sp.trace(Kmix_ro)
KK_ro=0
Kup_ro=hro.inv()*Klow_ro*hro.inv()
for i in range(2):
    for j in range(2):
        KK_ro += Kup_ro[i,j]*Klow_ro[i,j]
Kcurl_ro = sp.simplify(KK_ro-Ktr_ro**2)
print("𝒦 round =", Kcurl_ro, " (expect -2 e^{-2phi}/r^2)")
sqh_ro = sp.sqrt(hro.det())
src = sp.simplify(-2*sqh_ro*Kcurl_ro)  # -2 sqrt(h) 𝒦  (per d theta dpsi, incl sin theta)
print("-2 sqrt(h) 𝒦 round =", src, " (per solid angle drop sin: )", sp.simplify(src/sp.sin(th)))

print()
print("="*70)
print("CHECK 4: MS mass  1-2m/rho = e^{-2phi} rho'^2 with phi=phi_inf - q/r  => m=-q at O(1/r)")
print("="*70)
q, phinf = sp.symbols('q phi_inf', real=True)
rho = r  # rho=r theorem
phi_sol = phinf - q/r
lhs = sp.exp(-2*phi_sol)*sp.diff(rho,r)**2
# 1-2m/rho = lhs -> m = rho/2 (1-lhs)
m = sp.Rational(1,2)*rho*(1-lhs)
mseries = sp.series(m, r, sp.oo, 3)
print("m(r) large-r series (phi_inf general):")
print("  ", mseries)
m0 = m.subs(phinf,0)
print("phi_inf=0:  m =", sp.simplify(m0), " -> leading:", sp.series(m0,r,sp.oo,2))
