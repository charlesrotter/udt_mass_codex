import os,sys,math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0,"/home/udt-admin/udt_mass_codex"); sys.path.insert(0,"/tmp")
import whole_metric_3d_core as CORE, whole_metric_3d_matter as MAT
from full3d_spectral import Grid3D, attach_coord_weight, build_metric, DEV
from einstein_3d_general_eval import ricci_scalar_general
import free_s2_matter as FS
import b1prime_round as RAD
PI=math.pi; X,XI,KAP,KAP8=-2e5,2e-2,2e-2,1.0
T,Rr,TH,PS=0,1,2,3

def setup(Nr=16, cell=14.0):
    RG=RAD.RGrid(Nr,rc=0.05,cell=cell)
    u,Phi=RAD.solve(RG,X,XI,KAP,1.0,KAP8,m=1,maxit=120,verbose=False)
    dgd=RAD.diag(RG,u,X,XI,KAP)
    G=Grid3D(Nr=Nr,Nth=8,Nps=8,rc=0.05,cell=cell); G=attach_coord_weight(G)
    def lift(arr):
        t=torch.tensor(arr,device=DEV); return t[:,None,None].expand(G.Nr,G.Nth,G.Nps).contiguous()
    a=lift(dgd['a']);b=lift(dgd['b']);c=torch.zeros_like(a);d=torch.zeros_like(a);phi=lift(dgd['ph'])
    return G,a,b,c,d,phi

def energy(G,a,b,c,d,phi,alpha,beta,h_s,h_g,m=1):
    # TOTAL static energy: matter proper mass + GRAVITATIONAL action cost of the shear.
    # E_total(alpha,beta) = INT [ rho_matter * f + gravity_cost ] sqrt(g3) dV (body).
    # gravity_cost: turning on shear changes R; the on-shell energy includes the e^{2phi}R
    # term. We compute the FULL action-energy = -INT sqrt(-g) f (R + X(dphi)^2 + L_m)?? No:
    # For a STATIC config the ADM/Komar mass is the integral. Cleanest unambiguous proxy:
    # the matter proper mass M_m = INT rho f sqrt(g3) dV  AND separately the gravity-sector
    # action curvature, reported. Here we compute M_m (energy-correct sign) WITH shear in ginv.
    e_rp=alpha*h_s
    g=build_metric(G,a,b,c,d,e_rp=e_rp); ginv=CORE.metric_inverse(g)
    f=torch.exp(2*phi)
    g3=g[...,1:,1:]; sqrtg3=torch.sqrt(torch.clamp(torch.linalg.det(g3),min=1e-300))
    dn=FS.field_dn_freeaz(G, beta*h_g, m=m)
    Tab,*_=MAT.stress_tensor(g,ginv,dn,XI,KAP); Tm=torch.einsum('...ma,...an->...mn',ginv,Tab)
    rho=-Tm[...,T,T]
    w=G.wvol_coord; mask=G.body.double()
    Mm=(rho*f*sqrtg3*w*mask).sum()
    # gravity-sector cost of shear: the Einstein-Hilbert-like action density e^{2phi} R
    # (the derived operator's gravity term). Its change with alpha = gravitational stiffness.
    Rsc=ricci_scalar_general(G, dict(a=a,b=b,c=c,d=d,e_rp=e_rp))
    sqrtg=torch.sqrt(torch.clamp(-torch.linalg.det(g),min=1e-300))
    Sgrav=(sqrtg*f*Rsc*w*mask).sum()
    return Mm, Sgrav

def hess(G,a,b,c,d,phi,h_s,h_g,label,h=2e-3,m=1):
    def Mm(al,be): return energy(G,a,b,c,d,phi,al,be,h_s,h_g,m)[0].item()
    def Sg(al,be): return energy(G,a,b,c,d,phi,al,be,h_s,h_g,m)[1].item()
    # ENERGY hessian (matter proper mass)
    for name,Ffn,sgn in [("MATTER proper mass M_m (minimize for stable)",Mm,+1),
                         ("GRAVITY action e^{2phi}R term",Sg,+1)]:
        F0=Ffn(0,0)
        Faa=(Ffn(h,0)-2*F0+Ffn(-h,0))/h**2
        Fbb=(Ffn(0,h)-2*F0+Ffn(0,-h))/h**2
        Fab=(Ffn(h,h)-Ffn(h,-h)-Ffn(-h,h)+Ffn(-h,-h))/(4*h*h)
        H=np.array([[Faa,Fab],[Fab,Fbb]]); ev,evec=np.linalg.eigh(H)
        det=Faa*Fbb-Fab**2
        print("  [%s] %s"%(label,name))
        print("     H_aa=%+.4e H_bb=%+.4e H_ab=%+.4e det=%+.4e eig=[%+.4e,%+.4e]"
              %(Faa,Fbb,Fab,det,ev[0],ev[1]))
        soft=evec[:,np.argmin(ev)]
        print("     softest eigvec(alpha=shear,beta=twist)=(%+.3f,%+.3f)"%(soft[0],soft[1]))

G,a,b,c,d,phi=setup()
rc,ri=float(G.r[0]),float(G.r[-1]); rfac=torch.sin(PI*(G.Rg-rc)/(ri-rc))
mu=torch.cos(G.THg); P2=0.5*(3*mu**2-1.0)
print("ENERGY-HESSIAN (proper mass minimized => NEGATIVE eig = energy-lowering instability)")
print("="*78)
hess(G,a,b,c,d,phi,rfac,rfac,"shear=P0")
hess(G,a,b,c,d,phi,rfac*P2,rfac,"shear=l2P2")
# also a sin th azimuthal shear that matches the twist's sin^2 th source structure
sth=G.STHg
hess(G,a,b,c,d,phi,rfac*sth,rfac,"shear=sinth")
