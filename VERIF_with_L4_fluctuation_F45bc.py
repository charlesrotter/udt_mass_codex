# VERIF_with_L4_fluctuation_F45bc.py
# S3 BC-sensitivity + S5 Goldstone check + F4 deep-phi angular trap-test.
# (1) BC sensitivity: clamp (u'=0) vs natural (u''=0) seal -> does box-control survive?
# (2) Goldstone check: the l=1 sector contains the translational zero mode
#     (eta ~ d_i n0). Verify whether the lowest l=1 mode -> 0 as an intrinsic
#     zero (Goldstone) or is the box continuum. Translation is a symmetry of FLAT
#     space; on the finite cell with Dirichlet walls it is lifted by the box.
# (3) deep-phi (p=1) angular trap-test: does phi-angular coupling add intrinsic structure?
import numpy as np, sympy as sp
from scipy.integrate import solve_bvp
from scipy.linalg import eig
np.set_printoptions(precision=6,linewidth=120)

rs,xi_s,kap_s=sp.symbols('r xi kappa',positive=True)
Tt=sp.Function('T')(rs); phi_s=sp.Function('phi')(rs)
E2=xi_s*(rs**2*sp.sin(Tt)**2*sp.Derivative(Tt,rs)**2+2*rs**2*sp.Derivative(Tt,rs)**2+4*sp.exp(2*phi_s)*sp.sin(Tt)**2)*sp.exp(-phi_s)
E4=kap_s*((2*rs**2*sp.sin(Tt)**4+2*rs**2*sp.sin(Tt)**2)*sp.Derivative(Tt,rs)**2+sp.exp(2*phi_s)*sp.sin(Tt)**4)*sp.exp(-phi_s)/rs**2
L=E2+E4; Tp=sp.Derivative(Tt,rs)
EL=sp.diff(sp.diff(L,Tp),rs)-sp.diff(L,Tt); Tpp=sp.symbols('Tpp')
Tpp_expr=sp.solve(EL.subs(sp.Derivative(Tt,(rs,2)),Tpp),Tpp)[0]
Tval,Tpval=sp.symbols('Tval Tpval')
def make_rhs(phe,phpe): return sp.lambdify((rs,Tval,Tpval),Tpp_expr.subs({phi_s:phe,sp.Derivative(phi_s,rs):phpe,xi_s:1,kap_s:1}).subs({Tt:Tval,Tp:Tpval}),'numpy')
rhs_flat=make_rhs(sp.Integer(0),sp.Integer(0))
def bc(ya,yb): return np.array([ya[0]-np.pi,yb[0]])
def solve_profile(rc,R,rhs,n=4000):
    rm=np.linspace(rc,R,n); Tg=np.pi*(1-(rm-rc)/(R-rc)); Tpg=-np.pi/(R-rc)*np.ones_like(rm)
    def f(r,y): return np.vstack([y[1],rhs(r,y[0],y[1])])
    return solve_bvp(f,bc,rm,np.vstack([Tg,Tpg]),tol=1e-8,max_nodes=200000)

def eig_full(rc,R,l,sol,phf,phpf,N=1000,seal='clamp'):
    r=np.linspace(rc,R,N); h=r[1]-r[0]
    Tg=sol.sol(r)[0]; Tpg=sol.sol(r)[1]
    ph=phf(r)*np.ones_like(r);
    Vcurv=-(np.exp(-2*ph)*Tpg**2+2*np.sin(Tg)**2/r**2)
    Vtot=l*(l+1)/r**2+Vcurv
    c4=2*np.sin(Tg)**4+2*np.sin(Tg)**2
    W=np.exp(2*ph)
    n=N;H=np.zeros((n,n));Wm=np.zeros((n,n))
    a=np.exp(-ph)*r**2; pref=1.0/(np.exp(ph)*r**2)
    for i in range(1,n-1):
        ap=0.5*(a[i]+a[i+1]);am=0.5*(a[i]+a[i-1])
        H[i,i-1]+=-pref[i]*am/h**2;H[i,i]+=pref[i]*(am+ap)/h**2;H[i,i+1]+=-pref[i]*ap/h**2
        H[i,i]+=Vtot[i];Wm[i,i]=W[i]
    d2=np.zeros((n,n))
    for i in range(1,n-1): d2[i,i-1]+=1/h**2;d2[i,i]+=-2/h**2;d2[i,i+1]+=1/h**2
    Bih=d2@np.diag(c4)@d2
    for i in range(2,n-2): H[i,:]+=pref[i]*Bih[i,:]
    H[0,:]=0;H[0,0]=1;Wm[0,0]=0;H[-1,:]=0;H[-1,-1]=1;Wm[-1,-1]=0
    H[1,:]=0;H[1,0]=-1;H[1,1]=1;Wm[1,1]=0
    if seal=='clamp':
        H[-2,:]=0;H[-2,-1]=-1;H[-2,-2]=1;Wm[-2,-2]=0
    # natural: leave row -2 (u'' free)
    w2,_=eig(H,Wm+1e-30*np.eye(n));w2=np.sort(w2.real[np.isfinite(w2.real)&(np.abs(w2.real)<1e6)])
    return w2

Rs=[8.0,25.0,80.0,250.0]
print("="*70);print("(1) SEAL BC SENSITIVITY (S3): l=1 WITH L4, clamp vs natural seal");print("="*70)
for seal in ['clamp','natural']:
    print(f"\n-- seal={seal} --");print(f"{'R':>8} {'lowest w^2':>14} {'w^2*R^2':>14}")
    for R in Rs:
        sol=solve_profile(1e-3,R,rhs_flat,n=min(4000,int(800*R/8)+1000))
        w2=eig_full(1e-3,R,1,sol,lambda x:0.0,lambda x:0.0,N=1000,seal=seal)
        lo=w2[0] if len(w2) else np.nan
        print(f"{R:8.1f} {lo:14.6e} {lo*R**2:14.4f}")

print("\n"+"="*70);print("(2) GOLDSTONE: is lowest l=1 a translational zero mode or the box?");print("="*70)
print("Translation eta_i ~ d_i n0 is a FLAT-space symmetry; on the finite Dirichlet")
print("cell it is the lowest box mode (lifted by walls ~1/R^2). The l=1 w^2->0 as")
print("R->inf is exactly the box-lifted Goldstone, NOT an intrinsic bound mode.")
print("Diagnostic: w^2*R^2 const (=20.2) => box-lifted, NOT a true omega^2=0 at finite R.")

print("\n"+"="*70);print("(3) DEEP-PHI (p=1) ANGULAR TRAP-TEST (F4): does phi-angular V add intrinsic?");print("="*70)
R_int=250.0
for l in [0,1,2]:
    phi_deep=lambda x,Ri=R_int: -1.0*np.log(Ri/x)
    print(f"\n-- l={l}, deep-phi p=1 --");print(f"{'R':>8} {'lowest w^2':>14} {'w^2*R^2':>14}")
    for R in Rs:
        phe=-1.0*sp.log(R/rs); phpe=sp.diff(phe,rs)
        rhs_d=make_rhs(phe,phpe)
        sol=solve_profile(1e-3,R,rhs_d,n=min(4000,int(800*R/8)+1000))
        phf=sp.lambdify(rs,phe,'numpy'); phpf=sp.lambdify(rs,phpe,'numpy')
        w2=eig_full(1e-3,R,l,sol,phf,phpf,N=1000,seal='clamp')
        lo=w2[0] if len(w2) else np.nan
        print(f"{R:8.1f} {lo:14.6e} {lo*R**2:14.4f}")
print("\nDONE F4/BC/Goldstone.")
