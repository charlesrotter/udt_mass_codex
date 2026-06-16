#!/usr/bin/env python3
"""(E) off-diagonal core FD error shrinks with grid h (confirms ~5e-6 is truncation,
   not a bug). (F) confirm B=1/A is FREE in the converged radial solve: a != -b."""
import os
os.environ["CUDA_VISIBLE_DEVICES"]=""
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, numpy as np, sympy as sp, torch
torch.set_default_dtype(torch.float64)
import importlib.util
def load(m,p):
    s=importlib.util.spec_from_file_location(m,p); mod=importlib.util.module_from_spec(s)
    s.loader.exec_module(mod); return mod
core=load("c","/home/udt-admin/udt_mass_codex/whole_metric_3d_core.py")
rbf =load("r","/home/udt-admin/udt_mass_codex/radial_Bfree_soliton.py")

t,r,th,ps=sp.symbols('t r theta psi',real=True)
def sym_Gdn(g,coords):
    gi=g.inv(); n=4
    Gam=[[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
     for b in range(n):
      for c in range(n):
        Gam[a][b][c]=sp.simplify(sum(gi[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d])) for d in range(n))/2)
    def riem(a,b,c,d):
        s=sp.diff(Gam[a][b][d],coords[c])-sp.diff(Gam[a][b][c],coords[d])
        for e in range(n): s+=Gam[a][c][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][c]
        return s
    Ric=sp.zeros(n,n)
    for b in range(n):
     for d in range(n):
        Ric[b,d]=sp.simplify(sum(riem(a,b,a,d) for a in range(n)))
    Rs=sp.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
    return sp.simplify(sp.Matrix(n,n,lambda i,j:Ric[i,j]-sp.Rational(1,2)*g[i,j]*Rs))

a0,b0,w0=sp.Rational(1,10),sp.Rational(1,7),sp.Rational(1,5)
gtt=-(1+a0*r**2); gtp=w0*r**2*sp.sin(th)**2; grr=1+b0*r**2
gthth=r**2; gpsps=r**2*sp.sin(th)**2
gM=sp.Matrix([[gtt,0,0,gtp],[0,grr,0,0],[0,0,gthth,0],[gtp,0,0,gpsps]])
GdnM=sym_Gdn(gM,[t,r,th,ps])

def numeric_err(Nr,Nth,Nps):
    rg=torch.linspace(1.0,3.0,Nr); thg=torch.linspace(0.6,2.4,Nth)
    psg=torch.linspace(0,2*math.pi,Nps+1)[:-1]
    hr=(rg[1]-rg[0]).item(); hth=(thg[1]-thg[0]).item(); hps=2*math.pi/Nps
    RR,TT,PP=torch.meshgrid(rg,thg,psg,indexing='ij')
    g=torch.zeros(Nr,Nth,Nps,4,4)
    for (i,j),e in {(0,0):gtt,(0,3):gtp,(3,0):gtp,(1,1):grr,(2,2):gthth,(3,3):gpsps}.items():
        fn=sp.lambdify((r,th,ps),e,'numpy'); v=fn(RR.numpy(),TT.numpy(),PP.numpy())
        g[...,i,j]=torch.as_tensor(np.broadcast_to(v,RR.shape).astype(np.float64))
    gi=core.metric_inverse(g)
    dg=torch.zeros(Nr,Nth,Nps,4,4,4)
    for mu in range(4):
     for nu in range(4):
        dg[...,1,mu,nu]=core.d_dx(g[...,mu,nu],hr,0)
        dg[...,2,mu,nu]=core.d_dx(g[...,mu,nu],hth,1)
        dg[...,3,mu,nu]=core.d_dx(g[...,mu,nu],hps,2,periodic=True)
    Gam=core.christoffel(gi,dg)
    dGam=torch.zeros(Nr,Nth,Nps,4,4,4,4)
    for a in range(4):
     for b in range(4):
      for c in range(4):
        dGam[...,1,a,b,c]=core.d_dx(Gam[...,a,b,c],hr,0)
        dGam[...,2,a,b,c]=core.d_dx(Gam[...,a,b,c],hth,1)
        dGam[...,3,a,b,c]=core.d_dx(Gam[...,a,b,c],hps,2,periodic=True)
    Gmn,_,_=core.einstein(g,gi,Gam,dGam)
    ir,ith,ips=Nr//2,Nth//2,Nps//2
    rv,thv,psv=rg[ir].item(),thg[ith].item(),psg[ips].item()
    Gsym=np.array(GdnM.subs({r:rv,th:thv,ps:psv}).evalf(),dtype=np.float64)
    return np.abs(Gsym-Gmn[ir,ith,ips].numpy()).max()

print("E. off-diagonal core: max|G_num-G_sym| vs grid (must SHRINK ~ h^2):")
for (Nr,Nth) in [(21,21),(41,41),(81,81)]:
    e=numeric_err(Nr,Nth,24)
    print(f"   Nr=Nth={Nr}: max err = {e:.3e}")

print("\nF. radial: is B=1/A FREE? check a+b NOT identically 0 in converged solve:")
xi=kap=1.0; rc=0.05; ri=rc+14.0
rgr=rbf.make_grid(1,800,rc=rc,rint=ri,geom=False,device="cpu")
out=rbf.selfconsistent_Bfree(rgr,xi,kap,p=0.4,kap8=0.05,iters=400,relax=0.4,tol=1e-12)
a=out['a'][0].numpy(); b=out['b'][0].numpy()
apb=a+b
print(f"   max|a+b| (=0 iff B=1/A pinned) = {np.abs(apb).max():.4e}")
print(f"   rms a+b = {np.sqrt((apb**2).mean()):.4e}  (nonzero => B genuinely freed)")
print(f"   a range [{a.min():.3f},{a.max():.3f}]  b range [{b.min():.3f},{b.max():.3f}]")
