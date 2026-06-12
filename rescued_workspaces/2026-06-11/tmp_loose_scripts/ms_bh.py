import numpy as np
from scipy.integrate import solve_ivp

mu2 = np.pi/3
rstar = 6.9875
phi0_bh = +np.cos(np.pi/5)   # mirror BH branch

def rhs(r, y):
    phi, J = y
    dphi = J*np.exp(2*phi)/r**2
    dJ = r**2*mu2*phi
    return [dphi, dJ]

# event: phi blows up -> stop when phi crosses say 6 (e^{phi} large)
def blow(r,y):
    return y[0] - 8.0
blow.terminal = True
blow.direction = 1

r0 = 1e-6
y0 = [phi0_bh, 0.0]
sol = solve_ivp(rhs, [r0, rstar], y0, rtol=1e-11, atol=1e-13, events=blow, max_step=0.0005)
print("phi0_bh =", phi0_bh)
print("status / t_events:", sol.t_events)
if len(sol.t_events[0])>0:
    rc = sol.t_events[0][0]
    print("horizon r_c (phi=8) =", rc)
    # Misner-Sharp at horizon: m_MS = (r/2)(1 - e^{-2phi}) -> e^{-2phi}->0 so m_MS -> r_c/2
    print("m_MS at horizon ~ r_c/2 =", rc/2)
else:
    print("phi(r*) =", sol.y[0,-1])

# Refine: find where e^{-2phi} -> 0, i.e. true horizon. Try larger threshold
for thr in [6,8,10,15,20]:
    def blow2(r,y,thr=thr):
        return y[0]-thr
    blow2.terminal=True; blow2.direction=1
    s=solve_ivp(rhs,[r0,rstar],y0,rtol=1e-11,atol=1e-13,events=blow2,max_step=0.0005)
    if len(s.t_events[0])>0:
        print(f"  phi={thr}: r_c={s.t_events[0][0]:.5f}, r_c/2={s.t_events[0][0]/2:.5f}")
