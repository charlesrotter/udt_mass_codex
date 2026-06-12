import numpy as np
from scipy.integrate import solve_ivp

def phi_metric(r):
    return 0.5*np.log(r/(2.0+r))
def phip_metric(r):
    return 1.0/(r*(2.0+r))

m = 1.0

def rhs(r, y, E, kappa, sign):
    # sign=+1: operator sees PHI=+phi (bare, phi<=0).  sign=-1: operator sees PHI=-phi (>0)
    PHI = sign*phi_metric(r)
    PHIp = sign*phip_metric(r)
    G, F = y
    e2 = np.exp(2*PHI); e1 = np.exp(PHI)
    Gp = (PHIp - kappa/r)*G + (E*e2 + m*e1)*F
    Fp = (PHIp + kappa/r)*F - (E*e2 - m*e1)*G
    return [Gp, Fp]

def shoot(E, kappa, sign, r0=1e-6, rmax=40.0, npts=20000):
    # Start near origin. For kappa<0, G~r^{|kappa|... } small-r behavior; use regular solution.
    # Small-r: PHI -> sign*0.5 ln(r/2) -> -inf*sign. For bare (sign+1) PHI->-inf, e^PHI->0,
    # e^2PHI->0; centrifugal kappa/r dominates: G'~ -kappa/r G, F'~ +kappa/r F.
    # regular soln picks G~r^{-kappa}, F~r^{kappa} for the dominant balance -> for kappa=-1 G~r, F~r^-1 (sing)
    # Better: choose the regular combination. We'll start with G,F from leading powers of the
    # full singular system. Simpler robust approach: integrate inward+outward and match.
    # Use a power-series-free start: pick small r0 and the decaying/regular branch via the
    # frozen eigenvector with Re(lambda)>0 (growing outward = regular at 0 means we want the
    # solution that DECAYS toward 0, i.e. grows outward).
    # Start: G=r0^{|kappa|}, F sized by relation. We'll just set the regular leading behavior.
    ak = abs(kappa)
    if kappa < 0:
        G0 = r0**(ak); F0 = 0.0
    else:
        G0 = 0.0; F0 = r0**(ak)
    y0=[G0,F0]
    rs=np.linspace(r0,rmax,npts)
    sol=solve_ivp(rhs,[r0,rmax],y0,args=(E,kappa,sign),t_eval=rs,
                  rtol=1e-9,atol=1e-12,method='RK45',max_step=0.02)
    return sol

def count_nodes_and_tail(E,kappa,sign,rmax=40.0):
    sol=shoot(E,kappa,sign,rmax=rmax)
    G=sol.y[0]; r=sol.t
    # normalize by max abs to control overflow
    # count nodes of G in interior (r< rmax)
    s=np.sign(G)
    nodes=np.sum((s[:-1]*s[1:])<0)
    tail=G[-1]/ (np.max(np.abs(G))+1e-300)
    return nodes, tail, sol

# Bound-state condition: the decaying exterior. For 0<E<m and PHI->0 exterior,
# decay rate beta=sqrt(m^2-E^2). A bound state => G stays bounded/decays; generic E => blows up.
# Use sign of the tail (the diverging part flips sign as E crosses an eigenvalue) + node count.

def tail_at(E,kappa,sign,rmax=40.0):
    sol=shoot(E,kappa,sign,rmax=rmax)
    G=sol.y[0]
    # weight by exp(+beta r) growth removal: the divergent solution ~ e^{+beta r}.
    beta=np.sqrt(max(m**2-E**2,1e-12))
    val=G[-1]*np.exp(-beta*(sol.t[-1]))  # if pure decaying, ->0; divergent part survives sign
    return G[-1], val

print("=== Operator sees BARE phi (sign=+1, PHI<=0): expect NO bound states ===")
for kappa in [-1,-2,-3]:
    Es=np.linspace(0.02,0.98,49)
    signs=[]
    for E in Es:
        g_end,_=tail_at(E,kappa,1)
        signs.append(np.sign(g_end))
    signs=np.array(signs)
    flips=np.sum(signs[:-1]*signs[1:]<0)
    print(f"  kappa={kappa}: sign-flips of G(rmax) over E in (0,1): {flips}")
