import numpy as np
import sys
sys.path.insert(0,'.')
from engine2 import build_channel
from scipy.linalg import eigh
import bg  # background solver (bg.solve_profile, has f_Tpp)

def get_profile(p,R,r_core=0.05,r_int=1.0):
    sol=bg.solve_profile(p,r_core=r_core,R=R,r_int=r_int)
    def F(r): return float(sol.sol(np.atleast_1d(r))[0][0])
    def Fp(r): return float(sol.sol(np.atleast_1d(r))[1][0])
    def phi(r): return p*np.log(r/r_int)
    return F,Fp,phi,sol

def assemble_and_solve(Pr,Qr,Rr,Wr,rgrid, bc='dirichlet'):
    """Build self-adjoint radial operator -(d/dr)(P psi') + Veff psi = omega^2 W psi.
    Veff = Q - (1/2) dR/dr (symmetrizing the R psi psi' term). Discretize on rgrid
    with finite differences; eigensolve generalized symmetric problem."""
    N=len(rgrid); dr=rgrid[1]-rgrid[0]
    # build matrix for INT [P psi'^2 + Q psi^2 + R psi psi'] dr as (1/2) psi^T H psi?
    # Quadratic functional Phi[psi]=INT P psi'^2 + Q psi^2 + R psi psi' dr.
    # Weight functional  Om[psi]=INT W psi^2 dr.
    # delta^2 S = Phi (our alpha,beta,gamma already are coeffs of s^2,sp^2,s sp with s=eps psi).
    # Build H (stiffness) and M (mass) as symmetric matrices via FD.
    # psi' via central differences; assemble weak form.
    H=np.zeros((N,N)); M=np.zeros((N,N))
    # use trapezoidal weights
    w=np.full(N,dr); w[0]*=0.5; w[-1]*=0.5
    # first-derivative operator D (central, one-sided at ends)
    D=np.zeros((N,N))
    for i in range(N):
        if i==0: D[i,0]=-1/dr; D[i,1]=1/dr
        elif i==N-1: D[i,-1]=1/dr; D[i,-2]=-1/dr
        else: D[i,i+1]=1/(2*dr); D[i,i-1]=-1/(2*dr)
    # Phi = sum_i w_i [ P_i (Dpsi)_i^2 + Q_i psi_i^2 + R_i psi_i (Dpsi)_i ]
    WP=np.diag(w*Pr); WQ=np.diag(w*Qr); WR=np.diag(w*Rr)
    H = D.T@WP@D + WQ + 0.5*(D.T@WR + WR@D)
    M = np.diag(w*Wr)
    H=0.5*(H+H.T); M=0.5*(M+M.T)
    # Dirichlet BC: psi=0 at both ends (drop endpoints)
    if bc=='dirichlet':
        idx=np.arange(1,N-1)
    elif bc=='neumann-core':  # free at core, dirichlet at seal
        idx=np.arange(0,N-1)
    else:
        idx=np.arange(N)
    Hs=H[np.ix_(idx,idx)]; Ms=M[np.ix_(idx,idx)]
    # regularize M positive
    Ms=Ms+1e-14*np.eye(len(idx))
    evals,evecs=eigh(Hs,Ms)
    return evals,evecs,idx

if __name__=='__main__':
    p=0; R=18.0; r_core=0.05
    F,Fp,phi,sol=get_profile(p,R)
    print(f"profile p={p} R={R} solved, success={sol.success}")
    # radial grid for operator (coarser than bg mesh)
    Nr=160
    rgrid=np.linspace(r_core+1e-3, r_core+R-1e-3, Nr)
    # ---- l=0 breathing: angular factors f=1 (polar), g=0 ----
    fang=lambda T,P: np.ones_like(T)
    gang=lambda T,P: np.zeros_like(T)
    Pr,Qr,Rr,Wr,_=build_channel(F,Fp,phi,fang,gang,rgrid,Nth=120,Nph=8)
    ev,_,_=assemble_and_solve(Pr,Qr,Rr,Wr,rgrid)
    print("l=0 (polar f=1) lowest 6 omega^2:", np.round(ev[:6],5))
