"""H3 PRODUCTION rerun — the LOAD-BEARING A-vs-D test (2026-07-06, Category-A numerics).

Topology-preserving ARRESTED-NEWTON flow (Battye-Sutcliffe standard for FS hopfions),
NOT unconstrained Adam. The A-vs-D discriminator is RESOLUTION: on a lattice fine enough
to resolve the tube core, the discrete Q_H=1 hopfion is a genuine local minimum with a
barrier to shrinking; too coarse, the barrier vanishes and it slips through the grid.

Success (=> A) ONLY IF the FINAL relaxed field simultaneously holds:
  (i) |Q_H| ~ 1 on the RELAXED field, (ii) finite NONZERO energy, (iii) localized toroidal
  structure (a ring), (iv) stable virial balance E2/E4 -> 1.
Otherwise (unwinds / collapses / Q->0) => D (tool-limited).

Tracks, every log: Q_H, E, E2, E4, virial E2/E4, ring radius, core tube width, points-across-core (w/h).
No masses/labels/data/fitting. Bounded, ONE foreground process, no background poll.

argv: N L xi kappa seed seedsize STEPS dt tag
  seed = 'tor' (toroidal ring R0=seedsize, core=0.5*seedsize) or 'hopf' (stereographic, a=seedsize)
"""
import sys, math, numpy as np, torch, fs_hopfion as m

a = sys.argv
N=int(a[1]); L=float(a[2]); xi=float(a[3]); kappa=float(a[4])
seed=a[5]; ssize=float(a[6]); STEPS=int(a[7]); dt=float(a[8]); tag=a[9]
RESCALE_EVERY = int(a[11]) if len(a)>11 else 0   # 0=off; else Derrick-rescale the scale zero-mode every K steps
dev=m.dev
torch.manual_seed(0)

X,Y,Z,h = m.make_grid(N,L)
n_inf = torch.tensor([0.,0.,-1.], device=dev).view(3,1,1,1)
restart = a[10] if len(a)>10 else None
if restart:
    dat = np.load(restart)
    nc = torch.tensor(dat['n'], device=dev)  # (3, Nc,Nc,Nc) on box [-Lc,Lc]
    Nc = int(dat['N']); Lc = float(dat['L'])
    # physical-coordinate-aware resample onto the new [-L,L] N^3 grid (handles N-change AND box-change).
    # grid_sample grid last-dim order (x,y,z)->(W,H,D) = reverse of our (axis0,1,2); border-pad = n_inf tail.
    xg = torch.linspace(-L,L,N,device=dev)
    GX,GY,GZ = torch.meshgrid(xg,xg,xg,indexing='ij')
    grid = torch.stack([GZ/Lc, GY/Lc, GX/Lc], -1).unsqueeze(0)  # normalized into old box
    nc = torch.nn.functional.grid_sample(nc.unsqueeze(0), grid, mode='bilinear',
                                         padding_mode='border', align_corners=True).squeeze(0)
    print(f'[{tag}] RESTART from {restart}: N {Nc}->{N}, box L {Lc}->{L}',flush=True)
    nseed = nc
elif seed=='tor':
    nseed = m.toroidal_seed(X,Y,Z, ssize, 0.5*ssize)
else:
    nseed = m.hopf_seed(X,Y,Z, ssize)
nseed = nseed / nseed.norm(dim=0,keepdim=True)
sc = math.sqrt(xi*kappa)

def endensity(n):
    n = n/n.norm(dim=0,keepdim=True)
    dn = m.grads(n,h)
    e2 = 0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
    def cross(a,b):
        return torch.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],0)
    e4=torch.zeros_like(e2)
    for i in range(3):
        for j in range(3):
            if i==j: continue
            Fij=(n*cross(dn[i],dn[j])).sum(0)
            e4=e4+0.25*kappa*Fij*Fij
    return (e2+e4)

_xg = np.linspace(-L,L,N)
_XX,_YY,_ZZ = np.meshgrid(_xg,_xg,_xg,indexing='ij')
_interior = (np.abs(_XX)<0.8*L)&(np.abs(_YY)<0.8*L)&(np.abs(_ZZ)<0.8*L)

def geom(n):
    """ring radius (cyl-radius of the interior energy-density max) + core tube FWHM
    measured radially through that max; returns (Rring, core_w, coreOverH, (xm,ym,zm)).
    INTERIOR-MASKED: exclude a boundary margin (the pin jump spikes energy at the box edge)."""
    ed = endensity(n)
    edn = ed.detach().cpu().numpy()
    edm = np.where(_interior, edn, -1.0)
    idx = np.unravel_index(np.argmax(edm), edm.shape)
    xg = _xg
    xm,ym,zm = xg[idx[0]],xg[idx[1]],xg[idx[2]]
    # ROBUST ring radius = ENERGY-WEIGHTED mean cyl-radius over the interior (the per-point argmax is a
    # near-axis spike artifact — verifier af9b56bc, 2026-07-06). This is the physically meaningful metric.
    _rho = np.sqrt(_XX*_XX + _YY*_YY)
    edI = np.where(_interior, edn, 0.0)
    Rring = float((edI*_rho).sum()/max(edI.sum(),1e-30))   # <rho>_E  (torus => ~1.2)
    # radial profile through the per-point peak in the z=zm plane, along the azimuth of the peak (core-width proxy)
    kz = idx[2]
    plane = edn[:,:,kz]
    if math.hypot(xm,ym) < 1e-6:
        return Rring, float('nan'), float('nan'), (xm,ym,zm)
    # sample energy density along the ray from axis through the peak (xm,ym) for a core-width proxy
    rpk = math.hypot(xm,ym)
    ux,uy = xm/rpk, ym/rpk
    rs = np.linspace(0, L, 400)
    xs = rs*ux; ys = rs*uy
    ix = np.clip(((xs+L)/(2*L)*(N-1)).astype(int),0,N-1)
    iy = np.clip(((ys+L)/(2*L)*(N-1)).astype(int),0,N-1)
    prof = plane[ix,iy]
    pk = prof.max(); half = 0.5*pk
    above = np.where(prof>=half)[0]
    if len(above)<2:
        return Rring, float('nan'), float('nan'), (xm,ym,zm)
    core_w = rs[above[-1]]-rs[above[0]]
    return Rring, core_w, core_w/h, (xm,ym,zm)

# ---- Derrick scale-mode relaxation: n(x) -> n(x/lambda), lambda*=sqrt(E4/E2) balances the virial ----
# (moves along the EXACT scaling zero-mode to its stationary point; the minimizer IS scale-stationary,
#  so this imposes nothing — it relaxes the one mode arrested-Newton is critically slow on. Category-A.)
_base = torch.stack(torch.meshgrid(torch.linspace(-1,1,N,device=dev),
                                   torch.linspace(-1,1,N,device=dev),
                                   torch.linspace(-1,1,N,device=dev), indexing='ij'), -1)  # (N,N,N,3) in [-1,1]
def rescale(n_raw, lam):
    # sample field at x/lam: grid coords scaled by 1/lam (border-pad = n_inf tail). Damped/clamped by caller.
    with torch.no_grad():
        nn = (n_raw/n_raw.norm(dim=0,keepdim=True)).unsqueeze(0)  # (1,3,N,N,N)
        g = (_base/lam).flip(-1).unsqueeze(0)  # grid_sample wants (x,y,z)->(col,row,dep) reversed order
        out = torch.nn.functional.grid_sample(nn, g, mode='bilinear',
                                              padding_mode='border', align_corners=True).squeeze(0)
        out = out/out.norm(dim=0,keepdim=True)
        n_raw.copy_(out)
    return n_raw

# ---- arrested Newton flow (topology-preserving; velocity Verlet, arrest on E rise) ----
nr = nseed.clone().requires_grad_(True)
v = torch.zeros_like(nseed)
with torch.no_grad():
    Eprev = m.energy(nr,h,xi,kappa)[0].item()
narr=0
print(f'[{tag}] ARRESTED-NEWTON N={N} L={L} h={h:.4f} xi={xi} kappa={kappa} seed={seed} ssize={ssize} dt={dt} steps={STEPS}',flush=True)
print(f'[{tag}] {"step":>6} {"Ehat":>8} {"E2":>9} {"E4":>9} {"E2/E4":>7} {"|Q|":>7} {"Rring":>6} {"core_w":>6} {"w/h":>5} {"arr":>5}',flush=True)
LOG = max(1, STEPS//40)
def tgrad():
    if nr.grad is not None: nr.grad.zero_()
    E,E2,E4,_,_ = m.energy(nr,h,xi,kappa); E.backward()
    with torch.no_grad():
        nn = nr/nr.norm(dim=0,keepdim=True)
        g = nr.grad - (nr.grad*nn).sum(0,keepdim=True)*nn
    return g,E.item(),E2.item(),E4.item()
def logline(s):
    with torch.no_grad():
        E,E2,E4,_,_ = m.energy(nr,h,xi,kappa)
        nf = nr/nr.norm(dim=0,keepdim=True)
        q = abs(m.hopf_charge(nf,h,N,L)[0])
        R,cw,coh,loc = geom(nf)
        E2v,E4v = E2.item(),E4.item()
    cws = f'{cw:.3f}' if cw==cw else '  nan'
    cohs= f'{coh:.2f}' if coh==coh else ' nan'
    print(f'[{tag}] {s:>6} {E.item()/sc:>8.2f} {E2v:>9.2f} {E4v:>9.2f} {E2v/E4v:>7.3f} {q:>7.4f} {R:>6.3f} {cws:>6} {cohs:>5} z={loc[2]:+.2f} {narr:>5}',flush=True)
    return E.item(),E2v,E4v,q,R,cw
logline(0)
for s in range(1,STEPS+1):
    g,E,E2,E4 = tgrad()
    with torch.no_grad():
        v -= dt*g
        nn = nr/nr.norm(dim=0,keepdim=True)
        v = v - (v*nn).sum(0,keepdim=True)*nn
        nr += dt*v
        m.pin_boundary(nr,n_inf,2); nr.div_(nr.norm(dim=0,keepdim=True))
        Enew = m.energy(nr,h,xi,kappa)[0].item()
        if Enew>Eprev:
            v.zero_(); narr+=1
        Eprev=Enew
    if RESCALE_EVERY and s%RESCALE_EVERY==0 and E2>0 and E4>0:
        lam_star = math.sqrt(E4/E2)
        lam = min(1.18, max(0.85, lam_star**0.4))   # damped + clamped for topology safety
        with torch.no_grad():
            rescale(nr, lam)
            m.pin_boundary(nr, n_inf, 2); nr.div_(nr.norm(dim=0,keepdim=True))
            v.zero_()
            Eprev = m.energy(nr,h,xi,kappa)[0].item()
    if s%LOG==0 or s==STEPS:
        logline(s)
Efin,E2f,E4f,qf,Rf,cwf = logline(STEPS)
# classification — three-way: Q must HOLD (topology), energy finite, virial balanced + localized ring for A.
q_held   = abs(qf-1)<0.15                 # topology preserved
e_finite = Efin>1e-2*sc                    # not decayed to vacuum
virial   = 0.7<E2f/E4f<1.4                 # at the FS virial minimum
localized= (cwf==cwf) and (Rf>2*h)         # a resolved off-axis ring
if not q_held or not e_finite:
    cls='COLLAPSED/UNWOUND(->D at this resolution)'
elif virial and localized:
    cls='HOLDS+CONVERGED(->A candidate: Q~1, virial-balanced, localized ring)'
else:
    cls='HOLDS-BUT-UNCONVERGED(Q~1 held, energy finite; virial/ring not yet reached -> need more steps or finer grid)'
with torch.no_grad():
    nf=(nr/nr.norm(dim=0,keepdim=True)).cpu().numpy()
np.savez(f'prod_{tag}.npz', n=nf, N=N,L=L,xi=xi,kappa=kappa,h=h, E=Efin,E2=E2f,E4=E4f,Q=qf,Rring=Rf,core_w=cwf)
print(f'[{tag}] FINAL Ehat={Efin/sc:.3f} E2/E4={E2f/E4f:.4f} |Q|={qf:.4f} Rring={Rf:.3f} core_w={cwf:.3f} w/h={cwf/h:.2f}',flush=True)
print(f'[{tag}] CLASS={cls}',flush=True)
