#!/usr/bin/env python3
"""
dyn1_nodal_profiles.py -- STEP A part 2: resolve the node structure.

Recon (dyn1_nodal_explore) found TWO regimes:
  - DEEP cells D<=-0.8: phi rises monotone, crosses 0 ONCE at r*~2.546
    (the documented nodeless interface asymptote), then DIVERGES (+inf).
  - SHALLOW cells D>=-0.6: phi OSCILLATES about phi=0 (restoring const 3
    from linearizing 1-e^{3phi} at 0), many crossings.

Two distinct candidate "nodal" readings to test:
 (R1) BOUNDED-OSCILLATION reading: is the shallow oscillation a BOUNDED
      standing structure (a real nodal cavity, phi stays finite forever),
      or does its amplitude grow / is it transient? If bounded, the n-th
      zero is a candidate seal radius R_n for an n-node cavity at fixed D.
 (R2) DISCRETE-DEPTH reading (the true catalog label): fix the OUTER
      boundary type = "first regular return to phi=0 with phi'=0" (a
      smooth mirror-fold seal, finite-cell canon). A NODELESS cavity seals
      at the first turning; an n-NODE cavity would need phi to ring n times
      then seal. Does a DISCRETE set of depths D_n give an n-node sealed
      cell?

This script:
 (1) prints full profiles for one deep + one shallow D (amplitude growth?).
 (2) measures the oscillation amplitude envelope vs r for shallow D
     (bounded => nodal cavities exist; growing/decaying => not a standing
     catalog).
 (3) checks the local fixed point: phi=0, phi'=0 is the ONLY equilibrium;
     classify it (center vs spiral) in the r->inf autonomous limit.

DATA-BLIND. Log -> /tmp/dyn1.log.
"""
import numpy as np, json, time

PHI=1.0; R_IN=1.0
def rhs(r,y):
    phi,phip=y; arg=min(3.0*phi,5.0)
    return np.array([phip, -(2.0/r)*phip+2.0*phip**2+PHI*(1.0-np.exp(arg))])
def rk4(r,y,h):
    k1=rhs(r,y);k2=rhs(r+h/2,y+h/2*k1);k3=rhs(r+h/2,y+h/2*k2);k4=rhs(r+h,y+h*k3)
    return y+(h/6)*(k1+2*k2+2*k3+k4)

def run(D,rmax=120.0,tol=1e-12,phip0=1e-7):
    r=R_IN; y=np.array([float(D),phip0]); h=1e-3
    R=[r];P=[y[0]];V=[y[1]]; n=0; last=y[0]; cross=[]
    extrema=[]  # (r, phi) at phi'=0 -> amplitude envelope
    lastv=y[1]
    while r<rmax and n<3_000_000:
        big=rk4(r,y,h); m=rk4(r,y,h/2); s=rk4(r+h/2,m,h/2)
        err=np.sum(np.abs(s-big)); scale=tol*(1+np.sum(np.abs(s)))
        if err>scale and h>1e-11: h*=max(0.2,0.9*(scale/err)**0.2); continue
        ynew=s; rnew=r+h
        if last<0 and ynew[0]>=0 or last>0 and ynew[0]<=0:
            if abs(last)>1e-12:
                frac=(0-last)/(ynew[0]-last); cross.append(r+frac*h)
        if lastv*ynew[1]<0:  # phi' changes sign -> extremum
            extrema.append((r, y[0]))
        last=ynew[0]; lastv=ynew[1]; y=ynew; r=rnew; n+=1
        R.append(r);P.append(y[0]);V.append(y[1])
        if abs(y[0])>50 or not np.isfinite(y[0]):
            return dict(D=D,R=np.array(R),P=np.array(P),V=np.array(V),
                        cross=cross,extrema=extrema,blew=True)
        if err<scale/10: h=min(h*1.5,0.05)
    return dict(D=D,R=np.array(R),P=np.array(P),V=np.array(V),
                cross=cross,extrema=extrema,blew=False)

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72); log("dyn1_nodal_profiles -- STEP A part 2: node structure resolution"); log("="*72)

    # (3) Fixed-point classification in the r->inf autonomous limit.
    # Autonomous (drop 2/r): phi'' = 2 phi'^2 + (1-e^{3phi}). About (0,0):
    # phi''≈ -3 phi (linearize; 2phi'^2 quadratic). d/dr[phi,phip]=[phip,-3phi]
    # eigenvalues +-i*sqrt(3) -> CENTER (undamped). With +2/r the damping ->0,
    # so for large r it's a near-center -> bounded oscillation expected.
    log("\n(3) Fixed point (0,0): autonomous linearization phi''=-3 phi =>")
    log("    eigenvalues +- i*sqrt(3) = +-1.73205 i  -> CENTER (oscillatory,")
    log("    undamped). The 2/r term -> 0, so large-r motion is near-center.")
    log("    => the shallow oscillation should be BOUNDED (a standing pattern),")
    log("    NOT growing. (The +2 phi'^2 nonlinearity caps amplitude.)")

    # (1)(2) profiles + envelope
    log("\n(1)/(2) amplitude ENVELOPE (extrema of phi) vs r, shallow vs deep:")
    for D in [-0.4,-0.6,-0.8,-1.0]:
        res=run(D)
        ex=res['extrema']
        amps=[abs(p) for (_,p) in ex]
        nc=len(res['cross'])
        log(f"\n  D={D}: blew={res['blew']}, n_crossings={nc}, n_extrema={len(ex)}")
        if ex:
            first5=", ".join(f"{a:.4f}" for a in amps[:5])
            last5=", ".join(f"{a:.4f}" for a in amps[-5:])
            log(f"    extrema |phi| first: [{first5}]  last: [{last5}]")
            if len(amps)>=4:
                trend = "GROWING" if amps[-1]>1.5*amps[0] else ("DECAYING" if amps[-1]<0.6*amps[0] else "BOUNDED/STEADY")
                log(f"    envelope trend: {trend}  (max|phi|={max(amps):.4f})")
        if len(res['cross'])>=4:
            cs=", ".join(f"{c:.4f}" for c in res['cross'][:6])
            log(f"    first zero-crossings r: [{cs}]")

    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
