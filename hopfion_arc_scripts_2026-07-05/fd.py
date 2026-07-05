import os,sys,math,numpy as np
REPO="/home/udt-admin/udt_mass_codex"; sys.path.insert(0,REPO)
import torch; torch.set_default_dtype(torch.float64)
import cell_solver_f2d as F2D
def load(fn):
    d=torch.load(os.path.join(REPO,fn),map_location="cpu",weights_only=False)
    w=d["w"];Nr=d["Nr"];Nth=d["Nth"];Na=d["Na"];prm=d["prm"];i=0
    phi=w[i:i+Nr].numpy();i+=Nr; rho=w[i:i+Nr].numpy();i+=Nr
    r_p=float(w[2*Nr+Nr*Nth+2*Na])
    return phi,rho,r_p,Nr,tuple(prm)
# INDEPENDENT finite-difference build on a UNIFORM r-grid (interp fields), central diff, trap quad.
def energy_fd(theta,r,phi,rho,branch,Om2,N,XI):
    dr=r[1]-r[0]; thp=np.gradient(theta,dr)
    Wk=np.exp(-2*phi) if branch=="B" else np.ones_like(phi)
    Wb=np.exp(2*phi) if branch=="B" else np.ones_like(phi)
    dens=(XI/2)*rho**2*(Wk*thp**2+np.sin(theta)**2*(N**2/rho**2-Wb*Om2))
    return np.trapz(dens,r)
def lammin_fd(r,phi,rho,branch,Om2,N,XI,kind,M=40):
    x=np.linspace(0,1,M); th0=math.pi*(1-x) if kind=="linear" else math.pi*np.cos(math.pi*x/2)**2
    idx=np.arange(1,M-1); n=len(idx); H=np.zeros((n,n)); h=1e-5
    def E(u):
        th=th0.copy(); th[idx]=u; return energy_fd(th,r,phi,rho,branch,Om2,N,XI)
    u0=th0[idx].copy()
    for a in range(n):
        for b in range(a,n):
            ea=np.zeros(n);ea[a]=h; eb=np.zeros(n);eb[b]=h
            val=(E(u0+ea+eb)-E(u0+ea-eb)-E(u0-ea+eb)+E(u0-ea-eb))/(4*h*h)
            H[a,b]=val;H[b,a]=val
    return np.linalg.eigvalsh(H)[0]
fn="E2b_A1Z1_P2_W4_wall.pt"; phi,rho,r_p,Nr,prm=load(fn); Z,XI,KAP,N=prm; XI=float(XI);N=int(N)
zeta,_=F2D._cheb(Nr); rn=r_p*(np.array(zeta)+1)/2
M=40; ru=np.linspace(0,r_p,M); phiu=np.interp(ru,rn,phi); rhou=np.interp(ru,rn,rho)
print(f"INDEPENDENT FD (uniform grid, M={M}, central-diff Hessian)  {fn}")
Wb=np.exp(2*phiu); ceil=float((N**2/(rhou**2*Wb)).min())
print(f"  B=0 ceil~{ceil:.3e}")
for Om2 in [0.0, ceil, 3*ceil, 1e2*ceil, 1e4*ceil]:
    lm=lammin_fd(ru,phiu,rhou,"B",Om2,N,XI,"linear")
    print(f"  Branch B linear  Om2={Om2:.3e} (x{Om2/ceil:.0e})  lam_min_FD={lm:+.4e}")
# wide DERRICK on field2 (the one that showed E(0.15) going negative) - does interior min ever appear?
print("\nWIDE DERRICK, field2 branch B (E(0.15) went negative at 2xceil in orig):")
fn2="E2b_A1Z8_P2_W2_wall.pt"; phi2,rho2,r_p2,Nr2,prm2=load(fn2); Z2,XI2,K2,N2=prm2;XI2=float(XI2);N2=int(N2)
zeta2,_=F2D._cheb(Nr2); rn2=r_p2*(np.array(zeta2)+1)/2
rf=np.linspace(0,r_p2,400); phif=np.interp(rf,rn2,phi2); rhof=np.interp(rf,rn2,rho2)
Wkf=np.exp(-2*phif);Wbf=np.exp(2*phif); ceil2=float((N2**2/(rho2.__class__(rho2)**2)/np.exp(2*np.array(phi2))).min()) if False else float((N2**2/(np.array(rho2)**2*np.exp(2*np.array(phi2)))).min())
lams=np.linspace(0.05,1.6,40)
for Om2 in [0.0,ceil2:=float((N2**2/(np.array(rho2)**2*np.exp(2*np.array(phi2)))).min()), 10*ceil2,1e3*ceil2,1e5*ceil2]:
    Es=[]
    for lam in lams:
        x=np.clip((rf/r_p2)/lam,0,1); th=math.pi*(1-x); thp=np.gradient(th,rf)
        dens=(XI2/2)*rhof**2*(Wkf*thp**2+np.sin(th)**2*(N2**2/rhof**2-Wbf*Om2))
        Es.append(np.trapz(dens,rf))
    Es=np.array(Es); im=int(np.argmin(Es)); interior=0<im<len(lams)-1
    print(f"  Om2={Om2:.3e} (x{Om2/ceil2:.0e}): min at lam={lams[im]:.3f} {'INTERIOR' if interior else 'BOUNDARY-collapse'}  Emin={Es[im]:.3e}")
