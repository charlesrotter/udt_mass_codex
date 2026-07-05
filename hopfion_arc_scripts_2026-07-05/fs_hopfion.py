"""
H3 native hopfion = flat-R^3 Faddeev-Skyrme Q_H=1 solve (bounded, single process).
E[n] = int d^3x [ (xi/2)|d_i n|^2 + (kappa/4) F_ij^2 ],  F_ij = n.(d_i n x d_j n).
Q_H = (1/16pi^2) int A.B d^3x,  B_i = 1/2 eps_ijk F_jk,  B = curl A, div A = 0.
Discipline: no potential V(n); |n|=1 exact (normalize inside energy); periodic FD;
constant exterior n_inf pinned. GPU float64.
"""
import torch, math, numpy as np

torch.set_default_dtype(torch.float64)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

def make_grid(N, L):
    x = torch.linspace(-L, L, N, device=dev)
    h = (x[1]-x[0]).item()
    X, Y, Z = torch.meshgrid(x, x, x, indexing='ij')
    return X, Y, Z, h

def hopf_seed(X, Y, Z, a):
    """Degree-1 Hopf map: inverse stereographic R^3->S^3 then Hopf S^3->S^2.
    n_inf = -z at |x|->inf."""
    rho2 = X*X + Y*Y + Z*Z
    den = a*a + rho2
    X1 = 2*a*X/den; X2 = 2*a*Y/den; X3 = 2*a*Z/den; X4 = (a*a - rho2)/den
    # Z1=X1+iX2, Z2=X3+iX4 ; n1+in2 = 2 Z1 Z2*, n3=|Z1|^2-|Z2|^2
    # 2 Z1 Z2* = 2(X1+iX2)(X3-iX4)
    n1 = 2*(X1*X3 + X2*X4)
    n2 = 2*(X2*X3 - X1*X4)
    n3 = (X1*X1 + X2*X2) - (X3*X3 + X4*X4)
    n = torch.stack([n1, n2, n3], 0)
    return n / n.norm(dim=0, keepdim=True)

def toroidal_seed(X, Y, Z, R0, w):
    """Q_H=1 toroidal ansatz: ring in z=0 plane at cyl-radius R0, core width w.
    n=(sin f cos g, sin f sin g, cos f), f=f(d) 0->pi, g=phi_tor + psi_pol (m=l=1)."""
    rho = torch.sqrt(X*X + Y*Y) + 1e-30
    phi = torch.atan2(Y, X)                      # toroidal angle
    d = torch.sqrt((rho - R0)**2 + Z*Z)          # distance from ring core
    psi = torch.atan2(Z, rho - R0)               # poloidal angle
    f = 2*torch.atan(d / w)                      # 0 at core -> pi at infinity
    g = phi + psi                                # (m,l)=(1,1)
    n = torch.stack([torch.sin(f)*torch.cos(g),
                     torch.sin(f)*torch.sin(g),
                     torch.cos(f)], 0)
    return n / n.norm(dim=0, keepdim=True)

def d_central(f, axis, h):
    return (torch.roll(f, -1, dims=axis) - torch.roll(f, 1, dims=axis)) / (2*h)

def grads(n, h):
    # returns dn[i] = d_i n, each shape (3,N,N,N); axis for spatial dim i is i+1
    return [d_central(n, i+1, h) for i in range(3)]

def energy(n_raw, h, xi, kappa):
    n = n_raw / n_raw.norm(dim=0, keepdim=True)
    dn = grads(n, h)
    # L2
    e2 = 0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
    # F_ij = n.(d_i n x d_j n)
    def cross(a, b):
        return torch.stack([a[1]*b[2]-a[2]*b[1],
                            a[2]*b[0]-a[0]*b[2],
                            a[0]*b[1]-a[1]*b[0]], 0)
    F = {}
    e4 = torch.zeros_like(e2)
    for i in range(3):
        for j in range(3):
            if i == j: continue
            Fij = (n*cross(dn[i], dn[j])).sum(0)
            F[(i,j)] = Fij
            e4 = e4 + 0.25*kappa*Fij*Fij
    dV = h**3
    E2 = e2.sum()*dV
    E4 = e4.sum()*dV
    return E2+E4, E2, E4, n, F

def hopf_charge(n, h, N, L):
    """Q_H = (1/16pi^2) int A.B, B_i=1/2 eps F_jk, B=curl A, div A=0 via FFT."""
    n = n / n.norm(dim=0, keepdim=True)
    dn = grads(n, h)
    def cross(a, b):
        return torch.stack([a[1]*b[2]-a[2]*b[1],
                            a[2]*b[0]-a[0]*b[2],
                            a[0]*b[1]-a[1]*b[0]], 0)
    # F_jk pullback; B_i = 1/2 eps_ijk F_jk = F for (jk)->i cyclic
    F = {}
    for i in range(3):
        for j in range(3):
            if i==j: continue
            F[(i,j)] = (n*cross(dn[i], dn[j])).sum(0)
    # B_x = F_yz, B_y = F_zx, B_z = F_xy
    Bx = F[(1,2)]; By = F[(2,0)]; Bz = F[(0,1)]
    B = torch.stack([Bx, By, Bz], 0)
    # solve laplacian A = -curl B  (Coulomb gauge) via FFT
    k1 = 2*math.pi*torch.fft.fftfreq(N, d=h, device=dev)
    KX, KY, KZ = torch.meshgrid(k1, k1, k1, indexing='ij')
    k2 = KX*KX + KY*KY + KZ*KZ
    k2[0,0,0] = 1.0
    # curl B in real space (FD, consistent w/ energy)
    def curl(V):
        Vx, Vy, Vz = V[0], V[1], V[2]
        cx = d_central(Vz,1,h) - d_central(Vy,2,h)
        cy = d_central(Vx,2,h) - d_central(Vz,0,h)
        cz = d_central(Vy,0,h) - d_central(Vx,1,h)
        return torch.stack([cx,cy,cz],0)
    curlB = curl(B)
    A = torch.zeros_like(B)
    for c in range(3):
        rhs = -curlB[c]  # laplacian A_c = -curl B_c
        rhsk = torch.fft.fftn(rhs)
        Ak = rhsk / (-k2)   # laplacian -> -k^2
        Ak[0,0,0] = 0.0
        A[c] = torch.fft.ifftn(Ak).real
    AB = (A*B).sum(0)
    Q = AB.sum()*h**3 / (16*math.pi**2)
    # also report div A residual and A.B integrand for diagnostics
    divA = (d_central(A[0],0,h)+d_central(A[1],1,h)+d_central(A[2],2,h))
    return Q.item(), divA.abs().mean().item(), B

def pin_boundary(n_raw, n_inf, w=2):
    n_raw[:, :w,:,:] = n_inf; n_raw[:, -w:,:,:] = n_inf
    n_raw[:, :,:w,:] = n_inf; n_raw[:, :,-w:,:] = n_inf
    n_raw[:, :,:,:w] = n_inf; n_raw[:, :,:,-w:] = n_inf
    return n_raw

def relax(N, L, a, xi, kappa, steps, lr, log_every=400, verbose=True, qlog=True):
    X,Y,Z,h = make_grid(N, L)
    n = hopf_seed(X,Y,Z,a).clone()
    n_inf = torch.tensor([0.,0.,-1.], device=dev).view(3,1,1,1)
    n_raw = n.clone().requires_grad_(True)
    opt = torch.optim.Adam([n_raw], lr=lr)
    hist=[]
    for s in range(steps):
        opt.zero_grad()
        E,E2,E4,_,_ = energy(n_raw, h, xi, kappa)
        E.backward()
        opt.step()
        with torch.no_grad():
            pin_boundary(n_raw, n_inf, w=2)
            n_raw.div_(n_raw.norm(dim=0, keepdim=True))
        if s%log_every==0 or s==steps-1:
            with torch.no_grad():
                E,E2,E4,_,_ = energy(n_raw, h, xi, kappa)
                nf=(n_raw/n_raw.norm(dim=0,keepdim=True))
                q=hopf_charge(nf,h,N,L)[0] if qlog else float('nan')
            hist.append((s,E.item(),E2.item(),E4.item(),q))
            if verbose:
                print(f"  step {s:5d}  E={E.item():.5f}  E2={E2.item():.5f}  E4={E4.item():.5f}  E2/E4={E2.item()/E4.item():.4f}  Q={q:.4f}")
    with torch.no_grad():
        n_final = (n_raw/n_raw.norm(dim=0,keepdim=True))
        E,E2,E4,_,Fdict = energy(n_raw,h,xi,kappa)
        Q, divA, B = hopf_charge(n_final, h, N, L)
    return dict(N=N,L=L,a=a,xi=xi,kappa=kappa,h=h,
                E=E.item(),E2=E2.item(),E4=E4.item(),Q=Q,divA=divA,
                n=n_final.detach().cpu().numpy(), hist=hist,
                X=X.cpu().numpy(),Y=Y.cpu().numpy(),Z=Z.cpu().numpy())

def relax_gf(N, L, seed, xi, kappa, steps, dt, log_every=400, verbose=True, qlog=True):
    """Plain tangent-projected gradient flow (respects continuum Q-barrier)."""
    X,Y,Z,h = make_grid(N, L)
    n = seed(X,Y,Z).clone()
    n_inf = torch.tensor([0.,0.,-1.], device=dev).view(3,1,1,1)
    n_raw = n.clone().requires_grad_(True)
    hist=[]
    for s in range(steps):
        if n_raw.grad is not None: n_raw.grad.zero_()
        E,E2,E4,_,_ = energy(n_raw, h, xi, kappa)
        E.backward()
        with torch.no_grad():
            g = n_raw.grad
            nn = n_raw/n_raw.norm(dim=0,keepdim=True)
            g = g - (g*nn).sum(0,keepdim=True)*nn      # tangent projection
            n_raw -= dt*g
            pin_boundary(n_raw, n_inf, w=2)
            n_raw.div_(n_raw.norm(dim=0,keepdim=True))
        if s%log_every==0 or s==steps-1:
            with torch.no_grad():
                E,E2,E4,_,_ = energy(n_raw, h, xi, kappa)
                nf=(n_raw/n_raw.norm(dim=0,keepdim=True))
                q=hopf_charge(nf,h,N,L)[0] if qlog else float('nan')
            hist.append((s,E.item(),E2.item(),E4.item(),q))
            if verbose:
                print(f"  step {s:5d}  E={E.item():.5f}  E2={E2.item():.5f}  E4={E4.item():.5f}  E2/E4={E2.item()/E4.item():.4f}  Q={q:.4f}")
    with torch.no_grad():
        n_final=(n_raw/n_raw.norm(dim=0,keepdim=True))
        E,E2,E4,_,_=energy(n_raw,h,xi,kappa)
        Q,divA,_=hopf_charge(n_final,h,N,L)
    return dict(N=N,L=L,xi=xi,kappa=kappa,h=h,E=E.item(),E2=E2.item(),E4=E4.item(),
                Q=Q,divA=divA,n=n_final.detach().cpu().numpy(),hist=hist)

def relax_newton(N, L, seed, xi, kappa, steps, dt, log_every=200, verbose=True, qlog=True):
    """Arrested Newton flow (Battye-Sutcliffe): n_tt = -grad E (tangent-projected),
    velocity Verlet, zero velocity whenever E rises. Stays in the Q basin."""
    X,Y,Z,h = make_grid(N, L)
    n = seed(X,Y,Z).clone()
    n_inf = torch.tensor([0.,0.,-1.], device=dev).view(3,1,1,1)
    nr = n.clone().requires_grad_(True)
    v = torch.zeros_like(n)
    def tgrad():
        if nr.grad is not None: nr.grad.zero_()
        E,E2,E4,_,_ = energy(nr, h, xi, kappa); E.backward()
        with torch.no_grad():
            nn = nr/nr.norm(dim=0,keepdim=True)
            g = nr.grad - (nr.grad*nn).sum(0,keepdim=True)*nn
        return g, E.item(), E2.item(), E4.item()
    with torch.no_grad():
        Eprev = energy(nr,h,xi,kappa)[0].item()
    hist=[]; narrest=0
    for s in range(steps):
        g,E,E2,E4 = tgrad()
        with torch.no_grad():
            v -= dt*g
            nn = nr/nr.norm(dim=0,keepdim=True)
            v = v - (v*nn).sum(0,keepdim=True)*nn        # keep v tangent
            nr += dt*v
            pin_boundary(nr, n_inf, w=2)
            nr.div_(nr.norm(dim=0,keepdim=True))
            Enew = energy(nr,h,xi,kappa)[0].item()
            if Enew > Eprev:                              # arrest
                v.zero_(); narrest+=1
            Eprev = Enew
        if s%log_every==0 or s==steps-1:
            with torch.no_grad():
                E,E2,E4,_,_=energy(nr,h,xi,kappa)
                nf=nr/nr.norm(dim=0,keepdim=True)
                q=hopf_charge(nf,h,N,L)[0] if qlog else float('nan')
            hist.append((s,E.item(),E2.item(),E4.item(),q))
            if verbose:
                print(f"  s={s:5d} E={E.item():.4f} E2={E2.item():.4f} E4={E4.item():.4f} E2/E4={E2.item()/E4.item():.4f} Q={q:.4f} arr={narrest}",flush=True)
    with torch.no_grad():
        n_final=nr/nr.norm(dim=0,keepdim=True)
        E,E2,E4,_,_=energy(nr,h,xi,kappa)
        Q,divA,_=hopf_charge(n_final,h,N,L)
    return dict(N=N,L=L,xi=xi,kappa=kappa,h=h,E=E.item(),E2=E2.item(),E4=E4.item(),
                Q=Q,divA=divA,n=n_final.detach().cpu().numpy(),
                X=X.cpu().numpy(),Y=Y.cpu().numpy(),Z=Z.cpu().numpy(),hist=hist)

def ring_radius(res):
    """energy-density ring radius: locate max of energy density in a slab, measure |xy|."""
    n = torch.tensor(res['n'], device=dev)
    X,Y,Z,h = make_grid(res['N'], res['L'])
    _,_,_,_,_ = energy(n, h, res['xi'], res['kappa'])
    # energy density
    nn = n/n.norm(dim=0,keepdim=True)
    dn = grads(nn,h)
    e2 = 0.5*res['xi']*sum((dn[i]*dn[i]).sum(0) for i in range(3))
    def cross(a,b):
        return torch.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],0)
    e4=torch.zeros_like(e2)
    for i in range(3):
        for j in range(3):
            if i==j:continue
            Fij=(nn*cross(dn[i],dn[j])).sum(0)
            e4=e4+0.25*res['kappa']*Fij*Fij
    ed=(e2+e4).cpu().numpy()
    # find global max location
    idx=np.unravel_index(np.argmax(ed),ed.shape)
    xg=np.linspace(-res['L'],res['L'],res['N'])
    xm,ym,zm=xg[idx[0]],xg[idx[1]],xg[idx[2]]
    rring=math.hypot(xm,ym)
    return rring, (xm,ym,zm), ed.max()

if __name__=='__main__':
    import sys
    torch.manual_seed(0)
    print("=== SEED Q_H check (no relax) ===")
    for N,L,a in [(64,6.0,1.6),(96,6.0,1.6)]:
        X,Y,Z,h=make_grid(N,L)
        n=hopf_seed(X,Y,Z,a)
        Q,divA,_=hopf_charge(n,h,N,L)
        print(f"  N={N} L={L} a={a}: Q_seed={Q:.5f}  |divA|={divA:.2e}  |n|dev={ (n.norm(dim=0)-1).abs().max().item():.2e}")
