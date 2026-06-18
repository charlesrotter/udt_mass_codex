"""
Self-consistent UNIT-field soliton: minimize the EXACT 3D (L2+L4) energy of
nhat=normalize(A) over the radial profile F(r) on a grid, with F(r_core)=pi,
F(seal)=0. Energy and gradient computed by the SAME numeric sphere-integration used
in the Hessian engine, so the minimizer is a true stationary point of the discretized
action -> translation is a numeric zero mode.
"""
import numpy as np
from scipy.optimize import minimize

def make_energy(p, rgrid, Nth=160, Nph=24, r_int=1.0):
    ths=np.linspace(1e-3,np.pi-1e-3,Nth); dth=ths[1]-ths[0]
    phs=np.linspace(0,2*np.pi,Nph,endpoint=False); dph=2*np.pi/Nph
    TH,PH=np.meshgrid(ths,phs,indexing='ij'); sinth=np.sin(TH)
    phi=p*np.log(rgrid/r_int)
    dr=rgrid[1]-rgrid[0]
    cosP=np.cos(PH); sinP=np.sin(PH)
    def nhat(F):
        a=np.sin(F)*sinth*cosP; b=np.sin(F)*sinth*sinP; c=np.cos(F)*np.ones_like(TH)
        v=np.stack([a,b,c],axis=-1); return v/np.linalg.norm(v,axis=-1,keepdims=True)
    def energy_density_r(Farr):
        # Farr on rgrid; returns total energy (sum over r of density*dr)
        N=len(rgrid)
        # precompute fields and dF/dr
        flds=np.array([nhat(Farr[i]) for i in range(N)])  # (N,Nth,Nph,3)
        dFr=np.gradient(Farr,rgrid)
        E=0.0
        dens=np.zeros(N)
        for i in range(N):
            F=Farr[i]; Fp=dFr[i]; phd=phi[i]; r=rgrid[i]
            fld=flds[i]
            hF=1e-6
            dn_dF=(nhat(F+hF)-nhat(F-hF))/(2*hF)
            dnr=dn_dF*Fp
            # angular derivs
            dnt=np.zeros_like(fld);
            dnt[1:-1]=(fld[2:]-fld[:-2])/(2*dth); dnt[0]=(fld[1]-fld[0])/dth; dnt[-1]=(fld[-1]-fld[-2])/dth
            dnp=(np.roll(fld,-1,axis=1)-np.roll(fld,1,axis=1))/(2*dph)
            grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*sinth**2)
            g2=grr*np.sum(dnr*dnr,-1)+gtt*np.sum(dnt*dnt,-1)+gpp*np.sum(dnp*dnp,-1)
            e2=0.5*g2
            Srt=np.cross(dnr,dnt); Srp=np.cross(dnr,dnp); Stp=np.cross(dnt,dnp)
            L4s=2*(grr*gtt*np.sum(Srt*Srt,-1)+grr*gpp*np.sum(Srp*Srp,-1)+gtt*gpp*np.sum(Stp*Stp,-1))
            e4=0.25*L4s
            sqrtg=np.exp(phd)*r**2*sinth
            dens[i]=np.sum((e2+e4)*sqrtg)*dth*dph
        return np.trapezoid(dens,rgrid)
    return energy_density_r, phi

def solve_unit(p, R=18.0, r_core=0.05, Nr=120, Nth=120, Nph=16):
    rgrid=np.linspace(r_core, r_core+R, Nr)
    Efun,phi=make_energy(p,rgrid,Nth=Nth,Nph=Nph)
    # interior DOFs (fix endpoints pi and 0)
    F0=np.pi*np.exp(-(rgrid-r_core)/max(0.3,2.0/(1+p))); F0[-1]=0
    def pack(Fint):
        F=np.empty(Nr); F[0]=np.pi; F[-1]=0; F[1:-1]=Fint; return F
    def obj(Fint): return Efun(pack(Fint))
    res=minimize(obj, F0[1:-1], method='L-BFGS-B',
                 options={'maxiter':400,'ftol':1e-10,'gtol':1e-7})
    Ffull=pack(res.x)
    return rgrid, Ffull, res.fun, res

if __name__=='__main__':
    for p in (0,):
        rg,F,E,res=solve_unit(p,Nr=100,Nth=120,Nph=16)
        print(f"p={p}: unit-field E0={E:.4f}, converged={res.success}, nit={res.nit}")
        np.save(f'unitF_p{p}.npy', np.vstack([rg,F]))
