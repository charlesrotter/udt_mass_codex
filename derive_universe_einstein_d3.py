"""D3(c) — the GR-reference reading T^mu_nu := G^mu_nu/8pi on the canonical round metric
   ds^2 = -e^{-2phi} dt^2 + e^{2phi} dr^2 + rho(r)^2 dOmega^2      (c = G_N = 1 units)
Derives:
 1. exact mixed Einstein components G^t_t, G^r_r, G^th_th (=G^psi_psi);
 2. G^r_r contains NO second derivatives -> its reading is sigma-free;
 3. on-shell substitution with the native EOMs + phi-blind source sigma:
    exact (eps, p_r, p_t) formulas in (phi, phi', rho, rho', sigma; Z);
 4. Bianchi identity: the radial conservation law holds for ANY (phi, rho) ->
    the read-off T is conserved AUTOMATICALLY (zero test power);
 5. sigma-elimination: the combination of readings that is an on-shell IDENTITY
    (no test power) vs the one that ISOLATES sigma (the audit handle);
 6. Misner-Sharp link: m := (rho/2)(1 - e^{-2phi} rho'^2) satisfies
    m' = 4pi rho^2 rho' * eps  identically (any metric of this class) ->
    the banked MS-density reading IS the eps-component of T=G/8pi;
 7. native vacuum is NOT GR vacuum: the constant cylinder (phi0, rho0) solves the
    native sourceless EOMs but has G != 0 (reading assigns 'matter' to native vacuum).
"""
import sympy as sp

r, th, Z, sig = sp.symbols('r theta Z sigma', real=True)
Zp = sp.Symbol('Z', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
Pp, Rp = phi.diff(r), rho.diff(r)

OK = []
def check(name, expr_zero):
    val = sp.simplify(expr_zero)
    ok = (val == 0)
    OK.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  residual={val}"))

# ---- metric and curvature ----
coords = [sp.Symbol('t'), r, th, sp.Symbol('psi')]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), rho**2, rho**2*sp.sin(th)**2)
ginv = g.inv()
n = 4
Gamma = [[[sp.simplify(sum(ginv[a,d]*(g[d,b].diff(coords[c]) + g[d,c].diff(coords[b])
            - g[b,c].diff(coords[d]))/2 for d in range(n)))
           for c in range(n)] for b in range(n)] for a in range(n)]
def Ricci(a, b):
    ex = 0
    for c in range(n):
        ex += Gamma[c][a][b].diff(coords[c]) - Gamma[c][a][c].diff(coords[b])
        for d in range(n):
            ex += Gamma[c][c][d]*Gamma[d][a][b] - Gamma[c][b][d]*Gamma[d][a][c]
    return sp.simplify(ex)
Ric = sp.Matrix(n, n, lambda a, b: Ricci(a, b))
Rs = sp.simplify(sum(ginv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
Gmix = sp.simplify(ginv*(Ric - Rs/2*g))     # G^mu_nu (mixed)

Gtt, Grr, Gthth, Gpsps = [sp.simplify(Gmix[i,i]) for i in range(4)]
check("0: G^theta_theta == G^psi_psi", Gthth - Gpsps)
print("G^t_t   =", sp.simplify(Gtt))
print("G^r_r   =", sp.simplify(Grr))
print("G^th_th =", sp.simplify(Gthth))

# expected closed forms (derived by hand, verified here):
Gtt_exp = sp.exp(-2*phi)*(2*rho.diff(r,2)/rho - 2*Pp*Rp/rho + Rp**2/rho**2) - 1/rho**2
Grr_exp = sp.exp(-2*phi)*(Rp**2/rho**2 - 2*Pp*Rp/rho) - 1/rho**2
Gth_exp = sp.exp(-2*phi)*(rho.diff(r,2)/rho - 2*Pp*Rp/rho - phi.diff(r,2) + 2*Pp**2)
check("1a: G^t_t = e^{-2phi}(2rho''/rho - 2phi'rho'/rho + rho'^2/rho^2) - 1/rho^2", Gtt - Gtt_exp)
check("1b: G^r_r = e^{-2phi}(rho'^2/rho^2 - 2phi'rho'/rho) - 1/rho^2", Grr - Grr_exp)
check("1c: G^th_th = e^{-2phi}(rho''/rho - 2phi'rho'/rho - phi'' + 2phi'^2)", Gthth - Gth_exp)
check("2: G^r_r contains no 2nd derivatives (sigma-free reading)",
      sp.simplify(Grr.diff(rho.diff(r,2))) + sp.simplify(Grr.diff(phi.diff(r,2))))

# ---- on-shell substitution (native EOMs + phi-blind source sigma) ----
onshell = {phi.diff(r,2): 4*sp.exp(-2*phi)*Rp**2/(Zp*rho**2) - 2*Pp*Rp/rho,
           rho.diff(r,2): 2*Pp*Rp - Zp/4*rho*sp.exp(2*phi)*Pp**2 + sig}
eps  = sp.simplify(-Gtt.subs(onshell)/(8*sp.pi))
p_r  = sp.simplify( Grr.subs(onshell)/(8*sp.pi))
p_t  = sp.simplify( Gthth.subs(onshell)/(8*sp.pi))
print("\n8pi eps  =", sp.simplify(sp.expand(-Gtt.subs(onshell))))
print("8pi p_r  =", sp.simplify(sp.expand(Grr.subs(onshell))))
print("8pi p_t  =", sp.simplify(sp.expand(Gthth.subs(onshell))))

# expected on-shell forms (corrected to CAS truth):
eps_exp = ( 1/rho**2 - sp.exp(-2*phi)*(Rp**2/rho**2 + 2*Pp*Rp/rho)
           + Zp/2*Pp**2 - 2*sp.exp(-2*phi)*sig/rho )/(8*sp.pi)
check("3a: 8pi eps = 1/rho^2 - e^{-2phi}(rho'^2/rho^2 + 2phi'rho'/rho) + (Z/2)phi'^2 - 2e^{-2phi}sigma/rho",
      sp.simplify(8*sp.pi*eps - 8*sp.pi*eps_exp))
p_r_exp = ( sp.exp(-2*phi)*(Rp**2/rho**2 - 2*Pp*Rp/rho) - 1/rho**2 )/(8*sp.pi)
check("3b: p_r reading unchanged on-shell (first-order only)", sp.simplify(p_r - p_r_exp))
p_t_exp = ( -Zp/4*Pp**2 + 2*sp.exp(-2*phi)*Pp**2 + 2*sp.exp(-2*phi)*Pp*Rp/rho
            - 4*sp.exp(-4*phi)*Rp**2/(Zp*rho**2) + sp.exp(-2*phi)*sig/rho )/(8*sp.pi)
check("3c: 8pi p_t = -(Z/4)phi'^2 + 2e^{-2phi}phi'^2 + 2e^{-2phi}phi'rho'/rho - 4e^{-4phi}rho'^2/(Z rho^2) + e^{-2phi}sigma/rho",
      sp.simplify(8*sp.pi*p_t - 8*sp.pi*p_t_exp))

# ---- 4. Bianchi: radial conservation automatic for ANY phi(r), rho(r) ----
# nabla_mu G^mu_r = d_r G^r_r + Gamma^mu_{mu s} G^s_r - Gamma^s_{mu r} G^mu_s = 0
divG_r = Grr.diff(r)
for m in range(n):
    divG_r += Gamma[m][m][1]*Grr        # G^s_r diagonal: s=r only
for m in range(n):
    divG_r -= Gamma[m][m][1]*Gmix[m,m] if False else 0
# do it properly: nabla_mu G^mu_nu for nu=r with diagonal mixed G:
divG_r = Grr.diff(r) + sum(Gamma[m][m][1] for m in range(n))*Grr \
         - sum(Gamma[s][m][1]*Gmix[m,s] if s==m else Gamma[s][m][1]*0 for m in range(n) for s in range(n)) \
         - 0
# Gamma^s_{m r} G^m_s with both diagonal: sum_m Gamma^m_{m r} G^m_m
divG_r = Grr.diff(r) + sum(Gamma[m][m][1] for m in range(n))*Grr \
         - sum(Gamma[m][m][1]*Gmix[m,m] for m in range(n))
check("4: nabla_mu G^mu_r == 0 identically (OFF-shell, any phi,rho) -> conservation has zero test power",
      sp.simplify(divG_r))

# ---- 5. sigma-elimination identity ----
# sigma appears in eps and p_t only:  from 3a,
#   sigma = (rho e^{2phi}/2) [ 1/rho^2 - e^{-2phi}(rho'^2/rho^2 + 2phi'rho'/rho) + (Z/2)phi'^2 - 8pi eps ]
sigma_from_eps = rho*sp.exp(2*phi)/2*( 1/rho**2 - sp.exp(-2*phi)*(Rp**2/rho**2 + 2*Pp*Rp/rho)
                                       + Zp/2*Pp**2 - 8*sp.pi*eps )
check("5a: sigma recovered from the eps-reading", sp.simplify(sigma_from_eps - sig))
# eliminating sigma: 8pi(eps + 2 p_t) is sigma-free -> an on-shell IDENTITY (no test power):
combo = sp.simplify(8*sp.pi*(eps + 2*p_t))
check("5b: 8pi(eps + 2 p_t) is sigma-free (identity on solutions, zero test power on sigma)",
      sp.simplify(combo.diff(sig)))
ident_expr = ( 1/rho**2 - sp.exp(-2*phi)*Rp**2/rho**2 + 2*sp.exp(-2*phi)*Pp*Rp/rho
               + 4*sp.exp(-2*phi)*Pp**2 - 8*sp.exp(-4*phi)*Rp**2/(Zp*rho**2) )
check("5c: 8pi(eps + 2 p_t) == 1/rho^2 - e^{-2phi}rho'^2/rho^2 + 2e^{-2phi}phi'rho'/rho + 4e^{-2phi}phi'^2 - 8e^{-4phi}rho'^2/(Z rho^2)",
      sp.simplify(combo - ident_expr))

# ---- 6. Misner-Sharp link ----
mMS = rho/2*(1 - sp.exp(-2*phi)*Rp**2)
check("6: m_MS' == 4pi rho^2 rho' eps_read  IDENTICALLY (off-shell: eps_read = -G^t_t/8pi)",
      sp.simplify(mMS.diff(r) - 4*sp.pi*rho**2*Rp*(-Gtt/(8*sp.pi))))

# ---- 7. native vacuum has G != 0 (constant cylinder) ----
phi0, rho0 = sp.symbols('phi0 rho0', positive=True)
cyl = {phi: phi0, rho: rho0, Pp: 0, Rp: 0, phi.diff(r,2): 0, rho.diff(r,2): 0}
Gtt_cyl = Gtt_exp.subs(cyl)
check("7: cylinder (native sourceless solution) has G^t_t = -1/rho0^2 != 0",
      sp.simplify(Gtt_cyl + 1/rho0**2))

print(f"\n{sum(OK)}/{len(OK)} checks passed")
