"""One arrested-Newton hopfion point for convergence/scaling.
argv: N L xi kappa R0 w steps dt tag"""
import sys, math, numpy as np, torch, fs_hopfion as m
a=sys.argv
N=int(a[1]);L=float(a[2]);xi=float(a[3]);kappa=float(a[4]);R0=float(a[5]);w=float(a[6])
steps=int(a[7]);dt=float(a[8]);tag=a[9]
torch.manual_seed(0)
seed=lambda X,Y,Z: m.toroidal_seed(X,Y,Z,R0,w)
print(f'[{tag}] Newton N={N} L={L} xi={xi} kappa={kappa} R0={R0} w={w} dt={dt}',flush=True)
res=m.relax_newton(N,L,seed,xi,kappa,steps=steps,dt=dt,log_every=max(steps//4,1))
Eh=res['E']/math.sqrt(xi*kappa)
rr,loc,edmax=m.ring_radius(res)
lscale=math.sqrt(kappa/xi)
print(f"[{tag}] FINAL E={res['E']:.3f} E2/E4={res['E2']/res['E4']:.4f} Q={res['Q']:.4f} "
      f"Ehat={Eh:.3f} ring={rr:.4f} ring/sqrt(k/xi)={rr/lscale:.4f}",flush=True)
np.savez(f'pt_{tag}.npz',n=res['n'],N=N,L=L,xi=xi,kappa=kappa,h=res['h'],
         E=res['E'],E2=res['E2'],E4=res['E4'],Q=res['Q'],ring=rr,Ehat=Eh)
