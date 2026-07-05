import fs_hopfion as m, torch, math, numpy as np
torch.manual_seed(0)
N,L,xi,kappa=128,8.0,1.0,4.0
X,Y,Z,h=m.make_grid(N,L)
n_inf=torch.tensor([0.,0.,-1.],device=m.dev).view(3,1,1,1)
n=m.toroidal_seed(X,Y,Z,2.5,1.2).clone()
nr=n.clone().requires_grad_(True)
opt=torch.optim.Adam([nr],lr=1e-3)
print(f'ADAM toroidal seed N={N} L={L} xi={xi} kappa={kappa} h={h:.3f}')
for s in range(3001):
    opt.zero_grad()
    E,E2,E4,_,_=m.energy(nr,h,xi,kappa); E.backward(); opt.step()
    with torch.no_grad():
        m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
    if s%300==0 or s==3000:
        with torch.no_grad():
            E,E2,E4,_,_=m.energy(nr,h,xi,kappa)
            nf=nr/nr.norm(dim=0,keepdim=True); q=m.hopf_charge(nf,h,N,L)[0]
        print(f'  step {s:5d} E={E.item():.4f} E2={E2.item():.4f} E4={E4.item():.4f} E2/E4={E2.item()/E4.item():.4f} Q={q:.4f}')
with torch.no_grad():
    nf=nr/nr.norm(dim=0,keepdim=True)
np.savez('adam_k4.npz',n=nf.cpu().numpy(),N=N,L=L,xi=xi,kappa=kappa)
