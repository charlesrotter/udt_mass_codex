# Full adversarial: copy the script's core, then extend scan to kappa=-3 and 2-angle (combined) mixing.
import numpy as np
from numpy import pi as PI, cos, exp, sqrt
from scipy.integrate import solve_ivp
from scipy.special import sph_harm
from numpy.polynomial.legendre import leggauss
from scipy.linalg import solve_banded
import warnings; warnings.filterwarnings("ignore")

phi0=-cos(PI/5); MU2=PI/3; MU=sqrt(MU2); rstar=6.9875; ALPHA=1/(4*PI); r0=1e-6
RMAX=16.0; NG=4000; rg=np.linspace(r0,RMAX,NG); dr=rg[1]-rg[0]
def vac_rhs(r,y): return [y[1]*exp(2*y[0])/r**2 if r>0 else 0.0, r**2*MU2*y[0]]
y0=[phi0+(MU2*phi0*exp(2*phi0)/6)*r0**2, r0**3*MU2*phi0/3]
V=solve_ivp(vac_rhs,[r0,RMAX],y0,dense_output=True,rtol=1e-12,atol=1e-14,max_step=0.004)
sol=V.sol(rg); phibg=sol[0]; phibg_p=sol[1]*np.exp(2*phibg)/rg**2

def shoot(E,kappa,rmax=rstar):
    L=-kappa if kappa<0 else kappa
    if kappa<0: G=r0**L; F=-(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    else:       F=r0**L; G=(E*exp(2*phi0)/(2*L+1))*r0**(L+1)
    def rhs(r,y):
        ph=np.interp(r,rg,phibg); pp=np.interp(r,rg,phibg_p); e2=exp(2*ph); g,f=y
        return [(pp-kappa/r)*g+E*e2*f,(pp+kappa/r)*f-E*e2*g]
    s=solve_ivp(rhs,[r0,rmax],[G,F],dense_output=True,rtol=1e-10,atol=1e-12,max_step=0.006)
    ph=np.interp(rmax,rg,phibg); pp=np.interp(rmax,rg,phibg_p); g,f=s.y[0,-1],s.y[1,-1]
    return (pp-kappa/rmax)*g+E*exp(2*ph)*f, s
def eigs(kappa,Elo=0.2,Ehi=12.0,n=400,want=2):
    Es=np.linspace(Elo,Ehi,n); rs=np.array([shoot(E,kappa)[0] for E in Es]); out=[]
    for i in range(n-1):
        if rs[i]*rs[i+1]<0:
            a,b=Es[i],Es[i+1]
            for _ in range(60):
                m=0.5*(a+b)
                if shoot(a,kappa)[0]*shoot(m,kappa)[0]<0: b=m
                else: a=m
            out.append(0.5*(a+b))
            if len(out)>=want: break
    return out
modes={}
for k in [-1,2,-3]:
    ev=eigs(k, want=(3 if k==-1 else 1))
    for n,E in enumerate(ev):
        _,s=shoot(E,k); rr=np.linspace(r0,rstar,3000)
        G=s.sol(rr)[0]; F=s.sol(rr)[1]
        nrm=np.trapezoid((G**2+F**2)*np.exp(np.interp(rr,rg,phibg)),rr)
        modes[(k,n)]=(E, rr, G/sqrt(nrm), F/sqrt(nrm))

NTH=60; NPH=120
xg,wth=leggauss(NTH); th=np.arccos(xg); ph=np.linspace(0,2*PI,NPH,endpoint=False); wph=2*PI/NPH
TH,PH=np.meshgrid(th,ph,indexing='ij'); W=(wth[:,None]*wph*np.ones((1,NPH)))
def Y(l,m): return sph_harm(m,l,PH,TH)
def lj(kappa):
    j=abs(kappa)-0.5; l=(-kappa-1) if kappa<0 else kappa; return l,j
def Omega(kappa,m):
    l,j=lj(kappa)
    if abs(m)>j: return None
    if kappa<0:
        up=sqrt((j+m)/(2*j))*Y(l,int(m-0.5)) if abs(m-0.5)<=l else 0*TH
        dn=sqrt((j-m)/(2*j))*Y(l,int(m+0.5)) if abs(m+0.5)<=l else 0*TH
    else:
        up=-sqrt((j-m+1)/(2*j+2))*Y(l,int(m-0.5)) if abs(m-0.5)<=l else 0*TH
        dn= sqrt((j+m+1)/(2*j+2))*Y(l,int(m+0.5)) if abs(m+0.5)<=l else 0*TH
    return up,dn

def solve_radial(src,l,screened):
    w=np.exp(-2*phibg) if screened else np.ones_like(rg); N=NG; ab=np.zeros((3,N)); b=-src*rg**2*dr*dr
    rh=rg+dr/2; wh=np.interp(rh,rg,w); A=rh**2*wh
    for i in range(1,N-1):
        lo=A[i-1]; hi=A[i]
        ab[0,i+1]=hi; ab[1,i]=-(lo+hi)-(l*(l+1)+(MU2*rg[i]**2 if screened else 0.0))*dr*dr; ab[2,i-1]=lo
    if l==0: ab[1,0]=-1.0; ab[0,1]=1.0
    else: ab[1,0]=1.0; ab[0,1]=0.0
    if screened: ab[1,N-1]=1.0; ab[2,N-2]=0.0
    else: ab[1,N-1]=1.0+(l+1)*dr/rg[N-1]; ab[2,N-2]=-1.0
    b[0]=0.0; b[N-1]=0.0
    return solve_banded((1,1),ab,b)

def chan(kn):
    E,rr,G,F=modes[kn]
    Gi=np.interp(rg,rr,G,right=0.0); Fi=np.interp(rg,rr,F,right=0.0)
    return E,Gi,Fi
E_m1,G_m1,F_m1=chan((-1,0))
E_p2,G_p2,F_p2=chan((2,0))
E_m3,G_m3,F_m3=chan((-3,0))
Qq=2/3
Y00=Y(0,0); Y20=Y(2,0)
def angint(O1,O2,YL):
    return np.real(np.sum(W*(np.conj(O1[0])*YL*O2[0]+np.conj(O1[1])*YL*O2[1])))

# === ATTACK 1: scan kappa=-3 mixing instead of +2 ===
Om_m1=Omega(-1,0.5); Om_m3=Omega(-3,0.5)
# lower components use Om_{-kappa}: -kappa=+1 for -1, +3 for -3
Om_p1=Omega(1,0.5); Om_p3=Omega(3,0.5)
def Etot_single(beta, Ed_state, Gd,Fd, Om_up,Om_dn_kappa, Om_up_lo,Om_dn_lo):
    cb,sb=cos(beta),np.sin(beta)
    r2=rg**2
    uu_c=angint(Om_m1,Om_up,Y20); uu_dd=angint(Om_up,Om_up,Y20)
    # lower (small comp) uses Om_{+1} and Om_{lo}
    ll_c=angint(Om_p1,Om_up_lo,Y20); ll_dd=angint(Om_up_lo,Om_up_lo,Y20)
    n0=(cb**2*(G_m1**2+F_m1**2)+sb**2*(Gd**2+Fd**2))/r2*angint(Om_m1,Om_m1,Y00)
    n2=(2*cb*sb*(G_m1*Gd*uu_c+F_m1*Fd*ll_c)+sb**2*(Gd**2*uu_dd+Fd**2*ll_dd))/r2
    eps=cb**2*E_m1+sb**2*Ed_state; eph=np.exp(phibg)
    S0=(ALPHA*2*eps*eph/r2)*(cb**2*(G_m1**2+F_m1**2)+sb**2*(Gd**2+Fd**2))*angint(Om_m1,Om_m1,Y00)
    S2=(ALPHA*2*eps*eph/r2)*(2*cb*sb*(G_m1*Gd*uu_c+F_m1*Fd*ll_c)+sb**2*(Gd**2*uu_dd+Fd**2*ll_dd))
    kin=3*(cb**2*E_m1+sb**2*Ed_state)
    Ed=0.0
    for l,Sl in [(0,S0),(2,S2)]:
        if np.max(np.abs(Sl))<1e-15: continue
        D=solve_radial(Sl,l,True); Ed+=9*0.5*np.trapezoid(Sl*D*r2,rg)
    Ec=0.0
    for l,nl in [(0,n0),(2,n2)]:
        rho=Qq*nl
        if np.max(np.abs(rho))<1e-15: continue
        A=solve_radial(rho,l,False); Ec+=9*0.5*np.trapezoid(rho*A*r2,rg)
    return kin+Ed+Ec, kin, Ed, Ec

print("=== ATTACK: kappa=-3 mixing scan (gap=%.3f) ==="%(E_m3-E_m1))
print(f"{'beta':>6}{'tot':>12}{'kin':>12}{'Ed':>12}{'Ec':>12}")
for beta in [0.0,0.05,0.1,0.2,0.3]:
    t,k,ed,ec=Etot_single(beta,E_m3,G_m3,F_m3,Om_m3,None,Om_p3,None)
    print(f"{beta:6.2f}{t:12.5f}{k:12.5f}{ed:12.5f}{ec:12.5f}")

print("\n=== ATTACK 2: SIGN of field-energy curvature (does field favor deformation?) ===")
# Isolate field energy as function of beta for the +2 channel, fine grid near 0, fit curvature.
import numpy as np
def fields_only(beta):
    cb,sb=cos(beta),np.sin(beta); r2=rg**2
    uu_c=angint(Om_m1,Omega(2,0.5),Y20); uu_dd=angint(Omega(2,0.5),Omega(2,0.5),Y20)
    Om_p1=Omega(1,0.5); Om_m2=Omega(-2,0.5)
    ll_c=angint(Om_p1,Om_m2,Y20); ll_dd=angint(Om_m2,Om_m2,Y20)
    n0=(cb**2*(G_m1**2+F_m1**2)+sb**2*(G_p2**2+F_p2**2))/r2*angint(Om_m1,Om_m1,Y00)
    n2=(2*cb*sb*(G_m1*G_p2*uu_c+F_m1*F_p2*ll_c)+sb**2*(G_p2**2*uu_dd+F_p2**2*ll_dd))/r2
    eps=cb**2*E_m1+sb**2*E_p2; eph=np.exp(phibg)
    S0=(ALPHA*2*eps*eph/r2)*(cb**2*(G_m1**2+F_m1**2)+sb**2*(G_p2**2+F_p2**2))*angint(Om_m1,Om_m1,Y00)
    S2=(ALPHA*2*eps*eph/r2)*(2*cb*sb*(G_m1*G_p2*uu_c+F_m1*F_p2*ll_c)+sb**2*(G_p2**2*uu_dd+F_p2**2*ll_dd))
    Ed=0.0; Ed0=0.0; Ed2=0.0
    for l,Sl in [(0,S0),(2,S2)]:
        if np.max(np.abs(Sl))<1e-15: continue
        D=solve_radial(Sl,l,True); e=9*0.5*np.trapezoid(Sl*D*r2,rg); Ed+=e
        if l==0: Ed0=e
        else: Ed2=e
    Ec=0.0; Ec0=0.0; Ec2=0.0
    for l,nl in [(0,n0),(2,n2)]:
        rho=Qq*nl
        if np.max(np.abs(rho))<1e-15: continue
        A=solve_radial(rho,l,False); e=9*0.5*np.trapezoid(rho*A*r2,rg); Ec+=e
        if l==0: Ec0=e
        else: Ec2=e
    return Ed,Ec,Ed0,Ed2,Ec0,Ec2

print(f"{'beta':>6}{'Ed_tot':>12}{'Ec_tot':>12}{'Ed_l2':>12}{'Ec_l2':>12}")
betas=[0.0,0.02,0.04,0.06,0.08,0.10]
vals=[]
for b in betas:
    Ed,Ec,Ed0,Ed2,Ec0,Ec2=fields_only(b)
    vals.append((b,Ed,Ec,Ed2,Ec2))
    print(f"{b:6.2f}{Ed:12.6f}{Ec:12.6f}{Ed2:12.4e}{Ec2:12.4e}")

# numerical curvature of total FIELD energy (Ed+Ec) at beta=0
bs=np.array([v[0] for v in vals]); Ef=np.array([v[1]+v[2] for v in vals])
# central 2nd deriv using b=0,0.02,0.04 (forward) and a parabola fit
c=np.polyfit(bs,Ef,2)
print("\nfield-energy parabola fit E_field ~ %.4e*b^2 + %.4e*b + %.6f"%(c[0],c[1],c[2]))
print("=> field curvature d2E_field/db2 ~", 2*c[0], "(POSITIVE => field also opposes deformation)" if 2*c[0]>0 else "(NEGATIVE => field FAVORS deformation!)")
print("kinetic curvature 6*gap(+2) =", 6*(E_p2-E_m1))
print("\nRATIO |field curvature| / kinetic curvature =", abs(2*c[0])/(6*(E_p2-E_m1)))

print("\n=== ATTACK 3: how large would Qq (or coupling) need to be to flip it? ===")
# Coulomb field energy scales as Qq^2. Its l2 part at small beta ~ linear-ish; find threshold.
# E_total curvature = 6*gap + d2(Ed)/db2 + Qq_factor*d2(Ec)/db2.  Currently Ec uses Qq=2/3.
# Ec curvature scales with Qq^2. Solve 6*gap + cd*?? ... just brute: scale Ec by factor s=Qq_new^2/Qq^2
Ed_arr=np.array([v[1] for v in vals]); Ec_arr=np.array([v[2] for v in vals])
cd=np.polyfit(bs,Ed_arr,2)[0]*2; ce=np.polyfit(bs,Ec_arr,2)[0]*2
print("d2Ed/db2=",cd," d2Ec/db2=",ce," (both should be the opposing/help terms)")
# total curvature = 6*gap + cd + ce*s ; for flip need <0 -> s > (6*gap+cd)/(-ce) if ce<0
if ce<0:
    s=(6*(E_p2-E_m1)+cd)/(-ce); print("Coulomb favors deformation; charge-scale factor to flip =",s,"=> Qq=",Qq*np.sqrt(s))
else:
    print("Coulomb curvature POSITIVE => even infinite charge cannot flip via this term")

print("\n=== ATTACK 4: combined (+2 AND -3) two-angle mixing ===")
# psi_up = c0*Om_m1 + a*Om_p2 + b*Om_m3 (normalized). Scan a,b.
def Etot_combined(a,b):
    c0=sqrt(max(0.0,1-a*a-b*b))
    r2=rg**2
    Om2=Omega(2,0.5); Om3=Omega(-3,0.5); Omp1=Omega(1,0.5); Omm2=Omega(-2,0.5); Omp3=Omega(3,0.5)
    # density n0 (diagonal, ortho channels)
    n0=(c0**2*(G_m1**2+F_m1**2)+a**2*(G_p2**2+F_p2**2)+b**2*(G_m3**2+F_m3**2))/r2*angint(Om_m1,Om_m1,Y00)
    # n2: all cross + diagonal upper; lower analog
    def uc(Oa,Ga,Fa,Ob,Gb,Fb,OalLo,OblLo):
        return (Ga*Gb*angint(Oa,Ob,Y20)+Fa*Fb*angint(OalLo,OblLo,Y20))
    n2=( 2*c0*a*uc(Om_m1,G_m1,F_m1,Om2,G_p2,F_p2,Omp1,Omm2)
        +2*c0*b*uc(Om_m1,G_m1,F_m1,Om3,G_m3,F_m3,Omp1,Omp3)
        +2*a*b*uc(Om2,G_p2,F_p2,Om3,G_m3,F_m3,Omm2,Omp3)
        +a**2*(G_p2**2*angint(Om2,Om2,Y20)+F_p2**2*angint(Omm2,Omm2,Y20))
        +b**2*(G_m3**2*angint(Om3,Om3,Y20)+F_m3**2*angint(Omp3,Omp3,Y20)) )/r2
    eps=c0**2*E_m1+a**2*E_p2+b**2*E_m3; eph=np.exp(phibg)
    S0=(ALPHA*2*eps*eph)*n0  # n0 already has the density form incl angint; reuse structure
    S2=(ALPHA*2*eps*eph)*n2
    kin=3*(c0**2*E_m1+a**2*E_p2+b**2*E_m3)
    Ed=0.0
    for l,Sl in [(0,S0),(2,S2)]:
        if np.max(np.abs(Sl))<1e-15: continue
        D=solve_radial(Sl,l,True); Ed+=9*0.5*np.trapezoid(Sl*D*r2,rg)
    Ec=0.0
    for l,nl in [(0,n0),(2,n2)]:
        rho=Qq*nl
        if np.max(np.abs(rho))<1e-15: continue
        A=solve_radial(rho,l,False); Ec+=9*0.5*np.trapezoid(rho*A*r2,rg)
    return kin+Ed+Ec
print("scanning a,b in [0,0.3]; looking for any (a,b) with E < E(0,0)")
E00=Etot_combined(0,0); best=(0,0,E00)
for a in np.linspace(0,0.3,7):
    for b in np.linspace(0,0.3,7):
        if a==0 and b==0: continue
        E=Etot_combined(a,b)
        if E<best[2]: best=(a,b,E)
print("E(0,0)=",E00,"  min found=",best, " (lower than baseline?" , best[2]<E00, ")")

print("\n=== ATTACK 5: n>1 radial excitation of kappa=-1 (gap to 5.5643) ===")
print("kappa=-1 n=1 eigenvalue=",modes[(-1,1)][0]," gap=",modes[(-1,1)][0]-E_m1," -> even larger kinetic cost")
