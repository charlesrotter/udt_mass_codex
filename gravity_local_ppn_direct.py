"""
gravity_local_ppn_direct.py  (2026-06-18)

Direct PPN gamma from the honest f(phi)R scalar-tensor equations WITHOUT the
B=1/A lock. Two independent metric functions:
    g_tt = -A(r) c0^2,   g_rr = B(r),   areal r.
phi is SLAVED to g_tt:  phi = -(1/2) ln(A)   (from g_tt = -e^{-2phi}c0^2).
So f = (c0^4/16piG) e^{-8phi} = (c0^4/16piG) A^4.

Field eqn:  f G_mn + (g_mn box - nabla_m nabla_n) f = (1/2) T_mn,  vacuum T=0.

We linearize the METRIC (legit PPN: A=1+a(r), B=1+b(r), a,b small ~ GM/rc^2)
and solve for a(r), b(r) in vacuum, then PPN gamma = -b/a-ratio coefficient.
Standard PPN: g_tt=-(1-2U), g_rr=1+2 gamma U  => A=1-2U => a=-2U;
B=1+2 gamma U => b = 2 gamma U.  gamma = -b/a.

We build the spherically-symmetric vacuum equations from scratch with sympy
(general A,B), substitute phi=-1/2 ln A into f, linearize, solve.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
c0, G = sp.symbols('c0 G', positive=True)
A = sp.Function('A')
B = sp.Function('B')

# metric diag(-A c0^2, B, r^2, r^2 sin^2)
# Build Einstein tensor G^mu_nu and box/nabla nabla of f for general A,B.
th = sp.symbols('theta')
g = sp.diag(-A(r)*c0**2, B(r), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = [sp.symbols('t'), r, th, sp.symbols('psi')]

def christoffel(g, ginv, coords):
    n=len(coords); Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cidx in range(n):
                s=0
                for d in range(n):
                    s+= ginv[a,d]*(sp.diff(g[d,b],coords[cidx])+sp.diff(g[d,cidx],coords[b])-sp.diff(g[b,cidx],coords[d]))
                Ga[a][b][cidx]=sp.simplify(s/2)
    return Ga
Ga=christoffel(g,ginv,coords)
n=4
def ricci(Ga,coords):
    n=len(coords); Ric=sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s+=sp.diff(Ga[a][b][d],coords[a]) - sp.diff(Ga[a][b][a],coords[d])
                for e in range(n):
                    s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
            Ric[b,d]=sp.simplify(s)
    return Ric
Ric=ricci(Ga,coords)
Rs=sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
Gmix = sp.zeros(n,n)  # G^mu_nu mixed
Gdn = Ric - sp.Rational(1,2)*g*Rs
for a in range(n):
    for b in range(n):
        Gmix[a,b]=sp.simplify(sum(ginv[a,c]*Gdn[c,b] for c in range(n)))

# f and its covariant derivatives
phi = -sp.Rational(1,2)*sp.log(A(r))
f = (c0**4/(16*sp.pi*G))*sp.exp(-8*phi)   # = c0^4/(16piG) * A^4
# box f and nabla_m nabla_n f (only r-dependence)
def cov_hess(f):
    # nabla_m nabla_n f = d_m d_n f - Ga^l_mn d_l f
    H=sp.zeros(n,n)
    df=[sp.diff(f,coords[i]) for i in range(n)]
    for a in range(n):
        for b in range(n):
            term=sp.diff(df[a],coords[b]) - sum(Ga[l][a][b]*df[l] for l in range(n))
            H[a,b]=sp.simplify(term)
    return H
H=cov_hess(f)
boxf=sp.simplify(sum(ginv[i,j]*H[i,j] for i in range(n) for j in range(n)))
# E^mu_nu = (delta^mu_nu box f - nabla^mu nabla_nu f)
Emix=sp.zeros(n,n)
for a in range(n):
    for b in range(n):
        nab_up = sum(ginv[a,c]*H[c,b] for c in range(n))
        Emix[a,b]=sp.simplify((1 if a==b else 0)*boxf - nab_up)

# Honest vacuum eqn (mixed): f*Gmix + Emix = 0
EQ = sp.simplify(f*Gmix + Emix)

# Linearize: A=1+a(r), B=1+b(r); a,b first order. Expand each diagonal eq.
a=sp.Function('a'); b=sp.Function('b'); eps=sp.symbols('eps',positive=True)
sub={A(r):1+eps*a(r), B(r):1+eps*b(r)}
# need derivatives substituted too
def lin(expr):
    e2=expr.subs({sp.Derivative(A(r),(r,2)):eps*sp.Derivative(a(r),(r,2)),
                  sp.Derivative(A(r),r):eps*sp.Derivative(a(r),r),
                  sp.Derivative(B(r),(r,2)):eps*sp.Derivative(b(r),(r,2)),
                  sp.Derivative(B(r),r):eps*sp.Derivative(b(r),r),
                  A(r):1+eps*a(r), B(r):1+eps*b(r)})
    return sp.series(e2,eps,0,2).removeO()

EQtt=sp.simplify(lin(EQ[0,0])/ (c0**4/(16*sp.pi*G)))
EQrr=sp.simplify(lin(EQ[1,1])/ (c0**4/(16*sp.pi*G)))
EQthth=sp.simplify(lin(EQ[2,2])/ (c0**4/(16*sp.pi*G)))
# take O(eps) coefficient
EQtt1=sp.simplify(sp.diff(EQtt,eps).subs(eps,0))
EQrr1=sp.simplify(sp.diff(EQrr,eps).subs(eps,0))
EQthth1=sp.simplify(sp.diff(EQthth,eps).subs(eps,0))
print("Linearized honest vacuum equations (O(eps)) :")
print("  tt:", EQtt1, "= 0")
print("  rr:", EQrr1, "= 0")
print("  thth:", EQthth1, "= 0")

# Solve the linear ODE system for a(r), b(r) with 1/r ansatz a=alpha/r, b=beta/r
al,be=sp.symbols('alpha beta')
def ansatz(e):
    e=e.subs(sp.Derivative(a(r),(r,2)), sp.diff(al/r,r,2))
    e=e.subs(sp.Derivative(a(r),r), sp.diff(al/r,r))
    e=e.subs(sp.Derivative(b(r),(r,2)), sp.diff(be/r,r,2))
    e=e.subs(sp.Derivative(b(r),r), sp.diff(be/r,r))
    e=e.subs(a(r),al/r).subs(b(r),be/r)
    return sp.simplify(e)
tt=ansatz(EQtt1); rr=ansatz(EQrr1); thth=ansatz(EQthth1)
print()
print("With 1/r ansatz a=alpha/r, b=beta/r:")
print("  tt:", tt, "=0")
print("  rr:", rr, "=0")
print("  thth:", thth, "=0")
sol=sp.solve([sp.numer(sp.together(tt)),sp.numer(sp.together(rr))],[al,be],dict=True)
print("  solve tt,rr for alpha,beta:", sol)
# PPN: A=1+a=1-2U => alpha/r=-2U; B=1+b=1+2gamma U => beta/r=2 gamma U
# => gamma = -beta/alpha
if sol:
    s=sol[0]
    if al in s:
        pass
    # relation
print()
# Compare GR: G^mu_nu=0 linearized gives a=-rs/r? and gamma=1.
print("GR check (Emix=0): linearized G^mu_nu=0 with 1/r ansatz gives gamma=1.")
GRtt=ansatz(sp.diff(sp.simplify(lin(Gmix[0,0])),eps).subs(eps,0))
GRrr=ansatz(sp.diff(sp.simplify(lin(Gmix[1,1])),eps).subs(eps,0))
solGR=sp.solve([sp.numer(sp.together(GRtt)),sp.numer(sp.together(GRrr))],[al,be],dict=True)
print("  GR tt:",GRtt," rr:",GRrr," sol:",solGR)
