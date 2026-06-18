"""
Clean Rayleigh-quotient evaluator. Given a tangent mode field delta(r,th,ph) (a
3-vector field, tangent to nhat at each point), compute
   omega^2[delta] = delta^2 S[delta] / delta^2 T[delta]
where delta^2 S = (1/2) d^2/deps^2 INT (L2+L4) density sqrt(g) dr dOmega at
n(eps)=normalize(nhat + eps delta), and delta^2 T = (1/2) d^2/deps^2 of the
time-kinetic energy (g^{tt}=-e^{2phi}). Fully numeric, exact action.

Background: corpus candidate-A field, normalized -> genuinely unit nhat0.
Profile F(r) from corpus solve_bvp (the E0=45.6 soliton).

This lets us evaluate omega^2 for ANALYTIC symmetry modes (translation, isorotation)
to identify Goldstones, and for trial modes to bound the spectrum variationally.
"""
import numpy as np, sys
sys.path.insert(0,'.')
import bg

class Grid:
    def __init__(self, p, R=18.0, r_core=0.05, Nr=200, Nth=200, Nph=48, r_int=1.0):
        self.p=p; self.r_int=r_int
        sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
        self.sol=sol
        self.r=np.linspace(r_core+1e-3, r_core+R-1e-3, Nr)
        self.dr=self.r[1]-self.r[0]
        th=np.linspace(1e-3,np.pi-1e-3,Nth); self.dth=th[1]-th[0]
        ph=np.linspace(0,2*np.pi,Nph,endpoint=False); self.dph=2*np.pi/Nph
        self.TH,self.PH=np.meshgrid(th,ph,indexing='ij')
        self.sinth=np.sin(self.TH); self.costh=np.cos(self.TH)
        self.cosP=np.cos(self.PH); self.sinP=np.sin(self.PH)
        self.F=sol.sol(self.r)[0]; self.Fp=sol.sol(self.r)[1]
        self.phi=p*np.log(self.r/r_int)
    def nhat(self,Fval):
        a=np.sin(Fval)*self.sinth*self.cosP; b=np.sin(Fval)*self.sinth*self.sinP; c=np.cos(Fval)*np.ones_like(self.TH)
        v=np.stack([a,b,c],axis=-1); return v/np.linalg.norm(v,axis=-1,keepdims=True)

def angderiv(arr,dth,dph):
    dnt=np.zeros_like(arr)
    dnt[1:-1]=(arr[2:]-arr[:-2])/(2*dth); dnt[0]=(arr[1]-arr[0])/dth; dnt[-1]=(arr[-1]-arr[-2])/dth
    dnp=(np.roll(arr,-1,axis=1)-np.roll(arr,1,axis=1))/(2*dph)
    return dnt,dnp

def action_S(G, fieldfunc):
    """INT (L2+L4)*sqrtg over all r,th,ph. fieldfunc(i)->(Nth,Nph,3) field at r index i,
    plus must provide dn/dr. We pass fieldfunc that returns field on a 3-pt r stencil."""
    pass

def second_variation(G, delta_func, eps=1e-4):
    """delta_func(i) returns delta (Nth,Nph,3) tangent field at radial index i.
    Compute S(eps),S(0),S(-eps) and T similarly; return (d2S, d2T)."""
    def build_field(sign):
        flds=[]
        for i in range(len(G.r)):
            n0=G.nhat(G.F[i])
            d=delta_func(i)
            w=n0+sign*eps*d
            flds.append(w/np.linalg.norm(w,axis=-1,keepdims=True))
        return np.array(flds)   # (Nr,Nth,Nph,3)
    def S_of(flds):
        Etot=0.0
        dens=np.zeros(len(G.r))
        for i in range(len(G.r)):
            r=G.r[i]; phd=G.phi[i]
            fld=flds[i]
            # dn/dr central
            if i==0: dnr=(flds[1]-flds[0])/G.dr
            elif i==len(G.r)-1: dnr=(flds[-1]-flds[-2])/G.dr
            else: dnr=(flds[i+1]-flds[i-1])/(2*G.dr)
            dnt,dnp=angderiv(fld,G.dth,G.dph)
            grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*G.sinth**2)
            g2=grr*np.sum(dnr*dnr,-1)+gtt*np.sum(dnt*dnt,-1)+gpp*np.sum(dnp*dnp,-1)
            e2=0.5*g2
            Srt=np.cross(dnr,dnt); Srp=np.cross(dnr,dnp); Stp=np.cross(dnt,dnp)
            L4s=2*(grr*gtt*np.sum(Srt*Srt,-1)+grr*gpp*np.sum(Srp*Srp,-1)+gtt*gpp*np.sum(Stp*Stp,-1))
            e4=0.25*L4s
            sqrtg=np.exp(phd)*r**2*G.sinth
            dens[i]=np.sum((e2+e4)*sqrtg)*G.dth*G.dph
        return np.trapezoid(dens,G.r)
    fp=build_field(+1); fm=build_field(-1); f0=build_field(0)
    Sp=S_of(fp); Sm=S_of(fm); S0=S_of(f0)
    d2S=(Sp-2*S0+Sm)/(eps**2)   # = d^2S/deps^2 (this is 2*delta^2 S; ratio cancels factor)
    # time-kinetic: T = (1/2) INT [ xi e^{2phi}|dn/dt|^2 + kappa e^{2phi} g^{jj}|dn/dt x dn/dx^j|^2 ] sqrtg
    # with dn/dt = eps_dot * delta_tangent. Coeff of (1/2)epsdot^2:
    def T_weight():
        dens=np.zeros(len(G.r))
        for i in range(len(G.r)):
            r=G.r[i]; phd=G.phi[i]
            n0=G.nhat(G.F[i]); d=delta_func(i)
            # tangent component of d (project, since normalize keeps tangent part)
            dt=d-np.sum(d*n0,axis=-1,keepdims=True)*n0
            # spatial derivs of background n0
            if i==0: dnr=(G.nhat(G.F[1])-G.nhat(G.F[0]))/G.dr
            elif i==len(G.r)-1: dnr=(G.nhat(G.F[-1])-G.nhat(G.F[-2]))/G.dr
            else: dnr=(G.nhat(G.F[i+1])-G.nhat(G.F[i-1]))/(2*G.dr)
            dnt_,dnp_=angderiv(n0,G.dth,G.dph)
            grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*G.sinth**2); e2phi=np.exp(2*phd)
            w2=e2phi*np.sum(dt*dt,-1)
            cxr=np.cross(dt,dnr); cxt=np.cross(dt,dnt_); cxp=np.cross(dt,dnp_)
            w4=e2phi*(grr*np.sum(cxr*cxr,-1)+gtt*np.sum(cxt*cxt,-1)+gpp*np.sum(cxp*cxp,-1))
            sqrtg=np.exp(phd)*r**2*G.sinth
            dens[i]=np.sum((w2+w4)*sqrtg)*G.dth*G.dph
        return np.trapezoid(dens,G.r)
    d2T=2*T_weight()   # T = (1/2) w epsdot^2 -> d^2T/depsdot^2 = w; we returned weight; match factor with d2S (both are d^2/d.^2)
    return d2S, d2T

if __name__=='__main__':
    G=Grid(0, Nr=160, Nth=160, Nph=24)
    # --- analytic translational zero mode along z: delta = -d n0/dz ---
    # n0 unit field; translation x->x+a z : delta n = -(partial_z) n0(x).
    # partial_z in spherical: dz = cos th d_r - sin th /r d_th.
    def transl_z(i):
        r=G.r[i]
        n0=G.nhat(G.F[i])
        # d n0/dr (background varies via F)
        if i==0: dnr=(G.nhat(G.F[1])-G.nhat(G.F[0]))/G.dr
        elif i==len(G.r)-1: dnr=(G.nhat(G.F[-1])-G.nhat(G.F[-2]))/G.dr
        else: dnr=(G.nhat(G.F[i+1])-G.nhat(G.F[i-1]))/(2*G.dr)
        dnt,_=angderiv(n0,G.dth,G.dph)
        dz = G.costh[...,None]*dnr - (G.sinth[...,None]/r)*dnt
        d=-dz
        # project tangent
        return d-np.sum(d*n0,axis=-1,keepdims=True)*n0
    d2S,d2T=second_variation(G,transl_z)
    print(f"translational(z) mode: d2S={d2S:.4f}, d2T={d2T:.4f}, omega^2={d2S/d2T:.6f}")
    # iso-rotation about target z-axis: delta = dn0/d(chi) = z_hat x n0
    def isorot_z(i):
        n0=G.nhat(G.F[i])
        zhat=np.array([0,0,1.0])
        d=np.cross(zhat[None,None,:]*np.ones_like(n0), n0)
        return d-np.sum(d*n0,axis=-1,keepdims=True)*n0
    d2S,d2T=second_variation(G,isorot_z)
    print(f"iso-rotation(z) mode:  d2S={d2S:.4f}, d2T={d2T:.4f}, omega^2={d2S/d2T:.6f}")
