#!/usr/bin/env python3
"""
dyn1_regular_seal.py -- STEP A part 4: is there a DISCRETE set of core
depths D_n giving a REGULAR (mirror-fold) seal at the n-th node?

A genuine smoothly-sealed cavity (W6 mirror fold, finite-cell canon) needs
phi=0 AND phi'=0 at the seal R. Part 3 showed generic crossings keep
phi'!=0. Here we ask the sharper catalog question: define
    g_n(D) = phi'(R_{n+1}(D))   [slope at the (n+1)-th zero, i.e. the n-node seal]
and search for ROOTS g_n(D)=0. A discrete set of roots {D_n} = a discrete
nodal catalog of regularly-sealed cavities. NO roots (g_n never vanishes) =>
no regular nodal seal => the nodal family is NOT a discrete sealed catalog.

We scan D finely across the whole oscillatory regime and the deep regime and
tabulate g_0(D), g_1(D), g_2(D). We also locate the SEPARATRIX D* between
the oscillatory (bounded) and the monotone-then-blowup regime, which is the
one special depth the dynamics singles out.

Also: build the clean n=0 NODELESS cavity family and its Misner-Sharp mass
m(p) = (R/2)(1-e^{-2*phi}) read at the core, vs depth p, to have the
ground-state mass curve for the ratio table.

DATA-BLIND. Log -> /tmp/dyn1.log
"""
import numpy as np, json, time
PHI=1.0; R_IN=1.0
def rhs(r,y):
    phi,phip=y; arg=min(3.0*phi,5.0)
    return np.array([phip,-(2.0/r)*phip+2.0*phip**2+PHI*(1.0-np.exp(arg))])
def rk4(r,y,h):
    k1=rhs(r,y);k2=rhs(r+h/2,y+h/2*k1);k3=rhs(r+h/2,y+h/2*k2);k4=rhs(r+h,y+h*k3)
    return y+(h/6)*(k1+2*k2+2*k3+k4)
def shoot(D,rmax=40.0,tol=1e-13,phip0=1e-7,nmax=4):
    r=R_IN;y=np.array([float(D),phip0]);h=5e-4;crossings=[];last=y[0];n=0
    while r<rmax and n<3_000_000 and len(crossings)<nmax:
        big=rk4(r,y,h);m=rk4(r,y,h/2);s=rk4(r+h/2,m,h/2)
        err=np.sum(np.abs(s-big));scale=tol*(1+np.sum(np.abs(s)))
        if err>scale and h>1e-12:h*=max(0.2,0.9*(scale/err)**0.2);continue
        ynew=s;rnew=r+h
        if last<0 and ynew[0]>=0 or last>0 and ynew[0]<=0:
            if abs(last)>1e-12:
                frac=(0-last)/(ynew[0]-last)
                # interpolate slope at crossing
                pk=last_v+frac*(ynew[1]-last_v) if False else ynew[1]
                crossings.append((r+frac*h, ynew[1]))
        last=ynew[0];last_v=y[1];y=ynew;r=rnew;n+=1
        if abs(y[0])>50 or not np.isfinite(y[0]):
            return crossings,True
        if err<scale/10:h=min(h*1.5,0.02)
    return crossings,False

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72);log("dyn1_regular_seal -- STEP A part 4: regular-seal roots g_n(D)=0?");log("="*72)
    log("g_n(D)=phi' at the (n+1)-th zero. Root => regular mirror-fold seal.\n")

    # fine D scan
    Ds=np.round(np.arange(-0.75,-0.05,0.01),3)
    g0=[];g1=[];g2=[];blewD=None
    log(f"{'D':>8}{'g0=phip@R1':>14}{'g1=phip@R2':>14}{'g2=phip@R3':>14}{'blew':>7}")
    for D in Ds:
        cr,blew=shoot(D)
        vg=[cr[k][1] if len(cr)>k else np.nan for k in range(3)]
        g0.append(vg[0]);g1.append(vg[1]);g2.append(vg[2])
        if blew and blewD is None: blewD=D
        if abs(D*100)%5==0:
            log(f"{D:>8.3f}{vg[0]:>14.5e}{vg[1]:>14.5e}{vg[2]:>14.5e}{str(blew):>7}")
    g0=np.array(g0);g1=np.array(g1);g2=np.array(g2)
    def sign_changes(g,Ds):
        sc=[]
        for i in range(len(g)-1):
            if np.isfinite(g[i]) and np.isfinite(g[i+1]) and g[i]*g[i+1]<0:
                sc.append((Ds[i],Ds[i+1]))
        return sc
    log("\nROOT SEARCH (sign changes of g_n over the scanned D range):")
    for name,g in [("g0",g0),("g1",g1),("g2",g2)]:
        sc=sign_changes(g,Ds)
        log(f"  {name}: {'NO ROOT (slope never 0 at seal)' if not sc else f'roots near {sc}'}")
        log(f"        range g over D: [{np.nanmin(g):.4e}, {np.nanmax(g):.4e}]")

    log(f"\nSEPARATRIX (oscillatory<->monotone-blowup) first blows up near D*={blewD}")

    # nodeless n=0 cavity mass curve m(p): seal at first crossing r*(p).
    log("\n"+"-"*60)
    log("n=0 NODELESS cavity family: r*(p) and MS mass content vs depth p")
    log("MS at core m=(1/2)(1-e^{-2p}) (c=G=1, areal r_core=1); |m| = depth content")
    log(f"{'p':>8}{'r*':>12}{'|m_core|':>14}{'ratio m/m(-0.8)':>18}")
    ps=[-0.8,-1.0,-1.5,-2.0,-3.0,-5.0,-7.0,-10.0,-15.0]
    base=None;rows=[]
    for p in ps:
        cr,blew=shoot(p,nmax=1)
        rstar=cr[0][0] if cr else np.nan
        mc=abs(0.5*(1.0-np.exp(-2.0*p)))
        if base is None: base=mc
        log(f"{p:>8.2f}{rstar:>12.6f}{mc:>14.6f}{mc/base:>18.6f}")
        rows.append(dict(p=p,rstar=float(rstar),m=float(mc)))
    json.dump(rows,open("/tmp/dyn1_nodeless.json","w"),indent=2)
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
