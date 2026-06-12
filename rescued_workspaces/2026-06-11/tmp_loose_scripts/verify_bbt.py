# Verify B B^T = N * P_traceless for the commutator map on Lambda^2 End(H), gl(N)
import numpy as np
from itertools import combinations

for N in (2,3,4,5):
    n2 = N*N
    # basis of End(H): elementary matrices E_ij, orthonormal under <A,B>=Tr(A^T B)
    E = []
    for i in range(N):
        for j in range(N):
            m = np.zeros((N,N)); m[i,j]=1; E.append(m)
    # Lambda^2 basis: (Ea^Eb), a<b ; commutator map B: Ea^Eb -> [Ea,Eb]
    pairs = list(combinations(range(n2),2))
    Bmat = np.zeros((n2, len(pairs)))
    for k,(a,b) in enumerate(pairs):
        c = E[a]@E[b] - E[b]@E[a]
        Bmat[:,k] = c.flatten()
    BBT = Bmat @ Bmat.T
    # P_traceless on End(H): identity minus trace projector
    I9 = np.eye(n2)
    idvec = np.eye(N).flatten()/np.sqrt(N)
    Ptr = np.outer(idvec, idvec)
    Ptl = I9 - Ptr
    diff = np.abs(BBT - N*Ptl).max()
    print(f"N={N}: max|BB^T - N*P_traceless| = {diff:.2e}")
