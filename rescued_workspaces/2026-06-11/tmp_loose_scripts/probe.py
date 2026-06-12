import numpy as np
from numpy import pi as PI, cos, exp, sqrt
from scipy.integrate import solve_ivp
from scipy.linalg import solve_banded
from numpy.polynomial.legendre import leggauss

phi0=-cos(PI/5); MU2=PI/3; MU=sqrt(MU2); rstar=6.9875; ALPHA=1/(4*PI); r0=1e-6
RMAX=16.0; NG=4000
rg=np.linspace(r0,RMAX,NG); dr=rg[1]-rg[0]
def vac_rhs(r,y): return [y[1]*exp(2*y[0])/r**2 if r>0 else 0.0, r**2*MU2*y[0]]
y0=[phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2, r0**3*MU2*phi0/3]
V=solve_ivp(vac_rhs,[r0,RMAX],y0,dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.004)
sol=V.sol(rg); phibg=sol[0]; Jbg=sol[1]; phibg_p=Jbg*np.exp(2*phibg)/rg**2
em2=np.exp(-2*phibg)
def dirac_shoot(E,kappa,rmax_mode=rstar):
    l=-kappa if kappa<0 else kappa
    if kappa<0: G=r0**l; F=-(E*exp(2*phi0)/(2*l+1))*r0**(l+1)
    else: F=r0**l; G=(E*exp(2*phi0)/(2*l+1))*r0**(l+1)
    def rhs(r,y):
        ph=np.interp(r,rg,phibg); pp=np.interp(r,rg,phibg_p); e2l=exp(2*ph); g,f=y
        return [(pp-kappa/r)*g+E*e2l*f,(pp+kappa/r)*f-E*e2l*g]
    s=solve_ivp(rhs,[r0,rmax_mode],[G,F],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.006)
    ph=np.interp(rmax_mode,rg,phibg); pp=np.interp(rmax_mode,rg,phibg_p)
    g,f=s.y[0,-1],s.y[1,-1]
    resid=(pp-kappa/rmax_mode)*g+E*exp(2*ph)*f
    return resid,s
def find_E(kappa,Elo=0.2,Ehi=2.0,n=200):
    Es=np.linspace(Elo,Ehi,n); rs=[dirac_shoot(E,kappa)[0] for E in Es]
    for i in range(n-1):
        if rs[i]*rs[i+1]<0:
            a,b=Es[i],Es[i+1]
            for _ in range(60):
                m=0.5*(a+b); rm_=dirac_shoot(m,kappa)[0]
                if dirac_shoot(a,kappa)[0]*rm_<0: b=m
                else: a=m
            return 0.5*(a+b)
E1=find_E(-1)
_,smode=dirac_shoot(E1,-1)
rm=np.linspace(r0,rstar,3000); Gm=smode.sol(rm)[0]; Fm=smode.sol(rm)[1]

def solve_radial(source_l,l,screened):
    w=em2 if screened else np.ones_like(rg)
    N=NG; ab=np.zeros((3,N)); b=-source_l*rg**2*dr*dr
    rh=rg+dr/2; wh=np.interp(rh,rg,w); A=rh**2*wh
    for i in range(1,N-1):
        lo=A[i-1]; hi=A[i]
        diagc=-(lo+hi)-(l*(l+1)+(MU2*rg[i]**2 if screened else 0.0))*dr*dr
        ab[0,i+1]=hi; ab[1,i]=diagc; ab[2,i-1]=lo
    if l==0: ab[1,0]=-1.0; ab[0,1]=1.0; b[0]=0.0
    else: ab[1,0]=1.0; ab[0,1]=0.0; b[0]=0.0
    if screened: ab[1,N-1]=1.0; ab[2,N-2]=0.0; b[N-1]=0.0
    else: ab[1,N-1]=1.0+(l+1)*dr/rg[N-1]; ab[2,N-2]=-1.0; b[N-1]=0.0
    return solve_banded((1,1),ab,b)

def S_blob(s):
    s=np.clip(s,1e-9,None)
    ph=np.interp(np.clip(s,0,rstar),rg,phibg); G=np.interp(np.clip(s,0,rstar),rm,Gm); F=np.interp(np.clip(s,0,rstar),rm,Fm)
    val=(ALPHA/s**2)*(2*E1*np.exp(ph)*(G**2+F**2)-(2*(-1)/s)*np.exp(-ph)*G*F)
    return np.where(s<rstar,val,0.0)

import torch
torch.set_default_dtype(torch.float64); dev='cuda' if torch.cuda.is_available() else 'cpu'
LMAX=8
def real_Ylm_grid(theta,phi):
    from scipy.special import sph_harm
    Ys={}
    for l in range(LMAX+1):
        for m in range(-l,l+1):
            if m==0: Ys[(l,m)]=np.real(sph_harm(0,l,phi,theta))
            elif m>0: Ys[(l,m)]=np.sqrt(2)*(-1)**m*np.real(sph_harm(m,l,phi,theta))
            else: Ys[(l,m)]=np.sqrt(2)*(-1)**m*np.imag(sph_harm(-m,l,phi,theta))
    return Ys
NTH=48; NPH=96
xg,wth=leggauss(NTH); theta=np.arccos(xg)
phi=np.linspace(0,2*PI,NPH,endpoint=False); wph=2*PI/NPH
TH,PH=np.meshgrid(theta,phi,indexing='ij'); Wang=(wth[:,None]*wph*np.ones((1,NPH)))
Ys=real_Ylm_grid(TH.ravel(),PH.ravel())
TH_t=torch.tensor(TH.ravel(),device=dev); PH_t=torch.tensor(PH.ravel(),device=dev)
Wang_t=torch.tensor(Wang.ravel(),device=dev); Ys_t={k:torch.tensor(v,device=dev) for k,v in Ys.items()}
rg_t=torch.tensor(rg,device=dev)
sinTH=torch.sin(TH_t); cosTH=torch.cos(TH_t); cosPH=torch.cos(PH_t); sinPH=torch.sin(PH_t)
nx=sinTH*cosPH; ny=sinTH*sinPH; nz=cosTH

def project_density(b,weight_fn,nlump=3,charges=None):
    ang=np.array([0,2*PI/3,4*PI/3]); Rax=b*np.cos(ang); Ray=b*np.sin(ang)
    flm={k:torch.zeros(NG,device=dev) for k in Ys_t}
    r_t=rg_t; F=torch.zeros((NG,TH_t.shape[0]),device=dev)
    for a in range(nlump):
        ca=(charges[a] if charges is not None else 1.0)
        dotp=nx*Rax[a]+ny*Ray[a]
        s=torch.sqrt(torch.clamp(r_t[:,None]**2+b**2-2*r_t[:,None]*dotp[None,:],min=0.0))
        val=weight_fn(s.cpu().numpy())*ca
        F+=torch.tensor(val,device=dev)
    for (l,m),Y in Ys_t.items():
        flm[(l,m)]=(F*(Y*Wang_t)[None,:]).sum(dim=1)
    return flm

def US_of(b,nlump=3):
    S_lm=project_density(b,S_blob,nlump=nlump,charges=None)
    US=0.0
    for (l,m),sl in S_lm.items():
        sl_np=sl.cpu().numpy()
        if np.max(np.abs(sl_np))<1e-14: continue
        D=solve_radial(sl_np,l,screened=True)
        US+=0.5*np.trapezoid(sl_np*D*rg**2,rg)
    return US

# single lump self energy (nlump=1, b irrelevant)
U1=US_of(0.0,nlump=1)
print(f"U_self (single lump) = {U1:.6f}")
print(f"3*U_self = {3*U1:.6f}")
print(f"9*U_self = {9*U1:.6f}  (expected b=0 stacked, source 3x -> 9x energy)")
# now U_S at b=0 and large b
for b in [0.0,2.0,4.0,8.0,12.0,16.0,24.0]:
    print(f"b={b:5.1f}  U_S={US_of(b):.6f}  U_S/U1={US_of(b)/U1:.4f}")

print("\n--- LEAKAGE TEST: total source integral vs b ---")
def total_S(b,nlump=3):
    S_lm=project_density(b,S_blob,nlump=nlump,charges=None)
    # monopole l=0,m=0 integral: int S d3x = sqrt(4pi)*int S_00 r^2 dr
    s00=S_lm[(0,0)].cpu().numpy()
    return np.sqrt(4*PI)*np.trapezoid(s00*rg**2,rg)
def total_S_norm(b,nlump=3):
    return total_S(b,nlump)
S1=total_S(0.0,nlump=1)
print(f"single-lump total source int S d3x = {S1:.6f}")
for b in [0.0,2.0,4.0,8.0,12.0,16.0,24.0]:
    tot=total_S(b,nlump=3)
    print(f"b={b:5.1f}  total source(3 lumps)={tot:.6f}  vs 3*single={3*S1:.6f}  retained_frac={tot/(3*S1):.4f}")

print("\n--- TRUE INTERACTION = U(3 lumps,b) - 3*U_self ---")
print("If positive and decreasing -> genuine repulsion relieved. If it's just overlap, check vs naive overlap.")
for b in [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]:
    U3=US_of(b,nlump=3)
    Uint=U3-3*U1
    print(f"b={b:4.1f}  U3={U3:.6f}  U_int=U3-3Uself={Uint:.6f}")
print(f"\n3*U_self={3*U1:.6f}")
print("NOTE: in screened Yukawa, range 1/mu =",1/MU," but lump radius rstar=6.9875 >> 1/mu.")
print("So 'separation' by b<=4 < rstar barely moves the BULK of the source; field force range is tiny.")

print("\n--- OVERLAP-ARTIFACT TEST ---")
# A genuine field interaction between two screened sources of charge q at separation d ~ q^2 e^{-mu d}/(4pi d).
# For two lumps both of 'radius' rstar but screening 1/mu=0.98, the cross energy is the SELF-energy-like
# overlap. Compute pairwise: take 2 lumps, U2-2Uself, and see if the FALLOFF matches Yukawa e^{-mu b}/b
# (true field force) or a slow overlap geometry (lump still overlapping for b<2rstar).
def US_2(b):
    # two lumps at +b/2,-b/2 along x (use the 3-center machinery with nlump=2 won't be symmetric;
    # just place 2 of the 3 by zeroing the third via a custom projector)
    ang=np.array([0,PI]); Rax=(b/2)*np.cos(ang); Ray=(b/2)*np.sin(ang)
    flm={k:torch.zeros(NG,device=dev) for k in Ys_t}
    F=torch.zeros((NG,TH_t.shape[0]),device=dev)
    for a in range(2):
        dotp=nx*Rax[a]+ny*Ray[a]
        s=torch.sqrt(torch.clamp(rg_t[:,None]**2+(b/2)**2-2*rg_t[:,None]*dotp[None,:],min=0.0))
        F+=torch.tensor(S_blob(s.cpu().numpy()),device=dev)
    for (l,m),Y in Ys_t.items():
        flm[(l,m)]=(F*(Y*Wang_t)[None,:]).sum(dim=1)
    US=0.0
    for (l,m),sl in flm.items():
        sl_np=sl.cpu().numpy()
        if np.max(np.abs(sl_np))<1e-14: continue
        D=solve_radial(sl_np,l,screened=True)
        US+=0.5*np.trapezoid(sl_np*D*rg**2,rg)
    return US
print(f"2-lump separation = b (center-to-center)")
prev=None
for b in [2.0,4.0,6.0,8.0,10.0]:
    U2=US_2(b); Uint2=U2-2*U1
    yuk=np.exp(-MU*b)/b
    print(f"b={b:5.1f} U_int2={Uint2:.6e}  Yukawa e^-mu b/b={yuk:.6e}  ratio={Uint2/yuk:.3e}")

print("\n--- COULOMB channel: proton/neutron/like-charge dU_C ---")
def rho_blob(s):
    return np.where(s<rstar, np.interp(np.clip(s,0,rstar),rm,(Gm**2+Fm**2)/np.trapezoid(Gm**2+Fm**2,rm))/(4*PI*np.clip(s,1e-9,None)**2),0.0)
def UC_of(b,charges):
    rho_lm=project_density(b,rho_blob,nlump=3,charges=charges)
    UC=0.0
    for (l,m),rl in rho_lm.items():
        rl_np=rl.cpu().numpy()
        if np.max(np.abs(rl_np))<1e-14: continue
        A=solve_radial(rl_np,l,screened=False)
        UC+=0.5*np.trapezoid(rl_np*A*rg**2,rg)
    return UC
for name,Q in [("proton uud",[2/3,2/3,-1/3]),("neutron udd",[2/3,-1/3,-1/3]),("like uuu",[2/3,2/3,2/3])]:
    U0=UC_of(0.0,Q); U2=UC_of(2.0,Q); U4=UC_of(4.0,Q)
    print(f"{name:14s} UC(0)={U0:.6e} dU_C(2)={U2-U0:+.4e} dU_C(4)={U4-U0:+.4e}")
print("\ndU_S(b=2)=-0.0487 for comparison (dilaton). Coulomb is 1-2 orders smaller in all cases.")

print("\n--- SIGN CONVENTION of U_dilaton ---")
# Energy term: 0.5 * int S * D, with D solving (lap-mu2)D=-S (Yukawa convolution of S).
# For a localized source, D has the SAME sign as S (Yukawa kernel positive). So 0.5*S*D > 0 always.
# Check: is U_self > 0?  U_self=0.025997 > 0. YES positive.
print(f"U_self={U1:.6f} > 0 : so the dilaton field energy of a lump is POSITIVE (anti-binding).")
print("Energy DECREASING with b => the positive anti-binding cost is REDUCED by separation.")
print("Consistent with 'adding/overlapping fermion sources RAISES energy; separating relieves it.'")
print("Sign convention is self-consistent. But this is a POSITIVE-DEFINITE field self+overlap energy,")
print("NOT a binding well: it can only ever be relieved toward 0, never produce attraction. By")
print("construction 0.5*S*D>=0 can NEVER bind. The 'no attractive well' result is therefore")
print("GUARANTEED by the positive-definite quadratic form, not discovered.")

print("\n--- Is S_blob sign-definite? (decides whether 0.5 S D form is positive-definite) ---")
ss=np.linspace(0.01,rstar,400); Sv=S_blob(ss)
print(f"S_blob min={Sv.min():.4e} max={Sv.max():.4e} : sign-changes={np.any(Sv>0) and np.any(Sv<0)}")
print(f"S_blob at small r sign: {np.sign(Sv[0])}, at large r: {np.sign(Sv[-1])}")
# The energy 0.5<S, (lap-mu2)^{-1}(-S)> = 0.5 <S, K S> with K the positive Yukawa Green op.
# This is positive-definite REGARDLESS of S sign (K positive operator). So U>=0 always.
