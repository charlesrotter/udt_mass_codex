"""
Efficient EXACT second-variation engine, vectorized over the angular grid.

Mode: n(eps; r) = normalize( n0(F(r),th,ph) + eps * psi(r) * Tang(th,ph) )
where Tang = f(th,ph)*e1 + g(th,ph)*e2 is a fixed angular tangent vector field
(e1,e2 the orthonormal tangent frame at n0). psi(r) is the radial profile.

The total action S = INT dr dOmega A(r,th,ph) where A is the exact (L2+L4) density*sqrt(g)
evaluated on n(eps). delta^2 S = (1/2) d^2 S/deps^2 |_0. Because the mode is separable
n(eps;r) with eps*psi(r)*Tang, the second variation is a quadratic functional in psi:
   delta^2 S = INT dr [ P(r) psi'(r)^2 + Q(r) psi(r)^2 + R(r) psi(r)psi'(r) ]
We extract P,Q,R as radial densities by the following: the integrand A depends on
psi and psi' (psi' enters only through dn/dr). Expand A to O(eps^2):
   A2(r,th,ph) = alpha(r,th,ph) psi^2 + beta(r,th,ph) psi'^2 + gamma(r,th,ph) psi psi'
Integrate over the sphere -> P=INT beta, Q=INT alpha, R=INT gamma (per dr).
We get alpha,beta,gamma by finite differences in (psi, psi') treated as independent
local values at each r (valid: A is local in r, depends on field & its r-derivative).

Implementation: at fixed r, treat the field value contribution as
   N(eps) = n0 + eps*psi*Tang ; dN/dr = dn0/dr + eps*(psi'*Tang + psi*dTang/dr... )
Tang depends on r through e1,e2,F. We include that. We then normalize and compute A.
We compute A as a function of two scalars (s := eps*psi, sp := eps*psi') by setting
   field   = normalize( n0 + s*Tang )
   field_r-deriv = d/dr[ normalize(n0(F(r)) + s(r)*Tang(F(r)..)) ]
The r-derivative is taken analytically-by-FD over a small r-window where we prescribe
s(r)=s0+sp0*(r-r0). So at each r0 we build a 3-point r-stencil, set s linear with slope
sp0 and value s0, compute A, and read alpha,beta,gamma by FD in (s0,sp0).
"""
import numpy as np

def build_channel(F_of_r, Fp_of_r, phi_of_r, ang_f, ang_g, rgrid,
                  Nth=120, Nph=24, ds=1e-4):
    """Return radial densities P(r),Q(r),R(r) and time-weight Wd(r) on rgrid for the
    transverse channel with angular factors ang_f,ang_g (functions of th,ph).
    Vectorized over the angular grid."""
    ths=np.linspace(1e-3,np.pi-1e-3,Nth); dth=ths[1]-ths[0]
    phs=np.linspace(0,2*np.pi,Nph,endpoint=False); dph=2*np.pi/Nph
    TH,PH=np.meshgrid(ths,phs,indexing='ij')   # (Nth,Nph)
    sinth=np.sin(TH)
    f_ang=ang_f(TH,PH); g_ang=ang_g(TH,PH)

    def n0_frame(F):
        # vectorized n0,e1,e2 over (TH,PH)
        a=np.sin(F)*sinth*np.cos(PH); b=np.sin(F)*sinth*np.sin(PH); c=np.cos(F)*np.ones_like(TH)
        v=np.stack([a,b,c],axis=-1)               # (Nth,Nph,3)
        n0=v/np.linalg.norm(v,axis=-1,keepdims=True)
        hF=1e-6
        def nn(FF):
            a2=np.sin(FF)*sinth*np.cos(PH); b2=np.sin(FF)*sinth*np.sin(PH); c2=np.cos(FF)*np.ones_like(TH)
            w=np.stack([a2,b2,c2],axis=-1); return w/np.linalg.norm(w,axis=-1,keepdims=True)
        d=(nn(F+hF)-nn(F-hF))/(2*hF)
        d=d-np.sum(d*n0,axis=-1,keepdims=True)*n0
        e1=d/np.linalg.norm(d,axis=-1,keepdims=True)
        e2=np.cross(n0,e1)
        return n0,e1,e2

    def field(F, s):
        # s scalar (eps*psi); Tang = f*e1+g*e2 (uses frame at THIS F)
        n0,e1,e2=n0_frame(F)
        Tang=f_ang[...,None]*e1+g_ang[...,None]*e2
        w=n0+s*Tang
        return w/np.linalg.norm(w,axis=-1,keepdims=True)

    def angular_derivs(F,s):
        hT=1e-6; hP=1e-6
        # need dn/dth, dn/dph of field(F,s); F fixed, s fixed
        # recompute frame perturbations via finite diff in TH,PH by rebuilding -- but
        # ang factors & frame depend on TH,PH already in grid; do FD by shifting grid.
        pass

    # We compute A(r) densities by a local r-stencil. Simpler & exact-enough:
    # represent everything on the (TH,PH) grid and take angular derivatives by spectral-free
    # central differences ALONG the grid axes.
    def grad_ang(arr):
        # arr shape (Nth,Nph,3); central diff along th (axis0) and ph(axis1, periodic)
        dT=np.zeros_like(arr); dP=np.zeros_like(arr)
        dT[1:-1]=(arr[2:]-arr[:-2])/(2*dth)
        dT[0]=(arr[1]-arr[0])/dth; dT[-1]=(arr[-1]-arr[-2])/dth
        dP=(np.roll(arr,-1,axis=1)-np.roll(arr,1,axis=1))/(2*dph)
        return dT,dP

    def density_grid(F,Fp,phd,r,s,sp):
        """A(th,ph)*[no sphere integ yet]; s=eps*psi at r, sp=eps*psi' at r.
        dn/dr = dfield/dF*Fp + dfield/ds*sp."""
        hF=1e-6; hs=1e-7
        fld=field(F,s)
        dFld_dF=(field(F+hF,s)-field(F-hF,s))/(2*hF)
        dFld_ds=(field(F,s+hs)-field(F,s-hs))/(2*hs)
        dnr=dFld_dF*Fp + dFld_ds*sp
        dnt,dnp=grad_ang(fld)
        grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*sinth**2)
        grad2=grr*np.sum(dnr*dnr,axis=-1)+gtt*np.sum(dnt*dnt,axis=-1)+gpp*np.sum(dnp*dnp,axis=-1)
        e2=0.5*grad2
        Srt=np.cross(dnr,dnt); Srp=np.cross(dnr,dnp); Stp=np.cross(dnt,dnp)
        L4s=2*(grr*gtt*np.sum(Srt*Srt,axis=-1)+grr*gpp*np.sum(Srp*Srp,axis=-1)+gtt*gpp*np.sum(Stp*Stp,axis=-1))
        e4=0.25*L4s
        sqrtg=np.exp(phd)*r**2*sinth
        return (e2+e4)*sqrtg   # (Nth,Nph)

    def sphere_int(arr):
        return np.sum(arr)*dth*dph

    Pr=np.zeros_like(rgrid); Qr=np.zeros_like(rgrid); Rr=np.zeros_like(rgrid); Wr=np.zeros_like(rgrid)
    for i,r in enumerate(rgrid):
        F=F_of_r(r); Fp=Fp_of_r(r); phd=phi_of_r(r)
        # quadratic form in (s,sp): A = A0 + (linear) + alpha s^2 + beta sp^2 + gamma s sp
        # finite-difference second derivatives at s=sp=0
        d=ds
        A_pp=sphere_int(density_grid(F,Fp,phd,r, d, 0))
        A_mm=sphere_int(density_grid(F,Fp,phd,r,-d, 0))
        A_00=sphere_int(density_grid(F,Fp,phd,r, 0, 0))
        alpha=(A_pp-2*A_00+A_mm)/(2*d**2)        # d^2A/ds^2 /2 -> coefficient of s^2
        B_pp=sphere_int(density_grid(F,Fp,phd,r,0, d))
        B_mm=sphere_int(density_grid(F,Fp,phd,r,0,-d))
        beta=(B_pp-2*A_00+B_mm)/(2*d**2)
        C_pp=sphere_int(density_grid(F,Fp,phd,r, d, d))
        C_mm=sphere_int(density_grid(F,Fp,phd,r,-d,-d))
        gamma=((C_pp-2*A_00+C_mm)/(2*d**2) - alpha - beta)  # cross
        Qr[i]=alpha; Pr[i]=beta; Rr[i]=gamma
        # time-kinetic weight: g^{tt}=-e^{2phi}; kinetic energy density quadratic in s_dot.
        # The t-kinetic of L2: (xi/2) e^{2phi} |dn/dt|^2 ; n depends on t via s(t)=eps psi.
        # |dn/dt|^2 = |dfield/ds|^2 * sdot^2. Plus L4 time part: cross terms g^{tt}g^{spatial}.
        Wr[i]=weight_at(field, n0_frame, f_ang,g_ang, sinth, dth,dph, F,Fp,phd,r, sphere_int, grad_ang)
    return Pr,Qr,Rr,Wr,rgrid

def weight_at(field,n0_frame,f_ang,g_ang,sinth,dth,dph,F,Fp,phd,r,sphere_int,grad_ang):
    """Time-kinetic weight W(r): coefficient of (1/2) sdot^2 in the t-kinetic energy.
    L2 t-kinetic: (xi/2) g^{tt}_magnitude |dn/dt|^2 with g^{tt}=-e^{2phi} -> energy uses
    +e^{2phi}. density = (1/2) e^{2phi} |dfield/ds|^2. L4 t-kinetic: (kappa/2) sum over
    spatial j of g^{tt}g^{jj}|S_{tj}|^2, S_{tj}=dn/dt x dn/dx^j -> (1/2)e^{2phi} g^{jj}
    |dfield/ds x dn/dx^j|^2. All * sqrt(g). Coefficient of (1/2)sdot^2 -> W density."""
    hs=1e-7
    fld=field(F,0.0)
    dFld_ds=(field(F,hs)-field(F,-hs))/(2*hs)   # dn/ds at s=0 = Tang (tangent)
    # spatial derivs of background
    dFld_dF=(field(F+1e-6,0.0)-field(F-1e-6,0.0))/(2e-6)
    dnr=dFld_dF*Fp
    dnt,dnp=grad_ang(fld)
    grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*sinth**2)
    sqrtg=np.exp(phd)*r**2*sinth
    e2phi=np.exp(2*phd)
    # L2 weight density (coeff of (1/2) sdot^2): xi*e^{2phi}|Tang|^2
    w2=e2phi*np.sum(dFld_ds*dFld_ds,axis=-1)
    # L4 weight: kappa*e^{2phi}*[ grr|dFld_ds x dnr|^2 + gtt|x dnt|^2 + gpp|x dnp|^2 ]
    cxr=np.cross(dFld_ds,dnr); cxt=np.cross(dFld_ds,dnt); cxp=np.cross(dFld_ds,dnp)
    w4=e2phi*( grr*np.sum(cxr*cxr,axis=-1)+gtt*np.sum(cxt*cxt,axis=-1)+gpp*np.sum(cxp*cxp,axis=-1) )
    return sphere_int((w2+w4)*sqrtg)
