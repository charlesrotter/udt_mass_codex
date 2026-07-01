#!/usr/bin/env python3
"""CLAIM 1 (refined): the standard hedgehog stress assumes the field maps the
SPATIAL sphere to the target sphere via n^i = nhat^i(theta,phi) with profile Th(r),
i.e. n = (sinTh sin th cos ph, sinTh sin th sin ph, cos Th) is WRONG for a clean
hedgehog. The clean deg-1 hedgehog is n^a = (sin Th(r) * x^a/|x|) i.e. the unit
vector aligns with the SPATIAL direction: nhat = (sin th cos ph, sin th sin ph, cos th)
and n = nhat rotated by Th about an axis... Actually the canonical Skyrme hedgehog is
U = exp(i Th(r) nhat.tau), giving n^a profile. The proper map: the pion field
phi^a = nhat^a sin Th, phi^0 = cos Th, with nhat the SPATIAL unit radial vector.

So n (target S^2 reduction) = (sin Th * nhat_x, sin Th * nhat_y, sin Th * nhat_z)?? -- no.
The S^2 sigma reduction of the deg-1 hedgehog has n^a = nhat^a EXACTLY (the spatial
radial unit vector), independent of Th, with Th entering only via... that gives Y only.

The codex L2+L4 stress with X=e^{-2b}Th'^2 and Y=sin^2Th/r^2 is the SU(2) Skyrme
hedgehog energy density. Let me verify against the KNOWN Skyrme hedgehog stress
directly using U = exp(i Th nhat.tau), which is the unambiguous standard object.
The energy density (static) of the SU(2) Skyrme model hedgehog is textbook:
  e = (f/2)[Th'^2 + 2 sin^2Th/r^2] + (1/4 e^2)[2 sin^2Th/r^2 Th'^2 + sin^4Th/r^4]
matching rho with xi<->f (with metric factors X,Y). That is EXACTLY the claimed rho.

This script: build U=exp(i Th nhat.tau), compute the chiral currents L_mu = U^-1 d_mu U,
form the genuine SU(2) Skyrme stress, and compare T^t_t,T^r_r to the claim. This is
the physically correct hedgehog and removes the S^2-orientation ambiguity of claim1.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi', real=True)
a = sp.Function('a')(r); b = sp.Function('b')(r); Th = sp.Function('Theta')(r)
xi, kap = sp.symbols('xi kappa', positive=True)
coords = [t, r, th, ph]
g = sp.diag(-sp.exp(2*a), sp.exp(2*b), r**2, r**2*sp.sin(th)**2)
gilow = sp.diag(-sp.exp(-2*a), sp.exp(-2*b), 1/r**2, 1/(r**2*sp.sin(th)**2))

# Pauli matrices
I2 = sp.eye(2)
sx = sp.Matrix([[0,1],[1,0]]); sy = sp.Matrix([[0,-sp.I],[sp.I,0]]); sz = sp.Matrix([[1,0],[0,-1]])
tau = [sx, sy, sz]
# spatial radial unit vector
nhat = [sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)]
ndt = nhat[0]*tau[0] + nhat[1]*tau[1] + nhat[2]*tau[2]
U = sp.cos(Th)*I2 + sp.I*sp.sin(Th)*ndt   # exp(i Th nhat.tau)
Udag = U.H

# chiral current L_mu = U^dag d_mu U  (anti-hermitian, su(2))
L = []
for c in coords:
    dU = U.applyfunc(lambda e: sp.diff(e, c))
    L.append(sp.simplify(Udag*dU))

# tr(L_mu L_nu)
def trace(M):
    return sp.simplify(M[0,0]+M[1,1])
TrLL = sp.zeros(4,4)
for A in range(4):
    for Bb in range(4):
        TrLL[A,Bb] = sp.simplify(trace(L[A]*L[Bb]))

# L2 density (sigma): L_sigma = -(xi/4) tr(L_mu L_nu) g^{mu nu}  (normalization absorbs into xi)
# Standard: kinetic = -(f^2/4) tr(L_mu L^mu). We use coefficient c2 to be fixed by matching X,Y.
c2, c4 = sp.symbols('c2 c4', positive=True)
Lsig = c2*sum(gilow[A,A]*TrLL[A,A] for A in range(4))
Lsig = sp.simplify(Lsig)

# Skyrme term: tr([L_mu,L_nu][L^mu,L^nu]); F_{mn}=[L_m,L_n]
F = [[sp.simplify(L[A]*L[Bb]-L[Bb]*L[A]) for Bb in range(4)] for A in range(4)]
Lsky = 0
for A in range(4):
    for Bb in range(4):
        for P in range(4):
            for Q in range(4):
                Lsky += gilow[A,P]*gilow[Bb,Q]*trace(F[A][Bb]*F[P][Q])
Lsky = sp.simplify(c4*Lsky)
Ltot = sp.simplify(Lsig + Lsky)

# Build with diagonal inverse-metric symbols for variation
gtt,grr,gh,gp = sp.symbols('gtt grr gh gp')
gid = sp.diag(gtt,grr,gh,gp)
Lsig_s = c2*sum(gid[A,A]*TrLL[A,A] for A in range(4))
Lsky_s = 0
for A in range(4):
    for Bb in range(4):
        for P in range(4):
            for Q in range(4):
                Lsky_s += gid[A,A]*gid[Bb,Bb]*trace(F[A][Bb]*F[P][Q])*sp.KroneckerDelta(A,P)*sp.KroneckerDelta(Bb,Q)
Lsky_s = c4*Lsky_s
Ls = sp.simplify(Lsig_s + Lsky_s)

glow = {gtt:-sp.exp(2*a), grr:sp.exp(2*b), gh:r**2, gp:r**2*sp.sin(th)**2}
gilowd = {gtt:-sp.exp(-2*a), grr:sp.exp(-2*b), gh:1/r**2, gp:1/(r**2*sp.sin(th)**2)}
glow_mat = sp.diag(*[glow[s] for s in (gtt,grr,gh,gp)])
syms=[gtt,grr,gh,gp]
Tm={}
for i,s in enumerate(syms):
    dLdg=sp.diff(Ls,s)
    Tlow=-2*dLdg+glow_mat[i,i]*Ls
    Tlow=sp.simplify(Tlow.subs(gilowd))
    Tm[s]=sp.simplify(gilowd[s]*Tlow)

Thp=sp.diff(Th,r)
X=sp.exp(-2*b)*Thp**2; Y=sp.sin(Th)**2/r**2
rho_claim=(xi/2)*(X+2*Y)+(kap/2)*(2*X*Y+Y**2)
pr_claim =(xi/2)*(X-2*Y)+(kap/2)*(2*X*Y-Y**2)
pT_claim =(kap/2)*Y**2-(xi/2)*X

# Tm are in terms of c2,c4. Match normalization: T^t_t should = -rho_claim.
Ttt=sp.simplify(Tm[gtt]); Trr=sp.simplify(Tm[grr]); Thh=sp.simplify(Tm[gh])
print("Raw T^t_t (c2,c4):", Ttt)
print("Raw T^r_r (c2,c4):", Trr)
# solve for c2,c4 by matching coefficients of X and Y in -Ttt vs rho_claim at a sample
# substitute concrete to read normalization: set b=0. compare structure.
# -Ttt = c2*(stuff in X,Y) + c4*(...). Match to rho.
mrho=-Ttt
# collect in X,Y by substituting Thp,sinTh symbols
Xs,Ys=sp.symbols('Xs Ys',positive=True)
subs_xy={Thp:sp.sqrt(Xs)*sp.exp(b), sp.sin(Th):sp.sqrt(Ys)*r}
# better: express via X,Y directly using e^{-2b}Thp^2=X, sin^2Th/r^2=Y
def to_xy(expr):
    e=sp.expand(sp.simplify(expr))
    e=e.subs(sp.sin(Th)**2, Ys*r**2)
    e=e.subs(Thp**2, Xs*sp.exp(2*b))
    e=e.subs(sp.cos(Th)**2, 1-Ys*r**2)
    return sp.simplify(e)
mrho_xy=to_xy(mrho)
rho_xy=rho_claim.subs(X,Xs).subs(Y,Ys)
print("\n-T^t_t in X,Y (with c2,c4):", mrho_xy)
print("rho_claim in X,Y:", sp.simplify(rho_xy))
# match: coefficient comparison
diff=sp.simplify(mrho_xy-(xi/2)*(Xs+2*Ys)-(kap/2)*(2*Xs*Ys+Ys**2))
print("\nResidual after assuming c2->xi, c4->kap mapping family:")
sol=sp.solve([sp.Poly(mrho_xy,Xs,Ys).coeff_monomial(Xs)-xi/2,
              sp.Poly(mrho_xy,Xs,Ys).coeff_monomial(Ys**2)-kap/2],[c2,c4],dict=True)
print("c2,c4 from matching X and Y^2 coeffs:",sol)
if sol:
    s=sol[0]
    print("Check XY coeff:", sp.simplify(sp.Poly(mrho_xy.subs(s),Xs,Ys).coeff_monomial(Xs*Ys)-kap))
    print("Check Y coeff:", sp.simplify(sp.Poly(mrho_xy.subs(s),Xs,Ys).coeff_monomial(Ys)-xi))
    # now full rho/pr/pT match
    Trr_xy=to_xy(Trr).subs(s); Ttt_xy=mrho_xy.subs(s)
    print("\n-T^t_t==rho?:",sp.simplify(Ttt_xy-rho_xy))
    pr_xy=pr_claim.subs(X,Xs).subs(Y,Ys)
    print("T^r_r==pr?:",sp.simplify(Trr_xy-pr_xy))
    Thh_xy=to_xy(Thh).subs(s); pT_xy=pT_claim.subs(X,Xs).subs(Y,Ys)
    print("T^th_th==pT?:",sp.simplify(Thh_xy-pT_xy))
