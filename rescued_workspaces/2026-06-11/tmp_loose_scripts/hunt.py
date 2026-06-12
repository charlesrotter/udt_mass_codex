import numpy as np
from scipy.integrate import solve_ivp

mu2 = np.pi/3; rstar = 6.9875
phi0 = -np.cos(np.pi/5)
me = 0.51099895   # MeV
C = 4*np.pi**2*me*rstar   # 140.96 MeV
def rhs(r,y):
    phi,J=y
    return [J*np.exp(2*phi)/r**2, r**2*mu2*phi]
r0=1e-6
sol=solve_ivp(rhs,[r0,rstar],[phi0,0.0],rtol=1e-11,atol=1e-13,dense_output=True,max_step=0.001)
phiE=sol.y[0,-1]; JE=sol.y[1,-1]
em2=np.exp(-2*phiE); emphi=np.exp(-phiE)
mMS=(rstar/2)*(1-em2)

# BH branch
phi0b=+np.cos(np.pi/5)
sb=solve_ivp(rhs,[r0,rstar],[phi0b,0.0],rtol=1e-11,atol=1e-13,
             events=[lambda r,y:y[0]-8.0],max_step=0.0005)
sb.t_events[0]
rc=sb.t_events[0][0]; mMS_bh=rc/2

print(f"C={C:.4f} MeV")
print(f"phiE={phiE:.5f}, em2={em2:.5f}, emphi={emphi:.5f}, mMS={mMS:.5f}, rc={rc:.5f}, mMS_bh={mMS_bh:.5f}")
print()

# Targets
TARG = {
  "m_p MeV": 938.272,
  "m_p/m_e": 1836.15267,
  "m_p/C": 938.272/C,
  "6pi^5": 6*np.pi**5,
}
for k,v in TARG.items(): print(f"target {k} = {v:.5f}")
print("m_p/C =", 938.272/C)
print()

# Build a dictionary of geometric primitives
prim = {
 "mMS": mMS, "|mMS|": abs(mMS), "em2": em2, "emphi": emphi,
 "rc": rc, "mMS_bh": mMS_bh, "rstar": rstar, "phiE": phiE, "|phiE|": abs(phiE),
 "JE": JE, "|JE|": abs(JE), "13/pi":13/np.pi, "pi":np.pi,
 "em2-1": em2-1, "rstar/2": rstar/2,
}

# search: which primitive (or simple combo) times a small rational/pi factor hits m_p/C=6.6562
target = 938.272/C   # 6.6562
print(f"=== hunting m_p/C = {target:.5f} (dimensionless, =m mode) ===")
factors = {
 "1":1, "pi":np.pi, "1/pi":1/np.pi, "2pi":2*np.pi, "pi/2":np.pi/2,
 "4pi^2":4*np.pi**2, "pi^2":np.pi**2, "2":2,"1/2":0.5,"3":3,"1/3":1/3,
 "pi^5":np.pi**5,"6pi^5":6*np.pi**5,
}
hits=[]
for pn,pv in prim.items():
    for fn,fv in factors.items():
        for tn,tv in [("m_p/C",938.272/C),("m_p/m_e",1836.15267),("m_p MeV via *C",938.272)]:
            val = pv*fv
            # compare to dimensionless target
            err = abs(val-tv)/abs(tv)
            if err < 0.01:
                hits.append((err, f"{pn}*{fn}={val:.5f} ~ {tn}={tv:.5f}", err))
hits.sort()
print(f"hits within 1% (prim*factor vs target):")
for e,s,_ in hits[:40]: print(f"  err={e*100:.3f}%  {s}")
