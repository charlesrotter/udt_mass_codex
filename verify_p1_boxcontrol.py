import numpy as np
from scipy.special import spherical_jn
from scipy.optimize import brentq

def zeros_of(l, n, xmax=60):
    xs=np.linspace(0.3,xmax,40000); f=spherical_jn(l,xs); zs=[]
    for i in range(len(xs)-1):
        if f[i]*f[i+1]<0: zs.append(brentq(lambda x: spherical_jn(l,x), xs[i],xs[i+1]))
        if len(zs)>=n: break
    return np.array(zs)

# CLAIM 2: w_n*R = const across R for the Zerilli cavity (-Psi''+l(l+1)/r^2 Psi=w^2 Psi).
# Analytic: Psi=r j_l(wr), Dirichlet at R => j_l(wR)=0 => w_n = z_{l,n}/R. So w_n*R = z_{l,n} EXACTLY.
print("CLAIM 2 box-control: w_n*R should equal the fixed Bessel zero z_{l,n} for ALL R.")
z2=zeros_of(2,6)
for R in [1,2,4,8]:
    wn = z2/R
    print(f" R={R}: w_n*R =", np.round(wn*R,10))
print(" => w_n*R = const (= j2 zeros) to machine precision, EXACT analytically. No R-drift.")
# degeneracy/avoided crossing: the single-l problem is a regular Sturm-Liouville => simple spectrum,
# n-1 interior nodes, no crossings. Verify node count for r j2(z_{2,n} r/R).
print("\n node counts (should be n-1 interior nodes):")
R=1.0
for n in range(1,5):
    w=z2[n-1]/R
    rr=np.linspace(1e-4,R*0.999,4000)
    psi=rr*spherical_jn(2,w*rr)
    nodes=np.sum(np.diff(np.sign(psi))!=0)
    print(f"   mode {n}: interior sign changes = {nodes}")
# l=3,4 ratios
for l in (3,4):
    zl=zeros_of(l,3)
    print(f" l={l} Dirichlet ratios:", np.round(zl/zl[0],4))
