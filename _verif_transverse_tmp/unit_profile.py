"""
PATH 2 (genuinely-unit, self-consistent). Background = the TRUE unit degree-1
hedgehog. We must pick a unit field whose energy we then extremize.

The genuinely-unit degree-1 hedgehog (standard O(3) sigma model in 3D, 'monopole'
texture) that is SMOOTH and covers the target once is:
    n0 = ( sin G(r) * cos(theta)? ) ...
We use the WIDELY-USED unit hedgehog where the target unit vector is obtained by
rotating zhat by spatial colatitude theta about the spatial azimuth, then twisting
radially. The clean unit closed form with |grad|^2 = G'^2 + (1+sin^2 ...)/r^2 ...

To avoid ansatz disputes we use the manifestly-unit field
    n0(r,theta,phi) = ( sin Theta(r) sin theta cos phi,
                        sin Theta(r) sin theta sin phi,
                        cos Theta(r) ) / N,   N = sqrt(sin^2Theta sin^2theta + cos^2Theta)
i.e. normalize candidate A. This IS unit by construction. We build its EXACT 3D
reduced energy E[Theta] = INT over sphere of (L2+L4 density)*sqrt(g), reduce to a
1D functional of Theta(r) (it depends on Theta, Theta', r, phi only after sphere
integration), derive its EOM, solve, get the self-consistent profile + energy.
All numeric (sphere integral done on a theta-grid; phi integrates trivially by
symmetry? NO -- after normalization phi-dependence integrates out by symmetry in
modulus, check).
"""
import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.optimize import brentq

# Build reduced energy density per dr as a function of (Theta, Thetap, phi_dil, r)
# by numerically integrating the exact 3D (L2+L4) density of normalize(A) over the sphere.
def nhat(F, th, ph):
    v = np.array([np.sin(F)*np.sin(th)*np.cos(ph),
                  np.sin(F)*np.sin(th)*np.sin(ph),
                  np.cos(F)])
    return v/np.linalg.norm(v)

def cross(a,b): return np.cross(a,b)

def densities_at(F, Fp, phd, r, th, ph, h=1e-6):
    # derivatives of nhat wrt r (via F only), th, ph
    dF = (nhat(F+h,th,ph)-nhat(F-h,th,ph))/(2*h)
    dnr = dF*Fp
    dnt = (nhat(F,th+h,ph)-nhat(F,th-h,ph))/(2*h)
    dnp = (nhat(F,th,ph+h)-nhat(F,th,ph-h))/(2*h)
    grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*np.sin(th)**2)
    # L2
    grad2 = grr*dnr.dot(dnr)+gtt*dnt.dot(dnt)+gpp*dnp.dot(dnp)
    e2 = 0.5*grad2
    # L4: (1/4) sum 2 g^mm g^nn |S_mn|^2, S = dn x dn
    Srt=cross(dnr,dnt); Srp=cross(dnr,dnp); Stp=cross(dnt,dnp)
    L4s = 2*(grr*gtt*Srt.dot(Srt) + grr*gpp*Srp.dot(Srp) + gtt*gpp*Stp.dot(Stp))
    e4 = 0.25*L4s
    sqrtg = np.exp(phd)*r**2*np.sin(th)
    return (e2+e4)*sqrtg

def reduced_density(F, Fp, phd, r, Nth=200, Nph=16):
    ths=np.linspace(1e-4,np.pi-1e-4,Nth); dth=ths[1]-ths[0]
    phs=np.linspace(0,2*np.pi,Nph,endpoint=False); dph=2*np.pi/Nph
    tot=0.0
    for th in ths:
        for ph in phs:
            tot+=densities_at(F,Fp,phd,r,th,ph)
    return tot*dth*dph

if __name__=='__main__':
    # quick sanity: at phi=0, r=1, F=1, F'=0.5
    print("reduced density sample:", reduced_density(1.0,0.5,0.0,1.0))
    # check phi-independence (symmetry): compare Nph=16 vs sampling
    print("(this is the self-consistent UNIT-field reduced functional)")
