#!/usr/bin/env python3
"""
dyn1_nodal_explore.py -- STEP A reconnaissance: phase-space structure of the
static radial cavity ODE, hunting for a NODAL family (interior nodes) -- the
discrete-candidate set #34/#39 explicitly skipped (they swept the NODELESS
branch only).

Radial sector of the metric's own field equation (Phi=1, r_in=1):
    phi'' + (2/r) phi' - 2 phi'^2 = Phi (1 - e^{3 phi})
  => phi'' = -(2/r) phi' + 2 phi'^2 + Phi(1 - e^{3 phi})

Inside-out matter cell: core depth phi(1)=D<0, regular core phi'(1)=0+.
Integrate OUTWARD and watch how many times phi crosses 0 before settling /
diverging. A NODAL solution = phi returns to (and crosses) 0 one or more
times in the interior, i.e. the BVP phi(1)=D, phi(R)=0 admits solutions with
n=1,2,... interior nodes at DISCRETE depths D_n (a discrete catalog label).

The fixed points of the source: 1-e^{3phi}=0 => phi=0 is the only zero.
Linearize about phi=0: phi'' + (2/r)phi' = -3 phi  (since d/dphi[1-e^{3phi}]
at 0 = -3) -> an OSCILLATOR with restoring const 3 -> nodes are POSSIBLE
about phi=0. About a deep negative D the source ~ +Phi (const push), no
restoring -> monotone region. So structure: deep monotone rise, then near
phi~0 it can OVERSHOOT and ring -> NODES. This script maps that.

DATA-BLIND. Log -> /tmp/dyn1.log.
"""
import numpy as np
import json, time

PHI = 1.0
R_IN = 1.0

def rhs(r, y):
    phi, phip = y
    arg = 3.0*phi
    arg = min(arg, 5.0)  # overshoot guard (transient phi>0 not physical)
    src = PHI*(1.0 - np.exp(arg))
    return np.array([phip, -(2.0/r)*phip + 2.0*phip**2 + src])

def integrate(D, phip0=1e-7, rmax=60.0, h0=1e-3, tol=1e-11):
    """Adaptive RK4 (step-doubling) outward. Record zero crossings of phi."""
    r = R_IN
    y = np.array([float(D), float(phip0)])
    h = h0
    crossings = []   # r values where phi crosses 0
    rs=[R_IN]; phis=[float(D)]
    n=0
    last_phi = y[0]
    while r < rmax and n < 2_000_000:
        big = rk4(r, y, h)
        m  = rk4(r, y, h/2)
        s  = rk4(r+h/2, m, h/2)
        err = np.sum(np.abs(s-big))
        scale = tol*(1+np.sum(np.abs(s)))
        if err>scale and h>1e-10:
            h *= max(0.2, 0.9*(scale/err)**0.2); continue
        r_new = r+h; y_new = s
        # detect sign change of phi
        if (last_phi<0 and y_new[0]>=0) or (last_phi>0 and y_new[0]<=0) or (last_phi==0):
            if abs(last_phi)>1e-12:
                frac = (0-last_phi)/(y_new[0]-last_phi)
                crossings.append(r+frac*h)
        last_phi=y_new[0]
        y=y_new; r=r_new; n+=1
        rs.append(r); phis.append(y[0])
        if abs(y[0])>50 or not np.isfinite(y[0]):
            return dict(D=D, crossings=crossings, blewup=True, rmax=r,
                        rs=np.array(rs), phis=np.array(phis))
        if err<scale/10: h=min(h*1.5, 0.05)
    return dict(D=D, crossings=crossings, blewup=False, rmax=r,
                rs=np.array(rs), phis=np.array(phis))

def rk4(r,y,h):
    k1=rhs(r,y); k2=rhs(r+h/2,y+h/2*k1); k3=rhs(r+h/2,y+h/2*k2); k4=rhs(r+h,y+h*k3)
    return y+(h/6)*(k1+2*k2+2*k3+k4)

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a); print(s,flush=True); fh.write(s+"\n"); fh.flush()
    t0=time.time()
    log("\n"+"="*72)
    log("dyn1_nodal_explore -- STEP A recon: node structure vs core depth D")
    log("="*72)
    log("ODE phi''=-(2/r)phi'+2phi'^2+(1-e^{3phi}); core phi(1)=D, phi'(1)=0+")
    log("Counting interior zero-crossings of phi as we shoot outward.\n")
    log(f"{'D':>10}{'n_cross':>9}{'first r*':>14}{'2nd cross':>14}{'blewup':>8}{'rmax':>10}")
    out=[]
    Ds=[-0.2,-0.4,-0.6,-0.8,-1.0,-1.5,-2.0,-3.0,-5.0,-7.0,-10.0]
    for D in Ds:
        res=integrate(D)
        cr=res['crossings']
        c1=cr[0] if len(cr)>=1 else None
        c2=cr[1] if len(cr)>=2 else None
        log(f"{D:>10.3f}{len(cr):>9}{(f'{c1:.5f}' if c1 else '--'):>14}"
            f"{(f'{c2:.5f}' if c2 else '--'):>14}{str(res['blewup']):>8}{res['rmax']:>10.3f}")
        out.append(dict(D=D, n_cross=len(cr),
                        crossings=[float(x) for x in cr], blewup=res['blewup'],
                        rmax=float(res['rmax'])))
    json.dump(out, open("/tmp/dyn1_nodal_explore.json","w"), indent=2)
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
