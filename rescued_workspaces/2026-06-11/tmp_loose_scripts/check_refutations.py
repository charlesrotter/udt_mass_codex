import sympy as sp, numpy as np
# (1) Does the canonical scalar's T_{tr} vanish for a static field?  T_{tr}=d_t phi d_r phi - g_tr L
t,r=sp.symbols('t r'); phi=sp.Function('phi')
# static: phi=phi(r) only
phi_static=phi(r)
T_tr_static = sp.diff(phi_static,t)*sp.diff(phi_static,r)
print("scalar T_tr (static, d_t phi=0):", T_tr_static)  # expect 0
# (2) phase: chi from unscreened Poisson vs delta_phi from screened KG, both sourced by drho~cos(qr); check both are cos-phase -> dr(chi) is sin (quadrature) for BOTH
N=4000; L=20*np.pi; x=np.linspace(0,L,N); dx=x[1]-x[0]
def solve_screened(drho,mu2):
    # (d2/dx2 - mu2) f = drho  with Dirichlet; build tridiag
    import numpy as np
    A=np.zeros((N,N))
    for i in range(1,N-1):
        A[i,i-1]=1/dx**2; A[i,i]=-2/dx**2-mu2; A[i,i+1]=1/dx**2
    A[0,0]=1; A[-1,-1]=1
    b=drho.copy(); b[0]=0; b[-1]=0
    return np.linalg.solve(A,b)
for q in [20,100,300,700]:
    qq=q/700*3  # arbitrary scaling into grid; just need a mode
    drho=np.cos(qq*x)
    chi=solve_screened(drho,0.0)        # unscreened Poisson (transport potential)
    dphi=solve_screened(drho,0.5)       # screened KG (metric scalar), mu2=0.5
    # radial derivative of chi (the h_tr carrier)
    dchi=np.gradient(chi,dx)
    # phase of dchi relative to dphi: project onto cos/sin of dphi's argument
    # measure phase offset between dchi and dphi via FFT peak
    def phase(sig):
        s=sig[N//4:3*N//4]; F=np.fft.rfft(s); k=np.argmax(np.abs(F[1:]))+1; return np.angle(F[k])
    off=np.degrees(phase(dchi)-phase(dphi))
    off=(off+180)%360-180
    print(f"q={q}: phase(d_r chi) - phase(delta_phi) = {off:.1f} deg (expect ~90 quadrature)")
