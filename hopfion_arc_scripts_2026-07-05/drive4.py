import fs_hopfion as m, torch, math, numpy as np
torch.manual_seed(0)
N,L,xi,kappa=160,8.0,1.0,4.0
X,Y,Z,h=m.make_grid(N,L)
n_inf=torch.tensor([0.,0.,-1.],device=m.dev).view(3,1,1,1)
n=m.toroidal_seed(X,Y,Z,2.5,1.2).clone()
nr=n.clone().requires_grad_(True)
STEPS=6000; lr0=1.5e-4
opt=torch.optim.Adam([nr],lr=lr0)
sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,STEPS)
print(f'GENTLE ADAM N={N} L={L} xi={xi} kappa={kappa} h={h:.3f} lr0={lr0} steps={STEPS} target E~{275*math.sqrt(xi*kappa):.0f}',flush=True)
for s in range(STEPS):
    opt.zero_grad()
    E,E2,E4,_,_=m.energy(nr,h,xi,kappa); E.backward(); opt.step(); sched.step()
    with torch.no_grad():
        m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
    if s%500==0 or s==STEPS-1:
        with torch.no_grad():
            E,E2,E4,_,_=m.energy(nr,h,xi,kappa)
            nf=nr/nr.norm(dim=0,keepdim=True); q=m.hopf_charge(nf,h,N,L)[0]
        print(f'  s={s:5d} E={E.item():.3f} Ehat={E.item()/math.sqrt(xi*kappa):.2f} E2/E4={E2.item()/E4.item():.4f} Q={q:.4f}',flush=True)
with torch.no_grad():
    nf=nr/nr.norm(dim=0,keepdim=True)
    E,E2,E4,_,_=m.energy(nr,h,xi,kappa); Q,_,_=m.hopf_charge(nf,h,N,L)
np.savez('adam_gentle_N160.npz',n=nf.cpu().numpy(),N=N,L=L,xi=xi,kappa=kappa,h=h,E=E.item(),E2=E2.item(),E4=E4.item(),Q=Q)
print(f'SAVED final E={E.item():.3f} Ehat={E.item()/math.sqrt(xi*kappa):.2f} Q={Q:.4f}',flush=True)
