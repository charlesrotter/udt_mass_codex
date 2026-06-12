import numpy as np
# ===== work outward from CG: canonical vacuum phi + canonical algebraic eigenvalues =====
# CG: box_g phi = mu^2 phi, flux form  phi'=J e^{2phi}/r^2, J'=r^2 mu^2 phi
# CG locked Branch-M: mu^2=pi/3, phi0=-cos(pi/5), r*=6.9875
# CG S19.4 canonical eigenvalues (m=1 nat. units): kappa=-1 E1=2*sqrt2/3; kappa=-2 E1=16/3
mu2=np.pi/3; phi0=-np.cos(np.pi/5); rstar=6.9875
E_k1=2*np.sqrt(2)/3; E_k2=16/3
rmin,h=1e-4,1e-4; N=int((rstar-rmin)/h); rg=rmin+h*np.arange(N+1)

def vacuum_phi():
    phi=np.empty(N+1);J=np.empty(N+1);p=phi0;j=mu2*phi0*rg[0]**3/3
    for i,r in enumerate(rg):
        phi[i]=p;J[i]=j
        f=lambda r,p,j:(j*np.exp(2*p)/r**2, r**2*mu2*p)
        k1=f(r,p,j);k2=f(r+h/2,p+h/2*k1[0],j+h/2*k1[1]);k3=f(r+h/2,p+h/2*k2[0],j+h/2*k2[1]);k4=f(r+h,p+h*k3[0],j+h*k3[1])
        p+=h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]);j+=h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
    return phi
phi_g=vacuum_phi(); phip_g=np.gradient(phi_g,rg)
print(f"canonical vacuum phi: phi(0)={phi_g[0]:.4f} phi(r*)={phi_g[-1]:.4f} e^phi(r*)={np.exp(phi_g[-1]):.3f}")

def rhs(r,y,k,E,phi,phip,m=1.0):
    G,F=y;invr=1/r
    return np.array([-(k*invr-phip)*G+(m*np.exp(phi)+E*np.exp(2*phi))*F,
                     -(-k*invr-phip)*F+(m*np.exp(phi)-E*np.exp(2*phi))*G])
def integ(k,E):
    y=np.array([1.0,0.0]) if k<0 else np.array([0.0,1.0])
    G=np.empty(N+1);F=np.empty(N+1);G[0],F[0]=y
    for i in range(N):
        r=rg[i]
        k1=rhs(r,y,k,E,phi_g[i],phip_g[i]);k2=rhs(r+h/2,y+h/2*k1,k,E,phi_g[i],phip_g[i])
        k3=rhs(r+h/2,y+h/2*k2,k,E,phi_g[i],phip_g[i]);k4=rhs(r+h,y+h*k3,k,E,phi_g[i],phip_g[i])
        y=y+h/6*(k1+2*k2+2*k3+k4);G[i+1],F[i+1]=y
    return G,F

# BC residual G'(r*) at the canonical eigenvalues (honesty check on background match)
for lab,k,E in [("kappa=-1",-1,E_k1),("kappa=-2",-2,E_k2)]:
    G,F=integ(k,E); Gp=rhs(rg[-1],np.array([G[-1],F[-1]]),k,E,phi_g[-1],phip_g[-1])[0]
    scale=np.max(np.abs(G))
    print(f"{lab} at canonical E={E:.4f}: G'(r*)/max|G| = {Gp/scale:.3e}  (Neumann BC residual)")

def norm(k,E):
    G,F=integ(k,E); nrm=np.sqrt(np.trapezoid(np.exp(phi_g)*(G**2+F**2),rg)); return G/nrm,F/nrm
Ga,Fa=norm(-1,E_k1); Gb,Fb=norm(-2,E_k2)
l=np.concatenate([[0],np.cumsum(0.5*(np.exp(phi_g[1:])+np.exp(phi_g[:-1]))*np.diff(rg))])
w=np.exp(phi_g)*(Ga*Gb+Fa*Fb)
d_coord=np.trapezoid(rg*w,rg); d_proper=np.trapezoid(l*w,rg)
print("-"*52)
print(f"E1 transition kappa=-1(l=0)<->kappa=-2(l=1), dE={E_k2-E_k1:.4f}")
print(f"radial <r>_coord   = {d_coord:.5e}")
print(f"radial <l_proper>  = {d_proper:.5e}")
print(f"|d_radial|^2 coord = {d_coord**2:.5e}  (x O(1) angular factor for full |d|^2)")
print("finite & computable from canonical eigenstates -> rates derivable from the metric")
