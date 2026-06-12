import numpy as np
from scipy.integrate import solve_ivp
mu2=np.pi/3; rstar=6.9875; phi0=-np.cos(np.pi/5)
me=0.51099895; C=4*np.pi**2*me*rstar
def rhs(r,y):
    phi,J=y; return [J*np.exp(2*phi)/r**2, r**2*mu2*phi]
sol=solve_ivp(rhs,[1e-6,rstar],[phi0,0.0],rtol=1e-11,atol=1e-13,dense_output=True,max_step=0.001)
phiE=sol.y[0,-1]; JE=sol.y[1,-1]; em2=np.exp(-2*phiE); mMS=(rstar/2)*(1-em2)
# BH branch m_MS
sb=solve_ivp(rhs,[1e-6,rstar],[+np.cos(np.pi/5),0.0],rtol=1e-11,atol=1e-13,
             events=[lambda r,y:y[0]-8.0],max_step=0.0005)
rc=sb.t_events[0][0]; mMS_bh=rc/2

print("=== (a) DEFICIT / binding reading ===")
# m_MS at r* (hadron, -80.33) vs BH branch (+0.378). Difference:
print("mMS_hadron - mMS_bh =", mMS - mMS_bh, " *C=",(mMS-mMS_bh)*C)
print("|mMS_hadron| - mMS_bh =", abs(mMS)-mMS_bh)
print("|mMS| + mMS_bh =", abs(mMS)+mMS_bh)
# m_MS along the radius: is m_p a difference m_MS(r*)-m_MS(r1)?
# scan m_MS(r) for the hadron branch
rs=np.linspace(0.5,rstar,400)
mvals=[]
for r in rs:
    s=solve_ivp(rhs,[1e-6,r],[phi0,0.0],rtol=1e-9,atol=1e-11,max_step=0.005)
    e2=np.exp(-2*s.y[0,-1]); mvals.append((r/2)*(1-e2))
mvals=np.array(mvals)
# any pair (r_i,r_j) with m_MS diff -> 938/C=6.656 or 80.33-something
target=938.272/C
diffs=mMS - mvals  # deficit from full
# does any single m_MS(r) equal -6.656?  or |diff|=6.656?
idx=np.argmin(np.abs(np.abs(mvals)-target))
print(f"closest |m_MS(r)|={abs(mvals[idx]):.4f} at r={rs[idx]:.3f} vs target {target:.4f}")
idx2=np.argmin(np.abs(np.abs(diffs)-target))
print(f"closest |m_MS(r*)-m_MS(r)|={abs(diffs[idx2]):.4f} at r={rs[idx2]:.3f} vs {target:.4f}")

print("\n=== (b) dual-BH 0.3777 nat in natural unit -> 938/1836/6.656 ===")
for fn,fv in {"*C":C,"*4pi^2":4*np.pi**2,"/me*?":1}.items():
    print(f"  mMS_bh {fn} =", mMS_bh*fv)
print("  938.272/0.3777 =",938.272/mMS_bh, " (factor needed)")
print("  6.65621/0.3777 =",6.65621/mMS_bh, "  1836.15/0.3777=",1836.15/mMS_bh)

print("\n=== (e) lapse as mass factor ===")
lap=np.exp(-phiE)  # 4.898
print("  lapse=",lap," lapse*C=",lap*C," 6.656/lapse=",6.65621/lap," 1836/lapse=",1836.15/lap)
print("  em2=24, 1836.15/24=",1836.15/24," 6.656/24=",6.65621/24)
print("  em2/4 - 13/pi? :", em2/4, 13/np.pi)
