import numpy as np
from numpy import pi as PI, exp, sqrt
from scipy.linalg import solve_banded

MU2=PI/3; MU=sqrt(MU2)
RMAX=16.0; NG=4000; r0=1e-6
rg=np.linspace(r0,RMAX,NG); dr=rg[1]-rg[0]

def solve_radial(source_l,l,screened,em2=None):
    w = em2 if (screened and em2 is not None) else np.ones_like(rg)
    N=NG; ab=np.zeros((3,N)); b=-source_l*rg**2*dr*dr
    rh=rg+dr/2; wh=np.interp(rh,rg,w)
    A=rh**2*wh
    for i in range(1,N-1):
        lo=A[i-1]; hi=A[i]
        diagc=-(lo+hi)-(l*(l+1)+(MU2*rg[i]**2 if screened else 0.0))*dr*dr
        ab[0,i+1]=hi; ab[1,i]=diagc; ab[2,i-1]=lo
    if l==0: ab[1,0]=-1.0; ab[0,1]=1.0; b[0]=0.0
    else: ab[1,0]=1.0; ab[0,1]=0.0; b[0]=0.0
    if screened: ab[1,N-1]=1.0; ab[2,N-2]=0.0; b[N-1]=0.0
    else: ab[1,N-1]=1.0+(l+1)*dr/rg[N-1]; ab[2,N-2]=-1.0; b[N-1]=0.0
    return solve_banded((1,1),ab,b)

# Test operator: what does solve_radial actually solve? 
# The discretization: (1/r^2 dr^2)[ A_{i}(R_{i+1}-R_i) - A_{i-1}(R_i-R_{i-1}) ] - (l(l+1)/r^2 + mu^2 scr) R = ?
# multiplied by r^2 dr^2: A_i(R+1 -R) - A_{i-1}(R-R-1) - (l(l+1)+mu2 r^2)R = -source*r^2 dr^2 ... 
# Wait b = -source*r^2*dr^2 and LHS row = ab. So system: LHS_matrix @ R = b = -source r^2 dr^2.
# LHS = A_i R_{i+1} + diagc R_i + A_{i-1}R_{i-1}, diagc=-(A_i+A_{i-1})-(l(l+1)+mu2 r^2).
# = [discrete (r^2 w R')'] - (l(l+1)+mu2 r^2) R.  Set equal to -source r^2 dr^2.
# Divide by r^2 dr^2: (1/r^2)(r^2 w R')' - l(l+1)/r^2 R - mu2 R = -source.
# So solve_radial solves: L[R] = -source_l, where L=(lap_l - mu2).
# For screened gaussian test, script calls solve_radial(-rho0,...) => -source = -(-rho0)=+rho0.
# So L[R]=+rho0 => (lap-mu2)R = +rho0. Green: (lap-mu2)G=-delta => R = -Yukawa*rho0 <0. CONFIRMS negative.
sig=0.3; gauss=np.exp(-rg**2/(2*sig**2)); gauss/=np.trapz(gauss*rg**2*4*PI,rg)
rho0=gauss*sqrt(4*PI)
D0=solve_radial(-rho0,0,True,em2=np.ones_like(rg))
ic=np.argmin(abs(rg-5.0))
print("dphi(5)=",D0[ic]/sqrt(4*PI),"Yukawa=",np.exp(-MU*5)/(4*PI*5))
print("So solve_radial(-rho) gives (lap-mu2)R=+rho -> R=-Yukawa. The MINUS source flips it.")

# Is the 4.7% from gaussian form factor? Smeared Yukawa for gaussian source:
# convolution of gaussian(sig) with Yukawa. At r=5, sig=0.3 -> form factor exp(mu^2 sig^2/2)*... 
# Effective: point-Yukawa * exp(mu^2 sig^2 /2) (standard screened smearing enhancement)
ff=np.exp(MU2*0.3**2/2)
print("gaussian-smeared Yukawa enhancement factor exp(mu2 sig2/2)=",ff)
print("predicted |dphi|=",np.exp(-MU*5)/(4*PI*5)*ff, " vs solver |dphi|=",abs(D0[ic]/sqrt(4*PI)))
