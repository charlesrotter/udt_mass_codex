"""AXIS 5: is the C-3 (off-diagonal Class-B, 0/6800) object SEPARATE from the
diagonal time-kinetic sign? Independent mini-scan with my OWN seed.
Also: does the diagonal sign fix touch C-3 at all? Agent ns-verify 2026-06-13."""
import numpy as np, sympy as sp

# C-3 object: M=[[-f,a,b],[a,1/f,q],[b,q,A]] eliminated -> L*=-R/sqrt(fD2),
# R=fP+D2 vT^2.  NOTE: R already has the CORRECT Lorentzian sign in vT^2
# (D2 vT^2 with D2=A/f-q^2; the f_T^2 sector here is +D2 vT^2 inside R, and
# the overall -1/sqrt sign).  This object is NOT the diagonal L_red; the
# diagonal sign error lives ONLY in v_a3 line 23's spherical L_red used by C-2.
fL,AL = sp.symbols('fL AL', positive=True)
qS = sp.Symbol('qS', real=True)
vTs,vrs,vhs = sp.symbols('vTs vrs vhs', real=True)
D2L=AL/fL-qS**2; PL=AL*vrs**2-2*qS*vrs*vhs+vhs**2/fL
RL=fL*PL+D2L*vTs**2; QL=fL*PL-D2L*vTs**2
LB=-RL/sp.sqrt(fL*D2L)
H3=sp.hessian(LB,(vTs,vrs,vhs))
gq=[sp.diff(sp.diff(LB,qS),v) for v in (vTs,vrs,vhs)]
hqq=sp.diff(LB,qS,2)
F_H3=sp.lambdify((vTs,vrs,vhs,qS,fL,AL),H3,'numpy')
F_gq=sp.lambdify((vTs,vrs,vhs,qS,fL,AL),gq,'numpy')
F_hqq=sp.lambdify((vTs,vrs,vhs,qS,fL,AL),hqq,'numpy')
F_Q=sp.lambdify((vTs,vrs,vhs,qS,fL,AL),QL,'numpy')

rng=np.random.default_rng(112358)   # MY own seed, different from v_a3
def qroot(fv,Av,vrv,vhv,vTv):
    c3=vTv**2; c1=fv*Av*vrv**2+vhv**2-(Av/fv)*vTv**2; c0=-2*Av*vrv*vhv
    if c3<1e-300: return -c0/c1 if c1!=0 else None
    rts=np.roots([c3,0,c1,c0]); rts=[z.real for z in rts if abs(z.imag)<1e-9*max(1,abs(z))]
    if not rts: return None
    qs=2*Av*vrv*vhv/(fv*Av*vrv**2+vhv**2)
    return min(rts,key=lambda z:abs(z-qs))
sigs={}; n_tot=n_match=0; n_eT=0
for _ in range(8000):
    fv=float(np.exp(rng.uniform(np.log(.05),np.log(20))))
    Av=float(np.exp(rng.uniform(np.log(.05),np.log(20))))
    vrv,vhv,vTv=rng.normal(size=3)*10**rng.uniform(-1,1,size=3)
    qv=qroot(fv,Av,vrv,vhv,vTv)
    if qv is None or Av/fv-qv**2<=1e-8: continue
    try:
        Hvv=np.array(F_H3(vTv,vrv,vhv,qv,fv,Av),float)
        gvec=np.array(F_gq(vTv,vrv,vhv,qv,fv,Av),float)
        hq=float(F_hqq(vTv,vrv,vhv,qv,fv,Av))
    except Exception: continue
    if not np.isfinite(hq) or abs(hq)<1e-10: continue
    Heff=Hvv-np.outer(gvec,gvec)/hq
    if not np.all(np.isfinite(Heff)): continue
    w,V=np.linalg.eigh(Heff)
    if np.min(np.abs(w))<1e-9*np.max(np.abs(w)): continue
    sig=tuple(int(np.sign(x)) for x in w); sigs[sig]=sigs.get(sig,0)+1; n_tot+=1
    Qv=float(F_Q(vTv,vrv,vhv,qv,fv,Av))
    ok=(Qv>0 and sig==(-1,-1,1)) or (Qv<0 and sig==(-1,-1,-1)); n_match+=ok
    # is the +(timelike) eigenvector the T-component (index 0)?
    if sig==(-1,-1,1):
        vplus=V[:,2]
        if abs(vplus[0])==np.max(np.abs(vplus)): n_eT+=1
print("MY C-3 signatures:", sigs)
print(f"MY sgn(Q) partition match: {n_match}/{n_tot}")
print(f"timelike-dir == e_T (T-dominated): {n_eT}/{n_tot}  (0 or near-0 reproduces #22 '0/6800 e_T never timelike')")
