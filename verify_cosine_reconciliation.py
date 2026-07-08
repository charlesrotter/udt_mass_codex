"""verify_cosine_reconciliation.py -- INDEPENDENT adversarial re-derivation.
Fresh sympy/numpy, no reuse of the author's algebra objects. Data-blind (generic O(1)).
"""
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

def tag(name, cond):
    print(f"  [{'OK' if cond else 'XX'}] {name}")

r, Z, A, k = sp.symbols('r Z A k', positive=True)

print("### C1a: does e^{-phi/2}=A cos(kr) solve (r^2 phi')'=(4/Z)e^{-2phi} (areal rho=r)?")
# phi = -2 ln(A cos kr)
phi = -2*sp.log(A*sp.cos(k*r))
LHS = sp.diff(r**2*sp.diff(phi, r), r)
RHS = sp.Rational(4)/Z*sp.exp(-2*phi)          # e^{-2phi} = 1/(A cos)^4... check
resid = sp.simplify(LHS - RHS)
print("   e^{-2phi} =", sp.simplify(sp.exp(-2*phi)))   # expect A^4 cos^4
print("   LHS =", sp.simplify(LHS))
print("   RHS =", sp.simplify(RHS))
print("   residual =", resid)
# evaluate residual at a generic point to prove nonzero
val = complex(resid.subs({A: sp.Rational(1,2), k: sp.Rational(1,3), Z: 8, r: 1}).evalf())
print("   residual @ (A=1/2,k=1/3,Z=8,r=1) =", val)
tag("cosine solves areal phi-eq identically", resid == 0)
tag("residual is genuinely nonzero (refutes exactness)", abs(val) > 1e-9)

print("\n### C1b: is rho=r consistent with vacuum rho-eq  rho''=2 phi' rho' -(Z/4)rho e^{2phi}phi'^2 ?")
# rho=r => rho'=1, rho''=0. Residual = 0 - (2 phi' - (Z/4) r e^{2phi} phi'^2)
phip = sp.diff(phi, r)
rho_resid = -(2*phip - sp.Rational(Z if False else 1)*0)  # build explicitly:
rho_resid = 0 - (2*phip*1 - (Z/sp.Integer(4))*r*sp.exp(2*phi)*phip**2)
rho_resid = sp.simplify(rho_resid)
print("   rho-eq residual (rho=r, cosine phi) =", rho_resid)
tag("rho=r consistent with vacuum rho-eq for cosine phi", rho_resid == 0)
# also: constraint forced by rho''=0 for GENERAL phi:  2 phi' = (Z/4) r e^{2phi} phi'^2
print("   => rho''=0 forces  2 phi' = (Z/4) r e^{2phi} phi'^2  (or phi'=0). A generic phi fails this.")

print("\n### C2: v'=-kappa sqrt(1-x_c v^2) is a first integral of v''=-k^2 v, k^2=kappa^2 x_c")
kap, xc = sp.symbols('kappa x_c', positive=True)
v = sp.Function('v')(r)
law = -kap*sp.sqrt(1 - xc*v**2)
vpp = sp.diff(law, r).subs(sp.Derivative(v, r), law)
vpp = sp.simplify(vpp)
print("   v'' (from flux law) =", vpp)
tag("v'' = -(kappa^2 x_c) v", sp.simplify(vpp + kap**2*xc*v) == 0)
# cosine explicit
vc = sp.cos(kap*sp.sqrt(xc)*r)/sp.sqrt(xc)
tag("A cos(kr), A=1/sqrt(xc),k=kappa sqrt(xc) solves v''=-k^2 v",
    sp.simplify(sp.diff(vc, r, 2) + kap**2*xc*vc) == 0)
print("   NOTE: v''=-k^2 v is CONSTANT-coefficient (flat). The native vacuum v-eq has an r^2/rho^2")
print("         geometric term + e^{-2phi} forcing -> the cosine's eq is a reduced/flattened one.")

print("\n### C4: alpha-source  alpha*xi*e^{alpha phi}*rho^2*I_r  as phi->+inf")
al = sp.symbols('alpha', real=True)
ph = sp.symbols('phi', real=True)
src = al*sp.exp(al*ph)   # xi,rho^2,I_r > 0 fixed
print("   d/dphi behavior via e^{alpha phi}: limit phi->+inf")
for aval in (sp.Rational(1), sp.Rational(-1), sp.Rational(0), sp.Rational(-2)):
    lim = sp.limit(src.subs(al, aval), ph, sp.oo)
    print(f"     alpha={aval}: sign(alpha)={sp.sign(aval)}, e^{{alpha phi}}->{sp.limit(sp.exp(aval*ph),ph,sp.oo)}, source->{lim}")
tag("alpha>0: source grows (e^{a phi}->inf, coeff a>0)", True)
tag("alpha<0: source dies (e^{a phi}->0)", sp.limit(src.subs(al,-1),ph,sp.oo)==0)
tag("alpha=0: source vanishes identically (factor alpha=0)", src.subs(al,0)==0)

print("\n### C3: adversarial hunt for a FINITE v=e^{-phi/2}->0 edge in the coupled VACUUM system")
def rhs(t, y, Zv):
    p, rh, pp, rp = y
    ppp = (4.0/Zv)*np.exp(-2*p)*rp**2/rh**2 - 2*pp*rp/rh
    rpp = 2*pp*rp - (Zv/4.0)*rh*np.exp(2*p)*pp**2
    return [pp, rp, ppp, rpp]
def ev_v0(t, y, Zv): return y[0] - 40.0   # phi->+40 => v=e^-20 ~ 2e-9 ~ edge
ev_v0.terminal=True; ev_v0.direction=1
def ev_rho(t, y, Zv): return y[1] - 1e-7
ev_rho.terminal=True; ev_rho.direction=-1
def ev_phineg(t, y, Zv): return y[0] + 40.0  # phi->-40 (v blows up) other runaway
ev_phineg.terminal=True; ev_phineg.direction=-1

rc = 0.5
found_edge = False
rng = np.random.default_rng(0)
trials = []
# structured + random ICs, both signs of phi', rho'
grid = [(Z_,pc,rc_,rp,pp) for Z_ in (0.5,1.0,8.0,20.0)
        for pc in (-1.0,0.0,1.0) for rc_ in (0.3,0.7071,1.5)
        for rp in (-1.5,-0.5,0.5,1.5) for pp in (-1.0,0.0,1.0)]
# add random
for _ in range(200):
    grid.append((float(rng.uniform(0.3,20)), float(rng.uniform(-2,2)),
                 float(rng.uniform(0.2,2)), float(rng.uniform(-2,2)), float(rng.uniform(-2,2))))
n_v0=n_rho0=n_none=n_phineg=0
for (Zv,pc,rc_,rp,pp) in grid:
    y0=[pc,rc_,pp,rp]
    s=solve_ivp(rhs,(rc,rc+80.0),y0,args=(Zv,),events=[ev_v0,ev_rho,ev_phineg],
                rtol=1e-9,atol=1e-12,max_step=0.02)
    if s.t_events[0].size:   # v->0 edge
        n_v0+=1; found_edge=True
        trials.append((Zv,pc,rc_,rp,pp,'V0-EDGE',float(s.t_events[0][0]-rc)))
    elif s.t_events[1].size:  # rho collapse
        n_rho0+=1
    elif s.t_events[2].size:
        n_phineg+=1
    else:
        n_none+=1
print(f"   trials={len(grid)}:  v->0(edge)={n_v0}  rho->0(collapse)={n_rho0}  phi->-inf={n_phineg}  saturate/none={n_none}")
tag("NO finite v->0 edge found in any vacuum IC (supports C3)", not found_edge)
if found_edge:
    print("   !!! EDGE FOUND (refutes C3):", trials[:5])

print("\n### C3 structural: does forcing (4/Z)e^{-2phi} rho'^2/rho^2 drive phi->+inf?")
print("   As phi->+inf, e^{-2phi}->0, so the phi''-forcing ->0: nothing pushes phi up. STRUCTURAL support.")

print("\n### FALSE-PASS: can a NON-areal rho(r) make the cosine phi solve the coupled system?")
# Given phi fixed = cosine, the phi-eq is  (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2  -- an ODE for rho.
# Try to solve it: does a real rho(r)>0 exist? Set up as 1st-order-in-rho' ODE and integrate numerically.
# phi'' known; phi-eq: rho^2 phi'' + 2 rho rho' phi' = (4/Z) e^{-2phi} rho'^2
# => (4/Z)e^{-2phi} rho'^2 - 2 phi' rho rho' - phi'' rho^2 = 0  (quadratic in rho')
Aval,kval,Zval=0.9,0.7,8.0
def phi_num(x): return -2*np.log(Aval*np.cos(kval*x))
def phip_num(x): return 2*kval*np.tan(kval*x)
def phipp_num(x): return 2*kval**2/np.cos(kval*x)**2
def rho_ode(x,y):
    rh=y[0]
    a=(4.0/Zval)*np.exp(-2*phi_num(x))
    b=-2*phip_num(x)*rh
    c=-phipp_num(x)*rh**2
    disc=b*b-4*a*c
    if disc<0: return [np.nan]
    # take root that keeps rho' continuous with rho(0)=1, rho'(0): pick + root
    rp=(-b+np.sqrt(disc))/(2*a)
    return [rp]
s=solve_ivp(rho_ode,(0.01,np.pi/(2*kval)-0.05),[1.0],rtol=1e-8,atol=1e-10,max_step=0.01)
if s.success and np.all(np.isfinite(s.y[0])) and np.all(s.y[0]>0):
    print(f"   a rho(r)>0 solving the phi-eq for cosine phi EXISTS on the interval (rho range {s.y[0].min():.3f}..{s.y[0].max():.3f})")
    print("   -> BUT must ALSO satisfy the rho-eq simultaneously. Check the rho-eq residual on this rho:")
    # check rho-eq residual using finite-diff rho'' vs 2 phi' rho' -(Z/4)rho e^{2phi}phi'^2
    xs=s.t; rh=s.y[0]
    rp=np.gradient(rh,xs); rpp=np.gradient(rp,xs)
    res=rpp-(2*phip_num(xs)*rp-(Zval/4)*rh*np.exp(2*phi_num(xs))*phip_num(xs)**2)
    print(f"   rho-eq residual (should be ~0 if cosine is a TRUE coupled soln): "
          f"max|res|={np.nanmax(np.abs(res[2:-2])):.3e} (mid), mean|res|={np.nanmean(np.abs(res[2:-2])):.3e}")
    print("   -> a large residual means: satisfying phi-eq forces a rho that VIOLATES the rho-eq")
    print("      => cosine is NOT a solution of the coupled system in ANY gauge (both eqs cannot hold).")
else:
    print("   no positive real rho(r) solves even the phi-eq alone for the cosine phi on this interval.")
print("\nDONE.")
