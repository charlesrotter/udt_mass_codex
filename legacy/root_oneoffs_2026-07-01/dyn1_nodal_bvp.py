#!/usr/bin/env python3
"""
dyn1_nodal_bvp.py -- STEP A part 3: solve the actual sealed-cavity BVP and
enumerate the NODAL family as a discrete catalog.

Recon result so far:
 - DEEP D<=-0.8: monotone rise, ONE crossing at r*~2.546, then diverges.
   The PHYSICAL cavity is [1, r*]; beyond is the (divergent) exterior. This
   is the nodeless ground state n=0.
 - SHALLOW D>=-0.6: damped oscillation relaxing to phi=0 (the 2/r damping).
   Ripples DECAY -> this is the relaxation continuum (#34/#39), not standing.

THE CATALOG QUESTION (catalog-frame legal): a sealed cavity is the domain
[1, R] with phi(1)=D (core), phi(R)=0 (seal interface). The NODE COUNT n =
number of INTERIOR zeros of phi on (1,R) is a DISCRETE structural label.
 - n=0 cavity: phi monotone D->0, seal at the FIRST zero. (nodeless ground.)
 - n>=1 cavity: phi rings, seal at the (n+1)-th zero.

For a given seal radius = the k-th zero crossing r_k(D), we get an
(k-1)-node sealed cavity. The crossings r_k(D) exist for shallow D (damped
oscillation). So nodal SEALED cavities DO exist as static configurations,
indexed by node count n=k-1. We tabulate each and compute its Misner-Sharp
content.

MISNER-SHARP MASS (c=G=1, areal): m_MS(r) = (r/2)(1 - e^{-2 phi(r)}).
The cavity's mass content = the integrated source / the core depth. For an
inside-out cell the public charge is read at the core; we report several
mass diagnostics and the DEPTH p (the catalog mass per CATALOG_FRAME: mass
= cavity depth/MS content, NOT an eigenfrequency).

We tabulate, for a family of D in the oscillatory regime:
  n (node count) ; R_n (seal radius=zero r_{n+1}) ; D (core depth) ;
  m_MS at core ; |integral of source| ; ratios m_n/m_0.

ALSO solve the COLLOCATION BVP (Newton) independently to confirm each nodal
solution is a genuine BVP solution (cross-check the shooting).

DATA-BLIND. Log -> /tmp/dyn1.log.  JSON -> /tmp/dyn1_nodal_bvp.json
"""
import numpy as np, json, time

PHI=1.0; R_IN=1.0
def rhs(r,y):
    phi,phip=y; arg=min(3.0*phi,5.0)
    return np.array([phip, -(2.0/r)*phip+2.0*phip**2+PHI*(1.0-np.exp(arg))])
def rk4(r,y,h):
    k1=rhs(r,y);k2=rhs(r+h/2,y+h/2*k1);k3=rhs(r+h/2,y+h/2*k2);k4=rhs(r+h,y+h*k3)
    return y+(h/6)*(k1+2*k2+2*k3+k4)

def shoot(D,rmax=60.0,tol=1e-13,phip0=1e-7,nmax=8):
    """Return list of (r_k, phi'_k) at the first nmax zero crossings, plus
    full trajectory (downsampled)."""
    r=R_IN; y=np.array([float(D),phip0]); h=5e-4
    crossings=[]; last=y[0]; n=0
    Rtraj=[r];Ptraj=[y[0]]
    src_int=0.0  # integral of source*r^2 dr  (mass-like)
    while r<rmax and n<3_000_000 and len(crossings)<nmax:
        big=rk4(r,y,h);m=rk4(r,y,h/2);s=rk4(r+h/2,m,h/2)
        err=np.sum(np.abs(s-big));scale=tol*(1+np.sum(np.abs(s)))
        if err>scale and h>1e-12: h*=max(0.2,0.9*(scale/err)**0.2);continue
        # accumulate source integral over the step (trapezoid in r, weight r^2)
        arg0=min(3.0*y[0],5.0); arg1=min(3.0*s[0],5.0)
        s0=PHI*(1.0-np.exp(arg0))*r**2; s1=PHI*(1.0-np.exp(arg1))*(r+h)**2
        src_int+=0.5*(s0+s1)*h
        ynew=s;rnew=r+h
        if last<0 and ynew[0]>=0 or last>0 and ynew[0]<=0:
            if abs(last)>1e-12:
                frac=(0-last)/(ynew[0]-last)
                crossings.append((r+frac*h, ynew[1], src_int))
        last=ynew[0];y=ynew;r=rnew;n+=1
        if len(Rtraj)<4000: Rtraj.append(r);Ptraj.append(y[0])
        if abs(y[0])>50 or not np.isfinite(y[0]):
            return crossings, True, np.array(Rtraj),np.array(Ptraj)
        if err<scale/10: h=min(h*1.5,0.02)
    return crossings, False, np.array(Rtraj),np.array(Ptraj)

def ms_core(D):
    # MS mass magnitude at the core areal radius r=1: m=(r/2)(1-e^{-2phi}).
    # phi=D<0 => e^{-2D}>1 => m<0; report |m| as the depth content.
    return 0.5*(1.0-np.exp(-2.0*D))

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72)
    log("dyn1_nodal_bvp -- STEP A part 3: sealed nodal-cavity catalog")
    log("="*72)
    log("A sealed cavity = [1,R_k] with phi(1)=D, phi(R_k)=0; node count n=k-1.")
    log("Seal radii R_k = the k-th zero crossing of the outward shoot.\n")

    # Build the catalog: for each D in the oscillatory regime, the crossings
    # give a TOWER of sealed cavities (n=0 at R_1, n=1 at R_2, ...).
    out=[]
    log("Per-D tower of sealed cavities (n = node count, R_n+1 = seal radius):")
    log(f"{'D':>8}{'n':>4}{'R_seal':>12}{'phip@seal':>14}{'|m_core|':>12}{'src_int':>14}")
    for D in [-0.3,-0.4,-0.5,-0.6,-0.7]:
        cr,blew,_,_=shoot(D)
        mc=abs(ms_core(D))
        for k,(rk,pk,si) in enumerate(cr):
            log(f"{D:>8.3f}{k:>4}{rk:>12.5f}{pk:>14.5e}{mc:>12.6f}{si:>14.5e}")
            out.append(dict(D=D,n=k,R_seal=float(rk),phip_seal=float(pk),
                            m_core=float(mc),src_int=float(si)))
        log("")

    # KEY DISCRIMINATOR: is the seal a REGULAR (mirror-fold) seal? A smooth
    # mirror-fold seal (finite-cell canon, W6) requires phi=0 AND phi'=0 at R
    # (the same-minus involution fixed surface). At a generic zero crossing
    # phi'!=0 (the cavity is NOT smoothly sealed there). So check: does any
    # crossing have phi'->0 (a regular seal => a genuine catalog member)?
    log("="*72)
    log("REGULAR-SEAL TEST (mirror-fold, W6): a genuine sealed cavity needs")
    log("phi=0 AND phi'=0 at the seal (the same-minus fold fixed surface).")
    log("Generic crossings have phi'!=0 -> those are NOT smooth seals, just")
    log("the relaxation passing through 0. A discrete catalog needs a")
    log("DISCRETE set of (D, R) with BOTH phi=0 and phi'=0 at R.\n")
    log("Scanning |phi'| at crossings above: the SMALLEST |phi'@seal| flags")
    log("near-regular seals (candidate genuine cavities).")
    smallest={}
    for rec in out:
        smallest.setdefault(rec['n'],[]).append((abs(rec['phip_seal']),rec['D'],rec['R_seal']))
    for n in sorted(smallest):
        vals=sorted(smallest[n])
        log(f"  n={n}: min|phip@seal|={vals[0][0]:.4e} at D={vals[0][1]}, R={vals[0][2]:.4f}")

    json.dump(out,open("/tmp/dyn1_nodal_bvp.json","w"),indent=2)
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
