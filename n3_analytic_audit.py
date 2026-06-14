#!/usr/bin/env python3
"""
n3_analytic_audit.py — analytic cross-check of the split + easy-axis mechanism.

For the easy-axis hedgehog n=(sinTheta(r) sinth cosph, sinTheta(r) sinth sinph,
cosTheta(r)), do the theta,phi integrals of the L2 iso-inertia ANALYTICALLY (by
hand / sympy) and confirm the numeric perp/along-3 split.  This proves the split
is real (not an integrator artifact) and exposes the mechanism in closed form.

v_3 = e_3 x n = (-n2, n1, 0) = sinTheta(r)*(-st sp, st cp, 0)  [spins the (n1,n2)
   winding phase; magnitude sinTheta(r)*sin th, INDEPENDENT of the radial twist
   Theta'(r): v_3 has NO d_r component coupling, it is a pure phase rotation]
v_1 = e_1 x n = (0,-n3,n2)=(0,-cosTheta, sinTheta st sp)  [TILTS the easy axis;
   couples to the radial profile]

L2 inertia density (flat, xi): (xi/2) sqrt(g) (v_a.v_a), sqrt(g)=r^2 sin th.
  |v_3|^2 = sin^2Theta(r) sin^2 th
  |v_1|^2 = cos^2Theta(r) + sin^2Theta(r) sin^2 th sin^2 ph
Integrate over th in [0,pi], ph in [0,2pi]:
  INT |v_3|^2 dOmega = sin^2Theta(r) * INT sin^2 th dOmega
  INT |v_1|^2 dOmega = INT cos^2Theta dOmega + sin^2Theta INT sin^2 th sin^2 ph dOmega
We compute these with sympy and assemble Lambda_33, Lambda_11 as 1D radial
integrals over the BVP profile, then compare to the 3D GPU numbers.
"""
import math, numpy as np, sympy as sp

th,ph,T=sp.symbols('theta phi Theta',positive=True)
dO=sp.sin(th)
# v3.v3 and v1.v1 angular integrands (times sin th measure)
v3sq=(sp.sin(T)**2*sp.sin(th)**2)
v1sq=(sp.cos(T)**2 + sp.sin(T)**2*sp.sin(th)**2*sp.sin(ph)**2)
I3=sp.integrate(sp.integrate(v3sq*dO,(ph,0,2*sp.pi)),(th,0,sp.pi))
I1=sp.integrate(sp.integrate(v1sq*dO,(ph,0,2*sp.pi)),(th,0,sp.pi))
print("ANGULAR INTEGRALS (L2, flat), as functions of Theta(r):")
print("  INT |v_3|^2 dOmega =", sp.simplify(I3))
print("  INT |v_1|^2 dOmega =", sp.simplify(I1))
# => Lambda_33^{L2} = (xi/2) INT_r r^2 I3(Theta(r)) dr ; Lambda_11 similarly with I1
I3f=sp.lambdify(T,I3,'numpy'); I1f=sp.lambdify(T,I1,'numpy')

# Now build the BVP profile and do the radial integral, compare to GPU run.
import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
from scipy.integrate import solve_bvp
def theta_ddot(r,Th,Thp,phi,phip,xi,kappa):
    s=np.sin(Th)
    num=((0.5)*Thp*r**2*(-4*Thp*kappa*np.sin(2*Th)+Thp*kappa*np.sin(4*Th)
        -Thp*r**2*xi*np.sin(2*Th)+kappa*phip*(1-np.cos(2*Th))**2
        -2*kappa*phip*np.cos(2*Th)+2*kappa*phip-phip*r**2*xi*np.cos(2*Th)
        +5*phip*r**2*xi+2*r*xi*np.cos(2*Th)-10*r*xi)
        +2*kappa*np.exp(2*phi)*s**3*np.cos(Th)+2*r**2*xi*np.exp(2*phi)*np.sin(2*Th))
    den=r**2*(2*kappa*s**4+2*kappa*s**2+r**2*xi*s**2+2*r**2*xi)
    return num/den
xi=1.0; kappa=1.0; r_core=0.05; r_int=r_core+12.0
x0=np.linspace(r_core,r_int,500)
def rhs(r,y): return np.vstack([y[1],theta_ddot(r,y[0],y[1],0*r,0*r,xi,kappa)])
def bc(ya,yb): return np.array([ya[0]-math.pi,yb[0]-0.0])
Th0=math.pi*0.5*(1-np.tanh((x0-(r_core+2.0))/0.8))
sol=solve_bvp(rhs,bc,x0,np.vstack([Th0,np.gradient(Th0,x0)]),tol=1e-8,max_nodes=200000)
rg=np.linspace(r_core,r_int,4000); Th=sol.sol(rg)[0]
Lam33=(xi/2.0)*np.trapz(rg**2*I3f(Th),rg)
Lam11=(xi/2.0)*np.trapz(rg**2*I1f(Th),rg)
print(f"\nL2-only, analytic-angular x numeric-radial (flat, kappa=xi=1, cell=12L):")
print(f"  Lambda_33 (along target-3, spins winding phase) = {Lam33:.4f}")
print(f"  Lambda_11 (perp, tilts easy axis)               = {Lam11:.4f}")
print(f"  ratio perp/along3 = {Lam11/Lam33:.4f}")
print(f"  (GPU 3D L2-only gave perp=3655.75, along3=8.806, ratio=415.1 — compare)")
print("\nMECHANISM (closed form): INT|v_3|^2 ~ sin^2Theta(r) (LOCALIZED to the")
print("twist region, where sinTheta!=0); INT|v_1|^2 ~ cos^2Theta(r) which -> 1 in")
print("the ENTIRE unwound exterior (Theta->0), so Lambda_perp picks up the whole")
print("cell volume (cell-size divergent), while Lambda_along3 is soliton-localized.")
print("=> the split is the easy-axis (n3=cosTheta) structure of the native ansatz.")
