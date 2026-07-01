import sympy as sp
r=sp.symbols('r',real=True,positive=True)
phi=sp.Function('phi')(r)
c0,G,muc=sp.symbols('c0 G mu',positive=True)

# From einstein_probe: independent G^mu_nu (mixed)
Gtt=(-2*r*sp.diff(phi,r)-sp.exp(2*phi)+1)*sp.exp(-2*phi)/r**2
Grr=Gtt
Gthth=(2*r*sp.diff(phi,r)**2 - r*sp.diff(phi,r,2) - 2*sp.diff(phi,r))*sp.exp(-2*phi)/r
boxphi=-Gthth  # identity

print("################ ROUTE A/D: what does the GEOMETRY itself contain? ################")
print("Is there ANY 0th-order (phi with no derivative) term anywhere in G^mu_nu?")
print("G^t_t terms:", sp.srepr(sp.expand(Gtt*r**2*sp.exp(2*phi))))
print()
# The only non-derivative phi-dependence is via exp(2phi) (a metric warp factor),
# NOT a bare 'phi'. A 'mu^2 * phi' term is ALGEBRAIC-LINEAR in phi. Does it occur? 
# Test: can Gthth (=-Box phi) be written with a bare +mu^2*phi term? 
print("Box_g phi (=-G^th_th):")
print(sp.expand(boxphi*r*sp.exp(2*phi)/1))
print(" -> pure derivative operator on phi (phi'', phi', (phi')^2). NO bare 'phi'.")
print()

print("################ Conservation / Bianchi with VARYING c(phi) ################")
# physical source in ENERGY units: T^mu_nu_phys = (c(phi)^4/8piG) G^mu_nu, c=c0 e^{-2phi}
cphi=c0*sp.exp(-2*phi)
Tfac=cphi**4/(8*sp.pi*G)
# covariant conservation nabla_mu G^mu_nu =0 is identity (geometry). 
# But nabla_mu (f(phi) G^mu_nu) with f=c(phi)^4 varying:  the EXTRA piece is (d f) G.
# nabla_mu(f G^mu_r) = f nabla_mu G^mu_r + (partial_mu f) G^mu_r
# geometry: nabla_mu G^mu_r =0. So divergence of physical-source = (f' ) G^r_r-type terms.
# Build the r-component of nabla_mu(f G^mu_nu):
# For diagonal mixed tensor A^mu_nu, (nabla_mu A^mu_r) = (1/sqrt-g)d_mu(sqrt-g A^mu_r) - (1/2)A^ab d_r g_ab ... 
# Simpler: just report the EXTRA term f' * G that varying-c injects, vs constant-c.
fprime=sp.diff(Tfac,r)
extra=sp.simplify(fprime*Grr)   # the bare derivative-of-coefficient injection in the r-eqn
print("d/dr[c(phi)^4/8piG] * G^r_r  (the varying-c injection into conservation):")
print(sp.simplify(extra/Tfac))   # normalized
print(" -> proportional to phi' * G^r_r ; this is a DERIVATIVE-of-phi term, NOT a bare mu^2*phi.")
