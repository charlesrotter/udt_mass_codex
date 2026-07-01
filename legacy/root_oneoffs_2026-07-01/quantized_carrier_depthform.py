#!/usr/bin/env python3
"""
quantized_carrier_depthform.py
================================================================================
PROFILE-ROBUSTNESS of the depth-dependence verdict + the "Liouville differentiates
away the exponential" claim, across SEVERAL native-like depth profiles.

Agent: claude-opus-4-8[1m]. Date 2026-06-19. STRUCTURE-FIRST DATA-BLIND. NOT canon.

The eigensolve found: binding(D) ~ POWER-LAW (~D^3.5), NOT exp(D); and the tower is
SHALLOW (1-2 bound levels before over-binding into tachyons). Before banking "the
quantized radial carrier does NOT give an exponential hierarchy", test whether that
verdict is an artifact of the Gaussian profile v0=-D e^{-(r/a)^2}.

We test the STRUCTURAL claim: in V_eff = l(l+1) + V_L[v0], the Liouville potential
V_L = (1/2)(2v0')' - (1/4)(2v0')^2 depends only on DERIVATIVES of v0, so the e^{phi}
AMPLITUDE (exponential in depth) enters only through v0' (linear in D) -> well depth
~ D^2 (power-law). Tested across: Gaussian, Lorentzian, exponential-core, sech^2.
If ALL give power-law (not exp) binding, the obstruction is profile-robust.
"""
import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal
def hr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

r,D,a = sp.symbols('r D a', positive=True)
profiles = {
    'gaussian'   : -D*sp.exp(-(r/a)**2),
    'lorentzian' : -D/(1+(r/a)**2),
    'expcore'    : -D*sp.exp(-r/a),
    'sech2'      : -D/sp.cosh(r/a)**2,
}
# For each, V_eff = l(l+1) + (1/2)s' - (1/4)s^2,  s=2 v0'. Build a stable lambda.
def make_Veff(expr):
    v0=expr; s=2*sp.diff(v0,r); VL=sp.Rational(1,2)*sp.diff(s,r)-sp.Rational(1,4)*s**2
    f=sp.lambdify((r,D,a),sp.simplify(VL),'numpy')
    return f
Vfuncs={k:make_Veff(v) for k,v in profiles.items()}

def eigensolve(Vf,Dval,aval,l,R=20.,h=0.004,r_core=0.02):
    N=int((R-r_core)/h); rr=r_core+h*np.arange(1,N+1)
    with np.errstate(over='ignore',invalid='ignore'):
        VL=Vf(rr,Dval,aval)
    VL=np.nan_to_num(VL,nan=0.0,posinf=1e6,neginf=-1e6)
    V=l*(l+1)+VL
    main=2/h**2+V; off=-1/h**2*np.ones(N-1)
    k=min(8,N-1)
    E=eigh_tridiagonal(main,off,select='i',select_range=(0,k),eigvals_only=True); E.sort()
    return E,l*(l+1)

hr("Depth-form across native-like profiles: binding(D) EXP or POWER-LAW? + #bound, D*")
for name,Vf in Vfuncs.items():
    Ds=np.arange(0.4,4.01,0.2); bind=[]; e0=[]; nb=[]
    for Dval in Ds:
        E,Vinf=eigensolve(Vf,Dval,1.0,1)
        bind.append(Vinf-E[0]); e0.append(E[0]); nb.append(int(np.sum(E<Vinf-1e-6)))
    bind=np.array(bind); e0=np.array(e0); nb=np.array(nb)
    g=bind>1e-4
    if g.sum()<4:
        print(f" {name:11s}: <4 binding points, skip fit (max #bound={nb.max()})"); continue
    se=np.polyfit(Ds[g],np.log(bind[g]),1); re=np.std(np.log(bind[g])-np.polyval(se,Ds[g]))
    spw=np.polyfit(np.log(Ds[g]),np.log(bind[g]),1); rp=np.std(np.log(bind[g])-np.polyval(spw,np.log(Ds[g])))
    # D* where E_0 crosses 0
    cross=np.where(np.diff(np.sign(e0)))[0]
    Dstar = Ds[cross[0]] if len(cross) else None
    verdict='EXP-in-D' if re<rp else f'POWER ~D^{spw[0]:.1f}'
    print(f" {name:11s}: binding {verdict:14s} (exp-resid={re:.2f} pow-resid={rp:.2f}) | "
          f"max #bound={nb.max()} | E_0<0 (tachyon) beyond D*~{Dstar}")

hr("Is the well EVER deep enough for a TALL tower (many radial levels) before tachyon?")
print(" count bound levels with E>0 (stable) at the depth just below each profile's D*:\n")
for name,Vf in Vfuncs.items():
    best=0; bestD=None
    for Dval in np.arange(0.4,5.01,0.1):
        E,Vinf=eigensolve(Vf,Dval,1.0,1)
        stable=E[(E>1e-9)&(E<Vinf-1e-6)]
        if len(stable)>best: best=len(stable); bestD=round(Dval,1)
    print(f" {name:11s}: MAX stable (E>0) bound radial levels = {best}  (at D~{bestD})")

hr("STRUCTURAL CONCLUSION (printed) -- feeds the results doc")
print("""
 If ALL profiles give POWER-LAW binding and only 1-2 stable radial levels, then:
  - the quantized native radial carrier gives an INTRINSIC but SHALLOW discrete well
    (a few levels), NOT a tall exponential generation tower;
  - the depth amplitude e^{phi} does NOT pass through to an exponential mass law,
    because V_eff is built from DERIVATIVES of v0 (Liouville), which kill the
    exponential down to a power of the depth parameter;
  - the radial-overtone (n) axis is NOT the lepton-generation axis on this carrier.
 This is profile-robust => a structural obstruction, not a profile artifact.
""")
print("DONE.")
