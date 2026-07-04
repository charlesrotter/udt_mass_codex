"""BV attack 3: certification honesty with MY OWN perturbation shapes + runaway-gate test."""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import e2d_continuation_driver as D
DEV = D.DEV
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5

def build_mms(label, rp0_frac, amp, bulge=0.0):
    br = C.load_bracket(label); prm=(br["Z"],0.5,0.1,1)
    ctx=C.make_ctx_comp(Nr,Nth,Na,kmap=KMAP,device=DEV)
    rp0=rp0_frac*br["r_s"] if rp0_frac<=1.0 else rp0_frac
    def gen(vv):
        phi_c,rho_c,uf,phi_a,rho_a,r_p,r_sU=C.unpack_comp(vv,ctx)
        z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV); h=ctx["ha"].to(DEV)
        phi_c=phi_c+0.05*torch.cos(math.pi*z); rho_c=rho_c+0.03*torch.sin(0.5*math.pi*(z+1))
        uf=uf+0.05*(1-mu[None,:]**2)*mu[None,:]*torch.cos(math.pi*(z[:,None]+1))
        uf=uf+bulge*(1-mu[None,:]**2)*torch.sin(math.pi*(z[:,None]+1)/2)
        phi_a=phi_a+0.02*torch.sin(math.pi*h); rho_a=rho_a+0.01*h*(1-h)
        return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)
    v_star=gen(C.seed_comp(ctx,br,rp0=rp0,amp=amp,device=DEV))
    F_star=C.residual_comp(v_star,ctx,prm,br).detach()
    resfn=lambda vv: C.residual_comp(vv,ctx,prm,br)-F_star
    return dict(br=br,prm=prm,ctx=ctx,v_star=v_star,resfn=resfn,F_star=F_star,n=v_star.numel())

def metrics(mm,w):
    n=mm["n"]; vstar=mm["v_star"].cpu().numpy().astype(np.longdouble)
    wt=torch.as_tensor(np.asarray(w,dtype=float),device=DEV)
    mF=float(mm["resfn"](wt).abs().max())
    dist=float(np.abs(np.asarray(w,dtype=np.longdouble)-vstar).max())
    rp=float(abs(w[n-2])/abs(vstar[n-2]))
    return mF,dist,rp
def reach(mF,dist,rp): return mF<=1e-8 and dist<5 and 0.5<rp<2

for label,rpf,amp,bulge in [("A1 m=3 Z=8",0.95,0.8,0.0),("A3 Z=1",100.0,0.8,0.4)]:
    mm=build_mms(label,rpf,amp,bulge); ctx=mm["ctx"]; n=mm["n"]
    z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV); h=ctx["ha"].to(DEV)
    print(f"\n=== {label}  n={n} ===")
    # boundary 30 (my own: also perturb the ambient a bit)
    phi_c,rho_c,uf,phi_a,rho_a,r_p,r_sU=C.unpack_comp(mm["v_star"],ctx)
    v0=C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p)+30.0,float(r_sU)+33.0,device=DEV)
    w,info=D._correct(mm["resfn"],v0.cpu().numpy().astype(np.longdouble),n,maxit=250,budget=60)
    mF,dist,rp=metrics(mm,w); print(f"  boundary30  maxF={mF:.2e} dist={dist:.2e} rp={rp:.2f} {'REACH' if reach(mF,dist,rp) else 'no'}")
    # u axis 0.2 my-shape (different mode)
    uf2=uf+0.2*(1-mu[None,:]**2)*torch.cos(1.5*math.pi*z[:,None])
    v0=C.pack_comp(phi_c,rho_c,uf2,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)
    w,info=D.arclength_homotopy(mm["resfn"],v0.cpu().numpy().astype(np.longdouble),n,budget=55,maxsteps=150,fold_abort=0.03,runaway_cap=1e5)
    mF,dist,rp=metrics(mm,w); print(f"  u0.2 myshape arclen s_max={info['s_max']:.3f} maxF={mF:.2e} dist={dist:.2e} rp={rp:.2f} {'REACH' if reach(mF,dist,rp) else 'no'}")
    # cell 0.15 my-shape
    phi_c2=phi_c+0.15*torch.cos(2*math.pi*(z+0.3)); rho_c2=rho_c+0.15*torch.sin(math.pi*(z-0.2))
    uf3=uf+0.15*(1-mu[None,:]**2)*torch.cos(1.5*math.pi*z[:,None])
    v0=C.pack_comp(phi_c2,rho_c2,uf3,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)
    w,info=D.arclength_homotopy(mm["resfn"],v0.cpu().numpy().astype(np.longdouble),n,budget=55,maxsteps=150,fold_abort=0.03,runaway_cap=1e5)
    mF,dist,rp=metrics(mm,w); print(f"  cell0.15 myshape arclen s_max={info['s_max']:.3f} maxF={mF:.2e} dist={dist:.2e} rp={rp:.2f} {'REACH' if reach(mF,dist,rp) else 'no'}")

# runaway-gate test: fabricate a translation-gauge runaway (big boundary offset, then let corrector
# find the small-residual gauge orbit). Confirm is_reach rejects a small-maxF-at-distance.
print("\n=== runaway gate test (does dist/ratio clause reject a false floor?) ===")
mm=build_mms("A3 Z=1",100.0,0.8,0.4); n=mm["n"]; ctx=mm["ctx"]
phi_c,rho_c,uf,phi_a,rho_a,r_p,r_sU=C.unpack_comp(mm["v_star"],ctx)
# a state translated far in boundary but otherwise root-like -> if residual near-null on gauge, false floor
vbig=C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p)*1.6,float(r_sU)*1.6,device=DEV)
mF,dist,rp=metrics(mm,vbig.cpu().numpy().astype(np.longdouble))
print(f"  fabricated far-boundary state: maxF={mF:.2e} dist={dist:.2e} rp={rp:.2f} is_reach={reach(mF,dist,rp)} (want: rejected if dist/rp large)")
print("DONE bv_cert")
