import numpy as np

# CLAIM (VR 29.1, CG 18.6): 8 tensor operators on the l=1 subspace of S^2 --
# 3 from rank-1 (vector/rotations) and 5 from rank-2 (traceless symmetric tensor) --
# close as su(3), with Casimir C_2 = (4/3) I_3 (fundamental of SU(3)).
# The l=1 subspace is 3-dimensional (m = -1,0,+1).

# Rank-1 operators on l=1: these are just the SO(3) angular momentum generators Jx,Jy,Jz
# in the spin-1 (l=1) representation -> 3x3 matrices. These are anti-Hermitian gens of so(3).
# Spin-1 matrices:
Jz = np.diag([1,0,-1]).astype(complex)
Jp = np.array([[0,np.sqrt(2),0],[0,0,np.sqrt(2)],[0,0,0]],dtype=complex) # raising
Jm = Jp.conj().T
Jx = (Jp+Jm)/2
Jy = (Jp-Jm)/(2j)

# Rank-2 operators on l=1: the 5 components of the traceless symmetric rank-2 tensor
# built from J. Standard quadrupole operators T^2_q. Build the 5 independent
# symmetric traceless bilinears in {Jx,Jy,Jz}:
def sym(A,B): return (A@B+B@A)/2
I3 = np.eye(3,dtype=complex)
J2 = Jx@Jx+Jy@Jy+Jz@Jz
# traceless symmetric quadratic forms:
Q0 = (3*Jz@Jz - J2)            # 3Jz^2 - J^2  (m=0)
Q1 = sym(Jx,Jz)               # 
Q2 = sym(Jy,Jz)
Q3 = (Jx@Jx - Jy@Jy)
Q4 = sym(Jx,Jy)
rank2 = [Q0,Q1,Q2,Q3,Q4]
rank1 = [Jx,Jy,Jz]

ops = rank1 + rank2
print("Num ops:", len(ops))

# To check su(3): the 8 Gell-Mann generators are Hermitian and TRACELESS.
# Jx,Jy,Jz here are Hermitian, traceless. Good.
# Q's: Hermitian? traceless?
for i,O in enumerate(ops):
    herm = np.allclose(O,O.conj().T)
    tr = np.trace(O)
    print(f"op{i}: Hermitian={herm}, trace={tr:.3f}")
