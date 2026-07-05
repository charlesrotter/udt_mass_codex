"""Gentle-Adam ckpt from the SMOOTH stereographic Hopf seed (no axis singularity).
argv: N L xi kappa a steps lr0 Qmin tag"""
import sys, math, numpy as np, torch, fs_hopfion as m
a=sys.argv
N=int(a[1]);L=float(a[2]);xi=float(a[3]);kappa=float(a[4]);ascale=float(a[5])
STEPS=int(a[6]);lr0=float(a[7]);Qmin=float(a[8]);tag=a[9]
torch.manual_seed(0)
X,Y,Z,h=m.make_grid(N,L)
n_inf=torch.tensor([0.,0.,-1.],device=m.dev).view(3,1,1,1)
nr=m.hopf_seed(X,Y,Z,ascale).clone().requires_grad_(True)
opt=torch.optim.Adam([nr],lr=lr0); sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,STEPS)
sc=math.sqrt(xi*kappa)
print(f'[{tag}] STEREO-seed CKPT N={N} L={L} xi={xi} kappa={kappa} a={ascale} h={h:.3f} lr0={lr0} Qmin={Qmin} steps={STEPS}',flush=True)
bestE=1e30;bestn=None;bestQ=0;bests=-1;bestE2=0;bestE4=0
for s in range(STEPS):
    opt.zero_grad(); E,E2,E4,_,_=m.energy(nr,h,xi,kappa); E.backward(); opt.step(); sched.step()
    with torch.no_grad():
        m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
    if s%250==0 or s==STEPS-1:
        with torch.no_grad():
            E,E2,E4,_,_=m.energy(nr,h,xi,kappa); nf=nr/nr.norm(dim=0,keepdim=True); q=abs(m.hopf_charge(nf,h,N,L)[0])
        Eh=E.item()/sc
        if q>=Qmin and E.item()<bestE:
            bestE=E.item();bestn=nf.cpu().numpy();bestQ=q;bests=s;bestE2=E2.item();bestE4=E4.item()
            np.savez(f'ckpt_{tag}.npz',n=bestn,N=N,L=L,xi=xi,kappa=kappa,h=h,E=bestE,E2=bestE2,E4=bestE4,Q=bestQ,step=bests)
        print(f'  s={s:5d} Ehat={Eh:.2f} E2/E4={E2.item()/E4.item():.3f} |Q|={q:.4f}  [best Ehat={bestE/sc:.2f} Q={bestQ:.4f}]',flush=True)
print(f'[{tag}] BEST s={bests} Ehat={bestE/sc:.3f} E2/E4={bestE2/bestE4:.4f} |Q|={bestQ:.4f}',flush=True)
