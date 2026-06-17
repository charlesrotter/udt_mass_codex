# VERIF_with_L4_fluctuation_F3reconcile.py
# Reconcile F3 (l=0 box-controlled under W=e^{2phi}) with #44 (intrinsic breathing).
# #44 used the BREATHING weight W ~ e^{3phi} r^2 (field-space time-kinetic metric)
# and reported RATIOS (R1=om1/om0, R2=om2/om0), which are cell-size INDEPENDENT.
# This run: l=0, WITH L4, flat. Compute the omega^2 tower AND the RATIOS under
# BOTH weights, varying R, to show:
#   - absolute omega^2 ~ 1/R^2 (box) under either weight (the cell sets the scale),
#   - the RATIOS R1,R2 are R-INDEPENDENT (intrinsic shape of the tower) -- that is
#     what #44 reported as "intrinsic", and it is consistent with box-set absolute scale.
# This separates "the tower's SHAPE is intrinsic" (true, #44) from "the lowest
# omega^2 is an intrinsic gap" (FALSE -- it is box-controlled). Honest reconciliation.
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eig
np.set_printoptions(precision=6, linewidth=120)

rs, xi_s, kap_s = sp.symbols('r xi kappa', positive=True)
Tt = sp.Function('T')(rs); phi_s = sp.Function('phi')(rs)
E2 = xi_s*( rs**2*sp.sin(Tt)**2*sp.Derivative(Tt,rs)**2 + 2*rs**2*sp.Derivative(Tt,rs)**2
            + 4*sp.exp(2*phi_s)*sp.sin(Tt)**2 )*sp.exp(-phi_s)
E4 = kap_s*( (2*rs**2*sp.sin(Tt)**4 + 2*rs**2*sp.sin(Tt)**2)*sp.Derivative(Tt,rs)**2
            + sp.exp(2*phi_s)*sp.sin(Tt)**4 )*sp.exp(-phi_s)/rs**2
L = E2+E4
Tp = sp.Derivative(Tt,rs)
EL = sp.diff(sp.diff(L,Tp),rs) - sp.diff(L,Tt)
Tpp = sp.symbols('Tpp'); EL_e = EL.subs(sp.Derivative(Tt,(rs,2)),Tpp)
Tpp_expr = sp.solve(EL_e,Tpp)[0]
Tval,Tpval = sp.symbols('Tval Tpval')
rhs_flat = sp.lambdify((rs,Tval,Tpval), Tpp_expr.subs({phi_s:0,sp.Derivative(phi_s,rs):0,xi_s:1,kap_s:1}).subs({Tt:Tval,Tp:Tpval}),'numpy')

def bc(ya,yb): return np.array([ya[0]-np.pi, yb[0]])
def solve_profile(rc,R,n=4000):
    rmesh=np.linspace(rc,R,n); Tg=np.pi*(1-(rmesh-rc)/(R-rc)); Tpg=-np.pi/(R-rc)*np.ones_like(rmesh)
    def f(r,y): return np.vstack([y[1],rhs_flat(r,y[0],y[1])])
    return solve_bvp(f,bc,rmesh,np.vstack([Tg,Tpg]),tol=1e-8,max_nodes=200000)

def eig_l0(rc,R,sol,N=1000,weight='kg'):
    r=np.linspace(rc,R,N); h=r[1]-r[0]
    Tg=sol.sol(r)[0]; Tpg=sol.sol(r)[1]
    ph=np.zeros_like(r)
    Vcurv = -(Tpg**2 + 2*np.sin(Tg)**2/r**2)   # flat
    c4 = 2*np.sin(Tg)**4 + 2*np.sin(Tg)**2
    if weight=='kg':   W=np.ones_like(r)        # e^{2phi}=1 flat
    else:              W=r**2                    # e^{3phi} r^2 = r^2 flat (#44 breathing)
    n=N; H=np.zeros((n,n)); Wm=np.zeros((n,n))
    a=r**2; pref=1.0/r**2
    for i in range(1,n-1):
        ap=0.5*(a[i]+a[i+1]); am=0.5*(a[i]+a[i-1])
        H[i,i-1]+=-pref[i]*am/h**2; H[i,i]+=pref[i]*(am+ap)/h**2; H[i,i+1]+=-pref[i]*ap/h**2
        H[i,i]+=Vcurv[i]; Wm[i,i]=W[i]
    d2=np.zeros((n,n))
    for i in range(1,n-1): d2[i,i-1]+=1/h**2; d2[i,i]+=-2/h**2; d2[i,i+1]+=1/h**2
    Bih=d2@np.diag(c4)@d2
    for i in range(2,n-2): H[i,:]+=pref[i]*Bih[i,:]
    H[0,:]=0;H[0,0]=1;Wm[0,0]=0; H[-1,:]=0;H[-1,-1]=1;Wm[-1,-1]=0
    H[1,:]=0;H[1,0]=-1;H[1,1]=1;Wm[1,1]=0
    H[-2,:]=0;H[-2,-1]=-1;H[-2,-2]=1;Wm[-2,-2]=0
    w2,_=eig(H,Wm+1e-30*np.eye(n)); w2=np.sort(w2.real[np.isfinite(w2.real)&(np.abs(w2.real)<1e6)])
    return w2

Rs=[8.0,25.0,80.0,250.0]
for weight,lbl in [('kg','W=e^{2phi} (matter-wave/KG charge weight)'),
                    ('breathing','W=e^{3phi}r^2 (#44 breathing field-space weight)')]:
    print("="*70); print(f"l=0 WITH L4, weight: {lbl}"); print("="*70)
    print(f"{'R':>8} {'om0^2':>12} {'om0^2*R^2':>12} {'R1=om1/om0':>12} {'R2=om2/om0':>12}")
    for R in Rs:
        sol=solve_profile(1e-3,R,n=min(4000,int(800*R/8)+1000))
        w2=eig_l0(1e-3,R,sol,N=1000,weight=weight)
        pos=w2[w2>1e-9]
        if len(pos)>=3:
            om=np.sqrt(pos)
            print(f"{R:8.1f} {pos[0]:12.5e} {pos[0]*R**2:12.4f} {om[1]/om[0]:12.5f} {om[2]/om[0]:12.5f}")
print("\nReconciliation: if RATIOS are R-independent but om0^2*R^2 ~ const,")
print("the tower SHAPE is intrinsic (matches #44) while the absolute lowest")
print("omega^2 is BOX-controlled (no intrinsic gap). That is the honest reading.")
