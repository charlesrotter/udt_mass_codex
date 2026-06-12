import numpy as np

# ---- canonical Branch-M vacuum phi(r): box_g phi = mu^2 phi, flux form ----
#   phi' = J e^{2phi}/r^2 ,  J' = r^2 mu^2 phi ,  phi(0)=-cos(pi/5), J(0)=0
mu2 = np.pi/3.0
phi0 = -np.cos(np.pi/5)
rstar = 6.9875
rmin, h = 1e-4, 2e-4
N = int((rstar-rmin)/h)
rg = rmin + h*np.arange(N+1)

def vacuum_phi(rg):
    phi = np.empty_like(rg); J = np.empty_like(rg)
    # regular start: phi=phi0, J ~ mu^2 phi0 r^3/3
    p = phi0; j = mu2*phi0*rg[0]**3/3.0
    for i,r in enumerate(rg):
        phi[i]=p; J[i]=j
        # RK4 on (phi,J)
        def f(r,p,j):
            return (j*np.exp(2*p)/r**2, r**2*mu2*p)
        k1=f(r,p,j); k2=f(r+h/2,p+h/2*k1[0],j+h/2*k1[1])
        k3=f(r+h/2,p+h/2*k2[0],j+h/2*k2[1]); k4=f(r+h,p+h*k3[0],j+h*k3[1])
        p=p+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); j=j+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
    return phi
phi_g = vacuum_phi(rg)
phip_g = np.gradient(phi_g, rg)
print(f"vacuum phi: phi(0)={phi_g[0]:.4f} (target {phi0:.4f}), phi(r*)={phi_g[-1]:.4f}, e^phi(r*)={np.exp(phi_g[-1]):.3f}")

# ---- Form-T integrator (canonical eqs, matches udt_dirac_formT_solver.rhs) ----
def rhs(r,y,kappa,m,E,phi,phip):
    G,F=y; invr=1.0/r
    dG=-(kappa*invr-phip)*G+(m*np.exp(phi)+E*np.exp(2*phi))*F
    dF=-(-kappa*invr-phip)*F+(m*np.exp(phi)-E*np.exp(2*phi))*G
    return np.array([dG,dF])
def integ(kappa,m,E):
    y=np.array([1.0,0.0]) if kappa<0 else np.array([0.0,1.0])  # dominant component seed
    G=np.empty(N+1);Fc=np.empty(N+1);G[0],Fc[0]=y
    for i in range(N):
        r=rg[i]
        k1=rhs(r,y,kappa,m,E,phi_g[i],phip_g[i]); k2=rhs(r+h/2,y+h/2*k1,kappa,m,E,phi_g[i],phip_g[i])
        k3=rhs(r+h/2,y+h/2*k2,kappa,m,E,phi_g[i],phip_g[i]); k4=rhs(r+h,y+h*k3,kappa,m,E,phi_g[i],phip_g[i])
        y=y+h/6*(k1+2*k2+2*k3+k4); G[i+1],Fc[i+1]=y
    return G,Fc
def Gprime_end(kappa,m,E):  # G'(r*) for Neumann BC (kappa<0, G large)
    G,Fc=integ(kappa,m,E)
    return rhs(rg[-1],np.array([G[-1],Fc[-1]]),kappa,m,E,phi_g[-1],phip_g[-1])[0], (G,Fc)

def eigenvalues(kappa,m=1.0,Emax=10.0,nE=4000):
    Es=np.linspace(0.05,Emax,nE); vals=[]
    prev=None
    for E in Es:
        v=Gprime_end(kappa,m,E)[0]
        if prev is not None and np.isfinite(v) and np.isfinite(prev) and v*prev<0:
            # bisect
            lo,hi=Eprev,E
            for _ in range(60):
                mid=0.5*(lo+hi); vm=Gprime_end(kappa,m,mid)[0]
                if vm*Gprime_end(kappa,m,lo)[0]<0: hi=mid
                else: lo=mid
            vals.append(0.5*(lo+hi))
        prev=v; Eprev=E
    return vals

ev_m1 = eigenvalues(-1)
print(f"kappa=-1 eigenvalues (m=1, BC G'(r*)=0): {[f'{e:.4f}' for e in ev_m1[:4]]}")
print(f"  canonical electron anchor target E1 = 2*sqrt2/3 = {2*np.sqrt(2)/3:.4f}")
ev_m2 = eigenvalues(-2)
print(f"kappa=-2 eigenvalues: {[f'{e:.4f}' for e in ev_m2[:4]]}  (target 16/3={16/3:.4f})")

# ---- normalized eigenfunctions + radial dipole matrix element ----
def norm_state(kappa,E):
    G,Fc=integ(kappa,1.0,E)
    nrm=np.sqrt(np.trapezoid(np.exp(phi_g)*(G**2+Fc**2),rg))
    return G/nrm, Fc/nrm
if ev_m1 and ev_m2:
    Ga,Fa=norm_state(-1,ev_m1[0]); Gb,Fb=norm_state(-2,ev_m2[0])
    # E1 dipole radial integral, physical-norm weight e^phi, coordinate r and proper distance l=int e^phi dr
    l = np.concatenate([[0],np.cumsum(0.5*(np.exp(phi_g[1:])+np.exp(phi_g[:-1]))*np.diff(rg))])
    integrand = np.exp(phi_g)*(Ga*Gb+Fa*Fb)
    d_coord = np.trapezoid(rg*integrand, rg)
    d_proper= np.trapezoid(l *integrand, rg)
    dE = ev_m2[0]-ev_m1[0]
    print("-"*50)
    print(f"transition kappa=-1(l=0) -> kappa=-2(l=1), dE={dE:.4f} (natural units)")
    print(f"radial <r>      (coord)  = {d_coord:.5e}  [units of r*]")
    print(f"radial <l_proper>        = {d_proper:.5e}")
    print(f"|d_radial|^2 (coord)     = {d_coord**2:.5e}")
    print("NOTE: x angular Clebsch factor (O(1)) for full |d|^2; particle-scale, NOT thermal-CMB.")
