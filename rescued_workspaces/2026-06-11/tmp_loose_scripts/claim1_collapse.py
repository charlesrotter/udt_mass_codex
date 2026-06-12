import sympy as sp

# ---- Source collapse: delta S_matter/delta phi = -(1/2) T^{mu nu} (dg_{mu nu}/dphi) sqrt(-g)
# Metric: g_tt = -e^{-2phi}, g_rr = e^{2phi}, g_thth = r^2, g_phph = r^2 sin^2 th
phi, r, th = sp.symbols('phi r theta', real=True)

g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()

# dg_{mu nu}/dphi
dg = sp.diff(g, phi)
print("dg_tt/dphi =", sp.simplify(dg[0,0]), " expected 2 e^{-2phi}:", sp.simplify(dg[0,0]-2*sp.exp(-2*phi))==0)
print("dg_rr/dphi =", sp.simplify(dg[1,1]), " expected 2 e^{2phi}:", sp.simplify(dg[1,1]-2*sp.exp(2*phi))==0)
print("dg_thth/dphi =", dg[2,2], " dg_phph/dphi =", dg[3,3])

# sqrt(-g)
detg = g.det()
print("det g =", sp.simplify(detg))
sqrtmg = sp.sqrt(-detg)
print("sqrt(-g) =", sp.simplify(sqrtmg))   # should be r^2 sin th  (e^{-2phi}*e^{2phi}=1)

# Now T^{mu nu} dg_{mu nu}/dphi.  We want to express in terms of mixed components T^mu_nu.
# T^{mu nu} dg_{mu nu} = T^{mu nu} g_{mu a} g_{nu b} ... let's just use: for DIAGONAL metric,
# T^{mu nu} dg_{mu nu} = sum_mu T^{mu mu} dg_{mu mu}.
# And T^mu_nu = g_{nu a} T^{mu a}; diagonal => T^mu_mu = g_{mu mu} T^{mu mu} (no sum) => T^{mu mu} = T^mu_mu / g_{mu mu}.
Trr_up, Ttt_up, Tthth_up, Tphph_up = sp.symbols('T^{rr} T^{tt} T^{thth} T^{phph}')
# mixed:
Ttt_mix, Trr_mix, Tthth_mix, Tphph_mix = sp.symbols('Tt_t Tr_r Tth_th Tph_ph')

# T^{mu mu} = T^mu_mu / g_{mu mu}
Ttt_up_expr = Ttt_mix / g[0,0]
Trr_up_expr = Trr_mix / g[1,1]
Tthth_up_expr = Tthth_mix / g[2,2]
Tphph_up_expr = Tphph_mix / g[3,3]

contraction = (Ttt_up_expr*dg[0,0] + Trr_up_expr*dg[1,1]
               + Tthth_up_expr*dg[2,2] + Tphph_up_expr*dg[3,3])
contraction = sp.simplify(contraction)
print("\nT^{mu nu} dg_{mu nu}/dphi =", contraction)

# delta S/delta phi = -(1/2) * contraction * sqrt(-g)
dSdphi = sp.simplify(-sp.Rational(1,2)*contraction*sqrtmg)
print("\ndelta S_matter/delta phi (per the formula) =", dSdphi)
print("  = -sqrt(-g) * [...] where [...] =", sp.simplify(-dSdphi/sqrtmg))
