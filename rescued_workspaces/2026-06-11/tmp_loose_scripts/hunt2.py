import numpy as np, itertools
from scipy.integrate import solve_ivp
mu2=np.pi/3; rstar=6.9875; phi0=-np.cos(np.pi/5)
me=0.51099895; C=4*np.pi**2*me*rstar
def rhs(r,y):
    phi,J=y; return [J*np.exp(2*phi)/r**2, r**2*mu2*phi]
r0=1e-6
sol=solve_ivp(rhs,[r0,rstar],[phi0,0.0],rtol=1e-11,atol=1e-13,dense_output=True,max_step=0.001)
phiE=sol.y[0,-1]; JE=sol.y[1,-1]
em2=np.exp(-2*phiE); emphi=np.exp(-phiE); mMS=(rstar/2)*(1-em2)
sb=solve_ivp(rhs,[r0,rstar],[+np.cos(np.pi/5),0.0],rtol=1e-11,atol=1e-13,
             events=[lambda r,y:y[0]-8.0],max_step=0.0005)
rc=sb.t_events[0][0]; mMS_bh=rc/2

prim={"mMS":mMS,"|mMS|":abs(mMS),"em2":em2,"emphi":emphi,"rc":rc,"mMS_bh":mMS_bh,
 "rstar":rstar,"|phiE|":abs(phiE),"|JE|":abs(JE),"13/pi":13/np.pi,"rstar/2":rstar/2,
 "em2-1":em2-1,"em2+1":em2+1,"1":1.0}

targets={"m_p/C":938.272/C,"m_p/m_e":1836.15267,"m_p MeV":938.272,"6.6562":6.65621}
factors={"1":1,"pi":np.pi,"1/pi":1/np.pi,"2pi":2*np.pi,"pi/2":np.pi/2,"4pi^2":4*np.pi**2,
 "pi^2":np.pi**2,"2":2,"1/2":.5,"3":3,"1/3":1/3,"4":4,"6":6,"1/6":1/6,"sqrt":None}

names=list(prim); 
hits=[]
# ratios and products of two primitives, times a factor, vs dimensionless targets (m_p/C and m_p/m_e)
dtargs={"m_p/C":938.272/C,"m_p/m_e":1836.15267}
for a,b in itertools.product(names,names):
    pa,pb=prim[a],prim[b]
    combos={f"{a}*{b}":pa*pb, f"{a}/{b}":pa/pb if pb!=0 else np.nan,
            f"{a}-{b}":pa-pb, f"{a}+{b}":pa+pb}
    for cn,cv in combos.items():
        if not np.isfinite(cv) or cv<=0: continue
        for fn,fv in factors.items():
            if fv is None: continue
            val=cv*fv
            for tn,tv in dtargs.items():
                err=abs(val-tv)/tv
                if err<0.005:
                    hits.append((err,f"({cn})*{fn}={val:.5f} ~ {tn}={tv:.5f}"))
hits.sort()
seen=set();out=[]
for e,s in hits:
    key=s.split("=")[0]
    if key in seen: continue
    seen.add(key); out.append((e,s))
print("Two-primitive hits within 0.5% (dimensionless targets):")
for e,s in out[:50]: print(f"  err={e*100:.3f}%  {s}")
if not out: print("  NONE")

print()
print("=== Machian c^2=2GM/r* => M=r*/2 in nat; convert? ===")
print("r*/2 =",rstar/2, "  *C =",(rstar/2)*C, "MeV   /(target m_p)=",(rstar/2)*C/938.272)
print("r*/2 in m_e:", (rstar/2)*4*np.pi**2, " vs 1836.15")
