"""BV attack #3+#4: independent MMS gauntlet with MY OWN perturbation shapes (different from
e2c_mms_certification.perturb), plus attack #4 -- does PURE Gauss-Newton (no trust region) hit
the SAME field-axis minima as the dogleg? (intrinsic NLLS vs solver defect).
"""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
from torch.func import jacrev

DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5

def build_mms(label, rp0_frac, amp, bulge=0.0):
    br = C.load_bracket(label); prm = (br["Z"], 0.5, 0.1, 1)
    ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
    rp0 = rp0_frac*br["r_s"] if rp0_frac<=1.0 else rp0_frac
    def genericize(v):
        phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
        z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV); h=ctx["ha"].to(DEV)
        phi_c=phi_c+0.05*torch.cos(math.pi*z); rho_c=rho_c+0.03*torch.sin(0.5*math.pi*(z+1.0))
        uf=uf+0.05*(1.0-mu[None,:]**2)*mu[None,:]*torch.cos(math.pi*(z[:,None]+1.0))
        uf=uf+bulge*(1.0-mu[None,:]**2)*torch.sin(math.pi*(z[:,None]+1.0)/2.0)
        phi_a=phi_a+0.02*torch.sin(math.pi*h); rho_a=rho_a+0.01*h*(1.0-h)
        return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p),float(r_sU),device=DEV)
    v_star=genericize(C.seed_comp(ctx,br,rp0=rp0,amp=amp,device=DEV))
    F_star=C.residual_comp(v_star,ctx,prm,br).detach()
    resfn=lambda vv: C.residual_comp(vv,ctx,prm,br)-F_star
    return dict(br=br,prm=prm,ctx=ctx,v_star=v_star,resfn=resfn,F_star=F_star,n=v_star.numel())

def my_perturb(mm, cell_sc=0.0, amb_sc=0.0, dr=0.0):
    """MY OWN shapes -- deliberately different basis functions from the cert script."""
    ctx=mm["ctx"]; v=mm["v_star"]
    phi_c,rho_c,uf,phi_a,rho_a,r_p,r_sU=C.unpack_comp(v,ctx)
    z=ctx["cell"]["zeta"].to(DEV); mu=ctx["cell"]["mu"].to(DEV); h=ctx["ha"].to(DEV)
    # different: use z^2 and cos(2pi) etc.
    phi_c=phi_c+cell_sc*(z**2-0.3)
    rho_c=rho_c+cell_sc*torch.cos(1.5*math.pi*z)
    uf=uf+cell_sc*(1.0-mu[None,:]**2)*torch.cos(math.pi*(z[:,None]))
    phi_a=phi_a+amb_sc*torch.sin(3*math.pi*h)*0.5
    rho_a=rho_a+amb_sc*(h-0.5)
    # asymmetric boundary shift (not the 1.1x of the cert script)
    return C.pack_comp(phi_c,rho_c,uf,phi_a,rho_a,float(r_p)+dr,float(r_sU)+0.9*dr,device=DEV)

def cpu_check(mm, w):
    wt=torch.as_tensor(np.asarray(w,dtype=float),device="cpu")
    ctx_c=C.make_ctx_comp(Nr,Nth,Na,kmap=KMAP,device="cpu")
    Fc=C.residual_comp(wt,ctx_c,mm["prm"],mm["br"])-mm["F_star"].cpu()
    return float(Fc.abs().max())

def pure_gn(resfn, w0, maxit=200, budget=120.0):
    """Pure Ruiz-equilibrated Gauss-Newton + simple backtracking line search (NO trust region).
    For attack #4: does a different globalization hit the SAME field minima?"""
    t0=time.time()
    w=np.asarray(w0,dtype=np.longdouble).copy()
    evalF=lambda ww: resfn(torch.as_tensor(ww.astype(float),device=DEV)).detach().cpu().numpy().astype(np.longdouble)
    F=evalF(w); Phi=float((F*F).sum())
    for it in range(maxit):
        if Phi<1e-30 or time.time()-t0>budget: break
        wt=torch.as_tensor(w.astype(float),device=DEV)
        J=jacrev(resfn)(wt).detach().cpu().numpy().astype(np.float64)
        dr,dc=C._ruiz_equilibrate(J)
        Aeq=dr[:,None]*J*dc[None,:]; beq=-dr*np.asarray(F,dtype=np.float64)
        y,*_=np.linalg.lstsq(Aeq,beq,rcond=None)
        dx=dc*y
        step=1.0; acc=False
        for _ls in range(40):
            wn=w+ (step*dx).astype(np.longdouble)
            try:
                Fn=evalF(wn); Pn=float((Fn*Fn).sum())
            except Exception: Pn=float("inf")
            if math.isfinite(Pn) and Pn<Phi:
                w=wn; F=Fn; Phi=Pn; acc=True; break
            step*=0.5
        if not acc: break
    return w, float(np.abs(F).max())

if __name__=="__main__":
    print(f"BV GAUNTLET device={DEV}")
    mm=build_mms("A1 m=3 Z=8",0.95,0.8)
    print(f"MMS#1 n={mm['n']} root|F|={float(mm['resfn'](mm['v_star']).abs().max()):.2e}\n")

    print("== BASELINE lm_qr (should FAIL at boundary dr=10) ==")
    for dr in [10.0]:
        v0=my_perturb(mm,dr=dr); dvn=float((v0-mm['v_star']).abs().max())
        w,info=C.lm_qr(mm['resfn'],v0.cpu().numpy(),maxit=300,device=DEV,time_budget=150.0)
        wt=torch.as_tensor(np.asarray(w,dtype=float),device=DEV)
        maxF=float(mm['resfn'](wt).abs().max())
        print(f"  qr  dr={dr} ||v0-v*||={dvn:.2f} it={info['iters']} maxF={maxF:.2e}")

    print("== HARDENED lm_hardened -- boundary axis (MY shapes) ==")
    n=mm['n']
    for dr in [5.0,10.0,20.0,30.0]:
        v0=my_perturb(mm,dr=dr); dvn=float((v0-mm['v_star']).abs().max())
        t0=time.time()
        w,info=C.lm_hardened(mm['resfn'],v0.cpu().numpy(),maxit=300,time_budget=150.0,
                             device=DEV,pos_idx=[n-2,n-1],order_idx=(n-2,n-1))
        cpu=cpu_check(mm,w)
        print(f"  hard dr={dr} ||v0-v*||={dvn:.2f} it={info['iters']} ({time.time()-t0:.0f}s) "
              f"maxF={info['maxF']:.2e} cpu={cpu:.1e} {'CONV' if info['maxF']<=1e-8 and cpu<=1e-7 else 'no'}")

    print("== ATTACK#4: field axis -- dogleg vs pure-GN (same minima?) ==")
    for sc in [0.1,0.2,0.3]:
        v0=my_perturb(mm,cell_sc=sc); dvn=float((v0-mm['v_star']).abs().max())
        w1,info1=C.lm_hardened(mm['resfn'],v0.cpu().numpy(),maxit=200,time_budget=120.0,
                               device=DEV,pos_idx=[n-2,n-1],order_idx=(n-2,n-1))
        w2,mf2=pure_gn(mm['resfn'],v0.cpu().numpy(),maxit=200,budget=120.0)
        # distance between the two stall points
        dstall=float(np.abs(np.asarray(w1,dtype=float)-np.asarray(w2,dtype=float)).max())
        print(f"  cell {sc}: dogleg maxF={info1['maxF']:.2e}  pureGN maxF={mf2:.2e}  "
              f"||stall_dog - stall_gn||inf={dstall:.2e}")
    print("DONE")
