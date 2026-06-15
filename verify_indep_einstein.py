#!/usr/bin/env python3
"""
INDEPENDENT BLIND VERIFIER -- own closed-form Einstein engine + analytic disentanglement.
Driver: Claude (Opus 4.8, 1M) blind verifier.  2026-06-15.  DATA-BLIND.

Independent of whole_metric_3d_core.py: closed-form sympy G^mu_nu for a diagonal
metric  ds^2 = g_tt(r) dt^2 + g_rr(r) dr^2 + r^2 dth^2 + r^2 sin^2 th dps^2.
Validated on Schwarzschild (G=0).  Then the analytic forcing argument:
  B=1/A + G^t_t = k T^t_t  =>  p_r = -rho ?
and whether the L2+L4 soliton stress has T^t_t = T^r_r (twisted body).
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap, k8 = sp.symbols('xi kappa kappa8', positive=True)

# ===========================================================================
# 1. INDEPENDENT closed-form Einstein engine for a diagonal metric.
#    g_tt = A(r) (negative), g_rr = B(r) (positive).  Compute G^mu_nu mixed.
# ===========================================================================
def einstein_mixed(gtt, grr):
    """Return dict of mixed G^mu_nu for ds^2 = gtt dt^2 + grr dr^2 + r^2 dOmega^2.
       Built from scratch: g -> Gamma -> Riemann -> Ricci -> G_{mn} -> G^m_n."""
    g = sp.diag(gtt, grr, r**2, r**2*sp.sin(th)**2)
    gi = g.inv()
    coords = [t, r, th, ps]
    n = 4
    # Christoffel Gamma^a_{bc}
    Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += gi[a, d]*(sp.diff(g[d, b], coords[c])
                                   + sp.diff(g[d, c], coords[b])
                                   - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = sp.simplify(s/2)
    # Riemann R^a_{bcd}
    def riem(a, b, c, d):
        s = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
        for e in range(n):
            s += Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c]
        return s
    # Ricci R_{bd} = R^a_{bad}
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += riem(a, b, a, d)
            Ric[b, d] = sp.simplify(s)
    Rs = sp.simplify(sum(gi[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
    Gdn = sp.Matrix(n, n, lambda i, j: sp.simplify(Ric[i, j] - sp.Rational(1, 2)*g[i, j]*Rs))
    Gmix = sp.simplify(gi*Gdn)  # G^mu_nu
    return {'tt': sp.simplify(Gmix[0, 0]), 'rr': sp.simplify(Gmix[1, 1]),
            'thth': sp.simplify(Gmix[2, 2]), 'psps': sp.simplify(Gmix[3, 3])}, g, gi

print("="*78)
print("TASK 1: independent closed-form Einstein engine, validate on Schwarzschild")
print("="*78)
M = sp.symbols('M', positive=True)
f = 1 - 2*M/r
Gschw, _, _ = einstein_mixed(-f, 1/f)
for kk in ['tt', 'rr', 'thth', 'psps']:
    print(f"  Schwarzschild G^{kk} = {Gschw[kk]}  (must be 0)")
ok_schw = all(Gschw[kk] == 0 for kk in Gschw)
print("  SCHWARZSCHILD VALIDATION:", "PASS (G=0)" if ok_schw else "FAIL")

# ===========================================================================
# 2. The UDT soliton metric B=1/A:  g_tt = -e^{-2phi}, g_rr = e^{2phi}.
#    Compute G^t_t, G^r_r symbolically.
# ===========================================================================
print("\n" + "="*78)
print("TASK 3a: analytic forcing -- B=1/A + G^t_t = k8 T^t_t  =>  p_r = -rho ?")
print("="*78)
phi = sp.Function('phi')(r)
gtt = -sp.exp(-2*phi)
grr = sp.exp(2*phi)
Gba, gB, giB = einstein_mixed(gtt, grr)
print("  With B=1/A (g_tt g_rr = -1):")
print("    G^t_t =", sp.simplify(Gba['tt']))
print("    G^r_r =", sp.simplify(Gba['rr']))
diff_ttrr = sp.simplify(Gba['tt'] - Gba['rr'])
print("    G^t_t - G^r_r =", diff_ttrr, " -> identically zero?", diff_ttrr == 0)

# ===========================================================================
# 3. The L2+L4 soliton stress.  Use the committed reduced (rho,p_r) and verify
#    independently the mixed stress T^t_t = -rho, T^r_r = p_r and the EOS.
#    rho,p_r with X=e^{-2phi}Theta'^2, Y=sin^2 Theta / r^2.
# ===========================================================================
Th = sp.Function('Theta')(r)
Thp = sp.diff(Th, r)
X = sp.exp(-2*phi)*Thp**2
Y = sp.sin(Th)**2/r**2
rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
p_r = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
eos = sp.simplify(p_r + rho)
print("\n  L2+L4 soliton EOS:  p_r + rho =", eos)
print("    -> factored:", sp.factor(eos))
print("    p_r = -rho  iff  X=0 (Theta'=0, the exterior).  In body X>0 => p_r != -rho.")

# The forcing: if metric is B=1/A and G^t_t = k8 T^t_t = -k8 rho, and G^t_t=G^r_r
# (shown above), then G^r_r = -k8 rho.  Einstein (r,r): G^r_r = k8 T^r_r = k8 p_r.
# => -k8 rho = k8 p_r => p_r = -rho.  So (r,r) DEMANDS p_r=-rho.
print("\n  FORCING CHAIN (independent):")
print("    (i) B=1/A  => G^t_t = G^r_r  (shown: G^t_t - G^r_r = 0).")
print("    (ii) impose (t,t): G^t_t = k8 T^t_t = -k8 rho.")
print("    (iii) then G^r_r = -k8 rho automatically.")
print("    (iv) full (r,r): G^r_r = k8 T^r_r = k8 p_r.")
print("    => k8 p_r = -k8 rho  => p_r = -rho REQUIRED for (r,r).")
print("    But soliton has p_r + rho = X(xi+2 kap Y) > 0 in body => (r,r) MUST fail.")
print("    => the B=1/A over-imposition IS a real cause (analytically forced).")

# ===========================================================================
# 4. CANON CHECK: does T^t_t = T^r_r hold for the FULL L2+L4 twisted stress?
#    T^t_t = -rho, T^r_r = p_r.  Equal iff -rho = p_r iff p_r+rho=0 iff X=0.
# ===========================================================================
print("\n" + "="*78)
print("TASK 4: canon C-2026-06-14-1 -- does T^t_t = T^r_r in the twisted body?")
print("="*78)
Ttt = sp.simplify(-rho)   # mixed T^t_t = -rho (static)
Trr = sp.simplify(p_r)    # mixed T^r_r = p_r
dT = sp.simplify(Ttt - Trr)
print("  T^t_t - T^r_r = -(p_r+rho) =", sp.factor(dT))
print("  -> equals 0 IFF Theta'=0 (purely angular). With radial twist (Theta'!=0): NONZERO.")
print("  => canon 'T^t_t=T^r_r inside matter' holds ONLY for purely-angular (Theta'=0);")
print("     the L2+L4 sized soliton (Theta'!=0 in body) has T^t_t != T^r_r => B=1/A softened.")
print("     This is EXACTLY the EOS-softening refinement; the refinement SURVIVES.")
