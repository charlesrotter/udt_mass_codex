import torch, math, time
import gapcloser_axisym as ax
import gapcloser_axisym_gate as gt
from gapcloser_axisym_search import ricci_tvar, envelope
torch.set_default_dtype(torch.float64)
rc,ri=0.05,14.05
Nr,Nth=160,24
G=ax.mkgrid(Nr,Nth,rc,ri,0.30,math.pi-0.30)
a0,b0,c0,d0,Th0,M0=gt.round_seed(G,rc,ri)
Mr=gt.M_MS_readout(b0,G,rc)
print(f"ROUND M_MS={M0:.5f} readout={Mr:.5f} tvar={ricci_tvar(a0,b0,c0,d0,G):.4f}",flush=True)
t0=time.time()
env=envelope(G); ct=torch.cos(G['Tht'][...,0]); st=torch.sin(G['Tht'][...,0])
def mk(name):
    if name.startswith("l"):
        l=int(name[1]); Pl={1:ct,2:0.5*(3*ct**2-1),3:0.5*(5*ct**3-3*ct),4:0.125*(35*ct**4-30*ct**2+3)}[l]
        mod=0.3*env*Pl; return a0-0.5*mod,b0.clone(),c0+mod,d0+mod
    if name=="prolate": q=0.4*env*(ct**2-1/3); return a0.clone(),b0.clone(),c0+q,d0-q
    if name=="oblate":  q=0.4*env*(ct**2-1/3); return a0.clone(),b0.clone(),c0-q,d0+q
    if name=="ring": rg=st**4; return a0-0.25*env*rg,b0+0.15*env*rg,c0.clone(),d0.clone()
    if name=="largeamp": ew=envelope(G,2.5); return a0-0.6*ew,b0+0.6*ew,c0.clone(),d0.clone()
res=[]
import sys
names = sys.argv[1:] if len(sys.argv)>1 else ["l1","l2","l3","l4","prolate","oblate","ring","largeamp"]
for name in names:
    a,b,c,d=mk(name); tvs=ricci_tvar(a,b,c,d,G); tsa=time.time()
    for blk in range(14):
        a,b,c,d,Th,h=ax.metric_lm_solve(a,b,c,d,Th0.clone(),G,0.05,outer=12,cg_iters=30,mu0=1e-3,rfreeze=1.0,verbose=False,w_matter=0.0)
    Phi=h[-1][2]; tv=ricci_tvar(a,b,c,d,G); M=gt.M_MS_readout(b,G,rc)
    res.append((name,tvs,Phi,tv,M))
    print(f">> {name:9s}: seed_tvar={tvs:.3f} -> Phi={Phi:.3e} tvar={tv:.4f} M={M:.5f} dM={M-Mr:+.4f} ({time.time()-tsa:.0f}s)",flush=True)
print("== SUMMARY ==",flush=True)
for name,tvs,Phi,tv,M in res:
    relaxing = tv < 0.6*tvs
    print(f"  {name:9s}: tvar {tvs:.2f}->{tv:.2f} ({'relaxing' if relaxing else 'persists'}) Phi={Phi:.2e} dM={M-Mr:+.4f}",flush=True)
print(f"# total {time.time()-t0:.0f}s",flush=True)
