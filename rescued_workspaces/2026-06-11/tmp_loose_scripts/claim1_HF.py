import sympy as sp
# Independently reproduce the Hellmann-Feynman derivation of (T^r_r - T^t_t) from the Form-T action,
# WITHOUT copying their grouping. Build the symmetrized first-order Dirac Lagrangian density directly.
r=sp.symbols('r',positive=True)
G=sp.Function('G')(r); F=sp.Function('F')(r)
PHI=sp.Function('Phi')(r); PHIp=sp.diff(PHI,r)
E,m,kap=sp.symbols('E m kappa',real=True)
eP=sp.exp(PHI); e2P=sp.exp(2*PHI)

# The first-order system:
#  G' = (PHI' - k/r)G + (E e^{2PHI}+ m e^{PHI})F
#  F' = (PHI' + k/r)F - (E e^{2PHI}- m e^{PHI})G
# Symmetrized Lagrangian (Lagrange-multiplier / first-order Dirac form):
# L = G*(G' - RHS_G) + F*(F' - RHS_F)   [their eq line 191-193]
RHS_G = (PHIp - kap/r)*G + (E*e2P + m*eP)*F
RHS_F = (PHIp + kap/r)*F - (E*e2P - m*eP)*G
L = G*(sp.diff(G,r) - RHS_G) + F*(sp.diff(F,r) - RHS_F)
L = sp.expand(L)
print("L (full) =", L)

# Hellmann-Feynman: source = delta L / delta phi, with PHI = sigma*phi.
# Functional derivative wrt phi treating G,F as fixed (on-shell, by HF theorem):
# delta S/delta phi = dL/dphi (explicit) - d/dr( dL/d phi' ).
# Express L's phi dependence: PHI and PHIp. PHI=sigma*phi => dPHI/dphi=sigma, dPHIp/dphi'=sigma.
sigma=sp.symbols('sigma')
Phi_s, Phip_s = sp.symbols('Phi_s Phip_s', real=True)
Ls = L.subs({PHIp:Phip_s, PHI:Phi_s})
# Only keep the explicit-phi part; the kinetic G',F' terms have no phi. 
dL_dPhi  = sp.diff(Ls, Phi_s)
dL_dPhip = sp.diff(Ls, Phip_s)
print("\ndL/dPhi  =", sp.simplify(dL_dPhi))
print("dL/dPhip =", sp.simplify(dL_dPhip))

# delta S/delta phi density = sigma*(dL/dPhi) - d/dr( sigma*dL/dPhip )
# restore PHI,PHIp:
dL_dPhi_r  = dL_dPhi.subs({Phi_s:PHI, Phip_s:PHIp})
dL_dPhip_r = dL_dPhip.subs({Phi_s:PHI, Phip_s:PHIp})
deltaS = sigma*dL_dPhi_r - sigma*sp.diff(dL_dPhip_r, r)
deltaS = sp.expand(deltaS)
# eliminate G',F' on-shell:
deltaS_os = deltaS.subs({sp.diff(G,r):RHS_G, sp.diff(F,r):RHS_F})
deltaS_os = sp.expand(deltaS_os)
print("\ndelta S_D/delta phi (on-shell) =", sp.simplify(deltaS_os))

# (T^r_r - T^t_t) = - delta S/delta phi   (per collapse, /sqrt(-g) absorbed in measure)
src = sp.simplify(-deltaS_os)
print("\n(T^r_r - T^t_t) =", sp.factor(src))

# Compare to claim: -2 sigma [ kappa(F^2-G^2)/r + PHI'(F^2+G^2) + m e^{PHI} GF ]
claim = -2*sigma*( kap*(F**2-G**2)/r + PHIp*(F**2+G**2) + m*eP*G*F )
print("\nclaim =", sp.factor(sp.expand(claim)))
print("\nsrc - claim =", sp.simplify(src - claim))
