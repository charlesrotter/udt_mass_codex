#!/usr/bin/env python3
"""
gravity_sector_vacuum_solve.py

Decisive vacuum test using the FULL COVARIANT field equations (NOT the
minisuperspace reduced EL, which loses the Hamiltonian/constraint in the
locked single-DOF ansatz -- documented pitfall).

Full scalar-tensor vacuum equation (phi treated as the field appearing in f):
    f G_mu_nu + (g_mu_nu Box - nabla_mu nabla_nu) f  -  (1/2) g_mu_nu * 0  = 0   (no scalar potential, no kinetic in JORDAN action as written)
Actually the action as written in the doc is S = int sqrt(-g)[ f(phi) R + L_m ]
with NO explicit (grad phi)^2 kinetic term and NO potential. So phi has NO
kinetic term of its own in the Jordan action -- it enters ONLY through f(phi)R.
=> Varying w.r.t. g:   f G_mn + (g Box - nabla nabla) f = (1/2) T_mn      (metric eqn)
=> Varying w.r.t. phi (as independent): f'(phi) R = 0  (the phi eqn!), since
   d/dphi [ sqrt(-g) f(phi) R ] = sqrt(-g) f'(phi) R.  With f' != 0 this forces R=0.

We compute BOTH and check consistency on the SSS ansatz.

We test THREE phi-status scenarios honestly:
  (S1) phi INDEPENDENT field (generic Brans-Dicke-like, no kinetic): metric eqn
       f G + (gBox-nablanabla)f = 0 AND phi-eqn f' R = 0.
  (S2) phi SLAVED to metric (phi = -1/2 ln(N/c0^2)): only the metric eqn, phi
       not varied independently. Does Schwarzschild survive?
  (S3) The doc's claim: divide by f, drop E -> G=0 -> Schwarzschild.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
phi = sp.Function('phi')(r)
c0, G, rs = sp.symbols('c0 G r_s', positive=True)

gtt = -sp.exp(-2*phi)*c0**2
grr =  sp.exp( 2*phi)
g = sp.diag(gtt, grr, r**2, r**2*sp.sin(th)**2)
coords=[t,r,th,ph]; ginv=g.inv(); n=4

Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
  for b in range(n):
    for c in range(n):
      s=0
      for d in range(n):
        s+=ginv[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
      Gam[a][b][c]=sp.simplify(s/2)
Ric=sp.zeros(n,n)
for b in range(n):
  for d in range(n):
    s=0
    for a in range(n):
      s+=sp.diff(Gam[a][b][d],coords[a])-sp.diff(Gam[a][b][a],coords[d])
      for e in range(n):
        s+=Gam[a][a][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][a]
    Ric[b,d]=sp.simplify(s)
R=sp.simplify(sum(ginv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
Gdown=Ric-sp.Rational(1,2)*g*R
Gmix=sp.zeros(n,n)
for a in range(n):
  for b in range(n):
    Gmix[a,b]=sp.simplify(sum(ginv[a,c]*Gdown[c,b] for c in range(n)))

f=sp.exp(-8*phi)*c0**4/(16*sp.pi*G)
df=[sp.diff(f,coords[mu]) for mu in range(n)]
Hess=sp.zeros(n,n)
for mu in range(n):
  for nu in range(n):
    s=sp.diff(df[nu],coords[mu])
    for l in range(n):
      s-=Gam[l][mu][nu]*df[l]
    Hess[mu,nu]=sp.simplify(s)
Boxf=sp.simplify(sum(ginv[mu,nu]*Hess[mu,nu] for mu in range(n) for nu in range(n)))
Edown=sp.zeros(n,n)
for mu in range(n):
  for nu in range(n):
    Edown[mu,nu]=sp.simplify(g[mu,nu]*Boxf-Hess[mu,nu])
Emix=sp.zeros(n,n)
for a in range(n):
  for b in range(n):
    Emix[a,b]=sp.simplify(sum(ginv[a,c]*Edown[c,b] for c in range(n)))

# full metric eqn components (vacuum): EQ^a_a = f G^a_a + E^a_a = 0
print("="*70); print("FULL VACUUM METRIC EQUATION  f G^a_a + E^a_a = 0"); print("="*70)
EQ=[sp.simplify((Gmix[a,a]*f+Emix[a,a])) for a in range(n)]
for a,name in enumerate(['tt','rr','thth','pp']):
  print(f"EQ_{name} =", sp.simplify(EQ[a]/f))   # divide by f for readability

# The phi EOM (S1): f'(phi) R = 0
print("\n=== phi EOM (S1, phi independent):  f'(phi) R = 0  =>  R = 0 (since f'!=0) ===")
print("R =", sp.simplify(R))

# Test Schwarzschild profile
phi_schw = -sp.Rational(1,2)*sp.log(1 - rs/r)
print("\n=== Does SCHWARZSCHILD phi = -1/2 ln(1-rs/r) solve them? ===")
for a,name in enumerate(['tt','rr','thth','pp']):
  val=sp.simplify((EQ[a]/f).subs(phi,phi_schw).doit())
  print(f"  EQ_{name}(schw) =", sp.simplify(val))
Rschw=sp.simplify(R.subs(phi,phi_schw).doit())
print("  R(schw) =", Rschw, "  (Schwarzschild is Ricci-flat => R=0, consistent with phi-eqn)")

# So the phi-eqn R=0 is SATISFIED by Schwarzschild. But the metric eqn has extra E.
# Check: is the FULL metric eqn satisfied by Schwarzschild? (E terms nonzero there!)
print("\n=== KEY: with R=0 (Schwarzschild), the metric eqn reduces to E^a_a = 0? ===")
for a,name in enumerate(['tt','rr','thth','pp']):
  # G=0 on schw, so EQ = E. check E on schw:
  val=sp.simplify(Emix[a,a].subs(phi,phi_schw).doit())
  print(f"  E_{name}(schw) =", sp.simplify(val))

# Now SOLVE the full vacuum system honestly. Two independent eqns (tt and thth);
# tt-rr gives a 2nd order ODE. Let's find the ODE and attempt asymptotically-flat soln.
print("\n"+"="*70)
print("SOLVE: the full vacuum ODEs for phi(r)")
print("="*70)
eq_tt = sp.simplify(sp.expand(EQ[0]/f * r**2 * sp.exp(2*phi)))
eq_th = sp.simplify(sp.expand(EQ[2]/f * r * sp.exp(2*phi)))
print("eq_tt (xr^2 e^2phi) = 0:", eq_tt)
print("eq_th (xr e^2phi)   = 0:", eq_th)

# Combine to eliminate phi'' : try to see if constant-phi or power-law works.
# Trivial check: phi=const ?
for trial,name in [(sp.Integer(0),'phi=0 (flat)')]:
  vtt=sp.simplify(eq_tt.subs(phi,trial).doit())
  vth=sp.simplify(eq_th.subs(phi,trial).doit())
  print(f"  trial {name}: eq_tt={vtt}, eq_th={vth}")

# numeric shoot: see if a nontrivial asymptotically-flat (phi->0) solution exists
print("\n=== Numerical check: integrate the tt-rr 2nd-order ODE outward ===")
phif=sp.Function('phi')
ttmrr = sp.simplify(((EQ[0]-EQ[1])/f))
print("tt-rr (=0):", sp.simplify(ttmrr))
