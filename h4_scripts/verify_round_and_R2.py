import sympy as sp

r, th = sp.symbols('r theta')
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
Zf  = sp.symbols('Z_phi', positive=True)

# ---------- ROUND reduction: recover rho''_matter and the e^{2phi}/4 weight -----
# 1D reduced geometric Lagrangian (per solid angle, sqrt(Omega)=sinθ stripped):
#   L = (Z/2) rho^2 phi'^2  - 2 e^{-2phi} rho'^2  + 2   (+ L_m)
# from  sqrt(h)=rho^2 sinθ, 𝒦=-2e^{-2phi}rho'^2/rho^2, R2*sqrt(h)=2 sinθ (const in rho)
rp  = sp.diff(rho, r); php = sp.diff(phi, r)
xi, kap, N = sp.symbols('xi kappa N', positive=True)
Ir, I4th = sp.symbols('I_r I_4theta')   # matter angular integrals (rho-independent)
# reduced matter Lagrangian (round, per 4pi), from round_matter_reduction:
Lm = -(xi/2)*(rho**2*Ir) - (kap*N**2/2)*(I4th/rho**2)   # only rho-dependent pieces
L  = sp.Rational(1,2)*Zf*rho**2*php**2 - 2*sp.exp(-2*phi)*rp**2 + Lm

# Euler-Lagrange in rho:
ELrho = sp.diff(L, rho) - sp.diff(sp.diff(L, rp), r)
ELrho = sp.expand(ELrho)
# solve for rho''
rho_pp = sp.symbols('rho_pp')
EL2 = ELrho.subs(sp.Derivative(rho,(r,2)), rho_pp)
sol = sp.solve(EL2, rho_pp)[0]
sol = sp.simplify(sol)
print("rho'' (full) =", sol)
# isolate the MATTER piece: set Z-> keep; the matter part is the terms with Ir,I4th
rho_matter = sp.simplify(sol.coeff(Ir)*Ir + sol.coeff(I4th)*I4th)
print("rho''_matter =", sp.simplify(rho_matter))
target = (sp.exp(2*phi)/4)*(xi*rho*Ir - kap*N**2*I4th/rho**3)
print("MATCH corpus (e^{2phi}/4)(xi rho I_r - kappa N^2 I_4θ/rho^3):",
      sp.simplify(rho_matter - target))

# ---------- 𝒦 SIGN can flip (toroidal relevance) ----------------------------
# For an anisotropic h=diag(P,Q): 𝒦 = -1/2 e^{-2phi} P'Q'/(PQ).
# If one transverse dim GROWS (P'>0) while the other SHRINKS (Q'<0) as in a
# torus core, P'Q'<0  => 𝒦 > 0 (opposite sign to the round -2e^{-2phi}/r^2 <0).
print("\n𝒦 sign: round(=P'=Q'>0) -> P'Q'>0 -> 𝒦<0 ; anisotropic P'Q'<0 -> 𝒦>0 (flips)")

# ---------- R^{(2)} is topological (Gauss-Bonnet): explicit non-round metric ---
# transverse metric depending on theta (non-round), 2D:
a = sp.Function('a')(r,th); b = sp.Function('b')(r,th)
# use a concrete smooth non-round 2-metric g = diag(A(th)^2, B(th)^2 sin^2? ) -- 
# compute 2D Ricci scalar and check sqrt(h) R2 integrates to Euler char indep of r-scale.
A = sp.Function('A')(th)
g2 = sp.diag(A**2, sp.sin(th)**2)      # a non-round (theta-warped) 2-sphere-like metric
g2inv = g2.inv()
def christoffel(g, coords):
    n=len(coords); gi=g.inv()
    Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s=0
                for s_ in range(n):
                    s+=gi[l,s_]*(sp.diff(g[s_,m],coords[k])+sp.diff(g[s_,k],coords[m])-sp.diff(g[m,k],coords[s_]))
                Gamma[l][m][k]=sp.simplify(s/2)
    return Gamma
coords=[r,th]  # but g2 only depends on th; treat as 2D (th, psi)? redo in (th,psi)
th,ps=sp.symbols('theta psi')
A=sp.Function('A')(th)
g2=sp.diag(A**2, sp.sin(th)**2); coords=[th,ps]
G=christoffel(g2,coords)
n=2
Ric=sp.zeros(n,n)
for m in range(n):
    for k in range(n):
        s=0
        for l in range(n):
            s+=sp.diff(G[l][m][k],coords[l])-sp.diff(G[l][m][l],coords[k])
            for p in range(n):
                s+=G[l][l][p]*G[p][m][k]-G[l][k][p]*G[p][m][l]
        Ric[m,k]=sp.simplify(s)
Rscalar=sp.simplify(sum(g2.inv()[i,j]*Ric[i,j] for i in range(2) for j in range(2)))
# 2D Einstein tensor should vanish identically:
G2=sp.zeros(2,2)
for i in range(2):
    for j in range(2):
        G2[i,j]=sp.simplify(Ric[i,j]-sp.Rational(1,2)*g2[i,j]*Rscalar)
print("\n2D Einstein tensor G^(2)_AB (must be identically 0):")
print(sp.simplify(G2))
