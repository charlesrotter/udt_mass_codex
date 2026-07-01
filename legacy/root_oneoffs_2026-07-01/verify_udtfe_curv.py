import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_a', real=True)
c0 = sp.symbols('c0', positive=True)
phi = sp.Function('phi')(r)

def einstein_mixed(g, coords):
    n = len(coords)
    ginv = g.inv()
    # Christoffel
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for ccc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[ccc])+sp.diff(g[d,ccc],coords[b])-sp.diff(g[b,ccc],coords[d]))
                Gamma[a][b][ccc] = sp.simplify(s/2)
    # Ricci
    Ric = sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b,d] = sp.simplify(s)
    Rs = sp.simplify(sum(ginv[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
    G = sp.simplify(Ric - sp.Rational(1,2)*g*Rs)
    Gmix = sp.simplify(ginv*G)  # G^mu_nu
    return Gmix

coords = [t,r,th,ph]
g = sp.diag(-sp.exp(-2*phi)*c0**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
Gm = einstein_mixed(g, coords)
print("G^t_t =", Gm[0,0])
print("G^r_r =", Gm[1,1])
print("G^t_t - G^r_r =", sp.simplify(Gm[0,0]-Gm[1,1]), " (claim: 0 identically)")
print("G^th_th =", sp.simplify(Gm[2,2]))

# Check c0 does NOT appear in mixed Einstein tensor (folds into lapse)
print("\nc0 in G^t_t?", c0 in Gm[0,0].free_symbols)
print("c0 in G^th_th?", c0 in sp.simplify(Gm[2,2]).free_symbols)

# --- cl(r) promoted into g_tt: g_tt = -e^{-2phi} cl(r)^2 ---
cl = sp.Function('cl')(r)
g2 = sp.diag(-sp.exp(-2*phi)*cl**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
Gm2 = einstein_mixed(g2, coords)
print("\n--- cl promoted ---")
print("G^t_t - G^r_r (cl) =", sp.simplify(Gm2[0,0]-Gm2[1,1]), " (claim: -2 e^{-2phi} cl'/(r cl))")
print("  matches -2 e^{-2phi} cl'/(r cl):",
      sp.simplify((Gm2[0,0]-Gm2[1,1]) - (-2*sp.exp(-2*phi)*sp.diff(cl,r)/(r*cl)))==0)
