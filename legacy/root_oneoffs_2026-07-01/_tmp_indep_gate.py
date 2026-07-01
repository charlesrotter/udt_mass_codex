import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, numpy as np, torch
import radial_Bfree_soliton as rb
torch.set_default_dtype(torch.float64)
xi=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; P=0.4; KAP8=0.05
def grad(f,r):
    g=np.zeros_like(f); g[1:-1]=(f[2:]-f[:-2])/(r[2:]-r[:-2])
    g[0]=(f[1]-f[0])/(r[1]-r[0]); g[-1]=(f[-1]-f[-2])/(r[-1]-r[-2]); return g
def d2(f,r):
    fpp=np.zeros_like(f); hm=r[1:-1]-r[:-2]; hp=r[2:]-r[1:-1]
    fpp[1:-1]=(2*hp*f[:-2]-2*(hm+hp)*f[1:-1]+2*hm*f[2:])/(hm*hp*(hm+hp)); return fpp
def run(N):
    rN=rb.make_grid(1,N,rc=rc,rint=ri,geom=False)
    o=rb.selfconsistent_Bfree(rN,xi,kap,p=P,kap8=KAP8,iters=200,relax=0.4,tol=1e-11,verbose=False)
    r=o['r'][0].cpu().numpy();a=o['a'][0].cpu().numpy();b=o['b'][0].cpu().numpy();Th=o['Th'][0].cpu().numpy();M=o['M_MS'].item()
    ap=grad(a,r);bp=grad(b,r);app=d2(a,r);Thp=grad(Th,r)
    e2b=np.exp(2*b);em2b=np.exp(-2*b)
    Gtt=em2b*(-2*r*bp-e2b+1)/r**2; Grr=em2b*(2*r*ap-e2b+1)/r**2
    Gthth=em2b*(r*ap**2-r*ap*bp+r*app+ap-bp)/r
    X=em2b*Thp**2;Y=np.sin(Th)**2/r**2
    rho=(xi/2)*(X+2*Y)+(kap/2)*(2*X*Y+Y**2)
    pr=(xi/2)*(X-2*Y)+(kap/2)*(2*X*Y-Y**2); pT=(kap/2)*Y**2-(xi/2)*X
    res=[Gtt+KAP8*rho,Grr-KAP8*pr,Gthth-KAP8*pT]
    body=(r>rc+1.0)&(r<ri-0.5); idx=np.where(body)[0][3:-3]
    return N,M,[np.abs(x[idx]).max() for x in res]
print("INDEPENDENT numpy gate (uniform grid), body r>rc+1.0:")
prev=None
for N in [220,320,440]:
    N,M,res=run(N)
    line=f"  N={N}: M_MS={M:.6f}  res_tt={res[0]:.3e} res_rr={res[1]:.3e} res_thth={res[2]:.3e}"
    if prev: line+=f"  | conv rr={prev[1]/res[1]:.2f}x thth={prev[2]/res[2]:.2f}x"
    prev=res; print(line,flush=True)
