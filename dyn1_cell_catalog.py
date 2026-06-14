#!/usr/bin/env python3
"""
dyn1_cell_catalog.py -- STEP A (correct chart): the nodal cell catalog in the
VALIDATED flow chart, and STEP B linear stability sign-test.

CORRECTION over my first Step-A pass: the repo's VALIDATED canonical cell
(#34/#39, wint_cell2d.py) is NOT the Dirichlet neg_sweep shoot. It is the
flow-chart cell v(m):
    v_mm = Phi (e^{-2v} - e^{v}) = -dU/dv,   U(v)=Phi/2 e^{-2v} + Phi e^{v}
sealed by TWO turning points v_m=0 (regular mirror-fold seals, the W6 fold).
U has a single minimum at v=0 (U_min=1.5 Phi); the cell is ONE BOUNCE of a
particle of energy E in the well U. The half-period L(E) (cell chart-width)
is a SMOOTH continuum in E (registry #33). c=G=1, Phi=1.

STEP A -- the NODAL family as MULTI-BOUNCE orbits. In a single well U(v) a
bounded orbit has exactly ONE oscillation between its two turning points;
"n interior nodes" of v would require v to cross the well-bottom (v=0)
multiple times = multiple bounces = a LONGER orbit (period n*full-period).
We test directly: does the well admit DISTINCT multi-bounce sealed cells
(n=1,2,...) at DISCRETE energies, or is every sealed orbit a continuous
slice of the same one-parameter (E) family? We enumerate orbits, count
v=0 crossings (nodes), and tabulate Misner-Sharp content vs (E,n).

MS mass content: along the chart, m_MS = (1/2)(1 - e^{-2 v}) per the repo
convention; the cell's public charge = the depth content. We report the
amplitude / depth and an integrated MS diagnostic for each member.

STEP B -- linear stability sign-test (NOT a mass): perturb v(m)->v+eps u(m),
the static cell is a critical point of the action; the perturbation operator
is the Jacobi/Sturm-Liouville operator
    L u = -u_mm + W(m) u,   W(m) = d/dv[-Phi(e^{-2v}-e^{v})] = Phi(2 e^{-2v}+e^{v})
(second variation of the energy functional). Because W(m)=U''(v(m)) and U is
CONVEX (U''=2e^{-2v}+e^{v} > 0 everywhere), the operator L is POSITIVE on the
appropriate BC class => no negative mode => the one-bounce cell is a MINIMUM
=> STABLE; multi-bounce orbits cross the convex region's inflection and pick
up negative modes (classic: n-th excited orbit has n unstable directions).
We compute the lowest eigenvalues omega^2 of L for each member numerically
(Neumann BC = the turning-point seal) on GPU/CPU float64 and report the sign
pattern (omega^2>0 all => stable; any omega^2<0 => unstable, with growth rate
sqrt(-omega^2)). This is a legitimate existence/stability test.

DATA-BLIND. Log -> /tmp/dyn1.log. JSON -> /tmp/dyn1_cell_catalog.json
"""
import numpy as np, json, time
import mpmath as mp

Phi=1.0
def U(v): return 0.5*np.exp(-2*v)+np.exp(v)      # potential (Phi=1)
def Umin(): return 1.5
def force(v): return np.exp(-2*v)-np.exp(v)       # v_mm = force = -U'(v)
def Wpp(v): return 2*np.exp(-2*v)+np.exp(v)       # U''(v) = W(m), the Jacobi weight

def orbit(E, n_bounce=1, npts=4000):
    """Integrate v_mm=force from inner turning point through n_bounce full
    oscillations. Returns m grid, v(m), turning points, node count."""
    # inner/outer turning points: U(v)=E
    # bracket below and above v=0
    def root(sgn):
        a=0.0; b=sgn*0.01
        for _ in range(400):
            if U(b)>E:
                from scipy.optimize import brentq
                return brentq(lambda x:U(x)-E, a, b)
            a=b; b=b*1.3 if abs(b)<60 else b
            if abs(b)>80: return None
        return None
    vlo=root(-1); vhi=root(+1)
    if vlo is None or vhi is None: return None
    # integrate from vlo (v_m=0) outward in chart m. Use small step RK4.
    # full period = vlo->vhi->vlo. n_bounce half-bounces? We define ONE cell =
    # vlo -> vhi (half period L). n_bounce=1 is the standard cell. Multi-bounce
    # = repeat. Count v=0 crossings on the orbit.
    varr=[vlo]; m=0.0; marr=[0.0]; vm=1e-9
    h=1e-4
    # one half-period: integrate until v_m=0 again (reach vhi)
    half_segs=2*n_bounce  # number of vlo<->vhi traversals
    seg=0; v=vlo; cross=0; last=v
    msafe=0
    while seg<half_segs and msafe<5_000_000:
        # RK4 step of (v,vm)
        def f(v,vm): return vm, force(v)
        k1=f(v,vm); k2=f(v+0.5*h*k1[0],vm+0.5*h*k1[1])
        k3=f(v+0.5*h*k2[0],vm+0.5*h*k2[1]); k4=f(v+h*k3[0],vm+h*k3[1])
        vn=v+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        vmn=vm+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        m+=h
        if last<0 and vn>=0 or last>0 and vn<=0: cross+=1
        # turning point: vm changes sign
        if vm*vmn<0: seg+=1
        last=vn; v=vn; vm=vmn; marr.append(m); varr.append(v); msafe+=1
    return dict(E=E,vlo=vlo,vhi=vhi,L=m/(2*n_bounce),m=np.array(marr),
                v=np.array(varr),nodes=cross,n_bounce=n_bounce)

def stability(orb):
    """Lowest eigenvalues of L u = -u'' + W(m) u with Neumann BC (turning pts).
    omega^2 = eigenvalues. Positive => stable."""
    m=orb['m']; v=orb['v']
    # uniform regrid for clean FD
    N=2000
    mm=np.linspace(m[0],m[-1],N)
    vv=np.interp(mm,m,v)
    dm=mm[1]-mm[0]
    W=Wpp(vv)
    # -u'' + W u, Neumann (u'=0) at both ends via ghost reflection
    main=2.0/dm**2 + W
    off=-1.0/dm**2*np.ones(N-1)
    A=np.diag(main)+np.diag(off,1)+np.diag(off,-1)
    # Neumann: u_0=u_1, u_{N-1}=u_{N-2}: modify endpoints
    A[0,0]=1.0/dm**2+W[0]; A[-1,-1]=1.0/dm**2+W[-1]
    ev=np.linalg.eigvalsh(A)
    return np.sort(ev)[:6]

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72)
    log("dyn1_cell_catalog -- STEP A (flow chart) + STEP B linear stability")
    log("="*72)
    log("Cell: v_mm=e^{-2v}-e^{v} in well U=0.5e^{-2v}+e^{v}, U_min=1.5 at v=0.")
    log("Sealed by turning points v_m=0 (regular mirror fold). c=G=1, Phi=1.\n")

    # cross-check the banked anchor L(E=3)=1.67427938129 (mpmath)
    def U_mp(v): return 0.5*mp.e**(-2*v)+mp.e**v
    def cell_L(E):
        from mpmath import findroot,quad,sqrt,mpf
        g=lambda v:U_mp(v)-E
        def br(s):
            a=mpf(0);b=s*mpf('0.01')
            for _ in range(300):
                if g(b)>0: return findroot(g,(a,b),solver='bisect')
                a=b;b=b*mpf('1.3')
                if abs(b)>60: return None
            return None
        vlo=br(-1);vhi=br(1)
        return float(quad(lambda v:1/sqrt(max(2*(E-U_mp(v)),mpf('1e-40'))),[vlo,vhi]))
    Lanchor=cell_L(mp.mpf('3.0'))
    log(f"ANCHOR check L(E=3)={Lanchor:.11f} vs banked 1.67427938129 -> "
        f"{'MATCH' if abs(Lanchor-1.67427938129)<1e-6 else 'MISMATCH'}\n")

    # STEP A: the one-bounce E-family (the standard cell) -- continuum?
    log("STEP A.1 -- one-bounce cell family vs partition energy E:")
    log(f"{'E':>8}{'L(half-per)':>14}{'amp=vhi-vlo':>14}{'vlo':>9}{'vhi':>9}{'nodes':>7}")
    cat=[]
    Es=[1.6,1.8,2.0,2.5,3.0,4.0,6.0,9.0]
    for E in Es:
        orb=orbit(E,n_bounce=1)
        if orb is None: continue
        amp=orb['vhi']-orb['vlo']
        log(f"{E:>8.3f}{orb['L']:>14.6f}{amp:>14.6f}{orb['vlo']:>9.4f}{orb['vhi']:>9.4f}{orb['nodes']:>7}")
        cat.append(dict(E=E,L=orb['L'],amp=float(amp),nodes=orb['nodes'],n_bounce=1))

    # STEP A.2: multi-bounce orbits -- are these DISTINCT discrete cells?
    log("\nSTEP A.2 -- multi-bounce orbits (n_bounce=1,2,3) at fixed E=3:")
    log("If multi-bounce = genuinely distinct sealed cells at DISCRETE E, that")
    log("is a nodal catalog. If they are just repeated copies of the SAME")
    log("one-bounce cell (period multiples, same amp, continuous E), NO catalog.")
    log(f"{'n_bounce':>9}{'total chart len':>16}{'nodes':>7}{'amp':>10}{'E':>7}")
    for nb in [1,2,3]:
        orb=orbit(3.0,n_bounce=nb)
        log(f"{nb:>9}{orb['m'][-1]:>16.6f}{orb['nodes']:>7}{orb['vhi']-orb['vlo']:>10.6f}{3.0:>7}")

    # STEP B: linear stability sign-test of the one-bounce cells
    log("\nSTEP B -- linear stability sign-test (Jacobi op L u=-u''+U''(v)u,")
    log("Neumann/turning-point BC). U''=2e^{-2v}+e^{v} > 0 everywhere (CONVEX),")
    log("so L is POSITIVE => omega^2>0 all modes => STABLE. Numerical confirm:")
    log(f"{'E':>8}{'omega^2_0':>14}{'omega^2_1':>14}{'omega^2_2':>14}{'verdict':>10}")
    for E in [1.8,2.0,3.0,4.0,6.0]:
        orb=orbit(E,n_bounce=1)
        ev=stability(orb)
        verdict="STABLE" if ev[0]>-1e-8 else "UNSTABLE"
        log(f"{E:>8.3f}{ev[0]:>14.6e}{ev[1]:>14.6e}{ev[2]:>14.6e}{verdict:>10}")
        for c in cat:
            if abs(c['E']-E)<1e-9: c['omega2_min']=float(ev[0]); c['stable']=bool(ev[0]>-1e-8)

    # STEP B.2: stability of MULTI-BOUNCE orbits (the nodal members)
    log("\nSTEP B.2 -- stability of multi-bounce (nodal) orbits at E=3:")
    log("A 2-bounce orbit re-enters the well; its Jacobi operator on the LONGER")
    log("domain has MORE low modes -> test if any omega^2<0 (unstable).")
    log(f"{'n_bounce':>9}{'omega^2_0':>14}{'omega^2_1':>14}{'#neg modes':>12}{'verdict':>10}")
    for nb in [1,2,3]:
        orb=orbit(3.0,n_bounce=nb)
        ev=stability(orb)
        nneg=int(np.sum(ev<-1e-8))
        verdict="STABLE" if nneg==0 else f"UNSTABLE({nneg} neg)"
        log(f"{nb:>9}{ev[0]:>14.6e}{ev[1]:>14.6e}{nneg:>12}{verdict:>10}")

    json.dump(cat,open("/tmp/dyn1_cell_catalog.json","w"),indent=2)
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
