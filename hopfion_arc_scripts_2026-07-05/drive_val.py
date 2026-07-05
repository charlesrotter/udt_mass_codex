"""Flexible FS hopfion validation driver.
Usage: python3 drive_val.py N L xi kappa R0 w steps lr tag
Relaxes (Adam, lr-decay, toroidal seed), reports E,E2,E4,Q,ring radius, core width,
and dimensionless Ehat=E/sqrt(xi*kappa). Saves field npz."""
import sys, math, numpy as np, torch
import fs_hopfion as m

def run(N,L,xi,kappa,R0,w,steps,lr,tag):
    X,Y,Z,h=m.make_grid(N,L)
    n_inf=torch.tensor([0.,0.,-1.],device=m.dev).view(3,1,1,1)
    n=m.toroidal_seed(X,Y,Z,R0,w).clone()
    nr=n.clone().requires_grad_(True)
    opt=torch.optim.Adam([nr],lr=lr)
    sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,steps)
    for s in range(steps):
        opt.zero_grad()
        E,E2,E4,_,_=m.energy(nr,h,xi,kappa); E.backward(); opt.step(); sched.step()
        with torch.no_grad():
            m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
    with torch.no_grad():
        nf=nr/nr.norm(dim=0,keepdim=True)
        E,E2,E4,_,_=m.energy(nr,h,xi,kappa)
        Q,divA,_=m.hopf_charge(nf,h,N,L)
    res=dict(N=N,L=L,xi=xi,kappa=kappa,h=h,E=E.item(),E2=E2.item(),E4=E4.item(),
             Q=Q,n=nf.cpu().numpy(),X=X.cpu().numpy(),Y=Y.cpu().numpy(),Z=Z.cpu().numpy())
    rr,loc,edmax=m.ring_radius(res)
    Ehat=E.item()/math.sqrt(xi*kappa)
    # core width: energy-density FWHM across the ring tube in the z=0 plane along +x through ring
    print(f"[{tag}] N={N} L={L} xi={xi} kappa={kappa} h={h:.4f} steps={steps}")
    print(f"   E={E.item():.4f} E2={E2.item():.4f} E4={E4.item():.4f} E2/E4={E2.item()/E4.item():.4f}")
    print(f"   Q={Q:.4f}  ring_radius={rr:.4f}  Ehat=E/sqrt(xi*k)={Ehat:.4f}  (target~275)")
    np.savez(f'val_{tag}.npz', n=nf.cpu().numpy(),N=N,L=L,xi=xi,kappa=kappa,h=h,
             E=E.item(),E2=E2.item(),E4=E4.item(),Q=Q,ring=rr,Ehat=Ehat)
    return res, Ehat, rr

if __name__=='__main__':
    a=sys.argv
    N=int(a[1]);L=float(a[2]);xi=float(a[3]);kappa=float(a[4]);R0=float(a[5]);w=float(a[6])
    steps=int(a[7]);lr=float(a[8]);tag=a[9]
    torch.manual_seed(0)
    run(N,L,xi,kappa,R0,w,steps,lr,tag)
