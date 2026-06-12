import numpy as np
from scipy.integrate import cumulative_trapezoid
MU_G=0.2472981283; R_CMB=9.164114; COS5=np.cos(np.pi/5.0)
DL_IN=297.0; ELL_OFF=243.0
def phi0_f(r):
    x=MU_G*r; return 1.5*x-COS5*x**2+(2.0/3.0)*x**3
def phi0p_f(r):
    x=MU_G*r; return MU_G*(1.5-2.0*COS5*x+2.0*x**2)
PHI_C=phi0_f(R_CMB)
def make_fields(nfine=6000,rmin=1e-3):
    r=np.linspace(rmin,R_CMB,nfine); ph=phi0_f(r); php=phi0p_f(r); f=np.exp(-2.0*ph)
    dphi=phi0_f(r)/PHI_C
    H1E=np.exp(2*ph)*cumulative_trapezoid(2.0*dphi,r,initial=0.0)
    H1N=2.0*dphi/(f*php)
    WEE_E=(np.exp(2*ph)/r**2)*H1E*np.exp(-3*ph)
    WEE_N=(np.exp(2*ph)/r**2)*H1N*np.exp(-3*ph)
    WTT=r**2*np.exp(-3*ph)
    return dict(r=r,S=dphi,WEE_E=WEE_E,WEE_N=WEE_N,WTT=WTT)
def run_pass(N=260,kappa=1.0,rmin=1e-3,envpow=1.0,nfine=6000,ells=None,ell_off=ELL_OFF):
    if ells is None: ells=np.arange(100.0,2001.0,5.0)
    F=make_fields(nfine,rmin)
    rg=np.linspace(rmin,R_CMB,N); h=rg[1]-rg[0]
    S=np.interp(rg,F['r'],F['S'])**envpow; S=S/S.max()
    sqrtS=np.sqrt(np.clip(S,0.0,None))
    Vb={k:np.interp(rg,F['r'],F[k])*sqrtS for k in ('WTT','WEE_E','WEE_N')}
    R1,R2=np.meshgrid(rg,rg,indexing='ij'); DR2=(R1-R2)**2
    comb_tag={'WTT':'cos2','WEE_E':'sin2','WEE_N':'sin2'}
    out={k:np.empty(len(ells)) for k in Vb}; outc={k:np.empty(len(ells)) for k in Vb}
    for i,l in enumerate(ells):
        Lc=kappa*R_CMB/l
        Kern=np.exp(-DR2/(2.0*Lc*Lc))
        chi=np.pi*(l*(R_CMB/rg)-ell_off)/DL_IN
        kr=2.0*np.pi*l*R_CMB/(DL_IN*rg**2)
        damp=np.exp(-0.5*(kr*h/2.0)**2)
        cos2=0.5+(np.cos(chi)**2-0.5)*damp
        sin2=0.5+(np.sin(chi)**2-0.5)*damp
        for k,V in Vb.items():
            out[k][i]=V@Kern@V*h*h
            M=cos2 if comb_tag[k]=='cos2' else sin2
            Vc=V*np.sqrt(M)
            outc[k][i]=Vc@Kern@Vc*h*h
    return dict(ells=ells,smooth=out,comb=outc)
def comb_peaks(ells,Q,lo=330.0,hi=1950.0):
    step=ells[1]-ells[0]; pk=[]
    for i in range(1,len(ells)-1):
        if lo<=ells[i]<=hi and Q[i]>Q[i-1] and Q[i]>=Q[i+1]:
            den=Q[i-1]-2*Q[i]+Q[i+1]
            d=0.5*(Q[i-1]-Q[i+1])/den if den!=0 else 0.0
            pk.append(ells[i]+d*step)
    return np.array(pk)
def match_shift(pA,pB,tol=80.0):
    sh=[]
    for p in pA:
        if len(pB)==0: continue
        j=int(np.argmin(np.abs(pB-p)))
        if abs(pB[j]-p)<=tol: sh.append(pB[j]-p)
    return np.array(sh)
def shifts(P):
    ells=P['ells']
    Q={k:P['comb'][k]/P['smooth'][k] for k in ('WEE_E','WEE_N')}
    pkE=comb_peaks(ells,Q['WEE_E']); pkN=comb_peaks(ells,Q['WEE_N'])
    return match_shift(pkE,pkN)

# phase-anchor scan: 17 anchors over one full spacing
print("PHASE-ANCHOR SCAN (17 anchors):")
means=[]; allneg=True
for j in range(17):
    off=ELL_OFF+j*DL_IN/17.0
    sh=shifts(run_pass(ell_off=off))
    means.append(np.mean(sh)); allneg &= np.all(sh<0)
    print(f"  off={off:8.2f}  n={len(sh)}  mean signed shift={np.mean(sh):+.3f}  all<0: {np.all(sh<0)}")
print(f"  range of mean signed shift: [{min(means):+.3f}, {max(means):+.3f}]  all matched peaks negative: {allneg}")

# coherence / Limber proxies
for kap in (1.0,0.5,0.25,0.125,0.0625):
    sh=shifts(run_pass(kappa=kap))
    print(f"kappa={kap:7.4f}  mean signed shift={np.mean(sh):+.3f}  n={len(sh)}  all<0: {np.all(sh<0)}")

# true Limber / short-coherence (incoherent diagonal) limit:
# C_ell ~ sum_r V(r)^2 * M(r) (intensity-weighted local modulation)
def limber_pass(N=260,rmin=1e-3,envpow=1.0,nfine=6000,ells=None,ell_off=ELL_OFF,damped=True):
    if ells is None: ells=np.arange(100.0,2001.0,5.0)
    F=make_fields(nfine,rmin)
    rg=np.linspace(rmin,R_CMB,N); h=rg[1]-rg[0]
    S=np.interp(rg,F['r'],F['S'])**envpow; S=S/S.max()
    sqrtS=np.sqrt(np.clip(S,0.0,None))
    Vb={k:np.interp(rg,F['r'],F[k])*sqrtS for k in ('WEE_E','WEE_N')}
    out={k:np.empty(len(ells)) for k in Vb}; outc={k:np.empty(len(ells)) for k in Vb}
    for i,l in enumerate(ells):
        chi=np.pi*(l*(R_CMB/rg)-ell_off)/DL_IN
        kr=2.0*np.pi*l*R_CMB/(DL_IN*rg**2)
        damp=np.exp(-0.5*(kr*h/2.0)**2) if damped else 1.0
        sin2=0.5+(np.sin(chi)**2-0.5)*damp
        for k,V in Vb.items():
            out[k][i]=np.sum(V*V)*h
            outc[k][i]=np.sum(V*V*sin2)*h
    return dict(ells=ells,smooth=out,comb=outc)
for N in (260,520):
    P=limber_pass(N=N)
    sh=shifts(P)
    print(f"LIMBER N={N}: mean signed shift={np.mean(sh):+.3f} n={len(sh)} all<0: {np.all(sh<0)} shifts={np.round(sh,2)}")
P=limber_pass(envpow=2.0)
sh=shifts(P); print(f"LIMBER envpow=2: mean={np.mean(sh):+.3f} all<0: {np.all(sh<0)}")

# Limber WITHOUT anti-alias relaxation, fine ell grid
els=np.arange(100.0,2001.0,1.0)
for N,d in ((1040,False),(2080,False)):
    P=limber_pass(N=N,ells=els,damped=d)
    Q={k:P['comb'][k]/P['smooth'][k] for k in ('WEE_E','WEE_N')}
    pkE=comb_peaks(els,Q['WEE_E']); pkN=comb_peaks(els,Q['WEE_N'])
    sh=match_shift(pkE,pkN)
    print(f"LIMBER undamped N={N}: mean={np.mean(sh):+.3f} n={len(sh)} all<0: {np.all(sh<0)}")
    print("  pkE:",np.round(pkE,1)); print("  pkN:",np.round(pkN,1))
