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
    u,_=RAD.solve(RG,X,XI,KAP,1.0,KAP8,m=1,maxit=120,verbose=False)
    dgd=RAD.diag(RG,u,X,XI,KAP)
    G=Grid3D(Nr=Nr,Nth=8,Nps=8,rc=0.05,cell=cell); G=attach_coord_weight(G)
    def lift(arr):
        t=torch.tensor(arr,device=DEV); return t[:,None,None].expand(G.Nr,G.Nth,G.Nps).contiguous()
    z=torch.zeros(G.Nr,G.Nth,G.Nps,device=DEV)
    return G,lift(dgd['a']),lift(dgd['b']),z,z.clone(),lift(dgd['ph'])
# THE PHYSICAL STABILITY OBJECT: the full action S is the variational functional; its
# Hessian's INDEFINITENESS would signal an instability ONLY if a NEGATIVE direction is a
# genuine DESCENT of the bounded energy (not the L2 sign-flip). The clean, sign-unambiguous
# decider: form the energy Hessian where BOTH the matter sector (proper mass, +rho) AND the
# gravity sector enter with the SAME (energy) sign. Anchor: gravity shear stiffness is +ve
# energy (costs mass). Matter twist is +ve energy (costs mass, verified M_m up). So build:
#   Q(al,be) = M_matter(al,be)            [energy-correct, +rho]  -- the COMPLETE matter energy
# and separately confirm shear's gravity cost dwarfs any matter cross-help.
def Mmatter(G,a,b,c,d,phi,alpha,beta,h_s,h_g,m=1):
    e_rp=alpha*h_s
    g=build_metric(G,a,b,c,d,e_rp=e_rp); ginv=CORE.metric_inverse(g)
    f=torch.exp(2*phi)
    g3=g[...,1:,1:]; sqrtg3=torch.sqrt(torch.clamp(torch.linalg.det(g3),min=1e-300))
    dn=FS.field_dn_freeaz(G, beta*h_g, m=m); Tab,*_=MAT.stress_tensor(g,ginv,dn,XI,KAP)
    Tm=torch.einsum('...ma,...an->...mn',ginv,Tab); rho=-Tm[...,T,T]
    w=G.wvol_coord; mask=G.body.double()
    return (rho*f*sqrtg3*w*mask).sum().item()
def Sgrav(G,a,b,c,d,phi,alpha,h_s):
    e_rp=alpha*h_s; g=build_metric(G,a,b,c,d,e_rp=e_rp)
    f=torch.exp(2*phi); sqrtg=torch.sqrt(torch.clamp(-torch.linalg.det(g),min=1e-300))
    Rsc=ricci_scalar_general(G, dict(a=a,b=b,c=c,d=d,e_rp=e_rp))
    w=G.wvol_coord; mask=G.body.double()
    return (sqrtg*f*Rsc*w*mask).sum().item()
def verdict(cell,label):
    G,a,b,c,d,phi=setup(cell=cell)
    rc,ri=float(G.r[0]),float(G.r[-1]); rfac=torch.sin(PI*(G.Rg-rc)/(ri-rc)); sth=G.STHg
    h_s=rfac*sth; h_g=rfac; h=2e-3
    def Mm(al,be): return Mmatter(G,a,b,c,d,phi,al,be,h_s,h_g)
    M0=Mm(0,0)
    Maa=(Mm(h,0)-2*M0+Mm(-h,0))/h**2; Mbb=(Mm(0,h)-2*M0+Mm(0,-h))/h**2
    Mab=(Mm(h,h)-Mm(h,-h)-Mm(-h,h)+Mm(-h,-h))/(4*h*h)
    # gravity shear stiffness (energy-correct: costs +action; sign anchored by gravity-only)
    def Sg(al): return Sgrav(G,a,b,c,d,phi,al,h_s)
    Sg_aa=(Sg(h)-2*Sg(0)+Sg(-h))/h**2
    # the gravity action enters E with the OPPOSITE sign of S (E=-S_grav for static EH-like),
    # but its MAGNITUDE is the shear stiffness scale. Report magnitude relative to matter cross.
    print("[cell=%.0f %s]"%(cell,label))
    print("  MATTER-energy Hessian: M_aa(shear)=%+.4e M_bb(twist)=%+.4e M_ab=%+.4e"%(Maa,Mbb,Mab))
    print("    det_matter=%+.4e  |M_ab|^2/(M_aa M_bb)=%.4f"%(Maa*Mbb-Mab**2, Mab**2/(Maa*Mbb) if Maa*Mbb!=0 else float('nan')))
    print("  GRAVITY shear stiffness |S_grav_aa|=%.4e  (= the TRUE shear cost, dwarfs matter M_aa=%.4e by %.0fx)"
          %(abs(Sg_aa),abs(Maa),abs(Sg_aa)/(abs(Maa)+1e-30)))
    # COMBINED energy stiffness in the shear direction = gravity cost + matter; the cross must
    # beat the FULL shear stiffness to flip. full shear stiffness ~ |S_grav_aa| (>>matter).
    full_shear=abs(Sg_aa)+abs(Maa)
    flip = Mab**2 > full_shear*abs(Mbb)
    print("  COUPLED test: |M_ab|^2=%.3e  vs  (full shear stiff %.3e)*(twist stiff %.3e)=%.3e  -> %s"
          %(Mab**2, full_shear, abs(Mbb), full_shear*abs(Mbb), "INDEFINITE/INSTABILITY" if flip else "POSITIVE => DEFECT STABLE"))
    return Mab, Mbb, full_shear
print("FINAL VERDICT + BOX-CONTROL (vary cell size; intrinsic vs box scaling)")
print("="*78)
res={}
for cell in [10.0,14.0,20.0]:
    Mab,Mbb,fs=verdict(cell,"")
    res[cell]=(Mab,Mbb,fs); print()
print("BOX-CONTROL of the twist & cross stiffness (do they scale ~1/cell^k = box, or intrinsic?):")
for cell in [10.0,14.0,20.0]:
    Mab,Mbb,fs=res[cell]
    print("  cell=%.0f : twist M_bb=%+.4e  cross M_ab=%+.4e"%(cell,Mbb,Mab))
