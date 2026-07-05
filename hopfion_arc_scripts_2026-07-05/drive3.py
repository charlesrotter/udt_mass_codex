import fs_hopfion as m, torch, math, numpy as np
torch.manual_seed(0)
N,L,xi,kappa=160,8.0,1.0,4.0
seed=lambda X,Y,Z: m.toroidal_seed(X,Y,Z,2.5,1.2)
print(f'ARRESTED NEWTON N={N} L={L} xi={xi} kappa={kappa}  target Ehat=E/sqrt(xik)~275 => E~{275*math.sqrt(xi*kappa):.0f}',flush=True)
res=m.relax_newton(N,L,seed,xi,kappa,steps=4000,dt=0.004,log_every=250)
Eh=res['E']/math.sqrt(xi*kappa)
print(f"FINAL E={res['E']:.3f} E2={res['E2']:.3f} E4={res['E4']:.3f} E2/E4={res['E2']/res['E4']:.4f} Q={res['Q']:.4f} Ehat={Eh:.3f}",flush=True)
rr,loc,edmax=m.ring_radius(res)
print(f"ring_radius={rr:.4f} at ({loc[0]:.2f},{loc[1]:.2f},{loc[2]:.2f})",flush=True)
np.savez('newton_k4_N160.npz',n=res['n'],N=N,L=L,xi=xi,kappa=kappa,h=res['h'],E=res['E'],E2=res['E2'],E4=res['E4'],Q=res['Q'],ring=rr,Ehat=Eh)
