# CLAIM 3 ATTACK: hunt for hidden discreteness.
# Set up the SIMULTANEOUS core-regularity + seal-mirror-fold BVP as a self-adjoint
# Sturm-Liouville eigenproblem and check if the two BCs together quantize anything.
# Bare measure r^2 sin th; stiffness K_r=e^{-4phi}, K_th=e^{-2phi}/r^2.
import torch, math
torch.set_default_dtype(torch.float64)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'

# Build the radial operator for a perturbation/mode u(r) of the coupled system.
# Weighted SL form: -(d/dr)[ w(r) K_r(r) du/dr ] + q(r) u = E * m_w(r) u
# weight w(r) = r^2 (bare radial measure), K_r=e^{-4phi}, mass-weight m_w=r^2.
# Use a representative back-reacted phi: e^{-2phi}=1-delta-rs/r restricted on cell,
# i.e. deficit cell. The question: do core-regular + seal BC quantize E?

def build_eig(N, rc, ri, delta, rs, bc_seal='neumann', bc_core='neumann'):
    r = torch.linspace(rc, ri, N, device=dev)
    h = (ri-rc)/(N-1)
    em2 = 1 - delta - rs/r          # e^{-2phi}
    em2 = torch.clamp(em2, min=1e-12)
    Kr = em2**2                      # e^{-4phi} = (e^{-2phi})^2
    w  = r**2                        # bare radial measure
    mw = r**2                        # mass weight (bare)
    # operator A u = -(1/mw) d/dr[ w Kr u' ]  ; symmetric in <u,v>_mw
    # finite-volume / staggered for self-adjointness
    rm = 0.5*(r[:-1]+r[1:])
    em2m = 1 - delta - rs/rm
    em2m = torch.clamp(em2m, min=1e-12)
    Krm = em2m**2
    wm  = rm**2
    coef = wm*Krm/h**2               # face coefficients, length N-1
    A = torch.zeros(N, N, device=dev)
    for i in range(N):
        if i>0:
            A[i,i-1] -= coef[i-1]
            A[i,i]   += coef[i-1]
        if i<N-1:
            A[i,i+1] -= coef[i]
            A[i,i]   += coef[i]
    # divide rows by mass weight to get generalized -> use generalized eig instead
    M = torch.diag(mw)
    # BCs: core regular turning point => Neumann (du=0) is natural (already in FV).
    # Dirichlet => pin endpoint. seal mirror-fold: sigma-even=Neumann, sigma-odd=Dirichlet.
    def apply(bc, idx):
        if bc=='dirichlet':
            A[idx,:]=0; M[idx,:]=0
            A[idx,idx]=1.0; M[idx,idx]=1e-12  # push out
    apply(bc_core,0); apply(bc_seal,N-1)
    # generalized symmetric eig A v = E M v
    Minv_sqrt = torch.diag(mw.clamp(min=1e-30)**-0.5)
    C = Minv_sqrt @ A @ Minv_sqrt
    C = 0.5*(C+C.T)
    evals = torch.linalg.eigvalsh(C)
    return evals.cpu().numpy()

# The real test: does the SPECTRUM (set of allowed E) depend discretely on (delta,p,size)
# in a way that PINS them? An eigenproblem ALWAYS has a discrete spectrum on a bounded
# domain (that's trivial). The study's claim is that the PARAMETERS (p,delta,r_int) are
# NOT quantized -- you can dial them continuously. Test: vary delta continuously, watch
# lowest few eigenvalues move CONTINUOUSLY (no forbidden gaps / no selection).
import numpy as np
print("=== Mode spectrum vs continuous parameter delta (Neumann core + Neumann seal) ===")
for delta in [0.001,0.01,0.05,0.1,0.2]:
    ev = build_eig(400, 1e-3, 1.0, delta, 0.0, 'neumann','neumann')
    print(f" delta={delta:6.3f}  lowest 5 eig: {np.array2string(ev[:5], precision=5)}")
print()
print("=== vs cell size r_int (continuous) ===")
for ri in [0.5,1.0,2.0,5.0,10.0]:
    ev = build_eig(400, 1e-3, ri, 0.05, 0.0, 'neumann','neumann')
    print(f" r_int={ri:5.2f}  lowest 5 eig: {np.array2string(ev[:5], precision=5)}")
print()
print("=== Dirichlet core + Neumann seal (mixed parity) ===")
for delta in [0.01,0.05,0.1]:
    ev = build_eig(400, 1e-3, 1.0, delta, 0.0, 'neumann','dirichlet')
    print(f" delta={delta:5.3f}  lowest 5 eig: {np.array2string(ev[:5], precision=5)}")
