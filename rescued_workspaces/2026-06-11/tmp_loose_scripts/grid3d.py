import numpy as np
# Brute-force the FULL first-order curved-space Dirac operator on a 3D grid, for a STATIC
# metric perturbation h_ij(x) = f(r) H_ij (H const sym traceless). Build H_Dirac numerically,
# act on a kappa=-1 spinor mode, and read off the kappa-channel content of the result.
# This includes BOTH the vierbein (kinetic) modification AND the spin connection automatically,
# because we build the operator from the metric directly via the standard formula.
#
# Curved Dirac (static, 3+1, weak field): H = beta m + (1/2){ alpha^i, e^a_i(...) }... 
# We use the well-established weak-field Dirac Hamiltonian (e.g. linearized):
#   H = beta m + alpha^i p_i  - (1/2) h_{ij} alpha^i p^j  (vierbein/kinetic)  + H_spinconn
# H_spinconn (static spatial h) = -(1/4) eps_{ijk} (partial_j h_{kl}) alpha^l Sigma^i   (schematic, antisym part)
# Rather than trust coefficients, build everything from finite differences of the vierbein.
#
# Standard exact construction: gamma^mu_curved = e^mu_a gamma^a, spin connection
#   omega_mu^{ab} = e^a_nu (partial_mu e^{b nu} + Gamma^nu_{mu lambda} e^{b lambda}).
# Dirac: i gamma^a e_a^mu (partial_mu + (1/4) omega_mu^{bc} gamma_b gamma_c) psi = m psi.
# We implement e^a_i = delta^a_i - (1/2) h^a_i (linearized), e_a^i = delta + (1/2) h, on a grid.

# 3D grid
N=41; L=4.0; ax=np.linspace(-L,L,N); dx=ax[1]-ax[0]
X,Yg,Zg=np.meshgrid(ax,ax,ax,indexing='ij'); R=np.sqrt(X**2+Yg**2+Zg**2)+1e-9
nh=[X/R,Yg/R,Zg/R]
Hc=np.diag([-1.,-1.,2.])/np.sqrt(6)  # H_ij const
def fprof(r): return np.exp(-(r-2.0)**2)  # localized radial profile f(r), shell at r=2
f=fprof(R)
h=np.zeros((3,3,N,N,N)); 
for i in range(3):
    for j in range(3): h[i,j]=f*Hc[i,j]

# gamma matrices (Dirac rep), 4-spinors
I2=np.eye(2); Z2=np.zeros((2,2))
sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]]);sz=np.array([[1,0],[0,-1]],complex)
sig=[sx,sy,sz]
def blk(a,b,c,d): return np.block([[a,b],[c,d]])
alpha=[blk(Z2,s,s,Z2) for s in sig]
beta=blk(I2,Z2,Z2,I2)

def d(arr,axis): return np.gradient(arr,dx,axis=axis)

# vierbein e^a_i = delta - 1/2 h ; inverse e_a^i = delta + 1/2 h (linear)
# tetrad-frame: H = beta m + alpha^a e_a^i ( -i partial_i + spinconn_i )
# spin connection (spatial, static), linearized:  omega_i^{ab}=(1/2)(partial^b h_{ai}-partial^a h_{bi})
# Gamma_i = (1/4) omega_i^{ab} gamma_a gamma_b ; for spatial a,b: gamma_a gamma_b = -i eps_{abc} Sigma^c-ish
# Build (1/4) omega_i^{ab} alpha-rotation acting on spinor. Use Sigma^c=diag(sig^c,sig^c).
Sig=[blk(s,Z2,Z2,s) for s in sig]
def eps(a,b,c):
    return (a-b)*(b-c)*(c-a)/2

# Apply H_Dirac to a 4-spinor field PSI (shape (4,N,N,N)) -> returns same shape (first order in h).
def Hdirac(PSI):
    out=np.zeros_like(PSI)
    # kinetic with inverse vierbein e_a^i = delta + 1/2 h^a_i
    for a in range(3):
        # partial_i acting -> -i d_i ; tetrad alpha^a contracts e_a^i
        for i in range(3):
            eai = (1.0 if a==i else 0.0) + 0.5*h[a,i]
            # term: alpha[a] * eai * (-i d_i PSI)
            dpsi=np.stack([ -1j*d(PSI[c],i) for c in range(4)])
            out += np.einsum('cd,dxyz->cxyz', alpha[a], eai*dpsi)
    # spin connection: Gamma_i=(1/4) omega_i^{ab} (1/4-> use gamma_a gamma_b). 
    # H contribution = alpha^a e_a^i Gamma_i ~ alpha^i Gamma_i (first order eai->delta)
    # omega_i^{ab} = 1/2 (d_b h_{a i} - d_a h_{b i})  (linearized symmetric gauge)
    for i in range(3):
        Gam=np.zeros((4,4),complex)
        for a in range(3):
            for b in range(3):
                om = 0.5*(d(h[a,i],b)-d(h[b,i],a))
                # (1/4) gamma_a gamma_b ; spatial gamma_a gamma_b = -alpha_a alpha_b? use Sigma
                # (1/4)[gamma_a,gamma_b]/... -> (1/4)*(-i eps_{abc} 2 Sigma_c)= -(i/2)eps Sigma
                # We'll use Gamma_i=(1/4) om_i^{ab} gamma_a gamma_b ; gamma_a gamma_b (a!=b)= -i eps_{abc} Sigma_c (in this rep up to sign)
                for c in range(3):
                    e=eps(a,b,c)
                    if e!=0:
                        Gam += 0.25*om.mean()*0  # placeholder; om is a field, handle below
        # handle field-valued spin connection properly:
        Gfield=np.zeros((4,4,N,N,N),complex)
    # do spin connection field-valued:
    for i in range(3):
        for a in range(3):
            for b in range(3):
                if a==b: continue
                om=0.5*(d(h[a,i],b)-d(h[b,i],a))
                for c in range(3):
                    e=eps(a,b,c)
                    if e==0: continue
                    M=-0.25j*e*Sig[c]   # (1/4) gamma_a gamma_b -> -(i/4)eps Sigma_c
                    # H term: alpha^i * Gamma_i ; contract alpha[i]@M
                    AM=alpha[i]@M
                    out+=np.einsum('cd,dxyz->cxyz', AM, om*PSI)
    out+=np.einsum('cd,dxyz->cxyz', beta, 0.0*PSI)  # mass term irrelevant for angular content
    return out

# kappa=-1 ground spinor: large Om_{-1} (l=0), small i f Om_{+1} (l=1). Build on grid with radial g,fr.
def Y(l,m,th,ph):
    from scipy.special import sph_harm
    return sph_harm(m,l,ph,th)
TH=np.arccos(np.clip(Zg/R,-1,1)); PHI=np.arctan2(Yg,X)
def omega_grid(k,mu):
    def l_of(k): return k if k>0 else -k-1
    def j_of(k): return abs(k)-0.5
    l=l_of(k);j=j_of(k)
    a=np.sqrt((l+mu+0.5)/(2*l+1)); b=np.sqrt((l-mu+0.5)/(2*l+1))
    if k>0: a=-np.sqrt((l-mu+0.5)/(2*l+1)); b=np.sqrt((l+mu+0.5)/(2*l+1))
    up=a*Y(l,int(mu-0.5),TH,PHI) if abs(int(mu-0.5))<=l else np.zeros_like(R,complex)
    dn=b*Y(l,int(mu+0.5),TH,PHI) if abs(int(mu+0.5))<=l else np.zeros_like(R,complex)
    return up,dn
gr=np.exp(-(R-2.0)**2)  # radial weight (shell)
mu=0.5
up_m1=omega_grid(-1,mu); up_p1=omega_grid(1,mu)
PSI=np.zeros((4,N,N,N),complex)
PSI[0]=gr*up_m1[0]; PSI[1]=gr*up_m1[1]          # large comp Om_{-1}
PSI[2]=1j*gr*up_p1[0]; PSI[3]=1j*gr*up_p1[1]    # small comp i Om_{+1}

OUT=Hdirac(PSI)

# Project OUT onto kappa channels. Project each Dirac 2-spinor part (upper, lower) onto Om_{k}.
# Angular projection at fixed shell: integrate over angles with radial weight folded in.
def proj_channel(comp_up,comp_dn,k,mu):
    ou,od=omega_grid(k,mu)
    num=np.sum(np.conj(ou)*comp_up+np.conj(od)*comp_dn)
    return num
# build channel power for upper (large) Dirac part across kappa, summing mu and the gr weight implicitly
def channel_power(part_up,part_dn,klist):
    res={}
    for k in klist:
        def j_of(k): return abs(k)-0.5
        mus=[(-2*j_of(k)+2*t)/2 for t in range(int(2*j_of(k))+1)]
        s=0.0
        for m in mus:
            s+=abs(proj_channel(part_up,part_dn,k,m))**2
        res[k]=s
    return res
klist=[-1,1,-2,2,-3,3,-4,4,-5]
# upper Dirac 2-spinor of OUT:
up_part=(OUT[0],OUT[1]); dn_part=(OUT[2],OUT[3])
pu=channel_power(up_part[0],up_part[1],klist)
pd=channel_power(dn_part[0],dn_part[1],klist)
tot={k:pu[k]+pd[k] for k in klist}
mx=max(tot.values())
print("Full curved-Dirac H applied to kappa=-1 ground spinor (h=f(r)H, m0). Channel power (norm):")
for k in klist:
    print(f"  kappa={k:+d}: {tot[k]/mx:.4e} {'  <== kappa=-4' if k==-4 else ''}")
print(f"\nkappa=-4 relative power = {tot[-4]/mx:.2e}  -> {'LEAK' if tot[-4]/mx>1e-3 else 'NO first-order leak (within grid noise)'}")
