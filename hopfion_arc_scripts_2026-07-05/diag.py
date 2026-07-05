import fs_hopfion as m, torch, math
torch.manual_seed(0)
N,L,xi,kappa=96,8.0,1.0,4.0
X,Y,Z,h=m.make_grid(N,L)
n_inf=torch.tensor([0.,0.,-1.],device=m.dev).view(3,1,1,1)
n=m.toroidal_seed(X,Y,Z,2.5,1.2).clone()
nr=n.clone().requires_grad_(True)
lr=1e-4
opt=torch.optim.Adam([nr],lr=lr)
print(f'DIAG lr={lr} N={N} kappa={kappa} h={h:.3f}',flush=True)
for s in range(1201):
    opt.zero_grad()
    E,E2,E4,_,_=m.energy(nr,h,xi,kappa); E.backward(); opt.step()
    with torch.no_grad():
        m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
    if s%100==0:
        with torch.no_grad():
            E,E2,E4,_,_=m.energy(nr,h,xi,kappa)
            nf=nr/nr.norm(dim=0,keepdim=True); q=m.hopf_charge(nf,h,N,L)[0]
        print(f'  s={s:4d} E={E.item():.3f} E2/E4={E2.item()/E4.item():.3f} Q={q:.4f}',flush=True)
